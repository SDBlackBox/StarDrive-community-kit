"""Sections for the moddable-content reference.

Each section owns a page and a list of family ids from moddable-data*.py. The prose here is
deliberately deeper than a family line: level 2 explains how the files interact, level 3 gives
the numbers, units and vanilla usage a modder would quote. The five-sentence cap is a soft one
and is checked by `build-moddable.py --audit`.
"""

SECTIONS = [
dict(id="game-options", title="General game options", short="Game options",
     blurb="The numbers a new game starts from, and the AI's own spending rules.",
     families=["globals", "budgets", "fleetratios", "econstrats"],
     l1="The values every empire starts from: opponents, the turn clock, trait points, upkeep, repair, research and the AI's budgets.",
     l2=("These are the files a total conversion edits first, because one key changes every empire at once without touching a ship or a "
         "building. Most of them are multipliers applied after the per-item value, so a 2 doubles a whole category; a few are absolute "
         "starting numbers that only matter when a galaxy is generated. The AI files are read per race, keyed by portrait, and they "
         "replace vanilla rather than merging key by key."),
     l3=("Globals.yaml is matched by key to GamePlayGlobals; an unknown key is ignored with no warning, so a typo looks like a value that "
         "did nothing. Per-item prices live in the content files, and the globals scale them afterwards, which is why ShipMaintenance "
         "Multiplier is a stronger lever than editing 200 modules. Starting values such as TurnTimer, TraitPoints and the opponent count "
         "are baked into a save when it is created: test them in a new game, not an old one. Two flags, EnableSalvageOps and "
         "EnableHullPlates, are forced off for a mod before its own values are read, so a mod that wants them must turn them on itself."),
     notes="""<p class="note-p">Order of operations for a price: the module, weapon or building file gives the base number, the empire's
racial traits apply their modifier, then the global multiplier from this section applies. A save keeps the globals it was created with.</p>"""),

dict(id="map-creation", title="Map creation and solar systems", short="Map creation",
     blurb="How a galaxy is generated, and how hand-placed systems fit beside it.",
     families=["planettypes", "suns", "sunzones", "solarsystems", "randomstuff", "namegenerators"],
     l1="How a new galaxy is built: star types, orbital zones, planet types, spawned ruins and the name pools.",
     l2=("Galaxy generation picks a star, walks its orbits, rolls a planet category from that zone's weights, then rolls minerals, "
         "fertility and random buildings. Hand-placed systems are separate files and are not touched by any of these tables, so a mod can "
         "mix a designed home system with generated space around it. Every table here is read at galaxy creation; none of it changes a save "
         "that already exists."),
     l3=("WhichPlanet is an index into PlanetTypes.Types, not a name, so inserting a type in the middle re-points every system after it. "
         "SunPath is the opposite: a string id from Suns.yaml. SunZoneData weights are normalised per zone, so raising one category's weight "
         "changes the mix while the other weights keep their relative sizes. RandomStuff rolls a percentage once per planet of the matching "
         "type and caps the result with InstanceMax. The planet type's HabitableTileChance and PopPerTile decide how much of the surface can "
         "be settled before any building is placed."),
     notes="""<p class="note-p">Generation order: star from Suns.yaml → orbit count → per orbit, a category from SunZoneData → a type of that
category from PlanetTypes → surface tiles, fertility and minerals → RandomStuff rolls → name from the NameGenerators pool. A hand-placed
system in SolarSystems/ skips the first four steps but still gets its planets from PlanetTypes indices.</p>"""),

dict(id="ships", title="Ships, modules and designs", short="Ships",
     blurb="The hull grid, the modules that fill it, the weapons they point at, and the saved layouts.",
     families=["hulls", "modules", "weapons", "designs", "shiproles", "designoutput"],
     l1="The ship half of the game: hull slot grids, modules, weapons, saved designs and the roles the AI builds.",
     l2=("A ship is assembled at load from four kinds of file: the hull gives the slot grid and the model, each module gives cost, mass, "
         "health, power, shields and thrust, the weapon file gives damage, range and cadence, and the design records which module UID sits "
         "in which cell. The shipyard's offence, defence, power and speed are sums and formulas over those files, never fields in the "
         "design. That is why copying a design file without its hull or modules produces a ship that is missing parts rather than an error."),
     l3=("Slot letters are positional: a module's Restrictions must overlap the letter in the cell, with xI/xO/xIO requiring an exact match. "
         "A design's Modules count must equal its ModuleUIDs lines, and its Size and GridCenter must equal the hull's grid and C cell, or the "
         "design is dropped. Module and weapon UIDs come from file stems, and a weapon UID no file defines leaves the mount inert with a log "
         "line. Every hull needs a tech in its unlock closure or no design using it can ever be built."),
     notes="""<p class="note-p">The derived numbers are documented in <a href="../ship-content-reference.md">ship-content-reference.md</a>:
module cost and mass sum directly, health is scaled by modifiers, speed comes from thrust against mass with a hull floor, and a design's
research price is the closure of the techs that unlock its hull and modules.</p>"""),

dict(id="tech", title="Tech tree and research", short="Tech tree",
     blurb="What each node costs, what it opens, and the weights that make some areas cheaper.",
     families=["technology", "research", "militaryresearch"],
     l1="The research tree: what each node costs, what it unlocks, and the weights that make some areas cheaper for a race.",
     l2=("Techs are the only gate on content. A hull, module, building or troop that no tech lists still exists in memory and simply never "
         "appears in a build list, with no error to explain why. The node's Cost is its own price; the price shown on a design is the closure "
         "of every tech that unlocks its hull and modules. Research weights multiply that cost per race and per category."),
     l3=("LeadsTo fills the children's Parents in reverse, so a branch that nothing leads to is unreachable and silent. Unlock entries are "
         "child elements naming a UID; a UID that does not exist is at best a log line. Research.yaml is keyed by race portrait and "
         "multiplies Cost by technology type, hull class and weapon tag, with 1 neutral and 0.5 half price. MilitaryResearchStrategy sets "
         "which branch the AI walks; a path with no techs leaves it with no plan."),
     notes="""<p class="note-p">Unlock closure: start at a hull, walk every tech whose HullsUnlocked names it, then every parent those techs
list in LeadsTo, and stop at the roots. If the walk reaches no root, the hull is unbuildable even though it loads. The same test applies to
a module, building or troop.</p>"""),

dict(id="races-diplomacy", title="Races, diplomacy and events", short="Races & diplomacy",
     blurb="Who the empires are, what they are like, and what they say when they meet you.",
     families=["races", "racialtraits", "diplomacy", "diplomacydialogs", "encounters", "events"],
     l1="Who the empires are, what they are like and what they say: race templates, traits, personalities, encounters and events.",
     l2=("A race file is also the empire's startup template: every Default*, Pirate* and Remnant* line is a ship-design name, so changing one "
         "changes what that empire starts with and what its governors build. Traits are chosen at game start and add their modifiers to the "
         "empire. Diplomacy personalities set starting relations and how fast they drift, while dialog pools only choose the words. "
         "Encounters are looked up by faction and step, and exploration events by their own name."),
     l3=("A missing design name falls back to a default, often a vanilla one, so a typo looks like the AI ignoring your ship rather than an "
         "error. Trait Excludes is a name and trait points come from Globals.TraitPoints. An encounter is selected by Faction plus Step, and "
         "the first loaded match wins, so two files with the same pair shadow each other. Event outcomes are weighted by Chance and can spawn "
         "ships, grant a tech or edit the planet. A missing dialog pool falls back to Default and never blocks the treaty."),
     notes="""<table><tr><th>content</th><th>looked up by</th><th>what breaks if it is wrong</th></tr>
<tr><td class="n">Races/</td><td>Traits/Name</td><td>the empire loads, then builds fallback designs</td></tr>
<tr><td class="n">RacialTraits/</td><td>TraitName</td><td>the option disappears from the setup screen</td></tr>
<tr><td class="n">Diplomacy/</td><td>trait Name</td><td>relations start at a default personality</td></tr>
<tr><td class="n">Encounter Dialogs/</td><td>Faction + Step</td><td>the wrong dialog, or none, at that contact step</td></tr></table>"""),

dict(id="colonies", title="Colonies, economy and ground war", short="Colonies",
     blurb="What colonies build, what troops and goods do, and what an edict or a relic changes.",
     families=["buildings", "troops", "goods", "planetedicts", "artifacts", "dyson"],
     l1="What colonies build and what ground units, goods, edicts and relics do.",
     l2=("Buildings are the colony's modules: flat and per-colonist bonuses, upkeep, storage and defence. Troops fight on the surface and in "
         "boarding, goods move through the freight network, edicts are the governor's presets, and artifacts are permanent empire bonuses. "
         "A few buildings are found by name in code, so renaming one removes behaviour the XML never described."),
     l3=("A building's Icon is a sprite family, not a path: Buildings/icon_<Icon>_48x48 and _64x64 must both exist. Maintenance is per turn "
         "and Cost is one-off; Income and PlusTaxPercentage are credits. Troop Strength is current HP and MaxStrength the cap, with level "
         "adding five percent to both attacks and range at level five. Planet edict thresholds are fractions of storage, not absolute amounts. "
         "Artifact bonuses stack across the collection and the Spiritual trait multiplies each one."),
     intro="""<h2>Start here &mdash; your first colony mod</h2>
<details class="note" open><summary>Where the files go, what they are called, and what is required</summary>
<div class="in">
<p>A mod is one folder, <code>Mods/&lt;YourMod&gt;/</code>. Put the game's folder tree inside it, with no
<code>Content/</code> step: a building goes to <code>Mods/&lt;YourMod&gt;/Buildings/Civilian/My Building.xml</code>,
a troop to <code>Mods/&lt;YourMod&gt;/Troops/My Troop.xml</code>. Every file under the family folder is read, so
yours can sit in any subfolder and can be called anything; the <code>Name</code> inside is the id that techs,
planets, events, the build list and saves use.</p>
<table>
<tr><th>family</th><th>folder</th><th>root element</th><th>a file holds</th></tr>
<tr><td class="n">Buildings</td><td><code>Buildings/</code></td><td><code>&lt;Building&gt;</code></td><td>one building</td></tr>
<tr><td class="n">Troops</td><td><code>Troops/</code></td><td><code>&lt;Troop&gt;</code></td><td>one troop</td></tr>
<tr><td class="n">Goods</td><td><code>Goods/</code></td><td><code>&lt;Good&gt;</code></td><td>one good, plus its line in <code>Goods/Goods.yaml</code></td></tr>
<tr><td class="n">Planet edicts</td><td><code>PlanetEdicts/</code></td><td><code>&lt;PlanetEdict&gt;</code></td><td>one edict; vanilla ships one file, <code>Core.xml</code></td></tr>
<tr><td class="n">Artifacts</td><td><code>Artifacts/</code></td><td><code>&lt;ArrayOfArtifact&gt;</code></td><td>the whole collection in one file</td></tr>
<tr><td class="n">Dyson rings</td><td><code>DysonRings.yaml</code></td><td>a YAML list</td><td>one block per ring type</td></tr>
</table>
<p><b>Required and optional.</b> Only <code>Name</code> is mandatory: it is the id. Every other tag can be
omitted and the field keeps its default, but the default is not always zero &mdash; <code>Unique</code> and
<code>Scrappable</code> default to true and a building's <code>Strength</code> to 5. So copy the closest vanilla
file rather than writing from a blank page, then change <code>Name</code>, the numbers and the icon. That is
also how you add a building, troop or good: copy, rename, retune, and add the new id to whatever should
unlock it.</p>
<p><b>What overrides what.</b> Every file under the family folder is read, whatever it is called. An entry
that reuses a vanilla <code>Name</code> replaces that entry; a new <code>Name</code> adds one. The file name is
not the join key &mdash; <code>Name</code> is, and a tech's unlock list, a planet's building, a troop roster and
a save all hold that string or the id it maps to. Renaming <code>Name</code> on an existing building therefore
detaches it from the tech that unlocked it.</p>
</div></details>
<details class="note crit" open><summary>Critical: 19 building names are read from code</summary>
<div class="in">
<p><code>LoadBuildings</code> matches these <code>Name</code> strings and stores the match in a static id. Rename
one and the id stays 0; code that then asks for that template gets nothing, and the capital and space port
paths throw before the colony exists.</p>
<table>
<tr><th>Name in the file</th><th>id assigned</th><th>what stops working</th></tr>
<tr><td class="n">Capital City</td><td><code>Building.CapitalId</code></td><td>every new colony is given one at generation; with the id at 0, colony creation throws</td></tr>
<tr><td class="n">Space Port</td><td><code>SpacePortId</code></td><td>placed beside the capital at generation; same failure</td></tr>
<tr><td class="n">Outpost</td><td><code>OutpostId</code></td><td>the building a colony is founded with, and the one the AI queues to claim a planet</td></tr>
<tr><td class="n">Terraformer</td><td><code>TerraformerId</code></td><td>all three terraforming gates, the terraformer queue check and AI terraforming</td></tr>
<tr><td class="n">Biospheres</td><td><code>BiospheresId</code></td><td>the biosphere option on an evaluated planet, the colony screen and the queue check</td></tr>
<tr><td class="n">Dormant Volcano, Active Volcano, Erupting Volcano</td><td><code>VolcanoId</code>, <code>ActiveVolcanoId</code>, <code>EruptingVolcanoId</code></td><td>the three volcano states; a volcano then has no building to place</td></tr>
<tr><td class="n">Lava1, Lava2, Lava3</td><td><code>Lava1Id</code>&ndash;<code>Lava3Id</code></td><td>the cooled tiles a volcano leaves behind</td></tr>
<tr><td class="n">Crater1&ndash;Crater4</td><td><code>Crater1Id</code>&ndash;<code>Crater4Id</code></td><td>the crater a meteor impact places</td></tr>
<tr><td class="n">Fissionables, Mine Fissionables, Fuel Refinery</td><td><code>FissionablesId</code>, <code>MineFissionablesId</code>, <code>FuelRefineryId</code></td><td>nothing in the current code reads these three ids &mdash; they are assigned and unused, so renaming them is safe</td></tr>
</table>
<p>Keep the vanilla <code>Name</code> on your version of a name in this table and change its numbers instead.
A renamed copy is a new building with no special behaviour: a useful thing to make, but not a replacement
for the original.</p>
</div></details>
<h2>Common mistakes and what you see</h2>
<table>
<tr><th>symptom</th><th>cause</th><th>fix</th></tr>
<tr><td class="n">the value did nothing, no error</td><td>a misspelled element name; the XML reader ignores elements it does not know</td><td>compare the tag spelling with the card or the vanilla file, then restart</td></tr>
<tr><td class="n">"Failed to parse XML: Buildings/..." at startup</td><td>malformed XML, text in a numeric tag, or a value that is not in an enum</td><td>the message names the file; fix it and restart</td></tr>
<tr><td class="n">the whole file is ignored</td><td>it sits under <code>Mods/&lt;Name&gt;/Content/</code>, or the mod is not enabled</td><td>move it up one level and enable the mod</td></tr>
<tr><td class="n">two copies exist, one unreachable</td><td>two files set the same <code>Name</code>; the loader keeps the later one</td><td>make the <code>Name</code> unique</td></tr>
<tr><td class="n">a new building never appears in the build list</td><td>nothing unlocks it, or the tech still names the old id</td><td>add the new <code>Name</code> to a tech's unlock list</td></tr>
<tr><td class="n">blank or red icon</td><td>no <code>icon_&lt;Icon&gt;_48x48</code> and <code>_64x64</code> pair under <code>Buildings/</code></td><td>add both sizes, or reuse a vanilla icon name</td></tr>
<tr><td class="n">colonies throw when created</td><td>Capital City, Space Port or Outpost renamed</td><td>restore the exact name</td></tr>
<tr><td class="n">a good is never shipped</td><td>it has no entry in <code>Goods/Goods.yaml</code></td><td>add its <code>UID</code> there</td></tr>
<tr><td class="n">two artifacts show the same text</td><td>both reuse a <code>NameIndex</code>/<code>DescriptionIndex</code>, or the index has no GameText line</td><td>give the artifact its own ids and add them to <code>GameText.yaml</code></td></tr>
</table>
<h2>How to test a change</h2>
<ol>
<li>Keep a copy of the vanilla file. Restoring it is the fastest way to prove which change moved the result.</li>
<li>Restart the game. These XML and YAML files are read once at startup, and a running game keeps the values it loaded.</li>
<li>Read the load error before anything else: <code>Failed to parse XML: &lt;relative path&gt;</code> names the file the reader rejected.</li>
<li>Start a new game for anything used at galaxy or colony creation (capital, space port, terrain, artifacts). A save keeps the buildings it already has.</li>
<li>Look at the screen that uses it: the colony build list and a colony's building panel for buildings, the troop list for troops, the trade and freight views for goods, the governor panel for edicts, the empire summary for artifacts.</li>
<li>Change one number at a time. Two changes in one run cannot tell you which one moved the result.</li>
</ol>
<h2>Terms used on this page</h2>
<table>
<tr><th>term</th><th>meaning here</th></tr>
<tr><td class="n">UID</td><td>the text id that joins files. In this section it is <code>Name</code> for buildings, troops and edicts, and <code>UID</code> for goods.</td></tr>
<tr><td class="n">BID</td><td>the integer a building is given at load, in file order. Never author it; code uses it, players use <code>Name</code>.</td></tr>
<tr><td class="n">Per turn</td><td>once per game turn, not per second. Maintenance and Income are per turn.</td></tr>
<tr><td class="n">Per colonist</td><td>multiplied by population in billions, then added to the flat field of the same kind.</td></tr>
<tr><td class="n">Fertility</td><td>a planet's food multiplier, raised by <code>MaxFertilityOnBuild</code>; not the same field as richness.</td></tr>
<tr><td class="n">Richness</td><td>a planet's mineral multiplier; <code>PlusProdPerRichness</code> multiplies production by it.</td></tr>
<tr><td class="n">Storage</td><td>the cap on stored food or production. Edict thresholds are fractions of it, so 0.3 means 30% full.</td></tr>
<tr><td class="n">Pacing</td><td>the game-setup multiplier applied on top of listed costs and production, so the same <code>Cost</code> arrives at a different speed in a different game.</td></tr>
<tr><td class="n">Stacking</td><td>two bonuses of the same kind add; a percentage is a fraction of the base, not of the running total.</td></tr>
</table>"""),

dict(id="ui-assets", title="UI modding and assets", short="UI & assets",
     blurb="Screens, the main menu, text ids, and the files that must exist even in a total conversion.",
     families=["ui", "mainmenus", "gametext", "codex", "fonts", "textures", "models", "audio", "particles",
               "miscassets", "mgcb", "advice", "ftl", "explosions"],
     l1="The look and the words: UI layouts, the main menu, text ids, fonts, textures, models, audio and the compiled assets that must exist.",
     l2=("UI is a tree of elements in YAML, hot-reloadable while the game runs. Code finds controls by id, so a renamed button still draws "
         "but stops doing anything. Assets replace by relative path and a missing texture degrades to a red placeholder, while fonts and "
         "compiled shaders fail when they are missing. The main menu is the clearest worked example because every top-level option is a named "
         "element bound to a screen."),
     l3=("MainMenus.yaml picks a layout and a 3D scene; the layout's List named buttons holds new_game, load_game, options, mods, sandbox, "
         "info, support and exit, and MainMenuScreen binds each id to a screen. 'Mods' opens the manager, and the download/update address "
         "comes from Globals URL and DownloadSite, so a total conversion can point at its own host without touching UI code. Positions are "
         "virtual pixels under VirtualSize and AbsSize 0 auto-fits the texture. Fonts, the compiled Simple/MeshLighting/SkinnedEffect/BeamFX/"
         "Distort shaders, and Content.mgcb are the static group: they do not fall back."),
     notes="""<table><tr><th>element id</th><th>button</th><th>what it opens</th></tr>
<tr><td class="n">new_game</td><td>New Game</td><td>RaceDesignScreen, then galaxy setup</td></tr>
<tr><td class="n">load_game</td><td>Load Game</td><td>LoadSaveScreen</td></tr>
<tr><td class="n">options</td><td>Options</td><td>OptionsScreen</td></tr>
<tr><td class="n">mods</td><td>Mods</td><td>ModManager; the update/download link is Globals.DownloadSite</td></tr>
<tr><td class="n">sandbox</td><td>Dev Sandbox</td><td>DeveloperSandbox</td></tr>
<tr><td class="n">info</td><td>BlackBox Codex</td><td>CodexScreen</td></tr>
<tr><td class="n">support</td><td>Support BlackBox</td><td>SupportBlackbox</td></tr>
<tr><td class="n">exit</td><td>Exit</td><td>closes the game</td></tr>
<tr><td class="n">tutorials</td><td>Tutorials</td><td>TutorialScreen; bound by code but absent from the default layout</td></tr></table>
<p class="note-p">The same pattern applies to every screen: the layout names an element, code looks up that name. Renaming `buttons` or any
of the ids above removes the behaviour even though the screen still draws.</p>"""),
]
