# Saintess Seoyun

**A Korean otome isekai visual novel.**

> A healer with the fate of a fictional world in her hands — and the knowledge
> of exactly how that world is supposed to end.

---

## Premise

Seoyun is a Korean woman with healing powers who transmigrated into a fantasy
kingdom that exists inside a novel.

She arrives already knowing two things that no one else in that world can
know: the shape of the story she is inside, and the endings written into it.
Her medicine cannot undo what the book has already decided.

## Genre

| | |
|---|---|
| **Type** | Otome (romance, female protagonist) |
| **Setting** | Isekai — transmigrated into another world |
| **Tropes** | Transmigration, portal fiction, novel-world, healer class, predestined ending, Korean isekai |
| **Format** | Ren'Py visual novel, desktop (PC / macOS) |

## Themes

- Knowledge as burden — she can see the ending, but not unread it
- Whether a person is their story, or whether the story is them
- Healing as a practice vs. healing as a destiny

---

## Chapter Overviews

> **TODO — this section is a scaffold.** Each chapter entry should cover the
> location, the cast present, the emotional turn, and the choice points or
> endings it touches. Fill in as the scenario is written.

### Chapter 1 — *TBD*

- **Setting:**
- **Cast:**
- **Turn:** Seoyun arrives in the kingdom and recognises where she is.
- **Choices / Endings touched:**

### Chapter 2 — *TBD*

- **Setting:**
- **Cast:**
- **Turn:**
- **Choices / Endings touched:**

### Later Chapters

- **TBD**

---

## Story Design Notes

Open questions that shape the scenario:

- **Her healing powers vs. the text.** If the world is a novel, is her healing
  something that *edits* the manuscript, or something the manuscript already
  contains? This determines whether she can change an ending at all, or only
  decide how it is survived.
- **How much of the plot she acts on.** Full foreknowledge can deflate tension
  (nothing is a surprise) or create it (a known tragedy, deliberately
  approached). Pick deliberately; it is the load-bearing decision of the script.
- **What the original novel's ending is.** The book she fell into needs a real,
  written ending for the deviations to register as deviations.
- **Route count and exclusivity.** Whether routes are otome-standard separate
  playthroughs, or a single route with divergence.
- **Korean-language handling.** `options.rpy` sets `config.language` via
  `gui/` translation files under `game/tl/`. Decide early whether the shipped
  game is Korean-first with English secondary, or English-first.

---

## Technical

Built with **Ren'Py 8.5.3** (build 26051504). Base resolution **1920x1080**,
accent colour `#00b8c3`.

### Running the game

```bash
cd ~/Applications/RenPy-8.5.3-sdk
./renpy.sh ~/Projects/"Saintess Seoyun"
```

### Editing

```bash
cd ~/Applications/RenPy-8.5.3-sdk
./renpy.sh launcher
```

Point the launcher's projects directory at `~/Projects`, then select
`Saintess Seoyun`.

### Linting

```bash
cd ~/Applications/RenPy-8.5.3-sdk
./renpy.sh ~/Projects/"Saintess Seoyun" lint
```

Lint does **not** verify that images referenced by screens exist. A missing
`gui/...` asset crashes at runtime, not at lint time.

### Project layout

```
.
├── project.json          # launcher/build settings
└── game/
    ├── script.rpy        # the scenario — labels, dialogue, choices
    ├── options.rpy       # config.name, config.version, build.name, gui.about
    ├── screens.rpy       # screen definitions
    ├── gui.rpy           # GUI styling, generated — edit via launcher, not by hand
    ├── gui/              # generated GUI images (desktop + phone variants)
    ├── images/           # backgrounds, sprites
    ├── audio/            # music, sound effects
    ├── libs/             # third-party Ren'Py libraries
    ├── cache/            # generated, git-ignored
    └── saves/            # player saves, git-ignored
```

### Before building a distribution

`build.name` in `game/options.rpy` is currently `SaintessSeoyun`. The built
bundle is named from it, and it must be ASCII-only with no spaces, colons, or
semicolons.

---

## Status

- [x] Project scaffold generated from the Ren'Py 8.5.3 template
- [x] GUI image set generated (desktop and phone variants)
- [x] Git repository, private, `ClairWu/Saintess-Seoyun`
- [ ] Premise and story bible
- [ ] Chapter outlines
- [ ] Character definitions
- [ ] Backgrounds and character sprites
- [ ] Music and sound effects
- [ ] Icon and store assets
