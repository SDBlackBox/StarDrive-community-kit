"""Tier 2, tier 3 and asset families for the moddable-content page.

Same shape as moddable-data.py. Kept separate so the ship-data half stays readable.
"""

G = lambda title, l1, l2, l3, tags: dict(title=title, l1=l1, l2=l2, l3=l3, tags=tags)
T = lambda name, ty, l1, l2="", l3="", **kw: dict(name=name, ty=ty, l1=l1, l2=l2, l3=l3, **kw)

# The categories in PlanetCategory, in the order the enum declares them. Category is a label the
# generator and the moon table use; colonisation comes from each type's own Habitable flag, so the
# gloss must not claim a category is or is not colonisable.
PLANET_CATEGORIES = {
 "Barren": "Rocky, airless worlds and moons; every vanilla Barren type sets BaseFertility to 0.",
 "Desert": "Dry worlds; their fertility comes from the type's own BaseFertility, not the label.",
 "Steppe": "Grass-and-dust worlds; one of the fertile categories a race can prefer as a homeworld.",
 "Tundra": "Cold worlds; the vanilla Tundra types are colonisable and allow Ice moons.",
 "Terran": "The reference garden world, and the category a race means by a comfortable homeworld.",
 "Volcanic": "Hostile rock; only one of vanilla's four Volcanic types sets Habitable, the rest are barren.",
 "Ice": "Frozen worlds; vanilla Ice types are colonisable with fertility ranges around zero.",
 "Swamp": "Wet, low-lying worlds; fertile and colonisable in vanilla.",
 "Oceanic": "Water worlds; the highest fertility and population per tile in vanilla.",
 "GasGiant": "Never a colony in vanilla: no Habitable flag, only a 20% mining chance, and generation adds 1 to its scale.",
}

# PreferredEnv takes the same members, but the value means "this race's homeworld climate" and sets
# the neutral point its other Env*Multiplier fields are measured against.
PREFERRED_ENV = {c: f"The homeworld is {c}, and {c} is the climate this race measures the others against."
                 for c in PLANET_CATEGORIES}

# AtmosphereTypes presets, read from PlanetTypes.yaml. Glow is [R,G,B,alpha]; alpha is intensity,
# Fresnel scales the rim glow, and the two No* flags switch a layer off.
SPRITE_BLEND = {
 "None": "Draws with blending off, so the layer replaces whatever is behind it.",
 "AlphaBlend": "Normal transparency: the layer's alpha decides how much of the star shows through.",
 "Additive": "Adds the layer's colour to the background, so overlapping layers brighten; vanilla uses it for the back rings.",
 "NonPremultiplied": "The classic alpha blend for non-premultiplied textures: keeps the gradient without over-brightening overlaps.",
}

EXPLOSION_TYPES = {
 "Ship": "The set the game uses when a ship is destroyed; the caller passes this type.",
 "Projectile": "The set projectiles and hull debris pass when they explode.",
 "Photon": "A separate set, picked by a weapon that names Photon in its ExplosionType.",
 "Warp": "A separate set for warp effects; the manager keeps it in its own bucket.",
}

PARTICLE_COLORS = {
 "Default": "White, so the emitter's own colour is used unchanged.",
 "EmpireColor": "The colour of the empire that owns the effect.",
 "ThrustColor0": "The owning empire's first thruster colour.",
 "ThrustColor1": "The owning empire's second thruster colour.",
}

BUTTON_STYLES = {
 "Default": "The standard 168px top-bar button texture.",
 "Small": "The 68px button, used where the bar has no room.",
 "Low80": "A low-profile button 80px tall.",
 "Low100": "A low-profile button 100px tall.",
 "Medium": "The 132px golden-brown button.",
 "MediumMenu": "The 132px menu button, drawn greyed out.",
 "BigDip": "The 168px dipped variant.",
 "Military": "The 168px military-coloured button.",
 "Close": "The close button texture.",
 "ResearchQueueUp": "The research queue's up arrow.",
 "ResearchQueueDown": "The research queue's down arrow.",
 "ResearchQueueCancel": "The research queue's cancel icon.",
 "ResearchQueueToTop": "The research queue's move-to-top icon.",
 "DanButton": "The wide brown dan_button.",
 "DanButtonBlue": "The same wide button in blue.",
 "DanButtonRed": "The same wide button in red.",
 "EventConfirm": "The big wide confirm button used by event popups.",
 "Text": "Draws only the text, with no button background.",
}

# ExoticBonusType members, read from Good.cs. The empire keeps one bonus entry per value, keyed in a
# Map, so two mineable goods that name the same type collide rather than stacking.
EXOTIC_BONUS_TYPES = {
 "None": "No bonus: the good is mined and stored, but no empire stat reads it.",
 "Credits": "Credit income; consumption scales with the empire's population in billions.",
 "ShieldRecharge": "Shield regeneration; consumption scales with the recharge the fleet produces.",
 "DamageReduction": "Damage reduction on every ship; consumption scales with fleet surface area.",
 "Production": "Gross production; consumption scales with the production made before exotics.",
 "RepairRate": "Ship repair rate; consumption scales with the repair the fleet and colonies do.",
 "WarpSpeed": "Warp speed; consumption scales with the fleet's total warp thrust.",
}

DYSON_STAGES = {
 "1": "The first ring set: four back and four front layers, with a fixed structure only the textures may change.",
 "2": "The second ring set vanilla ships, with the same fixed layer structure as stage 1.",
}

ATMOSPHERE_PRESETS = {
 "None": "Carries no option at all: the type gets no glow, no clouds and no rim change from it.",
 "Clouds": "Loads a cloud texture, so the planet draws a separate cloud layer over the surface.",
 "NoHalo": "Switches the faint white halo towards the sun off.",
 "NoAtmosphere": "Switches the atmosphere sphere off, so the rim loses its subtle colour.",
 "Barren": "Red-brown glow (152,29,5) at 0.10 intensity, fresnel 1.0.",
 "BarrenRed": "The same red-brown glow at 0.30 intensity, fresnel 1.0.",
 "VolcanicRed": "The same red-brown glow at 0.45 intensity, the strongest of the three, fresnel 1.0.",
 "IceBlue": "Pale blue glow (180,220,255) at 0.50 intensity, fresnel 1.0.",
 "SwampAqua": "Green-aqua glow (44,204,149) at 0.50 intensity, fresnel 1.0.",
 "OceanicBlue": "Blue glow (57,146,215) at 0.60 intensity, fresnel 1.0.",
 "TerranBlue": "The same blue at 0.40 intensity, fresnel 0.6, so the rim is softer than Oceanic.",
 "TundraBlue": "Blue-grey glow (57,146,195) at 0.35 intensity, fresnel 1.0.",
 "SteppeYellow": "Yellow glow (249,229,91) at 0.35 intensity, fresnel 0.4.",
 "DesertOrange": "Orange glow (172,79,25) at 0.40 intensity, fresnel 1.0.",
 "GasYellow": "Yellow glow (249,229,91) at 0.40 intensity, fresnel 0.25.",
 "GasOrange": "Orange glow (172,79,25) at 0.40 intensity, fresnel 1.0.",
 "GasAqua": "Green-aqua glow (44,204,149) at 0.20 intensity, fresnel 1.0.",
 "GasBlue": "Blue glow (57,146,215) at 0.40 intensity, fresnel 1.0.",
}

FAMILIES = [

# ---------------------------------------------------------------- tier 2
dict(id="buildings", tier=2, title="Buildings", paths=["Buildings"], ext=".xml", roots=["Building"],
     fmt="XML", loader="ResourceManager.LoadBuildings → Building",
     override="XML unifies by file name. The building Name is the UID techs and planets use.",
     l1="A structure a colony can build: what it costs to keep, what it adds, and what it does in a fight.",
     l2="Buildings are the colony's modules. Flat and per-colonist bonuses are separate fields, and some buildings are hard-coded by name (capital, outpost, biospheres, spaceport, terraformer).",
     l3="Icon names a sprite family: Buildings/icon_<Icon>_48x48 and _64x64 must exist. Cost, Maintenance and Income are credits; Strength is building HP; BID is assigned at load, not authored.",
     notation=dict(title="Copy this: a minimal building", body="""
<p>Vanilla's smallest building is ten lines and sets no localisation ids. It still loads, appears under its <code>Category</code> and can be placed:</p>
<pre class="code">&lt;Building&gt;
  &lt;Name&gt;Biospheres&lt;/Name&gt;
  &lt;Icon&gt;biosphere&lt;/Icon&gt;
  &lt;Cost&gt;180&lt;/Cost&gt;
  &lt;Maintenance&gt;.1&lt;/Maintenance&gt;
  &lt;CanBuildAnywhere&gt;true&lt;/CanBuildAnywhere&gt;
  &lt;Unique&gt;false&lt;/Unique&gt;
&lt;/Building&gt;</pre>
<ul>
<li><b>Name</b> is the id. Make yours unique and add it to a tech's unlock list, or nothing will offer the building.</li>
<li><b>Icon</b> is a family, not a path: <code>icon_biosphere_48x48</code> and <code>icon_biosphere_64x64</code> must both exist under <code>Buildings/</code>.</li>
<li>Copy the file into <code>Mods/&lt;YourMod&gt;/Buildings/</code> (any subfolder, any file name) and restart.</li>
</ul>"""),
     groups=[
 G("Identity", "What it is and where it shows.", "Name is the UID used by techs and the colony build list.", "Unique and BuildOnlyOnce are different: one per empire versus one per planet or game.", [
   T("Name","string","Building UID and display name.","", ""),
   T("NameTranslationIndex","int","Localised name.","", ""),
   T("DescriptionIndex","int","Localised description.","", ""),
   T("ShortDescriptionIndex","int","Short tooltip id.","", ""),
   T("Icon","string","Icon family name.","Buildings/icon_<Icon>_48x48 and _64x64.", ""),
   T("ShowOnPlanetList","bool","Appears in the colony list.","", ""),
   T("Unique","bool","One per empire.","", "true"),
   T("BuildOnlyOnce","bool","Cannot be rebuilt after being destroyed.","", ""),
   T("Scrappable","bool","Can be scrapped.","", "true"),
   T("CanBuildAnywhere","bool","No terrain or fertility requirement.","", ""),
   T("NoRandomSpawn","bool","Only placed by events, never by galaxy generation.","", ""),
   T("WinsGame","bool","Owning it wins the game.","", ""),
   T("Category","enum","UI grouping.","", ""),
 ]),
 G("Cost and income", "What it costs and what it earns.", "Maintenance is per turn; Cost is the build price before pace.", "Income and PlusTaxPercentage are credits; a negative Income is a cost.", [
   T("Cost","float","Build cost.","", ""),
   T("Maintenance","float","Upkeep per turn.","The budget screen's building line.", ""),
   T("Income","float","Flat credits per turn.","", ""),
   T("PlusTaxPercentage","float","Extra tax rate.","0.1 = +10%.", ""),
   T("CreditsPerColonist","float","Credits per colonist per turn.","", ""),
 ]),
 G("Population, food and terrain", "What it does to the colony's growth.", "Flat and per-colonist bonuses stack with fertility.", "MaxPopIncrease raises the cap; MaxFertilityOnBuild changes the tiles when built.", [
   T("MaxPopIncrease","float","Population cap added.","", ""),
   T("PlusFlatPopulation","float","Flat population added.","", ""),
   T("PlusFlatFoodAmount","float","Flat food per turn.","", ""),
   T("PlusFoodPerColonist","float","Food per colonist.","", ""),
   T("FoodCache","float","Food storage added.","", ""),
   T("MaxFertilityOnBuild","float","Fertility the planet is raised to when built.","", ""),
   T("CanBeTerraformed","bool","Terraforming can replace it.","", ""),
   T("CanBeCreatedFromLava","bool","Can appear when lava cools.","", ""),
   T("ImmueToLava","bool","Immune to lava (spelling is the field's).","", ""),
 ]),
 G("Production, research and storage", "What it adds to the colony's output.", "Flat and per-colonist fields are added separately.", "ProdCache and FoodCache are storage, not production.", [
   T("PlusFlatProductionAmount","float","Flat production.","", ""),
   T("PlusProdPerColonist","float","Production per colonist.","", ""),
   T("PlusProdPerRichness","float","Production per richness point.","", ""),
   T("PlusFlatResearchAmount","float","Flat research.","", ""),
   T("PlusResearchPerColonist","float","Research per colonist.","", ""),
   T("StorageAdded","int","Storage capacity.","", ""),
   T("Infrastructure","float","Infrastructure added.","", ""),
   T("ProdCache","float","Production storage.","", ""),
 ]),
 G("Combat and defence", "What it contributes to a fight.", "Ground attack values are separate from orbital defence.", "DefenseShipsRole names a role; the building launches that role up to capacity.", [
   T("Strength","int","Building hit points.","Destroyed at 0.", "5"),
   T("CombatStrength","int","Military strength contributed.","", ""),
   T("SoftAttack","int","Attack against soft troops.","", ""),
   T("HardAttack","int","Attack against hard troops.","", ""),
   T("Defense","int","Defence against bombardment.","", ""),
   T("CannotBeBombed","bool","Immune to orbital bombing.","", ""),
   T("PlanetaryShieldStrengthAdded","float","Planetary shield added.","", ""),
   T("Weapon","string","Weapon UID fired from orbit.","", ""),
   T("InvadeInjurePoints","int","Damage to invaders.","", ""),
   T("DefenseShipsCapacity","int","Defence ships launched.","", ""),
   T("DefenseShipsRole","string","Role of those ships.","", ""),
   T("AllowShipBuilding","bool","The colony may build ships here.","A spaceport or shipyard flag.", ""),
   T("IsCommodity","bool","Counts as a tradeable commodity.","", ""),
   T("ShortDescription","string","Short tooltip text.","", ""),
   T("TechBranch","string","Legacy research branch label.","Use the tech tree's unlocks instead.", ""),
   T("AllowInfantry","bool","Can train infantry.","", ""),
 ]),
 G("Events and modifiers", "What it triggers or changes.", "EventOnBuild and EventTriggerUID point at an exploration event.", "EventSpawnChance is a percentage roll.", [
   T("EventOnBuild","string","Event fired on completion.","", ""),
   T("EventTriggerUID","string","Event UID.","", ""),
   T("EventSpawnChance","int","Percent chance to fire.","", "15"),
   T("PlusTerraformPoints","float","Terraforming points per turn.","", ""),
   T("SensorRange","float","Sensor range added.","", ""),
   T("ShipRepair","float","Ship repair per second at the colony.","Multiplied by the global repair value.", ""),
   T("IncreaseRichness","float","Mineral richness added.","", ""),
 ]),
 ]),

dict(id="troops", tier=2, title="Troops", paths=["Troops"], ext=".xml", roots=["Troop"],
     fmt="XML", loader="ResourceManager.LoadTroops → Troop",
     override="XML unifies by file name; Name is the UID.",
     l1="A ground unit: its strength, attacks, cost and animation.",
     l2="Troops fight on planets and in boarding. Level raises their attacks; range grows at level 5.",
     l3="TexturePath points into Textures/Troops and is loaded as an atlas. Several XML tags (MaintenanceCost, Movement, MaxStrength) do not map to a public field of the same name, so treat them as balanced-but-unverified until tested.",
     notation=dict(title="Copy this: a minimal troop", body="""
<p>Trimmed from <code>Troops/Antlion.xml</code>. The animation block is what makes a unit visible; the combat block is what makes it useful.</p>
<pre class="code">&lt;Troop&gt;
  &lt;Name&gt;Antlion&lt;/Name&gt;
  &lt;Description&gt;Strange and violent creatures.&lt;/Description&gt;
  &lt;RaceType&gt;Unknown&lt;/RaceType&gt;
  &lt;TexturePath&gt;Antlion/antlion_idle_01&lt;/TexturePath&gt;
  &lt;Icon&gt;antlion&lt;/Icon&gt;
  &lt;animated&gt;true&lt;/animated&gt;
  &lt;idle_path&gt;Antlion/antlion_idle_&lt;/idle_path&gt;
  &lt;attack_path&gt;Antlion/antlion_attack_&lt;/attack_path&gt;
  &lt;num_idle_frames&gt;7&lt;/num_idle_frames&gt;
  &lt;num_attack_frames&gt;6&lt;/num_attack_frames&gt;
  &lt;Cost&gt;25&lt;/Cost&gt;
  &lt;Strength&gt;10&lt;/Strength&gt;
  &lt;MaxStrength&gt;10&lt;/MaxStrength&gt;
  &lt;SoftAttack&gt;45&lt;/SoftAttack&gt;
  &lt;HardAttack&gt;25&lt;/HardAttack&gt;
  &lt;Range&gt;1&lt;/Range&gt;
  &lt;Class&gt;Infantry&lt;/Class&gt;
  &lt;TargetType&gt;Soft&lt;/TargetType&gt;
&lt;/Troop&gt;</pre>
<ul>
<li><b>Strength and MaxStrength</b> start equal: the first is current hit points, the second the cap. A lower Strength ships the unit already damaged.</li>
<li><b>RaceType</b> is the race that may build it; creatures and neutral units use <code>Unknown</code>. A race whose own value does not match never sees the troop.</li>
<li><b>TexturePath</b> is an atlas stem under <code>Textures/Troops</code>; <b>Icon</b> resolves to <code>TroopIcons/&lt;Icon&gt;_icon</code>.</li>
</ul>"""),
     groups=[
 G("Identity and cost", "What the unit is and what it costs.", "Cost is modified by difficulty and production pace at build time.", "Class and TargetType decide what it can attack.", [
   T("Name","string","Troop UID and display name.","", ""),
   T("RaceType","string","Race that may build it.","", ""),
   T("Class","string","Unit class.","", ""),
   T("TargetType","enum","What it can attack.","", ""),
   T("Cost","float","Build cost.","", ""),
   T("Description","string","Tooltip.","", ""),
   T("Icon","string","Icon name.","TroopIcons/<Icon>_icon.", ""),
 ]),
 G("Combat", "How hard it hits and how much it takes.", "Hard attack beats armour, soft attack beats infantry.", "Each level adds 5% to both attacks; range +1 at level 5.", [
   T("Strength","float","Current hit points at load.","Do not edit per-instance.", ""),
   T("MaxStrength","float","Maximum hit points.","", ""),
   T("HardAttack","int","Attack against hard targets.","", ""),
   T("SoftAttack","int","Attack against soft targets.","", ""),
   T("Range","int","Attack range in tiles.","", ""),
   T("BoardingStrength","int","Strength when boarding a ship.","", ""),
   T("Movement","float","Movement allowance.","See the note above.", ""),
   T("AttackTimerBase","int","Delay between attacks.","", "10"),
   T("MoveTimerBase","int","Delay between moves.","", "10"),
   T("MaintenanceCost","float","Upkeep per turn.","Present in the files; verify it is read before balancing around it.", ""),
   T("sound_attack","string","Attack sound cue.","", ""),
 ]),
 G("Animation", "How the unit is drawn.", "A texture atlas plus frame counts and offsets.", "A missing atlas falls back to the default texture.", [
   T("TexturePath","string","Atlas texture.","Textures/Troops/.", ""),
   T("animated","bool","Has animation frames.","", ""),
   T("idle_path","string","Idle animation name.","", ""),
   T("attack_path","string","Attack animation name.","", ""),
   T("num_idle_frames","int","Idle frame count.","", ""),
   T("num_attack_frames","int","Attack frame count.","", ""),
   T("first_frame","int","First frame index.","", "1"),
   T("attack_width","int","Attack frame width.","", "128"),
   T("idle_x_offset","int","Idle horizontal offset.","", ""),
   T("idle_y_offset","int","Idle vertical offset.","", ""),
   T("MovementCue","string","Move sound.","", ""),
 ]),
 ]),

dict(id="goods", tier=2, title="Goods", paths=["Goods"], ext=".yaml", roots=["Good"],
     fmt="YAML", loader="ResourceManager.LoadGoods → YamlParser.DeserializeArray<Good>",
     override="One file. A mod's Goods.yaml replaces vanilla's list; the blocks are not merged one by one.",
     l1="Every resource the game knows: the three cargo goods freighters carry and the six exotics mined at gas giants.",
     l2="Only Goods/Goods.yaml is read. It deserializes straight into Good, one block per good, and the UID is the id. The per-good XML files beside it are legacy: nothing loads them, so editing Name, Mass or Cost there changes nothing in play.",
     l3="The three freight goods are hardcoded by UID in the cargo and storage code, so their names are fixed. A good with IsGasGiantMineable true joins the gas-giant deposit pool and becomes an exotic resource for every empire, with its bonus driven by ExoticBonusType, MaxBonus and ConsumptionMultiplier. The loader sets no bounds on any number here.",
     notation=dict(title="Copy this: an exotic good", body="""
<p>One block of <code>Goods/Goods.yaml</code>, complete. The three freight goods are the same shape with <code>IsGasGiantMineable: false</code> and <code>ExoticBonusType: None</code>.</p>
<pre class="code">Good:
  UID: Energon
  RefiningRatio: 0.5
  MaxRichness: 6
  NameIndex: 4943
  RefinedNameIndex: 4936
  DescriptionIndex: 4944
  Weight: 5
  IsGasGiantMineable: true
  ExoticBonusType: Production
  MaxBonus: 0.25
  ConsumptionMultiplier: 0.02</pre>
<ul>
<li>Only <code>Goods.yaml</code> is loaded. The XML files in the same folder predate this loader and nothing reads them.</li>
<li><b>UID</b> is the id and the icon name: the game loads <code>Textures/Goods/&lt;UID&gt;</code>, so a renamed good needs a renamed texture.</li>
<li>A mineable good needs an <code>ExoticBonusType</code> other than None, plus a <code>MaxBonus</code> and a <code>ConsumptionMultiplier</code>, or its deposits pay nothing. At least one good must be mineable or gas-giant mining throws on the first deposit.</li>
</ul>"""),
     groups=[
 G("Good fields", "What one good is, how often it appears and what its bonus pays.",
   "Only the six exotics are mined; the three freight goods are recognised by their exact UIDs.",
   "Weight and MaxRichness shape a deposit when the planet is created, while the bonus fields decide what the empire gets every turn after that.", [
   T("UID","string","The good's id, and the name of its icon.",
     "Cargo, storage and the trade code find a good by this string, and the icon loads from Textures/Goods/<UID>. The three freight goods are matched by the exact literals Food, Production and Colonists_1000 in code, so those three ids are fixed.",
     "`Mineable.CargoId` returns `ResourceType.UID`, and `ShipInfoUIElement` finds the good with `TransportableGoods.Find(g => g.UID == cargoId)` before reading its name and description. `Ship_Cargo` and `ColonyStorage` compare the literal strings `Food`, `Production` and `Colonists_1000`, which is why a renamed freight good stops being food or production and becomes an inert commodity. The icon path is `Goods/` plus the UID through `ResourceManager.Texture`, and a missing texture draws a placeholder rather than failing."),
   T("NameIndex","int","Localisation id of the good's display name.",
     "The name is not stored in the good: it is looked up by id in the language files, and the cargo tooltip and the mining panel both read it from there.",
     "`Mineable.TranslatedResourceName` returns `new LocalizedText(ResourceType.NameIndex)`, and `ShipInfoUIElement`'s cargo tooltip prints the same token. Vanilla uses 162 for Production, 161 for Food, 4949 for Colonists_1000 and 4939-4953 for the exotics. A missing id leaves the name unresolved, and the screen shows the number or a blank instead of a word."),
   T("RefinedNameIndex","int","Localisation id of the refined form's name.",
     "Only the exotics use it: the mining and bonus screens label the refined output with this id, which is a different string from the raw ore's name.",
     "`ExoticBonusesWindow` builds its row label from `new LocalizedText(bonus.Good.RefinedNameIndex)` and passes `DescriptionIndex` as the tooltip, and `MiningOpsDebug` prints the same id. Vanilla sets it on the six exotics only (4933-4938) and leaves the three freight goods without it. A good that is never refined should leave it out rather than point it at an unrelated string."),
   T("DescriptionIndex","int","Localisation id of the tooltip text.",
     "It supplies the sentence under the good's name in a cargo slot and in the exotic-bonus window, and the same text is what the codex lookup receives.",
     "`ShipInfoUIElement` shows `new LocalizedText(good.DescriptionIndex)` and hands it to `Codex.CodexHooks.Find`, while `ExoticBonusesWindow` uses it as the second half of its tooltip. Vanilla: Production 4950, Food 4951, Colonists_1000 4952, exotics 4940-4954. Two goods that share a description also share whatever codex hook that text resolves, so give each one its own id."),
   T("Weight","int","How often this good is chosen for a gas giant's deposit.",
     "It is a lottery weight rather than a percentage: the generator adds a good to its pool once per point of Weight and then picks one entry uniformly. Vanilla gives all six exotics 5, so they are equally likely.",
     "`Mineable.GetRandomResourceType` fills an array from `TransportableGoods.Filter(g => g.IsGasGiantMineable)`, adding each good `good.Weight` times, then takes `universe.Random.Item`. A weight of 10 against six goods at 5 is a 10-in-40 chance, and 0 removes the good from the pool. If every mineable good is 0 the array is empty and the constructor throws with a message naming Goods.yaml."),
   T("MaxRichness","byte","The ceiling of the die a deposit's richness is rolled on.",
     "Each mineable gas giant rolls a richness up to this value when the planet is created, and richness is the rate at which the mining op extracts raw resource. Vanilla 6 for every good.",
     "`Mineable`'s constructor sets `Richness = planet.Universe.Random.RollDie(ResourceType.MaxRichness)`, and the field is a byte, so 255 is the arithmetic ceiling. The roll happens once at planet creation, so a change reaches new galaxies and not deposits that already exist. `Richness` is described in the code as how much of the resource is extracted per turn, so a higher roll makes a faster mining op rather than a larger total."),
   T("RefiningRatio","float","How much refined resource one raw point becomes.",
     "It is the exchange rate at a mining station: each raw point processed yields this much refined stock, scaled by the empire's refining-efficiency research and capped at 1. Vanilla 1 for the freight goods and 0.5 for every exotic.",
     "`Mineable.RefineRatioFor` returns `(RefiningRatio * empire.data.RefiningRatioMultiplier).UpperBound(1)`, so the Refining Ratio Bonus tech can lift 0.5 to 1 and no further; `RefiningEfficiencyTests` pins three levels at 1.3. A ratio of 0 makes a station refine nothing, and the mining goal then produces no stock. The ratio changes the yield per raw point, not how fast the deposit is mined."),
   T("IsGasGiantMineable","bool","Whether the good can be mined at a gas giant.",
     "It does two jobs: it puts the good into the pool a deposit is chosen from, and it makes every empire create an exotic-bonus entry for it. False leaves the good as cargo or a fixed commodity only.",
     "`Mineable.GetRandomResourceType` filters on it, and both `Empire` constructors loop `TransportableGoods.Filter(g => g.IsGasGiantMineable)` to build `ExoticBonuses`. `GetNumExoticGoods` counts the same filter, and the mining constructor throws when the count is zero. Vanilla has six true and the three freight goods false, so mining ops need at least one exotic in the file."),
   T("ExoticBonusType","ExoticBonusType","Which empire stat the refined resource pays into.",
     "Each value names one stat, and the empire keeps one bonus entry per value, so two mineable goods cannot share a type. None is a mined good that pays nothing: legal, but the deposit is wasted.",
     "`Empire` fills `ExoticBonuses`, a `Map<ExoticBonusType, EmpireExoticBonuses>`, by calling `Add(good.ExoticBonusType, ...)` for each mineable good; `Map` is a `Dictionary`, so a duplicate key throws at empire creation instead of merging. The same value picks the consumption base in `EmpireExoticBonuses.UpdateStaticConsumption`: population for Credits, fleet surface area for DamageReduction, gross production for Production, warp thrust for WarpSpeed, and the ships' own recharge and repair for ShieldRecharge and RepairRate. Vanilla uses each of the six non-None values exactly once.",
     values=("enum:ExoticBonusType", EXOTIC_BONUS_TYPES)),
   T("MaxBonus","float","The ceiling of the bonus, as a fraction of the stat.",
     "The bonus rises with the refined stock and per-turn output the empire holds against its consumption, and stops here. 0.5 multiplies the stat by 1.5 at full supply, and 1 doubles it.",
     "`EmpireExoticBonuses.DynamicBonus` returns `((RefinedPerTurnForConsumption + CurrentStorage) / Consumption * MaxBonus).UpperBound(MaxBonus)`, and `CurrentBonusMultiplier` adds 1 to it. When `Consumption` is 0 the full MaxBonus applies as soon as any stock exists, which makes a zero-consumption good an unconditional buff. Vanilla runs from 0.25 (Energon, production) to 1.0 (NanoGas repair and Aetherium warp)."),
   T("ConsumptionMultiplier","float","Scales how much of the boosted stat an empire pays for the bonus.",
     "Consumption is the stat's own size times this value, so the same number means different amounts for a bonus on credits than for one on repair. That is what keeps a bonus proportional as an empire grows.",
     "`UpdateStaticConsumption` computes a base from the bonus type and then `Consumption = consumption * Good.ConsumptionMultiplier`, which `NeedMoreOps` and `RefiningNeeded` compare against the refining output. Vanilla spans 0.0001 (Aetherium, warp) to 0.12 (Luxarium, credits), which is why one exotic needs a single station and another needs several. 0 makes consumption zero, and `DynamicBonus` then pays the full MaxBonus from the first refined unit."),
 ]),
 G("The list", "How the file is laid out.", "One Good block per resource, in any order.",
   "Lookups are by UID, so order is not a priority; a duplicate UID or bonus type is a real error.", [
   T("Good","element","One good block in the list.",
     "The YAML key repeats once per good, and each block deserializes into one Good. Order is not a priority: lookups are by UID or by bonus type.",
     "Vanilla ships nine blocks: Production, Food, Colonists_1000, Pulsefield, Luxarium, Fortifume, Energon, NanoGas and Aetherium. A repeated UID leaves two entries, and `TransportableGoods.Find` returns the first, so the later one is unreachable through the cargo code. Two mineable goods with the same ExoticBonusType are worse: the empire's bonus map throws when it is built."),
 ]),
 ]),

dict(id="races", tier=2, title="Races", paths=["Races"], ext=".xml", roots=["EmpireData"],
     fmt="XML", loader="ResourceManager.LoadEmpires → EmpireData + RacialTrait",
     override="XML unifies by file name. Name inside Traits is the race id used by saves and dialogs.",
     l1="A playable people: its name, look, personality and the ships it starts with.",
     l2="The file is two things at once: the saved empire template (EmpireData) and its racial traits (RacialTrait). Most of its lines are design UIDs the AI uses for each job.",
     l3="Every Default*/Pirate*/Remnant* value is a ship-design name, not a path. A missing design logs and falls back, often to a vanilla name. Trait options are chosen from RacialTraits.xml at game start.",
     groups=[
 G("Identity", "Who the race is.", "These names appear throughout the UI and the save.", "The traits name is the race UID; the portrait drives the flag and colour.", [
   T("Traits","element","Container for the racial trait block.","", ""),
   T("Name","string","Race name and UID.","", ""),
   T("Singular","string","One member of the race.","", ""),
   T("Plural","string","Many members.","", ""),
   T("Adj1","string","Adjective.","", ""),
   T("Adj2","string","Second adjective.","", ""),
   T("HomeworldName","string","Starting homeworld name.","", ""),
   T("HomeSystemName","string","Starting system name.","", ""),
   T("PortraitName","string","Portrait and flag identity.","Portraits/<name>.", ""),
   T("FlagIndex","int","Flag sprite index.","", ""),
   T("R/G/B","float","Empire colour.","0-255 per channel.", ""),
   T("ShipType","string","Hull style family.","Matches hull Style.", ""),
   T("VideoPath","string","Intro video.","", ""),
   T("MusicCue","string","Diplomacy music.","", ""),
   T("DiplomacyDialogPath","string","Dialog folder.","DiplomacyDialogs/<language>/.", ""),
 ]),
 G("Starting ships and defaults", "The design the AI builds for each job.", "All values are design names; the AI falls back when one is missing.", "Changing these changes what the empire starts with and what its governors build.", [
   T("StartingShip","string","First warship.","", ""),
   T("StartingScout","string","Scout design.","", ""),
   T("PrototypeShip","string","Prototype design.","", ""),
   T("DefaultColonyShip","string","Colony ship.","", ""),
   T("DefaultSmallTransport","string","Freighter.","", ""),
   T("DefaultTroopShip","string","Troop transport.","", ""),
   T("DefaultConstructor","string","Constructor.","", ""),
   T("DefaultMiningShip","string","Mining ship.","", ""),
   T("DefaultResearchStation","string","Research station.","", ""),
   T("DefaultMiningStation","string","Mining station.","", ""),
   T("DefaultSalvageShip","string","Salvage ship.","", ""),
   T("DefaultAssaultShuttle","string","Boarding shuttle.","", ""),
   T("DefaultSupplyShuttle","string","Supply shuttle.","", ""),
 ]),
 G("Pirates and remnants", "The designs those factions use.", "Only read for pirate or remnant factions.", "A missing entry falls back to a default design name.", [
   T("IsPirateFaction","bool","Marks a pirate faction.","", ""),
   T("IsRemnantFaction","bool","Marks a remnant faction.","", ""),
   T("PirateBaseBasic","string","Pirate base design.","", ""),
   T("PirateFighterBasic","string","Pirate fighter design.","", ""),
   T("PirateFrigateBasic","string","Pirate frigate design.","", ""),
   T("PirateSlaverBasic","string","Pirate slaver design.","", ""),
   T("PirateStationBasic","string","Pirate station design.","", ""),
   T("RemnantFighter","string","Remnant fighter.","", ""),
   T("RemnantCruiser","string","Remnant cruiser.","", ""),
   T("RemnantBattleship","string","Remnant battleship.","", ""),
   T("RemnantBehemoth","string","Remnant behemoth.","", ""),
   T("PirateBaseImproved","string","Improved pirate base.","", ""),
   T("PirateBaseAdvanced","string","Advanced pirate base.","", ""),
   T("PirateFighterImproved","string","Improved pirate fighter.","", ""),
   T("PirateFighterAdvanced","string","Advanced pirate fighter.","", ""),
   T("PirateFrigateImproved","string","Improved pirate frigate.","", ""),
   T("PirateFrigateAdvanced","string","Advanced pirate frigate.","", ""),
   T("PirateSlaverAdvanced","string","Advanced pirate slaver.","", ""),
   T("PirateSlaverImproved","string","Improved pirate slaver.","", ""),
   T("PirateStationImproved","string","Improved pirate station.","", ""),
   T("PirateStationAdvanced","string","Advanced pirate station.","", ""),
   T("PirateFlagShip","string","Pirate flagship.","", ""),
   T("PiratePaymentPeriodTurns","int","Turns between pirate demands.","", ""),
   T("MinimumColoniesForStartPayment","int","Colonies required before tribute starts.","", ""),
   T("RemnantAssimilator","string","Remnant assimilator.","", ""),
   T("RemnantBattleCorvette","string","Remnant battle corvette.","", ""),
   T("RemnantBeamCorvette","string","Remnant beam corvette.","", ""),
   T("RemnantBomber","string","Remnant bomber.","", ""),
   T("RemnantBomberLight","string","Remnant light bomber.","", ""),
   T("RemnantBomberMedium","string","Remnant medium bomber.","", ""),
   T("RemnantCarrier","string","Remnant carrier.","", ""),
   T("RemnantCorvette","string","Remnant corvette.","", ""),
   T("RemnantExterminator","string","Remnant exterminator.","", ""),
   T("RemnantFrigate","string","Remnant frigate.","", ""),
   T("RemnantInhibitor","string","Remnant inhibitor.","", ""),
   T("RemnantMotherShip","string","Remnant mothership.","", ""),
   T("RemnantPortal","string","Remnant portal.","", ""),
   T("RemnantSupportSmall","string","Remnant small support ship.","", ""),
   T("RemnantTorpedoCruiser","string","Remnant torpedo cruiser.","", ""),
 ]),
 G("Traits and personality", "What the people are like.", "Weights choose a personality; the trait set chooses starting bonuses.", "TraitSet names a set in RacialTraits.xml; TraitOptions are the options offered.", [
   T("TraitSet","string","Starting trait set.","", ""),
   T("TraitSets","element","Available trait sets.","", ""),
   T("TraitOptions","string[]","Trait options in the set.","", ""),
   T("PersonalityTraitsWeights","string[]","Personality weighting.","", ""),
   T("EconomicTraitsWeights","string[]","Economic weighting.","", ""),
   T("PreferredEnv","enum","Preferred planet category.",
     "Picks the homeworld category and the climate the other Env weights are measured against.",
     "", values=("enum:PlanetCategory", PREFERRED_ENV)),
   T("EnvTerran","float","Terran habitability multiplier.","", "1"),
   T("EnvOceanic","float","Oceanic multiplier.","", ""),
   T("EnvSteppe","float","Steppe multiplier.","", ""),
   T("EnvTundra","float","Tundra multiplier.","", ""),
   T("EnvSwamp","float","Swamp multiplier.","", ""),
   T("EnvDesert","float","Desert multiplier.","", ""),
   T("EnvIce","float","Ice multiplier.","", ""),
   T("EnvBarren","float","Barren multiplier.","", ""),
   T("EnvVolcanic","float","Volcanic multiplier.","", ""),
   T("BaseShipLevel","int","Starting ship experience level.","", ""),
   T("MinimumTroopLevel","int","Minimum troop level produced.","", ""),
   T("Cost","float","This item has no function in game.","", ""),
   T("Faction","byte","Faction index.","", ""),
   T("HullColors","map","Which hull parts take empire colour.","", ""),
   T("SpacePortModel","string","Model used for the race's spaceport.","", ""),
   T("TechTree","string","Starting tech tree id.","", ""),
   T("WarpStart","string","Warp-in effect override.","", ""),
   T("WarpEnd","string","Warp-out effect override.","", ""),
   T("ThrustColor0R","byte","Primary thrust colour, red.","0-255.", ""),
   T("ThrustColor0G","byte","Primary thrust colour, green.","", ""),
   T("ThrustColor0B","byte","Primary thrust colour, blue.","", ""),
   T("ThrustColor1R","byte","Secondary thrust colour, red.","", ""),
   T("ThrustColor1G","byte","Secondary thrust colour, green.","", ""),
   T("ThrustColor1B","byte","Secondary thrust colour, blue.","", ""),
   T("TroopNameIndex","int","Localised troop name.","", ""),
   T("TroopDescriptionIndex","int","Localised troop description.","", ""),
   T("RebelSing","string","Rebel faction name, singular.","", ""),
   T("RebelPlur","string","Rebel faction name, plural.","", ""),
   T("RebelName","string","Rebel faction adjective.","", ""),
 ]),
 ]),

dict(id="racialtraits", tier=2, title="Racial traits", paths=["RacialTraits"], ext=".xml", roots=["RacialTraits", "TraitList", "RacialTraitOption", "RacialTrait"],
     fmt="XML", loader="ResourceManager.RaceTraits → TryDeserialize → RacialTraitOption",
     override="One file. TraitName is the id a race file's TraitOptions list uses.",
     l1="The menu of racial bonuses: what each trait costs, what it forbids, and what it changes.",
     l2="A trait is a bundle of modifiers. The race file picks a set; the traits in it are added together into the empire's starting stats.",
     l3="Excludes names a trait that cannot be taken with this one. Category groups the UI; Cost is in trait points.",
     groups=[
 G("Trait definition", "What the trait is and what it costs.", "Cost is paid from the game-start trait point pool.", "Excludes is a name, not an index.", [
   T("TraitName","string","Trait id.","", ""),
   T("TraitIndex","int","Localisation id.","", ""),
   T("Description","int","Localisation id for the tooltip.","", ""),
   T("Category","string","UI group.","", ""),
   T("Cost","int","Trait point cost.","", ""),
   T("Excludes","string","Trait that cannot be combined with this one.","", ""),
 ]),
 G("Growth", "How fast a colony grows and what it eats.", "The six fields are separate: two set growth bounds, one scales the result, one sets the food charge, and two shape the homeworld.", "Population is held in thousandths of a billion, so 0.005 is 5 million people per turn.", [
   T("ConsumptionModifier","float","Food or production eaten per colonist.","", ""),
   T("PopGrowthMin","float","Minimum population growth.","", ""),
   T("PopGrowthMax","float","Maximum population growth.","", ""),
   T("ReproductionMod","float","Population growth multiplier.","", ""),
   T("HomeworldFertMod","float","Homeworld fertility.","", ""),
   T("HomeworldRichMod","float","Homeworld richness.","", ""),
 ]),
 G("Economy", "What the trait adds to income, research and upkeep.", "These are additive fractions: 0.1 means +10% and -0.1 means -10%.", "They apply to every colony or ship the empire owns.", [
   T("ResearchMod","float","Research output.","", ""),
   T("ProductionMod","float","Production output.","", ""),
   T("TaxMod","float","Tax income.","", ""),
   T("MaintMod","float","Maintenance.","Negative is cheaper.", ""),
   T("ShipCostMod","float","Ship cost.","", ""),
   T("Mercantile","float","Trade income modifier.","", ""),
   T("CreditsPerKilledSlot","float","Credits per enemy slot destroyed.","", ""),
   T("PenaltyPerKilledSlot","float","Penalty per friendly slot lost.","", ""),
   T("Spiritual","float","Artifact bonus multiplier.","", ""),
   T("ResearchBenefitFromAlliance","float","Extra research from allies.","", ""),
 ]),
 G("Combat and ships", "What the trait changes in a fight.", "Most are additive fractions; a modifier of 0.1 adds ten percent to the stat named in the field.", "Passenger fields change how many troops a ship can carry.", [
   T("ModHpModifier","float","Module hit points.","", ""),
   T("GroundCombatModifier","float","Ground combat.","", ""),
   T("DodgeMod","float","Dodge chance.","", ""),
   T("TargetingModifier","float","Weapon accuracy.","", ""),
   T("RepairMod","float","Repair rate.","", ""),
   T("PassengerBonus","float","Passenger capacity.","", ""),
 ]),
 G("Start and exploration", "What the empire begins with.", "These are read once, when the empire is created.", "The explore and construction fields are multipliers around a default of 1.", [
   T("DiplomacyMod","float","Starting relations and trade value.","", ""),
   T("SpyMultiplier","float","Espionage strength.","", ""),
   T("ExtraStartingScouts","int","Extra scouts at start.","", ""),
   T("BonusExplored","int","Extra explored systems at start.","", ""),
   T("ExploreDistanceMultiplier","float","How far scouts range.","", ""),
   T("ConstructionRateMultiplier","float","Constructor build rate.","", ""),
   T("BuilderShipConstructionMultiplier","float","Builder ship construction rate.","", ""),
   T("Prototype","int","Starts with a prototype ship.","", ""),
 ]),
 G("Environment", "How the race relates to planet types.", "A multiplier of 1 is neutral; 1.2 makes that climate more productive and 0.8 less.", "PreferredEnv picks the homeworld category and the neutral point for the others.", [
   T("HomeworldSizeMod","float","Homeworld size.","", ""),
   T("PreferredEnv","enum","Preferred planet category.",
     "Picks the homeworld category and the climate the other Env multipliers are measured against.",
     "", values=("enum:PlanetCategory", PREFERRED_ENV)),
   T("EnvTerranMultiplier","float","Terran habitability multiplier as spelled in the file.","The runtime field is EnvTerran.", ""),
   T("EnvOceanicMultiplier","float","Oceanic multiplier as spelled in the file.","Runtime field EnvOceanic.", ""),
   T("EnvSteppeMultiplier","float","Steppe multiplier as spelled in the file.","Runtime field EnvSteppe.", ""),
   T("EnvTundraMultiplier","float","Tundra multiplier as spelled in the file.","Runtime field EnvTundra.", ""),
   T("EnvSwampMultiplier","float","Swamp multiplier as spelled in the file.","Runtime field EnvSwamp.", ""),
   T("EnvDesertMultiplier","float","Desert multiplier as spelled in the file.","Runtime field EnvDesert.", ""),
   T("EnvIceMultiplier","float","Ice multiplier as spelled in the file.","Runtime field EnvIce.", ""),
   T("EnvBarrenMultiplier","float","Barren multiplier as spelled in the file.","Runtime field EnvBarren.", ""),
   T("EnvVolcanicMultiplier","float","Volcanic multiplier as spelled in the file.","Runtime field EnvVolcanic.", ""),
 ]),
 G("Flags", "Switches that change how the race plays.", "Each is a whole number; 1 turns the flag on and 0 leaves it off.", "They are summed across the selected traits before the empire is built.", [
   T("Cybernetic","int","Cybernetic race flag.","", ""),
   T("Militaristic","int","Militaristic flag.","", ""),
   T("Aquatic","int","Aquatic flag.","", ""),
   T("Pack","int","Pack flag.","", ""),
 ]),
 G("No function", "Fields that change nothing.", "", "", [
   T("Blind","int","This item has no function in game.","", ""),
   T("Prewarp","int","This item has no function in game.","", ""),
   T("ShipMaintMultiplier","float","This item has no function in game.","", ""),
   T("SpyModifier","float","This item has no function in game.","", ""),
   T("InBordersSpeedBonus","float","This item has no function in game.","", ""),
   T("PassengerModifier","float","This item has no function in game.","", ""),
 ]),
 G("Definition", "The entry itself.", "It is one option in the trait menu.", "The container is TraitList.", [
   T("RacialTraitOption","element","One option in the trait menu.","The container is TraitList.", ""),
 ]),
 ]),

dict(id="diplomacy", tier=2, title="Diplomatic traits", paths=["Diplomacy"], ext=".xml", roots=["DiplomaticTraits", "DTrait", "ETrait"],
     fmt="XML", loader="ResourceManager.DiplomaticTraits → TryDeserialize → DiplomaticTraits",
     shape=("<p>Two lists under one root: <code>&lt;DiplomaticTraitsList&gt;</code> holds the "
            "<code>&lt;DTrait&gt;</code> entries and <code>&lt;EconomicTraitsList&gt;</code> holds the "
            "<code>&lt;ETrait&gt;</code> entries. An empire takes one from each list, and the two lists are read "
            "by different code &mdash; only the DTrait fields are diplomacy.</p>"),
     override=("Races name entries in PersonalityTraitsWeights / EconomicTraitsWeights; an id that is not in "
               "this file logs a warning and the empire gets a random entry. Rebels draw at random too."),
     l1="The personalities an empire can be given: one diplomatic (DTrait) and one economic (ETrait).",
     l2=("Diplomatic values are thresholds on a relationship's trust and the anger it tolerates; economic "
         "values pick a research strategy and add AI ship goals."),
     l3=("A race's weights choose the entries, and the player gets neither: the player's diplomatic trait is "
         "the blank None entry, so the code that needs a player's territorialism averages all six DTrait "
         "entries, and the economic trait is Generalists."),
     groups=[
 G("Diplomatic personality (DTrait)", "Thresholds and anger for one empire's diplomacy.",
   "Six entries in vanilla: Xenophobic, Honorable, Cunning, Aggressive, Ruthless, Pacifist.",
   "The numbers are read when a treaty is offered, when trust is updated and when anger is recalculated.", [
   T("Name","string","The personality id, parsed into the PersonalityType enum.",
     "Read through TraitName, which runs Enum.TryParse each time; a name that does not parse becomes None and no warning is logged.",
     "PersonalityType decides which diplomacy planner runs, which spy missions are considered and how war goals are picked, and Empire exposes IsCunning through IsPacifist for the rest of the code. The vanilla ids match the enum names exactly, case included."),
   T("Description","string","Flavour text for the entry.",
     "DTrait declares the field and the loader fills it, but nothing in the game reads it: no screen shows it and diplomacy dialogs print lines from the DiplomacyDialog files.",
     "Editing it changes no behaviour, which also makes it useless as a place to record what the numbers do."),
   T("Territorialism","int","Border tolerance: the anger at which foreign ships become an attack.",
     "Total anger above it makes open war acceptable, and a trader's border violation attacks once border anger plus 10 passes it. Opening borders needs AvailableTrust at or above it, and border anger over 75% of it cancels the offer. Vanilla runs 30 to 50.",
     "A peace treaty writes off a third of the value from the border and territorial anger pools. It enters the ratios inverted: 1 - T/100 in the war offensive ratio and T/100 in the expansion ratio, so one value pushes an empire toward expansion and away from invasion at the same time."),
   T("Opportunism","float","Appetite for a weak neighbour, added to the expansion and war ratios.",
     "Added unnormalised in GetExpansionRatio (0.2 adds 0.2, the same scale as territorialism/100) and averaged in GetWarOffensiveRatio. Vanilla runs 0.2 to 0.75.",
     "Values above 1 skew expansion further than vanilla ever does, and 0 removes weakness from both ratios. Nothing else reads it."),
   T("NAPact","int","Trust needed before the AI offers a non-aggression pact.",
     "The offer is skipped while AvailableTrust is at or below the value, so 0 offers as soon as the other gates pass and 13 waits for real trust. Vanilla runs 0 to 13.",
     "In an incoming offer the value is added to the trust the AI needs before saying yes, and open borders charge NAPact + 7.5. The NAP part is waived when the empire is already at war with someone else or sees a threat of 20 or more."),
   T("Alliance","int","Trust needed before the AI accepts an alliance.",
     "It rejects while AvailableTrust is below Alliance + TotalAnger, so an angry empire needs more than the file's number. Vanilla runs 15 to 50.",
     "This is only the trust gate: turns known, the player side's turns of open borders and the TurnsAbove95 threshold are checked separately, and an empire that fails those never reaches the comparison."),
   T("Trade","int","Trust needed before the AI offers a trade treaty.",
     "A trade treaty comes after a non-aggression pact: the offer is skipped without one and while AvailableTrust is at or below the value. Vanilla runs 2 to 15.",
     "In an incoming offer Trade is added to the trust the AI needs, and against a player an empire also stays silent while its total anger minus trust is above 50."),
   T("Trustworthiness","int","Anger tolerated before declaring war, and a weight in the spy budget.",
     "The war check compares the other side's anger with Trustworthiness x its peacefulness (1 - military ratio). Vanilla runs 25 (Cunning) to 80 (Honorable).",
     "The spy budget adds Trustworthiness x 0.01 to the treasury an empire sets aside, so a low value spends the difference on ships instead. IsTrusting (>= 80) and Careless (<= 60) are defined on the class and read by nothing, so they are not thresholds in play."),
   T("AngerDissipation","float","Anger points removed from every pool each turn.",
     "Each of the four pools (diplomatic conflict, ships in borders, military conflict, territorial conflict) loses the value per turn, doubled while a peace treaty holds; total anger is capped at 100. Vanilla runs 0.05 to 0.2.",
     "At 0.05 a full pool takes about 2,000 turns to empty and at 0.2 about 500. Peace also removes 0.1 from each pool per turn on top of this until the treaty runs out."),
   T("WeaknessDecline","float","Written by vanilla, parsed, and read by no code.",
     "DTrait declares the field and the loader fills it, but nothing in the checkout reads it.",
     "No code outside the declaration reads it, so a file may set the key but changing it cannot change the game."),
   T("PowerIncrease","float","Declared on DTrait, parsed, and never read.",
     "The names suggest a relation drift for rising and falling powers, but the drift is computed in Relationship.UpdateThreat from military strength instead.",
     "No code outside the declaration reads it, so a file may set the key but changing it cannot change the game."),
   T("TrustGainedAtPeace","float","Declared on DTrait, parsed, and never read.",
     "Trust moves through ImproveRelations and the trust entries, not through this value.",
     "No code outside the declaration reads it, so a file may set the key but changing it cannot change the game."),
   T("SalvageStationTrustLoss","float","Trust each system owner loses when a player builds a salvage platform there.",
     "Default 5 when the element is absent, which every vanilla entry relies on. The loss is multiplied by the owner's difficulty modifier before it is applied.",
     "Owners that are the player, factions, at war, allied or holding open borders with the salvager are skipped. It is the only field here that moves trust directly instead of setting a threshold."),
   T("NaturalRelChange","float","A vanilla key with no field on DTrait.",
     "Honorable writes <NaturalRelChange>0</NaturalRelChange>, and DTrait has no field of that name, so the value is discarded silently.",
     "This item has no function in game."),
 ]),
 G("Economic personality (ETrait)", "The research strategy and the AI goal bump.",
   "Five entries in vanilla: Generalists, Industrialists, Technologists, Militarists, Expansionists.",
   "Chosen from the same file and read by the economy and research code, not by diplomacy.", [
   T("Name","string","The economic personality id, and the key its strategy is looked up under.",
     "EmpireResearch calls GetEconomicStrategy(Name), and EconomicResearchStrategies.yaml has one entry per vanilla name, so the spelling is the identity.",
     "The same id is what race weights and the diplomacy screen display. The player has no economic trait and is given Generalists when one is needed."),
   T("Description","string","Flavour text for the entry, read by nothing.",
     "The loader fills it and no screen prints it; a unit test asserts the player's entry has none, which is the only place the field is touched.",
     "No behaviour depends on it."),
   T("EconomicResearchStrategy","string","Maps to the enum used when trust accrues.",
     "EconomicPersonality() switches on this string and falls back to Generalists for anything it does not recognise; vanilla writes Balanced in all five entries, so every empire is Generalists here.",
     "The strategy object an empire researches with comes from Name, not this field, so editing it moves trust handling and leaves the research plan alone."),
   T("ColonyGoalsPlus","int","Expansionists set 1 here; nothing reads it.",
     "ETrait declares the field and the loader fills it, but no code in the checkout reads ColonyGoalsPlus: colony targets come from the strategy and the difficulty.",
     "No code outside the declaration reads it, so a file may set the key but changing it cannot change the game."),
   T("ShipGoalsPlus","int","Extra ship goals the AI gets when it is built.",
     "Added once to EmpireAI.NumberOfShipGoals during construction, so Militarists (6) run six more concurrent goals than an empire without the value.",
     "It is read once, at empire creation, and nothing revisits it later, so a change shows only in a new game."),
 ]),
 ]),

dict(id="solarsystems", tier=2, title="Solar systems", paths=["SolarSystems"], ext=".xml", roots=["SolarSystemData"],
     fmt="XML", loader="ResourceManager.LoadSolarSystemData / LoadRandomSolarSystems → SolarSystemData",
     override="Careful: the systems directory can be all-or-nothing. If a mod supplies any file there, vanilla's set is ignored.",
     l1="A hand-placed star system: its sun, planets, moons and resources.",
     l2="These are the fixed systems a mod can add; the rest of the galaxy is generated. Ring order is orbital order.",
     l3="WhichPlanet is an index into PlanetTypes.yaml, not a name. HomePlanet marks an empire start. planetScale is a multiplier on the type's size.",
     groups=[
 G("System", "The star and its rings.", "Rings are planets or asteroid belts in orbital order.", "SunPath names a Suns.yaml Id.", [
   T("Name","string","System name.","", ""),
   T("SunPath","string","Sun type id.","", "star_yellow"),
   T("RingList","element","Container for rings.","", ""),
   T("Ring","element","One orbit.","", ""),
 ]),
 G("Planet in a ring", "One planet or belt.", "WhichPlanet indexes PlanetTypes; WhichMoon indexes its moon list.", "Asteroids is a string flag in the file, not a bool.", [
   T("Planet","string","Planet name.","", ""),
   T("WhichPlanet","int","Planet type index.","", ""),
   T("Asteroids","string","Asteroid belt flag.","", ""),
   T("HasRings","string","Planet has rings.","", ""),
   T("HomePlanet","bool","Is an empire homeworld.","", ""),
   T("planetScale","float","Size multiplier.","", ""),
   T("Station","string","Space station present.","", ""),
   T("SpecialDescription","string","Flavour text.","", ""),
   T("Population","int","Starting population.","", ""),
   T("ResourceList","element","Resources on the planet.","", ""),
   T("Resource","element","One resource entry.","", ""),
   T("Moons","element","Moon container.","", ""),
   T("Moon","element","One moon.","", ""),
   T("WhichMoon","int","Moon type index.","", ""),
   T("MoonScale","float","Moon size multiplier.","", ""),
 ]),
 ]),

dict(id="events", tier=2, title="Exploration events", paths=["Exploration Events"], ext=".xml", roots=["ExplorationEvent"],
     fmt="XML", loader="ResourceManager.LoadExpEvents → EventsDict",
     override="XML unifies by file name; Name is the event UID.",
     l1="Something that happens when a ship explores: a find, a trap, a fight or a story beat.",
     l2="An event has a trigger, a set of possible outcomes, and text. Chance weights the outcomes; the rest are effects.",
     l3="Image and ConfirmText drive the popup. UnlockTech and SecretTechDiscovered grant research; Spawn* place ships. RemoveTrigger and ReplaceWith edit the event pool for later.",
     groups=[
 G("Trigger and text", "When it fires and what it says.", "Chance is relative weight within the outcome list.", "Image is a texture path; the three text fields are plain strings.", [
   T("Name","string","Event UID.","", ""),
   T("Chance","float","Outcome weight.","", ""),
   T("Image","string","Popup image.","", ""),
   T("TitleText","string","Popup title.","", ""),
   T("DescriptionText","string","Body text.","", ""),
   T("ConfirmText","string","Button text.","", ""),
   T("Story","string","Story id.","", ""),
   T("StoryStep","int","Step within the story.","", ""),
   T("AllRemnantStories","bool","Available to all remnant stories.","", ""),
 ]),
 G("Outcomes", "What the event does.", "Each PotentialOutcomes entry is one possible result.", "Effects are applied to the exploring ship, its empire or the planet.", [
   T("PotentialOutcomes","element","Outcome container.","", ""),
   T("Outcome","element","One outcome.","", ""),
   T("MoneyGranted","float","Credits awarded.","", ""),
   T("ChangeRichness","float","Mineral richness change.","", ""),
   T("ChangeBaseFertility","float","Fertility change.","", ""),
   T("ChangeBaseMaxFertility","float","Maximum fertility change.","", ""),
   T("NumTilesToMakeHabitable","int","Tiles made habitable.","", ""),
   T("NumTilesToMakeUnhabitable","int","Tiles made uninhabitable.","", ""),
   T("GrantArtifact","string","Artifact granted.","", ""),
   T("UnlockTech","string","Tech unlocked.","", ""),
   T("SecretTechDiscovered","string","Secret tech revealed.","", ""),
   T("ScienceBonus","float","Research awarded.","", ""),
   T("SpawnBuildingOnPlanet","string","Building placed.","", ""),
   T("SpawnFleetInOrbitOfPlanet","string","Fleet spawned.","", ""),
   T("FriendlyShipsToSpawn","string","Friendly ships spawned.","", ""),
   T("PirateShipsToSpawn","string","Pirate ships spawned.","", ""),
   T("RemnantShipsToSpawn","string","Remnant ships spawned.","", ""),
   T("TroopsToSpawn","string","Troops spawned.","", ""),
   T("SelectRandomPlanet","bool","Apply to a random planet.","", ""),
   T("ReplaceWith","string","Replace this event with another.","", ""),
   T("RemoveTrigger","string","Remove a trigger.","", ""),
   T("TriggerWhenOnlyRemnantsLeft","bool","Fire only when remnants remain.","", ""),
 ]),
 ]),

dict(id="encounters", tier=2, title="Encounter dialogs", paths=["Encounter Dialogs"], ext=".xml", roots=["Encounter"],
     fmt="XML", loader="ResourceManager.LoadDialogs → Encounters",
     override="XML unifies by file name. Faction + Step chooses which encounter is shown.",
     l1="A conversation with a faction that demands money, declares war, or moves a contact story forward.",
     l2="Encounters are looked up by faction and contact step, not by file name. Two files with the same faction and step mean the first loaded wins.",
     l3="PercentMoneyDemanded is a share of the victim's income. SetWar/EndWar and Set*ContactStep change relations and story state.",
     groups=[
 G("Selection", "Who is talking and when.", "Step must match the relation's contact step.", "FactionInitiated and PlayerInitiated decide which side can start it.", [
   T("Encounter","root","Encounter root.","", ""),
   T("Name","string","Encounter id.","", ""),
   T("Faction","string","Race/faction this belongs to.","", ""),
   T("Step","int","Contact step.","", ""),
   T("FactionInitiated","bool","The faction can start it.","", ""),
   T("PlayerInitiated","bool","The player can start it.","", ""),
   T("FirstContact","bool","First-contact encounter.","", ""),
   T("DescriptionText","string","Opening text.","", ""),
 ]),
 G("Messages and responses", "What is said and what the player can choose.", "MessageList holds the lines; ResponseOptions hold the buttons.", "Each response points at an index in the outcome set.", [
   T("MessageList","element","Message container.","", ""),
   T("Message","element","One line.","", ""),
   T("Text","string","Line text.","", ""),
   T("ResponseOptions","element","Response container.","", ""),
   T("Response","element","One response.","", ""),
   T("Index","int","Outcome index.","", ""),
   T("FailIndex","int","Failure outcome.","", ""),
   T("SuccessIndex","int","Success outcome.","", ""),
   T("LocalizedText","int","Localisation id instead of text.","", ""),
   T("DefaultIndex","int","Outcome used when no response matches.","", ""),
   T("EndTransmission","bool","Closes the encounter window.","", ""),
 ]),
 G("Effects", "What the encounter changes.", "Applied when the chosen response resolves.", "Money demands are percentages of income, not flat sums.", [
   T("PercentMoneyDemanded","float","Share of income demanded.","", ""),
   T("MoneyToThem","float","Flat credits paid.","", ""),
   T("SetWar","bool","Declares war.","", ""),
   T("EndWar","bool","Ends war.","", ""),
   T("SetFactionContactStep","int","New faction contact step.","", ""),
   T("SetPlayerContactStep","int","New player contact step.","", ""),
   T("SetEncounterStep","int","New encounter step.","", ""),
   T("RequiredTech","string","Tech required to see it.","", ""),
   T("FailIfNotAlluring","bool","Fails without the Alluring trait.","", ""),
 ]),
 ]),

dict(id="diplomacydialogs", tier=2, title="Diplomacy dialog pools", paths=["DiplomacyDialogs"], ext=".xml", roots=["DiplomacyDialog", "Dialogs"],
     fmt="XML per language", loader="ResourceManager.LoadDialogs → DiplomacyDialog",
     override="One folder per language under DiplomacyDialogs/. Mods merge by file name.",
     l1="The lines an empire speaks in diplomacy, grouped by personality and mood.",
     l2="These are flavour: the same treaty is proposed with different words depending on the speaker's personality and relationship.",
     l3="DL_* keys are personality pools; Friendly/Neutral/Hostile are relationship pools. DialogType selects the occasion.",
     groups=[
 G("Dialog structure", "The pools a line is chosen from.", "A missing pool falls back to Default.", "The game picks a line by personality, relation and occasion.", [
   T("DialogType","string","Occasion, e.g. treaty proposal.","", ""),
   T("DialogOption","element","One option entry.","", ""),
   T("StatementSet","element","One personality/mood pool.","", ""),
   T("StatementSets","element","Pool container.","", ""),
   T("Friendly","element","Friendly lines.","", ""),
   T("Neutral","element","Neutral lines.","", ""),
   T("Hostile","element","Hostile lines.","", ""),
   T("Default","element","Fallback lines.","", ""),
   T("DL_Agg/DL_Cunn/DL_Hon/DL_Pac/DL_Ruth/DL_Xeno","element","Personality pools (aggressive, cunning, honourable, pacifist, ruthless, xenophobic).","", ""),
   T("misc1/misc2/words","element","Supporting text pools.","", ""),
   T("DL_Exp","element","Explorer personality pool.","", ""),
   T("DL_Gen","element","General personality pool.","", ""),
   T("DL_Ind","element","Industrial personality pool.","", ""),
   T("DL_Mil","element","Militarist personality pool.","", ""),
   T("DL_Tech","element","Technologist personality pool.","", ""),
   T("DialogLine","element","One spoken line.","", ""),
   T("DialogOptions","element","Response container.","", ""),
   T("Name","string","Dialog set id.","", ""),
   T("Response","element","One reply.","", ""),
   T("SpecialInquiry","element","Special question entry.","", ""),
 ]),
 ]),

dict(id="artifacts", tier=2, title="Artifacts", paths=["Artifacts"], ext=".xml", roots=["ArrayOfArtifact", "Artifact"],
     fmt="XML", loader="ResourceManager.LoadArtifacts",
     override="One file. Name is the artifact id used by events and saves.",
     l1="A collectible relic that gives the empire holding it a permanent bonus.",
     l2="Artifacts are found by exploration and then sit in the empire's collection. Most bonuses are percentages; money is flat.",
     l3="The Spiritual trait multiplies every artifact bonus. Bonuses are additive across artifacts.",
     notation=dict(title="Copy this: an artifact entry", body="""
<p>All artifacts live in one array. This is the first entry of <code>Artifacts/MainArtifacts.xml</code>, complete:</p>
<pre class="code">&lt;Artifact&gt;
  &lt;Discovered&gt;false&lt;/Discovered&gt;
  &lt;Name&gt;Birth Crystal&lt;/Name&gt;
  &lt;Description&gt;A shard that induces good health and long life.&lt;/Description&gt;
  &lt;NameIndex&gt;800&lt;/NameIndex&gt;
  &lt;DescriptionIndex&gt;801&lt;/DescriptionIndex&gt;
  &lt;ReproductionMod&gt;0.5&lt;/ReproductionMod&gt;
  &lt;FertilityMod&gt;0&lt;/FertilityMod&gt;
  &lt;ProductionMod&gt;0&lt;/ProductionMod&gt;
  &lt;ResearchMod&gt;0&lt;/ResearchMod&gt;
  &lt;PlusFlatMoney&gt;0&lt;/PlusFlatMoney&gt;
&lt;/Artifact&gt;</pre>
<ul>
<li><b>Name and Description are display-only.</b> The strings the game shows come from <code>NameIndex</code> and <code>DescriptionIndex</code> in <code>GameText.yaml</code>, so a new artifact needs new ids and text there.</li>
<li>Percent fields are fractions: 0.5 is +50%. <code>PlusFlatMoney</code> is the only flat one.</li>
<li>An artifact with <code>Discovered</code> true is in the collection from the start; otherwise it has to be found by exploration.</li>
</ul>"""),
     groups=[
 G("Artifact effects", "What holding it changes.", "Percent values are fractions of the base stat.", "Spiritual adds its bonus on top of each value.", [
   T("Name","string","Artifact id.","", ""),
   T("Description","string","Flavour text.","", ""),
   T("NameIndex","int","Localised name.","", ""),
   T("DescriptionIndex","int","Localised description.","", ""),
   T("Discovered","bool","Already known at start.","", ""),
   T("FertilityMod","float","Colony fertility.","", ""),
   T("ProductionMod","float","Production.","", ""),
   T("ResearchMod","float","Research.","", ""),
   T("ReproductionMod","float","Population growth.","", ""),
   T("GroundCombatMod","float","Ground combat.","", ""),
   T("ModuleHPMod","float","Module hit points.","", ""),
   T("ShieldPenBonus","float","Shield penetration.","", ""),
   T("SensorMod","float","Sensor range.","", ""),
   T("DiplomacyMod","float","Diplomatic relations.","", ""),
   T("PlusFlatMoney","float","Credits per turn.","", ""),
 ]),
 ]),

dict(id="planetedicts", tier=2, title="Planet edicts", paths=["PlanetEdicts"], ext=".xml", roots=["ArrayOfPlanetEdict", "PlanetEdict"],
     fmt="XML", loader="no loader: PlanetEdict is a class but nothing deserializes PlanetEdicts/",
     override="One file. Edicts are chosen per colony; Name is the id.",
     l1="A standing order for a colony: what it should prioritise and how much it keeps.",
     l2="Edicts are the governor's sliders in preset form. They do not change output directly; they change what the colony does with it.",
     l3="Thresholds are shares of storage. Priority values weight the three outputs.",
     notation=dict(title="Copy this: a planet edict", body="""
<p>The whole of vanilla's <code>PlanetEdicts/Core.xml</code>, shortened by three fields:</p>
<pre class="code">&lt;PlanetEdict&gt;
  &lt;Name&gt;Core&lt;/Name&gt;
  &lt;Localization&gt;120&lt;/Localization&gt;
  &lt;Description&gt;1&lt;/Description&gt;
  &lt;PreventStarvation&gt;true&lt;/PreventStarvation&gt;
  &lt;FoodPriority&gt;0.1&lt;/FoodPriority&gt;
  &lt;ProductionPriority&gt;0.45&lt;/ProductionPriority&gt;
  &lt;ResearchPriority&gt;0.45&lt;/ResearchPriority&gt;
  &lt;FoodImportThreshold&gt;0.2&lt;/FoodImportThreshold&gt;
  &lt;FoodStoreThreshold&gt;0.3&lt;/FoodStoreThreshold&gt;
  &lt;FoodExportThreshold&gt;1.0&lt;/FoodExportThreshold&gt;
  &lt;BuildsTroops&gt;true&lt;/BuildsTroops&gt;
  &lt;BuildsDefensePlatforms&gt;true&lt;/BuildsDefensePlatforms&gt;
&lt;/PlanetEdict&gt;</pre>
<ul>
<li>Thresholds are fractions of that resource's storage: import below 0.2, store below 0.3, export at 1.0, with 0 and 1 the empty and full ends.</li>
<li>Priorities are relative weights, read against each other rather than against a total; vanilla splits 0.1 / 0.45 / 0.45.</li>
<li>One edict per file. A mod can ship a second file, but the governor screen lists what loads, so keep <code>Name</code> distinct.</li>
</ul>"""),
     groups=[
 G("Priorities and thresholds", "What the colony favours and when it trades.", "Thresholds are fractions; priorities are relative weights.", "The same fields the colony sliders write.", [
   T("Name","string","Edict id.","", ""),
   T("Localization","int","Localised name.","", ""),
   T("Description","int","Localised description.","", ""),
   T("PreventStarvation","bool","Never export food below need.","", ""),
   T("FoodPriority","float","Food weighting.","", ""),
   T("ProductionPriority","float","Production weighting.","", ""),
   T("ResearchPriority","float","Research weighting.","", ""),
   T("FoodImportThreshold","float","Import food below this.","", ""),
   T("FoodStoreThreshold","float","Store food below this.","", ""),
   T("FoodExportThreshold","float","Export food above this.","", ""),
   T("ProductionImportThreshold","float","Import production below this.","", ""),
   T("ProductionStoreThreshold","float","Store production below this.","", ""),
   T("ProductionExportThreshold","float","Export production above this.","", ""),
   T("BuildsTroops","bool","Allow troop construction.","", ""),
   T("BuildsDefensePlatforms","bool","Allow defence platforms.","", ""),
 ]),
 ]),

dict(id="randomstuff", tier=2, title="Planet spawn table", paths=["RandomStuff"], ext=".xml", roots=["RandomItem"],
     fmt="XML", loader="ResourceManager.LoadRandomItems",
     override="XML unifies by file name. BuildingID is the building placed.",
     l1="The odds that a generated planet gets a particular building or ruin.",
     l2="One file per building: a chance and an instance range for each planet type. This is how ruins, mines and abandoned structures appear.",
     l3="Chance is a percentage per planet of that type; InstanceMax caps how many can spawn. The nine planet-type groups repeat the same two fields.",
     groups=[
 G("Spawn rule", "What spawns and how often.", "Chance is a percentage; Min/Max bound the count.", "The same pattern exists for every planet category, including Gas and Volcanic.", [
   T("BuildingID","string","Building placed.","", ""),
   T("HardCoreOnly","bool","Only in hard-core games.","", ""),
   T("TerranChance/OceanicChance/DesertChance/SwampChance/TundraChance/BarrenChance/IceChance/SteppeChance/GasChance/VolcanicChance","float","Percent chance per planet of that type.","", ""),
   T("*InstanceMin/*InstanceMax","int","Minimum and maximum count on one planet.","", ""),
 ]),
 ]),

dict(id="namegenerators", tier=2, title="Name lists", paths=["NameGenerators"], ext=".txt", roots=[],
     fmt="plain text", loader="ResourceManager.GetNameGenerator / GetRandomNames (MarkovNameGenerator)",
     override="Text files merge or replace by file name; one name per line.",
     l1="Plain lists of names the game draws from for ships, spies and systems.",
     l2="A mod can replace a list or add a race-specific one. Blank lines and duplicates are harmless.",
     l3="The file stem selects the pool (names.txt, spynames_<Race>.txt). One entry per line, no commas.",
     groups=[
 G("List file", "One name per line.", "Order is the draw order until the list is shuffled.", "A missing race-specific list falls back to the generic one.", [
   T("line","text","A single name.","", ""),
 ]),
 ]),

dict(id="advice", tier=2, title="Advisor text", paths=["Advice"], ext=".xml", roots=["ArrayOfString"],
     fmt="XML per language", loader="ResourceManager.LoadRandomAdvice → LoadAdviceFor",
     override="One file per language. Mods replace by file name.",
     l1="The tips the game shows in the loading and advisor panels.",
     l2="Each entry is one tip, shown at random. There is no id to preserve.",
     l3="ArrayOfString > string. A missing language falls back to English.",
     groups=[
 G("Tip entry", "One tip.", "Text only; no formatting tags are interpreted.", "Keep tips short enough for the panel.", [
   T("string","text","One advisor tip.","", ""),
 ]),
 ]),

dict(id="militaryresearch", tier=2, title="Military research strategy", paths=["MilitaryResearchStrategy"], ext=".xml", roots=["MilitaryResearchStrategy"],
     fmt="XML", loader="no loader: no class or reader exists for MilitaryResearchStrategy/",
     override="No override: the folder is loaded by nothing.",
     l1="A research-order file that vanilla ships but no code loads.",
     l2="There is no MilitaryResearchStrategy class and no call that reads the folder: the name, the six path lists and every Tech entry are consumed by nothing, so editing or deleting the file changes no behaviour.",
     l3="Vanilla ships one file, Swarm.xml, and the build manifest lists it, which makes it look supported; outside the file itself the only mention of these path names in the repository is that manifest. Every card below therefore carries the fixed dead-key sentence rather than an explanation.",
     groups=[
 G("Strategy", "The keys the file carries.", "No loader reads any of them.", "Each card is the fixed dead-key sentence.", [
   T("Name","string","This item has no function in game."),
   T("BeamPath","element","This item has no function in game."),
   T("KineticPath","element","This item has no function in game."),
   T("MissilePath","element","This item has no function in game."),
   T("EnergyPath","element","This item has no function in game."),
   T("HullPath","element","This item has no function in game."),
   T("Tech","element","This item has no function in game."),
   T("id","string","This item has no function in game."),
   T("DefensePath","element","This item has no function in game."),
 ]),
 ]),

# ---------------------------------------------------------------- tier 2 YAML tuning
dict(id="research", tier=2, title="Research weights", paths=["Research.yaml"], roots=["ResearchSettings"],
     fmt="YAML", loader="ResourceManager.LoadResearchOptionSettings",
     override="One file; a mod's file replaces it, not merges per key.",
     l1="How expensive each research area is, per race and per hull or weapon type.",
     l2="Each block is a set of multipliers applied on top of the tech's own Cost: one map for technology types, one for hull classes, one for research areas and one for weapon tags. The file is a list of blocks keyed by race portrait, with All as the base every empire gets.",
     l3="`ResearchSettings.LoadYaml` deserializes the array and sorts it by `IsAll`, which puts the All block last, despite the comment there saying All is applied first. `LoadResearchOptions` then applies the blocks in that order and assigns `toMap[key] = value`, so All overwrites a race block for any key both set; a race block only wins on keys All leaves out. The four maps are read at different points: technology types and hull classes scale the AI's tech costs, research areas add to its priorities, and weapon tags scale a design's score once per tag.",
     groups=[
 G("Cost weights", "The multipliers.", "1 is neutral; 0.5 halves the price.", "Weapon and hull weights are selected by tag.", [
   T("PortraitName","string","The race portrait whose block this is, or All for every empire.",
     "It is matched against the empire's own PortraitName, and All matches every empire and is applied last, so a race block only survives on keys All does not set.",
     "`ResearchSettings.IsAll` compares it to `All` ignoring case, and `ApplyMatchingModifiers` accepts a block when `IsAll` or when `PortraitName == empire.PortraitName` exactly. `LoadYaml` sorts blocks by `IsAll` and `LoadResearchOptions` assigns each block's values in turn, so the last writer wins, which is All. A misspelt portrait never matches and its block does nothing."),
   T("TechnologyTypeModifiers","map","Cost multiplier for each technology branch.",
     "A tech that belongs to one of these types is priced with that multiplier, so 0.5 halves its research cost for the AI's chooser. A tech matching several types takes the first match in map order.",
     "`ResearchOptions.GetAnyTypeMod` walks `TechTypeMods` and returns the value of the first `TechnologyType` where `tech.IsTechnologyType` is true, or 1; `CostMultiplier(TechEntry)` multiplies that by the tech's own `LowPriorityCostMultiplier`, and `ChooseTech` applies the result to the cost. Vanilla's All block sets every type to 1, so the block is a template rather than a tuned table."),
   T("ShipCostModifiers","map","Score multipliers for hull classes and the ship picker's own knobs.",
     "The picker multiplies a candidate design's tech score by the value for its role, but only while the empire cannot build that role, so 2 makes that class twice as expensive to aim for. The same map holds Randomize, LineFocusIntensity and BalanceToInfraIntensity, which are numbers rather than multipliers.",
     "`ShipPicker` calls `Options.CostMultiplier(ShipCosts.X)` for hull techs, orbitals, colony and freighter designs, and role values gated on `!empire.CanBuild...`; `Randomize` scales the random cost swing, `LineFocusIntensity` is read as an int and discounts ships continuing a known line, and `BalanceToInfraIntensity` scales the ship-versus-infrastructure cost ratio. Vanilla: Carrier, Bomber, TroopShip and Support 0.95, ColonyShip, Freighter and Orbitals 2, AllHulls 1, GroundCombat 0.95, Randomize 0.1."),
   T("ResearchAreaModifiers","map","Extra weight each research area gets in the AI's priorities.",
     "It is added to the strategy's own ratio for that area, so 1 is a full point of preference and 0.5 a half, not a multiplier. Vanilla's All block uses 1 for every area except GroundCombat at 0.5.",
     "`ResearchPriorities` builds its table as the strategy ratio plus `Priority.GetPriority(area)`, and `GetPriority` returns the map value or 1 when the area is absent. Because the numbers are added rather than multiplied, a value of 10 swamps the strategy's own ratios and a negative value can push an area below zero. Vanilla's block reproduces the code defaults."),
   T("WeaponModifiers","map","Score multiplier for each weapon tag on a candidate design.",
     "Every distinct weapon tag on a design multiplies its tech score, so a design with beams and missiles gets both values applied; 0.5 makes that design half as expensive for the AI to aim for. Vanilla sets every tag to 1.",
     "`ShipPicker` iterates the design's distinct tags and does `techScore *= Options.CostMultiplier(tag)`, which reads `WeaponPreference` and returns 1 for a tag the file does not name. The keys are `WeaponTag` members, and vanilla's All block lists twelve of them at 1.00, from Kinetic to Torpedo."),
   T("LineFocusIntensity","float","How strongly the AI focuses a line.","Read as an int, so 0 to 0.99 all disable line focusing; 1 counts each already-known tech once, larger values discount ships that continue a line more, and nothing clamps them.", "", key="ShipCosts"),
   T("Randomize","float","Randomise the weights.","0 turns the roll off, 0.1 gives a 10% swing either way, and at 1 a roll can cancel the whole score; above 1 it can drive the score negative, so the useful maximum is 1.", "", key="ShipCosts"),
 ]),
 G("Weight keys", "The names inside each modifier map.", "These are keys, not separate elements: the value beside each one is a multiplier.", "A key that does not match a technology type, hull class or weapon tag is ignored.", [
   T("General","float","General research weight.","0 zeroes that branch's price, which makes the chooser skip it, and adds no weight to its area; 1 leaves both unchanged, and nothing clamps values above 1.", "", key=("TechnologyType", "ResearchArea")),
   T("Colonization","float","Colonization weight.","0 zeroes that branch's price, which makes the chooser skip it, and adds no weight to its area; 1 leaves both unchanged, and nothing clamps values above 1.", "", key=("TechnologyType", "ResearchArea")),
   T("Economic","float","Economic weight.","0 zeroes that branch's price, which makes the chooser skip it, and adds no weight to its area; 1 leaves both unchanged, and nothing clamps values above 1.", "", key=("TechnologyType", "ResearchArea")),
   T("Industry","float","Industry weight.","0 zeroes that branch's price, which makes the chooser skip it, and adds no weight to its area; 1 leaves both unchanged, and nothing clamps values above 1.", "", key=("TechnologyType", "ResearchArea")),
   T("Research","float","Research weight.","0 zeroes that branch's price, which makes the chooser skip it, and adds no weight to its area; 1 leaves both unchanged, and nothing clamps values above 1.", "", key=("TechnologyType", "ResearchArea")),
   T("GroundCombat","float","Ground combat weight.","0 zeroes GroundCombat techs (so the chooser skips them), their hull-class cost and the area weight; 1 leaves all three unchanged, and nothing clamps values above 1.", "", key=("TechnologyType", "ShipCosts", "ResearchArea")),
   T("ShipHull","float","Hull weight.","0 zeroes that branch's price, and the chooser only takes costs above 0, so 0 drops the branch instead of making it free; 1 leaves the price unchanged, and nothing clamps values above 1.", "", key="TechnologyType"),
   T("ShipDefense","float","Defence weight.","0 zeroes that branch's price, and the chooser only takes costs above 0, so 0 drops the branch instead of making it free; 1 leaves the price unchanged, and nothing clamps values above 1.", "", key="TechnologyType"),
   T("ShipWeapons","float","Weapons weight.","0 zeroes that branch's price, and the chooser only takes costs above 0, so 0 drops the branch instead of making it free; 1 leaves the price unchanged, and nothing clamps values above 1.", "", key="TechnologyType"),
   T("ShipGeneral","float","General ship weight.","0 zeroes that branch's price, and the chooser only takes costs above 0, so 0 drops the branch instead of making it free; 1 leaves the price unchanged, and nothing clamps values above 1.", "", key="TechnologyType"),
   T("ShipTech","float","Ship technology weight.","0 leaves only the strategy's own ratio, 1 adds 100 points of weight, a negative value subtracts, and nothing clamps the result.", "", key="ResearchArea"),
   T("Carrier","float","Carrier hull weight.","0 makes that role free to research and therefore first pick, 1 leaves it unchanged, and nothing clamps values above 1; the multiplier applies only while the empire cannot build the role.", "", key="ShipCosts"),
   T("Bomber","float","Bomber hull weight.","0 makes that role free to research and therefore first pick, 1 leaves it unchanged, and nothing clamps values above 1; the multiplier applies only while the empire cannot build the role.", "", key="ShipCosts"),
   T("TroopShip","float","Troop ship weight.","0 makes that role free to research and therefore first pick, 1 leaves it unchanged, and nothing clamps values above 1; the multiplier applies only while the empire cannot build the role.", "", key="ShipCosts"),
   T("Support","float","Support hull weight.","0 makes that role free to research and therefore first pick, 1 leaves it unchanged, and nothing clamps values above 1; the multiplier applies only while the empire cannot build the role.", "", key="ShipCosts"),
   T("ColonyShip","float","Colony ship weight.","0 makes every design of that role free to pick, 1 leaves it unchanged, and nothing clamps values above 1.", "", key="ShipCosts"),
   T("Freighter","float","Freighter weight.","0 makes every design of that role free to pick, 1 leaves it unchanged, and nothing clamps values above 1.", "", key="ShipCosts"),
   T("AllHulls","float","All hull classes.","0 makes the hull techs inside a ship's score free, 1 leaves them unchanged, and nothing clamps values above 1.", "", key="ShipCosts"),
   T("Orbitals","float","Orbital hull weight.","0 makes every design of that role free to pick, 1 leaves it unchanged, and nothing clamps values above 1.", "", key="ShipCosts"),
   T("Kinetic","float","Kinetic weapon weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Energy","float","Energy weapon weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Guided","float","Guided weapon weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Missile","float","Missile weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Plasma","float","Plasma weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Beam","float","Beam weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Intercept","float","Interception weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Bomb","float","Bomb weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("BioWeapon","float","Biological weapon weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Cannon","float","Cannon weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("PD","float","Point defence weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("SpaceBomb","float","Space bomb weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Torpedo","float","Torpedo weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
   T("Drone","float","Drone weight.","Every distinct weapon tag on a design multiplies its score, so three tags apply three values; 0 makes designs with that tag free, 1 is neutral, and nothing clamps values above 1.", "", key="WeaponTag"),
 ]),
 ]),

dict(id="budgets", tier=2, title="AI budgets", paths=["Budgets.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadBlackboxSpecific",
     override="One file; replaces vanilla.",
     l1="The starting budget split each AI uses for defence, building, spying and savings.",
     l2="Shares are per race, keyed by portrait. They steer the AI's spending, not the player's.",
     l3="Each value is a share of income: the set is divided by its own total, and the planner floors every area's result at 1, so no area can be switched off from this file.",
     groups=[
 G("Budget split", "Where the AI's money goes.", "Values are relative shares.", "PortraitName selects the race.", [
   T("PortraitName","string","Which race's budget block this is.","Only the block named All is read. The loader logs a warning for every other name and skips its numbers, so a per-race split in a mod does nothing.","The comparison ignores case. A file that contains only a race-specific block therefore loads no budgets at all."),
   T("Budgets","map","The block holding one weight per spending area.","The loader reads it as a table of area names, which is why the keys below are spelled exactly as the game spells them.","An area the file omits is absent from the table and gets nothing; a misspelled name is absent too, with no warning."),
   T("Defense","float","The share of income kept for holding what the empire owns.","The eight numbers in this block are weights, not percentages: the AI adds them up and gives each area its slice of that total, so raising defence takes from every other area without any other number changing. Even 0 cannot switch an area off: the planner floors every area's budget at 1, so this value still buys a token amount.","The slice is this value divided by the sum of all eight, so only their ratios matter: doubling every value changes no budget. Defence also receives half of build plus spy when the empire is the player, and the slice is scaled again by the threat level, so the same file funds more defence in a war.", key="BudgetAreas"),
   T("SSP","float","The share set aside for subspace projector stations.","Subspace projectors are the platforms that push an empire's border outward, and this is what the AI spends on them. Like the other seven it is a weight in one total, so it competes directly with ships and colonies for the same income. 0 is floored to a budget of 1 rather than 0, so projector building is starved to a token amount rather than switched off.","A player empire gets half of build plus spy added to this slice on top of the file's value, which is why a player projects influence sooner than the numbers alone suggest.", key="BudgetAreas"),
   T("Build","float","The share spent on new hulls.","This is the biggest sink in most AI economies, and it is a weight in the eight-part split: the real ship budget is this value's slice of the whole, not the value itself. 0 is floored to 1, so construction is starved rather than stopped.","The slice is scaled once more by the threat level and the treasury goal before the ship goals spend it, so a rich empire at peace builds less than the same empire at war. A player empire's build slice is unchanged, but half of build plus spy is also copied into defence, colony and projectors.", key="BudgetAreas"),
   T("Spy","float","The share the AI devotes to espionage.","A player empire never has a spy budget, so this number only means something for the AI. It is a weight in the same split as the rest.","For an AI empire with the new espionage system on, the file's value is ignored: the slice is overwritten with Espionage, or forced to 0 on Normal difficulty. With the old system the value is used as written, and a race that knows no foreign empire spends nothing regardless.", key="BudgetAreas"),
   T("Espionage","float","A weight that only seeds the spy slice.","It never becomes a spending area of its own, and on Normal difficulty even the spy slice is forced to 0, so the key does nothing there.","The loader drops Espionage before the split, so unlike Savings it does not dilute the other seven. It is read only for an AI empire with the new espionage system on, and only to set what the spy area receives.", key="BudgetAreas"),
   T("Colony","float","The share for settling and holding worlds.","Colony ships, outposts and the support they need come out of this slice, so expansion is funded at the expense of ships and defence. A player empire also gets half of build plus spy added here.","The slice feeds the colony budget the expansion goals draw on. Terraforming is paid from a separate slice computed the same way, so the two do not share a pool.", key="BudgetAreas"),
   T("Terraform","float","The share for improving worlds already held.","Terraformers, atmosphere and the projects that follow come from this slice, which is its own cut rather than a share of the colony budget. 0 is floored to 1, so terraforming is starved rather than switched off.","The colony slice keeps its own money either way. A world the AI cannot afford to terraform stays as it is until something else changes it.", key="BudgetAreas"),
   T("Savings","float","A weight that is read and then never spent.","The AI keeps no savings budget of its own, yet the value still counts in the total, so raising it shrinks every other area's slice while buying nothing.","Only the divisor changes when this value moves. Leave it at 0 unless the intent is to starve every other area at once.", key="BudgetAreas"),
 ]),
 ]),

dict(id="fleetratios", tier=2, title="Fleet build ratios", paths=["FleetBuildRatios.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadBuildRatios",
     override="One file; replaces vanilla.",
     l1="How many of each hull class the AI wants in a fleet.",
     l2="Each role key holds a low and a high count in a two-item list. The block is chosen by the best hull class the empire can build, and with randomized sizes off the low count is the count actually used.",
     l3="CanBuild is one value per block, not a list; the loader picks the block for the highest class the empire can build and throws at load if that block is missing. The numbers are ship counts, not percentages: they feed the fleet assembly target and a cost-weighted share of the AI's budget. The second number is read only when EnableRandomizedAIFleetSizes is true.",
     notation=dict(title="The [0, 6] notation, number by number", body="""
<p><code>Fighters: [0, 6]</code> is a YAML list of two numbers on one line. The game reads the first number as the low end and the second as the high end of a ship count; it never reads the brackets and the comma as one value.</p>
<table>
<tr><th>item</th><th>what it is</th><th>what it does</th></tr>
<tr><td class="n">[ ]</td><td>list</td><td>Marks the two numbers as one list. The comma separates them; the space after it is optional.</td></tr>
<tr><td class="n">0</td><td>low end</td><td>The count used when randomized fleet sizes are off, and the smallest result when they are on. It is a whole number of ships, not a percentage and not a share of a budget.</td></tr>
<tr><td class="n">6</td><td>high end</td><td>The upper bound when randomized sizes are on. It is exclusive: the roll is <code>[0, 6)</code> and the result is truncated to a whole number, so the highest count produced is 5. With randomization off this number is ignored entirely.</td></tr>
</table>
<p><b>Vanilla setting.</b> <code>Globals.yaml</code> sets <code>EnableRandomizedAIFleetSizes: false</code>, so vanilla uses only the first number: <code>[0, 6]</code> means 0 ships, <code>[4, 6]</code> means 4, and <code>[24, 36]</code> means 24. Turn the setting on and the same block rolls between the two numbers instead, which is why the second number must still be a count the AI should accept.</p>
<p><b>In a mod.</b> Copy the whole <code>FleetBuildRatios.yaml</code> to <code>Mods/&lt;Name&gt;/FleetBuildRatios.yaml</code>, beside <code>Content/</code> rather than inside it; the file replaces vanilla rather than merging with it. Keep a block for every <code>CanBuild</code> tier the AI can reach (vanilla has six) and all ten role keys in each block, then write the two numbers in the order low, high. <code>Frigates: [4, 6]</code> gives 4 frigates with randomization off, and 4 or 5 with it on.</p>"""),
     groups=[
 G("Ratios", "The desired mix.", "Counts are ships, not percentages.", "A role the empire cannot build is set to 0 after the block is chosen.", [
   T("CanBuild","string","Which build tier this block describes.","Its value is one of six fixed names, from CanBuildFighters to CanBuildCapitals, and the AI picks the block for the highest class it can build. A tier with no block makes content load fail.","The loader builds a map keyed by the six enum values and throws when a block is missing, so all six are required even if a mod never reaches the top. The value is not a list and not a count. It selects which set of role numbers applies."),
   T("Fighters","int","Fighter count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The role is zeroed when the empire cannot build fighters.","Fighters are the fallback tier's main hull, and later blocks keep a small screen of them. The count is a minimum in the fleet plan that the planner turns into a budget share, so raising it crowds out other roles. Vanilla starts at 24-36 and falls to 1-4 once capitals are buildable."),
   T("Corvettes","int","Corvette count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The role is zeroed when the empire cannot build corvettes.","Corvettes appear from the second tier and peak in the battleship block. The number is a minimum that becomes a budget share in the fleet planner, not a hard cap. A zero keeps the role out of the plan at that tier."),
   T("Frigates","int","Frigate count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The role is zeroed when the empire cannot build frigates.","Frigates first appear when the empire can build them and stay in every later block as a screen. The value is a minimum that the planner converts into a maintenance budget, so raising it reduces what is left for larger hulls. Vanilla keeps them at 4-6 or above once available."),
   T("Cruisers","int","Cruiser count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The role is zeroed when the empire cannot build cruisers.","Cruisers are the first heavy line and rise sharply in the capital block. The number is a minimum used as a budget weight, not a target the AI always reaches. A zero in an earlier block keeps the role out until its tier."),
   T("Battleships","int","Battleship count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The role is zeroed when the empire cannot build battleships.","Battleships are zero until the battleship tier and become the bulk of the line at the capital tier. The value is a minimum that becomes a budget share, so it competes with capitals rather than adding to them. Vanilla goes from 2-3 to 8-12."),
   T("Capitals","int","Capital count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The role is zeroed when the empire cannot build capitals.","Capitals are zero until the top tier, where they take the largest share of the line. The value is a minimum and a budget weight, so the AI builds them only while maintenance allows. Vanilla sets 4-6."),
   T("TroopShips","int","Troop ship count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The planner zeroes the role when the empire cannot build troop ships.","Troop ships carry the ground invasion, so the value decides how much army a fleet can land at once. It is zeroed by capability, not by the block, and the plan still builds to it on a small budget. Vanilla keeps it at 1-2 in every tier."),
   T("Bombers","int","Bomber count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The planner zeroes the role when the empire cannot build bombers.","Bombers are the anti-ship strike wing, and in practice they arrive in carrier wings because only carriers can bring them. The number is a minimum budget weight, so it buys squadrons rather than single hulls. Vanilla runs 1-3."),
   T("Carriers","int","Carrier count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The planner zeroes the role when the empire cannot build carriers.","Carriers bring the fighter and bomber wings and have weak guns of their own, so this value trades direct fire for strike range. The number is a minimum budget weight, not a fixed escort count. Vanilla keeps 1-5 depending on tier."),
   T("Support","int","Support ship count, low then high.","The low number is used unless randomized fleet sizes are on, and the high end is then exclusive. The planner zeroes the role when the empire cannot build support ships.","Support ships repair and resupply the fleet, so a high value makes it more durable but slower to replace losses. The value is a minimum budget weight rather than a fixed escort count. Vanilla keeps 1-2 in every block."),
 ]),
 ]),

dict(id="econstrats", tier=2, title="AI economic strategies", paths=["EconomicResearchStrategies.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadEcoResearchStrats",
     override="One file; replaces vanilla.",
     l1="Named AI economic plans: how much it values military, expansion, research and industry.",
     l2="A race's diplomatic personality names one of these strategies.",
     l3="Priority values are relative weights; TechPath lists the techs the plan prefers.",
     groups=[
 G("Strategy", "The priorities and tech path.", "Higher priority means more budget.", "The name is referenced by DiplomaticTraits ETrait entries.", [
   T("Name","string","The strategy's lookup name.","Races name a strategy in their ETrait EconomicResearchStrategy field, and the loader keys this file by the name. A race naming one that is absent has no strategy to load.","The diplomacy code also recognises the five vanilla names in a fixed switch; a new name falls back to Generalists there while still supplying its research ratios. Two entries with the same name keep the last one. The name is not shown to the player."),
   T("MilitaryPriority","float","How much the plan values military research and ground combat.","Priorities are summed and each becomes its share of the total with a 10% floor, so a 2 among 1s takes twice the slice. Changing one rebalances all four.","The military share is added to the ground-combat research priority and the fleet planner's build desire; fleet composition itself comes from FleetBuildRatios, not here. A zero still gets the 10% floor. The raw sum is the divisor, so raising one priority dilutes the others."),
   T("ExpansionPriority","float","How much the plan values colonisation and economic techs.","It is a weight, not a count: the ratio is the priority over the sum of all four, floored at 10%. It feeds colonisation and economic research plus the colony build desire.","The same ratio raises expansion and economic research priorities and the colony production weighting, so one value moves both research and building. A zero is raised to the floor rather than removing the area. Because the divisor is the raw sum, a high expansion value shrinks the other three."),
   T("ResearchPriority","float","How much the plan values research and general techs.","The ratio is the priority over the sum of all four, floored at 10%, and it feeds research and general research priorities. It also lowers the per-level production bonus a colony gives, because research-heavy plans accept slower development.","The colony formula subtracts colony level times this ratio from the development bonus, so a research-heavy plan builds less per world. The same ratio is added to the research and general research areas. A zero still keeps the floor, so it never disappears completely."),
   T("IndustryPriority","float","How much the plan values industrial techs and colony production.","The ratio is the priority over the sum of all four, floored at 10%, and it raises industry research and the colony build desire. It competes directly with military and expansion for the same budget.","The colony production formula adds the industry ratio to the build desire, which raises the worker share for construction. The research side adds the same ratio to the industry research area. A high value therefore speeds both building and the techs that improve it."),
   T("TechPath","string[]","The techs the plan researches first, in order.","Each entry is a tech UID; the AI follows the list before falling back to weighted research. A name that resolves to no tech is skipped when the list is walked.","An entry may carry a colon and a number to jump within the list, which the chooser parses. The path is a preference, not a lock: when every listed tech is owned or unavailable, normal priorities take over. Vanilla lists IndustrialFoundations for all five strategies."),
 ]),
 ]),

dict(id="planettypes", tier=2, title="Planet types", paths=["PlanetTypes.yaml"],
     roots=["PlanetType", "PlanetTypes"],
     fmt="YAML", loader="PlanetTypes.LoadPlanetTypes (called from ResourceManager.LoadContent)",
     override="One file; a mod's file replaces it.",
     catalogue=dict(key="Id", title="Every planet type in vanilla, by Id",
       fields=[("Name", ""), ("Category", ""), ("Habitable", "habitable"),
               ("HabitableTileChance", "habitable tiles"), ("PopPerTile", "pop/tile"),
               ("BaseFertility", "fertility"), ("MiningChance", "mining chance")],
       note=("These 43 types are the values a solar system can name. WhichPlanet writes one of these "
             "Ids, not a position in the list, so a mod can add types without renumbering the rest. "
             "An Id that no longer exists falls back to a random type during generation; the direct "
             "lookup used when a planet is restored has no fallback. Ids must be unique: a duplicate "
             "logs an error and the first entry wins.")),
     l1="The catalogue of planet looks and stats: what a Terran, ice or volcanic world is like.",
     l2="Each type sets rendering meshes and textures, habitability, population per tile and fertility. Solar systems pick a type by its Id.",
     l3="WhichPlanet is a PlanetType.Id, not the entry's position: the loader builds a map keyed by Id, so appending a type changes no existing reference.",
     groups=[
 G("Globals", "Meshes and scales shared by all types.", "Paths are relative to Content/.", "NewRenderer is a work-in-progress switch; leave it false.", [
   T("PlanetScale","float",
     "The size of every planet in the galaxy, as a multiplier on the shared planet mesh.",
     "The shared mesh is 100 units across; vanilla's 10 draws each planet 1,000 units across before its own size variation, so this one number sets how large worlds look next to ships, stations and orbits.",
     "Each planet's visible radius is the mesh's radius times this value times that planet's own size — a generated world adds a random 0.9 to 1.8 to its type's Scale, a homeworld uses the race's homeworld size trait, and a system file that sets a planet scale overrides both — so a replacement mesh of a different size changes what this number means. "
     "The radius is added to the planet's orbit distance when the system is generated, so raising this value also pushes every body outward by its own planet's radius. "
     "Reloading the file rescales what is drawn at once, but the stored radius and orbit keep their old size until the system is generated again. "
     "It leaves the gravity well alone — that follows the per-planet size, not this value — and it changes no population, fertility or mining figure. "
     "Near 0 every planet collapses to a point while its orbit stays; far above 10 the added radius dominates the orbit spacing, which is where neighbouring worlds start to overlap."),
   T("RingsScale","float",
     "How wide a planet's ring disc is, measured against the ring mesh rather than the planet.",
     "Vanilla's 3 is chosen for the shared ring mesh so the rings come out slightly wider than the planet; a replacement mesh needs its own number.",
     "Rings are drawn with this scale applied on top of the planet's own scale, so PlanetScale moves the rings with the planet while this value only resizes the disc. "
     "The disc is tilted by the planet's ring tilt and drawn only when the body has rings; a type without rings ignores the value. "
     "Nothing else reads it: no orbit, click area or gravity well depends on the disc, so a ring that looks far too wide changes no gameplay. "
     "A value that draws the disc inside the planet hides its inner edge behind the surface."),
   T("CloudsScale","float",
     "How far the cloud layer floats above the planet surface.",
     "It multiplies the planet's radius: 1.015 is 1.5% wider, enough to keep the clouds off the surface without a visible gap.",
     "Clouds are drawn only for types whose atmosphere preset supplies a cloud map, and the layer turns at two thirds of the planet's spin. "
     "The layer is the same sphere mesh as the planet, so this number is the whole gap between cloud and ground. "
     "At 1 the two surfaces coincide and flicker; below 1 the clouds vanish inside the planet. "
     "AtmosphereScale and HaloScale are measured from the planet-sized sphere, not from the clouds, so raising this value does not move the haze."),
   T("AtmosphereScale","float",
     "How far the blue haze shell sits outside the planet's surface.",
     "1.03 draws the haze 3% wider than the planet, which reads as a coloured rim at the edges rather than a thick envelope.",
     "The haze is drawn only when the type has clouds and its atmosphere preset does not switch the sphere off with NoAtmosphere. "
     "It inverts the planet's own mesh, so it shows near the silhouette and disappears at the centre of the disc; at exactly 1 it is hidden in the surface. "
     "Its colour and strength come from the preset's glow colour, not from this scale. "
     "HaloScale is a separate shell with its own key, so widening one does not widen the other."),
   T("HaloScale","float",
     "How far the pale halo sits outside the planet, the faint shine on the sunlit edge.",
     "1.03 puts it 3% wider than the planet, the same shell size as the blue haze; it is drawn only on clouded worlds that do not switch it off.",
     "The halo needs both a cloud map and an atmosphere preset that does not set NoHalo, so an airless world never shows it. "
     "It is fainter and tighter than the glow, and its brightness comes from the sun's direction rather than from this number. "
     "At 1 it lies on the surface and is lost; below 1 it is inside the planet and invisible, so raise it in small steps and watch the limb."),
   T("GlowScale","float",
     "How far the coloured glow and its fresnel rim sit outside the planet surface.",
     "1.005 keeps the glow almost on the surface, so it reads as light coming off the world rather than a separate ring; the colour and strength come from the atmosphere preset.",
     "The glow is drawn only for a type whose preset sets a glow colour, and it stops being drawn once the camera is more than about 300,000 units away. "
     "It scales the glow mesh and the fresnel shell together, so the two always line up. "
     "At 1 or below the glow sinks into the planet and is hidden; raise it only as far as the preset's colour can carry without showing a gap. "
     "The glow always turns to face the camera, so this size is the only thing that decides how wide the light looks."),
   T("PlanetMesh","string","Shared planet mesh.","", ""),
   T("RingsMesh","string[]","Ring mesh and texture.","", ""),
   T("GlowEffect","string[]","Glow mesh and texture.","", ""),
   T("FresnelEffect","string[]","Fresnel mesh and texture.","", ""),
   T("NewRenderer","bool","Use the experimental renderer.","", ""),
   T("AtmosphereTypes","map","Atmosphere presets.","", ""),
 ]),
 G("A planet type", "One entry in Types.", "The index is the WhichPlanet value solar systems use.", "Diffuse/normal/emissive maps are texture paths.", [
   T("Id","int","The number a solar system writes as WhichPlanet.",
     "Ids must be unique: a duplicate logs an error and the first entry wins.",
     "Generation falls back to a random type when the Id is missing; the direct lookup used to restore a planet has no fallback."),
   T("Name","string","Display name.","", ""),
   T("Category","enum","Which family of planet this is.",
     "The category drives generation weights, allowed moons and icons; the Habitable flag, not the category, decides colonisation.",
     "", values=("enum:PlanetCategory", PLANET_CATEGORIES)),
   T("AmbientCues","string[]","Ambient sounds.","", ""),
   T("Composition","string","Flavour composition.","", ""),
   T("IconPath","string","Colony icon.","", ""),
   T("DiffuseMap","string","Colour texture.","", ""),
   T("SpecularMap","string","Specular texture.","", ""),
   T("NormalMap","string","Normal map.","", ""),
   T("EmissiveMap","string","Emissive map.","", ""),
   T("SpecularPower","float","Specular strength.","", ""),
   T("AtmosphereType","string","One or more AtmosphereTypes preset ids.",
     "A list is applied in order, so a later preset adds to or overrides the earlier glow, fresnel and flags.",
     "A name that is not defined under AtmosphereTypes logs an error and is skipped.",
     values=("ids:PlanetTypes.yaml:AtmosphereTypes", ATMOSPHERE_PRESETS)),
   T("Habitable","bool","Can be colonised.","", ""),
   T("HabitableTileChance","float","Share of tiles that are habitable.","", ""),
   T("PopPerTile","float","Population per tile.","", ""),
   T("BaseFertility","float","Starting fertility.","", ""),
   T("MoonTypes","PlanetCategory[]","Moon categories this type may roll.",
     "A moon is picked from the listed categories at random, then a type is picked inside that category.",
     "An empty list throws when the game asks for a moon of this planet.",
     values=("enum:PlanetCategory", PLANET_CATEGORIES)),
   T("ResearchableChance","float","Chance of a research bonus.","", ""),
   T("MinBaseFertility","float","Fertility floor.","", ""),
   T("Scale","float","Type-specific scale.","", ""),
   T("PlanetTile","string","Surface tile texture.","", ""),
   T("MiningChance","float","Chance of minerals.","", ""),
   T("Types","element","The list of planet types.","Order is the index WhichPlanet uses.", ""),
 ]),
 ]),

dict(id="suns", tier=2, title="Sun types", paths=["Suns.yaml"], roots=[],
     fmt="YAML", loader="SunType.LoadSunTypes",
     override="One file; replaces vanilla.",
     catalogue=dict(key="Id", title="Every sun in vanilla",
       fields=[("Habitable", "habitable zone"), ("Radius", "radius"),
               ("LightIntensity", "light intensity"), ("MultiSun", "multi-star")],
       note=("These Ids are what SunPath in a solar-system or map file names; the Id string is the "
             "join key, and the renderer layers below each entry only change how the star looks.")),
     l1="The catalogue of stars: colour, light, size and whether they damage ships.",
     l2="A solar system's SunPath names one of these Ids. Radiation is a real damage zone, not decoration.",
     l3="Layers are the visual shells; IconLayer picks the map icon. RadiationRadius is in game units.",
     groups=[
 G("Sun", "One star type.", "Ids are what SunPath references.", "ResearchableChance affects generated systems, not hand-placed ones.", [
   T("Id","string","The id a solar system's SunPath names.",
     "Every Id vanilla ships is listed in the table above; a SunPath with no matching Id is not a star.",
     "The Id is the join key, so renaming one breaks every map file that names it."),
   T("IconPath","string","Map icon.","", ""),
   T("IconScale","float","Icon size.","", ""),
   T("LightIntensity","float","Light output.","", ""),
   T("Radius","float","Star radius.","", ""),
   T("LightColor","float[]","Light colour RGB.","", ""),
   T("Habitable","bool","Can host habitable planets.","", ""),
   T("MultiSun","bool","Multiple stars.","", ""),
   T("Layers","map","Visual layers.","", ""),
   T("IconLayer","string","Layer used for the icon.","", ""),
   T("ResearchableChance","float","Chance of a research bonus.","", ""),
   T("RadiationDamage","float","Damage per second.","", ""),
   T("RadiationRadius","float","Damage radius.","", ""),
   T("TexturePath","string","Star texture.","", ""),
   T("TextureColor","float[]","Texture tint.","", ""),
   T("BlendMode","SpriteBlendMode","How the layer is blended onto the star.",
     "Additive makes overlapping layers brighter; AlphaBlend keeps the texture's own transparency.",
     "An unknown name fails to bind, and the layer keeps its default of AlphaBlend.",
     values=("enum:SpriteBlendMode", SPRITE_BLEND)),
   T("LayerScale","float","Layer size multiplier.","", ""),
   T("RotationSpeed","float","Layer rotation speed.","", ""),
   T("RotationStart","float","Starting rotation.","", ""),
   T("PulseColor","float[]","Pulse tint.","", ""),
   T("PulsePeriod","float","Pulse cycle seconds.","", ""),
   T("PulseScale","float","Pulse size multiplier.","", ""),
   T("AnimationPath","string","Animated layer texture.","", ""),
   T("AnimationSpeed","float","Animation frames per second.","", ""),
 ]),
 ]),

dict(id="sunzones", tier=2, title="Sun zone data", paths=["SunZoneData.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadSunZoneData",
     override="One file; replaces vanilla.",
     l1="How likely each orbit is to hold a given kind of planet.",
     l2="Zones are the rings around a star; each has a distribution of planet categories.",
     l3="The sum of a distribution is normalised. Changing it changes generated systems, not hand-placed ones.",
     groups=[
 G("Zone", "One orbital band.", "Zone is the band index; Distribution weights planet categories.", "Weights need not sum to 1.", [
   T("Zone","int","Orbital band.","", ""),
   T("Distribution","map","Category weights.","", ""),
 ]),
 ]),

dict(id="dyson", tier=2, title="Dyson rings", paths=["DysonRings.yaml"], roots=["SunLayerInfo", "DysonRings"],
     fmt="YAML", loader="DysonRings.LoadDysonRings",
     override="One file; replaces vanilla.",
     l1="The ring layers drawn around a star for each stage of a Dyson swarm.",
     l2="The file is presentation only: each stage lists eight ring layers with a texture and their motion. What a swarm produces is decided by the swarm itself and the racial trait that unlocks its stage, not here.",
     l3="`DysonRings.LoadDysonRings` deserializes the file into a Map keyed by Type, so a repeated stage keeps only the last block. `SolarSystem` asks for a stage through `GetDysonRings` and draws the back rings before the star's own layers and the front rings after them. The file's own header says the structure is hardcoded: the count and order of the eight rings are code, and only the paths and motion are content.",
     notation=dict(title="Copy this: a Dyson ring layer", body="""
<p>The first layer of the first ring type. The file's own header comment says the layer structure is hardcoded and only the texture paths should change:</p>
<pre class="code">- DysonSwarm:
  Type: 1
  Rings:
    - Ring:
      TexturePath: Suns/Type1DysonSwarmBack1.png
      BlendMode: Additive
      RotationSpeed: -0.001
      PulsePeriod: 5.0
      LayerScale: 0.15</pre>
<ul>
<li><b>Type</b> is the swarm stage. Vanilla ships stages 1 and 2; a stage the file omits throws when the swarm asks for it, because the map lookup has no fallback.</li>
<li><code>TexturePath</code> is relative to <code>Textures/</code>. Keep the eight layers and their order, and swap the images for a retexture.</li>
<li><code>PulsePeriod</code> is in seconds and 0 turns the pulse off; <code>RotationSpeed</code> is radians per second, so a negative value turns the layer the other way.</li>
</ul>"""),
     groups=[
 G("Ring stage", "One upgrade stage.", "The file repeats the block per stage; the stages are code-driven, so content only supplies their look.", "A stage the file omits throws when asked for, and a repeated Type keeps only the last block.", [
   T("Type","byte","The swarm stage this ring set belongs to.",
     "The loader keeps the sets in a byte-keyed map, so a repeated Type keeps only the last entry.",
     "The layer structure is hardcoded: a new stage needs a matching entry and a caller that asks for it.",
     values=("key:DysonRings.yaml:Type", DYSON_STAGES)),
   T("Rings","map","The eight ring layers of one stage.",
     "The loader reads it as a list of SunLayerInfo; the first four draw behind the star and the last four in front, and each ring fades in at its own quarter of the swarm's completion.",
     "`DysonRings.NumBacktRings` is 4, and `SolarSystem` draws the set twice: `DrawDysonRings(..., drawBackRings: true)` before the star's layers and once more after them for the front rings. `GetRingAlpha(index, completion)` maps index 0-3 to `((completion - 0.25*index)*4).Clamped(0,1)` and index 4-7 the same with index-4, so ring 0 appears first and ring 3 last. The four/four split is a constant, not something the file can change."),
   T("TexturePath","string","The image for one ring layer.",
     "It is relative to Textures/ and is what the layer draws unless AnimationPath is set. A path that no longer resolves falls back to the game's default texture instead of failing the load.",
     "`SunLayerState.CreateSprite` calls `DrawableSprite.SubTex(content, info.TexturePath)`, which loads `Textures/` plus the path through `LoadTextureOrDefault`; a non-empty `AnimationPath` wins and this field is then unused. Vanilla points the eight rings of a stage at `Suns/Type1DysonSwarmBack1.png` and its seven siblings, so a retexture only has to replace those eight files."),
   T("BlendMode","SpriteBlendMode","How the ring layer is blended.",
     "Additive brightens where rings overlap; AlphaBlend keeps the texture's transparency.",
     "An unknown name is not a blend mode, so the layer keeps its default of AlphaBlend.",
     values=("enum:SpriteBlendMode", SPRITE_BLEND)),
   T("LayerScale","float","How large one ring layer draws against the star.",
     "It multiplies the layer's on-screen size after the star's own scale and the pulse, so 0.15 draws the ring at 15% of the star's size. Vanilla uses 0.15 on every ring.",
     "`SunLayerState.Draw` computes `scale = ScaleIntensity * sizeScaleOnScreen * Info.LayerScale`, where `sizeScaleOnScreen` comes from the star's radius. There is no clamp: 0 hides the layer, 1 draws it at the star's full size, and values above 1 push it past the star's edge. Because the star's radius is a per-type field, the same 0.15 is a different absolute size around a white dwarf and a blue giant."),
   T("RotationSpeed","float","Radians per second the layer turns.",
     "It is added to the sprite's rotation every simulation step, so 0.03 (the field's default) is a full turn in about 3.5 minutes and a negative value turns the other way. Vanilla uses -0.001 on every ring, a very slow counter-rotation.",
     "`SunLayerState.Update` runs `Sprite.Rotation += Info.RotationSpeed * timeStep.FixedTime` with the rotation in radians, so a full turn takes 2*pi/speed seconds: 0.03 is about 209 s and 0.001 about 6,283 s. `RotationStart` sets where it begins, generated per layer from its -1 to 1 range. The value is read every frame and is not clamped, so a large number makes the ring spin visibly fast."),
   T("PulsePeriod","float","Seconds in one pulse cycle, or 0 to switch pulsing off.",
     "With a positive value the layer's scale and colour breathe between the PulseScale and PulseColor bounds, one cycle every this many seconds; 0 or less leaves both at full. Vanilla 5.0 on every ring.",
     "`SunLayerState.Update` only enters the pulse branch when `PulsePeriod > 0f`, then computes `Intensity = (1 + sin(PulseTimer/PulsePeriod * TwoPi)) * 0.5` and lerps `PulseScale` and `PulseColor` by it. The field's default is 0, so an omitted value is a static ring. The period is in simulation seconds, not frames, so it holds at any game speed."),
 ]),
 ]),

dict(id="ftl", tier=2, title="FTL effect", paths=["FTL.yaml"], roots=[],
     fmt="YAML", loader="FTLManager.AddHotLoadTarget (FTL.yaml, hot reload)",
     override="One file; can be edited while the game runs.",
     l1="What the warp flash looks like: layers, timing, rotation and scale curves.",
     l2="Each layer is one texture with its own timing. It is presentation only.",
     l3="ScaleCurve points are [time, scale], smoothed; Duration is seconds; Rotation is radians per second.",
     groups=[
 G("Layer", "One visual layer.", "Layers draw in order.", "FrontToBack reverses travel direction.", [
   T("FTLLayer","element","One layer.","", ""),
   T("Texture","string","Layer texture.","", ""),
   T("Duration","float","Seconds.","", ""),
   T("Rotation","float","Radians per second.","", ""),
   T("FrontToBack","bool","Travel direction.","", ""),
   T("DebugGraphColor","int[]","Debug curve colour.","", ""),
   T("ScaleCurve","float[][]","Scale over time.","", ""),
   T("ColorCurve","float[][]","Colour over time.","", ""),
   T("PositionFromLayer","string","Layer whose position the effect follows.","", ""),
 ]),
 ]),

dict(id="explosions", tier=2, title="Explosion effects", paths=["Explosions.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadExplosions",
     override="One file; replaces vanilla.",
     l1="Which visual effect plays for each kind of explosion.",
     l2="Type selects the effect; Path is the texture or atlas, Scale its size.",
     l3="Types are looked up by name from combat code; an unknown type is not used.",
     groups=[
 G("Explosion", "One effect entry.", "Path is relative to Content/.", "Scale multiplies the sprite size.", [
   T("Type","ExplosionType","Which explosion set this entry joins.",
     "A caller passes one of these four values and gets the entries filed under it.",
     "A name that is not one of them is not a set, so the entry cannot be spawned.",
     values=("enum:ExplosionType", EXPLOSION_TYPES)),
   T("Path","string","Effect texture.","", ""),
   T("Scale","float","Size multiplier.","", ""),
 ]),
 ]),

dict(id="mainmenus", tier=2, title="Main menus", paths=["MainMenus.yaml"], roots=[],
     fmt="YAML", loader="MainMenuScreen + YamlParser.Deserialize<MainMenusDescr> (hot reload)",
     override="One file; replaces vanilla.",
     l1="The list of background scenes the main menu can show.",
     l2="Each entry pairs a UI layout with a 3D scene; Default picks the first one.",
     l3="UILayoutFile and SceneFile are paths under UI/, both hot-reloadable.",
     groups=[
 G("Menu entry", "One menu background.", "Default names the entry to open first.", "The layout and the scene are separate files.", [
   T("Default","string","Default menu name.","", ""),
   T("MainMenus","element","Menu list.","", ""),
   T("Name","string","Menu id.","", ""),
   T("UILayoutFile","string","UI layout YAML.","", ""),
   T("SceneFile","string","3D scene YAML.","", ""),
 ]),
 ]),

# ---------------------------------------------------------------- tier 3
dict(id="gametext", tier=3, title="GameText", paths=["GameText.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadLanguage → Localizer.LoadFromYaml",
     shape=("<p>One block per string, keyed by the NameId code looks up, with <code>Id</code> and one line "
            "per language indented under it. The block's key is the name, not a field: the file is read as "
            "<code>Array&lt;LangToken&gt;</code> with <code>NameId</code> as its key name, so a renamed block "
            "is a different string.</p>"),
     override="Merged by NameId: an entry with a vanilla NameId replaces that text and keeps its number; any other NameId adds a string.",
     l1="Every player-visible string the game looks up, in seven languages.",
     l2="A block per string: a NameId, an optional integer Id, and a column per language. A mod ships only the keys it changes and inherits the rest.",
     l3="An entry without Id gets a number after the highest one, so pin Id before another file points at it. A blank column falls back to ENG for that entry; a blank ENG is blank in every language.",
     groups=[
 G("Entry", "The key and the number that reach this string.", "The key is what code calls by name; the number is what content fields store.", "A block with an unknown NameId and no referenced Id is dead weight.", [
   T("NameId","key","The name code passes to Localizer.Token.","Case-sensitive and never translated. A by-name lookup that misses shows the name itself on screen.","e.g. NewGame, CodexControlsSelectingShips."),
   T("Id","int","The number an int field or a {token} stores.","Optional: an omitted id is generated after the highest one, in file order, so it moves when entries are added.","1-99,999 general text; 100,000-199,999 codex."),
 ]),
 G("Translations", "One line per language, English first.", "English is the base every other column falls back to, per entry.", "A blank ENG leaves the string blank in every language.", [
   T("ENG","string","English, the fallback for every other language.","Required in practice: the loader starts from this column whatever the language is.","Set on all 4,011 vanilla entries."),
   T("RUS","string","Russian text.","Used when the game language is Russian.","3,596 vanilla entries set it."),
   T("SPA","string","Spanish text.","Used when the game language is Spanish.","1,973 vanilla entries set it."),
   T("UKR","string","Ukrainian text.","Used when the game language is Ukrainian.","3,321 vanilla entries set it."),
   T("GER","string","German text.","Used when the game language is German.","Only 2 vanilla entries set it."),
   T("PTB","string","Brazilian Portuguese text.","Used when the game language is Portuguese; the file column is PTB.","3,587 vanilla entries set it."),
   T("POL","string","Polish text.","Used when the game language is Polish.","No vanilla entry sets it."),
 ]),
 ]),

dict(id="codex", tier=3, title="Codex and hooks", paths=["Codex.yaml", "CodexHooks.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadBlackboxSpecific",
     shape=("<p>A YAML sequence of entries: each one starts with a line that is only <code>-</code>, and "
            "the indented keys under it are that entry's properties. The <code>UID</code> is the id the "
            "code looks up, not a field of a class, and the article text lives in <code>GameText.yaml</code> "
            "under token ids 100000 and up. The file's own note warns that the inline "
            "<code>- UID: value</code> form drops the first value in this parser, so the dash goes on its "
            "own line.</p>"),
     override="Merged by id; Codex ids are 100000 and up.",
     l1="The in-game encyclopedia entries and the links from game objects to them.",
     l2="Codex.yaml holds the articles; CodexHooks.yaml says which module, tech or concept opens which article.",
     l3="Ids below 100000 are reserved for game text. A hook pointing at a missing id opens nothing.",
     groups=[
 G("Article", "One encyclopedia entry.", "Title and body are plain text with the game's markup.", "Ids must be unique and 100000+.", [
   T("Title","string","Article title.","", ""),
   T("Text","string","Article body.","", ""),
 ]),
 G("Hook", "One link to an article.", "A hook can target many objects with the same id.", "A hook for a missing object is ignored.", [
   T("<object>","int","Codex id for that object.","", ""),
 ]),
 ]),

dict(id="designoutput", tier=3, title="Ships/DesignOutput.xml", paths=["Ships"], ext=".xml", roots=["ShipData"],
     fmt="XML", loader="written by the design exporter; not read as content",
     override="Not a mod override: this is an example of the game's own ship-data writer.",
     l1="A sample of the ship data the game can export, not a file the game loads.",
     l2="It mirrors ShipData: slots, installed module UIDs, position, size and model. Useful as a reference, not as content.",
     l3="If a tool asks for a ship template, this is not it; use a .design plus its hull.",
     groups=[
 G("Exported ship", "The writer's fields.", "Read-only reference.", "Changing it changes nothing in game.", [
   T("Name","string","Ship name.","", ""),
   T("ModuleSlotList","element","Placed modules.","", ""),
   T("InstalledModuleUID","string","Module in a slot.","", ""),
   T("Position","int,int","Slot position.","", ""),
   T("Dimensions","int,int","Hull size.","", ""),
   T("ModelPath","string","Model.","", ""),
   T("TexturePath","string","Texture.","", ""),
   T("DefaultAIState","string","Starting AI order.","", ""),
   T("DeployPosition","int","Deployment position.","", ""),
   T("Loyalty","string","Empire the sample belongs to.","", ""),
   T("ModuleSlotData","element","One placed module.","", ""),
   T("SlotOptions","element","Slot options for the sample.","", ""),
   T("Restrictions","string","Slot restriction of the sample.","", ""),
   T("StrategicIconPath","string","Strategic icon.","", ""),
   T("X","int","Slot x position.","", ""),
   T("Y","int","Slot y position.","", ""),
 ]),
 ]),

# ---------------------------------------------------------------- assets
dict(id="textures", tier=3, title="Textures", paths=["Textures"], roots=[],
     fmt="PNG, DDS, atlas folders", loader="ResourceManager.Texture / LoadTextureAtlases",
     override="Relative path for images (.png/.dds); an .atlas folder replaces the whole atlas.",
     l1="Every image the UI and the world draw. Mods replace them by putting a file at the same relative path.",
     l2="PNG and DDS both load; DDS is used for big ship and planet art. A missing texture logs a warning and draws a red placeholder instead of crashing.",
     l3="Names are looked up without extension under Textures/. Atlas folders have a .atlas file naming their sprites. Replacing one frame means replacing the folder, not one PNG.",
     groups=[
 G("Image", "One texture file.", "Same relative path wins; extension may differ if the loader probes both.", "UI atlases are compiled and must keep their frame names.", [
   T(".png",".png","Lossless image, fine for UI and icons.","", ""),
   T(".dds",".dds","Compressed texture for large art.","", ""),
   T(".atlas",".atlas","Atlas manifest for a sprite folder.","", ""),
 ]),
 ]),

dict(id="models", tier=3, title="Models", paths=["Model"], roots=[],
     fmt="FBX, OBJ, MTL, DDS", loader="MeshImporter / RawContentLoader",
     override="Relative path; hulls and weapons reference the path without extension.",
     l1="The 3D meshes for ships, stations, projectiles and planet parts.",
     l2="FBX and OBJ both load; MTL carries OBJ materials. Ship textures are usually DDS next to the model.",
     l3="A hull's ModelPath and a weapon's ModelPath are the references. A missing mesh logs and the object may draw as a placeholder.",
     groups=[
 G("Mesh file", "One model or material.", "Paths are relative to Content/.", "Do not rename a shared mesh another hull still points at.", [
   T(".fbx",".fbx","Binary mesh, the common ship format.","", ""),
   T(".obj",".obj","Text mesh, used for planets and simple parts.","", ""),
   T(".mtl",".mtl","OBJ material list.","", ""),
   T(".dds",".dds","Texture beside a mesh.","", ""),
 ]),
 ]),

dict(id="audio", tier=3, title="Audio", paths=["Audio"], roots=[],
     fmt="M4A, MP3, WAV, AAC, AIF + AudioConfig.yaml", loader="GameAudio → AudioConfig(Audio/AudioConfig.yaml)",
     shape=("<p><code>AudioConfig.yaml</code> is the parsed file: a list of <code>- Category:</code> blocks, "
            "each with a <code>Name</code>, a <code>Volume</code> and a list of <code>- SoundEffect:</code> "
            "items. Each item carries an <code>Id</code>, a <code>Volume</code> and the file that plays. The "
            "sound files beside it are named from those cues and replace by relative path.</p>"),
     override="AudioConfig.yaml merges by category and sound id; sound files replace by relative path.",
     l1="Music and sound effects, plus one config that names volumes and which file plays for each cue.",
     l2="A mod can override a single cue without copying the whole audio folder. Supported formats are listed in the config header.",
     l3="A SoundEffect entry has an Id, a Volume and either Sound (one file) or Sounds (a random list). A missing file is a log warning and silence.",
     groups=[
 G("Cue", "One sound in the config.", "Ids are what code passes to the audio system.", "Prefer compressed formats to keep memory down.", [
   T("Id","string","Cue id.","", ""),
   T("Sound","string","One file for the cue.","", ""),
   T("Sounds","string[]","Files chosen at random.","", ""),
   T("Volume","float","Per-cue volume.","", ""),
 ]),
 G("Category", "A group of cues.", "Categories carry a default volume and fade time.", "Music, UI and combat are separate categories.", [
   T("Name","string","Category name.","", ""),
   T("Volume","float","Category volume.","", ""),
   T("FadeOutTime","float","Fade seconds when stopped.","", ""),
   T("SoundEffects","element","The cues in this category.","", ""),
   T("MaxConcurrent","int","Most instances of one cue at once.","", ""),
   T("MaxConcurrentSounds","int","Most sounds overall.","", ""),
   T("MaxConcurrentSoundsPerEffect","int","Most instances per cue.","", ""),
   T("MaxSoundsPerFrame","int","Sounds started in one frame.","", ""),
   T("MemoryCache","bool","Keep the sound cached.","", ""),
 ]),
 ]),

dict(id="particles", tier=3, title="Particles and shaders", paths=["3DParticles", "Effects"], roots=[],
     fmt="YAML, PNG, FX, MGFX, MGFXO, XNB", loader="Particle.LoadParticleEffect → ParticleEffect",
     shape=("<p>The folder is mixed, and only one part is a schema. <code>3DParticles/ParticleEffects.yaml</code> "
            "is parsed into named particle effects, so the keys inside an effect are fields that bind by name. "
            "PNG textures are picked up by name from the paths that YAML writes. The compiled shaders in "
            "<code>Effects/</code> are loaded by hardcoded name as <code>.mgfxo</code> or <code>.xnb</code>, so a "
            "shader is replaced by file, never by a key.</p>"),
     override="YAML by name; textures by relative path. Shaders must be compiled for the current pipeline.",
     l1="The engine's particle looks and the shaders that draw beams, shields, fog and the warp effect.",
     l2="Particle YAML plus PNG textures make most effects. Shaders are compiled artefacts; replacing a .fx alone does nothing at runtime.",
     l3="The game loads compiled .mgfxo/.xnb effects by hardcoded name (Simple, MeshLighting, SkinnedEffect, BeamFX, Distort). A missing one is fatal, not a placeholder.",
     groups=[
 G("Particle YAML", "Named particle effects.", "Hot-reloadable.", "ParticleEffects.yaml references textures and shader names.", [
   T("Particles.yaml","file","Particle definitions.","", ""),
   T("ParticleEffects.yaml","file","Effect presets.","", ""),
 ]),
 G("Shader artefact", "A compiled effect.", "Must match the current MonoGame build.", "Source .fx is not read at runtime; .mgfxo is.", [
   T(".fx",".fx","Shader source, for editing.","", ""),
   T(".mgfx",".mgfx","Compiled MonoGame effect.","", ""),
   T(".mgfxo",".mgfxo","OpenGL-compiled effect, loaded by name.","", ""),
   T(".xnb",".xnb","Legacy compiled effect, still loaded.","", ""),
 ]),
 G("Particle fields", "The keys inside one particle effect.", "Most are visual; a few change the simulation.", "A misspelled key is silently ignored by the particle loader.", [
   T("Name","string","Effect name.","", ""),
   T("Effect","string","Effect preset name.","", ""),
   T("TextureName","string","Particle texture.","", ""),
   T("Emitters","element","Emitter list.","", ""),
   T("Particle","element","One particle definition.","", ""),
   T("Duration","float","Emitter lifetime in seconds.","", ""),
   T("DurationRandomness","float","Random variation in lifetime.","", ""),
   T("Rate","float","Particles per second.","", ""),
   T("MaxParticles","int","Particle cap.","", ""),
   T("Scale","float","Particle size.","", ""),
   T("StartEndSize","float[]","Size at birth and death.","", ""),
   T("StartColorRange","float[]","Colour range at birth.","", ""),
   T("EndColorRange","float[]","Colour range at death.","", ""),
   T("EndColorTime","float","When the end colour is reached.","", ""),
   T("ColorSource","ColorSource","Which colour the particles start with.",
     "Default keeps the emitter's own colour; the other three read it from the owning empire.",
     "The value is only applied when it is not Default and a loyalty is present.",
     values=("enum:ColorSource", PARTICLE_COLORS)),
   T("LocalOffset","float[]","Offset from the emitter.","", ""),
   T("Velocity","float[]","Initial velocity.","", ""),
   T("EndVelocity","float[]","Velocity at death.","", ""),
   T("RandomVelocityXY","float[]","Random velocity spread.","", ""),
   T("PositionIncrements","float[]","Spawn position spread.","", ""),
   T("AlignRandomVelocityXY","bool","Align to random velocity.","", ""),
   T("AlignRotationToVelocity","bool","Point along travel.","", ""),
   T("RotateSpeed","float","Particle spin.","", ""),
   T("InheritOwnerVelocity","bool","Add the emitter's motion.","", ""),
   T("InheritSprayVelocity","bool","Add the spray velocity.","", ""),
   T("RandomizedSpray","bool","Randomise the spray.","", ""),
   T("RandomizedSprayParticles","int","Particles in a spray burst.","", ""),
   T("OnlyNearView","bool","Only simulate near the camera.","", ""),
   T("Static","bool","Do not move the emitter.","", ""),
   T("SrcDstBlend","string","Blend mode pair.","", ""),
 ]),
 ]),

dict(id="fonts", tier=3, title="Fonts", paths=["Fonts"], roots=[],
     fmt="SpriteFont, XNB, TTF, OTF", loader="Fonts.LoadFonts (XNB font assets)",
     override="Fonts are loaded by name from code; a missing font throws rather than falling back.",
     l1="The typefaces the UI uses. These are the files most likely to break a stripped-down mod.",
     l2="The .spritefont files are sources; the game loads the compiled .xnb beside them. Keep the pairs together.",
     l3="Do not delete a font a layout names. If you add a font, add both the source and the compiled XNB, or the content build will not produce it.",
     groups=[
 G("Font file", "One typeface or its compiled form.", "Names are referenced from UI code and layouts.", "A missing XNB is a startup failure when that font is first used.", [
   T(".spritefont",".spritefont","Source description (family, size, style).","", ""),
   T(".xnb",".xnb","Compiled font the game loads.","", ""),
   T(".ttf/.otf",".ttf/.otf","Raw typeface used by the source.","", ""),
 ]),
 ]),

dict(id="ui", tier=3, title="UI layouts and menu scenes", paths=["UI"], roots=[],
     fmt="YAML (layout and scene)", loader="LayoutParser / SceneInstance (hot reload)",
     shape=("<p>Two shapes share the folder. A layout (<code>*.yaml</code>) is a tree: each element is a "
            "block with an id, a position and a size, and the code looks elements up by id, so the ids are "
            "the interface. A scene (<code>*.scene.yaml</code>) is one flat block of camera, sun and ambient "
            "values. Both are hot-reloadable, so an edit appears without a restart.</p>"),
     override="Files replace by name; both are hot-reloadable.",
     l1="Where the buttons sit and what the 3D main-menu background looks like.",
     l2="Layouts are a tree of elements with positions and sizes; scenes set camera, sun and ambient light.",
     l3="Sizes use virtual coordinates; AbsSize 0 auto-fits the texture. Elements are found by id from code, so renaming one breaks its behaviour.",
     groups=[
 G("Layout", "One screen's element tree.", "Positions are virtual pixels or relative to the parent.", "Hardcoded ids (buttons, panels) must keep their names.", [
   T("Name","string","Layout id.","", ""),
   T("VirtualSize","int,int","Virtual resolution.","", ""),
   T("Elements","element","Element tree.","", ""),
   T("Groups","element","Element groups.","", ""),
 ]),
 G("Scene", "The 3D backdrop.", "Camera and lighting only.", "AmbientIntensity 0 makes the scene black.", [
   T("CameraPos","float[]","Camera position.","", ""),
   T("LookAt","float[]","Camera target.","", ""),
   T("SunPos","float[]","Sun position.","", ""),
   T("SunColor","float[]","Sun colour.","", ""),
   T("SunIntensity","float","Sun strength.","", ""),
   T("AmbientColor","float[]","Ambient colour.","", ""),
   T("AmbientIntensity","float","Ambient strength.","", ""),
 ]),
 G("Element attributes", "The keys an element in the tree can carry.", "Positions are virtual pixels or relative to the parent; ids are found by code.", "A renamed id still draws but loses its hardcoded behaviour.", [
   T("AI","bool","Element is laid out automatically.","", ""),
   T("AbsPos","int[]","Absolute position.","", ""),
   T("AbsSize","int[]","Absolute size; 0 auto-fits.","", ""),
   T("Alpha","float","Opacity.","", ""),
   T("Animation","string","Animation name.","", ""),
   T("Animations","element","Animation list.","", ""),
   T("AxisAlign","string","Alignment within the parent.","", ""),
   T("ButtonStyle","ButtonStyle","Which button skin the layout asks for.",
     "The style picks the normal, hover and pressed textures, and Text draws no background.",
     "A name that is not a member of the enum is not a style and the button falls back to the default.",
     values=("enum:ButtonStyle", BUTTON_STYLES)),
   T("CenterScale","float","Scale about the centre.","", ""),
   T("Children","element","Child elements.","", ""),
   T("ClickSfx","string","Click sound.","", ""),
   T("Color","float[]","Tint.","", ""),
   T("Delay","float","Delay before showing.","", ""),
   T("DisableJumpSfx","bool","Mute the jump sound.","", ""),
   T("DiverseShipEmpires","bool","Show several empire colours.","", ""),
   T("DrawDepth","float","Draw order.","", ""),
   T("Duration","float","Animation duration.","", ""),
   T("DustTrails","bool","Draw dust trails.","", ""),
   T("Empire","bool","Tint with the empire colour.","", ""),
   T("EngineTrails","bool","Draw engine trails.","", ""),
   T("FreezeAtLastFrame","bool","Stop on the last frame.","", ""),
   T("ListLayout","string","List layout mode.","", ""),
   T("LocalAxis","string","Local alignment axis.","", ""),
   T("LocalPos","int[]","Position relative to the parent.","", ""),
   T("Looping","bool","Loop the animation.","", ""),
   T("MaxColor","float[]","Maximum tint.","", ""),
   T("MinColor","float[]","Minimum tint.","", ""),
   T("ObjectGroups","element","3D object groups.","", ""),
   T("Objects","element","3D objects.","", ""),
   T("Padding","int[]","Inner padding.","", ""),
   T("Params","map","Extra parameters.","", ""),
   T("ParentAlign","string","Origin within the parent.","", ""),
   T("Path","string","Asset path.","", ""),
   T("RelPos","float[]","Relative position 0-1.","", ""),
   T("RelSize","float[]","Relative size 0-1.","", ""),
   T("SpriteAnim","string","Sprite animation.","", ""),
   T("StartAt","float","Animation start time.","", ""),
   T("Texture","string","Background texture.","", ""),
   T("Title","string","Window title.","", ""),
   T("Visible","bool","Shown at start.","", ""),
   T("VisibleBeforeDelay","bool","Show during the delay.","", ""),
 ]),
 ]),

dict(id="miscassets", tier=3, title="Loading screens, cursors, flags, tutorials, video", paths=["LoadingScreen", "Cursors", "Flags", "Tutorials", "Video"], roots=[],
     fmt="XNB, PNG, WMV", loader="ResourceManager.LoadRandomLoadingScreen / LoadVideo; TutorialScreen; flags by FlagIndex",
     override="Relative path; these are presentation assets with few hardcoded names.",
     l1="The remaining presentation folders: loading art, mouse cursors, empire flags, tutorial slides and intro videos.",
     l2="Most are looked up by index or folder, so adding files is safe and deleting one degrades that screen.",
     l3="Flags are indexed by FlagIndex in a race file; reordering the folder changes which flag a race gets. Tutorials and videos are compiled XNB plus source.",
     groups=[
 G("Asset folders", "What each folder holds.", "A missing file degrades or skips that screen.", "Flag order is meaningful.", [
   T("LoadingScreen","xnb","Loading art.","", ""),
   T("Cursors","png","Mouse cursors.","", ""),
   T("Flags","png","Empire flags, indexed by FlagIndex.","", ""),
   T("Tutorials","xnb","Tutorial slides per language.","", ""),
   T("Video","wmv/xnb","Intro and race videos.","", ""),
 ]),
 ]),

dict(id="mgcb", tier=3, title="Content.mgcb", paths=["Content.mgcb"], roots=[],
   fmt="MonoGame content manifest", loader="MonoGame content pipeline at build time",
   shape=("<p><code>Content.mgcb</code> is a MonoGame build manifest, not a runtime file: it lists which "
          "fonts, effects, videos and tutorials the content pipeline compiles into the <code>.xnb</code> "
          "and <code>.mgfxo</code> files the game loads. A new font or shader needs an entry here; the game "
          "reads the compiled output and never the manifest.</p>"),
   override="Not runtime content; a mod does not need one unless it ships compiled XNB assets.",
   l1="The build manifest that tells the content pipeline how to compile fonts, effects, videos and tutorials.",
   l2="It is read when the game is built, not when it runs. Editing it changes the build, not a running game.",
   l3="Most data files are copied rather than compiled. If you add a .spritefont or .fx, it needs an entry here to produce an XNB/MGFXO.",
   groups=[
 G("Build entry", "One compile rule.", "Paths and importer/processor names.", "A missing entry means no compiled output.", [
   T("build",".mgcb","Compile an asset.","", ""),
 ]),
 ]),

]
