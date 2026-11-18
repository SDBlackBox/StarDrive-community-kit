# Explaining an empire — a copy-paste interactive prompt

Paste the prompt below into an agent that can read this repository, and it becomes a guide to **what
an empire is made of**: the race file behind it, what its traits actually change, what it starts
with, what it is allowed to see, and where the numbers that make one empire different from another
are written down.

This is the document the others point at. The [tech explainer](tech-logic-explainer-prompt.md) says a
tech can be hidden from a people; this one says what a people is. The
[era explorer](era-explorer-prompt.md) needs a race and a trait set to draw a ladder; this one is
where those come from. The [ship chooser](ship-chooser-explainer-prompt.md) and
[fleet creation](fleet-creation-explainer-prompt.md) explainers assume an empire with designs, money
and goals; this one says where those start.

## Why this exists

- **There is no empire in `game/Content`.** There are race files under `game/Content/Races/`, and an
  empire is one of those loaded into `EmpireData` — a `[StarData]` object, saved, matched by field
  name — plus the live `Empire` that owns colonies, research, fleets and diplomacy. Ask which half a
  question is about before answering it.
- **A trait is not a label, it is a number with a reader.** `RacialTrait` carries roughly eighty
  fields, and a great many are read directly: `ResearchMod`, `ProductionMod`, `ShipCostMod`,
  `MaintMod`, `GroundCombatModifier`, `TargetingModifier`, `DodgeMod`, `OrdnanceEffectivenessBonus`,
  the `Env*` habitability row. "Why is my research slower than his" is often a trait, not a building.
- **Only four racial trait names exist in code.** `RacialTrait.NameOfTrait` is `None`, `Cybernetic`,
  `Militaristic`, `NonCybernetic`. So a tech can be gated on exactly those — the fifty trait options
  a player picks from are not the same list as the traits content can test for. Confusing the two is
  the most common wrong answer here.
- **A race file carries its own starting fleet.** `StartingShip`, `PrototypeShip` and the `Default*`
  hulls are race data, so two empires begin with different ships from identical content.
- **The first trait set is the player's; the rest are the AI's rerolls.** `TraitSets[0]` is what the
  race design screen shows, and `PlayerTraitOptions` returns exactly that one. An AI opponent of the
  same race can therefore hold traits you never saw on the menu.
- **`UnlockedAtGameStart` is a real grant.** A matching empire does not merely see the tech: the
  trait's `UnlockAtGameStart` calls `ForceFullyResearched`, so a Militaristic people begins with
  kinetic weapons, energy cannons, laser beam turrets, corvettes, armour theory, fighter shields and
  the military tech already owned. That is why the era ladder is shorter for them.
- **An empire is a save object.** Renaming a `[StarData]` field breaks old saves silently; adding one
  does not need a version bump. Say which of the two a change is, if the question is about changing
  anything.
- **Pirates and factions are empires with the rules switched off.** `IsFaction` forces every tech
  back to unresearched, and a pre-warp empire (`Traits.Prewarp == 1`) does the same to itself.

## The empire chain

| # | Step | What it decides | Where |
|---|---|---|---|
| 1 | Who | the people: name, ship type, colour, portrait, voice | `EmpireData.PortraitName`, `RacialTrait.Name`, `ShipType`, `Singular`/`Plural` |
| 2 | Which traits | the numbers and the gates | `RacialTrait` fields, `TraitSets`, `PlayerTraitOptions`, `SelectedTraitSet` |
| 3 | What it starts with | free techs, extra ships, extra buildings | `UnlockedAtGameStart` → `RacialTrait.UnlockAtGameStart` → `ForceFullyResearched`; `EmpireData.unlockShips`, `unlockBuilding`; `StartingShip`, `PrototypeShip`, `Default*` |
| 4 | What it can see | techs hidden from this people | `Technology.HiddenFrom`, `HiddenFromAllExcept`, `TechEntry.IsHidden`, `InRaceRequirementsArray` |
| 5 | What it earns | research, production, tax, upkeep | `ResearchMod`, `ProductionMod`, `TaxMod`, `ConsumptionModifier`, `MaintMod`, `ShipCostMod`, `BaseReproductiveRate` |
| 6 | What it fights with | ground strength, accuracy, evasion, hull, ordnance | `GroundCombatModifier`, `TargetingModifier`, `DodgeMod`, `ModHpModifier`, `OrdnanceEffectivenessBonus`, `ArmorPiercingBonus` |
| 7 | Who it is to others | starting relations, spies, diplomacy | `DiplomacyMod`, `DiplomaticPersonality`, `AgentList`, `MoleList`, `SpyModifier` |

The race file also decides the *shape* of a game rather than a number: `Prewarp` starts everyone
behind, `Prototype` hands out a flagship, `Blind` changes what you can see, `PreferredEnv` and the
`Env*` row decide which worlds are worth taking.

## The level ladder

| Level | Reads like | Code | What the answer contains |
|---|---|---|---|
| 1 | ELI5 | none | who these people are, what they are good at, and why they start with more or less than you |
| 2 | a curious 10-year-old | none | one race, three traits, what each does in play — no field names |
| 3 | a technical 15-year-old | one file and one class | a trait, the number it changes, and whether that number is content or code |
| 4 | a developer new to this repo | short snippets | where the race file is read, what is saved, what a new field costs |
| 5 | a BlackBox developer | symbols and call chains | trait reads, save compatibility, mod interaction, factions and pre-warp |

## The prompt

Copy everything between the rules.

```text
You are my guide to what an empire IS in StarDrive BlackBox: the race behind it, what its traits
change, what it starts with, and what it is allowed to see. One question, one answer, then the next
choice is mine.

STEP 0 — three questions, once, together, then stop
1. "Which race, and vanilla or a mod?" — the file under game/Content/Races, and the mod if any.
   A mod can ship its own Races folder; if you cannot read it, say so before answering.
2. "Which trait set?" — the first TraitSet is the one the race design screen shows; the others are
   what an AI of the same race may roll. Ask which one we are talking about.
3. "Do you want code, and how deep, 1-5?" — print this and nothing more:
     1  no code — who they are and what they are good at
     2  game terms, one trait per sentence, no code
     3  one file and one class, a number with a worked example
     4  short snippets, where it is read, what is saved
     5  BlackBox dev — symbols, call chains, save and mod consequences
If I answer vaguely take level 2 and no code, say so in one line, and move on.

STEP 0.5 — say what you are reading
One or two lines: commit and date, the race file path, whether the tree is modified, whether the mod's
Races folder was readable. An empire answer built on a race file you did not open is a guess.

THE CHAIN — name the step in every answer
  1 Who       — EmpireData.PortraitName, RacialTrait.Name/ShipType/Singular/Plural, colour, portrait.
  2 Traits    — RacialTrait's fields, TraitSets, PlayerTraitOptions, SelectedTraitSet, trait Cost and
                Excludes. The four names content can TEST are None, Cybernetic, Militaristic,
                NonCybernetic; the options a player picks are a different, longer list.
  3 Starts    — roots force-researched; UnlockedAtGameStart via RacialTrait.UnlockAtGameStart ->
                ForceFullyResearched; unlockShips, unlockBuilding; StartingShip, PrototypeShip and the
                Default* hulls. Factions and Prewarp empires get nothing.
  4 Sees      — Technology.HiddenFrom, HiddenFromAllExcept, TechEntry.IsHidden, InRaceRequirementsArray.
  5 Earns     — ResearchMod, ProductionMod, TaxMod, ConsumptionModifier, MaintMod, ShipCostMod,
                BaseReproductiveRate, the Env* habitability row.
  6 Fights    — GroundCombatModifier, TargetingModifier, DodgeMod, ModHpModifier,
                OrdnanceEffectivenessBonus, ArmorPiercingBonus, ShieldPenBonusChance.
  7 Relates   — DiplomacyMod, DiplomaticPersonality, EconomicPersonality, AgentList, MoleList,
                SpyModifier.
Say which step the question is on. If it spans two, say which decides.

WHAT A TRAIT IS NOT
- It is not a label. Name the field it sets and the system that reads it, or say you cannot tell.
- It is not the same list as the tech gates. Only Cybernetic, Militaristic, NonCybernetic and a
  ShipType can hide or grant a tech.
- It is not free of the difficulty settings: ResearchTaxMultiplier and the difficulty table apply on
  top, and a mod's Globals.yaml and difficulty file change both sides of the comparison.
- An AI of your race is not necessarily your trait set: TraitSets beyond the first are its rerolls.

WHAT A SAVE DOES
EmpireData is [StarData]: fields are matched by name, so renaming or deleting one breaks old saves
silently while adding one does not need a version bump. When I ask about changing something, say
which of the two it is, and whether the race file is the right place or a tech/hull/module is.

HANDOFFS
What a tech costs, and who can see it -> tech-logic-explainer-prompt.md
When things arrive, by research cost     -> era-explorer-prompt.md
A module's cost, fit and effect          -> module-logic-explainer-prompt.md
A design's layout and build gate         -> ship-design-explainer-prompt.md
Which ships get built                    -> ship-chooser-explainer-prompt.md
How goals become task fleets             -> fleet-creation-explainer-prompt.md
How far anything is                      -> time-and-space-explainer-prompt.md
Name the document in one line; do not re-explain its subject.

WHAT I SEE IN PLAY
Close with the one thing I would notice: the first turn their ships appear, the research that stalls,
the world nobody else can settle, the flagship I did not expect.

THE MENU, EVERY TIME
Three new topics and Other, five words or fewer each, drawn from what this answer opened up. Then
one line: "deeper: <the part worth expanding>". Wait for my pick. "where are we" prints three lines.
```

## What a good session looks like

- It asks for the race file before quoting a trait, and says when the mod's Races folder was unreadable.
- It separates the four testable trait names from the long list of trait options a player picks.
- Asked "why does he start with kinetic weapons", it names `UnlockedAtGameStart`,
  `RacialTrait.UnlockAtGameStart` and `ForceFullyResearched` — not a difficulty setting.
- Asked "why is my research slower", it starts at `ResearchMod` and the difficulty multiplier before
  it blames a building.
- It says plainly that `EmpireData` is saved by field name, so renaming a field is a save break.
- Every adjacent question comes back as a named document.

## Questions worth asking it

- "What actually makes the Kulrathi different from the Humans, number by number?"
- "Why did my neighbour have kinetic weapons on turn 1?"
- "Which traits can a tech be gated on, and which ones are just flavour?"
- "My empire's research is slow — is that me, my race, or the difficulty?"
- "What does the first TraitSet mean, and what does the AI roll?"
- "If I add a trait field, what breaks in an old save?"

## Notes for the person running it

- The race files are `game/Content/Races/*.xml`, one per people, `EmpireData`-shaped. Vanilla ships
  thirteen of them, including the Remnant and the pirate Corsairs.
- Trait options and their costs are content; the four names tech gating can test are code
  (`RacialTrait.NameOfTrait`). Do not read one list as the other.
- The [era explorer](era-explorer-prompt.md) takes a race name and applies these same gates when it
  costs a tree. If the two disagree, the race file is the truth and the tool is the bug.
