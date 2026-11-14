# Building and refreshing the concept map — a copy-paste agent prompt

Paste the prompt below into an AI assistant that can read this repository. It produces
`docs/concept-map.md`: roughly forty-six entries, each saying what a player-visible part of the game
means, where the decision is actually made, and where the numbers live. The same prompt doubles as the
refresh procedure — run it again later and it verifies every address and reports what moved.

It is an address book, not an explanation. Formulas stay in
[`ship-content-reference.md`](ship-content-reference.md), walkthroughs stay in the explainer prompts,
and known problems stay in [`code-findings.md`](../code-findings.md).

## Why this exists

The repository already maps itself twice, along two axes, and neither one answers the question people
actually arrive with.

- [`ARCHITECTURE.md`](../../ARCHITECTURE.md) maps **technology to code** — Rendering, UI, Audio, Input,
  AI, Save/Load, Modding. It is organised by layer, and it was written during the migration: it still
  describes .NET Framework 4.8, x86, XNA 3.1 and SunBurn, and it states there are no MonoGame
  references. The Jupiter line is x64, .NET 8, MonoGame 3.8. As an index of systems it is still the
  best page in the repo; as a description of the current stack it is wrong in its first paragraph.
- [`ship-content-reference.md`](ship-content-reference.md) maps **content fields to code** — every
  field of `.hull`, `.design`, module, weapon and tech XML, with the formulas that consume it, pinned
  to a commit.

Neither is organised by **what the player does**. "How does colonising work" has no address, and it
should. It runs across `AI/ExpansionAI`, `Commands/Goals`, `Universe/SolarBodies/Planet`,
`Universe/SolarBodies/Planet/Planet_ConstructionQueue.cs`, `GameScreens/ColonyScreen` and
`game/Content/PlanetTypes.yaml` — five folders, six decisions, one concept.

Two traps the layer-based document actively causes, both of which the map exists to kill:

- **There are no turns.** `UniverseParams.TurnTimer` is documented as *"seconds between Empire turns,
  every turn advances stardate by 0.1"*. The simulation is a real-time fixed timestep. A "turn" is an
  economic tick inside continuous simulation. Every newcomer and every agent gets this wrong first.
- **"Combat" is two unrelated systems.** Space combat is continuous and lives in `ShipAI.DoCombat`,
  `CombatAI`, `Weapon` and the collision pass. Ground combat is a tile grid behind `CombatScreen` and
  `TroopManager`. ARCHITECTURE.md's systems section does not mention ground combat at all. Any entry
  that says "combat = X" is wrong on arrival.

## Why the output is checked in, when the explainer prompts' output is not

`game-logic-explainer-prompt.md` and `colonization-ai-explainer-prompt.md` deliberately do not check
in their answers: an explanation drifts the moment a number moves, and a stale explanation is
indistinguishable from a correct one. An index is different. An address either resolves or it does
not, and that is a thing a script or a later pass can test. So the map is checked in, carries the
commit it was built from, and the refresh mode below is the test.

## The shape

Six clusters, wide by design — the core loop, the map, empire and economy, ships, opponents, framing.
Each entry has the same six labels in the same order, so a refresh can be mechanical and a diff is
readable:

```
### Founding a colony
In play: A colony ship arrives, and the planet becomes a colony with people, a build queue and a governor if you automate them.
Decides: Ship_Game/Universe/SolarBodies/Planet/Planet_Colonize.cs — Planet.Colonize
Read first: Planet.Colonize
Also: Planet.SetupColonyType; Empire.AssessColonyNeeds; Commands/Goals/MarkForColonization
Data: game/Content/PlanetTypes.yaml
Trap: The player does not choose the colony type — SetupColonyType asks the empire unless auto-colonize is off.
```

`Decides` is the whole point of the document. It is the place a change would be made, not the first
file that mentions the concept, and it is a symbol rather than a line number because line numbers rot
in a week and a moved symbol is a cheap repair.

## The prompt

Copy everything between the rules.

```text
You are building and then maintaining a concept map for StarDrive BlackBox: one file,
docs/concept-map.md, that answers "where is this decided?" for the things a player sees in the game.

This is an index, not an explanation. A good entry is six short lines. A good map is one a reader can
scan in two minutes and then jump from, correctly, in one hop.

WHAT THE MAP IS FOR
A reader who plays the game but has never opened the repository should be able to take a concept in
the game's own words — "colonising", "ship combat", "why my fleet lost", "where the money comes
from" — and land on the function that decides it, without reading anything else first.

WHAT THE MAP IS NOT
- Not a tutorial. No prose walkthrough, no worked examples, no "first it checks X, then it checks Y".
  That is what docs/kit/game-logic-explainer-prompt.md is for.
- Not a formula reference. Never restate a strength, cost, mass or power formula.
  docs/kit/ship-content-reference.md owns those, and duplicating them guarantees two versions that
  disagree.
- Not a bug list. docs/code-findings.md owns known problems. Link to it; do not summarise it.
- Not a file listing. If an entry would be "here are the files in this folder", it is not a concept.
- Not a duplicate of ARCHITECTURE.md's systems index. Where the layer view is the better answer
  (rendering, audio, input), the entry is two lines and a pointer.

WHICH MODE
There are two. If I do not say which, ask me in one line and wait.
  BUILD   — docs/concept-map.md does not exist or I have asked for a rebuild. Produce the whole file.
  REFRESH — the file exists. Verify every entry, repair what moved, report what changed. Do not
            rewrite entries that are still correct.

THE ADMISSION TEST — what counts as a concept
An entry earns its place only if all three hold:
  1. A player can name it in the game's own words, without knowing the code.
  2. There is one place that decides it, or at most two, and you can point at them.
  3. If someone changed it, something visible in play would change.
If it fails any of the three, it is a library, a folder or an implementation detail. Leave it out.

ENTRY SCHEMA — fixed. Six labels, this order, no extra labels, no prose between entries.
  ### <Concept name, in the game's words, sentence case, no code identifiers>
  In play: <one sentence. What the player sees or decides. No identifiers.>
  Decides: <path/from/repo/root.cs — Type.Symbol>
  Read first: <one symbol, the single best entry point>
  Also: <up to three, semicolon separated, path-not-repeated type of shorthand is fine>
  Data: <content files a modder could edit, or "none">
  Trap: <optional, one line. The thing people get wrong about this concept. Omit the label entirely
         if there is nothing worth saying — do not write filler.>

  Rules for the labels:
  - Decides is the place a change would be made, not the first file that mentions the concept. If
    three files are involved, say in Trap which one wins.
  - Read first must be the deciding symbol, not the highest-level caller and not the data class.
  - Data is only for files under game/Content or game/Mods. If the number is in C#, write "none" —
    that is a useful answer, because it tells a modder to stop looking.
  - Never write a line number anywhere. Cite path plus symbol. Line numbers are wrong within a week
    and a wrong line number is worse than no line number.

RULES FOR THE FILE
- The first lines are a title, one sentence of purpose, and the commit and date the map was built
  from, in this shape: "Built from commit <sha> on <date>. Refresh with docs/kit/concept-map-prompt.md."
- Then an Index: the six clusters as a linked list, one line each, with the entry count.
- Then the clusters in this order: I. The loop; II. The map; III. Empire and economy; IV. Ships;
  V. Opponents and AI; VI. Framing; VII. The machine.
- Number the entries continuously through the file, not per cluster, so a refresh can say "entry 27".
- Within a cluster, order by what a new player meets first, not alphabetically. Setup before steady
  state, colony before fleet.
- No code blocks. No tables. No formulas. No links except cross-document links to docs/ and
  ARCHITECTURE.md.
- Close with a "Not covered on purpose" section: three to six lines naming what was left out and
  which document owns it instead.

VERIFICATION — this is the part that makes the map worth having
For every entry, before you write it:
  1. Open the cited file. Confirm the symbol exists, by name.
  2. Confirm it is the decider: read enough of it to see the branch, the score or the assignment
     that produces the player-visible behaviour. If it only calls something else, follow the call.
  3. If the symbol does not exist, or you cannot open the file, do not guess and do not substitute a
     plausible-sounding name. Write the entry with "Decides: UNVERIFIED — <what you looked for>" and
     list it in the footer.
Never cite a file you have not opened in this session. Never cite a symbol from memory of this
codebase, of a previous session, or of StarDrive generally.

COVERAGE — the wide list. Verify each anchor; several will be wrong or renamed, and finding that out
is the job. Add concepts you find that are missing; drop ones that fail the admission test.
Paths are repo-root-relative except where shortened to the folder that owns the file (Planet/,
SolarBodies/, Audio/); resolve them by filename with a find, never by trusting the prefix.

This list and docs/concept-map.md are kept in step in both directions: BUILD fills the map from the
list, REFRESH folds what it learns back into the list. A concept that exists only in the map is lost
the next time anyone builds.

I. The loop
  1  A frame, and the simulation step inside it   — Universe/UniverseScreen/UniverseObjectManager.Update
  2  "Turns" are economic ticks, not turns        — Universe/UniverseParams.TurnTimer
  3  Screens and the screen stack                 — GameScreens/ScreenManager.cs
  4  The UI thread and the simulation thread      — UniverseScreen.RunOnSimThread; Threading/Parallel.cs
  5  Starting, saving and loading a game          — GameScreens/Program.cs; Data/Binary/BinarySerializer.cs

II. The map
  6  Generating the universe                      — Universe/UniverseState.cs; Planet/Planet_Generate.cs
  7  A solar system                               — Universe/SolarSystem.cs; Planet/SunZoneData.cs
  8  A planet                                     — Universe/SolarBodies/Planet/Planet.cs (partials)
  9  Where things are, and what touches what      — Spatial/SpatialManager.cs; Qtree.Collision.cs
  10 Borders and influence                        — Empire_Borders.cs; Universe/InfluenceTree.cs
  11 Sensors and fog of war                       — UniverseObjectManager.UpdateAllSensors; ExplorableGameObject.cs

III. Empire and economy
  12 An empire                                    — Empire.cs and its partials; EmpireData.cs
  13 Founding a colony                            — Planet/Planet_Colonize.cs — Planet.Colonize
  14 What a colony produces                       — SolarBodies/ColonyResource.cs; Planet_Resources.cs
  15 The build queue                              — Planet/Planet_ConstructionQueue.cs; SolarBodies/SBProduction.cs
  16 Money, upkeep and the budget                 — AI/EmpireAI/Budget.cs; game/Content/Budgets.yaml
  17 Research and unlocking tech                  — EmpireResearch.cs; game/Content/Research.yaml
  18 What you are allowed to build                — Empire_ShipsWeCanBuild.cs; TechEntry.cs
  19 Relations, trust and war                     — Gameplay/Relationship.cs; Empire_Relationship.cs
  20 Diplomacy actions                            — AI/EmpireAI/EmpireAI.DiplomacyOffers.cs
  21 Espionage and infiltration                   — AI/EmpireAI/EspionageManager.cs; Espionage/*.cs

IV. Ships
  22 Design, hull, module, tech: how a ship exists — Ships/ShipDesign.cs; ShipHull.cs; ShipModule.cs
  23 A ship's numbers                             — Ships/ShipDesign_Stats.cs; ShipStats.cs
  24 Ordering a ship around                       — Ships/OrderType.cs; AI/ShipAI/ShipAI.Goals.cs
  25 Moving a ship                                — Ships/Ship_Movement.cs; PathFinder/Astar.cs
  26 Space combat                                 — AI/ShipAI/ShipAI.DoAction.cs — ShipAI.DoCombat
  27 Damage, shields and destruction              — Shield.cs; Gameplay/Weapon.cs; ExplosionManager.cs
  28 Fleets and fleet orders                      — Fleets/Fleet.cs; Fleets/FleetPatrol.cs
  29 Ground combat and invasion                   — GameScreens/CombatScreen/CombatScreen.cs; SolarBodies/TroopManager.cs
  30 Trade, freighters and supply                 — Empire_Trade.cs; Ships/Ship_Trade.cs; Ships/SupplyShuttles.cs
  31 Mining and finite resources                  — Ships/MiningBays.cs; Planet/Mineable.cs
  32 Shipyards, stations and orbitals             — Planet/Planet_BuildDefenses.cs; SpaceStation.cs

V. Opponents and AI
  33 The empire AI: one planner per domain        — AI/EmpireAI/EmpireAI.cs and its Run*Planner partials
  34 Threat assessment                            — AI/ThreatMatrix.cs; AI/DefensiveCoordinator.cs
  35 How a single ship decides                    — AI/ShipAI/ShipAI.DoAction.cs; AI/ShipAI/AIState.cs
  36 Pirates, remnants and minor factions         — Pirates.cs; Remnants.cs; Commands/Goals/PirateAI.cs

VI. Framing
  37 Difficulty and racial traits                 — EmpireDifficultyModifers.cs; Data/RacialTrait.cs
  38 Events, anomalies and artifacts               — StoryAndEvents/RandomEventManager.cs; AnomalyManager.cs
  39 Notifications and the event log              — StoryAndEvents/NotificationManager.cs
  40 The in-game Codex                            — Codex/CodexScreen.cs; game/Content/Codex.yaml
  41 Mods overriding vanilla                      — ModManager.cs; Data/GameContentManager.cs
  42 Text and localisation                        — Data/Localizer.cs; game/Content/GameText.yaml

VII. The machine — thin entries, two or three lines each, pointing at ARCHITECTURE.md
  43 Drawing a frame                              — GameScreens/ScreenManager.cs; Graphics/DeferredRenderer.cs
  44 Particles and explosions on screen           — Graphics/Particles/ParticleManager.cs
  45 Audio                                        — Audio/GameAudio.cs; Audio/NAudio/NAudioPlaybackEngine.cs
  46 The content pipeline                         — Data/ResourceManager.cs; Data/RawContentLoader.cs

BUILD PROCEDURE
Work one cluster per pass, in order. After each cluster, check: does every entry name a player-facing
concept, and does every Decides line point at something you opened? If a cluster needs more than
fifteen entries, it is being sliced by folder rather than by concept — merge them.
Do not hold the whole map in one response if the session is interactive: produce clusters I-III,
then IV-VII, then the index and the footer. Say which part you are writing.

REFRESH PROCEDURE
1. Read the existing docs/concept-map.md. Note the commit it was built from.
2. For every entry, verify only the two things that rot: the file path and the symbol name. Open the
   file, confirm the symbol. Do not re-read the whole codebase.
3. Classify each entry: OK, MOVED (path changed), RENAMED (symbol changed), GONE (neither exists),
   or UNVERIFIED (could not open).
4. Repair MOVED and RENAMED in place. For GONE, look for the successor symbol — if there is one, fix
   the entry and note it; if not, delete the entry and put it in the report.
5. Re-run the admission test on nothing else. Do not rewrite In play, Trap or Data lines that are
   still true. A refresh that rewrites correct prose is a refresh nobody can review.
6. Fold the result back into the coverage list in this file, under the rules below. Skip this step
   only if nothing in the set of concepts changed.
7. Update the commit and date line in the map.
8. Report a short table: entries checked, repaired, deleted, added, still unverified. Then list the
   repaired ones by number so I can see what moved.

FOLDING BACK INTO THIS FILE
You are allowed to edit the coverage list in this file, and only these three ways:
  - append a concept you added to the map, in its cluster, in the same shape as its neighbours
  - annotate a concept you merged or renamed, in place, with the date
  - delete a concept only if its code is gone and it has no successor
Never delete a seed entry because it was hard to verify. That is UNVERIFIED, not a finding, and
quietly shrinking this list is how a wide map becomes a narrow one. Numbers may shift when you
insert; if they do, state old-to-new for the shifted entries in the report. Change nothing else in
this file — not the rules, not the procedures, not the tone.

FINISH
End every run with five lines and nothing more:
  - the file written, entries per cluster, total
  - every UNVERIFIED entry, by number and what was missing
  - any concept from the coverage list you dropped or merged, and why
  - whether you edited this file's coverage list, and exactly which concepts
  - the commit read

Tone: terse. The map is read by someone with a question, not someone browsing. Short labels beat
complete sentences, and an empty Trap is better than a invented one.
```

## What a good map looks like

- One screen per cluster. You can find "ship combat" and see, without scrolling, that it splits into
  space and ground and which file decides each.
- `Decides` never points at a caller. If it did, the reader would arrive one call too early and have
  to search again in the file they were just sent to.
- Every `Data:` line is either a real content path or the word `none`. A modder can tell from the map
  alone whether the number they want is tunable.
- No line numbers, anywhere. Grep the finished file for `:L` and `#L` — both should return nothing.
- The traps read as surprises, not definitions: "the player does not choose the colony type", "there
  are no turns".
- Someone who plays the game and has never read the code can get from a concept to a function in one
  hop, and does not need to read the entry's neighbours to do it.

## Notes for the person running it

- Expect it to be wrong about several anchors on the first pass. The coverage list above was written
  from a directory scan, not from opening every symbol, and the prompt is explicit that the agent
  verifies rather than trusts it. An entry that comes back `UNVERIFIED` is the process working.
- Rough cost: one cluster per pass is a comfortable unit. The whole file is around six hundred lines
  of output; run it in two or three passes rather than one.
- Refresh is cheap — hours of work becomes a check of about ninety file paths — so run it before any
  release branch bump, and after any rename that touches `Ship_Game/`. There is no schedule worth
  setting; the map tells you when it is stale when an address stops resolving.
- The map will overlap `ARCHITECTURE.md` §5 deliberately, in cluster VII only, and those entries are
  two lines and a pointer. If anyone starts growing them, that content belongs in `ARCHITECTURE.md`
  and the map should shrink back.
- If a concept keeps failing the admission test — it has no single decider, or nobody can name it from
  the game — that is a finding, not a gap. Note it in the footer's "Not covered on purpose" rather
  than filling the entry with three competing anchors.
- This is the one doc here that edits itself. Refresh is allowed to extend the coverage list in this
  file and nothing else in it, so the seed stays a record of everything ever considered rather than a
  snapshot of one directory scan. If you would rather review those additions yourself, change step 6
  of the refresh procedure to "report the proposed additions" and it stops touching this file.
