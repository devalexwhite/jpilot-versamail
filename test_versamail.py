import struct
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
import versamail as vm


def fixture():
    data = Path(__file__).with_name('MultiMail+Messages.pdb').read_bytes()
    entries = [struct.unpack_from('>IB3s', data, 78+i*8) for i in range(3)]
    return [(int.from_bytes(uid), attr & 0xf0, attr & 15,
             data[start:(entries[i+1][0] if i < 2 else len(data))])
            for i, (start, attr, uid) in enumerate(entries)]


class ConduitTests(unittest.TestCase):
    def test_fastmail_authentication(self):
        for port, transport in [(465, 'SMTP_SSL'), (587, 'SMTP')]:
            with self.subTest(port=port), patch.object(vm.smtplib, transport) as connect, patch.object(vm, 'write'):
                db = vm.database(':memory:')
                self.addCleanup(db.close)
                smtp = connect.return_value
                smtp.send_message.return_value = {}
                account = dict(outgoing='smtp.fastmail.com', smtp_port=port, username='user@fastmail.com')
                with self.assertRaisesRegex(ValueError, 'Enable SMTP authentication'):
                    vm.send(db, 1, account, 'app-password', fixture(), False, '')
                connect.assert_not_called()
                vm.send(db, 1, account, 'app-password', fixture(), True, '')
                operations = [call[0] for call in smtp.method_calls]
                expected = ['ehlo', 'starttls', 'ehlo'] if port == 587 else ['ehlo']
                self.assertEqual(operations, expected + ['auth', 'send_message'])
                smtp.auth.assert_called_once_with('PLAIN', smtp.auth_plain)
                self.assertEqual((smtp.user, smtp.password), ('user@fastmail.com', 'app-password'))

    def test_fixture_send_and_retry(self):
        db = vm.database(':memory:')
        self.addCleanup(db.close)
        rows = fixture()
        with patch('smtplib.SMTP') as connect, patch.object(vm, 'write') as write:
            connect.return_value.send_message.return_value = {}
            connect.return_value.has_extn.return_value = False
            smtp = connect.return_value
            for _ in range(2):
                vm.send(db, 1, dict(smtp_port=25, outgoing='example.invalid'), '', rows, False, '')
            smtp.send_message.assert_called_once()
            msg = smtp.send_message.call_args.args[0]
            self.assertEqual(msg['Subject'], 'Hi test')
            self.assertEqual(msg.get_content(), '119abz\n\nSig123\n')
            self.assertIsNone(msg['Bcc'])
            self.assertEqual(smtp.send_message.call_args.kwargs['to_addrs'],
                             ['123@i.com', 'cc1@i.com', 'bcc1@i.com'])
            write.assert_called_with(rows[1][0], rows[1][1], 3, rows[1][3])

    def test_to_only_retries_after_recipient_refusal(self):
        db = vm.database(':memory:')
        self.addCleanup(db.close)
        uid, attr, cat, raw = fixture()[1]
        fields = raw[24:].split(b'\0')
        fields[3:5] = [b'', b'']
        rows = [(uid, attr, cat, raw[:24] + b'\0'.join(fields))]
        account = dict(smtp_port=25, outgoing='example.invalid')
        with patch('smtplib.SMTP') as connect, patch.object(vm, 'write') as write:
            smtp = connect.return_value
            smtp.has_extn.return_value = False
            smtp.send_message.side_effect = [
                vm.smtplib.SMTPRecipientsRefused({'123@i.com': (450, b'Try later')}), {}
            ]
            with self.assertRaisesRegex(ValueError, 'refused all recipients'):
                vm.send(db, 1, account, '', rows, False, '')
            write.assert_not_called()
            vm.send(db, 1, account, '', rows, False, '')
            self.assertEqual(smtp.send_message.call_args.kwargs['to_addrs'], ['123@i.com'])
            write.assert_called_once_with(uid, attr, 3, rows[0][3])

    def test_fetch_twice(self):
        db = vm.database(':memory:')
        self.addCleanup(db.close)
        with (patch('imaplib.IMAP4_SSL') as connect, patch.object(vm, 'write') as write,
              patch.object(vm, 'date') as calendar):
            calendar.today.return_value = date(2026, 1, 3)
            client = connect.return_value
            client.select.return_value = ('OK', [b'1'])
            client.response.return_value = ('UIDVALIDITY', [b'145'])
            client.uid.side_effect = [('OK', [b'12']), ('OK', [(b'12', b'Subject: Test\n\nBody')]),
                                      ('OK', [b'12'])]
            account = dict(tls=True, incoming='example.invalid', port=993, username='user', limit=5)
            vm.fetch(db, 1, account, '', [], True)
            vm.fetch(db, 1, account, '', [], False, 1)
            self.assertEqual(client.uid.call_args_list[0].args, ('search', None, 'UNSEEN', 'SINCE', '28-Dec-2025'))
            self.assertEqual(client.uid.call_args_list[-1].args, ('search', None, 'ALL', 'SINCE', '03-Jan-2026'))
            write.assert_called_once()
            uid, attr, category, raw = write.call_args.args
            self.assertEqual((uid, attr, category), (0, 0, 0))
            self.assertEqual(vm.HEADER.unpack_from(raw)[3], 2)
            self.assertEqual(raw[24:].split(b'\0')[7], b'Body')

    def test_account_changes_in_both_directions(self):
        prefs = {i: bytes(180) for i in range(8)}
        db = vm.database(':memory:')
        self.addCleanup(db.close)
        with (patch.object(vm, 'pref', prefs.get), patch.object(vm, 'put', prefs.__setitem__),
              patch.object(vm, 'records', return_value=[]), patch.object(vm, 'send'),
              patch.object(vm, 'fetch'), patch.object(vm, 'rpc')):
            self.assertFalse(vm.sync(db))
            a = vm.DEFAULT | dict(name='Personal', incoming='imap.example', outgoing='smtp.example',
                                  username='alex', email='alex@example.com')
            db.execute('update accounts set local=?,password=? where slot=1', (vm.json.dumps(a), 'test'))
            db.commit()
            self.assertFalse(vm.sync(db))
            self.assertEqual(vm.account(1)[1], a)
            prefs[35] = b'Renamed on Palm\0'
            self.assertFalse(vm.sync(db))
            local = db.execute('select local from accounts where slot=1').fetchone()[0]
            self.assertEqual(vm.json.loads(local)['name'], 'Renamed on Palm')
            db.execute("update accounts set local='{}' where slot=1")
            db.commit()
            self.assertFalse(vm.sync(db))
            self.assertEqual(vm.account(1)[1], {})
            prefs[35] = b'Added on Palm\0'
            vm.sync(db)
            local = db.execute('select local from accounts where slot=1').fetchone()[0]
            self.assertEqual(vm.json.loads(local)['name'], 'Added on Palm')
            del prefs[35]
            self.assertFalse(vm.sync(db))
            self.assertEqual(db.execute('select local from accounts where slot=1').fetchone()[0], '{}')

    def test_html_import(self):
        raw = b'Content-Type: text/html\r\nSubject: HTML\r\n\r\n<p>A &amp; <b>B</b><br>C</p>'
        record = vm.incoming_record(raw, 1, 17, 'key', 5)
        self.assertEqual(vm.HEADER.unpack_from(record)[:1], (17,))
        self.assertEqual(record[24:].split(b'\0')[7], b'A & B\nC')


if __name__ == '__main__':
    unittest.main()
