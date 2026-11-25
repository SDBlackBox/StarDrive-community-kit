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
    "The design a hangar launches, named exactly as the design's Name. "
    "Three reserved names turn the field into a switch: DynamicLaunch, DynamicInterceptor and DynamicAntiShip make the bay re-pick the empire's best design for that role at every launch, which is the auto-upgrade the design screen colours. "
    "The field is HangarShipUID; a lowercase hangarShipUID element matches no element on the template and is dropped without a warning. "
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
    "It is applied before the target's shield resistance, so the two multiply: a 0.9 weapon against a 20 percent resistant shield lands at 0.72 of its damage. "
    "The singular EffectVsShield is not a field on the template; the loader drops it, so only the plural spelling does anything.",

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
        "weapon and leaves the mount inert with a log line. Two files that share a stem in different folders collapse into one entry, the newer winning, so a copied weapon silently replaces the original. Renaming the file without updating the modules "
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


# Races: authored from ResourceManager.LoadEmpires, EmpireData, Pirates, Remnants and
# RacialTrait.LoadTraitConstraints. The l1/l2/l3 replace the short labels in moddable-data-world.py.
NOTES.update({
("races", "Traits"): dict(
    l1="The container the loader turns into EmpireData.Traits.",
    l2="LoadEmpires deserializes this block into the RacialTrait that almost every racial stat is read from.",
    l3="`EmpireData` has no fields of its own for race identity: `Name`, `Singular`, `ShipType` and the rest are pass-throughs to `Traits`. After loading, `LoadEmpires` repairs an empty `ShipType` from `Singular` with a warning, and `FixSpacePortScale` corrects a scale of zero or less. A tag written outside this block that also exists inside it is dropped, which is why the race files nest everything here."),
("races", "Name"): dict(
    l1="The race id, and the name the game shows for the empire.",
    l2="`EmpireData.Name` returns `Traits.Name`, and the save, `Universe.GetEmpireByName` and the encounter lookup all compare against that string.",
    l3="`EmpireData.Name` is a pass-through to `Traits.Name`, so this is the id, not only a label. The save stores empires by it, `Universe.GetEmpireByName` finds them by it, and `ResourceManager.GetEncounter` matches an encounter's `Faction` against it. Renaming it strands saved empires and any encounter written for the old string; `Singular` and `Plural` are separate and do not follow."),
("races", "VideoPath"): dict(
    l1="The empire's intro video, and the stem of its portrait.",
    l2="`ScreenMediaPlayer` plays it as the empire's video, and `RacialTrait.Icon` loads `Portraits/<VideoPath>`.",
    l3="`PlayVideo` is called with `empire.data.Traits.VideoPath`, and `RacialTrait.Icon` uses the same string as a portrait file name, falling back to `Portraits/Unknown`. One value therefore drives two assets, so a missing video and a missing portrait fail together. The string is a file stem, not a path with an extension."),
("races", "MusicCue"): dict(
    l1="The track this empire plays in peace.",
    l2="`ScreenMediaPlayer` plays it while the empire is selected and not at war, and swaps to `CombatMusic` during war.",
    l3="The cue is chosen in `ScreenMediaPlayer` and only when nothing is already playing, so it is the ambient theme rather than a jingle. A name that is not a loaded cue leaves the previous track playing, and the value is an audio file stem under `Audio`. War replaces it entirely, which is why a race that sets no cue still has combat music."),
("races", "Faction"): dict(
    l1="A non-zero value marks the file a faction rather than a playable people.",
    l2="`EmpireData.IsFaction` is `Faction > 0`, and `LoadEmpires` files such a race under `MinorEmpires` instead of `MajorEmpires`.",
    l3="`IsFactionOrMinorRace` also accepts the deprecated `MinorRace` bool, but this byte is the live switch. `EmpireAI` gives a faction its pirate or remnant persona only when this is set together with the matching flag. Corsairs and Draugar write 1; a major race writes nothing, and the setup screen offers only major races as a player pick."),
("races", "HullColors"): dict(
    l1="Which parts of a hull take the empire colour.",
    l2="`Empire.HullTintOf` uses the two-member `HullColorParts` enum, `None` or `Paint`, to decide whether a ship is tinted.",
    l3="`Empire.HullTint` passes this field and the empire colour to `HullTintOf`, which either paints the hull or leaves the texture alone; the new-game ship preview calls the same code. `HullColors` is not saved with the empire, so a loaded game reads it from the race file again. `None` is how a race keeps its ships in their authored livery while still owning a flag and border colour."),
("races", "SpacePortModel"): dict(
    l1="An optional model for this race's space station.",
    l2="`SpaceStation` loads it instead of the default station mesh when the race names one.",
    l3="`SpaceStation.HasRaceModel` requires a non-empty value, and `StaticMesh.LoadMesh` then builds the station from that path. `FixSpacePortScale` separately corrects `SpacePortScale` to 1 with a warning when it is zero or negative, so model and scale are the two halves of one override. Leaving the field empty uses the shared station model."),
("races", "TechTree"): dict(
    l1="This item has no function in game.",
    l2="Kulrathi.xml writes it, and no field of that name exists on EmpireData: the only TechTree in the build is ResourceManager's map of loaded technologies.",
    l3="`EmpireData` has no `TechTree` field, so the element is dropped with the other unknown ones. The tech an empire starts with comes from `UnlockedAtGameStart` entries in the tech files and the racial trait flags those entries test, not from the race file. Deleting the line changes nothing."),
("races", "WarpStart"): dict(
    l1="The sound cue for a ship's warp-in.",
    l2="`Ship_Warp.GetStartWarpCue` returns it when it is not null, and otherwise picks a cue from the hull's surface area.",
    l3="The fallback is `sd_warp_start_small` below 60 surface area, `sd_warp_start_large` above 350, and `sd_warp_start_02` in between. The same non-null test gates `GetEndWarpCue`, so a race that sets only `WarpEnd` gets neither override. The value is an audio cue name, not a path."),
("races", "WarpEnd"): dict(
    l1="The sound cue for a ship's warp-out.",
    l2="`Ship_Warp.GetEndWarpCue` returns it only when `WarpStart` is also set, because that is the condition the method tests.",
    l3="The test is `data.WarpStart != null`, so `WarpEnd` alone is ignored and the surface-area default plays instead: `sd_warp_stop_small`, `sd_warp_stop_large` or `sd_warp_stop`. Setting both fields is the only way to override the warp sounds completely. The field is a cue name, not an asset path."),
("races", "TroopNameIndex"): dict(
    l1="The GameText id for this race's troop name.",
    l2="`EmpireData.TroopName` wraps the index in a `LocalizedText`, and `Troop.Name` uses it for every troop the empire owns.",
    l3="The index must match an id in `GameText.yaml`; an id with no text resolves to an empty string, which is what the troop list then shows. `Bomb.ResolveSpecialBombActions` also renames freed Owlwok troops with the Cordrazine race's name taken from here. `TroopDescriptionIndex` is the description half of the same pair."),
("races", "TroopDescriptionIndex"): dict(
    l1="The GameText id for this race's troop description.",
    l2="`EmpireData.TroopDescription` wraps the index, and that text is what the troop tooltip shows.",
    l3="It is the companion of `TroopNameIndex` and obeys the same rule: the number is a localisation id, and an id with no entry renders blank. Neither index is validated at load, so a wrong number is a silent text bug rather than a load error."),
("races", "RebelName"): dict(
    l1="The empire name a rebellion is created under.",
    l2="`Empire_Espionage` looks the rebel empire up with `Universe.GetEmpireByName(data.RebelName)`.",
    l3="The string must match the name the rebel faction is actually created with, or the lookup returns null and the rebellion has no empire to hand planets to. It is the faction's full name, while `RebelSing` and `RebelPlur` are the display forms copied into its traits. A missing value still starts a rebellion, but its planets are not transferred."),
("races", "RebelSing"): dict(
    l1="The rebel faction's singular name.",
    l2="`UniverseState_Empires` copies it into `Traits.Singular` when it builds the rebel empire.",
    l3="The rebel faction is a real empire cloned from the parent, and its `Singular` and `Plural` are replaced from this pair so the UI calls its people something else. It does not affect who owns the planets; `RebelName` does that. An empty value leaves the rebel with the parent's singular name."),
("races", "RebelPlur"): dict(
    l1="The rebel faction's plural name.",
    l2="`UniverseState_Empires` copies it into `Traits.Plural` when it creates the rebel empire.",
    l3="It is the plural half of the same substitution as `RebelSing`, so a rebellion can call itself Confederates while keeping the parent's adjective and ship style. The pair is read once at creation and then saved with the new empire. Changing the tag does not rename a rebellion that already exists."),
("races", "EnvTerran"): dict(
    l1="Fertility multiplier for this race on Terran worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Terran`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Terran` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvTerranMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvOceanic"): dict(
    l1="Fertility multiplier for this race on Oceanic worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Oceanic`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Oceanic` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvOceanicMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvSteppe"): dict(
    l1="Fertility multiplier for this race on Steppe worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Steppe`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Steppe` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvSteppeMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvTundra"): dict(
    l1="Fertility multiplier for this race on Tundra worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Tundra`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Tundra` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvTundraMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvSwamp"): dict(
    l1="Fertility multiplier for this race on Swamp worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Swamp`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Swamp` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvSwampMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvDesert"): dict(
    l1="Fertility multiplier for this race on Desert worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Desert`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Desert` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvDesertMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvIce"): dict(
    l1="Fertility multiplier for this race on Ice worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Ice`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Ice` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvIceMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvBarren"): dict(
    l1="Fertility multiplier for this race on Barren worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Barren`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Barren` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvBarrenMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "EnvVolcanic"): dict(
    l1="Fertility multiplier for this race on Volcanic worlds.",
    l2="`Empire.EnvironmentalModifier` returns it for a colony of category `Volcanic`, and a trait option with the same climate multiplies it again.",
    l3="`EnvironmentalModifier` switches on `PlanetCategory.Volcanic` and returns this field, which scales the colony's fertility; 1 is neutral and below 1 is worse. `LoadTraitConstraints` multiplies it by the matching `EnvVolcanicMultiplier` from any selected trait, so race and trait stack. It cannot make an uninhabitable world colonisable: habitability comes from the planet type's own `Habitable` flag."),
("races", "PreferredEnv"): dict(
    l1="The climate this race treats as home.",
    l2="`EmpireData.PreferredEnvPlanet` exposes it and the colony and blueprint screens compare a planet's category against it.",
    l3="The new-game panel shows the race's preference and hides the row when it is Terran, which is the default. `LoadTraitConstraints` lets any trait option with a non-Terran `PreferredEnv` overwrite it, so the last such trait in the list decides. It is a preference, not a habitability flag: a world of another category still colonises, but the colony's fertility is measured against this climate."),
("races", "BaseShipLevel"): dict(
    l1="A level added to every ship this empire spawns.",
    l2="`Ship_Initialize` adds it to the hull's level, and the pirate and remnant AIs write it as their faction level rises.",
    l3="`Pirates` sets it to `level / 4` and `Remnants` to `Level / 3`, so a value in a race file is overwritten the first time either AI advances. The level feeds crew skill, and `Weapon.AimLevel` turns crew level into accuracy, which is why late-game pirate ships shoot straighter. It is a faction-tuning number rather than a racial constant."),
("races", "MinimumTroopLevel"): dict(
    l1="The troop level the AI treats as the rookie floor.",
    l2="`DefensiveCoordinator` scraps a troop at exactly this level, and the `Minimum Troop Level` tech bonus adds to the field in `TechEntry`.",
    l3="The comparison is `troop.Level == Us.data.MinimumTroopLevel`, so troops below it are not swept and troops above it are kept. The tech bonus of the same name raises the field mid-game, which is how an empire stops fielding level-1 troops. It is a level, not a percentage: the experience curve decides what reaching it costs."),
("races", "StartingShip"): dict(
    l1="A design name the load validates for the empire.",
    l2="`CheckForRequiredShipDesigns` resolves it and logs an error for a major race when no design carries that name, and `CarrierBays` returns it as a fallback fighter name.",
    l3="The assert runs once at content load, so a typo is a log line rather than a crash, and `IsFactionOrMinorRace` exempts factions from the complaint. The only other reader is `CarrierBays`, which falls back to it when a hull asks for a default fighter and names none. It is a design `Name`, not a file path."),
("races", "StartingScout"): dict(
    l1="The scout design the empire falls back to.",
    l2="`EmpireData.ScoutShip` returns the automation pick, then this field, then the literal `Unarmed Scout`, and the load asserts the resolved name.",
    l3="The precedence lives in `ScoutShip`, so a player who picks a scout in the automation window overrides this field without editing the race. An empty value still produces a usable scout, but it is the generic vanilla design rather than one matched to the race. The assert checks the resolved name, not the tag alone."),
("races", "PrototypeShip"): dict(
    l1="The design name that pays no upkeep.",
    l2="`ShipMaintenance.IsFreeUpkeepShip` returns true for any ship whose name matches, and the load asserts the design exists.",
    l3="The check has an overload for a live `Ship` and one for an `IShipDesign`, so the prototype and everything built to it are free. That makes the field a cost lever as well as a name, since pointing it at an expensive design removes that design's maintenance. Remnant empires are free regardless of the setting."),
("races", "DefaultColonyShip"): dict(
    l1="The colony ship the empire builds by default.",
    l2="`EmpireData.ColonyShip` returns the automation pick, then this field, then `Colony Ship`, and the load asserts it is a colony ship.",
    l3="The fallback chain means a race that names nothing still expands, using the vanilla design. The assert checks `IsColonyShip`, so a freighter here logs an error and the resolved name is still what the AI tries to build. The automation window lists the valid designs and writes the player's pick to `CurrentAutoColony`, which outranks this field."),
("races", "DefaultSmallTransport"): dict(
    l1="The freighter the empire builds by default.",
    l2="`EmpireData.FreighterShip` returns the automation pick, then this field, then `Small Transport`, and the load asserts both `IsFreighter` and `IsCandidateForTradingBuild`.",
    l3="Two asserts run on this one tag, so a design that can carry cargo but is not a trading candidate still logs an error. The `FreighterShip` fallback is what the AI uses when auto-freighters are left alone. The automation window exposes the same slot and stores the player's choice in `CurrentAutoFreighter`."),
("races", "DefaultTroopShip"): dict(
    l1="The troop transport the empire builds by default.",
    l2="`Empire.CommonInitialize` fills an empty value with `<PortraitName> Troop`, and the load asserts the result is a single-troop ship.",
    l3="Because the default is derived from `PortraitName`, a race that leaves the tag out looks for a design named after its portrait, which usually does not exist. `IsSingleTroopShip` is the shape the assert wants, so a multi-troop design here logs an error. Invasion goals ask the empire for its troop ship by this resolved name."),
("races", "DefaultConstructor"): dict(
    l1="The constructor the empire builds by default.",
    l2="`EmpireData.ConstructorShip` returns the automation pick, then this field, then `Terran Constructor`, and the load asserts `IsConstructor`.",
    l3="The literal fallback is a Terran design, so a race that names nothing here builds a ship from another people's tree. The assert is what catches a name that resolves to something that cannot build. The automation window stores the player's choice in `CurrentConstructor`, which outranks the tag."),
("races", "DefaultMiningShip"): dict(
    l1="The mining ship the empire builds by default.",
    l2="`Empire.GetMiningShipName` returns it when the design exists and otherwise `DefaultMiningShipName`, and the load asserts `BaseCargoSpace > 0`.",
    l3="The test is `ResourceManager.ShipTemplateExists`, so an empty or misspelt name silently falls back to the shared default. The cargo assert is the only check that the design can actually mine. Mining goals and the automation window both ask for the name through the same method."),
("races", "DefaultResearchStation"): dict(
    l1="The research station the empire builds by default.",
    l2="`EmpireData.ResearchStation` returns the automation pick, then this field, then `Basic Research Station`, and the load asserts `IsResearchStation`.",
    l3="The assert checks the role, not the name, so a station with the wrong role logs an error while the fallback still gives the AI something to build. Research goals ask for the resolved name, which means a race with no tag uses the vanilla station. The automation window writes the player's choice to `CurrentResearchStation`."),
("races", "DefaultMiningStation"): dict(
    l1="The mining station the empire builds by default.",
    l2="`EmpireData.MiningStation` returns the automation pick, then this field, then `Basic Mining Station`, and the load asserts `IsMiningStation`.",
    l3="As with the research station, the fallback keeps the AI working when the tag is absent and the assert only complains about the role. The station is built on a planet's mining slot, so the role is what makes it legal there. `CurrentMiningStation` outranks the tag once a player picks one."),
("races", "DefaultSalvageShip"): dict(
    l1="The salvage ship the empire builds when salvage ops are on.",
    l2="`SalvageShipDesignOf` returns it only when the design exists and `IsSalvageShip`, and the load warns when salvage ops are enabled and the race names none.",
    l3="The warning appears in `CheckForRequiredShipDesigns` only when `GlobalStats.Defaults.EnableSalvageOps` is set, so a mod that leaves the feature off never needs the tag. The automation window offers the same slot through `CurrentSalvageShip`. A design that exists but is not a salvage ship is treated as none."),
("races", "DefaultAssaultShuttle"): dict(
    l1="The shuttle used for boarding and troop landings.",
    l2="`Empire.GetAssaultShuttleName` returns it when the design exists, otherwise `BoardingShuttle.Name`, and troop bays launch with that name.",
    l3="The existence test is `ResourceManager.ShipTemplateExists`, so an empty value falls back to the shared boarding shuttle rather than failing. `ShipModule` sets a troop bay's `HangarShipUID` from this method, and `Ship_Troop` creates assault ships with it. It is a design name, and the assert checks only that it resolves."),
("races", "DefaultSupplyShuttle"): dict(
    l1="The shuttle that ferries ordnance and supplies.",
    l2="`Empire.GetSupplyShuttleName` returns it when the design exists, otherwise `DefaultSupplyShuttleName`, and supply bays and refund goals ask for it by that method.",
    l3="Supply bays, `DeliverRefund`, `RearmShipFromPlannet` and planet building all call the method, so one tag feeds every supply route the empire has. The fallback keeps those routes working when the tag is absent or misspelt. The load asserts `IsSupplyShuttle` on the value, which catches a freighter parked in the wrong slot."),
("races", "TraitSets"): dict(
    l1="The list of trait sets a race can start with.",
    l2="`RacialTrait.TraitSets` is filled from this block, and `LoadTraitConstraints` gives the player set 0 and the AI a random set.",
    l3="`PlayerTraitOptions` returns `TraitSets[0].TraitOptions`, and the AI path uses `random.Item(TraitSets)`, which is why the vanilla files comment that the first set is the player's. Each option name is matched against `RacialTraits.xml` and its modifiers are added to the race's traits; a name that matches nothing is skipped silently. A race with no sets gets no traits at all."),
("races", "TraitSet"): dict(
    l1="One trait set inside the list.",
    l2="The loader maps it to a `TraitSet` object whose only field is the `TraitOptions` list.",
    l3="`TraitSets` is an array of these, and the array order matters: index 0 is what a human player is offered and the rest are drawn for the AI. Moving a set therefore changes which traits a player sees. The element carries nothing else, so all of a set's meaning is in its options."),
("races", "TraitOptions"): dict(
    l1="The trait names that make up one set.",
    l2="`LoadTraitConstraints` adds each named option's modifiers to the race, and an unknown name is ignored without a warning.",
    l3="Each string must be a `TraitName` in `RacialTraits.xml`; the loop tests `Contains` against the loaded list, so a repeated name changes nothing. The options are added on top of the race's own fields, which is how a trait and a race bonus of the same name stack. What the player sees is the localised name of each option, not the string in the file."),
("races", "PersonalityTraitsWeights"): dict(
    l1="The pool the empire's diplomatic personality is drawn from.",
    l2="`UniverseState_Empires` picks one name per personality trait with `empire.Random.Item`, so a repeated name is weighted.",
    l3="Each name must be a `DTrait.Name` in `Diplomacy/DiplomaticTraits.xml`; an unknown string still consumes a draw and then contributes nothing. The draw fills `DiplomaticPersonality`, which sets war, peace and treaty behaviour. Listing a name three times is how a race is made reliably aggressive without forcing it."),
("races", "EconomicTraitsWeights"): dict(
    l1="The pool the empire's economic personality is drawn from.",
    l2="`UniverseState_Empires` picks one `ETrait` name with `empire.Random.Item`, and the result becomes `EconomicPersonality`.",
    l3="The names are `ETrait.Name` values from `Diplomacy/DiplomaticTraits.xml`, and an unrecognised name is a wasted draw. Weighting works by repetition, exactly as in the personality pool. The trait decides spending and research priorities rather than combat behaviour."),
("races", "R/G/B"): dict(
    l1="The three 8-bit channels of the empire colour.",
    l2="`RacialTrait.Color` casts each channel to a byte, and the flag, border and map tints all use the resulting colour.",
    l3="The cast is unchecked, so a value above 255 or below zero wraps instead of clamping. The three tags are read together into one `Color`, so a race that sets only one channel gets a strongly tinted empire rather than a neutral one. The new-game ship preview and the border drawing use the same colour."),
("races", "IsPirateFaction"): dict(
    l1="Marks the race as a pirate faction.",
    l2="`EmpireAI` gives the empire the pirate persona when this flag and `IsFaction` are both set, which is what starts tribute and raid goals.",
    l3="A race with the flag but no `Faction` value is an ordinary empire that never gets the pirate AI. The pair is read once when the empire is created, so editing the tag mid-game changes nothing. The persona is what loads `Pirates` and its base, raid and payment goals."),
("races", "IsRemnantFaction"): dict(
    l1="Marks the race as a remnant faction.",
    l2="`EmpireAI` gives the empire the remnant persona when this flag and `IsFaction` are both set.",
    l3="`Remnants` then owns the empire's goals, ship costs and guardian behaviour, and every ship it spawns is marked `IsGuardian`. As with pirates, the flag does nothing without a non-zero `Faction`. The persona is chosen at creation, so a save keeps the one it was made with."),
("races", "PirateBaseBasic"): dict(
    l1="The basic pirate base design.",
    l2="`PirateForces` uses it while the effective level is 4 or less, and `GetBaseNames` counts it as a base for defence.",
    l3="The effective level is the faction level times a difficulty multiplier (0.7 on normal, 0.8 on hard), so easier games stay on this tier longer. `GetBaseNames` returns all three tiers, which is how `IsBase` recognises a base whatever built it. A missing design leaves that tier with no base."),
("races", "PirateBaseImproved"): dict(
    l1="The improved pirate base design.",
    l2="`PirateForces` uses it for effective levels 5 to 9, between the basic and advanced bases.",
    l3="The tier swap is a single `if/else` on the effective level, so the improved base exists only while the faction is in that band. All three names are listed together in `GetBaseNames`, which is what lets the AI find its bases after an upgrade. An empty value makes the band build nothing."),
("races", "PirateBaseAdvanced"): dict(
    l1="The advanced pirate base design.",
    l2="`PirateForces` uses it above effective level 9, and `GetBaseNames` keeps recognising it as a base.",
    l3="This is the tier a long-lived pirate faction builds, and nothing in the AI chooses it directly: it falls out of the level check. The design must exist for the AI to spawn a base at all, and a missing one is not replaced by the lower tiers. That makes the tag the difference between a raider and a faction with a home."),
("races", "PirateFighterBasic"): dict(
    l1="The basic pirate fighter design.",
    l2="`PirateForces` uses it up to effective level 4 and `AddToShipWeCanSpawn` lists it for raids.",
    l3="`Pirates.AdvanceInShips` adds the improved fighter at level 5 and the advanced at 8, so this design is the starting wing and then a fallback. The fighter is also what a pirate carrier launches, which is why it must be a fighter-role design. An empty value leaves the faction unable to field fighters."),
("races", "PirateFighterImproved"): dict(
    l1="The mid-tier pirate fighter design.",
    l2="`AdvanceInShips` adds it at level 5, and `PirateForces` uses it for effective levels 5 to 9.",
    l3="`AdvanceInShips` also adds it to `ShipsWeCanSpawn` and, if the empire cannot build it, adds the design as buildable so carriers can launch it. The tier is skipped entirely when the name is empty, with a warning that points at the race XML. It replaces the basic fighter for the band rather than sitting beside it."),
("races", "PirateFighterAdvanced"): dict(
    l1="The top-tier pirate fighter design.",
    l2="`AdvanceInShips` adds it at level 8, and `PirateForces` uses it above effective level 9.",
    l3="Like the improved tier, it is added to the spawn list and made buildable so carriers can launch it. The pair of level checks means a faction can reach the advanced fighter before the advanced base, since the base needs level 10. An empty design leaves the top band with the previous tier's fighter."),
("races", "PirateFrigateBasic"): dict(
    l1="The basic pirate frigate design.",
    l2="`PirateForces` uses it up to effective level 4, and `AddToShipWeCanSpawn` lists it as a raid ship.",
    l3="The frigate is the pirate line ship, so this design is what a young faction fights with. `AdvanceInShips` replaces it at level 7 with the improved frigate and at 10 with the advanced. An empty value leaves raiding parties without a line ship."),
("races", "PirateFrigateImproved"): dict(
    l1="The mid-tier pirate frigate design.",
    l2="`AdvanceInShips` adds it at level 7, and `PirateForces` uses it for effective levels 5 to 9.",
    l3="It arrives later than the improved fighter and slaver, which is the intended curve: frigates are the last hull a pirate faction upgrades. `AddToShipWeCanSpawn` is what makes the design appear in raids. A missing name is logged and the band keeps the previous frigate."),
("races", "PirateFrigateAdvanced"): dict(
    l1="The top-tier pirate frigate design.",
    l2="`AdvanceInShips` adds it at level 10, and `PirateForces` uses it above effective level 9.",
    l3="This is the last ship tier the pirate AI reaches, so a faction with this design and an advanced base is at its ceiling. It is added to the spawn list the same way as the lower tiers, and made buildable when carriers need it. An empty value is a faction that never fields its best hull."),
("races", "PirateSlaverBasic"): dict(
    l1="The basic pirate boarding-ship design.",
    l2="`PirateForces` uses it as the boarding ship up to effective level 4, and `AddToShipWeCanSpawn` lists it for raids.",
    l3="`PirateForces` names the field `BoardingShip`, which is what the AI uses when it wants to capture rather than destroy. `AdvanceInShips` upgrades it at level 6 and again at 9. A faction with no slaver can still raid, but it cannot take ships."),
("races", "PirateSlaverImproved"): dict(
    l1="The mid-tier pirate boarding-ship design.",
    l2="`AdvanceInShips` adds it at level 6, and `PirateForces` uses it for effective levels 5 to 9.",
    l3="It is the first upgrade a pirate faction gets at level 6, ahead of the improved frigate, which is what makes capture the mid-game pirate tactic. The design is added to the spawn list so it appears in raids. An empty name is logged and the previous slaver is kept."),
("races", "PirateSlaverAdvanced"): dict(
    l1="The top-tier pirate boarding-ship design.",
    l2="`AdvanceInShips` adds it at level 9, and `PirateForces` uses it above effective level 9.",
    l3="The advanced slaver arrives one level before the advanced frigate, so a faction at that point can take ships it could not before. It is added to the spawn list like the other tiers. A missing design ends the boarding upgrades and leaves the AI with the improved slaver."),
("races", "PirateStationBasic"): dict(
    l1="The basic pirate orbital station design.",
    l2="`PirateForces` uses it while the effective level is 4 or less, and `GetStationNames` counts it as a station for defence.",
    l3="Stations are separate from bases: `GetStationNames` feeds the defensive list, and `IsBase` only looks at the base names. The tier is chosen by the same effective-level check as the base. A missing design leaves the low band without orbitals."),
("races", "PirateStationImproved"): dict(
    l1="The improved pirate orbital station design.",
    l2="`PirateForces` uses it for effective levels 5 to 9, and `GetStationNames` keeps recognising it.",
    l3="The station upgrades on the same schedule as the base, so the two swap together when the faction crosses level 5. `GetStationNames` is what lets the AI find and defend its orbitals. An empty value means that band builds no station."),
("races", "PirateStationAdvanced"): dict(
    l1="The advanced pirate orbital station design.",
    l2="`PirateForces` uses it above effective level 9, and `GetStationNames` still returns it for defence.",
    l3="It is the orbital a mature pirate faction defends with, chosen by the level check rather than by any explicit upgrade goal. The design must exist for the AI to spawn one. Nothing falls back to a lower station, so an empty value is an undefended band."),
("races", "PirateFlagShip"): dict(
    l1="The design the pirate flagship is spawned from.",
    l2="`SpawnFlagShip` creates it once at half the faction's maximum level, and `StaysAtBase` keeps it home.",
    l3="`SpawnFlagShip` refuses to create a second ship with that name, so the flag is a singleton. `PirateForces` also records it as `FlagShip`, and `StaysAtBase` prevents the AI from sending it on raids. An empty value means the faction never gets a flagship."),
("races", "PiratePaymentPeriodTurns"): dict(
    l1="Turns between pirate tribute demands.",
    l2="`Pirates.RefusedPaymentPeriodTurns` scales it by `ProductionPace`, and the payment goal uses that as the delay.",
    l3="The pace scaling keeps the same number of turns passing at every game speed, and it applies only to the refusal cooldown. The value does not change how much is demanded, only how often. A value of 0 turns the demand into an every-turn event."),
("races", "MinimumColoniesForStartPayment"): dict(
    l1="The colony count at which a pirate begins demanding tribute.",
    l2="`PirateDirectorPayment` compares the victim's colony count with `Pirates.MinimumColoniesForPayment`, which returns this field.",
    l3="The goal is only sent when the victim is at or above the threshold, so a higher number delays tribute until the target is worth robbing. The comparison uses the victim's planet count at the moment the goal runs, not at game start. Zero makes every empire a target on contact."),
("races", "RemnantFighter"): dict(
    l1="The design the remnant AI spawns as its fighter.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Fighter`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantCorvette"): dict(
    l1="The design the remnant AI spawns as its corvette.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Corvette`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantBeamCorvette"): dict(
    l1="The design the remnant AI spawns as its beam corvette.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.BeamCorvette`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantBattleCorvette"): dict(
    l1="The design the remnant AI spawns as its battle corvette.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.BattleCorvette`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantSupportSmall"): dict(
    l1="The design the remnant AI spawns as its small support ship.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.SmallSupport`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantAssimilator"): dict(
    l1="The design the remnant AI spawns as its assimilator.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Assimilator`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantTorpedoCruiser"): dict(
    l1="The design the remnant AI spawns as its torpedo cruiser.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.TorpedoCruiser`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantCruiser"): dict(
    l1="The design the remnant AI spawns as its cruiser.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Cruiser`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantCarrier"): dict(
    l1="The design the remnant AI spawns as its carrier.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Carrier`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantMotherShip"): dict(
    l1="The design the remnant AI spawns as its mothership.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Mothership`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantExterminator"): dict(
    l1="The design the remnant AI spawns as its exterminator.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Exterminator`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantInhibitor"): dict(
    l1="The design the remnant AI spawns as its inhibitor.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Inhibitor`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantBattleship"): dict(
    l1="The design the remnant AI spawns as its battleship.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.BattleShip`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantBomber"): dict(
    l1="The design the remnant AI spawns as its bomber.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Bomber`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantFrigate"): dict(
    l1="The design the remnant AI spawns as its frigate.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Frigate`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantBomberLight"): dict(
    l1="The design the remnant AI spawns as its light bomber.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.BomberLight`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantBomberMedium"): dict(
    l1="The design the remnant AI spawns as its medium bomber.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.BomberMedium`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantBehemoth"): dict(
    l1="The design the remnant AI spawns as its behemoth.",
    l2="`Remnants.CalculateShipCosts` registers it as `RemnantShipType.Behemoth`, and `SpawnShip` returns it for that type.",
    l3="`AddShipCost` logs `Could not find a ship named ... in <race>'s race xml` when the name is empty or matches no design, and the type is then skipped rather than substituted. Every ship spawned this way is marked `IsGuardian`, which keeps it out of ordinary fleet filtering. It is a design `Name`, so a file rename without a tag edit breaks the spawn."),
("races", "RemnantPortal"): dict(
    l1="The design the remnant portal is built from.",
    l2="`SpawnShip` returns it for `RemnantShipType.Portal`, and `Empire_Borders` treats a ship of that name as the remnants' portal.",
    l3="The portal is what projects remnant borders, so the name is compared in `Empire_Borders` as well as used to spawn the hull. `Remnants` also has a portal goal, but it targets the ship rather than reading this tag again. A missing design means no portal and no projected border."),
("races", "RemnantMotherShip"): dict(
    l1="The design the remnant AI spawns as its mothership.",
    l2="`CalculateShipCosts` registers it as `RemnantShipType.Mothership`, and `SpawnShip` returns it for that type.",
    l3="The mothership is one of the types the spawn table can pick, and its cost is what the remnant economy pays before it appears. An empty name is logged and the type is skipped. Like every remnant spawn, the ship is marked `IsGuardian`."),
("races", "ThrustColor0R"): dict(
    l1="The red channel of thruster colour 1.",
    l2="`Empire.CreateThrusterColors` packs the three channels into `ThrustColor0`, and the particle colour modes of the same name use it.",
    l3="The particle system's `ThrustColor0` mode tints a plume with this colour, which is how two races' drives look different. The channels are bytes, so a value outside 0-255 throws during deserialization rather than wrapping. Colour 1 and colour 2 are separate, which lets a race fade one drive colour into another."),
("races", "ThrustColor0G"): dict(
    l1="The green channel of thruster colour 1.",
    l2="`Empire.CreateThrusterColors` packs the three channels into `ThrustColor0`, and the particle colour modes of the same name use it.",
    l3="The particle system's `ThrustColor0` mode tints a plume with this colour, which is how two races' drives look different. The channels are bytes, so a value outside 0-255 throws during deserialization rather than wrapping. Colour 1 and colour 2 are separate, which lets a race fade one drive colour into another."),
("races", "ThrustColor0B"): dict(
    l1="The blue channel of thruster colour 1.",
    l2="`Empire.CreateThrusterColors` packs the three channels into `ThrustColor0`, and the particle colour modes of the same name use it.",
    l3="The particle system's `ThrustColor0` mode tints a plume with this colour, which is how two races' drives look different. The channels are bytes, so a value outside 0-255 throws during deserialization rather than wrapping. Colour 1 and colour 2 are separate, which lets a race fade one drive colour into another."),
("races", "ThrustColor1R"): dict(
    l1="The red channel of thruster colour 2.",
    l2="`Empire.CreateThrusterColors` packs the three channels into `ThrustColor1`, and the particle colour modes of the same name use it.",
    l3="The particle system's `ThrustColor1` mode tints a plume with this colour, which is how two races' drives look different. The channels are bytes, so a value outside 0-255 throws during deserialization rather than wrapping. Colour 1 and colour 2 are separate, which lets a race fade one drive colour into another."),
("races", "ThrustColor1G"): dict(
    l1="The green channel of thruster colour 2.",
    l2="`Empire.CreateThrusterColors` packs the three channels into `ThrustColor1`, and the particle colour modes of the same name use it.",
    l3="The particle system's `ThrustColor1` mode tints a plume with this colour, which is how two races' drives look different. The channels are bytes, so a value outside 0-255 throws during deserialization rather than wrapping. Colour 1 and colour 2 are separate, which lets a race fade one drive colour into another."),
("races", "ThrustColor1B"): dict(
    l1="The blue channel of thruster colour 2.",
    l2="`Empire.CreateThrusterColors` packs the three channels into `ThrustColor1`, and the particle colour modes of the same name use it.",
    l3="The particle system's `ThrustColor1` mode tints a plume with this colour, which is how two races' drives look different. The channels are bytes, so a value outside 0-255 throws during deserialization rather than wrapping. Colour 1 and colour 2 are separate, which lets a race fade one drive colour into another."),
})


# Buildings: authored from Building.cs and the colony, technology and bombardment code.
NOTES.update({
("buildings", "AllowInfantry"): dict(
    l1="Marks a building that houses infantry.",
    l2="`Building.CalcMilitaryStrength` counts it as a military building when it is set, and `Technology` classifies it for tech bonuses.",
    l3="`Building.cs` reads it at line 472 while it adds the building to the planet's military score, and `Technology.cs` treats a building with it as military when it decides which techs apply. It is a flag, not a capacity: how many troops a planet holds comes from the planet. A building without it adds nothing to the defence score."),
("buildings", "AllowShipBuilding"): dict(
    l1="Lets the planet build ships while the building stands.",
    l2="`Planet_ConstructionQueue` sets `HasSpacePort` when it is true, and `Technology` counts it as a production building.",
    l3="The queue computes `HasSpacePort |= b.IsSpacePort || b.AllowShipBuilding`, so any building with this flag enables the planet's ship construction. Losing the last such building stops ship building even if the capital remains. The field grants the ability, not a design list."),
("buildings", "BuildOnlyOnce"): dict(
    l1="Restricts the building to a single build order.",
    l2="`Building.IsSuitableForBlueprints` excludes it from plans, and `Empire` consults the existing buildings before ordering it.",
    l3="`IsSuitableForBlueprints` returns false for a build-once building, so blueprints never place it. `Empire.cs` also checks the planet's buildings before it hands the order out. The per-planet duplicate limit is `Unique`; this flag is the stricter, empire-facing version."),
("buildings", "CanBeCreatedFromLava"): dict(
    l1="Lets the building appear when lava on a tile solidifies.",
    l2="`Volcano` filters the buildings it may create with this flag.",
    l3="`Volcano.cs` builds its candidate list from `ResourceManager.BuildingsDict` filtered on `CanBeCreatedFromLava`, so a building without it can never replace cooling lava. `ImmueToLava` is the other half, protecting an existing building from the eruption. Both are read only when a tile changes."),
("buildings", "CanBeTerraformed"): dict(
    l1="Lets the building's tile be terraformed.",
    l2="`PlanetGridSquare.TerrainCanBeTerraformed` requires it, and `Planet.HasTerrainToTerraform` looks for it across the planet.",
    l3="The predicate is `BuildingOnTile && Building.CanBeTerraformed`, so only a building that sets the flag has its tile improved. `HasTerrainToTerraform` is the same check over every tile, and the terraforming tech uses it to decide whether the investment buys anything. A building without it protects its tile."),
("buildings", "CanBuildAnywhere"): dict(
    l1="Lets the building ignore tile restrictions.",
    l2="`Building.cs` uses it when it places an event building and when it searches for a valid tile.",
    l3="The flag appears twice in `Building.cs`: once to stop an event building forcing a random habitable tile (line 414), and once in the tile filter at line 426, where an ordinary building needs `NoBuildingOnTile`. A building with it can sit on any free tile, which is how crash sites and event structures land anywhere."),
("buildings", "CannotBeBombed"): dict(
    l1="Excludes the building from orbital bombardment.",
    l2="`SolarSystemBody` skips a tile whose building has this flag when it picks a bombardment target.",
    l3="The check is `!TargetTile.BuildingOnTile || TargetTile.Building.CannotBeBombed`, so such a tile is never chosen. That protects the building from orbit without giving it hit points. It does not protect it from invasion or ground combat."),
("buildings", "Category"): dict(
    l1="The palette group the building is listed under.",
    l2="The type is `BuildingCategory`, and the colony build list groups and sorts by it.",
    l3="`BuildingCategory` is a fixed enum, so a value outside it becomes the default. The label does not change behaviour; it decides which tab lists the building and which filter the AI uses when it looks for a kind of building. `Technology` classifies buildings from their numbers, not from this field."),
("buildings", "CombatStrength"): dict(
    l1="Attack strength of a building that fights.",
    l2="`Building.IsAttackable` is `CombatStrength > 0`, and the planet's military score adds it.",
    l3="A building with a positive value becomes a target in ground combat and contributes to the planet's defence estimate. `Technology.cs` also counts it as a military building when it sorts tech bonuses. It is not hit points: `Strength` is what absorbs damage."),
("buildings", "Cost"): dict(
    l1="Production cost of the building before pace scaling.",
    l2="`Building.ActualCost` multiplies it by `ProductionPace`, and the colony build list and research popup show that result.",
    l3="`ActualCost(e)` is `Cost * e.Universe.ProductionPace`, so the file's number is the cost at pace 1. The build list, the deep-space building window and the research popup all display the scaled figure. Maintenance is a separate field and does not follow the cost."),
("buildings", "CreditsPerColonist"): dict(
    l1="Credits per colonist per turn.",
    l2="`Building.IsMoneyBuilding` is true when it is positive, and the colony income calculation adds it.",
    l3="It is a per-colonist rate, so its value grows with the planet's population rather than sitting flat. `IsMoneyBuilding` uses it for tech classification and the colony summary. A planet with no colonists gets nothing from it."),
("buildings", "Defense"): dict(
    l1="Defence of the building against bombardment.",
    l2="The field is the defensive half of the combat stat pair, while `SoftAttack` and `HardAttack` are the offensive half.",
    l3="The code comment states the purpose: defence versus bombardment, not ground attack. Ground combat builds its stat block from the attack fields and the building's `Strength`, so a building with only `Defense` cannot fight a landing. It is separate from `PlanetaryShieldStrengthAdded`, which protects the whole planet."),
("buildings", "DefenseShipsCapacity"): dict(
    l1="How many defence ships the building supports.",
    l2="`Building.CalcMilitaryStrength` multiplies the chosen design's strength by it, and zero skips the building.",
    l3="When the value is zero the building is left out of the defence-ship calculation; otherwise the picked design's strength is multiplied by it and added to the planet's score. The role of those ships is `DefenseShipsRole`. It is a count of slots, not a build queue."),
("buildings", "DefenseShipsRole"): dict(
    l1="The ship role the building launches for defence.",
    l2="`GetDefenseShipName` and `ShipBuilder.PickFromCandidates` use it to choose a design.",
    l3="The value is a `RoleName`, so a misspelt role falls back to the enum default instead of being rejected. `PickFromCandidates` chooses from the empire's buildable designs for that role, which lets a building defend with a newer hull without a content edit. The count is `DefenseShipsCapacity`."),
("buildings", "DescriptionIndex"): dict(
    l1="GameText id for the building's tooltip.",
    l2="`Building.DescriptionText` wraps it in a `LocalizedText`.",
    l3="The index is a `GameText.yaml` id, and an id with no text shows an empty tooltip. Nothing validates it at load. `ShortDescriptionIndex` is the one-line version used in lists."),
("buildings", "EventOnBuild"): dict(
    l1="Exploration event triggered when the player finishes the building.",
    l2="`Planet_ConstructionQueue` looks it up in `ResourceManager.Event` and runs it once.",
    l3="The trigger runs only for the player and only on completion, which makes it a story hook rather than a modifier. A name that matches no event logs an error and does nothing. `EventTriggerUID` is the other direction: an event already placed on the map."),
("buildings", "EventSpawnChance"): dict(
    l1="Percent chance this event building appears on a generated planet.",
    l2="`SolarSystemBody` rolls it with `Random.RollDice` when it picks an event building for a tile.",
    l3="`RollDice` takes a byte percentage, so 100 always places the building and 0 never does. It is consulted only while the planet is generated, which is why editing it does not change an existing galaxy. `NoRandomSpawn` removes a building from the pool entirely."),
("buildings", "EventTriggerUID"): dict(
    l1="Event id this building links to on the map.",
    l2="`Building.EventHere` is true when it is set, and `PlanetGridSquare` resolves it through `ResourceManager.Event`.",
    l3="A non-empty value marks the building as an event site (`EventHere`), and the event can then fire when the tile is visited. The name is an `ExplorationEvent` file stem, and a bad one leaves the tile inert. It is read when the event fires, not at generation."),
("buildings", "FoodCache"): dict(
    l1="Food storage the building adds.",
    l2="`IsBadCacheResourceBuilding` warns when a cache exists without any food production on the same building.",
    l3="The field is storage, so it raises the planet's buffer rather than its output. `Building.cs` warns when `FoodCache > 0` and both `PlusFlatFoodAmount` and `PlusFoodPerColonist` are zero, which catches a cache with nothing to cache. The warning fires during generation, in `SolarSystemBody`, not at load."),
("buildings", "HardAttack"): dict(
    l1="Attack strength against hard targets.",
    l2="`Combat` builds its attacker stat block from `ActualHardAttack`, which is derived from this field.",
    l3="Hard targets are buildings and armour; soft targets are troops and light structures, which `SoftAttack` covers. The value is not damage per hit, because `Combat` rolls attacks against the defender's strength. A building with neither attack field cannot fight on the ground."),
("buildings", "ImmueToLava"): dict(
    l1="Protects the building from lava destroying its tile.",
    l2="`PlanetGridSquare.ImmuneToLava` returns true when the building sets it.",
    l3="The field is misspelled in the code (`ImmueToLava`), so the correct spelling in a file is dropped. A protected building survives an eruption that would otherwise clear the tile. `CanBeCreatedFromLava` is the other half, controlling what appears after lava cools."),
("buildings", "Income"): dict(
    l1="Flat credits per turn from the building.",
    l2="`Building.IsMoneyBuilding` counts it, and the colony income code adds it when it is above zero.",
    l3="Unlike `CreditsPerColonist`, this is a flat sum that does not scale with population. `IsMoneyBuilding` treats it as a money building for tech classification and the colony summary. It is gross income, with `Maintenance` subtracted separately."),
("buildings", "IncreaseRichness"): dict(
    l1="Mineral richness the building adds to the planet.",
    l2="The building description prints it, and the colony's richness total adds it.",
    l3="It raises the richness that mining and production-per-richness read, so its effect is multiplicative rather than a flat income. `Building.cs` prints it in the description when it is non-zero. `PlusProdPerRichness` is the field that turns that richness into production."),
("buildings", "Infrastructure"): dict(
    l1="Infrastructure the building adds to the colony.",
    l2="`Building.cs` prints it in the description, and the colony's infrastructure total adds it.",
    l3="Infrastructure is what a colony needs to support its population and buildings, so this is an indirect production field. It is shown in the building description when non-zero. It does not change the building's own cost or upkeep."),
("buildings", "InvadeInjurePoints"): dict(
    l1="Damage the building does to invading troops.",
    l2="`PlanetGridSquare` applies it during an invasion, and the building's defence score adds twenty times it.",
    l3="The invasion code reads the value from the building on the tile, so a fortress can hurt the landing force before the ground fight starts. The military score weights it at 20 per point, which is how it affects the planet's estimated strength. Zero is the default and means no invasion damage."),
("buildings", "IsCommodity"): dict(
    l1="Marks the building as a commodity structure.",
    l2="`Building.IsSuitableForBlueprints` excludes commodities, and `IsEventTerraformer` requires the flag together with terraform points.",
    l3="The field is read twice: blueprint planning skips a commodity (line 142), and a commodity with `PlusTerraformPoints > 0` is an event terraformer. It does not by itself make the building buildable from the colony list. `CommodityRequired` and `ResourceCreated` are the separate trade fields."),
("buildings", "Maintenance"): dict(
    l1="Credits per turn the building costs.",
    l2="`Building.GetMaintenanceCost` scales it by the empire's civilian maintenance modifier.",
    l3="The deep-space building window prints the scaled figure, and the colony upkeep total adds it. `CivMaintMod` on the empire multiplies it, which is why a tech that reduces civilian maintenance changes the number without touching the file. It is a cost, so the colony budget subtracts it."),
("buildings", "MaxFertilityOnBuild"): dict(
    l1="Fertility ceiling the building adds to its tile.",
    l2="`MaxFertilityOnBuildFor` multiplies it by the empire's racial environment modifier for the planet's category.",
    l3="The per-empire helper is what the colony screen and the blueprint screen call, so the same building is worth different amounts to different races. It is a ceiling rather than a flat addition, so a tile already at that fertility gains nothing. `PlusTerraformPoints` is the other way buildings change fertility."),
("buildings", "MaxPopIncrease"): dict(
    l1="Maximum population the building adds.",
    l2="`Building.ProducesPopulation` and the population-relevance check at line 398 use it.",
    l3="It raises the planet's population cap, so its effect only appears once the colony fills the old one. A zero value makes the building not population-relevant, which is what the tech classification tests. It does not change the growth rate."),
("buildings", "NameTranslationIndex"): dict(
    l1="GameText id for the building's name.",
    l2="`Building.TranslatedName` wraps it, and the build list shows that text.",
    l3="The index must match an id in `GameText.yaml`; the loader copies it into every clone of the building. An index with no text shows blank rather than the XML `Name`, because the display path uses the localised string only. `DescriptionIndex` and `ShortDescriptionIndex` are the other two text ids."),
("buildings", "NoRandomSpawn"): dict(
    l1="Keeps the building out of the random event pool.",
    l2="`SolarSystemBody` filters event buildings with `EventHere && !NoRandomSpawn`.",
    l3="That filter decides which buildings can be placed as a random ruin on a generated tile. Setting it means the building appears only when an event or a file names it. `EventSpawnChance` is the frequency for the ones that stay in the pool."),
("buildings", "PlanetaryShieldStrengthAdded"): dict(
    l1="Planetary shield strength the building adds.",
    l2="The planet's shield total adds it, and `Technology` counts it as a defensive building.",
    l3="The value goes into the planet's shield pool, which bombardment must break before it reaches the buildings. `Technology.cs` classifies a building with it above zero as defensive when it sorts tech bonuses. It is separate from `Defense`, which is the building's own bombardment resistance."),
("buildings", "PlusFlatFoodAmount"): dict(
    l1="Flat food produced per turn.",
    l2="`Building.ProducesFood` and the colony food total use it.",
    l3="It is a flat amount, unlike `PlusFoodPerColonist`, so it does not scale with population. A building with it above zero counts as food-producing for tech classification and for the bad-cache warning. Negative values are allowed and make the colony consume food."),
("buildings", "PlusFlatPopulation"): dict(
    l1="Population added when the building completes.",
    l2="`Building.ProducesPopulation` is true when it is positive.",
    l3="The value lands once rather than per turn, which is how a colony pod or a biosphere raises a new colony's headcount. `MaxPopIncrease` is the cap version of the same idea. Tech classification counts a building with it as population-relevant."),
("buildings", "PlusFlatProductionAmount"): dict(
    l1="Flat production per turn.",
    l2="`Building.ProducesProduction` includes it, and the colony production total adds it.",
    l3="It does not scale with colonists or richness, which makes it the field for a fixed-output building. `PlusProdPerColonist` and `PlusProdPerRichness` are the scaling versions. A negative value is a production cost."),
("buildings", "PlusFlatResearchAmount"): dict(
    l1="Flat research per turn.",
    l2="`Building.ProducesResearch` returns true when it is positive, and the colony research total adds it.",
    l3="It is the unscaled research field; `PlusResearchPerColonist` scales with population. The colony research total adds both, and `Technology` classifies a building with either as a research building. Negative values reduce output."),
("buildings", "PlusFoodPerColonist"): dict(
    l1="Food produced per colonist.",
    l2="`Building.ProducesFood` includes it, and the colony food total multiplies it by population.",
    l3="Because it scales with colonists, a large colony gains more from the same building than a small one. `PlusFlatFoodAmount` is the unscaled partner. A building with only this field produces nothing on a planet with no population."),
("buildings", "PlusProdPerColonist"): dict(
    l1="Production per colonist.",
    l2="`Building.ProducesProduction` includes it, and the colony production total scales it by population.",
    l3="It is the population-scaled production field, distinct from `PlusFlatProductionAmount` and `PlusProdPerRichness`. The colony total multiplies it by the number of colonists. A building with only this produces nothing on an empty world."),
("buildings", "PlusProdPerRichness"): dict(
    l1="Production per point of mineral richness.",
    l2="`Building.ProducesProduction` includes it, and the colony total scales it by the planet's richness.",
    l3="This is the mining-shaped field: a rich planet gets more from it and a barren one gets nothing. `IncreaseRichness` can change the input, so the two fields interact. It is not scaled by population."),
("buildings", "PlusResearchPerColonist"): dict(
    l1="Research per colonist.",
    l2="`Building.ProducesResearch` includes it, and the colony research total scales it by population.",
    l3="It is the population-scaled research field; `PlusFlatResearchAmount` is the flat partner. The loader does no validation, so a negative value is simply a research drain. Tech classification treats any positive value here as a research building."),
("buildings", "PlusTaxPercentage"): dict(
    l1="Tax rate the building adds.",
    l2="`Building.IsMoneyBuilding` counts it, and the colony tax calculation adds it to the rate.",
    l3="It is a percentage contribution to the colony's tax rate, not credits, so its effect depends on the population and goods being taxed. `CreditsPerColonist` and `Income` are the direct money fields. A negative value lowers the rate."),
("buildings", "PlusTerraformPoints"): dict(
    l1="Terraforming points the building provides.",
    l2="`IsEventTerraformer` requires it together with `IsCommodity`, and the terraforming tech counts it.",
    l3="Terraform points are spent to raise a planet's fertility, so a building with them is what makes a world worth terraforming. `Technology.cs` treats a building with them as food-related when it sorts tech bonuses. `MaxFertilityOnBuild` caps what the tile can gain."),
("buildings", "ProdCache"): dict(
    l1="Production storage the building adds.",
    l2="`IsBadCacheResourceBuilding` warns when a cache exists without any production on the same building.",
    l3="It is storage, so a colony keeps a stock instead of losing overflow. The warning fires when `ProdCache > 0` and all three production fields are zero, which catches a cache with nothing to hold. `StorageAdded` is the general storage field beside it."),
("buildings", "Scrappable"): dict(
    l1="Whether the building can be scrapped.",
    l2="`Building.IsSuitableForBlueprints` requires it, and the defence picker only scraps buildings that have it.",
    l3="`Planet_BuildDefenses` looks for the weakest military building that is also `Scrappable`, so a protected building is never removed for a new one. Blueprints also skip a non-scrappable building. The default is true, so the tag is written only to protect something."),
("buildings", "SensorRange"): dict(
    l1="Sensor radius the building adds.",
    l2="`Building.IsSensor` is `SensorRange > 0`, and the planet's sensor range includes it.",
    l3="A planet's coverage is the largest of its buildings' ranges, which is what `Empire_Borders` uses when it marks known space. `Technology.cs` classifies a building with it as a sensor building. The value is in world units, the same as a ship's `SensorRange`."),
("buildings", "ShipRepair"): dict(
    l1="Base ship repair rate the building provides.",
    l2="`Building.cs` multiplies it by `GlobalStats.BaseShipyardRepair` before the rate is used.",
    l3="The multiplier in `Globals.yaml` means the file's number is a base rate rather than the final one. The rate decides how fast docked ships are repaired each turn. A building without it contributes no repair."),
("buildings", "ShortDescriptionIndex"): dict(
    l1="GameText id for the one-line description.",
    l2="`Building.cs` prints it in lists when the index is above zero.",
    l3="It is the short form used in the build list and tooltips, while `DescriptionIndex` is the long form. An index of zero means the field is skipped and the list falls back to the name. A wrong id shows blank rather than the XML text."),
("buildings", "ShowOnPlanetList"): dict(
    l1="Shows the building in the planet list.",
    l2="`PlanetListScreenItem` adds it to the colony's icon row when the flag is set.",
    l3="The planet list is the sidebar of colony icons, and this flag decides which buildings get one. It is a display field only: hiding a building from the list does not hide it from the colony screen or the AI. `Category` still controls which build tab lists it."),
("buildings", "StorageAdded"): dict(
    l1="General storage the building adds.",
    l2="The colony storage total adds it, and the description prints it when non-zero.",
    l3="It raises the planet's capacity for stored resources, which stops overflow being lost. `FoodCache` and `ProdCache` are the specialised versions. The value does not change production or income."),
("buildings", "Strength"): dict(
    l1="Hit points of the building.",
    l2="`IsAlive` and `IsDestroyed` compare it with zero, and ground combat reduces it.",
    l3="The default is 5, so a building that omits the tag dies to the first hits; most content sets a larger number. `IsAlive` is simply `Strength > 0`, and infantry combat subtracts damage from it. `CombatStrength` is the attack value, not the health."),
("buildings", "Unique"): dict(
    l1="Allows only one of the building per planet.",
    l2="`SBProduction` refuses a second copy and logs a warning.",
    l3="The check is `q.Building.Unique && P.BuildingBuilt(q.Building.BID)`, so a duplicate is dropped from the queue with a warning rather than built silently. `BuildOnlyOnce` is the broader build-order restriction. A unique building can still exist on every planet."),
("buildings", "Weapon"): dict(
    l1="Weapon template the building fires.",
    l2="`Building.IsWeapon` is true when it is non-empty, and the planet's defence code loads it through `GetWeapon`.",
    l3="The string is a weapon UID, and a missing one logs an error when the building tries to fire. Buildings use the same weapon stats as ships, including range and damage, without a module to mount them. `AttackTimer` and `WeaponTimer` pace the shots."),
("buildings", "WinsGame"): dict(
    l1="Marks the building as a victory condition.",
    l2="`Planet_ConstructionQueue` sets `HasWinBuilding` when it is true.",
    l3="One building with this flag on any of an empire's planets is enough to set the win flag, so a mod can make a hidden structure the objective. The check runs when the queue finishes the building, not continuously. It is the only building field the victory code reads."),
})

NOTES.update({
("buildings", "SoftAttack"): dict(
    l1="Attack strength against soft targets.",
    l2="`Combat` builds its attacker stat block from `ActualSoftAttack`, which is derived from this field.",
    l3="Soft targets are troops and light structures, while hard targets are buildings and armour, which `HardAttack` covers. The value is not damage per hit: `Combat` rolls attacks against the defender's strength. A building with neither attack field cannot fight on the ground."),
})
