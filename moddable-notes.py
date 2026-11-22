"""Deep level-3 notes for the tags that carry the most weight.

Keyed by (family id, tag name). A note is either the level-3 text or a dict that replaces l1, l2
and l3 together, and may also set range= (the code's bounds and the arithmetic) or vanilla= (the
whole "In vanilla" line). build-moddable.py applies it, then appends the generated values. A
note that carries the whole card is for a field a modder edits directly, where the unit and the
vanilla values need more room than the one-line family data can hold. Each level 3 aims at the
five-sentence soft cap: what the number is, its unit or scale, how it combines, and what a modder
sees when it is wrong.
"""

NOTES = {

# Tags the vanilla files set that the loader cannot bind to a field. XmlSerializer ignores an element
# it has no field for, so these are written, copied by modders and read by nothing.
("troops", "Movement"): dict(
    l2=("The loader binds an element to a field of the same name, and Troop.cs has no Movement field: it "
        "moves on MoveTimerBase and AvailableMoveActions. The value is silently discarded."),
    l3="This item has no function in game."),
("troops", "MaintenanceCost"): dict(
    l2=("Troop.cs has no field of this name; a troop costs its build Cost, and upkeep is charged to the "
        "colony, not per troop. The value is silently discarded."),
    l3="This item has no function in game."),
("troops", "MaxStrength"): dict(
    l2=("The hit points of a troop are StrengthMax, which this element cannot fill because the names "
        "differ. A troop keeps the default and the value is silently discarded."),
    l3="This item has no function in game."),
("troops", "sound_attack"): dict(
    l2=("Troop.cs has no field for a sound; attacks play the animation from attack_path and the global "
        "combat sounds. The value is silently discarded."),
    l3="This item has no function in game."),
("goods", "Mass"): dict(
    l2=("Good.cs has no Mass field, so cargo space is charged from the ship and its modules, not from the "
        "good. The value is silently discarded."),
    l3="This item has no function in game."),
("goods", "IsCargo"): dict(
    l2=("Good.cs has no IsCargo field: a good is cargo if a freighter carries it, and nothing reads this "
        "flag. The value is silently discarded."),
    l3="This item has no function in game."),
("buildings", "ShortDescription"): dict(
    l2=("Only ShortDescriptionIndex is read; this free-text element has no field, and the short tooltip is "
        "built from the stats when the index is 0. The value is silently discarded."),
    l3="This item has no function in game."),
("buildings", "TechBranch"): dict(
    l2=("Building.cs has no field of this name; unlocking is decided by the tech tree that lists the "
        "building. The value is silently discarded."),
    l3="This item has no function in game."),

("racialtraits", "ConsumptionModifier"): dict(
    l1="Scales how much food each billion colonists eats per turn.",
    range=("the loader sets no bounds; -1 is the lowest sensible value because 1 + value reaches 0, "
           "and below -1 the charge turns negative. Math: consumption = 1 + value, per billion colonists "
           "per turn; -1 = 0, -0.15 = 0.85, 0 = 1, 0.1 = 1.1, 0.5 = 1.5."),
    vanilla=("In vanilla: RacialTraits/RacialTraits.xml, one value per trait option \u2014 Efficient Metabolism "
             "-0.15 = 0.85 food per billion colonists, Gluttonous 0.1 = 1.1 food per billion colonists."),
    l2=("The game charges 1 food per billion colonists per turn before this field, and the value is added to that 1, "
        "so -0.15 charges 0.85 and 0.1 charges 1.1. Cybernetic races pay the same charge in production instead of food. "
        "It applies to every colony, and to the food that troops in space consume, not only the homeworld."),
    l3=("`ConsumptionPerColonist = 1 + ConsumptionModifier` is multiplied by population in billions, so -0.15 saves "
        "0.15 food per billion people per turn and 0.1 adds the same. Vanilla Efficient Metabolism sets -0.15 for 3 "
        "points and Gluttonous sets 0.1 and refunds 2. The code applies no clamp: at -1 a colony eats nothing, and "
        "below -1 the charge is negative, so keep the value above -1. The tech bonus Consumption Bonus subtracts its "
        "value from this field, which is why a positive tech bonus makes food cheaper.")),

("racialtraits", "PopGrowthMin"): dict(
    l1="Sets a floor on how many people a colony gains each turn.",
    range=("the loader sets no bounds; the colony is clamped to 0..MaxPopulation and then to at least 10 "
           "people, so a negative floor can shrink a colony but not empty it. Math: floor = value \u00d7 1000 "
           "people per turn; -0.005 = -5 million, 0 = no floor, 0.005 = 5 million, 0.05 = 50 million."),
    vanilla=("In vanilla: RacialTraits/RacialTraits.xml, one value on one trait option \u2014 Fertile 0.005 = at "
             "least 5 million people per turn, for 2 points."),
    l2=("Growth is computed from population, spare capacity and the empire's base reproductive rate, and this field "
        "raises the result to a minimum. The unit is billions per turn, so 0.005 means at least 5 million people per "
        "turn. The floor is applied after the growth ceiling and before ReproductionMod, and it is skipped while a "
        "colony is starving, over capacity or in recent combat. Vanilla Fertile sets 0.005."),
    l3=("`repRate = repRate.LowerBound(PopGrowthMin * 1000)` runs on the internal scale where 1000 is one billion, "
        "so 0.005 is a floor of 5 units, or 5 million people, per turn. On a small or crowded colony the floor can "
        "supply most of the growth, which is why Fertile matters most early. Because the floor applies even when "
        "natural growth is negative, a positive value can keep a shrinking colony from emptying. Vanilla uses it only "
        "on Fertile, at 0.005 for 2 points.")),

("racialtraits", "PopGrowthMax"): dict(
    l1="Caps how many people a colony can gain in one turn.",
    range=("the loader sets no bounds; 0 turns the cap off and a negative cap forces population loss. Math: "
           "cap = value \u00d7 1000 people per turn; -0.005 = at most -5 million, 0 = no cap, 0.015 = at most "
           "15 million, 0.05 = at most 50 million."),
    vanilla=("In vanilla: RacialTraits/RacialTraits.xml, one value on one trait option \u2014 Less Fertile 0.015 = "
             "at most 15 million people per turn, for -3 points (a refund of 3)."),
    l2=("The cap is checked before the floor and before ReproductionMod, and 0 disables it, so an unset field does "
        "not mean no growth. The unit is billions per turn: 0.015 caps growth at 15 million people per turn. It bites "
        "hardest on large, fertile worlds where natural growth is high, and it affects every colony including the "
        "homeworld. Vanilla Less Fertile sets 0.015."),
    l3=("`if (PopGrowthMax.NotZero()) repRate = repRate.UpperBound(PopGrowthMax * 1000)` caps the per-turn gain at "
        "0.015 billion, or 15 million people, on the internal scale. It is a ceiling rather than a multiplier, so a "
        "world below it grows exactly as it would without the trait. Vanilla Less Fertile sets 0.015 and refunds 3 "
        "points, and no other trait sets it. A value of 0 skips the cap entirely, so use a small positive number to "
        "slow growth.")),

("racialtraits", "ReproductionMod"): dict(
    l1="Multiplies a colony's population growth after the floor and ceiling are applied.",
    range=("the loader sets no bounds; -1 zeroes growth and below -1 reverses it. Math: growth = base \u00d7 "
           "(1 + value); -1 = 0%, -0.5 = 50%, 0 = 100%, 0.5 = 150%, 1 = 200%."),
    vanilla=("In vanilla: no racial trait sets it; Artifacts/MainArtifacts.xml sets 0.5 = 150% growth on the "
             "first artifact."),
    l2=("The value is a fraction added to the growth rate rather than a flat number of people: 0.5 makes growth half "
        "again as fast and -0.5 halves it. It stacks with the growth floor and ceiling and applies to every colony. "
        "It is separate from PopGrowthMin and PopGrowthMax, which set the bounds this multiplier then scales. No "
        "vanilla racial trait sets it, so it is free design space."),
    l3=("`repRate += repRate * ReproductionMod` runs after the floor and ceiling, so 0.5 turns a 10-million gain into "
        "15 million and -0.5 turns it into 5 million. The vanilla artifact set uses the same field: the first artifact "
        "in `Artifacts/MainArtifacts.xml` grants 0.5. A value of -1 stops all natural growth, and below -1 growth "
        "turns negative; the loader does not clamp it. Because it is multiplicative, it cannot lift a colony that is "
        "already at its population maximum.")),

("racialtraits", "HomeworldFertMod"): dict(
    l1="Raises or lowers the fertility of the empire's starting homeworld when a galaxy is generated.",
    range=("the loader and the generator set no bounds. Math: fertility = (2 + value) / the race's environment "
           "modifier for that planet category; at a neutral modifier of 1: -2 = 0, -1 = 1, -0.35 = 1.65, "
           "0 = 2, 1 = 3."),
    vanilla=("In vanilla: RacialTraits/RacialTraits.xml, two values on two trait options \u2014 Polluted Homeworld "
             "-0.35 = 1.65 fertility, Industrialized Homeworld -1.0 = 1.0 fertility."),
    l2=("The homeworld's maximum fertility is built from a base of 2 plus this value, then divided by the race's "
        "environment modifier for that planet category. -0.35 gives 1.65 and -1.0 gives 1.0, half the neutral base. "
        "It is applied once at galaxy creation and only to the starting homeworld, so captured and later-settled "
        "worlds are unaffected. Vanilla Polluted Homeworld uses -0.35 and Industrialized Homeworld uses -1.0."),
    l3=("`baseMaxFertility = (2 + HomeworldFertMod) / PreferredEnvModifier` runs in "
        "`CreateHomeWorldFertilityAndRichness`, once per homeworld, before buildings add their own fertility. -0.35 "
        "(Polluted Homeworld, -2 points) gives 1.65 against the neutral 2.0, and -1.0 (Industrialized Homeworld, 2 "
        "points) gives 1.0. Because it is read only when the galaxy is generated, it does nothing in an existing save "
        "and nothing on a world settled later.")),

("racialtraits", "HomeworldRichMod"): dict(
    l1="Raises or lowers the mineral richness of the empire's starting homeworld.",
    range=("galaxy generation sets no bounds; later richness changes are floored at 0. Math: richness = "
           "1 + value; -1 = 0, -0.5 = 0.5, 0 = 1, 0.5 = 1.5, 1 = 2, 2 = 3."),
    vanilla=("In vanilla: RacialTraits/RacialTraits.xml, one value on one trait option \u2014 Industrialized "
             "Homeworld 1.0 = 2.0 mineral richness."),
    l2=("The homeworld starts at a mineral richness of 1 before this value is added, so 1.0 doubles it and -0.5 "
        "halves it. Richness multiplies the production a colony gets from its tiles, which makes this a long-term "
        "economic trait. Like fertility, it is applied once at galaxy generation and only to the starting homeworld. "
        "Vanilla Industrialized Homeworld sets 1.0."),
    l3=("`MineralRichness = 1f + HomeworldRichMod` is set in the same generation pass as fertility, before buildings "
        "or technology change production. 1.0, the Industrialized Homeworld value, doubles the homeworld's tile "
        "production for the rest of the game. The field is read only when the galaxy is created, so a save keeps the "
        "richness it was generated with and other colonies ignore it.")),

("globals", "ShipMaintenanceMultiplier"):
    "Every ship's upkeep is its build cost times this value, so it scales the whole fleet at once rather than one hull class. "
    "A value of 5 makes a 1,000-credit frigate cost 5,000 per turn to keep, which usually ends expansion long before combat does. "
    "The gate applies after racial MaintMod and before the budget screen totals, so two races with the same ships still pay differently. "
    "It is read when a save loads; an old save keeps the multiplier it was created with.",

("globals", "TurnTimer"):
    "This is real seconds per turn, not simulation speed: five means a turn advances every five seconds while ships move in real time. "
    "Lower values compress a campaign and make reaction time more valuable than planning; higher values let a player micromanage every fight. "
    "It is written into the save at creation and is not re-read for an existing game.",

("globals", "GravityWellRange"):
    "The radius in game units inside which a planet or star prevents warp, measured from the object's centre. "
    "At 8,000 units a fleet must leave orbit and cross the well before it can jump, which is what makes blockades and chokepoints work. "
    "Setting it to 0 removes the wells entirely and lets fleets warp out from orbit, changing every defensive plan in the game.",

("globals", "TraitPoints"):
    "The pool a race spends on racial traits at setup; the trait options' own Cost values are deducted from it. "
    "Vanilla 8 is enough for a strong specialisation plus one weakness, so raising it makes every custom race strictly better. "
    "It is a setup-screen value, not a live modifier: existing saves keep their choices.",

("globals", "EnableSalvageOps"):
    "Turns salvageable derelicts, salvage ships and the recovery work into real mechanics; with it off the files still load but nothing spawns. "
    "It is forced false for every mod before the mod's own Globals.yaml is read, so inheriting vanilla does not inherit this. "
    "A mod that wants derelicts must set it true explicitly, and must also supply the salvage modules and ships the mechanic expects.",

("globals", "Mod.FormatVersion"):
    "The only value in the Mod block that can stop a mod from loading: it must be 1, and a mismatch produces a message instead of a game. "
    "SupportedBlackBoxVersions is the softer check: a comma list matched by substring against the running version, so jupiter-1.60 covers 1.60.x. "
    "Name is the mod's identity for saves and download links; changing it after release looks like a different mod to both.",

("hulls", "Size"):
    "Two integers, width and height, that must equal the number of characters in every slot row and the number of rows. "
    "A mismatch is not repaired: the hull loads with a grid that does not match its declared size, and designs built on it fail their own consistency check. "
    "The size also feeds the design screen's slot count and the cost curve once a hull passes CostBasedOnSizeThreshold.",

("hulls", "HullName"):
    "This string is the hull's UID: designs name it in Hull=, techs name it in HullsUnlocked, and the AI's default designs point at it. "
    "The file stem is the override key, but HullName is what references resolve to, so the two are normally kept identical. "
    "Renaming only the stem adds a second hull with the same UID; renaming only HullName silently dangles every reference.",

("hulls", "slots"):
    "One line per grid row, one character per cell, with no key: I is interior, O is outer, E is engine, and a combined letter accepts either. "
    "The C character marks the grid centre that a design stores in GridCenter, and x-prefixed slots require an exact module restriction match. "
    "A row that is one character short shifts every cell after it, which is why a design can look correct and still place modules in the wrong cells.",

("modules", "Cost"):
    "Credits added once per module when the design is priced; the hull itself contributes nothing. "
    "Racial ShipCostMod applies on top, and the global size curve can apply to the hull total, but there is no hidden multiplier inside this field. "
    "Armour is the cheapest per cell in vanilla, which is why a design's cost is dominated by weapons, reactors and shields rather than plating.",

("modules", "Mass"):
    "Tonnage added to the ship, used with total thrust to derive sublight acceleration and turning. "
    "It does not affect cost directly, so a heavy design can be cheap and still slow; the hull also contributes a floor that keeps a tiny ship from becoming infinitely fast. "
    "Doubling a module's mass without adding thrust is the usual reason a refit feels worse in combat than its stat line suggests.",

("modules", "HealthMax"):
    "The module's own hit points before empire and tech modifiers; the ship's total is the sum over its modules. "
    "A ship dies when its internal modules fall below the global ShipDestroyThreshold share, so spreading damage across many cheap modules survives longer than concentrating it in a few expensive ones. "
    "Resistances apply before this pool is reduced, and APResist also marks the module as armour for targeting.",

("modules", "PowerFlowMax"):
    "Power supplied per second; any value of 1 or more makes the module count as a power plant for the ship's power budget. "
    "PowerStoreMax is the battery that absorbs a burst, and PowerDraw is what consumers take per second, so a design can fit, look fine at rest, and still fail the first time it fires. "
    "Warp draw is charged at half weight, which is why a ship that is power-neutral in combat can still be unable to jump.",

("modules", "Restrictions"):
    "The slot letters this module accepts: I, O, E, IO, IOE, xI, xO or xIO. "
    "The check is per cell, not per module: a two-cell module needs every cell it covers to accept it, and a rotated module swaps its footprint. "
    "x-prefixed values are the strict form and require an exact match, so xI will not fit a plain I cell even though the letter is present.",

("modules", "WeaponType"):
    "The UID of a file in Weapons/, not a type name and not a damage value. "
    "A missing weapon logs a warning and leaves the mount present but inert, which reads in play as a ship that closes to range and never fires. "
    "Damage, range, cadence and the Tag_ flags all live in that other file, so a module's cost can be high while the gun it carries is weak.",

("modules", "PercentLimitOnShips"):
    "The share of a hull's slots this module may occupy, with 0 meaning unlimited. "
    "The loader also imposes a floor of six modules, and stations are exempt, so the limit mainly stops a design being all armour or all reactors. "
    "A design that exceeds the limit is not silently trimmed: the extra modules fail to place, and the ship launches with empty cells.",

("modules", "HangarShipUID"):
    "The design a hangar builds, named exactly as the design's Name. "
    "The loader accepts both HangarShipUID and hangarShipUID, which is why both spellings appear in content; the lowercase form is not a different field. "
    "MaximumHangarShipSize and PermittedHangarRoles gate what the bay may launch, so a design that exists but is too large simply never appears in the wing.",

("weapons", "DamageAmount"):
    "Base damage per hit before resistances, EffectVsShields/EffectVsArmor and tag bonuses. "
    "The design screen's offence divides it by FireDelay and multiplies by SalvoCount and ProjectileCount, which is why a low-damage rapid weapon can out-score a heavy slow one. "
    "A value of 0 is legal and produces a utility weapon such as a repair or tractor beam.",

("weapons", "FireDelay"):
    "Seconds between shots for one mount; the design's DPS is damage divided by this, not a separate stat. "
    "SalvoCount adds shots per trigger and SalvoTimer spaces them, so a salvo weapon can have a long delay and still deliver a burst. "
    "Changing only the delay is the least invasive way to rebalance a weapon because range and accuracy stay put.",

("weapons", "Range"):
    "Maximum range in game units, and the number the design screen's offence score falls off with. "
    "A weapon that outranges the target's guns fires for several seconds before return fire, so range is usually worth more than raw damage per shot. "
    "FireArc and FireCone are separate: they constrain where the mount can point, not how far the shot travels.",

("weapons", "EffectVsShields"):
    "A multiplier on damage against shields, with 1 neutral and 0.9 meaning ten percent less. "
    "The loader also accepts the singular EffectVsShield, so either spelling works and neither is a dead field. "
    "This is applied after the target's shield resistances, which is why a shield-resistant weapon still needs a good multiplier to be worth fitting.",

("weapons", "BeamPowerCostPerSecond"):
    "The sustained power draw while a beam is firing, separate from PowerRequiredToFire which is per shot. "
    "A beam with a high value can drain a ship that looks power-positive on the design screen once combat starts. "
    "BeamDuration, BeamThickness and BeamTexture are visual or timing fields and do not change the damage maths.",

("technology", "Cost"):
    "Research points for level one; MaxLevel and MultiLevelCostMultiplier control the later levels. "
    "This is the node's own price, not a design's: a design's research price is the closure of every tech that unlocks its hull and modules. "
    "Research.yaml multiplies this per race and category, so the same node can be cheap for one empire and expensive for another.",

("technology", "LeadsTo"):
    "Names the child techs and, in reverse, fills their Parents list. "
    "A tech that no parent leads to is unreachable from the roots and will never appear in the tree, no matter how it is unlocked. "
    "The legacy spelling LeadsToTech is still accepted in older files, but new content should use LeadsTo.",

("technology", "ModulesUnlocked"):
    "A container whose child ModuleUID names a module to unlock; HullsUnlocked, BuildingsUnlocked and TroopsUnlocked follow the same pattern. "
    "The named UID must exist or the unlock does nothing and only a log line records it. "
    "A module no tech names is still loaded, still shows in the palette if another gate passes, and can never be built.",

("technology", "BonusType"):
    "The stat a bonus raises, paired with Bonus as a fraction where 0.05 means five percent. "
    "Tags narrow which modules or weapons the bonus applies to; a bonus whose tags match nothing applies nowhere and is not an error. "
    "Bonuses stack additively across techs, so ten small nodes can be stronger than one large one.",

("designs", "Modules"):
    "The number of installed modules, which must equal the number of ModuleUIDs lines in the file. "
    "A mismatch drops the design at load rather than producing a partial ship. "
    "The count includes every cell of a multi-cell module once, not once per cell.",

("designs", "ModuleUIDs"):
    "The ordered list of module UIDs; the slot lines refer to these by one-based position. "
    "A UID that no module file defines leaves that cell empty, and the design still loads if the counts match. "
    "Order matters: reordering this list without reordering the slot lines moves every module to a different cell.",

("designs", "GridCenter"):
    "The centre cell copied from the hull's C character; it anchors rotation and the design screen's grid. "
    "If it disagrees with the hull, the design is rejected rather than rotated wrongly. "
    "Size must match the hull grid for the same reason, so a design is effectively pinned to one hull layout.",

("buildings", "Icon"):
    "A sprite family name, not a path: the colony screen looks for Buildings/icon_<Icon>_48x48 and _64x64. "
    "One missing size shows a placeholder at that zoom rather than failing the building. "
    "Reusing another building's Icon is the fastest way to add a variant without new art.",

("buildings", "Maintenance"):
    "Credits paid per turn while the building stands, shown on the budget screen's building line. "
    "It is separate from Cost, which is paid once at construction, and from Income, which can offset it. "
    "A negative Income is a cost, so a building can be cheap to build and ruinous to keep.",

("buildings", "Unique"):
    "One per empire, checked by building Name; BuildOnlyOnce is different and prevents rebuilding after destruction. "
    "The capital, outpost and spaceport are also special-cased by name in code, so a unique copy with a new name loses that behaviour. "
    "A second copy of a Unique building is not placed and does not refund its cost.",

("races", "StartingShip"):
    "A design name, not a hull or a path: the empire spawns this exact design at game start. "
    "A missing name falls back to a default design, often a vanilla one, so a typo looks like the race ignoring your ship. "
    "The same rule applies to every Default*, Pirate* and Remnant* line in the file.",

("races", "EnvTerranMultiplier"):
    "A habitability multiplier for that planet category, spelled with the Multiplier suffix in the race file but read into the runtime field without it. "
    "1 is neutral; values above 1 make that climate more productive and below 1 less. "
    "The same suffix pattern applies to Oceanic, Steppe, Tundra, Swamp, Desert, Ice, Barren and Volcanic.",

("diplomacy", "Alliance"):
    "How willing a personality is to accept an alliance, weighed against the current relation and the other side's strength. "
    "It is not a threshold: a high value still refuses when trust is low, and a low value can accept when the alternative is worse. "
    "NAPact and Trade are the same kind of willingness for their treaties.",

("diplomacy", "NaturalRelChange"):
    "The baseline drift in relations per turn before events, treaties and actions adjust it. "
    "Positive values slowly heal a rivalry, negative values slowly poison a peace. "
    "AngerDissipation and TrustGainedAtPeace modify the same drift, so changing one without the others rarely has the intended effect.",

("solarsystems", "WhichPlanet"):
    "An index into PlanetTypes.Types, counted from zero in file order. "
    "Inserting a type in the middle re-points every system after it, which is the most common way a map mod silently changes its planets. "
    "planetScale then multiplies the chosen type's size; it does not change the type or its habitability.",

("solarsystems", "HomePlanet"):
    "Marks a planet as an empire start; the galaxy generator assigns a race to it. "
    "A system with no HomePlanet is still valid but is never a starting position. "
    "Population and the resource list are applied at generation, so editing them changes a new game, not an existing save.",

("ui", "VirtualSize"):
    "The coordinate system for the whole layout: every AbsPos and AbsSize in the file is measured against it. "
    "The engine scales those virtual pixels to the real window, so a 1920x1080 layout works at 2560x1440 without new numbers. "
    "Different aspect ratios are repositioned by the alignment fields, not by rewriting the layout.",

("ui", "AbsSize"):
    "Absolute width and height in virtual pixels; 0 means auto-fit from the texture, and 0 in one axis fits only that axis. "
    "This is what makes a button keep its art's proportions while its width follows the list. "
    "RelSize is the alternative: a fraction of the parent, with 0.5 meaning half.",

("ui", "Name"):
    "The element id code uses to find the control; the main menu binds new_game, load_game, options, mods, sandbox, info, support and exit by this string. "
    "Renaming it does not break the layout and does not produce an error: the element still draws and simply stops responding. "
    "Ids are also how panels are found for animation and hit tests, so keep them when copying a screen.",

("mainmenus", "UILayoutFile"):
    "The layout YAML for a main-menu background, relative to Content/, paired with a SceneFile that sets the camera and lighting. "
    "Default names which entry opens first; the others are alternatives the game can select. "
    "Both files are hot-reloadable, so a menu can be edited while it is on screen.",

("gametext", "NameIndex"):
    "An integer id looked up in GameText.yaml, not a key and not a file path. "
    "Content fields such as NameIndex and DescriptionIndex point at these ids, which is why a missing id shows the number or a blank instead of crashing. "
    "A mod only needs the ids it changes; the rest of the map is inherited.",

("textures", ".atlas"):
    "A manifest for a folder of sprite frames, not a single image: replacing one frame means replacing the folder and keeping the frame names. "
    "The loader finds sprites by name inside the atlas, so renaming a frame breaks the lookup even though the pixels are present. "
    "Plain .png and .dds files are simpler and replace by relative path.",

("fonts", ".xnb"):
    "The compiled font the game loads: the .spritefont beside it is only the recipe. "
    "Fonts are loaded by name from UI code, so a missing XNB throws when that font is first used rather than showing a placeholder. "
    "If you add a face, add both files and a Content.mgcb entry, then rebuild; a mod that ships only the .spritefont has nothing to load.",

("particles", ".mgfxo"):
    "A compiled MonoGame effect loaded by hardcoded name (Simple, MeshLighting, SkinnedEffect, BeamFX, Distort). "
    "The .fx source is for editing and is not read at runtime, and a .mgfx does not replace a .mgfxo on the OpenGL path. "
    "A missing compiled shader is fatal when its renderer starts, so keep the pair and match the MonoGame build.",

("particles", ".fx"):
    "The shader source; it does nothing at runtime until it is compiled to .mgfxo (and, on some paths, .xnb). "
    "Editing it in a mod without rebuilding changes nothing, which looks like a broken override rather than a missing build step. "
    "Use it to understand or recompile an effect, not as the file the game loads.",

("textures", ".png"):
    "The straightforward image case: a mod replaces it by putting a file at the same relative path under Textures/. "
    "The extension may differ when the loader probes both .png and .dds, but the stem must match. "
    "A missing image logs and draws a red placeholder, so the screen still runs and the mistake is visible rather than fatal.",

("textures", ".dds"):
    "A compressed texture used for large art such as ship and planet surfaces. "
    "It replaces by relative path like a PNG, and the loader accepts it wherever it probes both formats. "
    "Keep the same dimensions and mip expectation as the vanilla file, or the model can show stretched or black surfaces without an error.",

("globals", "MaxOpponents"): dict(
    l1="How many opponents the setup screen offers at most.",
    l2=("It caps the opponent button, which cycles from 1 to this value, and a corners game ignores it and "
        "uses 3. It is a new-game setting, so a save keeps the opponents it was created with."),
    range=("no loader bound; the setup screen uses 1 to this value in a standard game and 3 in a corners "
           "game. Math: the button cycles 1..value; 7 = seven opponents, 1 = a duel, 0 or less collapses "
           "to 1."),
    l3=("`MaxOpponents` caps the standard setup screen: the button increments from 1 and wraps back to 1 "
        "once the count passes it, and `GameSetupScreen.OnNumOpponentsClicked` substitutes 3 in a corners "
        "game. Vanilla 7 allows seven opponents, 1 forces a duel, and 0 makes every click reset the count "
        "to 1 because the wrap condition is always true. The loader does not clamp it, and a negative value "
        "behaves like 0 rather than producing an error. The setup screen is the only reader, so editing it "
        "changes nothing once a galaxy exists.")),

("globals", "DefaultNumOpponents"): dict(
    l1="How many opponents a default game starts with.",
    l2=("It is the initial count on the setup screen, not a cap, so the player can raise it up to "
        "MaxOpponents. A save keeps the count it was generated with."),
    range=("no loader bound; the setup screen expects 1..MaxOpponents. Math: the opening count is value, "
           "then clicks cycle 1..MaxOpponents; 5 = vanilla, 1 = a duel."),
    l3=("The setup screen opens on this many opponents, and its button then moves the count between 1 and "
        "`MaxOpponents`. Vanilla 5 leaves room for two more clicks up to the cap of 7, and a value above "
        "the cap still opens at that value until the first click wraps it. No loader clamp: 0 or a "
        "negative number shows an impossible start, so keep it within 1..MaxOpponents.")),

("globals", "StartingPlanetRichnessBonus"): dict(
    l1="Extra mineral richness on the empire's planets at galaxy generation.",
    l2=("It is added to every planet the empire owns when the galaxy is created, not just the capital, and "
        "the setup slider runs from 0 to 5. It does not touch worlds settled later, so it is a start bonus, "
        "not an empire modifier."),
    range=("the setup slider accepts 0 to 5; the YAML loader sets no bound. Math: richness = rolled "
           "richness + value; 0 = no bonus, 1 = +1 step (vanilla), 5 = +5 steps."),
    l3=("`planet.MineralRichness += StartingPlanetRichnessBonus` runs per owned planet in "
        "`FinalizeEmpires`, after the planet's own roll and before buildings, so 1 raises every starting "
        "world by one richness step. Vanilla 1 gives the capital a richness of 2 on a normal roll, but the "
        "same bonus also applies to the empire's other starting planets. The setup slider accepts 0 to 5; a "
        "YAML value is not clamped, so 10 is accepted and simply adds ten steps. A save keeps the richness "
        "it was generated with.")),

("globals", "ShipDestroyThreshold"): dict(
    l1="How much internal module damage a ship can take before it dies.",
    l2=("It is a share of the ship's internal-slot health, not its total hit points, and it also pulls each "
        "role's retreat threshold toward it. A higher value makes ships die and retreat earlier."),
    range=("no loader bound; the comparison expects a 0..1 share. Math: a ship dies when internal health "
           "share < value; 0 = only at zero, 0.5 = vanilla, 1 = any internal damage."),
    l3=("`InternalSlotsHealthPercent < ShipDestroyThreshold` kills the ship in `Ship_Events`, and "
        "`ShipResupply` blends a role's own threshold toward this value, so one number changes both death "
        "and when a ship leaves a fight. Vanilla 0.5 means a ship dies once half its internal health is "
        "gone; 0 keeps it fighting until the last internal module, and 1 kills it as soon as any internal "
        "damage lands. The loader does not clamp it, so a value outside 0..1 makes the comparison "
        "meaningless rather than producing an error. It is read from the globals whenever the checks run, "
        "not stored per ship.")),

("globals", "ShieldPowerMultiplier"): dict(
    l1="Multiplies every empire's shield power after its racial modifier.",
    l2=("It scales the empire's ShieldPowerMod, so 1 is neutral and 2 doubles the shields on every ship "
        "that empire builds. It does not change shield regeneration or module storage, which keep their own "
        "numbers."),
    range=("no loader bound. Math: shield strength = module shields \u00d7 (1 + empire ShieldPowerMod) "
           "\u00d7 value; 0.5 = half, 1 = vanilla, 2 = double."),
    l3=("`ShieldMod = EmpireDataMod(empire.data.ShieldPowerMod) * ShieldPowerMultiplier` in "
        "`EmpireHullBonuses.Update`, and `ShieldMod` scales shield strength on every hull the empire fields. "
        "Vanilla 1 is neutral; 0.5 halves every shield in the game and 2 doubles them, which is a blunter "
        "lever than editing individual shield modules. The loader does not clamp it, and a negative value "
        "makes the multiplier negative, which the combat math does not expect. It is applied when the "
        "empire's bonuses are rebuilt, so a change reaches existing ships on the next update.")),

("technology", "UID"): dict(
    l1="The tech's own id.",
    l2=("It is the node's id for LeadsTo and every unlock list; a second UID inside LeadsTo names a child "
        "tech, not another id for this node."),
    vanilla=("In vanilla: Technology/Ballistics/AdvancedKineticTurrets.xml \u2014 <UID>AdvancedKineticTurrets</UID>, "
             "then <LeadsTo><UID>MagneticTurrets</UID>; the second is a child tech, not this node."),
    l3=("The first `<UID>` in a tech file is the node's id; a `<UID>` inside `<LeadsTo><LeadsToTech>` "
        "names a child, which is why one file can show two values for this tag. Renaming the node without "
        "updating the files that lead to it breaks the branch silently, because LeadsTo is resolved by "
        "string. By convention the id matches the file stem, so an override at the same path replaces the "
        "same node; a different stem adds a second tech with the same id.")),

("technology", "MaxLevel"): dict(
    l1="Levels the tech can be researched.",
    l2=("A tech at level N can be researched N times, each level costing more through "
        "MultiLevelCostMultiplier. Most vanilla techs are level 1; the multi-level ones are the exception."),
    range=("no loader bound; 0 or less makes the tech unpurchasable. Math: the first level costs Cost, "
           "each later level multiplies by 1.4 by default; 1 = one purchase, 5 = five levels."),
    l3=("`MaxLevel` caps repeat research, and `TechEntry` prices each later level with "
        "`MultiLevelCostMultiplier`, whose default is 1.4. Bonus effects can scale with the level, so a "
        "level-5 tech is not just five times the price but a stronger effect. Vanilla mostly uses 1, with "
        "Refining Efficiency and a few others at 5; 0 or a negative value leaves the tech with no "
        "purchasable level, so keep it at 1 or more.")),

("modules", "UID"): dict(
    l1="The module's unique name.",
    l2=("The loader overwrites it with the file stem, so the tag documents the id rather than setting it; "
        "references use the stem."),
    l3=("`UID` is replaced from the file name at load, so editing only this line changes nothing: the "
        "design's ModuleUID, a tech's ModuleUID and the shipyard all resolve to the stem. Renaming the file "
        "renames the module and dangles every reference that still uses the old stem. Keep the tag equal to "
        "the stem so a reader can see the id the game will use.")),

("weapons", "UID"): dict(
    l1="The weapon's unique name.",
    l2=("It is overwritten from the file stem, and a module's WeaponType points at that stem."),
    l3=("The loader takes the stem as the UID, so a module whose `WeaponType` names anything else finds no "
        "weapon and leaves the mount inert with a log line. Renaming the file without updating the modules "
        "that use it is the common way to break a gun that still looks installed. Keep the tag equal to "
        "the stem; the value in the file is documentation.")),

("buildings", "Name"): dict(
    l1="Building UID and display name.",
    l2=("It is the join key techs use to unlock the building, and the string the build list and saves "
        "carry. A name no tech lists still loads, but the building is never buildable."),
    l3=("Techs unlock a building by this string, and the colony build list and save both key on it, so a "
        "rename breaks the unlock unless the tech is renamed with it. The capital, outpost, spaceport, "
        "terraformer and biosphere are also found by name in code, so a renamed copy is a new building "
        "without their behaviour. The loader reports nothing when the link is missing; the building simply "
        "never appears.")),

("races", "ShipType"): dict(
    l1="The race's ship-style id: the string that ties it to hulls, tech unlocks and its own text and name files.",
    l2=("Hulls carry a matching `Style`, and a tech's `<HullsUnlocked><ShipType>` applies only when it is "
        "empty, `ALL`, or this value, so the same tree gives each people a different hull list. The same "
        "string also picks the race's diplomacy lines, spy-name file, vanity-name pool and role labels, "
        "and the setup screen uses it to find the race's archetype."),
    range=("any string, but it must match the `Style` of the hulls you want and the keys already used by "
           "the dialogue, spy-name and ship-name files. Vanilla has 13 values: Terran for Human, plus "
           "Cordrazine, Pollops, Opteris, Draylok, Kulrathi, Vulfen, Ralyeh, Revoran, Draug, Corsair, "
           "Remnant and Unknown."),
    l3=("`WeCanBuildThis` refuses a design until its hull is in `UnlockedHullsDict`, which "
        "`TechEntry.UnLockHulls` fills only from tech entries whose `<ShipType>` passes "
        "`IsTypeUnlockableBy` — empty, `ALL`, or this value — so this is the field that makes a hull tech "
        "racial. The restriction is not permanent ownership: `CheckSource` also accepts a tech stolen from "
        "or conquered from that people, and `ShipStyleMatch` keeps an absorbed empire's styles buildable, "
        "which is how a race can end up flying another people's hulls. The same string drives UI and "
        "spawns: the design browser sorts the race's own style first, the race setup preview picks its "
        "largest cruiser, and scenario and faction spawns filter hulls by it. It also keys text and names "
        "— `Opinion_Positive_/Neutral_/Negative_<ShipType>` in the diplomacy file, "
        "`spynames_<ShipType>.txt` for agents (falling back to Humans), vanity names in "
        "`ShipNames/ShipNames.xml`, and race-specific role labels in `ShipRoles`. An empty value is "
        "replaced at load by the race's `Singular` with only a warning, after which its hull entries, "
        "dialogue keys and name files no longer match; a wrong value silently gives a race with a thinner "
        "hull list and blank opinion lines.")),

("races", "StartingScout"): dict(
    l1="The design an empire starts with as its scout.",
    l2=("It is a ship-design name, not a hull, and the empire spawns one ship from that design when the "
        "galaxy is created. The name must match a design in ShipDesigns/ or the empire falls back to a "
        "default."),
    l3=("The value is the design's `Name`, the same string a design file carries, and the starting fleet is "
        "built from it during galaxy generation. Vanilla gives each race its own scout, so the nine race "
        "files carry nine names; the line above quotes one. A name with no matching design logs and falls "
        "back to a default, which reads in play as the AI ignoring your ship rather than an error. Changing "
        "the design's contents changes every race that names it; changing only this line changes that "
        "empire's start.")),

("races", "Name"): dict(
    l1="The empire's name and its id: the exact string every other reference uses to find it.",
    l2=("Other files reach an empire by this text: `AbsorbedBy`, `RebelName`, an encounter's `Faction` "
        "and the espionage messages all resolve it through `GetEmpireByName`, which compares the string "
        "exactly. It is also what the player reads everywhere, from the diplomacy header to the colony "
        "list, so it is both a label and a join key."),
    range=("free text, but it doubles as an id: keep it unique and change every string that names this "
           "empire with it. Vanilla uses full titles, e.g. `The United Federation`, `Cordrazine "
           "Collective`, `The Remnant`, `Corsairs` and `Unknown`."),
    l3=("`AddEmpire` special-cases four values \u2014 `Cordrazine Collective`, `The Remnant`, `Unknown` and "
        "`Corsairs` \u2014 by setting `Universe.Cordrazine`, `Remnants`, `Unknown` and `Corsairs`, which the "
        "remnant storyline, portals and pirate spawning read, so renaming one of those races leaves the game "
        "running with that content quietly off. `AbsorbedBy` and rebellion creation compare the string "
        "against other empires' names, so a duplicate makes the second empire unresolvable. The save stores "
        "it as the player name and the difficulty and score screens print it, so it is the empire's whole "
        "identity rather than a display field. There is no localisation id behind it, so a translation must "
        "override the race file.")),

("races", "Singular"): dict(
    l1="One member of the race, used wherever a sentence talks about a single person.",
    l2=("It fills the `SING` token in story encounters, is the subject of the race-description paragraphs, "
        "labels the owner column in the planet and exotic-system lists, and appears in invasion alerts such "
        "as 'Human troops are landing'. It also becomes the race's `ShipType` when that field is left "
        "empty, so it decides the default hull family."),
    l3=("`EncounterInstance.FormatText` replaces `SING` with it, `SolarSystemBody.OwnerName` and "
        "`PlanetListScreenItem` print it, and `ResourceManager` copies it into `ShipType` when that field is "
        "blank. The race setup screen searches for the race whose `Singular` is exactly `Human` to choose "
        "its default selection, so renaming that value silently opens setup on the first major race instead. "
        "Empty text is accepted and produces blank subjects plus an empty `ShipType`, which then warns at "
        "load and strips that race's hull and dialogue keys. It is stored in the save, so a change reaches "
        "new games only.")),

("races", "Plural"): dict(
    l1="Many members of the race, used where the sentence treats them as a people.",
    l2=("The race-description builder inserts it before phrases like 'are natural sailors', the budget "
        "screen lists trade partners by it, and the espionage screen names the target people with it. Rebel "
        "factions replace it with `RebelPlur`, so a rebellion does not inherit the parent's name."),
    l3=("`RaceDesignScreen_RaceDescription` calls `.Plural(...)` on the generated paragraphs, which makes "
        "this the word the setup screen repeats most. `BudgetScreen` prints it in the trade list and "
        "`AgentListItem` in the espionage target list, while notifications use `Singular` instead, which is "
        "why both fields are needed. `CreateRebelsFromEmpireData` overwrites it with `RebelPlur` and "
        "`Singular` with `RebelSing` at rebellion time. There is no fallback and no localisation id, so an "
        "empty value leaves a gap in every one of those sentences.")),

("races", "Adj1"): dict(
    l1="An adjective for the race, substituted into story text.",
    l2=("Only the encounter formatter reads it: an `ADJ1` token in an event's text becomes this word. The "
        "race setup screen passes the value through unchanged and offers no field to edit it, so a custom "
        "race keeps the adjective of the file it was based on."),
    l3=("`EncounterInstance.FormatText` handles the `ADJ1` and `ADJ2` tokens and no other code reads either "
        "field. Vanilla sets `strange` in three race files and leaves the rest empty. The word is inserted "
        "as written with no capitalisation fix, so an event that opens a sentence with the token needs a "
        "capitalised value. An empty value substitutes nothing and leaves the event's sentence short rather "
        "than failing.")),

("races", "Adj2"): dict(
    l1="A second adjective for the race, used by the same event text as `Adj1`.",
    l2=("The encounter formatter substitutes it for an `ADJ2` token. Like `Adj1` it has no screen of its "
        "own and does not appear in the race description, so it only shows up where a hand-written event "
        "asks for it."),
    l3=("`EncounterInstance.FormatText` is the only reader, through the `ADJ2` case next to `ADJ1`. Vanilla "
        "sets `eerie` in the same three race files that set `strange`. The value is used verbatim, so "
        "capitalisation and punctuation come from the event, not from the field. A missing value produces "
        "an empty substitution with no warning.")),

("races", "PortraitName"): dict(
    l1="The race's portrait id and the key its per-race AI settings are filed under.",
    l2=("The game loads `Portraits/<value>` for the race's picture in diplomacy, espionage, the governor "
        "panel and the relations diagram, and uses the same string to find the race's block in "
        "`Research.yaml` and `Budgets.yaml`. It also names the Markov name file that labels planets in that "
        "empire's new systems."),
    l3=("`ResourceManager.Texture(\"Portraits/\" + PortraitName)` draws the picture everywhere it appears, "
        "and a missing texture logs and falls back to the red `NewUI/x_red` placeholder rather than failing. "
        "`ResearchOptions` matches its per-race block on this string or `All`, while `BudgetPriorities` reads "
        "only the `All` block and warns that every other block is ignored. `GetRandomNames` builds the path "
        "`NameGenerators/spynames_<value>.txt` and returns no generator when that file is absent, so planet "
        "naming in new systems quietly loses its custom names. `FindRebellion` compares this value against "
        "a rebel name, so two races sharing a value are treated as the same rebellion, which is why the "
        "three faction files reuse `unknown`. Vanilla uses the short name here even when `Name` is a full "
        "title (`Human`, not `The United Federation`).")),

("races", "FlagIndex"): dict(
    l1="Zero-based index of the sprite in the `Flags` atlas that marks this empire.",
    l2=("The flag is drawn on diplomacy cards, the relations diagram, colony and mining overlays, event "
        "popups and the espionage list, tinted with the empire colour. `0` is the first flag in the atlas, "
        "not 'no flag'; only a save header uses `-1` to mean that."),
    range=("0 to the flag count minus one; the setup screen clamps to that, a race file is not clamped. "
           "Vanilla runs from 3 (Human) to 64 (Corsairs and Unknown), and the count follows the `Flags` "
           "atlas."),
    l3=("`ResourceManager.Flag(index)` returns the sprite or null past the end of the atlas, and the draw "
        "helpers dereference it, so an out-of-range value throws in the first screen that draws the flag "
        "instead of showing a blank. `RaceDesignScreen` wraps its picker between 0 and `NumFlags - 1` and "
        "`SavedGame` stores the player's flag by index with `-1` for absent, but nothing corrects a race "
        "file. The value is cosmetic only: it changes which sprite marks the empire and nothing about its "
        "relations or strength.")),

("races", "DiplomacyDialogPath"): dict(
    l1="The file stem of the diplomacy lines this race speaks.",
    l2=("It names a file, not a path: the game looks for `DiplomacyDialogs/<Language>/<value>.xml` and "
        "reads its dialog sets for greetings, treaty exchanges and opinion lines. A mod file with the same "
        "name inherits every line it omits from the vanilla file, so only the changed lines need shipping."),
    l3=("`LoadDialogs` indexes the files by stem and `GetDiplomacyDialog` is a map lookup that throws "
        "`MapKeyNotFoundException` when the key is missing. Empire creation calls it unconditionally in "
        "`CreateEmpireFromEmpireData`, so a wrong value is fatal at game start, before the diplomacy screen "
        "is ever opened. `SharedDiplomacy` is loaded separately by that screen for generic lines and is not "
        "a fallback for this field. Vanilla gives the three faction files `Human`, because they reuse the "
        "human lines rather than shipping their own.")),

("races", "HomeworldName"): dict(
    l1="The name of the race's home planet, as shown in text.",
    l2=("It is a label, not a rename: the starting planet keeps whatever name its solar system file gives "
        "it, and this string is what the interface calls that world. It appears in the diplomacy intel "
        "line, the closing sentence of the race description and the espionage dossier's home-planet "
        "field."),
    l3=("`MainDiplomacyScreen` prints it under the Homeworld heading and "
        "`RaceDesignScreen_RaceDescription` ends with 'The <Singular> homeworld of <value>'. "
        "`DossierPanel` copies it into the agent's `HomePlanet` label, which is the only place espionage "
        "shows it. Galaxy generation never reads it, so changing it on an existing race changes text and "
        "nothing else, and a value that disagrees with the planet's real name is not an error. The human "
        "file and the three factions all name Earth.")),

("races", "HomeSystemName"): dict(
    l1="The file stem of the solar system where the empire starts.",
    l2=("Galaxy generation loads `SolarSystems/<value>.xml` for the empire's starting system, and that file "
        "supplies the homeworld the race begins on. If no file matches, the game generates a random system "
        "under the same name instead, so a typo costs the hand-built layout but not the start."),
    l3=("`CreateSystemPlaceHolders` calls `LoadSolarSystemData(HomeSystemName)` and keeps a null when the "
        "file is missing. `GenerateSystems` then takes the null branch and calls `GenerateRandomSystem` "
        "with the same name, while a non-null result goes through `GenerateFromData` and uses the file's "
        "planets, resources and placement. Several vanilla races share `Sol`, and two races naming the same "
        "system each get their own copy of its layout rather than sharing one. The field is read only when "
        "a galaxy is created, so a save keeps the system it was generated with.")),
}
