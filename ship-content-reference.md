# Ship content reference — data files → code

How the ship-related content files under `game/Content` are read, what every field does, and the
formulas the game derives from them (strength, cost, mass, speed, power, role, research cost).

**Who this is for.** Modders writing `.hull`, module/weapon/tech XML and `.design` files; and
developers who need to know which code owns a number before changing it. It is written to be read
top-to-bottom once, then used as a lookup.

**Pinned to** commit `f575899f` (2026-11-10). Every source link is a permalink to that commit, so
line numbers stay correct even as `main` moves. When you change one of the referenced methods,
update the link and the formula here in the same PR — this document is the map, and a stale map is
worse than none.

**Not covered here:** mesh/texture pipelines, the AI that picks designs, combat resolution. This is
the data model and the numbers that can be computed from it before a ship ever spawns.

- Companion docs: [`ARCHITECTURE.md`](../../ARCHITECTURE.md) (engine/solution layout),
  [`docs/code-findings.md`](../code-findings.md) (known code problems, not the data model).
- Developer conventions and agent instructions: [`AGENTS.md`](../../AGENTS.md).

---

## Contents

1. [The five content types, and who loads them](#1-the-five-content-types-and-who-loads-them)
2. [`.hull` — a hull and its slots](#2-hull--a-hull-and-its-slots)
3. [Module XML — `ShipModules/`](#3-module-xml--shipmodules)
4. [Weapon XML — `Weapons/`](#4-weapon-xml--weapons)
5. [Tech XML — `Technology/`](#5-tech-xml--technology)
6. [`.design` — a ship built on a hull](#6-design--a-ship-built-on-a-hull)
7. [Derived numbers and their formulas](#7-derived-numbers-and-their-formulas)
8. [Invariants that break a design silently](#8-invariants-that-break-a-design-silently)
9. [Reading a design without the game](#9-reading-a-design-without-the-game)

---

## 1. The five content types, and who loads them

| Folder | Files | Format | Loader | In-memory type |
|---|---|---|---|---|
| `Hulls/` | 125 | `.hull` (custom text) | [`ShipHull.Load`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipHull.cs#L751), driven by [`ResourceManager.LoadHulls`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Data/ResourceManager.cs#L1737) | `ShipHull` |
| `ShipModules/` | 199 | XML | [`ResourceManager.LoadShipModules`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Data/ResourceManager.cs#L1627) (`XmlSerializer` over `ShipModule_XMLTemplate`) | `ShipModule` template (+ `ShipModuleFlyweight`) |
| `Weapons/` | 95 | XML | [`ResourceManager.LoadWeapons`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Data/ResourceManager.cs#L2123) | `WeaponTemplate` → `Weapon` at runtime |
| `Technology/` | 190 | XML | [`ResourceManager.LoadTechs`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Data/ResourceManager.cs#L2071) | `Technology` |
| `ShipDesigns/` | 1334 | `.design` (custom text) | [`ShipDesign.ParseDesign`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipDesign_WriterParser.cs#L112) | `ShipDesign` |

**The folder decides the type, not the file.** All five walk the same content root
([`GatherFilesUnified`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Data/ResourceManager.cs#L531)),
which merges the mod directory over vanilla, so a mod overrides a file by using the same
**UID**, not the same path. Two files claiming one UID is a load-order bug, not an error.

**UIDs are the join keys.** A `.design` names a hull by `HullName` and modules by `ModuleUID`.
A module names a weapon by `WeaponType`. No `.design` or `.hull` field names a tech — research
requirements are derived (see §5.3). That asymmetry is why a design can look complete and still be
unbuildable.

**Load order that matters:**

```
ShipModules/*.xml  →  ModuleTemplates[uid]        (a module needs its WeaponType to exist)
Weapons/*.xml      →  WeaponsDict[uid]            (weapon templates, then InitializeTemplate)
Technology/*.xml   →  TechsList, LeadsTo/ComesFrom resolved
Hulls/*.hull       →  HullsDict[HullName]
ShipDesigns/*.design → ShipDesign + InitializeCommonStats
then ShipDesignUtils.MarkDesignsUnlockable()      → fills every TechsNeeded (§5.3)
```

---

## 2. `.hull` — a hull and its slots

A hull is the **grid** a design is built on: a bounding `Size`, the set of cells that can hold a
module and what kind of module each accepts, plus the visual model.

Format: `Key=Value` lines until a bare `Slots` line; everything after is the slot grid, one row per
line. `#` starts a comment; comments before `Slots` are kept and written back on save.

### 2.1 Header fields

Every key below is read by the `switch` inside
[`ShipHull.Load`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipHull.cs#L751).
Keys it does not recognise are skipped without a warning.

| Field | Type | Meaning / effect |
|---|---|---|
| `Version` | int | Format version, currently `1`. Mismatch logs a warning only. |
| `HullName` | string | **The UID.** `<Style>/<Name>`, e.g. `Terran/Battleship`. Designs reference this. |
| `VisibleName` | string | UI name. |
| `Role` | `RoleName` | Hull class — `fighter` … `capital`, `freighter`, `platform`, `station`, `shipyard`. Drives role derivation (§7.5) and which modules are legal (module `*Module` flags). |
| `ModName` | string | `""` = vanilla. Used to disable a hull when its mod is not loaded. |
| `Description`, `Style` | string | Flavour; `Style` picks the icon/name set. |
| `Size` | `X,Y` | Bounding grid size in cells. **Must equal the row/column count of the slot grid** — mismatch logs `design rows=N does not match Size Height=M`. |
| `MeshOffset` | `X,Y` | Model offset so the mesh lines up with the grid. |
| `IconPath`, `SelectIcon` | string | UI art. |
| `ModelPath` | string | Mesh (`.obj`/`.fbx`, loaded via `SDNative`). |
| `Animated` | bool | Skinned mesh. |
| `IsShipyard`, `IsOrbitalDefense` | bool | Behaviour flags; also OR-ed into the design. |
| `Thruster` | `X,Y,Z,Scale` | Repeatable. Each is a VFX emitter; `Scale/8` is the world radius ([`ThrusterZone`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipHull.cs#L462)). |

### 2.2 The slot grid

One line per row, `Size.X` columns, each column **exactly 3 characters**, separated by `|`:

```
___|O  |___|IO |___
___|O  |IC |IO |___
```

- `___` — no slot. A module cannot be placed here.
- `I`, `O`, `E`, `IO`, `IE`, `OE` — a slot with that restriction (§2.3).
- A column containing `C` marks `GridCenter` — the cell the ship rotates and is measured around.
  `IC `, `IOC`, `OC `, `EC `, `IEC`, `OEC` make it a legal slot too; `C__` puts the centre on an
  empty cell (a hull with a hole in the middle). **A hull with no `C` logs
  `invalid GridCenter` and will point the wrong way.**

`SurfaceArea` is not a field — it is **the number of slots**
([L856](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipHull.cs#L856))
and it is the denominator of several formulas (§7.1, §7.6). Adding one row of slots changes a
ship's strength.

### 2.3 Slot restrictions — which module fits where

`Restrictions` is an enum
([`Restrictions.cs`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/Restrictions.cs#L3)):
`I` interior, `O` outer, `E` engine mount, plus partial combinations `IO`, `IE`, `OE`, the wildcard
`IOE`, and the exclusive forms `xI`, `xIO`, `xO`.

A module may occupy a slot when
[`SlotStruct.CanSlotSupportModule`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/SlotStruct.cs#L71)
returns true:

1. module `Restrictions == IOE` → **any** slot;
2. module `Restrictions` **equals** the slot's → yes;
3. otherwise the two must **share a letter** (`I`↔`I`, `O`↔`O`, `E`↔`E`), computed by
   [`IsPartialMatch`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/SlotStruct.cs#L57);
4. `xI` / `xIO` / `xO` accept **only** the identical slot letter.

So a module stamped `I` fits an `I`, `IO` or `IE` slot but not `O` or `E`; a module stamped `IO`
fits any slot containing `I` or `O`; an `E` module only fits `E`, `IE`, `OE`. For a multi-cell
module the check runs for **every cell it covers** — one bad cell rejects the whole placement.

---

## 3. Module XML — `ShipModules/`

One `<ShipModule>` element per file. The class is
[`ShipModule_XMLTemplate`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/ShipModuleFlyweight.cs#L230);
`XmlSerializer` maps element names to fields, so **an element name that is not a field is silently
dropped**. Notably ignored today: `Version`, `TechBranch`, `TexturePath`.

The UID is **overridden by the loader**: `LoadShipModules` sets `data.UID` from the file's UID
registry entry, so `<UID>` inside the file is documentation. Keep it equal to the filename stem
anyway — everything else looks up the UID.

A module template is turned into a runtime module by
[`ShipModule.CreateTemplate`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L414),
which copies the fields into a shared `ShipModuleFlyweight` (one per UID, shared by every ship that
mounts it) and precomputes `WeaponInaccuracyBase`, `Radius` and `ExplosionRadius`.

### 3.1 Identity and gating

| Field | Type | Meaning / effect |
|---|---|---|
| `UID` | string | UID (overwritten by the file registry, §3 preamble). |
| `NameIndex`, `DescriptionIndex` | ushort | Ids into `GameText.yaml`. Missing ids log warnings. |
| `TechLevel` | int | Era hint, carried into the flyweight. Its only runtime effect today is adding to a module's dice roll when it takes internal damage ([L1422](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L1422)). It is **not** the tech that unlocks the module — that is §5. |
| `Cost` | float | Build cost contribution (§7.2). |
| `XSize`, `YSize` | int | Grid footprint in cells, before rotation. A module longer than it is tall rotates to swap them (`ModuleRot.Left/Right`). |
| `ModuleType` | [`ShipModuleType`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/ShipModuleType.cs#L3) | Primary classification: `Turret`, `Command`, `Armor`, `PowerPlant`, `PowerConduit`, `Engine`, `Shield`, `Hangar`, `FuelCell`, `Ordnance`, `Construction`, … Drives many formulas and the shipyard's category tab. |
| `Restrictions` | `Restrictions` | Which hull slots it fits (§2.3). |
| `Powered` | bool | Draws power; false means it works unpowered. |
| `IndirectPower` | bool | Surfaces as `AlwaysPowered` — power comes from the grid/conduits, not a direct draw. |
| `DisableRotation` | bool | Forces one orientation. The loader also forces it for **square** modules (`XSize == YSize`), except 1×1 weapons. |
| `DroneModule` … `StationModule` | bool (default true) | Which hull classes may mount it: `DroneModule`, `FighterModule`, `CorvetteModule`, `FrigateModule`, `DestroyerModule`, `CruiserModule`, `BattleshipModule`, `CapitalModule`, `FreighterModule`, `PlatformModule`, `StationModule`. All default `true`, so a module that omits them is mountable everywhere. |
| `PercentLimitOnShips` | float | Caps how many of this module one ship may mount, as a % of `SurfaceArea` ([`SlotLimitOnShip`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L199)). `0` = unlimited. |
| `Salvage` | bool | Marks a salvage unit; contributes to the salvage-ship role and salvage counts. |

### 3.2 Mass, health, damage resistance

| Field | Type | Meaning / effect |
|---|---|---|
| `Mass` | float | Mass (§7.3). **Negative mass** = inertial damper: it only subtracts while the module is powered. |
| `HealthMax` | float | Template health; the real value is `HealthMax * EmpireHullBonuses.HealthMod` ([L262](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L262)). Values below 1 are warned about: such a module dies instantly. |
| `RepairDifficulty` | float | Default 1. Caps how much a single repair tick can restore (`maxRepair = maxHealth * 1/(1+difficulty)`). |
| `Deflection` | float | Flat damage threshold: adds `1 + Deflection*0.01` to defence (§7.1) and subtracts from incoming damage in combat. |
| `KineticResist`, `EnergyResist`, `PlasmaResist`, `BeamResist`, `ExplosiveResist` | float ≤ 1 | Per-damage-type resistance. Clamped to ≤ 1 on read. Each adds `1 + resist*0.2` to defence, i.e. a 1.0 resist is `×1.2` in each of the five factors. |
| `APResist` | int | Armour-piercing resistance. A non-zero value also **marks the module as armour** for `ShipModule.Is(Armor)`; defence multiplies by `1 + APResist*0.5` for armour-typed modules. Negative values only mark armour. |
| `EMPProtection` | float | `def *= 1 + EMPProtection/Area*0.002`. |
| `Regenerate` | float | Self-repair rate; `def += Regenerate*0.1`. |
| `BonusRepairRate` | float | Repair aura; `def += BonusRepairRate*RepairRateMod*0.5`. |
| `ExplosionDamage`, `ExplosionRadius` | int | On-death blast. Radius is expanded by module size when damage > 0 (`8 + radius + avgSize*16`). |
| `ShieldBubbleColor` | string | VFX tint. |

### 3.3 Power

| Field | Type | Meaning / effect |
|---|---|---|
| `PowerFlowMax` | float | Power **supply** per second. `ActualPowerFlowMax = PowerFlowMax * PowerFlowMod`. Any module with `PowerFlowMax >= 1` counts as a `PowerPlant` for `Is(...)` checks even if its `ModuleType` differs. |
| `PowerStoreMax` | float | Power **storage**. `FuelCell` modules scale theirs by `FuelCellMod`. |
| `PowerDraw` | float | Continuous draw. Negative `PowerDraw` is a producer in the power-duration maths. |
| `PowerDrawAtWarp` | float | Extra draw while warping; counted at **half** weight (§7.4). |
| `PowerRadius` | int | Range within which this plant feeds conduits. |

### 3.4 Weapons, shields, hangars, everything else

| Field | Type | Meaning / effect |
|---|---|---|
| `WeaponType` | string | UID of a `Weapons/*.xml`. Missing weapon logs `missing WeaponType`. The module gets `InstalledWeapon` on install and its area becomes offensive area. |
| `FieldOfFire` | degrees | Turret arc. Offence multiplies by `clamp(radians / (π*0.34), 1, 4)` — a full 360° turret is worth ~4× a narrow one. |
| `TargetValue` | int | AI prioritisation of this module as a target; +1 when damaged. |
| `AccuracyPercent` | float | Default `-1` = use the default inaccuracy model. `>= 0` overrides it ([`GetWeaponInaccuracyBase`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/WeaponTemplate.cs#L249)). |
| `OrdinanceCapacity` | short | Ordnance (ammo) storage; feeds `BaseOrdnanceMax`. |
| `OrdnanceAddedPerSecond` | float | Ammo regeneration. |
| `BombType` | string | For `ModuleType == Bomb`: the weapon UID whose payload it drops. |
| `ShieldPowerMax` | float | Shield strength. `>= 1` makes it a shield for `Is(Shield)`. Actual value: `ShieldPowerMax*ShieldMod + amplification` ([L320](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L320)). |
| `ShieldRadius` | float | Bubble radius, in cells. Defence scales with `(radius+8)²/256/slotCount`, capped at 1 — small ships get less from the same shield. |
| `ShieldRechargeRate`, `ShieldRechargeCombatRate` | float | Out-of-combat / in-combat regeneration. Both enter defence as ratios to `ShieldPowerMax`. |
| `ShieldRechargeDelay` | float | Seconds before recharge resumes; defence multiplies by `1/delay`. |
| `ShieldDeflection` | float | Shield damage threshold; `def *= 1 + deflection/50`. |
| `ShieldKineticResist` … `ShieldBeamResist` | float ≤ 1 | Same five types as §3.2, applied to the shield term only. |
| `AmplifyShields` | float | Adds `value / numberOfMainShields` to **each** main shield's max, then `*0.05` to defence. Several amplifiers stack additively. |
| `HangarShipUID` | string | The ship a bay launches, or a `DynamicHangarOptions` token (`DynamicLaunch`, `DynamicInterceptor`, `DynamicAntiShip`) to launch whatever fits. `NotApplicable` = size-valued only. |
| `MaximumHangarShipSize`, `PermittedHangarRoles` | short / string[] | What a dynamic bay may launch; also makes the bay's area offensive. |
| `IsSupplyBay`, `IsTroopBay` | bool | Supply/troop bays: area counts as offensive, and no hangar ship is set. |
| `HangarTimerConstant`, `HangarTimer` | float | Launch interval (default 30). Lower = faster launches, and it divides a dynamic bay's offence. |
| `NumberOfColonists`, `NumberOfEquipment`, `NumberOfFood` | float | Colony module payload. |
| `TransporterRange`, `TransporterPower`, `TransporterOrdnance`, `TransporterTroopLanding`, `TransporterTroopAssault`, `TransporterTimerConstant` | | Boarding/teleport capability. Any of the first three marks a support module. |
| `TroopCapacity`, `TroopsSupplied` | int | Barracks capacity / troops added on spawn. `TroopCapacity*50` in defence. |
| `CargoCapacity` | float | Cargo; ≥ 50 % of slots makes a civilian design a freighter (§7.5). |
| `ResearchPerTurn`, `Refining` | float | Research/mining station throughput. |
| `SensorRange`, `SensorBonus` | float | Detection, and the ship's max sensor bonus. |
| `ECM` | float | Flat defence addition and combat accuracy penalty. |
| `MechanicalBoardingDefense` | float | Resistance to boarding. |
| `InhibitionRadius` | float | Interdiction; marks the ship as support and is used for FTL inhibition. |
| `FTLSpoolTime` | float | Charge time before warp; the ship takes the **max** across modules. |
| `Thrust`, `WarpThrust`, `TurnThrust` | float | Movement (§7.6). |
| `HealPerTurn` | float | Out-of-combat self-heal. |
| `DeployBuildingOnColonize` | string | Building placed on colonisation; each one counts toward `NumBuildingsDeployed`. |
| `ResourceStored`, `ResourceRequired`, `ResourceStorageAmount` | | Legacy resource fields — present in the template, no runtime consumer found in `Ship_Game` today. |
| `WarpMassCapacity`, `MountLeft`, `MountRight`, `MountRear`, `FTLSpeed` | | Legacy/unused in the template; no consumer found. `Mount*` was replaced by `ModuleRot` in the `.design` slot data. |

---

## 4. Weapon XML — `Weapons/`

`<Weapon>` maps to
[`WeaponTemplate`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/WeaponTemplate.cs#L13).
After all weapons load, [`InitializeTemplate`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/WeaponTemplate.cs#L181)
fills the derived values (`ActiveWeaponTags`, `BeamDuration` default 2 s, `FireDelay` floor
0.016 s, `DamagePerSecond`).

### 4.1 Tags — the type system

`Tag_Kinetic`, `Tag_Energy`, `Tag_Guided`, `Tag_Missile`, `Tag_Plasma`, `Tag_Beam`,
`Tag_Intercept`, `Tag_Bomb`, `Tag_Torpedo`, `Tag_Cannon`, `Tag_PD` (booleans, stored as one bitmask).
They do four things: pick which empire tech bonuses apply
(`EmpireData.WeaponTags[tag]`), select damage type against a target's armour/shield resist,
feed offence multipliers (§7.7), and decide intercept/point-defence behaviour. Unknown tags in
content (`Tag_BioWeapon`, `Tag_Drone` in `Ballistic cannons/…xml`) have no property and are
therefore ignored.

### 4.2 Timing and payload

| Field | Meaning |
|---|---|
| `FireDelay` | Seconds between shots/salvos. |
| `SalvoCount`, `SalvoTimer` | A salvo of N shots spread over the timer. `NetFireDelay = FireDelay + SalvoTimer` (or `+ BeamDuration` for beams, [L164](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/WeaponTemplate.cs#L164)). |
| `ProjectileCount` | Projectiles per shot (flak buckshot, MIRV warheads). |
| `DamageAmount` | Damage per projectile/beam tick. |
| `ProjectileSpeed` | Speed; **also** an offence multiplier (`speed/range`), so a slow projectile at long range is worth much less. |
| `Range` → `BaseRange` | Range in world units. Multiplied by tag range bonuses at runtime (`GetActualRange`, L426). |
| `PowerRequiredToFire` | Power per shot; see §7.4 for the kinetic penalty at 10× module area. |
| `OrdinanceRequiredToFire` | Ammo per projectile. |
| `IsBeam`, `BeamDuration`, `BeamPowerCostPerSecond`, `BeamThickness`, `BeamTexture` | Beam behaviour. Beams use `DamageAmount` (or `PowerDamage` if zero) × `BeamDuration*60` for DPS. |
| `ExplosionRadius` | > 0 means the projectile explodes; > 16 also boosts offence. |
| `ArmorPen`, `EffectVsArmor`, `EffectVsShields` | Penetration and multipliers (1.0 = neutral). |
| `ShieldPenChance` | % chance to bypass shields; adds `1 + chance*0.01` to offence. |
| `TruePD` | Point defence that cannot hit ships: offence **×0.2**. |
| `ExcludesFighters/Corvettes/Capitals/Stations` | Targeting exclusions; each also cuts offence (−0.15/−0.15/−0.45/−0.25). |
| `FireCone`, `FireArc` | Random spread and fixed fan-out. FireCone also cuts offence for unguided weapons. |
| `IsTurret`, `IsMainGun` | Placement/turret behaviour; `ModuleType == Turret` gives offence ×1.25. |
| `Tag_Missile` with a non-`Missile` `WeaponType` | Warned: produces invisible projectiles. |
| `MirvWeapon`, `MirvSeparationDistance` | Warhead split; offence counts the carrier at ×0.25 plus the warheads (§7.7). |
| `TerminalPhaseAttack`, `TerminalPhaseDistance`, `TerminalPhaseSpeedMod` | Terminal manoeuvre; modifies offence. |
| `DelayedIgnition` | Hurts offence (`1 - min(delay*0.1, 0.95)`). |
| `HitPoints`, `ProjectileRadius`, `RotationRadsPerSecond` | Interception survivability: offence gets `1 + HP*0.02/radius` when interceptable and agile. |
| `OffPowerMod` | Manual balance multiplier on offence (default 1). |
| `WeaponHitEffect`, `WeaponShieldHitEffect`, `WeaponDeathEffect`, `WeaponTrailEffect`, `MuzzleFlash`, `FireCueName`, `DieCue`, `InFlightCue` | VFX/audio names, resolved from `3DParticles/ParticleEffects.yaml` and `AudioConfig.yaml`. |
| `HardCodedAction`, `Bomb*`, `TroopDamageChance`, `TractorDamage`, `RepulsionDamage`, `EMPDamage`, `PowerDamage`, `SiphonDamage` | Special effects; each has an offence weight (§7.7). |

---

## 5. Tech XML — `Technology/`

### 5.1 Fields

| Field | Meaning |
|---|---|
| `UID` | Tech id. **This is what `TechsNeeded` and the save file store.** |
| `Cost` | Research cost, scaled at runtime by `ActualCost` (pace × size-based multiplier, [L185](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Technology.cs#L185)). |
| `LeadsTo/LeadsToTech` | Direct children. `ComesFrom` is the reverse; both resolve into `Children`/`Parents` in [`ResolveLeadsToTechs`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Technology.cs#L265). Root techs have `RootNode != 0` and no parents. |
| `ModulesUnlocked/UnlockedMod` | `ModuleUID` + optional `Type` (race/trait gate). **The only link between a module and a tech.** |
| `HullsUnlocked/UnlockedHull` | `Name` = `HullName` + optional `ShipType`. |
| `BuildingsUnlocked`, `TroopsUnlocked`, `BonusUnlocked` | Other content types. `BonusUnlocked` is how flat bonuses (FTL speed, mass reduction, weapon tags…) are granted; `BonusType` selects the effect. |
| `TechsRevealed`, `EventsTriggered` | Reveal/event side effects. |
| `MaxLevel`, `MultiLevelCostMultiplier` | Multi-level techs (default 1 level). |
| `Secret`, `Unlockable`, `HiddenFrom`, `HiddenFromAllExcept`, `UnlockedAtGameStart` | Visibility and race gating. |
| `RequiresResearchStations`, `RequiresMiningOps`, `RequiresSalvageOps` | Prerequisite mechanics for the research tree. |

`TechnologyTypes` is **derived**, not authored: [`UpdateTechnologyTypesFromUnlocks`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Technology.cs#L294)
infers `ShipWeapons`/`ShipDefense`/`ShipHull`/`Industry`/… from what the tech unlocks. That is why
the same tech can show up under several research filters.

### 5.2 Which tech unlocks a module

`GetModuleTechUnlocks` ([L40](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/NewGame/ShipDesignUtils.cs#L40))
walks every tech's `ModulesUnlocked` and builds `ModuleUID → Tech`. If **two** techs list the same
module the last one loaded wins — a real hazard in mods, and invisible in game.

### 5.3 Research cost of a design, and why it is not a field

`MarkDesignsUnlockable` ([L12](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/NewGame/ShipDesignUtils.cs#L12))
runs once after content load:

1. **Hull** — `GetHullTechUnlocks` maps each hull to the tech that lists it. Root techs are stored
   as `null` (always unlocked). `MarkHullsUnlockable` ([L83](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/NewGame/ShipDesignUtils.cs#L83))
   then sets `hull.TechsNeeded` to the tech's **full path** and `Unlockable = true`. A hull no tech
   lists, or one whose role sorts before `fighter`, ends up `Unlockable` with no techs.
2. **Design** — `MarkShipsUnlockable` ([L108](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/NewGame/ShipDesignUtils.cs#L108))
   collects the leaf tech of **every unique module UID** in the design. If any module UID has no
   tech, the design is **not unlockable at all** and gets no `TechsNeeded`. Otherwise it unions the
   full tech path of each leaf tech, then adds the hull's `TechsNeeded`.
3. **Full path** — `GetFullTechTreePaths` ([L54](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/NewGame/ShipDesignUtils.cs#L54))
   turns a tech into `[tech, parent, grandparent, …]` but **deliberately drops the root node**,
   since roots are free.

So: **design research cost = Σ `Cost` of every tech in `TechsNeeded`**, and buildability is gated on
`design.TechsNeeded ⊆ empire's researched techs`
([`Empire_ShipsWeCanBuild`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Empire_ShipsWeCanBuild.cs#L373)).
Consequences worth remembering: adding one late-era module to a design can add a whole branch;
swapping a module for an equivalent one from another branch can make a design *cheaper* to unlock
at the same cost; and a module no tech lists silently makes its design unbuildable.

---

## 6. `.design` — a ship built on a hull

Writer: [`CreateShipDataText`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipDesign_WriterParser.cs#L37).
Parser: [`ParseDesign`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipDesign_WriterParser.cs#L112),
slot line: [`ParseDesignSlot`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipDesign_WriterParser.cs#L274).

### 6.1 Header

| Field | Meaning |
|---|---|
| `Version` | Must be `1`. Missing/invalid throws and the design is skipped. |
| `Name` | Design UID **and** display name. |
| `Hull` | `HullName` of a `.hull`. Unknown hull → design dropped with a warning. |
| `Role` | `RoleName`. A **starting point only** — the shipyard recomputes it from the modules (§7.5). Early-return roles (`prototype`, `supply`, `construction`, `station`, `platform`, `scout`, `troop`) are honoured as written. |
| `ModName` | `""` = vanilla. |
| `Style`, `Description`, `IconPath`, `SelectIcon` | Presentation; falls back to the hull's. |
| `Size` | `X,Y`. Informational: strength uses the **hull's** surface area, not this. A mismatch shows up in `GetCompletionPercent` and the grid overlay. |
| `GridCenter` | Must match the hull's `GridCenter` (from its `C` slot), or the grid and the model disagree. |
| `FixedCost`, `FixedUpkeep` | Override the computed values when > 0. |
| `DefaultCombatState` | `CombatState` (`AttackRuns`, `HoldPosition`, …). |
| `ShipCategory` | `Unclassified`/`Civilian`/`Conservative`/… — gates freighter behaviour. |
| `HangarDesignation` | `General`/`Interceptor`/`AntiShip` — changes issue severity for weapon coverage. |
| `IsShipyard`, `IsOrbitalDefense`, `IsCarrierOnly` | Flags, OR-ed with the hull's. |
| `EventOnDeath` | Event UID fired on death (e.g. `DefeatedMothership`). |
| `ModuleUIDs` | `;`-separated palette. **Position is the index** used by slot lines. |
| `Modules` | Number of slot lines that follow. Must match exactly or the parse throws. |

Unrecognised keys are **ignored silently** — the vanilla files still contain `DefaultAIState=`,
which nothing reads. Do not assume a key in an old file is live.

### 6.2 Slot line grammar

```
gridX,gridY;moduleUIDIndex;sizeX,sizeY;turretAngle;moduleRot;hangarShipUID
```

```
10,8;5;2,2;270;1;Terran Assault Shuttle
```

| Position | Field | Rules |
|---|---|---|
| 1 | `gridX,gridY` | Top-left cell, `0..Size-1`. Must be inside the hull and every covered cell must be a slot. |
| 2 | `moduleUIDIndex` | Index into `ModuleUIDs`. |
| 3 | `sizeX,sizeY` | **Oriented** footprint. `1,1` may be omitted; a 1×2 module rotated `Left`/`Right` is written `2,1`. |
| 4 | `turretAngle` | 0–360, the turret's rest facing. |
| 5 | `moduleRot` | `0` Normal, `1` Left, `2` Right, `3` Rear. |
| 6 | `hangarShipUID` | Only for hangars: the launched ship, or a `Dynamic*` token. |

Trailing empty fields may be dropped — the writer omits everything after the last non-default
value. `2,2;;;Terran Assault Shuttle` is legal.

**Overlap is not detected by the parser.** Two slots covering the same cell load fine and are
rejected only when the design is validated ([`ShipDesignIssues`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/ShipDesign/ShipDesignIssues.cs#L16))
or when the module grid is built.

---

## 7. Derived numbers and their formulas

Everything below is computed at load time or on demand; none of it is stored in the content files
(except `FixedCost`/`FixedUpkeep`).

### 7.1 Strength

Entry point: `ShipDesign.BaseStrength` =
[`ShipStrength.OfDesign`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipDesign_Stats.cs#L200)
→ [`OfModules`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipStrength.cs#L40).

```
surfaceArea    = hull.SurfaceArea                 # number of hull slots
mainShields    = count(m.type == Shield && m.shieldPowerMax > 0)
amplification  = Σ m.amplifyShields               # only powered+active ones when workingOnly
amplifyPerShld = mainShields > 0 ? amplification / mainShields : 0

for each module:
    shieldsMax = m.shieldPowerMax * bonuses.ShieldMod
    if mainShield: shieldsMax += amplifyPerShld
    offense       += m.CalculateModuleOffense(empire)
    defense       += m.CalculateModuleDefense(surfaceArea, bonuses, shieldsMax)
    offensiveArea += m.area  if (m.installedWeapon || m.isTroopBay || m.isSupplyBay
                                 || m.maximumHangarShipSize > 0)

if empire != null and offensiveArea == 0 and IsUnarmedSupport(design, empire): return 0

strength = Combine(surfaceArea, offensiveArea, offense, defense)
if role is platform or station: strength *= 0.5        # StationaryStrength
```

`Combine` is
[`ShipBuilder.GetModifiedStrength`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/EmpireAI/ShipBuilder.cs#L494):

```
offenseRatio = offensiveArea / surfaceArea
if defense > offense and offenseRatio < 0.1:
    strength = offense*2 + defense*0.1        # a shielded ship with almost no weapons
else:
    strength = offense + defense
```

Two things follow that surprise people: **defence counts the full hull-slot count as a divisor**
(a big hull with few shields is not penalised directly, but shield coverage is), and a support ship
with no weapons and no bays gets strength **0** by definition
([`IsUnarmedSupport`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipStrength.cs#L14):
default troop ship, mining ship, assault shuttle, supply shuttle, scout, subspace projector,
freighter, constructor).

### 7.2 Cost

`BaseCost` = **Σ module `Cost`**. The hull contributes nothing.
[`GetCost`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipDesign_Stats.cs#L211):

```
if FixedCost > 0:  cost = FixedCost * pace
else:
    cost  = BaseCost * pace
    cost += cost * empire.data.Traits.ShipCostMod
    if role is platform or station: cost *= 0.7
cost = (int)cost
```

`pace` is the universe's `ProductionPace` (game-speed multiplier). Upkeep is separate
(`ShipMaintenance.GetBaseMaintenance`).

### 7.3 Mass

[`GetMassParts`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipStats.cs#L167)
and [`MassAfterDampers`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipStats.cs#L187):

```
minMass      = (int)(surfaceArea * 0.5 * (1 + surfaceArea * 0.002))   # hull mass floor
positiveMass = minMass
negativeMass = 0
for each module:
    m = module.GetActualMass(loyalty, ordnancePercent, useMassModifier:false)
    if m >= 0: positiveMass += m  else: negativeMass += m

positiveMass *= empire.data.MassModifier          # tech bonus
mass = max(positiveMass + negativeMass, positiveMass * 0.5)
mass = max(mass, minMass)
```

`GetActualMass` ([L1305](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L1305)):
armour mass is multiplied by `ArmourMassModifier`; `Ordnance`-type modules are multiplied by the
ordnance fill fraction (floor 10 %); **negative-mass modules only reduce mass while powered**,
otherwise their absolute mass is added.

So the hull alone gives a small ship a real mass, and inertial dampers can never remove more than
half of the rest of the ship.

### 7.4 Power

[`Power.Calculate`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/Power.cs#L16)
(`designModule: true` when called from `InitializeCommonStats`, so **every** module counts, powered
or not):

```
flow   = Σ m.actualPowerFlowMax        # PowerFlowMax * PowerFlowMod
store  = Σ m.actualPowerStoreMax       # FuelCell: * FuelCellMod
shieldDraw   = Σ m.powerDraw  where m.is(Shield)
otherDraw    = Σ m.powerDraw  elsewhere
warpDraw     = (shieldDraw + otherDraw) * FTLPowerDrainModifier
             + (Σ m.powerDrawAtWarp) * FTLPowerDrainModifier / 2
subLightDraw = shieldDraw + otherDraw
duration     = store / (draw - flow)   if draw > flow, else float.MaxValue
```

Weapon firing power is **not** in this draw — it is per-shot
(`PowerFireUsagePerSecond` = `(BeamPowerCostPerSecond*BeamDuration + PowerRequiredToFire*ProjectileCount*SalvoCount)/NetFireDelay`,
[L176](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/WeaponTemplate.cs#L176)),
and the shipyard's power time is `capacity / (weaponPower - (flow - subLightDraw))`
([`ShipDesignStats.Update`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/ShipDesign/ShipDesignStats.cs#L61)).

### 7.5 Role

`Role` in the `.design` is a hint; the shipyard rewrites it from the modules via
[`RoleData.GetDesignRole`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/RoleData.cs#L32),
in this order (first match wins):

```
prototype, supply, construction, station, platform, scout, troop   (as authored)
name == "Subspace Projector"          → ssp
IsShipyard                            → shipyard
has colony module                     → colony
any salvage bay                       → support
freighter + Civilian + cargo≥50% slots → freighter
  (hull role ≥ freighter) and:
    construction module                → construction
    troop bays/transports >10% slots   → troopShip   (needs ≥1 troop bay and ≥1 troop capacity)
    bomb modules >5% slots             → bomber
    hangars >10% slots                 → carrier
    supply/troop hangars >10% slots    → support
    Civilian + cargo ≥50% (non-freighter hull) → freighter
special modules >10% slots             → support
otherwise map the hull role: corvette/gunboat→corvette, carrier→battleship,
  capital→capital, destroyer/frigate→frigate, scout/fighter→fighter if armed else scout
```

`ShipCategory` interacts with this: a freighter hull that cannot carry cargo in `Civilian`
category is demoted to `Unclassified`.

### 7.6 Speed and turning

From [`ShipStats`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipStats.cs#L248):

```
FTL  = max(warpThrust / mass * FTLModifier, LightSpeedConstant)      if warpThrust > 0
STL  = min(thrust / mass * SubLightModifier, MaxSubLightSpeed)
turn = min(turnThrust / mass / 700, MaxTurnRadians)                  (+5%/level, tractor penalty)
```

For a **design** the static overloads use `BaseThrust/BaseMass` and skip level/tractor terms. Since
mass is dominated by module mass, thrust-to-weight is the only lever — and a station has no thrust
at all (`IsStationary` returns 0,0,0).

### 7.7 Offence and defence per module

**Defence** —
[`CalculateModuleDefense`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L1505):

```
def = healthMax * HealthMod * 0.005
if shieldsMax > 0:
    shieldDef      = shieldsMax * 0.02
    coverage       = ((shieldRadius + 8)^2 * π) / 256 / slotCount
    shieldDef     *= min(coverage, 1)
    shieldDef     *= 1 + shieldKineticResist*0.2      # × energy, beam, explosive, plasma
    shieldDef     *= rechargeRate  > 0 ? rechargeRate/(shieldsMax*0.01) : 1
    shieldDef     *= rechargeDelay > 0 ? 1/shieldRechargeDelay : 1
    shieldDef     *= rechargeCombat> 0 ? 1 + rechargeCombat/(shieldsMax*0.04) : 1
    shieldDef     *= 1 + shieldDeflection/50
    def += shieldDef
def *= 1 + beamResist*0.2        # × kinetic, energy, plasma, explosive
def *= 1 + deflection*0.01
def *= isArmor ? 1 + APResist*0.5 : 1
def += ECM
def *= 1 + EMPProtection / area * 0.002
def += (turnThrust + warpThrust + thrust) / 15000
def += powerFlowMax * PowerFlowMod * 0.02
def += powerStoreMax * 0.002
def += troopCapacity * 50
def += bonusRepairRate * RepairRateMod * 0.5
def += amplifyShields * 0.05
def += regenerate * 0.1
```

**Offence** —
[`CalculateModuleOffense`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipModule.cs#L1564):

```
off = installedWeapon?.CalculateOffense(this) ?? 0
off += isTroopBay ? 50 : 0
if not a hangar, or no hangar ship, or supply/troop bay: return off
if dynamic hangar:
    off += strength of the ship it would launch
         (or maximumHangarShipSize*100*permittedRoles/max(hangarTimerConstant,1) as a fallback)
else:
    off += strength of the named hangar ship (100 if the ship is missing)
return off * 0.5
```

Weapon offence — [`WeaponTemplate.CalculateOffense`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/WeaponTemplate.cs#L273),
with the damage part in [`PayloadOffense`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Gameplay/WeaponTemplate.cs#L304):

```
shots = 1 / netFireDelay
beam:  off = damage*60*beamDuration*shots + tractor*30*shots
             + (power + repulsion + siphon)*45*shots + troopChance*shots
other: off = damage*salvoCount*projectiles*shots
           + (emp*0.5 + power*0.75)*salvoCount*projectiles*shots

×2.5 if guided
×(1 + armorPen*0.2)
×(1 ± (effectVsArmor   - 1)*0.5)      >1 buffs, <1 cuts, half-strength each way
×(1 ± (effectVsShields - 1)*0.5)
×0.2 if TruePD
×(projectileSpeed / baseRange)        if speed > 1
×flightFactor                          intercept 0.8; agile intercept +HP*0.02/radius;
                                       delayedIgnition 1-min(d*0.1, 0.95)
×(explosionRadius*0.0625)              if radius > 16 and not TruePD
×(1 + shieldPenChance*0.01)
×terminalPhase modifier
×exclusions (1 − 0.15/0.15/0.45/0.25)
×(1 - fireCone*0.01*range*0.0005)      unguided only, floor 0.1
×reach²                                unguided, reach = baseRange*0.00025
×reach*sqrt(reach)                     guided
×(1.25 if the module is a Turret)
×clamp(fieldOfFireRads/(π*0.34), 1, 4)
×0.5                                   kinetic weapon needing >10*area power per shot or
                                       >2*area sustained draw
×OffPowerMod
```

Every term there is a design lever: range and speed multiply, guided weapons are worth far more
than their raw DPS, and a kinetic weapon on an under-powered ship is halved twice.

### 7.8 What the shipyard warns about

[`ShipDesignIssues`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/ShipDesign/ShipDesignIssues.cs#L16)
turns these numbers into severity-tagged warnings (`None < Informative < Minor < Major < Critical`,
[types at L732](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/GameScreens/ShipDesign/ShipDesignIssues.cs#L732)).
Thresholds worth knowing before you submit a design:

| Check | Rule |
|---|---|
| No command module | Critical unless role is `platform` |
| Backup command | Major when area ≥ 500 and only one command module |
| Power | `recharge < 0` Critical; recharge time > 25 s Critical, >10 s Informative |
| Weapon power time | < 2 s Critical, < 4 s Major (energy weapons that out-draw recharge) |
| Ammo time | `ammoTime/60` (large craft) or `/30`; < 0.3 Critical |
| Ordnance burst | burst > capacity: efficiency <0.5 Critical |
| Warp | no warp on a large craft = Critical; warp time < 60 s Critical |
| Troops | area ≥ 500 expects `area/500` troops; more bays than troops = Major |
| PD | area ≥ 500 needs PD value > area/60 |
| Targeting | no anti-fighter/anti-capital coverage on a large craft = Critical |
| Platform hangars | fighter hangars + `HoldPosition` on a station/platform = Critical |

---

## 8. Invariants that break a design silently

These all load without an exception and misbehave later — the expensive class of bug.

1. **Exactly one command module** (`IsCommandModule`) — `Cockpit`, `Bridge`, `CIC`. Zero is
   Critical; one on a 500+ slot ship means no backup.
2. **`Size` must equal the slot grid**, and the design's `GridCenter` must equal the hull's `C`
   slot. A mismatch shifts every module relative to the model and the hit grid.
3. **Every covered cell must be a slot and must accept the module** (§2.3). One bad cell rejects
   the placement; the design screen will silently keep the module where you dragged it.
4. **`ModuleUIDs` indices are positional.** Reordering the palette without rewriting every slot
   line re-arms the whole ship with different modules.
5. **`Modules=` must equal the number of slot lines**, or the parse throws and the design is
   dropped (a warning in the log, no ship).
6. **`HangarShipUID` only matters on hangars** and is ignored on supply/troop bays, which take the
   empire's default shuttle. A hangar naming a ship the player cannot build is converted to
   `DynamicLaunch` at runtime.
7. **A module no `Technology` lists makes the whole design un-unlockable** (§5.3). This is the most
   common reason a new mod ship never appears.
8. **`Restrictions` on an engine module** must be `E`/`IE`/`OE`; an `IO` engine can never be placed
   even though the file loads.
9. **Negative `Mass` only works while powered.** Unpowered dampers add their mass.
10. **`HealthMax < 1`** makes the module die on the first damage tick — `LoadShipModules` warns
    about it precisely because the failure looks like "the ship is missing a part".

---

## 9. Reading a design without the game

The game's own CLI can regenerate and normalise content:

```
StarDrive.exe --generate-hulls    # legacy XML hulls -> .hull
StarDrive.exe --generate-ships    # legacy XML ships -> .design
StarDrive.exe --fix-roles         # recompute Role/Category for every .design
```

These run headless with `--continue` appended to proceed into the game afterwards. `--fix-roles`
is the way to learn what the role derivation (§7.5) actually says about a design.

To compute strength/cost/research cost **without** a running game, the numbers above are all
available from the text files:

- cost = Σ module `Cost`, ×0.7 for platform/station, ×(1+`ShipCostMod`)
- mass = §7.3, needing only the hull's `SurfaceArea` and module `Mass`
- strength = §7.1 + §7.7, needing hull `SurfaceArea`, module fields, and the weapons each module
  names — but a hangar's offence needs the *launched* design, so hangar ships must be resolved
  first (topological order, fighters before carriers)
- research cost = Σ `Cost` over the `TechsNeeded` closure (§5.3)

Two caveats: `EmpireHullBonuses` modifiers, weapon-tag tech bonuses and `ProductionPace` are empire
/ universe state and are **not** in the content files, so any offline number is a baseline, not the
in-game value; and `TechsNeeded` is computed at load, so it has to be reimplemented (module → tech
map, then parent closure without the root) rather than read from anywhere.
