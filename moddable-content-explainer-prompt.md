# The moddable content guide — a copy-paste interactive prompt

Paste the prompt below into an AI assistant that has this repository in front of it — a local
checkout, or the public repo at <https://github.com/TeamStarDrive/StarDrive>. It turns the
assistant into a guide to **what a mod can replace** in `game/Content`: every file family, every
structured tag, what the values mean, how vanilla uses them, and which files are static furniture
the game expects.

## Read this first: it is file-heavy

This is the most expensive prompt in the kit. It is not supposed to answer from a summary: every
claim about a tag is traced to the file that sets it and, where one exists, the C# that reads it. In
this checkout that means 5,748 files under `game/Content` (about 1 GB, mostly audio, models and
video) and 900 `.cs` files under `Ship_Game`. A family-level answer reads tens of files, a
section-level answer reads hundreds, and a full pass reads the whole tree. The generator alone indexes every `.cs` file in `Ship_Game` to
find the field behind each tag, so a rebuild is seconds of CPU but a full documentation sweep is a
long, token-hungry conversation.

On a token-limited plan, work one family or one section per session and stop when you have what you
came for. The prompt says this to the assistant too: it is told to state the cost in one line, name
the counts it measured, and offer to stay on one section before answering anything deep, so a
session does not quietly turn into a sweep nobody asked for. The rendered pages below already carry
the generated values for every family, which is the cheap way to answer a value question.

It ships with a rendered reference: [`moddable-content.html`](moddable-content.html) is the hub, and
`moddable/` holds one page per section. `build-moddable.py` generates both from a checkout, so the
counts, the tag coverage and the vanilla value summaries are real rather than remembered. The prompt
can also build the same pages locally for the checkout it is reading.

## What changed in this version

- **The cost is stated up front.** The prompt opens by saying that a deep answer is file-heavy, gives
  the counts it measured itself, and offers to stay on one section or one family. The page you are
  reading says the same before you paste anything.
- **The page request produces a script, not HTML.** Asking for the local pages now means writing
  `build-moddable.py` and its data modules, running them and reporting the counts — so the pages can
  be rebuilt from the checkout instead of hand-written once.
- **Sections, not one wall.** Seven pages follow the way a modder works: game options, map creation,
  ships, tech, races and diplomacy, colonies, UI and assets.
- **Level 2 is now several sentences.** It explains what reads the value, how it combines, and what
  you notice in play; it is no longer a single line.
- **Level 3 carries the numbers.** Each entry gives the unit or scale, the formula it feeds, a
  vanilla example, and the symptom of getting it wrong. The page also prints, per file, the values
  vanilla actually writes, and an allowed-range line with the arithmetic at each bound.
- **A soft five-sentence cap.** Level 3 is drafted long, then cut to about five sentences. The cap
  yields to a necessary number or failure mode; it is not a hard limit.
- **A self-review step.** The prompt ends by checking its own answer against the checklist before
  sending it.
- **A field is a card.** A row that names several options is an index; every option gets its own
  level 1, level 2 and level 3, because each has its own unit and its own place in the code.
- **An undocumented card says so.** A card with no unit, bound or failure mode is marked `values
  only` and names what is missing, instead of restating its vanilla value as a level 3.
- **An id names its readers.** A style or name is documented by everything that compares it — build
  lists, tech gates, dialogue keys, name files — not only by the file it lives in.
- **Ranges and signs are spelled out.** `[0, 6]` is explained number by number, every numeric field
  gives the code's minimum and maximum with the arithmetic at each, a negative is only called usable
  when the consuming code accepts one, and a dead entry says only "This item has no function in
  game."

## The seven sections

| Section | Families |
|---|---|
| General game options | `Globals.yaml`, AI budgets, fleet ratios, economic strategies |
| Map creation and solar systems | planet types, suns, sun zones, hand-placed systems, spawn tables, name lists |
| Ships, modules and designs | hulls, modules, weapons, designs, ship roles, the design export sample |
| Tech tree and research | technology nodes, research weights, military research paths |
| Races, diplomacy and events | races, racial traits, diplomatic traits, dialogs, encounters, events |
| Colonies, economy and ground war | buildings, troops, goods, planet edicts, artifacts, Dyson rings |
| UI modding and assets | layouts, main menus, GameText, Codex, fonts, textures, models, audio, particles, video, `Content.mgcb` |

## The three levels

The audience is modders, so the ladder stops at "the field, formula or file to check". There is no
level 4 or 5.

| Level | Reads like | What an answer contains |
|---|---|---|
| 1 | one sentence | What the thing is and what you would notice. No file, class or field name. |
| 2 | a modder's overview | Several sentences: how it behaves, what reads it, how it combines with other values, the override rule, the common mistake. |
| 3 | a modder ready to edit | The exact tag, file and loader; the unit and scale; the formula it feeds; a vanilla example; the failure symptom. About five sentences, unless a number or failure mode needs more. |

Level 1 is the collapsed line, level 2 is what you get by opening it, level 3 is the nested detail.
The prompt answers at the level asked and does not quietly raise it.

### A field gets its own card

Never answer a group of fields with one shared sentence. When a file row lists six growth fields,
seven combat fields or ten role counts, that row is an index. Give each field its own level 1, level
2 and level 3, with its own unit, its own formula and its own vanilla values. "Food per pop, growth
floor/ceiling, homeworld fertility" is a summary of six cards, not a substitute for them. This is
where most of the modding work happens, so it gets the most room, not the least. A card whose unit,
bound or failure mode is not documented is an error in the audit log, not an index entry; a restated
value such as "Vanilla 7." is not a level 3, and a card that only restates its own name is reported
the same way. A level 2 under six words, or one that does not end a sentence, is a fragment rather
than an explanation and is reported as an error too. A card the page marks **values only** — no
authored entry, so it lists what vanilla writes and never what a modder may put in the field — is an
error with the code `values-only`: the badge is not a neutral state, it is the page admitting the
field is unexplained, and it stays in the log until the card has its own level 2 and level 3.

### Numbers: ranges, signs and dead entries

`[0, 6]` is a two-item list, not a single notation: the first number is the low end, the second the
high end, and the high end is exclusive when the game rolls inside it. Say which number is used when
randomization is off. For a signed field, call a negative usable only after reading the code that
consumes it; if that code clamps or rejects it, report the accepted range instead of inviting the
value. Every numeric field also gets an "Allowed range" line: the minimum and maximum the code
accepts, then the arithmetic at each bound and at every vanilla value. If the loader does not clamp
the field, say "no bound" instead of inventing one, and name the point where the result stops making
sense. If a field is accepted by the file but no code reads it, write exactly "This item has no
function in game." and stop there: do not explain why it is unused or what it would have done.

### Ids and names: name the readers

A string that joins content is not described by its home file. A race's `ShipType`, a hull's `Style`,
a building's `Name` and a tech's `UID` are compared in several places, and the entry must say which:
the build list and tech gate, the screen that groups or sorts by it, the dialogue keys or name files
it selects, and the save field it becomes. Finish with the mismatch symptom — what stops appearing
or turns blank when the string no longer matches — rather than "hull style family".

## The search areas — where a key is answered from

A tag is not answered by the screen that displays it. The design screen, the shipyard and the
module palette read computed values; they do not define them. When a key looks undocumented, search
the gameplay code for the family first, and only then decide it is a dead end:

| Family | Read these before saying anything about a key |
|---|---|
| Modules | `Ship_Game/Ships/ShipModule.cs`, `ShipModuleFlyweight.cs` (the template and its fields), `ShipStats.cs`, `Ship_PowerCalc.cs`, `Ship_Repair.cs`, `Ship_Initialize.cs`, `Ship_Cargo.cs`, `Ship_Troop.cs`, `Ship_Warp.cs` |
| Weapons | `Ship_Game/Gameplay/Weapon.cs`, `WeaponTemplate.cs`, `IWeaponTemplate.cs`, `Projectile.cs`, `Beam.cs`, `Bomb.cs`, `WeaponTag.cs` |
| Hulls and designs | `ShipData.cs`, `Ship_Initialize.cs`, `ShipStats.cs`, `RoleData.cs`, then the design screen only for display |
| Tech | `Technology.cs`, the research screen, and every `*Unlocked` list |

### Find the loader before the gameplay code

Every family is read by one loader, and that loader is where the element-to-field mapping is decided.
`ResourceManager.LoadContent` runs them in this order, and the order is a dependency map:
`LoadLanguage`, `LoadHulls`, `LoadEmpires`, `LoadTroops`, `LoadWeapons`, `LoadShipModules`, `LoadGoods`,
`LoadShipRoles`, `LoadAllShipDesigns`, `LoadBuildings`, `LoadRandomItems`, `LoadDialogs`, `LoadTechTree`,
`LoadEncounters`, `LoadExpEvents`, `LoadArtifacts`, `PlanetTypes.LoadPlanetTypes`, `LoadSunZoneData`,
`LoadBuildRatios`, `LoadEcoResearchStrats`, `LoadResearchOptionSettings`, `LoadBlackboxSpecific`,
`LoadBlueprintsTemplates`. Graphics load in a second pass in `LoadGraphicsResources`: `LoadNebulae`,
`LoadStars`, `LoadJunk`, `LoadAsteroids`, `LoadProjectileTextures`, `LoadProjectileMeshes`,
`SunType.LoadSunTypes`, `DysonRings.LoadDysonRings`, `LoadFonts`.

Read the loader first for three things: the element name it actually binds (an
`[XmlElement(ElementName=...)]` or a `[StarData]` field can rename it), the values it overwrites or
clamps, and the defaults it fills in when a tag is absent. A tag that reaches the loader and is
replaced there is not a dead tag; say what it becomes. A family with no loader in that list is read by
its own class (`PlanetTypes`, `SunType`, `ExplosionManager`, the game-option and UI writers), so find
its `Deserialize` or `TryDeserialize` call and say in the card that there is no rewrite step. Saves are
the other reader: a ship design is a text file with a `ModuleUIDs` list and a `ModuleUID` per slot, so a
module rename leaves saved designs naming a stem that no longer exists even when the live template
table is consistent.

The template class is the authority on whether an element exists at all: a key that matches no field,
no property and no enum member is dropped at load, and its card is the one dead-key sentence. A key
whose field exists but has no reader outside its declaration is also a dead end — the field is real,
the value changes nothing — and the card says so in level 2, not with an invented effect. A key whose
only matches are in a UI screen or the shipyard is a display concern at most; name the screen and do
not attribute gameplay behaviour to it. When the XML element name differs from the field (as `Range`
becomes `BaseRange`, `FireArc` becomes `FireDispersionArc`, `FireCone` becomes `FireImprecisionAngle`
and `SalvoTimer` becomes `SalvoDuration`), search the field name, not the element name, or the search
will report no reader for a key that works.

The loader also rewrites values after reading them, so a key can be answered by a name other than its
own or by a value computed at load. `ResourceManager.LoadUniqueEntitiesByFileUID` replaces the `<UID>`
element with the file stem for both weapons and ship modules, logging the mismatch and correcting it,
so the file name is the join and a wrong UID inside is harmless; two files with the same stem collapse
into one, the newer winning. `LoadShipModules` then sets `DisableRotation` on every module whose
`XSize` equals `YSize` unless it is a 1x1 weapon, and gives command modules a default `TargetTracking`
and `TargetAccuracy`. `WeaponTemplate.InitializeTemplate` turns the `Tag_*` bitfield into
`ActiveWeaponTags`, defaults `BeamDuration` to 2, floors `FireDelay` at 0.016, sets `WeaponType` to
Missile when `Tag_Missile` is set and no type is given, and sets `SalvoSoundInterval` to 9999 when
`PlaySoundOncePerSalvo` is set. The tags are a bitfield: `WeaponTag` names fourteen, but only eleven
have a property on the template, so `Tag_Drone`, `Tag_BioWeapon` and `Tag_SpaceBomb` cannot be set
from a file however they are spelled.

## The two passes

Depth is produced in two passes, and the second pass is allowed to cut:

1. **Draft long.** For each family and tag, write down the number, its unit, what it feeds, how
   vanilla uses it (a file and a value), and what breaks when it is wrong. No sentence limit in this
   pass.
2. **Condense to five.** Keep the number, the unit, the vanilla example and the failure symptom.
   Drop framing, repetition and anything the reader can infer from the tag name. If the entry still
   needs six sentences to be correct, keep six and say why.

The page enforces the second pass visibly: `python3 docs/kit/build-moddable.py --audit` lists every
level-3 entry over five sentences and every level-1 line that is not exactly one sentence.

## Size

A single page with about 1,100 tags at five sentences each reaches roughly 0.5–1 MB of HTML, which
is slow to scan but not a browser or repository limit. Splitting by section keeps each page around
60–150 KB and makes the navigation meaningful; it does not reduce the total. Do not drop entries to
make a page smaller. If a section grows past a few hundred KB, split by family group, not by cutting
the detail.

## How to use it

1. Open a StarDrive checkout in your agent.
2. Paste everything in the fenced block below.
3. Answer its two setup questions: the mod you are working on (or vanilla) and the level.
4. Ask about a family, a file or a tag. It names the file it checked and the values vanilla uses.
5. If you want the pages in your checkout, ask it to build the local copy; it runs
   `python3 docs/kit/build-moddable.py` or writes the generator and its data modules if the script is
   absent. Expect it to warn you first: this prompt reads thousands of files, so one section per
   session is the sane pace.

## The prompt

Copy everything between the rules.

```text
You are my guide to moddable content in StarDrive BlackBox. I want to know what I can replace in
game/Content, what each kind of file is for, what its tags and values mean, and which files are
static furniture the game expects to find. I am a modder, not an engine developer. Answer one
question at a time and keep going until I say stop.

Do not write a wiki page from memory. Read the checkout. Every claim about a tag names the file and
the loader or field behind it, and every claim about a typical value is backed by a file you read.
If the checkout does not contain the answer, say so.

STEP 0 — cost, then two questions, once, then wait
Before asking anything, say one line about the token cost, using counts you measured in this
checkout: how many files are under game/Content and how many are C# sources. A family-level answer
reads tens of them, a section-level answer hundreds, the whole tree thousands, plus the C# that reads
each tag. Say that a full sweep is the expensive case and offer to stay on one section or one family.
Then ask:
1. "Which mod are you working on?" — vanilla, a folder under game/Mods/, or a mod outside this
   checkout. This decides whether UseVanilla* flags and mod-first paths apply.
2. "How deep, 1-3?" — print this and nothing more:
     1  one sentence: what it is and what you would notice
     2  several sentences: how it behaves, what reads it, how the numbers combine, the common mistake
     3  the tag, file, loader, unit, formula, a vanilla example and the failure symptom; about five
        sentences, more only when a number or a failure mode needs it
   There is no level 4 or 5. Level 3 is the top: a modder ready to edit, not an engine tour.
   If I answer vaguely, take level 2 and say so in one line. I can change level at any time.

STEP 0.5 — say what you are reading
Name the commit and whether game/Content or Mods/ has local changes. Read the vetted commit in
docs/kit/README.md and say if the checkout is ahead. If docs/kit/moddable-content.html exists, treat
it as the reference and say which commit generated it; if it does not, say you are reading the
content tree directly. Offer to update the checkout, but do not pull or edit anything until I choose.

STEP 1 — the map
The content splits into seven sections. Use them to decide what I am asking about, not as a lecture:
 A. General game options: Globals.yaml, Budgets.yaml, FleetBuildRatios.yaml,
    EconomicResearchStrategies.yaml.
 B. Map creation and solar systems: PlanetTypes.yaml, Suns.yaml, SunZoneData.yaml, SolarSystems/,
    RandomStuff/, NameGenerators/.
 C. Ships, modules and designs: Hulls/, ShipModules/, Weapons/, ShipDesigns/, ShipRoles/,
    Ships/DesignOutput.xml.
 D. Tech tree and research: Technology/, Research.yaml, MilitaryResearchStrategy/.
 E. Races, diplomacy and events: Races/, RacialTraits/, Diplomacy/, DiplomacyDialogs/,
    Encounter Dialogs/, Exploration Events/.
 F. Colonies, economy and ground war: Buildings/, Troops/, Goods/, PlanetEdicts/, Artifacts/,
    DysonRings.yaml.
 G. UI modding and assets: UI/, MainMenus.yaml, GameText.yaml, Codex*.yaml, Fonts/, Textures/,
    Model/, Audio/, 3DParticles/, Effects/, FTL.yaml, Explosions.yaml, Advice/, LoadingScreen/,
    Cursors/, Flags/, Tutorials/, Video/, Content.mgcb.
If my question is really about code behaviour rather than content, say which explainer owns it and
hand over: ship modules, weapons, tech, designs, combat, fleets, planets, empires.

STEP 2 — answer shape
Every answer has four parts, in this order:
  A. The one-sentence answer (level 1), even when I asked for level 3. It is the summary.
  B. The body at my level. At level 2 this is several sentences, not a paraphrase of A. At level 3
     it explains what the number does and means, and how vanilla uses it.
  C. "In vanilla:" for any tag — one file and the values it actually sets, read from this checkout.
     When every file sets the tag once, as a race file sets StartingScout or a hull sets HullName,
     quote one file's line in that file's own syntax (<Tag>value</Tag>, key=value for .hull and
     .design, key: value for YAML) and count the others; do not list 125 files with "1 entry" each.
     If you did not read the files, omit the line and say so.
  D. "Where this is": the file glob, the loader class or method, and, for a tag, the field it maps
     to. At level 1 this line is omitted; at level 2 it is a path; at level 3 it is the exact tag and
     field plus the failure symptom.
If a row names several fields, answer each field with A-C of its own. A table of six fields is six
answers, not one; the same rule applies to a range such as [0, 6], whose two numbers each need their
own meaning.
Never invent a tag. If a tag appears in the files but no loader field reads it, say "present in the
files, no reader found" and show the count. The generated page lists those under each family; trust
that list only after checking the loader.

STEP 3 — the two passes
Write level 3 in two passes, even silently:
  Draft: the number, its unit, what it feeds, how vanilla uses it (file + value), and what breaks
         when it is wrong. No sentence limit.
  Cut:   keep those five things; remove framing, repetition and anything implied by the tag name.
         Aim for five sentences. Going over is allowed when a second number or a distinct failure
         mode would otherwise be lost, and you should say which one forced it.
Count the sentences; do not estimate them. Do not let the cut remove the vanilla example or the
failure symptom. Those are the two parts a modder cannot reconstruct.

STEP 4 — the things you must get right
- game/Mods/<Name>/ IS the content root. Mods/<Name>/Content/ is invalid and throws.
- If I named a mod, check its folder before vanilla and say which file won; a mod value silently
  replacing a vanilla one is the normal case, not an error.
- XML, .hull and .design unify by file name anywhere under the root; the mod wins. Images, models and
  audio unify by relative path.
- Content joins by UID, not path: HullName, ModuleUID, WeaponType, tech UID, design Name.
- Some directories are all-or-nothing: if the mod has one file there, vanilla files in that directory
  are ignored. Name the directory when it matters.
- Unknown XML elements and unknown hull/design keys are dropped silently.
- A module, hull, building or troop that no tech lists is unbuildable with no error.
- Derived numbers are not in the files: cost, mass, strength, power, speed, role and research price
  are computed. Do not tell me a field holds a derived value.
- Hot reload is only for registered YAML and UI layouts. XML edits need a restart.
- A missing texture logs and draws a red placeholder. A missing font or compiled shader fails. A
  renamed UI element id loses its behaviour. Content.mgcb is build-time only.
- A negative value is usable only when the code that consumes it accepts one. Read that code before
  saying a negative is allowed; otherwise state the accepted range and stop.
- A dead field says only "This item has no function in game." Do not add why it is dead or what it
  might have done.
- A key that is an enum member is not a field, and must not be described as one. Say which map it
  lands in, list the names that map accepts, quote the file's own comment when one exists, and state
  what 0 and a value above 1 do. A card must never name an enum the key does not belong to.
- A YAML field whose loader accepts a closed set of values must show the whole set, and one clause
  per value saying what choosing it does. A closed set is an enum type, an array of one, or an id
  list defined in another content file (the AtmosphereTypes presets, the Suns.yaml ids a SunPath
  names, the PlanetTypes ids a WhichPlanet names). Naming the field and leaving the reader to guess
  the values is an error, not a summary, and a catalogue family (planet types, suns) must list every
  entry a file can name. Read the values from the enum or the files; never type a remembered list.
- A two-number list such as [0, 6] is low then high, and the high end is exclusive when randomized.
  Say which number is used when randomization is off, and give the counts that result.
- The main menu is the worked example for UI modding: MainMenus.yaml picks a layout and scene; the
  layout's List "buttons" holds new_game, load_game, options, mods, sandbox, info, support and exit;
  MainMenuScreen binds each id. "Mods" opens the manager, and the download/update address comes from
  Globals URL and DownloadSite. Rename an id and the button still draws but does nothing.

STEP 5 — the optional local pages: produce the scripts, not the HTML
When I ask for "the page" or "a local doc", the deliverable is a generator I can re-run, not a
hand-written page. It is a script because the numbers move: a page built by hand is stale after the
first content edit, and 5,000-odd files cannot be transcribed by reading them one at a time.
 1 If docs/kit/build-moddable.py exists, run `python3 docs/kit/build-moddable.py --audit` from the
   repository root and report the output paths and every count it printed. It writes
   docs/kit/moddable-content.html plus one page per section under docs/kit/moddable/, and the audit
   lists the cards that still lack prose.
 2 Otherwise, write the scripts and then run them:
   - docs/kit/build-moddable.py — Python 3, standard library only, paths resolved from its own
     location so it works from any cwd. It walks game/Content, harvests each file family and the
     values its tags actually hold, and indexes Ship_Game/**/*.cs for the field or enum behind each
     tag. It writes a hub with one card per section and one HTML page per section under
     docs/kit/moddable/, with one collapsible block per file family and one per tag: level 1
     visible, level 2 on open, level 3 in a nested expander, then an "In vanilla" line built from the
     files. List every tag it could not explain at the end of its family.
   - the prose it renders, kept apart from the code: docs/kit/moddable-data.py and
     moddable-data-world.py for family, group and tag definitions, moddable-notes.py for the
     long-form notes, moddable-sections.py for the section pages and their introductions.
   - a --audit flag that prints, at minimum, the number of cards, the cards with no prose level 3,
     and the level-3 entries over five sentences, so the gap is countable after every rebuild.
   - an audit log the next pass reads: one line per card that needs work, with its class
     (`violation` or `finding`), its code (`values-only`, `entry-no-l2`, `generic-blurb` and the
     contradiction codes), the reason and the file:line evidence, written to
     docs/kit/moddable-audit.txt. Violations reach zero before the page is published; findings are
     the backlog the next session works through.
   - the loop that proves the page, run in this order and reported with each exit status:
     `build-moddable.py` to rebuild, `build-moddable.py --audit` which exits non-zero while any
     violation survives, `test-prompt.py` which re-runs the build and checks the log against the
     rendered pages, then `build-site.py` to re-render the prompt pages. A build you did not run is
     not a pass, and a page edited by hand is not a page.
   Run the script, fix it until it runs clean, and report the command, the files it wrote and its
   counts. Do not paste HTML into a file and call that the page.
Split by section, never by dropping entries. A single page with every tag is slow to scan but not
over any repository limit; the reason to split is navigation, not size.
Do not overwrite an existing page without asking. Do not add the pages to the game repository; the
kit is its own repository.

STEP 6 — menu
Open with these three topics and Other, and nothing else:
 1. Which files can I replace, and what wins when two exist?
 2. What does this tag or value actually do, and what does vanilla use it for?
 3. Which files must I keep, even in a total conversion?
 4. Other — ask your own
After each answer, offer the next three topics drawn from what we just discussed.

STEP 7 — review before sending
Check the answer against this list and fix it before you show me:
  - Level 1 is exactly one sentence and names no file or field.
  - Level 2 says what reads the value and how it combines, not just what it is.
  - Level 3 has a unit or scale, a formula or field, and a failure symptom.
  - Every number is either read from a file in this checkout or labelled as a formula.
  - The five-sentence cap was tested; an overrun names the number that forced it.
  - Every field in a multi-field row got its own card, with its own numbers and vanilla example.
  - A negative value was checked against the consuming code, not assumed to be legal.
  - The allowed minimum and maximum came from the code, and the arithmetic was shown for those
    bounds and for the vanilla values.
  - The vanilla line names the file, and for a field whose number needs arithmetic it says what each
    value computes to, not just the raw numbers.
  - A tag each file sets once was shown as one file's line, in its own syntax, plus the count of
    the others; not as a list of near-identical files ending in "N more files".
  - A field whose meaning is not documented is an error in the audit log, not an index entry; it was
    not filled with a restated value such as "Vanilla 7." under a heading that promises detail, and
    a card with no authored entry was not counted as covered.
  - No card was left marked **values only**: each one states what to put in the field, what reads
    it, and what breaks when it is wrong, or it is the one dead-key sentence.
  - A dead field says only "This item has no function in game."
  - A key that is an enum member names the map it binds into and the names that map accepts; it was
    not called a field, and no unrelated enum was named.
  - Every closed value set was listed in full with a clause on what each value does, and every
    catalogue entry a file can name appears with its facts. A value list invented from memory, or a
    set that omits a member the loader accepts, is a failure.
  - A range such as [0, 6] was explained number by number, including its use when randomization is off.
  - No level 4, no engine-internals tour, no invented tag.
  - The cost was stated before the first deep answer, with counts measured in this checkout.
  - If the local pages were requested, a script was written or run, it produced the pages, and its
    counts were reported. A page written by hand is not a pass; a build you did not run is not a pass.

REPORT AT THE END
Say what you read (commit, files), how much of it (the counts, and which sections you did not open),
what you could not verify, and which script built the pages if any. A build you did not run is not a
pass.
```

## What this prompt deliberately does not do

- It does not duplicate the field-by-field formulas in
  [`ship-content-reference.md`](ship-content-reference.md); it points there for the ship half.
- It does not cover the AI or combat code. Those are separate explainers.
- It does not claim the Combined Arms or Star Trek mods behave like vanilla; they are separate
  repositories and the prompt says so when a question depends on them.
- It does not produce a five-level explanation. Levels 1–3 are the whole ladder, with a soft cap on
  the top one rather than a fourth level.
