# Contributing to VersaMail Conduit

Thank you for helping keep Palm OS hardware doing real work.

## Principles

1. **Hardware is the point.** Small screens, Latin-1, slow links, and real
   cradles are the design constraints, not bugs to work around.
2. **Say what ran.** When adding a feature or reporting a test, write down
   the handheld model, the Palm OS version, the viewer, and the desktop
   environment. “Untested on hardware” is a valid note; unstated assumptions
   are not.
3. **Calm dependencies.** This is a desktop tool that talks to a handheld.
   Keep build and runtime dependencies standard (C99, GTK 3, Python 3.11+,
   pilot-link). Don't add a service or a daemon when a file and a sync
   will do.

## Development

### Building

```sh
make
```

### Testing without hardware

You don't need a Palm to run the test suite:

```sh
python3 -m unittest -v
```

The tests mock network services and exercise PDB decoding, Outbox preservation, and SMTP error handling against the sample databases.

## Pull Requests

- Keep changes focused. One feature or fix per PR.
- Update the README if you change behavior, dependencies, or add a feature.
- If you tested on real Palm hardware, mention the model in your PR description.

## Brand Assets

Brand assets (marks, banners, badges) live in `brand/assets/` and `docs/`.
They are generated from pixel definitions by `brand/tools/build_assets.py`.
See [brand/README.md](brand/README.md) for palette, typography, and guidelines.

To rebuild brand assets:

```sh
python3 brand/tools/build_assets.py --title "VersaMail Conduit" --subtitle "J-Pilot IMAP and SMTP mail conduit"
```
