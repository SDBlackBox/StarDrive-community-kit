"""Tier 2, tier 3 and asset families for the moddable-content page.

Same shape as moddable-data.py. Kept separate so the ship-data half stays readable.
"""

G = lambda title, l1, l2, l3, tags: dict(title=title, l1=l1, l2=l2, l3=l3, tags=tags)
T = lambda name, ty, l1, l2="", l3="", **kw: dict(name=name, ty=ty, l1=l1, l2=l2, l3=l3, **kw)

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

dict(id="goods", tier=2, title="Goods", paths=["Goods"], ext=".xml", roots=["Good"],
     fmt="XML + one YAML", loader="ResourceManager.LoadGoods",
     override="XML unifies by file name; Goods/Goods.yaml is the transportable-goods list.",
     l1="A physical commodity that freighters move between colonies.",
     l2="Goods have mass and cost and use cargo space. Goods.yaml lists which goods are transported automatically.",
     l3="Only goods marked cargo and listed in Goods.yaml enter the freight network. Icons resolve from IconTexturePath or the good's name.",
     notation=dict(title="Copy this: a good, and its freight entry", body="""
<p>One XML file per good, plus one block in <code>Goods/Goods.yaml</code> if freighters should move it:</p>
<pre class="code">&lt;Good&gt;
  &lt;Name&gt;Colonists in Stasis Pods&lt;/Name&gt;
  &lt;UID&gt;Colonists_1000&lt;/UID&gt;
  &lt;Mass&gt;1&lt;/Mass&gt;
  &lt;Description&gt;People, packed for the journey.&lt;/Description&gt;
&lt;/Good&gt;</pre>
<pre class="code">Good:
  UID: Production
  RefiningRatio: 1
  MaxRichness: 6
  Weight: 1</pre>
<ul>
<li><b>UID</b> is the id and also the texture name: <code>Textures/Goods/&lt;UID&gt;</code> unless <code>IconTexturePath</code> overrides it.</li>
<li>The YAML entry is the transport list. A good with no block there exists in the game but is never shipped, which looks like freight ignoring it.</li>
<li><code>Weight</code> sets how common the resource is for mining; <code>MaxRichness</code> caps the deposit richness it can generate.</li>
</ul>"""),
     groups=[
 G("Good fields", "What one good is worth and weighs.", "Mass limits how much a freighter can carry; Cost is its value.", "Description is plain text, not a localisation id.", [
   T("UID","string","Good id.","", ""),
   T("Name","string","Display name.","", ""),
   T("Mass","float","Mass per unit.","", ""),
   T("Cost","float","Value per unit.","", ""),
   T("IsCargo","bool","Moves through freight.","", ""),
   T("IconTexturePath","string","Icon.","", ""),
   T("Description","string","Tooltip.","", ""),
 ]),
 G("Goods.yaml", "The transport list.", "One entry per good the freight AI may move.", "A good absent here exists but is never shipped.", [
   T("Good","element","A transportable good entry.","", ""),
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
   T("PreferredEnv","enum","Preferred planet type.","", ""),
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

dict(id="racialtraits", tier=2, title="Racial traits", paths=["RacialTraits"], ext=".xml", roots=["RacialTraits", "TraitList"],
     fmt="XML", loader="ResourceManager.LoadRaceTraits → RacialTraitOption",
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
   T("PreferredEnv","enum","Preferred planet category.","", ""),
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

dict(id="diplomacy", tier=2, title="Diplomatic traits", paths=["Diplomacy"], ext=".xml", roots=["DiplomaticTraits", "DiplomaticTraitsList"],
     fmt="XML", loader="ResourceManager.LoadDiplomacyTraits",
     override="One file. Name is the personality id a race's DiplomaticPersonality refers to.",
     l1="A diplomatic personality: how trusting, opportunistic or aggressive a people is.",
     l2="These values set the starting relationship and how fast it drifts. They are separate from racial traits, though both use the word trait.",
     l3="DTrait and ETrait are the diplomatic and economic personality lists; a race names one of each in Races/.",
     groups=[
 G("Personality", "The two lists a race can choose from.", "DTrait is diplomatic, ETrait is economic.", "Weights and modifiers are read when relations change.", [
   T("DTrait","element","Diplomatic personality entry.","", ""),
   T("ETrait","element","Economic personality entry.","", ""),
   T("Name","string","Personality id.","", ""),
   T("Description","int","Localisation id.","", ""),
   T("Alliance","float","Willingness to ally.","", ""),
   T("NAPact","float","Willingness to sign a non-aggression pact.","", ""),
   T("Trade","float","Willingness to trade.","", ""),
   T("Trustworthiness","float","How much trust is kept.","", ""),
   T("TrustGainedAtPeace","float","Trust gained per peaceful turn.","", ""),
   T("Opportunism","float","Willingness to exploit weakness.","", ""),
   T("Territorialism","float","Sensitivity to border pressure.","", ""),
   T("AngerDissipation","float","How fast anger fades.","", ""),
   T("NaturalRelChange","float","Baseline relation drift.","", ""),
   T("PowerIncrease","float","Weight given to power growth.","", ""),
   T("WeaknessDecline","float","Weight given to weakness.","", ""),
   T("EconomicResearchStrategy","string","Economic strategy id.","", ""),
   T("ColonyGoalsPlus","float","Extra colony ambition.","", ""),
   T("ShipGoalsPlus","float","Extra fleet ambition.","", ""),
   T("EconomicTraitsList","element","Container for the economic personality list.","", ""),
 ]),
 ]),

dict(id="solarsystems", tier=2, title="Solar systems", paths=["SolarSystems"], ext=".xml", roots=["SolarSystemData"],
     fmt="XML", loader="ResourceManager.LoadSolarSystems (GatherFilesModOrVanilla for Random/)",
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
     fmt="XML per language", loader="ResourceManager.LoadDiplomacyDialogs",
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
     fmt="XML", loader="ResourceManager.LoadPlanetEdicts",
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
     fmt="plain text", loader="ResourceManager.LoadShipNames / spy-name loaders",
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
     fmt="XML per language", loader="ResourceManager.LoadAdvice",
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
     fmt="XML", loader="ResourceManager.LoadMilitaryStrategies",
     override="XML unifies by file name; Name is the strategy id.",
     l1="A named research order for the AI's military, split by weapon and hull path.",
     l2="The AI follows one path (beam, kinetic, missile, energy, hull) and researches the techs listed for it.",
     l3="Each Tech entry has an id and a path element; the order in the file is the order it researches.",
     groups=[
 G("Strategy", "The paths and the techs in them.", "A path with no techs leaves the AI without a plan.", "Tech ids must exist; a missing one is skipped.", [
   T("Name","string","Strategy id.","", ""),
   T("BeamPath","element","Beam tech list.","", ""),
   T("KineticPath","element","Kinetic tech list.","", ""),
   T("MissilePath","element","Missile tech list.","", ""),
   T("EnergyPath","element","Energy tech list.","", ""),
   T("HullPath","element","Hull tech list.","", ""),
   T("Tech","element","One tech entry.","", ""),
   T("id","string","Tech UID.","", ""),
   T("DefensePath","element","Defence tech list.","", ""),
 ]),
 ]),

# ---------------------------------------------------------------- tier 2 YAML tuning
dict(id="research", tier=2, title="Research weights", paths=["Research.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadResearchOptionSettings",
     override="One file; a mod's file replaces it, not merges per key.",
     l1="How expensive each research area is, per race and per hull or weapon type.",
     l2="Weights multiply the tech's own Cost. A race can be cheaper at weapons and dearer at colonization without touching the tree.",
     l3="The file is a list of ResearchSettings keyed by PortraitName; All applies first.",
     groups=[
 G("Cost weights", "The multipliers.", "1 is neutral; 0.5 halves the price.", "Weapon and hull weights are selected by tag.", [
   T("PortraitName","string","Race the block applies to; All is the base.","", ""),
   T("TechnologyTypeModifiers","map","Cost per technology branch.","", ""),
   T("ShipCostModifiers","map","Cost per hull class.","", ""),
   T("ResearchAreaModifiers","map","Cost per research area.","", ""),
   T("WeaponModifiers","map","Cost per weapon tag.","", ""),
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
   T("CanBuild","string","Build tier this block applies to.","One of CanBuildFighters, CanBuildCorvettes, CanBuildFrigates, CanBuildCruisers, CanBuildBattleships or CanBuildCapitals. The AI takes the highest tier it can build.", ""),
   T("Fighters","int","Fighter count, low then high.","", ""),
   T("Corvettes","int","Corvette count, low then high.","", ""),
   T("Frigates","int","Frigate count, low then high.","", ""),
   T("Cruisers","int","Cruiser count, low then high.","", ""),
   T("Battleships","int","Battleship count, low then high.","", ""),
   T("Capitals","int","Capital count, low then high.","", ""),
   T("TroopShips","int","Troop ship count, low then high.","", ""),
   T("Bombers","int","Bomber count, low then high.","", ""),
   T("Carriers","int","Carrier count, low then high.","", ""),
   T("Support","int","Support ship count, low then high.","", ""),
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
   T("Name","string","Strategy id.","", ""),
   T("MilitaryPriority","float","Military weighting.","", ""),
   T("ExpansionPriority","float","Expansion weighting.","", ""),
   T("ResearchPriority","float","Research weighting.","", ""),
   T("IndustryPriority","float","Industry weighting.","", ""),
   T("TechPath","string[]","Preferred techs.","", ""),
 ]),
 ]),

dict(id="planettypes", tier=2, title="Planet types", paths=["PlanetTypes.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.PlanetTypes",
     override="One file; a mod's file replaces it.",
     l1="The catalogue of planet looks and stats: what a Terran, ice or volcanic world is like.",
     l2="Each type sets rendering meshes and textures, habitability, population per tile and fertility. Solar systems pick a type by index.",
     l3="Type entries are indexed by order, and WhichPlanet in a solar system is that index. Reordering Types rewrites every reference.",
     groups=[
 G("Globals", "Meshes and scales shared by all types.", "Paths are relative to Content/.", "NewRenderer is a work-in-progress switch; leave it false.", [
   T("PlanetScale","float","Base planet scale.","", ""),
   T("RingsScale","float","Ring scale.","", ""),
   T("CloudsScale","float","Cloud layer scale.","", ""),
   T("AtmosphereScale","float","Atmosphere scale.","", ""),
   T("HaloScale","float","Halo scale.","", ""),
   T("GlowScale","float","Glow scale.","", ""),
   T("PlanetMesh","string","Shared planet mesh.","", ""),
   T("RingsMesh","string[]","Ring mesh and texture.","", ""),
   T("GlowEffect","string[]","Glow mesh and texture.","", ""),
   T("FresnelEffect","string[]","Fresnel mesh and texture.","", ""),
   T("NewRenderer","bool","Use the experimental renderer.","", ""),
   T("AtmosphereTypes","map","Atmosphere presets.","", ""),
 ]),
 G("A planet type", "One entry in Types.", "The index is the WhichPlanet value solar systems use.", "Diffuse/normal/emissive maps are texture paths.", [
   T("Id","string","Type id.","", ""),
   T("Name","string","Display name.","", ""),
   T("Category","enum","Terran, ice, volcanic, gas, barren.","", ""),
   T("AmbientCues","string[]","Ambient sounds.","", ""),
   T("Composition","string","Flavour composition.","", ""),
   T("IconPath","string","Colony icon.","", ""),
   T("DiffuseMap","string","Colour texture.","", ""),
   T("SpecularMap","string","Specular texture.","", ""),
   T("NormalMap","string","Normal map.","", ""),
   T("EmissiveMap","string","Emissive map.","", ""),
   T("SpecularPower","float","Specular strength.","", ""),
   T("AtmosphereType","string","Atmosphere preset id.","", ""),
   T("Habitable","bool","Can be colonised.","", ""),
   T("HabitableTileChance","float","Share of tiles that are habitable.","", ""),
   T("PopPerTile","float","Population per tile.","", ""),
   T("BaseFertility","float","Starting fertility.","", ""),
   T("MoonTypes","int[]","Allowed moon types.","", ""),
   T("ResearchableChance","float","Chance of a research bonus.","", ""),
   T("MinBaseFertility","float","Fertility floor.","", ""),
   T("Scale","float","Type-specific scale.","", ""),
   T("PlanetTile","string","Surface tile texture.","", ""),
   T("MiningChance","float","Chance of minerals.","", ""),
   T("Types","element","The list of planet types.","Order is the index WhichPlanet uses.", ""),
 ]),
 ]),

dict(id="suns", tier=2, title="Sun types", paths=["Suns.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadSunTypes",
     override="One file; replaces vanilla.",
     l1="The catalogue of stars: colour, light, size and whether they damage ships.",
     l2="A solar system's SunPath names one of these Ids. Radiation is a real damage zone, not decoration.",
     l3="Layers are the visual shells; IconLayer picks the map icon. RadiationRadius is in game units.",
     groups=[
 G("Sun", "One star type.", "Ids are what SunPath references.", "ResearchableChance affects generated systems, not hand-placed ones.", [
   T("Id","string","Sun type id.","", ""),
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
   T("BlendMode","string","Layer blend mode.","", ""),
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

dict(id="dyson", tier=2, title="Dyson rings", paths=["DysonRings.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadDysonRings",
     override="One file; replaces vanilla.",
     l1="The stages of a Dyson ring and what each stage produces.",
     l2="A ring upgrades through Types in order; each type lists its rings and output.",
     l3="Type is the upgrade level; Rings is the visual/mechanical set for it.",
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
<li><b>Type</b> is the upgrade stage, and the file repeats the block for each stage; a missing stage stops progression past it.</li>
<li><code>TexturePath</code> is relative to <code>Textures/</code>. Keep the layer count and order, and swap the image for a retexture.</li>
<li><code>PulsePeriod</code> is in seconds; <code>RotationSpeed</code> is radians per second, so a negative value turns the layer the other way.</li>
</ul>"""),
     groups=[
 G("Ring type", "One upgrade stage.", "Order in the file is the upgrade order.", "A missing stage stops progression.", [
   T("Type","int","Upgrade level.","", ""),
   T("Rings","map","Ring definitions for the level.","", ""),
   T("TexturePath","string","Ring texture.","", ""),
   T("BlendMode","string","Blend mode.","", ""),
   T("LayerScale","float","Layer scale.","", ""),
   T("RotationSpeed","float","Rotation speed.","", ""),
   T("PulsePeriod","float","Pulse cycle seconds.","", ""),
 ]),
 ]),

dict(id="ftl", tier=2, title="FTL effect", paths=["FTL.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadFTLData (hot reload)",
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
   T("Type","string","Explosion type id.","", ""),
   T("Path","string","Effect texture.","", ""),
   T("Scale","float","Size multiplier.","", ""),
 ]),
 ]),

dict(id="mainmenus", tier=2, title="Main menus", paths=["MainMenus.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadMainMenus (hot reload)",
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
     override="Merged by id: the mod's text overrides vanilla per key, other keys stay.",
     l1="Every player-visible string the game looks up by id, in every language.",
     l2="One big map of id to text. A mod only needs the keys it changes; the rest are inherited.",
     l3="Keys are the ids code passes to LocalizedText or GameText. NameIndex and DescriptionIndex fields point at numeric ids, not keys.",
     groups=[
 G("String id", "One id and its text.", "Only the languages present are overridden.", "Unknown ids are harmless; missing ids show the id or blank.", [
   T("<id>","string","The text for one id.","", ""),
 ]),
 ]),

dict(id="codex", tier=3, title="Codex and hooks", paths=["Codex.yaml", "CodexHooks.yaml"], roots=[],
     fmt="YAML", loader="ResourceManager.LoadBlackboxSpecific",
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
     fmt="PNG, DDS, atlas folders", loader="ResourceManager.Texture / LoadTextureAtlas",
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
     fmt="M4A, MP3, WAV, AAC, AIF + AudioConfig.yaml", loader="GameAudio / ResourceManager.LoadAudioConfig",
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
     fmt="YAML, PNG, FX, MGFX, MGFXO, XNB", loader="ParticleEffect / shader loaders",
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
   T("ColorSource","string","Where colour comes from.","", ""),
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
     fmt="SpriteFont, XNB, TTF, OTF", loader="Content pipeline + UI text renderers",
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
   T("ButtonStyle","string","Button skin.","", ""),
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
     fmt="XNB, PNG, WMV", loader="LoadingScreen / CursorManager / Flag / Tutorial / Video players",
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
