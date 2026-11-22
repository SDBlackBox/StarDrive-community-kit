# Review: the moddable-content docs from a new modder's chair

**Reviewed:** the seven HTML section pages in this folder — `game-options.html`,
`map-creation.html`, `ships.html`, `tech.html`, `races-diplomacy.html`, `colonies.html`,
`ui-assets.html`. The Markdown files were ignored, as asked. I read the parent hub once for
context, but the findings below are about these seven pages.

**Who is reading:** a BlackBox player who can edit a text file, has a clear design vision, and
has never shipped a StarDrive mod. Not a programmer, but not afraid of a folder tree.

**The vision I kept in mind while reading:** a slower, heavier game — fewer and more expensive
capital ships, a custom race, a hand-built home system, a tech tree that gates the good hulls,
and a UI that matches the fiction. Each pass below is the same reader at a different moment.

**Method:** read all seven pages, then counted what is actually in the HTML so the impressions
could be checked. Counts are reproducible from the page source; the script used was a tag split
plus `grep` for the badge classes.

| Measure | Count |
|---|---:|
| Pages / tag cards | 7 / 1,065 |
| Content files covered | 5,735 |
| Cards labelled **values only** | 959 (90.0%) |
| Cards with an explicit "No traced reader yet" note | 811 |
| Cards with a level-2 explanation or range block | 397 (37.3%) |
| Cards with only a one-line summary and a gap note | 668 (62.7%) |
| Generated "In vanilla" lines | 904 (84.9%) |
| Copyable code blocks (`<pre class="code">`) | 7 — all in `colonies.html` |
| Pages with a "Start here" walkthrough | 1 — `colonies.html` |

**Verdict in one paragraph:** yes, these help — but as a reference library, not as a tutorial.
They are excellent once I already know the internal name of the thing I want to change, and weak
at the moment I only know the effect I want. The pages repeatedly tell me *what a value is* and
*what vanilla uses*; they rarely tell me *what happens if I change it*, and almost never show me
a complete file I can copy. For a first mod, that gap is the difference between "I can do this"
and "I will come back when someone writes a guide."

---

## Pass 1 — Cold open: "I have a vision. Where do I start?"

I arrived knowing the game, not the files. I want to decide which lever to pull first.

### Good (5)

1. **The seven-way split matches how I think about the game.** Game options, map, ships, tech,
   races, colonies, UI. Each page's lede is one sentence, so I can route "I want slower battles"
   to game options and "I want a new faction" to races without opening anything.
2. **Level 1 is genuinely skimmable.** Every card is a named, one-sentence summary. Across 1,065
   cards, with the filter and Expand/Collapse, I can survey a whole subject in a minute. That is
   the right shape for an eager reader with a broad idea.
3. **The generated "In vanilla" lines make the docs concrete.** 904 of 1,065 cards name a real
   file and the value it writes, e.g. `Hulls/Cordrazine/Cordrazine_Station_Small.hull — Size=28,28`.
   I am never left with an abstract key; I have a file to open.
4. **The section intros teach the mental model before the fields.** `map-creation.html` gives the
   generation order (star → orbits → zone → type → rolls → name); `game-options.html` gives the
   price order (module base → racial modifier → global multiplier). That lets me predict side
   effects before I touch a number.
5. **The docs admit what they do not know.** "values only" and "No traced reader yet" are honest
   labels, not invented behaviour. After years of wikis that guess, that is a reason to trust the
   cards that *do* have detail.

### Bad (5)

1. **Most of the library is a dead end for my actual idea.** 959 of 1,065 cards (90%) are
   "values only", and 668 (63%) have no level-2 explanation at all. My "slower, heavier capitals"
   idea lands on `ShipMaintenanceMultiplier` (well covered) but also on `RushCostPercentage`,
   which says "1 = pay the full price again" and nothing about what 0.5 or 2 does. The card is
   honest about the gap, but it still cannot answer the question I came with.
2. **The badges are never explained.** Every family carries `Tier 1`, `Tier 2` or `Tier 3`, and
   every page header counts `families`, `files` and `tags`. Nowhere in these seven pages — or in
   the hub's "How to read an entry" — is there a legend. Is Tier 1 easiest, most impactful, or
   load order? I cannot tell whether a Tier 3 family is advanced or just large.
3. **There is no on-ramp unless my idea is a colony.** `colonies.html` opens with "Start here —
   your first colony mod": the `Mods/<YourMod>/` root, the no-`Content/` rule, required fields,
   defaults, a code-read-name table, and common mistakes. The other six pages open with dense
   prose. So "add a building" has a path and "add a ship" — the more common fantasy — does not.
   (The hub explains the `Mods/` root, but not a first ship/tech/race walkthrough.)
4. **Code identifiers arrive before the plain-language payoff.** `GamePlayGlobals.Deserialize`,
   `ResourceManager.PlanetTypes`, `InternalSlotsHealthPercent < ShipDestroyThreshold`. The hub
   says "Nothing here is written for engine contributors"; these pages often read as if it is.
   I can skip the identifiers, but they are the most visually prominent thing on several cards,
   and they make the docs feel harder than the task.
5. **I cannot tell whether the docs match my game build.** The only provenance is
   `generated from: ef406fa04` — a commit hash. There is no BlackBox version, no date, and no
   changelog. If a patch changed a default, I have no way to know whether the page or my install
   is stale.

---

## Pass 2 — Execution: "I picked one value. Now make it work."

I have a target: double ship upkeep, then give my custom race a cheaper tech branch. I want to
edit, launch, and see the result.

### Good (5)

1. **The level-3 math often lets me choose a direction, not just a name.** `ShipDestroyThreshold`
   explains 0 = fight to the last internal module, 1 = die on any internal damage.
   `GravityWellRange` gives 8,000 units and says 0 removes blockades entirely. That is enough to
   predict play, which is what I actually need.
2. **Failure symptoms are spelled out, including the silent ones.** Unknown Globals keys are
   ignored with no warning; a `.hull` `Size` mismatch is not repaired; a missing tech makes a
   design unbuildable with only a log line; renaming a hull stem vs `HullName` dangles references.
   These are exactly the hours a first mod would otherwise lose.
3. **Override semantics are stated per family.** File name vs UID, XML unifying by file name,
   Globals inheriting key-by-key, and the two salvage flags forced off for mods. This is the
   part that silently breaks first attempts, and the docs do not hide it.
4. **The "copy the closest vanilla file" instruction is the right one — where it appears.**
   `colonies.html` says it explicitly and pairs it with real defaults (`Unique` and `Scrappable`
   are true, a building's `Strength` is 5). I would follow that instruction everywhere if every
   page said it.
5. **Save-baked values are called out.** Opponents, turn timer, trait points, starting richness,
   research-cost-by-size, globals: the docs tell me to test in a new game rather than chase a
   change that a save cannot see. That single warning prevents a very common false negative.

### Bad (5)

1. **Six of seven pages give me no copyable syntax.** There are seven code blocks in the entire
   920 KB, all on the colonies page, all showing root elements. For Globals, tech XML, `.hull`,
   race XML and UI YAML I get prose and an "In vanilla" line, but not the indentation, root
   element, or attribute form. I know the key and still cannot safely write the file.
2. **"Keep inside the vanilla span" is unusable when no span is shown.** `PlanetScale` shows
   `10.0`; `RushCostPercentage` shows `1`; `CloudsScale` shows `1.015`. The advice appears on the
   very cards that have only one data point. It protects me from nothing.
3. **There is no test loop.** No log path, no launch instruction, no "you will know it loaded
   when…", no reload behaviour except "restart" in the colonies mistakes table. "Enable the mod"
   appears once in 920 KB. I can make a correct edit and still have no way to confirm it.
4. **The internal noun is not the in-game noun.** I think "ship upkeep"; the field is
   `ShipMaintenanceMultiplier`. I think "rushing"; the field is `RushCostPercentage`. The filter
   searches the page text, so if I do not already know the internal noun I cannot find the card.
   There is no glossary or alias list.
5. **Depth depends on which section my idea lands in.** Colonies gives defaults, a hardcoded-name
   table and a symptom→cause→fix table. Game options and map creation give one-liners for many
   cards. The quality of my first mod would depend on the accident of which family it belongs to.

---

## Pass 3 — Maintenance: "It works. Now I want to expand it and keep it working."

My first ship and tech are in. I want to add a race, wire the unlock chain, and not break the
mod when the game updates.

### Good (5)

1. **The docs explain that ship stats are derived, not stored.** A design's price is the closure
   of its hull and module techs; shipyard offence/defence/power/speed are sums and formulas; the
   design file only records which UID sits in which cell. That stops me editing the wrong file.
2. **Shadowing and fallback rules are documented.** First encounter matching `Faction + Step`
   wins; two files with the same `Name` mean the later one wins; a missing design falls back to a
   vanilla name; duplicate UIDs shadow. These are real maintenance landmines, and they are named.
3. **The colonies hardcoded-name table is unusually precise.** Nineteen names read from code,
   what each id controls, and even the three ids that are assigned but unused. It tells me what is
   safe to rename and what must keep its vanilla name. Every section should have this box.
4. **Coverage counts let me size the work before committing.** 1,778 ship files, 3,425 UI/asset
   files, 192 tech files. For a total conversion, that is the difference between a weekend and a
   year, and the numbers are on the header rather than buried.
5. **Mod inheritance gives me a clean total-conversion path.** The hub's `UseVanillaShips/Techs/
   Weapons/Modules/Buildings/Races` flags and the per-family override rules mean I can replace one
   family without deleting the rest. The section pages consistently say what "replace" means.

### Bad (5)

1. **Coupled values are never linked to each other.** Tech `Cost` ↔ `Research.yaml` weights ↔
   `ChangeResearchCostBasedOnSize`; ship cost ↔ `ShipMaintenanceMultiplier` ↔
   `UseUpkeepByHullSize`; `PlanetTypes` index ↔ a system's `WhichPlanet`. They live on different
   pages with no "Related" section. I find the coupling only by reading everything, after I have
   already broken it once.
2. **There is no consolidated "do not touch / safe to rename / unfinished" list outside colonies.**
   The docs imply all fields are fair game, then mention in passing that `NewRenderer` is
   work-in-progress, three building ids are unused, and four empire names are special-cased in
   code. Those are exactly the things a maintainer needs in one place per section.
3. **No migration guidance for my own mod across game updates.** Saves keep the globals they were
   created with and `[StarData]` fields are matched by name, but there is no advice on what to do
   when the doc's commit hash changes, no changelog, and no diff view. A published mod has no
   documented update path.
4. **Search is page-local.** The filter script hides cards within the current page only; there is
   no cross-page result set and no "show me everything that affects upkeep". With 1,065 cards I
   must first guess the right section, which is the same problem the seven-way split was supposed
   to solve.
5. **There is no worked end-to-end example across families.** Colonies has the only vertical
   slice. Nothing shows "one new hull + one module + one tech unlock + one race default design"
   as a single small mod. The rest is horizontal reference, so I can look up each piece but never
   see them joined.

---

## Consensus

The three passes were deliberately different readers — browsing, executing, maintaining — and
they converged on the same core. Five strengths and five weaknesses appeared in all three.

### What all three passes agree is good

| Finding | Pass 1 | Pass 2 | Pass 3 |
|---|:---:|:---:|:---:|
| Progressive disclosure (one-line card → detail → math) plus 904 "In vanilla" anchors | ✓ | ✓ | ✓ |
| Silent-failure and gotcha warnings (unknown keys, missing tech, rename traps, save-baked values) | ✓ | ✓ | ✓ |
| Override/join-key semantics stated per family (file name vs `Name`/UID, inheritance) | ✓ | ✓ | ✓ |
| Honest labelling of undocumented values instead of invented behaviour | ✓ | ✓ | ✓ |
| Section intros that give the generation order / price order / derived-stat model | ✓ | ✓ | ✓ |

### What all three passes agree is bad

| Finding | Pass 1 | Pass 2 | Pass 3 |
|---|:---:|:---:|:---:|
| 90% "values only"; 63% of cards have only a one-liner, so a specific idea often hits a wall | ✓ | ✓ | ✓ |
| Almost no copyable syntax outside colonies (7 code blocks in 920 KB) | ✓ | ✓ | ✓ |
| No end-to-end on-ramp or test loop outside colonies (no first file, no log, no "it worked") | ✓ | ✓ | ✓ |
| Unexplained Tier badges and code-first jargon raise the entry cost | ✓ | ✓ | ✓ |
| Uneven depth across sections, with no cross-links between coupled values | ✓ | ✓ | ✓ |

### Where the passes differed (worth noting, not consensus)

- **Pass 1 only:** the missing Tier legend and the "where do I start" routing problem. Once I knew
  the files, these stopped mattering.
- **Pass 2 only:** the "keep inside the vanilla span" advice with no span shown. This is an
  execution-time trap, invisible when browsing.
- **Pass 3 only:** cross-family coupling, the lack of a per-section "safe to rename" box, and no
  update/migration path. These only appear after the first version works.

### What I would fix first, in order

1. **Give the six missing sections a `colonies.html`-style "Start here".** One page each: where
   the files go, the minimum valid file with one copyable snippet, one vanilla example, and one
   "you will know it worked when…" line. This is the single biggest unlock for a new modder.
2. **Promote the top ~50 high-leverage values-only cards to level 2.** Start with Globals, ship
   cost/upkeep, tech cost, planet types and racial traits. Do not try to fill all 959 at once;
   cover the levers a first mod actually pulls.
3. **Add a legend for `Tier 1/2/3`, `values only`, `families`, `files`, `tags`.** A four-line box in
   the sticky bar would remove the most common "what am I looking at" pause.
4. **Add a "Related" line to coupled cards and a per-section "safe to rename / do not touch / WIP"
   box.** The colonies table proves the format works; copy it.
5. **Show the test loop once, globally.** Mod folder, enable step, log location, new-game caveat,
   and what a successful load looks like. Link it from every section header.

**Bottom line:** the reference layer is strong and trustworthy; the tutorial layer is missing on
six of seven pages. Keep the honesty about gaps, but give an eager reader one complete, copyable
path from "I want this" to "I see it in game" in each section — and the docs would turn from a
lookup table into something a new modder can actually build from.
