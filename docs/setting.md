# Setting

The two worlds of *Saintess Seoyun*, and the rules that connect them.

---

## The two settings

The two worlds deliberately do not match in genre, and the contrast is the
point. They are not two backdrops for one story; they are the two halves of a
**status inversion** that defines the protagonist.

### Modern Korea — low fantasy, high-tech science fiction

Magic exists but is **rare, institutionalised, and industrialised**. It is not
mythic; it is a workforce. The technology is ordinary and near-future —
phones, portals that manifest as equipment-scale incidents, a bureaucracy that
mobilises people. Society is recognisably modern and bureaucratic, and the
magic sits *inside* that infrastructure rather than replacing it.

Mages are few and far between, so the state has organised the ones it has into
a **magic alliance** that forcibly recruits every person with magical power and
deploys them against portal monsters. The fantasy is low and institutional: no
wizards in towers, no apprentice lineages — **a civil service with casualties**.

Recruitment is not a career. It is a census.

Mage ranks run **S, A, B, C, D, E, F**, highest to lowest.

### The fantasy kingdom — high fantasy

A genuinely high-fantasy world, and the tonal opposite of the one Seoyun left.
Magic is **common, unremarkable, and integrated into daily life** rather than
rare and weaponised. There is no magic alliance, no rank system, no state
apparatus built around mages, because there was never a scarcity to manage.

The kingdom is **small**. Small enough that when Seoyun arrives, she is the only
healing-type mage in it.

**The kingdom has no monsters.** Neither does modern Korea. The kingdom's fantasy
is high and its magic is everyday, but the things it has never had to fight are
the things in the between.

### What the contrast defines

| | Modern Korea | The kingdom |
|---|---|---|
| Genre | Low fantasy / high-tech sci-fi | High fantasy |
| Magic | Rare, state-controlled, ranked S–F | Common, ordinary, part of life |
| Magic's role | Conscripted labour | Everyday practice |
| Scale | Large, institutional | Small kingdom |
| Native monsters | **None** | **None** |
| Where monsters come from | The space between the dimensions | The space between the dimensions |
| Portals | Threat, militarised, answered with raids | A window that has never been opened |
| Healer | One of many medics, ordinary | **The only one** |
| Her status | Unnoticed, expendable, abandoned | **Believed a saintess, god's emissary** |

The same healing ability that made Seoyun an ordinary medic — one of many in a
large conscripted force, valued only for what she could do for others and never
looked at twice — makes her, in a small kingdom where mages are scarce and she
alone can heal, **a saintess sent by god**. She goes from the least remarkable
member of a large conscripted force to the most revered individual in a small
kingdom. The thing she was conscripted for in Korea is the thing she is
worshipped for here.

That inversion points straight at her drive: **she arrived having felt small and
abandoned, and the kingdom handed her the one thing that answers that — attention,
reverence, standing.** Being the saintess is not an unwanted interruption of her
plans. It is the first rung of a ladder she is climbing on purpose.

---

## The between

**Monsters do not belong to either world. They live in the inter-dimensional
space that a portal holds open — the between.**

Neither modern Korea nor the fantasy kingdom has native monsters. Both are
monster-free, and that is what makes them look safe until they are not.
**A portal is not a doorway between two places. It is a window into the space
where monsters actually live**, and it spills them out in both directions.

There is no asymmetry to exploit. The kingdom does not have monsters the way it
has forests or weather; the kingdom has no monsters at all, and a portal is how
it gets some. Opening a hole does not let local wildlife loose. It introduces an
enemy that has never been there before, into a place with no defence against it
and no idea what that enemy is.

The kingdom is not a place that has adapted to monsters. It is a place about to
find out what monsters are — and Seoyun is the reason.

---

## The portal mechanic

**Seoyun's phone opens portals. She can use it deliberately, in both directions,
repeatedly, to move between modern Korea and the kingdom.**

| | |
|---|---|
| **What she gains** | Magical energy absorbed on each crossing; she grows stronger |
| **What it costs** | The portal stays open after she passes through |
| **Who pays** | **Both worlds at once.** Monsters from the between spill into each |

She is not a reluctant conduit being used against her will, and she is not
choosing which side to hurt. She is the reason neither world is safe. Every
crossing damages the kingdom that worships her *and* the country that abandoned
her, simultaneously, and she grows either way.

**Korea has never had monsters of its own.** Every incursion is something that
came through a hole in the between — and since Seoyun's arrival, the count is
climbing.

---

## Open questions

### Why a phone, and why can it do this?

An artefact the kingdom's magic recognises? Something the between leaked and
bonds to whoever carries it? A device from the original novel-world? And is there
a cost she is not seeing, or is the cost exactly the one she has accepted?

### Which side figures her out first?

She is personally responsible for introducing the first monsters the kingdom has
ever seen, and she is the reason Korea's numbers are climbing. Whichever world
discovers her first becomes the antagonist for the rest of the story, and the
other is the complication.

### Could the alliance connect the breaches?

Korea is the world where magic is rare enough to be *studied* and an institution
exists to investigate it. The magic alliance is methodical, and a rising monster
count with a consistent cause is precisely the kind of thing it would isolate.
They abandoned a medic once. They would not abandon this.

---

## Korean-language handling

`options.rpy` sets `config.language` via `gui/` translation files under
`game/tl/`. Decide early whether the shipped game is Korean-first with English
secondary, or English-first.

**The current GUI uses DejaVuSans, which has no Hangul coverage.** A CJK-capable
font is required in `game/fonts/` or Korean text renders as boxes.
