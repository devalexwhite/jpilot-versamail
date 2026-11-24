# Bitcradle

A portable brand kit for a collection of small tools that keep Palm OS handhelds doing useful work. Copy this folder into another repository, or lift it out later into its own repo. Everything the kit needs is in this directory: the name, the voice, the colors, the type, the marks, and a README template. Fonts are linked, not bundled.

The first project in the collection is Feeds to Plucker, a J-Pilot conduit in this repository. The kit is written so the next Palm OS repo can reuse it without depending on that conduit.

## Audience

Technologists who like old hardware and still use it. Many of them are tired of AI marketing. Talk to them as people who already know what a cradle, a conduit, and a 160×160 screen are. Be warm, precise, and a little playful. Treat the hardware as the point of the work.

AI, when a project uses it, is a tool for a specific step: extract a page, draft a conduit, convert a file. The sentence after that should say what the handheld can do. Feeds to Plucker does not call a model. Say so when that is true of a project, and say which step a model covers when it is not.

## Name

### Chosen: Bitcradle

The cradle is where the desktop hands the handheld a finished file, and the bit is what the screen can hold. **Bitcradle** names that handoff. It still fits if a later tool is color or hi-res, and it does not use a Palm trademark.

Say it “bit cradle.” In prose, write **Bitcradle**. The pixel wordmark is **BITCRADLE**.

A search did not turn up a software brand with this spelling. Check it again before a domain or a printed case.

### Set-aside alternate: Fourshade

Fourshade was the first working name. It pointed at four shades of grey on a Palm OS LCD. Alex chose Bitcradle instead, so Fourshade is a set-aside alternate. It stays in this list so the next repo does not revive it by accident. It was a nod to the greyscale era, not a promise of four-shade output. Feeds to Plucker still dithers images to one bit.

### Alternate: Pocket Phosphor

This one names the green electroluminescent glow and the pocket the machine still fits in. It is the warmest of the three. Nearby names already in use: a Phosphor mobile app marketed as “a brilliant light in your pocket,” and Phosphor BBS. The exact phrase “Pocket Phosphor” was not a clear product hit. “Phosphor” on its own is busy.

### Names set aside

These were real candidates. They are listed so the next repo does not revive them by accident.

| Name | Why it was set aside |
| --- | --- |
| Greylight | SideFX Project Greylight, the Greylight venture studio (greylight.co), and Grey Light Software. |
| Pixcradle | pixelcradle.com is PixelCradle, a photo-backup product. The spellings are too close. |
| Lampblack | A book-writing app (lampblack.dev), plus a studio and a consultancy. |
| Synclamp | synclamps.com already uses the word. |
| Fourshade | Set-aside alternate. First working name, replaced by Bitcradle. |

This was a web search, not a trademark clearance.

## Tagline

**Palm OS hardware, still at work.**

The line still fits Bitcradle. The name is the handoff at the cradle. The tagline is why the collection exists: the machines are still doing a job. A line that only mentions the cradle would fit this conduit, and it would fit a later notes or maps tool less well.

Two alternates, if a tighter line is wanted later:

- **The cradle still has a job.** Same idea, closer to the name.
- **A finished file, left on the handheld.** Concrete. Narrower if a project is not a document.

Use the chosen line under the wordmark, in a collection footer, and as the last line of a social preview. Project taglines stay specific to the tool.

## Messaging

### One-liner

Bitcradle makes small, practical tools so a Palm OS handheld can keep doing a real job. A model is welcome only at the step where it saves one.

### Short paragraph

A lot of these machines still power on. The screen is small, the battery is a known quantity, and the software pattern is a cradle, a conduit, and a document that stays on the device after the cable comes out. Bitcradle builds that kind of tool. When ordinary code can turn something from the network into a file the handheld can hold, that code is the product. When a model can do one of those steps more carefully, use it there and name the step in the README. The aim is a device that still earns its pocket, with the claims kept as small as the screen.

### Pillars

1. **The handheld sets the spec.** Memory, Latin-1, the pixels on that device, the battery, and a cradle. If it does not fit on the hardware, it is not finished.
2. **A finished sync beats a clever demo.** The useful thing is what is on the handheld after the cable comes out.
3. **Use a model like a tool.** Put it on a step you can check: extract, convert, draft. Leave it out when ordinary code is clearer. Write down which one you did.
4. **Write down what ran.** Desktop versions, the viewer, and the device. “Untested on hardware” is a finished sentence.

### Words to use

handheld, conduit, sync, cradle, document, edition, offline, greyscale, monochrome, pixel, dither, practical, careful, tested, untested, Palm OS, record, feed, lamp, bezel.

“HotSync” is the right word when you mean Palm’s sync operation. It is their trademark. Use it as a descriptive name for that step. Do not draw their arrows mark.

### Words to avoid

AI-powered, revolutionary, seamless, magic, disrupt, unlock, next-gen, smart (as a boast), delight, leverage, ecosystem, future-proof, blazing-fast, “breathing new life,” digital companion, supercharge, effortless.

## Voice and tone

Write like a person who owns a soldering iron and a Palm, explaining a tool to a friend who owns one too. Short sentences. Concrete nouns. Numbers from the code, not from a launch post. A dry joke is welcome. A slogan is not.

The hardware gets respect. Constraints are interesting. They are not a punchline about how quaint the device is.

### Do and don't

**Describing the tool**

- Do: “HotSync builds one Plucker document from articles dated today and installs it over the previous edition.”
- Don't: “An AI-powered reading experience that unlocks your legacy device.”

**Talking about models**

- Do: “This conduit does not call a model. Extraction is a parser and a few heuristics. If a later tool uses a model, name the step it replaces.”
- Don't: “We leverage generative AI to seamlessly reimagine offline content.”

**Hardware limits**

- Do: “Images are fit inside 160×160 and dithered to one bit. The rest of the article is Latin-1 text.”
- Don't: “The app intelligently adapts any modern layout to the beautiful Palm canvas.”

**Status**

- Do: “Tested with a Tungsten T3 syncing from an Omarchy Linux desktop. Other models are not listed, because they have not been synced.”
- Don't: “Works with every Palm ever made.”

**Tone**

- Do: “The lamp is still on. The screen is still small. Here is a document that fits.”
- Don't: “Revolutionary pocket intelligence for the post-smartphone era.”

## Color

The palette did not change with the name. Bitcradle is about the handoff, and the colors are still the screen: reflective greyscale in daylight, and the same screen with the green backlight on. Plastic colors from particular models (silver aluminum, blue faceplates) stay out. So do Palm’s blue title bars from later color releases.

Hex values are the source of truth. Names are for writing and for CSS variables.

| Token | Hex | Name | Use |
| --- | --- | --- | --- |
| `--paper` | `#E8E6DE` | Paper | Light page background, the unlit LCD field |
| `--silver` | `#D2D0C8` | Silver | Cards, wells, secondary surfaces on Paper |
| `--mist` | `#A7AAA2` | Mist | Decorative dither only. Never text, never a UI boundary |
| `--graphite` | `#4E524A` | Graphite | Secondary text on Paper and Silver |
| `--ink` | `#161814` | Ink | Primary text, light-mode bezel, pixel-on in daylight |
| `--phosphor` | `#D7E7A1` | Phosphor | Lit “paper” highlight, primary text on Night and Moss |
| `--backlight` | `#C5D48A` | Backlight | The green LCD field, large fills |
| `--olive` | `#5C6B3A` | Olive | Filled chips and shields message colors. Large text only on Paper |
| `--pine` | `#3E4A24` | Pine | Links and small text that must sit on Paper, Phosphor, or Soft Amber |
| `--moss` | `#2C3420` | Moss | Dark surfaces, LCD bezel, badge fills |
| `--night` | `#14180F` | Night | Darkest background |
| `--amber` | `#8A5A12` | Amber | “Untested” and other warnings, on Paper |
| `--soft-amber` | `#F0D7A2` | Soft Amber | Warning banner background. Put Ink on it, not Amber |

Mist on Paper is about 1.9:1. It disappears if you use it for a rule or a label. Use Graphite for rules that have to be seen, Silver for quiet fills.

Olive on Phosphor is about 4.4:1 and Olive on Backlight is about 3.6:1. That is large-text territory. Body copy on a green field is Ink or Night.

### Contrast pairs

Ratios below were computed against WCAG 2 relative luminance. “AAA” means at least 7:1, “AA” at least 4.5:1.

**Light UI**

| Foreground | Background | Ratio | Use |
| --- | --- | --- | --- |
| Ink `#161814` | Paper `#E8E6DE` | 14.3:1 AAA | Body text |
| Graphite `#4E524A` | Paper `#E8E6DE` | 6.4:1 AA | Secondary text |
| Ink `#161814` | Silver `#D2D0C8` | 11.6:1 AAA | Text on cards |
| Graphite `#4E524A` | Silver `#D2D0C8` | 5.2:1 AA | Secondary text on cards |
| Pine `#3E4A24` | Paper `#E8E6DE` | 7.6:1 AAA | Links |
| Amber `#8A5A12` | Paper `#E8E6DE` | 4.7:1 AA | Warning text |
| Ink `#161814` | Soft Amber `#F0D7A2` | 12.7:1 AAA | Text on a warning banner |
| White `#FFFFFF` | Ink `#161814` | 17.9:1 AAA | Inverted chips |

**Green LCD and dark UI**

| Foreground | Background | Ratio | Use |
| --- | --- | --- | --- |
| Ink `#161814` | Phosphor `#D7E7A1` | 13.5:1 AAA | Pixels on a lit screen |
| Ink `#161814` | Backlight `#C5D48A` | 11.2:1 AAA | Text on a green field |
| Night `#14180F` | Phosphor `#D7E7A1` | 13.6:1 AAA | Same idea, slightly softer ink |
| Moss `#2C3420` | Phosphor `#D7E7A1` | 9.8:1 AAA | Secondary LCD text |
| Phosphor `#D7E7A1` | Night `#14180F` | 13.6:1 AAA | Dark-theme body |
| Phosphor `#D7E7A1` | Moss `#2C3420` | 9.8:1 AAA | Text on a dark card |
| Backlight `#C5D48A` | Night `#14180F` | 11.3:1 AAA | Dark-theme headlines |
| Backlight `#C5D48A` | Moss `#2C3420` | 8.1:1 AAA | Headlines on Moss |
| Pine `#3E4A24` | Phosphor `#D7E7A1` | 7.2:1 AAA | Links on a lit field |
| White `#FFFFFF` | Moss `#2C3420` | 13.0:1 AAA | shields.io label text |
| White `#FFFFFF` | Olive `#5C6B3A` | 5.8:1 AA | shields.io message text |
| White `#FFFFFF` | Graphite `#4E524A` | 8.0:1 AAA | shields.io message text |

**Leave these alone for small text**

| Pair | Ratio | Why |
| --- | --- | --- |
| Mist on Paper | 1.9:1 | Decorative only |
| Olive on Backlight | 3.6:1 | Fails body text |
| Olive on Phosphor | 4.4:1 | Large text only |
| Amber on Phosphor | 4.5:1 | Borderline. Use Ink for text on Phosphor |
| Amber on Soft Amber | 4.2:1 | Use Ink on Soft Amber instead |

For one-bit illustrations, dither with a 2×2 pattern instead of inventing more greys: 25% one pixel, 50% a checker, 75% three pixels. Pixel color is Ink on Paper, or Night on Backlight.

## Typography

Four roles. All of them are freely licensed. None of them is a Palm system font, a FontHack PDB, or Jason Kottke’s Silkscreen (that face is freeware drawn to imitate the Newton/Palm UI, and it is not OFL). Do not bundle font files in this folder. Link them, and keep the OFL text with any copy you redistribute.

The logo wordmarks do not depend on these fonts. They are drawn as rectangles on a 5×7 grid so they render with nothing installed.

| Role | Face | License | Where to get it | Use |
| --- | --- | --- | --- | --- |
| Display, pixel | [Departure Mono](https://departuremono.com/) by Helena Zhang | SIL OFL 1.1. Reserved font name “Departure Mono.” | [GitHub](https://github.com/rektdeckard/departure-mono) | Hero titles, social previews, badges set in live text. Size in multiples of 11px. |
| Handheld UI | [Ark Pixel](https://github.com/TakWolf/ark-pixel-font) 12px proportional, by TakWolf | SIL OFL 1.1. The build tools are MIT. The font is OFL. | [GitHub](https://github.com/TakWolf/ark-pixel-font) | Short labels painted inside screen illustrations. 16px was removed upstream; use 12px or 10px. Latin coverage is what this kit needs. CJK is still incomplete upstream. |
| Body | [IBM Plex Sans](https://www.ibm.com/design/language/typography/typeface/) | SIL OFL 1.1. Reserved font name “Plex.” | [GitHub](https://github.com/IBM/plex), [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Sans) | READMEs you control, manuals, the future brand site. |
| Mono | [IBM Plex Mono](https://github.com/IBM/plex) | SIL OFL 1.1. Reserved font name “Plex.” | [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Mono) | Commands, paths, feed URLs, code. |

Optional alternate bitmap, if a project needs a system font at several pixel sizes: [Spleen](https://github.com/fcambus/spleen) by Frederic Cambus, BSD 2-Clause. It is not the default.

GitHub’s README renderer uses its own font stack. Specify Plex and Departure Mono where you control CSS. The banner PNG carries the display face for the README.

When you bundle a font with software, ship the license file and respect the reserved names. Documents and logos you make with the font are yours. The OFL FAQ is at <https://openfontlicense.org/ofl-faq/>.

## Marks

The mark is a handheld sitting in a plain cradle. The screen is square, with one selected list row, three quieter rows, and a lamp pixel on the chin. The cradle is two posts and a base, drawn in the same pixel geometry. It should still read at a small size. It is not a drawing of a Palm V, a Tungsten, or any other specific model.

Leave these out of every asset:

- The Palm wordmark, the Palm “p,” and PalmOne marks
- The HotSync arrows
- The four silkscreen icons (home, menu, calculator, find)
- The Graffiti alphabet
- A fake photograph of a device, or a screenshot that pretends to be one

“Palm OS” and “HotSync” may appear as words. They name the platform and the sync step.

### Asset files

SVG is the source. PNG companions are what GitHub READMEs and the social-preview setting can show. GitHub does not render SVG in Markdown. Each PNG of a dark or LCD mark has its intended background baked in, so it stays visible on GitHub’s white page. The SVG backgrounds are transparent unless the file is a full banner.

| File | What it is |
| --- | --- |
| `assets/mark-light.svg` | Mark, ink bezel, paper screen, green lamp |
| `assets/mark-dark.svg` | Mark for a Night background |
| `assets/mark-lcd.svg` | Mark with the green backlight field |
| `assets/wordmark-light.svg` | BITCRADLE in 5×7 pixels, Ink |
| `assets/wordmark-dark.svg` | Wordmark in Phosphor |
| `assets/wordmark-lcd.svg` | Wordmark in Night, for use on Backlight |
| `assets/lockup-light.svg` | Mark plus wordmark, for Paper |
| `assets/lockup-dark.svg` | Mark plus wordmark, for Night |
| `assets/lockup-lcd.svg` | LCD mark plus Ink wordmark, for Paper |
| `assets/hero-banner.svg` | README banner template, 1280×360. Edit the text nodes marked `EDIT` |
| `assets/social-preview.svg` | Social card template, 1280×640. Same `EDIT` markers |
| `assets/placeholder-frame.svg` | A frame that says PLACEHOLDER, so an empty screenshot slot cannot be mistaken for a capture |
| `assets/badges/palm-os-compatible.svg` | “Palm OS / compatible” |
| `assets/badges/hotsync-ready.svg` | “HotSync / ready” |
| `assets/badges/bitcradle.svg` | “Bitcradle / collection” |
| `assets/pixel-alphabet.svg` | The 5×7 capitals the wordmarks use |

Each of those has a `.png` beside it.

`brand/tools/build_assets.py` redraws the pixel grids from one letter table. Copy the SVG and PNG files to use the kit. Run the script only when the wordmark or the banner copy changes. It does not download fonts. Banner text is set in Departure Mono when that face is installed, and the committed PNGs were rasterized with it.

### Badges

The SVG badges use Phosphor on Ink (label) and Phosphor on Moss (message), flat and square, with the 5×7 face. shields.io paints its text white, so the README URLs use the dark end of the same palette. White on these fills clears AA.

```
https://img.shields.io/badge/Palm%20OS-compatible-2C3420?style=flat-square&labelColor=161814
https://img.shields.io/badge/HotSync-ready-5C6B3A?style=flat-square&labelColor=161814
https://img.shields.io/badge/Bitcradle-collection-4E524A?style=flat-square&labelColor=161814
https://img.shields.io/badge/license-GPL--2.0--or--later-4E524A?style=flat-square&labelColor=161814
```

| Badge | Label fill | Message fill | Text |
| --- | --- | --- | --- |
| Palm OS compatible | Ink `#161814` | Moss `#2C3420` | white |
| HotSync ready | Ink `#161814` | Olive `#5C6B3A` | white |
| Bitcradle collection | Ink `#161814` | Graphite `#4E524A` | white |
| GPL-2.0-or-later | Ink `#161814` | Graphite `#4E524A` | white |

Change the collection badge if the name changes. “HotSync” on a badge means the tool runs during that sync. It is not Palm’s logo. The license badge points at a `LICENSE` file. This repository’s file is GPL-2.0-or-later, the same terms as J-Pilot, with the “or any later version” grant.

## README template

`README_TEMPLATE.md` in this folder is the starting README for a project. Sections, in order:

1. Hero banner
2. Pitch
3. Screenshots or GIF
4. Features
5. Supported devices
6. Install
7. Usage
8. Roadmap
9. Contributing
10. License
11. Collection footer

Screenshot slots stay labeled as placeholders until a real capture exists. A diagram of a file format is fine. A drawing that looks like a Palm screen and is presented as a photo is not.

## Applying the kit to a new repo

1. Copy `brand/` into the repo. Update the footer link if the kit later moves to its own repository.
2. Duplicate `assets/hero-banner.svg`. Replace every text node whose id starts with `edit-`. Export a PNG at 1280×360 and commit it next to the project README. Point the README at the PNG.
3. Do the same for `assets/social-preview.svg` at 1280×640. Commit the PNG (`.github/social-preview.png` is a reasonable path). Then upload that PNG in the GitHub repository settings. A file in the tree does not set the social image by itself.
4. Copy `README_TEMPLATE.md` to the repo root `README.md` and fill it. Keep claims inside what the code does.
5. Add the three badges, or drop any that would be a lie for that project. “HotSync ready” is for a tool that actually runs at HotSync.
6. Add `CONTRIBUTING.md`, keep the GPL-2.0-or-later `LICENSE` (or say plainly if a new repo uses different terms), and add issue templates if the repo takes contributions.
7. Set the GitHub description (350 characters or fewer) and topics in the repository settings.
8. In “Supported devices,” name only hardware that someone has synced, and mark everything else untested.

## Trademarks

Palm, Palm OS, HotSync, Graffiti, and the old Palm logos belong to their owners. Bitcradle is an independent collection. We use “Palm OS” and “HotSync” to identify the platform and the sync step. We do not use Palm’s logos.

Plucker is the name of the open-source document format and viewer this conduit targets. Use the name. Do not copy a Plucker logo into this kit.

## License of the kit

This folder is part of Feeds to Plucker, which is free software under the GNU General Public License, version 2, or (at your option) any later version. Copyright (C) 2026 Alex White. The grant is in [LICENSE](../LICENSE) at the repository root. Copying the kit into another repository keeps that license unless the new project says otherwise in its own `LICENSE` file.

The typefaces keep their own licenses, listed above. Those licenses are not the license for the SVG artwork, and the font files are not in this folder.
