# The BlackBox kit

Prompts, references and tools for StarDrive BlackBox — the open continuation of the 2013 game.
Each file is something you *paste into a chat with an AI agent* while it has a StarDrive checkout in
front of it. They work on Windows and Linux; the tools that need to build or run the game say so.

Start with the file that matches your question. You do not need to read them in order, and none of
them assumes you have read the others.

## Get it

From the root of a StarDrive checkout:

```
git clone https://github.com/SDBlackBox/StarDrive-community-kit.git docs/kit
```

You get `docs/kit/` with its own `.git`. To update later:

```
git -C docs/kit pull --ff-only
```

If git refuses to fast-forward, your copy has local edits: commit or discard them, then pull. Never
merge or rebase inside `docs/kit` — that turns an update into a conflict.

## What is here

| Want to… | Open | Kind |
|---|---|---|
| get a checkout that builds (Windows) | `clone-setup-prompt.md` | tool |
| get a checkout that reads and edits (Linux, macOS) | `clone-setup-prompt-linux.md` | tool |
| understand how the game works | `game-logic-explainer-prompt.md` | explanation |
| understand what an empire is made of, and what its race decides | `empire-explainer-prompt.md` | explanation |
| understand how far anything is, and how long a hull takes to get there | `time-and-space-explainer-prompt.md` | explanation |
| understand why a fight is won or lost | `ship-combat-explainer-prompt.md` | explanation |
| understand how a tech is gated, priced and paid out | `tech-logic-explainer-prompt.md` | explanation |
| understand what a module costs, fits and does | `module-logic-explainer-prompt.md` | explanation |
| understand a gun's tags, damage numbers and power draw | `weapon-logic-explainer-prompt.md` | explanation |
| understand a design's layout, numbers, role and build gate | `ship-design-explainer-prompt.md` | explanation |
| understand which ships an empire builds, and why that one | `ship-chooser-explainer-prompt.md` | explanation |
| understand how the AI turns goals into task fleets | `fleet-creation-explainer-prompt.md` | explanation |
| understand how a planet is taken, and what survives the handover | `planet-capture-explainer-prompt.md` | explanation |
| go deep on one subsystem | `colonization-ai-explainer-prompt.md` | explanation |
| find where a player-visible thing is decided | `concept-map-prompt.md` | tool |
| look up a content field, or a formula | `ship-content-reference.md` | reference |
| know which content files and tags a mod can replace (token-heavy: reads thousands) | `moddable-content-explainer-prompt.md` | reference |
| turn a strategy into a tech-ordered fleet plan | `ship-strategy-brief.md` | tool |
| turn a belief about the AI into a test you can run, and a result you can read | `ai-test-explainer-prompt.md` | tool |
| cut the tech tree into eras by research cost, for one mod and one race | `era-explorer-prompt.md` | tool |

The twelve explainers are the depth bar: they ask what you already know, then walk one subject at a
chosen level. The combat, tech, module, weapon, design, ship-choice, fleet, planet-capture and empire
ones
also rebuild their concept list from the code and check whether the checkout and the concept map are
current before answering. The tools either write a
file (`concept-map.md`), check something against the game (`--fix-roles`, a unit test, a build), or
run a working session with you (`ship-strategy-brief.md`, and `ai-test-explainer-prompt.md`, which
settles the rung, the two arms and the result format before anything is run). `era-explorer-prompt.md` is a tool of the
third kind and ships with an engine — `docs/era-explorer/era-scan.py` in the StarDrive repository —
because the cut it makes has to be recomputed for your content root and your race rather than
remembered. The reference is lookup-only — it exists
to be quoted from, not read start to finish.

The moddable-content guide is the expensive one. Every claim about a tag is traced to the file that
sets it and the C# that reads it, so a deep answer reads hundreds of content files and a full pass
reads all 5,748 of them plus 900 `.cs` sources. The prompt says that before it answers, and it asks
you to pick one section or one family; its rendered pages already hold the generated values, which is
the cheap way to look one up.

## How to use one

1. Open a checkout of StarDrive in your agent.
2. Paste the whole file, then ask your question.
3. Answer its setup questions. It will offer a menu rather than guessing your level.
4. When it gives an answer, ask it to name the file and symbol behind each claim. Every document here
   is written so it can.

Each file ends by reporting what it checked and what it could not — a build it did not run, a mod it
did not have. Treat that as part of the answer.

## What is not here

These stay in the StarDrive repository, because they are for people changing the code:

- `AGENTS.md` — contributor rules.
- `ARCHITECTURE.md` — engine overview and startup order.
- `docs/code-findings.md` — known problems, deliberately not a bug tracker.
- `docs/concept-map.md` — generated by `concept-map-prompt.md`; lives beside the code it describes.

## Backlog

- **Revisit the dead ends, with the user, family by family.** Every key written as "This item has no
  function in game." was checked against the loader's template and its readers, and some were only
  checked in one place. Go back over the list together and confirm the field really is absent before
  the sentence stands; the module family alone has nine such keys (`Name`, `Description`, `Version`,
  `TexturePath`, `Left`, `Right`, `Rear`, `radius`, `OffPowerMod`).
- **Walk every family through its loader, not only its gameplay class.** Modules, weapons and hulls
  have been checked that way; the twelve families still carrying `values only` cards have not. Start
  with the family's loader (the order and the rename/overwrite rules are in
  `moddable-content-explainer-prompt.md`), then search the name the loader actually binds. Current
  counts: races 89, buildings 54, ui 51, racialtraits 46, particles 35, technology 35, events 31,
  encounters 28, planettypes 26, troops 25, suns 22, designs 20 — 671 violations in all, so `--audit`
  exits 1 on purpose until the prose exists.
- **Settle the two names that look like a feature and are not.** `Tag_SpaceBomb` is an enum member
  with no property, and `ShipModuleType.Spacebomb` is a module type no vanilla file uses, which mounts
  `WeaponType` like a turret. Planet bombing is `ModuleType` Bomb plus `BombType`; say that wherever
  the Spacebomb names surface, or drop the path if it is dead.
- **Re-check the cards that still have no data** once the search areas in
  `moddable-content-explainer-prompt.md` are tuned: a card that stayed `values only` because the
  search looked in the wrong file is a gap in the search, not in the game.

## Status

Vetted against `StarDrive@f575899` on 10 November 2026. Every prompt uses paths and symbol names
rather than line numbers, so it survives ordinary edits; a file whose citations no longer resolve is
a bug worth reporting in Discord.
