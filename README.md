# Saintess Seoyun

**A Korean otome isekai visual novel.**

> An evil protagonist in a saintess's robes. She came to a kingdom that
> worshipped her and decided that being worshipped was the first step toward
> being the most powerful woman in the world.

An ordinary battle medic in an alternate modern Korea is forcibly recruited into
a government magic alliance, survives a raid that goes catastrophically wrong,
and falls through a portal her own phone opened. She lands in a small
high-fantasy kingdom with no monsters and no healer but her, and is taken for a
saintess.

She intends to use that. She crosses between the worlds repeatedly to absorb
magical energy and grow stronger — and every portal she opens stays open behind
her, spilling monsters from the space between the dimensions into **both**
worlds at once.

She is not a reluctant conduit. She is the one holding the door open.

---

## Design documents

| | |
|---|---|
| **[docs/setting.md](docs/setting.md)** | The two worlds, the between, the portal mechanic |
| **[docs/characters.md](docs/characters.md)** | Seoyun, the mask, the love interests |
| **[docs/plot.md](docs/plot.md)** | Premise, themes, chapter scaffolds, route structure |

---

## Genre

| | |
|---|---|
| **Type** | Otome (romance, female protagonist) |
| **Protagonist** | Evil protagonist, disguised as a saintess |
| **Setting** | Isekai — transmigrated from alternate modern Korea into a fantasy kingdom |
| **Tropes** | Transmigration, portal fiction, novel-world, conscription, class hierarchy, healer class, evil protagonist, false idol, saintess, non-combatant protagonist, authoritarian government, Korean isekai |
| **Format** | Ren'Py visual novel, desktop (PC / macOS) |

## Premise in brief

**Before.** An ordinary battle medic in an alternate modern Korea, where magic is
rare and conscripted. The government establishes a magic alliance that forcibly
recruits everyone with power and deploys them against monsters from portals of
unknown origin. Ranks run S through F. When a raid goes wrong and her forces
scatter, separated and unable to fight, she believes she will die there — small,
abandoned, unseen. Her phone opens a portal, and she falls through.

**After.** A small high-fantasy kingdom with everyday magic, no monsters, and no
one who can heal. She is the only healing-type mage there, and the kingdom takes
her for a saintess sent by god.

**The drive.** She wants to be the most powerful woman in the world, as
compensation for the moment she felt smallest and most abandoned. The sainthood
is a step toward that goal, not the destination.

**The cost.** Every crossing strengthens her and leaves a portal open behind her.
Monsters from the between spill into both worlds — the one that worships her and
the one that abandoned her, together.

Full detail in [docs/plot.md](docs/plot.md).

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
├── docs/                 # design documents
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
- [x] Premise and story bible, split into design documents
- [x] The two settings, and the status inversion between them
- [x] Seoyun's drive, origin wound, and method
- [ ] Love interests
- [ ] Chapter outlines
- [ ] Route structure decided
- [ ] Backgrounds and character sprites
- [ ] Music and sound effects
- [ ] CJK-capable font, if shipping in Korean
- [ ] Icon and store assets
