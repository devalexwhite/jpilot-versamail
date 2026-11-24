"""VersaMail 2.6.1 J-Pilot conduit and account editor."""
import base64
import hashlib
import imaplib
import json
import os
import smtplib
import sqlite3
import ssl
import struct
import sys
import time
from datetime import date, timedelta
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import formatdate, getaddresses, parsedate_to_datetime
from html.parser import HTMLParser

# String preference IDs for account slot zero. Slots have a stride of 19.
FIELDS = dict(name=16, username=17, email=11, incoming=15, outgoing=10,
              display=12, reply=20, signature=13)
DEFAULT = dict.fromkeys(FIELDS, '') | dict(port=993, smtp_port=25, limit=5, tls=True)
DEFAULT_FETCH_DAYS = 7
HEADER = struct.Struct('>IIHHHBBHBBI')


def rpc(*args):
    print(*args, flush=True)
    line = sys.stdin.readline()
    if not line or line.startswith('error '):
        raise RuntimeError(f'Palm {args[0]} failed ({line.strip()})')
    return line.rstrip('\n')


def pref(key):
    value = rpc('pref', key)
    return None if value == 'missing' else base64.b64decode(value, validate=True)


def put(key, data):
    rpc('set', key, base64.b64encode(data).decode())


def account(slot):
    block = pref(slot)
    if block is None or len(block) != 180:
        raise ValueError('Unknown VersaMail account preferences')
    name = pref(FIELDS['name'] + 19 * slot)
    if not name or not name.rstrip(b'\0'):
        return block, {}
    if block[:2] != b'\0\1':
        return block, {'other': True}
    a = {}
    for field, key in FIELDS.items():
        data = name if field == 'name' else pref(key + 19 * slot)
        a[field] = (data or b'').split(b'\0')[0].decode('cp1252', 'replace')
    a.update(port=int.from_bytes(block[4:6]), limit=int.from_bytes(block[6:8]),
             smtp_port=int.from_bytes(block[32:34]), tls=bool(block[30]))
    return block, a


def reconcile(slot, block, remote, base, local):
    if local == base:
        return remote
    if any(remote.get(k) not in (base.get(k), local.get(k))
           for k in base.keys() | remote.keys() | local.keys()):
        raise ValueError('Account changed on both devices. Revert the desktop edit and sync.')
    if remote == local:
        return local
    changed = bytearray(block)
    if local:
        changed[:2] = b'\0\1'
        for offset, key in [(4, 'port'), (6, 'limit'), (32, 'smtp_port')]:
            struct.pack_into('>H', changed, offset, local[key])
        changed[30] = int(local['tls'])
    if not local or not base:
        # Passwords and alternate SMTP credentials belong to the old account.
        for key in (18 + 19*slot, 350 + slot, 400 + slot, 410 + slot):
            if pref(key):
                put(key, b'\0')
    if changed != block:
        put(slot, bytes(changed))
    for field in [k for k in FIELDS if k != 'name'] + ['name']:
        if local.get(field, '') != remote.get(field, ''):
            put(FIELDS[field] + 19 * slot, local.get(field, '').encode('cp1252') + b'\0')
    return local


class PlainHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'head'):
            self.hidden += 1
        if tag in ('br', 'p', 'div', 'li', 'tr') and not self.hidden:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'head') and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def incoming_record(raw, slot, uid, marker, limit):
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    part = msg.get_body(preferencelist=('plain', 'html'))
    body = part.get_content() if part else ''
    if part and part.get_content_type() == 'text/html':
        html = PlainHTML()
        html.feed(body)
        html.close()
        body = ''.join(html.parts).strip()
    date = msg.get('Date', '')
    try:
        timestamp = parsedate_to_datetime(str(date)).timestamp()
    except (ValueError, TypeError, OverflowError):
        timestamp = time.time()
    values = [marker, msg.get('To'), msg.get('From'), msg.get('Cc'), msg.get('Bcc'),
              msg.get('Subject'), date, body, msg.get('Reply-To')]
    fields = [str(v or '').replace('\x00', '').replace('\r\n', '\n').encode('cp1252', 'replace')
              for v in values]
    fields = [v[:1800] if i != 7 else v[:min(limit * 1024, 47000)] for i, v in enumerate(fields)]
    payload = b'\0'.join(fields) + b'\0'
    return HEADER.pack(uid, max(0, min(0xffffffff, int(timestamp)+2082844800)), slot,
                       slot+1, 0, 0, 2, 0, 0, 0, len(raw)) + payload


def records():
    result = []
    for index in range(int(rpc('count'))):
        uid, attr, cat, data = rpc('record', index).split(' ', 3)
        if int(attr) & 0x88:  # archived or deleted
            continue
        raw = base64.b64decode(data)
        if len(raw) < HEADER.size:
            raise ValueError('Short message record')
        result.append((int(uid), int(attr), int(cat), raw))
    return result


def write(uid, attr, cat, raw):
    rpc('write', uid, attr, cat, base64.b64encode(raw).decode())


def fetch(db, slot, a, password, rows, unread, fetch_days=DEFAULT_FETCH_DAYS):
    ctx = ssl.create_default_context()
    if a['tls'] and a['port'] != 143:
        client = imaplib.IMAP4_SSL(a['incoming'], a['port'], ssl_context=ctx, timeout=30)
    else:
        client = imaplib.IMAP4(a['incoming'], a['port'], timeout=30)
    with client:
        if a['tls'] and a['port'] == 143:
            client.starttls(ssl_context=ctx)
        client.login(a['username'], password)
        if client.select('INBOX', readonly=True)[0] != 'OK':
            raise ValueError('Cannot select INBOX')
        validity = int(client.response('UIDVALIDITY')[1][0])
        key = json.dumps([slot, a['incoming'], a['username'], validity])
        prefix = 'jp-' + hashlib.sha256(key.encode()).hexdigest()[:24] + '-'
        markers = {r[3][24:].split(b'\0', 1)[0] for r in rows}
        cutoff = date.today() - timedelta(days=fetch_days - 1)
        since = f'{cutoff.day:02d}-{imaplib.Months[cutoff.month]}-{cutoff.year:04d}'
        status, hits = client.uid('search', None, 'UNSEEN' if unread else 'ALL', 'SINCE', since)
        if status != 'OK':
            raise ValueError('IMAP search failed')
        for uid in hits[0].split():
            marker = prefix + str(int(uid))
            if db.execute('select 1 from seen where id=?', (marker,)).fetchone():
                continue
            if marker.encode() not in markers:
                status, data = client.uid('fetch', uid, '(BODY.PEEK[])')
                if status != 'OK':
                    raise ValueError('IMAP fetch failed')
                raw = next(item[1] for item in data if isinstance(item, tuple))
                write(0, 0, 0, incoming_record(raw, slot, int(uid), marker, a['limit']))
            db.execute('insert into seen values (?)', (marker,))
            db.commit()


def send(db, slot, a, password, rows, auth, bcc):
    for uid, attr, cat, raw in rows:
        header = HEADER.unpack_from(raw)
        if cat != 1 or attr & 0x20 or header[3] != slot + 1:
            continue
        fields = raw[24:].split(b'\0', 9)
        if len(fields) != 10 or fields[-1]:
            raise ValueError('Unsupported Outbox record or attachment')
        _, to, sender, cc, blind, subject, _, body, reply = [s.decode('cp1252', 'replace') for s in fields[:9]]
        msg = EmailMessage()
        msg['From'] = sender or a['email']
        msg['To'] = to
        if cc:
            msg['Cc'] = cc
        if reply:
            msg['Reply-To'] = reply
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg.set_content(body)
        key = f'{slot}/{uid}/' + hashlib.sha256(raw).hexdigest()
        state = db.execute('select state from delivery where id=?', (key,)).fetchone()
        if state == ('pending',):
            raise ValueError(f'Check SMTP delivery of Palm record {uid} before retrying')
        if not state:
            recipients = []
            for label, value in [('To', to), ('Cc', cc), ('Bcc', blind), ('account Bcc', bcc)]:
                if value.strip():
                    addresses = getaddresses([value])
                    if not addresses or any(not address for _, address in addresses):
                        raise ValueError(f'Invalid {label} address in Palm record {uid}')
                    recipients.extend(address for _, address in addresses)
            if not recipients:
                raise ValueError(f'Palm Outbox record {uid} has no recipients')
            fastmail = a['outgoing'].lower().rstrip('.') == 'smtp.fastmail.com'
            if fastmail and not auth:
                raise ValueError('Enable SMTP authentication in Manage VersaMail accounts for Fastmail')
            ctx = ssl.create_default_context()
            port = a['smtp_port']
            smtp = (smtplib.SMTP_SSL(a['outgoing'], port, context=ctx, timeout=30)
                    if port == 465 else smtplib.SMTP(a['outgoing'], port, timeout=30))
            with smtp:
                smtp.ehlo()
                if port != 465 and (auth or smtp.has_extn('starttls')):
                    smtp.starttls(context=ctx)
                    smtp.ehlo()
                if auth:
                    if fastmail:
                        smtp.user = a['username']
                        smtp.password = password
                        smtp.auth('PLAIN', smtp.auth_plain)
                    else:
                        smtp.login(a['username'], password)
                db.execute("insert into delivery values (?, 'pending')", (key,))
                db.commit()
                try:
                    refused = smtp.send_message(msg, to_addrs=recipients)
                except smtplib.SMTPRecipientsRefused as exc:
                    with db:
                        db.execute("delete from delivery where id=? and state='pending'", (key,))
                    raise ValueError(f'SMTP refused all recipients for Palm record {uid}: {exc}') from exc
                if refused:
                    raise ValueError('Partial SMTP delivery. Check the recipients before retrying.')
                db.execute("update delivery set state='sent' where id=?", (key,))
                db.commit()
        write(uid, attr, 3, raw)


def sync(db):
    rows = records()
    failures = []
    for slot in range(8):
        try:
            db.execute('begin immediate')
            block, remote = account(slot)
            saved = db.execute('select base,local,password,unread,auth,fetch_days from accounts where slot=?', (slot,)).fetchone()
            base, local, password, unread, auth, fetch_days = saved or ('{}', '{}', '', 1, 0, DEFAULT_FETCH_DAYS)
            base, local = json.loads(base), json.loads(local)
            if not base and local and any(HEADER.unpack_from(r[3])[3] == slot+1 for r in rows):
                raise ValueError('Clear the previous account’s Palm messages before reusing its slot')
            a = reconcile(slot, block, remote, base, local)
            if any(a.get(k) != local.get(k) for k in ('username', 'incoming', 'outgoing', 'tls')):
                password = ''
            if not a or a.get('other'):
                password = ''
            db.execute('replace into accounts values (?,?,?,?,?,?,?)',
                       (slot, json.dumps(a), json.dumps(a), password, unread, auth, fetch_days))
            db.commit()
            if not a or a.get('other'):
                continue
            if any(c in password for c in '\r\n\0'):
                raise ValueError('Desktop mail password contains a line break or NUL. Re-enter it in Manage VersaMail accounts.')
            if not password:
                raise ValueError('Enter the mail password in Manage VersaMail accounts')
            blind = (pref(350 + slot) or b'').rstrip(b'\0').decode('cp1252')
            try:
                send(db, slot, a, password, rows, auth, blind)
            except Exception as exc:
                failures.append(f'Slot {slot + 1} Outbox: {exc}')
            fetch(db, slot, a, password, rows, unread, fetch_days)
        except Exception as exc:
            db.rollback()
            failures.append(f'Slot {slot + 1}: {exc}')
    for message in failures:
        rpc('log', ' '.join(message.splitlines()))
    return bool(failures)


def edit(db):
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    window = Gtk.Window(title='VersaMail accounts')
    grid = Gtk.Grid(column_spacing=10, row_spacing=5, margin=12)
    window.add(grid)
    chooser = Gtk.ComboBoxText()
    grid.attach(chooser, 0, 0, 2, 1)
    entries = {}
    labels = dict(name='Account name', username='Username', email='Email address',
                  incoming='IMAP server', outgoing='SMTP server', display='Your name',
                  reply='Reply-To', signature='Signature', port='IMAP port',
                  smtp_port='SMTP port', limit='Body limit (KiB)', password='Desktop mail password')
    for row, (field, label) in enumerate(labels.items(), 1):
        grid.attach(Gtk.Label(label=label, xalign=0), 0, row, 1, 1)
        entries[field] = Gtk.Entry()
        grid.attach(entries[field], 1, row, 1, 1)
    entries['password'].set_visibility(False)
    flags = {}
    row += 1
    grid.attach(Gtk.Label(label='Fetch mail from the last (days)', xalign=0), 0, row, 1, 1)
    days = Gtk.SpinButton.new_with_range(1, 65535, 1)
    days.set_numeric(True)
    grid.attach(days, 1, row, 1, 1)
    row += 1
    for field, label in [('tls', 'IMAP over TLS'), ('unread', 'Fetch unread only'), ('auth', 'SMTP authentication')]:
        flags[field] = Gtk.CheckButton(label=label)
        grid.attach(flags[field], 0, row, 2, 1)
        row += 1
    status = Gtk.Label(xalign=0, wrap=True)
    save = Gtk.Button(label='Save account')
    delete = Gtk.Button(label='Delete account')
    grid.attach(save, 0, row, 1, 1)
    grid.attach(delete, 1, row, 1, 1)
    grid.attach(status, 0, row+1, 2, 1)
    snapshot = None

    def select(*_):
        nonlocal snapshot
        slot = chooser.get_active_id()
        if slot is None:
            return
        snapshot = db.execute('select * from accounts where slot=?', (slot,)).fetchone()
        _, _, local, pwd, unread, auth, fetch_days = snapshot
        days.set_value(fetch_days)
        values = DEFAULT | json.loads(local) | dict(password=pwd, unread=unread, auth=auth)
        for k, entry in entries.items():
            entry.set_text(str(values[k]))
        for k, button in flags.items():
            button.set_active(bool(values[k]))

    def refresh(slot=None):
        chooser.remove_all()
        for i, local in db.execute('select slot,local from accounts order by slot'):
            a = json.loads(local)
            if not a.get('other'):
                chooser.append(str(i), f"{i+1}   {a.get('name', 'Add account')}")
        if slot is None or not chooser.set_active_id(slot):
            chooser.set_active(0)
        enabled = chooser.get_active_id() is not None
        save.set_sensitive(enabled)
        delete.set_sensitive(enabled)
        if not enabled:
            status.set_text('Run HotSync to discover available Palm account slots.')

    def change(button):
        slot = chooser.get_active_id()
        try:
            a = {k: e.get_text().strip() for k, e in entries.items() if k != 'password'}
            if button == save:
                if any(c in entries['password'].get_text() for c in '\r\n\0'):
                    raise ValueError('Desktop mail password contains a line break or NUL. Re-enter it.')
                for k in ('name', 'username', 'email', 'incoming', 'outgoing'):
                    if not a[k]:
                        raise ValueError(f'Enter {labels[k]}')
                for key in ('port', 'smtp_port', 'limit'):
                    a[key] = int(a[key])
                    if not 1 <= a[key] <= 65535:
                        raise ValueError(f'Invalid {labels[key]}')
                a['tls'] = flags['tls'].get_active()
                for k in FIELDS:
                    if len(a[k].encode('cp1252')) > 255:
                        raise ValueError(f'{labels[k]} exceeds 255 bytes')
            else:
                a = {}
            with db:
                db.execute('begin immediate')
                if snapshot != db.execute('select * from accounts where slot=?', (slot,)).fetchone():
                    raise ValueError('Account changed. Reopen the editor.')
                db.execute('update accounts set local=?,password=?,unread=?,auth=?,fetch_days=? where slot=?',
                           (json.dumps(a), entries['password'].get_text() if a else '',
                            flags['unread'].get_active(), flags['auth'].get_active(),
                            days.get_value_as_int() if a else DEFAULT_FETCH_DAYS, slot))
            refresh(slot)
            status.set_text('Saved for the next HotSync.')
        except (ValueError, sqlite3.Error) as exc:
            status.set_text(str(exc))

    chooser.connect('changed', select)
    save.connect('clicked', change)
    delete.connect('clicked', change)
    window.connect('destroy', Gtk.main_quit)
    refresh()
    window.show_all()
    Gtk.main()


def database(path):
    os.umask(0o077)
    db = sqlite3.connect(path)
    db.executescript('''
        create table if not exists accounts (slot integer primary key, base text, local text,
                                             password text, unread integer, auth integer);
        create table if not exists seen (id text primary key);
        create table if not exists delivery (id text primary key, state text);
    ''')
    with db:
        db.execute('begin immediate')
        if 'fetch_days' not in {col[1] for col in db.execute('pragma table_info(accounts)')}:
            db.execute(f'alter table accounts add column fetch_days integer not null default {DEFAULT_FETCH_DAYS}')
    return db


if __name__ == '__main__':
    db = database(sys.argv[2])
    try:
        if sys.argv[1] == 'edit':
            edit(db)
        else:
            sys.exit(sync(db))
    finally:
        db.close()
