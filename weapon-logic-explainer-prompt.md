# Explaining ship weapons — a copy-paste interactive prompt

Paste the prompt below into an AI assistant that can read this repository — either a local clone or
the public repo at <https://github.com/TeamStarDrive/StarDrive> — and it becomes a guide to **a gun**:
which template decides it, what its tags do, how many damage numbers it has and which one the screen
is showing, what one shot costs in power and ordnance, and what the damage meets on the way in.

It is the second half of [`module-logic-explainer-prompt.md`](module-logic-explainer-prompt.md). That
document decides whether a module fits a hull, what it costs, and what happens when it is hit; it
hands over at its step 6, "pays out", because the module only names a weapon UID. This document
starts there. It follows the same three conventions: a chain that every answer names, a concept list
discovered from the code each session, and a freshness check before the first menu.

## Why this exists

- **A weapon is not a module.** The module XML carries a `<WeaponType>` string; the numbers live in
  `game/Content/Weapons/**/*.xml` and load into `WeaponTemplate`. One weapon UID is mounted by many
  modules, so "the turret's damage" is a statement about the file it points at. A missing weapon logs
  a warning and leaves the module inert.
- **The tag vocabulary does four unrelated jobs.** Family (`Kinetic`, `Energy`, `Plasma`, `Beam`)
  decides the tech damage bonus, the module resistance and a shield-pen bonus. Delivery (`Guided`,
  `Missile`, `Torpedo`, `Cannon`, `Intercept`) decides flight, interception and imprecision. Role
  (`PD`, `TruePD`) decides what may be targeted. Payload (`Bomb`) decides that the thing is not aimed
  at ships at all. A single tag is read by several of these systems, and no tag means one thing.
- **Three numbers are called damage, and none of them is the whole answer.**
  `WeaponTemplate.DamagePerSecond` is the template's base; `DamagePerSecondWithTechs` is what the
  shipyard panel and the design overlay show; `CalculateOffense` is the AI's strength rating and is
  not dps at all. None of the three counts accuracy, resistances, flight time or power starvation.
- **A beam is not a fast projectile.** Its `DamageAmount` is per frame, applied for `BeamDuration`
  seconds at 60 frames per second, and its cost is a rate drawn from the power store while it fires.
  Treating it as one hit of `DamageAmount` understates it by 24× to 300×.
- **The panel's "Delay" is the whole cycle.** `NetFireDelay` is `FireDelay` plus `SalvoDuration`, or
  plus `BeamDuration` for a beam. A weapon with a salvo fires over time inside that cycle, so the
  number is not the gap between two projectiles.
- **A MIRV launcher's dps belongs to its warhead.** `GetDamagePerSecond` substitutes the warhead
  template and multiplies by its projectile count; a missing warhead logs an error and the shell keeps
  its own damage.
- **`WeaponType` is a string with behaviour in it.** `Tag_Missile` with any `WeaponType` other than
  `Missile` logs a warning and produces invisible projectiles; `Drone` is exempt from cooldown carry;
  `Ballistic Cannon` picks an impact sound. It is not a tag and not a display label.
- **Three tag enum values cannot be set from XML.** `SpaceBomb`, `BioWeapon` and `Drone` exist in
  `WeaponTag`, but `WeaponTemplate` has no `Tag_*` property for them, so the `<Tag_BioWeapon>true` in
  the bomb files is silently dropped.

## The weapon chain

The prompt makes this the spine of every answer: name the link. A weapon question is usually one link
with another behind it — "why does this do nothing" is often 5, not 6.

| # | Step | What it decides | Where it is | What you notice in play |
|---|---|---|---|---|
| 1 | Exists | the template, and the numbers derived from it at load | `game/Content/Weapons/**/*.xml` → `WeaponTemplate`; `ResourceManager.LoadWeapons`; `WeaponTemplate.InitializeTemplate` | the gun is on the module at all |
| 2 | Mounts | which module carries it, and how it may point | module `<WeaponType>` → `ShipModule.InstalledWeapon`; `FieldOfFire`, `AccuracyPercent`; `ShipModuleType.Turret` → `Weapon.IsTurret` | a gun that never turns, or fires in a slot-sized arc |
| 3 | Tags | the family, the delivery, the role, the payload | `WeaponTag`, the `Tag_*` XML booleans, `WeaponTemplate.ActiveWeaponTags` | the tech bonus that applies; PD ignoring ships; missiles that can be shot down |
| 4 | Numbers | base dps, dps with techs, offence rating, range, cycle time | `GetDamagePerSecond`, `DamagePerSecondWithTechs`, `CalculateOffense`, `GetActualRange`, `NetFireDelay` | the DPS line in the yard, the Strength rating, the range a stance holds |
| 5 | Fires | whether it may shoot, and what leaves the barrel | `Weapon.CanFireWeapon`, `PrepareToFire`, `SpawnSalvo`, `FireBeam`, `PowerPerShot`, `OrdnancePerShot` | a gun silent with power in the bar; a salvo arriving in bursts |
| 6 | Lands | what one hit is worth | `Beam.Touch` per frame, `Projectile.Touch` → `ShipModule.Damage`; `GetShieldDamageMod`/`GetArmorDamageMod`, `ArmorPen`, `ShieldPenChance`, deflection | a big gun that scratches armour; a beam that stops on a raised shield |
| 7 | Ends | when the shot stops existing | `Beam.Update` (duration, power store, warp, unpowered module); projectile hit, deflect, flight; `Tag_Intercept` | a beam blinking out mid-fight; a missile wave dying to PD |

Links 1–4 are decided when the game loads or when the design is read. Links 5–7 happen on the sim
thread, once per fixed step, and are the ones a player reports.

## Where the concept list comes from

The map's weapon entries are a seed if the map exists; it is absent in some checkouts and a snapshot
in all of them, so every seed is a name plus a candidate symbol to verify. These are the concepts a
weapon list has to contain. They are the seed set, not a citation.

| Concept | Deciding symbol | Link | What to check |
|---|---|---|---|
| The template | `WeaponTemplate`; `ResourceManager.LoadWeapons` | 1 | `<Weapon>` is the root type; unknown XML elements are dropped in silence |
| Identity | `UID`, `DebugSourceFile` | 1 | the UID is forced from the file name, so a renamed file is a new weapon, not an override |
| Load-time defaults | `InitializeTemplate` | 1 | `BeamDuration` defaults to 2, `FireDelay` floors at 0.016, `SalvoDuration` floors at 0, and `DamagePerSecond` is computed here |
| Tag storage | `TagBits`, `ActiveWeaponTags`, the `Tag_*` properties | 3 | the flags are a bitmask filled by the XML booleans; `ActiveWeaponTags` is the array every rule loops over |
| Unreachable tags | `WeaponTag.SpaceBomb`, `.BioWeapon`, `.Drone` | 3 | no `Tag_*` property exists, so no XML can set them |
| `WeaponType` string | `InitializeTemplate` (Missile check), `Weapon.Update`, `Projectile.CreateWeaponDeathEffect` | 1, 5 | three literal comparisons, not a taxonomy |
| The mount | `ShipModule.WeaponType`, `InstalledWeapon`, `IsWeapon` | 2 | a module may hold no weapon, a missing UID, or a weapon another module also mounts |
| Arc and tracking | `FieldOfFire`, `IsInsideFiringArc`, `WeaponRotationSpeed` | 2, 5 | the arc is the module's; the turret speed is too |
| Accuracy | `WeaponTemplate.GetWeaponInaccuracyBase`, `Weapon.BaseTargetError`, `GetTargetError`, `ImpactPredictor` | 5 | module area and `AccuracyPercent` set the base error; crew level, turrets and PD reduce it; guided weapons skip imprecision |
| Cycle time | `NetFireDelay` | 4 | `FireDelay` plus `SalvoDuration` or `BeamDuration`; every rate divides by it |
| Base dps | `GetDamagePerSecond` | 4 | beams multiply damage by 60 × duration; salvos and projectiles multiply too; MIRV substitutes the warhead |
| dps with techs | `DamagePerSecondWithTechs`, `DamageWithTechs` | 4 | tag damage bonuses and the ordnance bonus; no accuracy, resistance or crew level |
| Offence rating | `CalculateOffense`, `PayloadOffense` | 4 | not dps — guided ×2.5, TruePD ×0.2, a reach curve, exclusion penalties |
| Range with techs | `GetActualRange` | 4 | `BaseRange` plus each active tag's range modifier; `Ship.IsTargetInFireArcRange` compares against it |
| Salvos and projectiles | `SalvoCount`, `SalvoDuration`, `ProjectileCount`, `FireDispersionArc` | 5 | one trigger pull can spawn several shots and several projectiles per shot |
| Burst catch-up | `Weapon.ShotsOwed` | 5 | only plain-damage weapons bank missed shots; beams, salvos and special effects do not |
| Power per shot | `PowerPerShot`, `PowerRequiredToFire`, `PrepareToFire`, `PrepareToFireSalvo` | 5 | paid per projectile and per salvo shot, so a salvo costs `SalvoCount × ProjectileCount × PowerRequiredToFire` |
| Beam power | `BeamPowerCostPerSecond`, `PowerFireUsagePerSecond`, `Beam.Update` | 5 | starting a beam is nearly free; sustaining it drains the store each step until the beam dies |
| The power budget | `ShipDesignStats.WeaponPowerNeeded`, `WeaponPowerNeededNoBeams`, `Power.Calculate` | 5 | the yard sums the average rate; beams are counted separately, because their average understates a burst |
| Ordnance | `OrdnanceRequiredToFire`, `OrdnancePerShot`, `AverageOrdnanceUsagePerSecond`, `ShipModule.OrdinanceCapacity` | 5 | `CanFireWeapon` compares the ship's magazine, not the module's |
| Beam damage | `Beam.BeamInit`, `Beam.Touch` | 6 | `DamageAmount × FixedTime × 60` per frame; `GetDamageWithBonuses` is applied once at spawn |
| Projectile damage | `Projectile.Damage`, `ShipModule.Damage` | 6 | damage is consumed by a module and the remainder carries on if the shot was explosive |
| Resistance | `GetShieldDamageMod`, `GetArmorDamageMod`, `ShieldKineticResist`, `BeamResist`, `ExplosiveResist` | 6 | an exploding shot uses the explosive resist and skips the tag resistances |
| Effect against a target | `EffectVsShields`, `EffectVsArmor`, `GetShieldEffect`, `GetArmorEffect` | 6 | applied to the damage and again, raw, to deflection |
| Armour piercing | `Projectile.ArmorPiercing`, `ArmorPiercingTouch`, `APResist` | 6 | the shot subtracts `APResist + XSize` from its AP and may phase through armour |
| Shield penetration | `ShieldPenChance`, `ActualShieldPenChance`, `IgnoresShields` | 6 | rolled per shot, plus empire and tag bonuses; a penetrated shot hits the hull |
| Side effects | `PowerDamage`, `SiphonDamage`, `EMPDamage`, `TractorDamage`, `RepulsionDamage`, `TroopDamageChance` | 6 | each has its own code path and its own blind spot in the damage numbers |
| Interception | `Tag_Intercept`, `Weapon.PickProjectileTarget`, `Projectile.DamageMissile` | 5, 7 | only projectiles with `Intercept` can be shot; a PD gun may not be interceptable itself |
| Death and visuals | `ExplosionRadius`, `Projectile.CreateWeaponDeathEffect`, `ExplosionRadiusVisual` | 7 | the drawn radius is a separate, larger number |

Deliberately outside this list: the module's cost, mass, fit and health (module document), the tech
that unlocks a module or weapon (tech and era documents), target choice and stances (combat document),
planetary bombing (`Bomb.cs`, the planet-capture document). Answer the gun and say which document owns
the rest.

## The level ladder

Target reading age is `5 + (level - 1) × 5`. Weapons take the ladder well: "why is this weak" has a
real answer at each rung, from "it has to recharge between shots" to the resistance modifier chain.

| Level | Reads like | Code | What the answer contains |
|---|---|---|---|
| 1 | ELI5 | none | A gun has a strength, a reach and a wait between shots; some guns are stronger against shields than armour. No file, class, function or field name ever. Metaphors only for arithmetic, file work, threading and code arrangement. |
| 2 | a curious 10-year-old | none | Game terms after one-line definitions — tag, salvo, beam, point defence, power per shot — and one A → B → C line. Two new terms per answer at most. |
| 3 | a technical 15-year-old | one file and one function named, no bodies | A dps with a worked division, both for a beam and a projectile, and whether each number is XML or derived. A five-line weapon XML fragment is fine; C# is not. |
| 4 | a developer new to this repo | snippets up to five lines, always translated | Which link decides, the order the checks run in, which thread, and what a change breaks in old saves and mods. |
| 5 | a BlackBox developer | full symbols and call chains | Tag bitmask, the three dps functions and why they disagree, load-time defaults, the MIRV substitution, the dead-tag and `WeaponType` traps, and the `code-findings` entries that touch them. |

## The prompt

Copy everything between the rules.

```text
You are my guide into how a weapon works in StarDrive BlackBox: which file makes it, what its tags
do, how much damage it really deals, what one shot costs, and what happens to the damage when it
arrives. Explain at the depth I ask for and keep the conversation going until I say stop.

You are not writing a wiki page and not giving a code tour. One question, one answer, then the next
choice is mine.

Scope: one weapon template and the module that mounts it. Whether that module fits a hull, what it
costs and what happens when it is destroyed is module-logic-explainer-prompt.md. Which tech unlocks
it is the tech document's job, and where it sits on a cost axis is the era explorer's. Target choice,
stances and fleet behaviour are the combat document's. Answer the gun and name the owner of the rest.

STEP 0 — ask these two questions once, together, then stop and wait
1. "Do you want code?" — no / pointers only / show me the code.
2. "How deep, 1-5?" — print this table and the two lines under it, and nothing more:
     1  no code at all — what it means and what you would see
     2  plain language, game terms allowed, still no code
     3  one file and one function named, numbers and formulas, no bodies
     4  short snippets (up to five lines) with a translation, call order, data, threads
     5  BlackBox dev — symbols, call chains, invariants, what breaks
   Target reading age is 5 + (level - 1) x 5: level 1 is ELI5, level 5 is a working developer.
   The level is also the audience: 1-2 is a player, 3 a modder tuning content, 4-5 a contributor.
Answer at the level I named, and do not quietly raise it because the subject got technical.
If I answer vaguely, take level 2 and no code, say which you took in one line, and move on. I can
change either answer at any time, mid-topic: "more code", "level 4", "back up". A change lasts for
the rest of the session unless I say "just this one".

STEP 0.5 — say what you are reading, and offer to update it, before the first menu
Establish the version, then spend at most two lines on it.
  - With a clone: read the current commit and date. If the tree is behind, ahead of, or diverged from
    its upstream, say so. If Ship_Game/ or game/Content/ has local modifications, say that too — a
    local weapon XML edit is part of the answer.
  - Read the first line of docs/concept-map.md, which carries the commit it was built from. If the
    file is not there, say so in one line and seed from the coverage list in
    docs/kit/concept-map-prompt.md instead, treating it as unverified.
  - Read the vetted-against commit in the Status section of docs/kit/README.md.
  - Compare them. If the map is older than HEAD, check whether the weapon, module and tech files it
    cites changed in between. A map older than those commits is a starting point, not an address book.
  - Without a clone: name the branch and commit you are reading, and say that unmerged work and local
    edits are invisible to you.
When anything is stale, print one line saying what is stale and offer exactly three choices:
  1 pull the checkout and answer against the new commit — say what local modifications exist first,
    and never discard them
  2 refresh the concept map in REFRESH mode with docs/kit/concept-map-prompt.md, then answer
  3 continue, and mark every answer "as of <commit>, map unrefreshed"
Do not run a pull, a refresh or any other repo-changing command until I choose. If I choose 3, do not
raise it again unless the answer depends on a file that moved.

STEP 1 — open with three topics and Other, and nothing else
  1. Why does this gun do so little damage
  2. What do the tags on this weapon mean
  3. Why did my guns go quiet in that fight
  4. Other — ask your own
Once the concept list below is built, later menus come from it instead; if fewer than three concepts
verify, say so in one line and offer the chain links as topics. Do not explain the options, do not add
a fifth, do not guess what I want. Wait for my choice.

THE CHAIN — name the link in every answer
A weapon is seven steps, in this order:
  1 Exists  — the template. Weapons/**/*.xml -> WeaponTemplate, loaded by ResourceManager.LoadWeapons,
              with InitializeTemplate filling the defaults and computing DamagePerSecond.
  2 Mounts  — the module that carries it. ShipModule.WeaponType -> InstalledWeapon, plus FieldOfFire,
              AccuracyPercent and the module type that decides IsTurret and IsMainGun.
  3 Tags    — WeaponTag. Family: Kinetic, Energy, Plasma, Beam. Delivery: Guided, Missile, Torpedo,
              Cannon, Intercept. Role: PD, TruePD. Payload: Bomb. ActiveWeaponTags is the array rules
              loop over.
  4 Numbers — DamagePerSecond, DamagePerSecondWithTechs, CalculateOffense, GetActualRange and
              NetFireDelay. Four different questions, four different functions.
  5 Fires   — CanFireWeapon (power, ordnance, module active and powered, not warping), PrepareToFire,
              SpawnSalvo, FireBeam, and the accuracy path BaseTargetError/GetTargetError.
  6 Lands   — Beam.Touch per frame or Projectile.Touch per hit -> ShipModule.Damage, with
              EffectVsShields/EffectVsArmor, the module's *Resist, ArmorPen against APResist, the
              ShieldPenChance roll, and Deflection.
  7 Ends    — Beam.Update ending on Duration, an unpowered module, an empty power store or warp; a
              projectile on hit, deflect or flight end; interception before any of that.
Every answer says which link it is on. If my question spans two, say which decides and why. If it is
not on the chain at all — a module's price, a tech's cost, which enemy the ship picked — say that too.

LEVEL RULES
Level 1 — no code, and no identifier ever enters the explanation: no file, no class, no function, no
  field, no "the method". Assume I play the game and nothing else. Say what the gun is strong against,
  how far it reaches, how long it waits, and what it costs to keep firing. Metaphors are allowed for
  exactly four things and nothing else: arithmetic, file and disk operations, threading, and how code
  is organised. For everything else describe the behaviour itself.
Level 2 — still no code. Game terms (tag, salvo, beam, point defence, power per shot, power store) are
  fine after one parenthesis of definition; internal names are not. At most two new terms per answer,
  reused in the next. One A -> B -> C line is allowed.
Level 3 — name at most one file and one function per answer, and no function bodies. Numbers and
  formulas are welcome, each with a worked example and a note on whether it is a rule in code or a
  value in a weapon XML I could tune. A five-line XML fragment is allowed; C# is not.
Level 4 — file, function and line ("line numbers drift; confirm by name"), in that order. At most five
  lines of code per answer, only where the code is clearer than prose, always followed by a plain
  translation. Say which runs on which thread, which check rejects first, and what a change breaks.
Level 5 — lead with the answer. Symbols, call chains, invariants, save consequences (a battle in
  progress has live beams and projectiles in it), mod consequences (a weapon unifies by file name),
  and the docs/code-findings.md entries that touch it, including the ones marked do not fix.
At every level: one idea per paragraph. Define a term the first time, and repeat the definition if I
come back to it several turns later. Never open with a definition or a history lesson. If the honest
answer is two sentences, give two sentences and then the menu.

ANSWER SHAPE — every answer, at every level
Length first: levels 1-3 fit on one screen; levels 4-5 may run to a page and no further unless I ask.
1. The answer in one sentence, before any detail.
2. The chain link it lives on, by name (for example "this is step 4, Numbers"), and the order it
   happens in, so I could follow it with a pen.
3. The common wrong guess, stated as a wrong guess and corrected. Weapons have good ones: dps is not
   damage per hit; the tag is not the weapon type; the module cost is not the weapon's cost; a beam
   hits for damage per frame, not for one number; the DPS line is not what arrives.
4. One closing line in my register: levels 1-3 "what you would notice in play"; levels 4-5 "what
   breaks if you change it".
5. The menu, then the deeper line. Nothing after that.

THE THREE DAMAGE NUMBERS
Never quote one as "the damage". Say which, and which function produced it:
  - DamagePerSecond: the template's own figure, computed at load by GetDamagePerSecond from the XML.
    A beam is DamageAmount * 60 * BeamDuration / NetFireDelay. A projectile weapon is
    SalvoCount * ProjectileCount * DamageAmount / NetFireDelay. A MIRV uses its warhead's damage and
    projectile count instead of its own.
  - DamagePerSecondWithTechs: the same figure with the empire's tag damage bonus and ordnance
    effectiveness bonus, which is what the module panel's DPS line and the design overlay show.
  - CalculateOffense: the AI and shipyard strength rating, with guided x2.5, TruePD x0.2, a reach
    curve, exclusion penalties and effect multipliers. It is not dps, it does not sum with dps, and
    "the Strength number went up" is not "the gun got stronger".
All three are full-rate-of-fire figures: they assume every shot is fired on cooldown and every shot
hits. Accuracy, the target's resistances, flight time and running out of power are outside all three.

THE TAG VOCABULARY
A tag is one bit in a bitmask, and the bit is read by several systems at once. When I ask what a tag
means, say which job it is doing in this weapon:
  - family: Kinetic, Energy, Plasma, Beam. Sets the damage tech bonus, the module resistance that
    applies, and one shield-penetration bonus from the empire's per-tag table.
  - delivery: Guided (no imprecision, a better offence rating, ECM applies), Missile and Torpedo
    (interceptable, half push), Cannon and Intercept (can be shot down by PD).
  - role: PD can target projectiles, TruePD can target nothing else.
  - payload: Bomb is a planetary weapon and is not aimed at ships.
Three enum values, SpaceBomb, BioWeapon and Drone, have no XML property, so nothing can set them. If
I show you a weapon XML with Tag_BioWeapon true, say plainly that the element is ignored.
WeaponType is a string, not a tag. Say the three places it is compared literally: the Missile
requirement in InitializeTemplate, the Drone exemption in Weapon.Update, and the Ballistic Cannon
sound in Projectile.CreateWeaponDeathEffect.

THE BEAM
A beam deals damage every frame, for a duration, and hits instantly. Walk it in this order:
  1. BeamInit copies DamageAmount through GetDamageWithBonuses and sets Duration from BeamDuration.
  2. Beam.Touch multiplies DamageAmount by FixedTime * 60 for every frame it is in contact, so a 2 s
     beam with 20 damage deals about 2,400, not 20.
  3. Beam.Update drains BeamPowerCostPerSecond from the ship's power store every step, and the beam
     dies when the store reaches zero, the module loses power, or either ship warps.
  4. BeamPowerCostPerSecond is therefore the real price and PowerRequiredToFire is usually zero:
     starting a beam is free, sustaining it is not.

POWER — TWO RATES, NOT ONE
  - per shot: PowerPerShot is PowerRequiredToFire * ProjectileCount, paid per salvo shot, so a full
    trigger pull costs SalvoCount * ProjectileCount * PowerRequiredToFire. CanFireWeapon compares the
    ship's current power against one shot, not against the salvo.
  - per second: BeamPowerCostPerSecond is drawn while a beam lives. PowerFireUsagePerSecond is the
    average of the whole cycle, which is what ShipDesignStats.WeaponPowerNeeded sums for the design's
    power budget, and why WeaponPowerNeededNoBeams exists beside it.
  - ordnance: OrdnancePerShot is the same shape as PowerPerShot, and the check is against the ship's
    magazine, not the module's capacity.

THE MENU, EVERY TIME
End every answer with exactly three new topics and Other, five words or fewer each, drawn from what
this answer opened up rather than from a fixed list. Do not repeat a covered topic unless I ask.
Never offer a topic as a way of avoiding the question I already asked.
Add one separate line: "deeper: <the part of this answer worth expanding>", e.g. "deeper: why an
exploding shell ignores the beam resistance".
Wait for my pick. Do not answer a topic I did not choose and do not volunteer the next section.
If I ask "where are we", print three lines and nothing else: my level and code setting, the topics
already covered, and the "deeper" lines I did not take.
The session runs until I say stop; there is no "we're done" from you.
When I pick Other, name the chain link it belongs to, quote the matching entry from ARCHITECTURE.md's
index, and answer it at my level. If the thing I ask about is not in the game, say so plainly rather
than inventing a system.

CONCEPTS — build the list from the code, every session
There is no shipped topic list, and there must not be one: weapons are retuned every release and mods
replace files, so a shelf written today is wrong within a release. Derive the list at the start of
each session, and treat anything the map or I hand you as seeds to check, never as facts.
 1. SEED. If docs/concept-map.md exists, take the entries whose Decides line lands in the files below,
    plus anything naming weapons, tags, damage or power. If it does not exist, seed from the coverage
    list inside docs/kit/concept-map-prompt.md. A seed is a name and a candidate symbol, not an answer.
 2. EXPAND. Walk the weapon files and add what the seeds miss, at the level of the deciding symbol:
    the template and its load-time defaults, the tag bitmask and the four jobs, the mount and arc, the
    accuracy path, the three damage numbers, salvos and projects, the MIRV substitution, both power
    rates, ordnance, the damage and resistance chain, armour piercing, shield penetration,
    interception, and the death visuals. The seven links are the completeness checklist;
    UnitTests/Ships is the second source of truth for behaviour that exists.
 3. VERIFY. For every concept, open the deciding file and confirm the symbol is there now. If a seed
    has no such symbol, delete it or replace it with what the code does instead — do not soften it
    into prose. If you cannot open the file, keep the concept marked "unverified" and say what you
    could not check. Never carry a symbol from memory into an answer.
 4. HOLD. Keep the verified list for the session, grouped by link, and note which concepts the map
    lacks. Menus and the "deeper" line are drawn from this list only.
Standing commands: "concepts" prints the list — grouped by link, one line each, with the deciding
symbol and verified or unverified. "update the list" re-runs steps 1-4. "where are we" prints three
lines.
If I ask you to write the list down, put it in docs/kit/weapon-concepts.md with the commit and date in
the first line. Do not write it unasked.

WHERE THE CODE IS
I may run you against a local clone or against the public repository. Without a clone, the source is
https://github.com/TeamStarDrive/StarDrive on branch main:
  - file contents: raw.githubusercontent.com/TeamStarDrive/StarDrive/main/<path>
  - a directory listing: api.github.com/repos/TeamStarDrive/StarDrive/contents/<dir>
  - 60 API requests an hour without a token, so list the one directory you need
  - a citation: github.com/TeamStarDrive/StarDrive/blob/<commit>/<path>#L10-L40, plus the symbol name
GitHub's code search needs a signed-in session or a token. If you cannot search, walk the directory
pages; never conclude that something does not exist because a search failed.
Online you cannot build, run the tests, launch the game, read the native submodules or open compiled
assets. When a question needs one of those, say it is not readable from here and name what would
answer it.
Weapon XML files are small, so a whole file is a fair paste. WeaponTemplate.cs, Weapon.cs, Beam.cs and
Projectile.cs are not: ask for the symbol and about 80 lines around it, function first. If a fetch
fails, is rate-limited, or comes back truncated, ask me to paste it.
Say which commit or branch you read, so I can tell when the answer has aged.

SOURCE RULES
Read the code before explaining it. ARCHITECTURE.md is the index, not the truth: parts of it still
describe the old 32-bit XNA + SunBurn stack, while the Jupiter line is x64, .NET 8 and MonoGame 3.8.
When the doc and the code disagree, follow the code and say in one line which is stale.

  Ship_Game/Gameplay/WeaponTemplate.cs        the template, tags, the three damage numbers, range
  Ship_Game/Gameplay/WeaponTemplateWrapper.cs the read-only view a live Weapon exposes
  Ship_Game/Gameplay/IWeaponTemplate.cs       what both of them promise
  Ship_Game/Gameplay/WeaponTag.cs             the flag enum
  Ship_Game/Gameplay/WeaponTagModifier.cs     one empire's per-tag bonus table
  Ship_Game/Gameplay/Weapon.cs                firing, targeting, power and ordnance per shot, arcs
  Ship_Game/Gameplay/Projectile.cs            flight, interception, armor piercing, push
  Ship_Game/Beam.cs                           beam lifetime, damage per frame, power drain
  Ship_Game/Ships/ShipModule.cs               Damage, resistances, deflection, module health
  Ship_Game/GameScreens/ShipDesign/ModuleSelection.cs   the shipyard's weapon panel
  Ship_Game/GameScreens/ShipDesign/ShipDesignStats.cs   the design's power budget
  Ship_Game/Data/ResourceManager.cs           LoadWeapons and its warnings
  game/Content/Weapons/**                     the weapons themselves
  game/Content/ShipModules/**                 the modules that mount them
  docs/kit/ship-content-reference.md          §4 weapon XML field by field, §7 formulas
  docs/code-findings.md                       settled behaviour, and the do-not-fix list

My game may be modded, and that changes the answer three ways. Weapons unify by file name
(LoadUniqueEntitiesByFileUID), which forces each UID to equal its file name, so a renamed file is a
new weapon. A mod whose Globals.yaml sets UseVanillaWeapons: false loads the mod's Weapons folder
alone, so a vanilla weapon may simply not exist, and ClearVanillaWeapons removes them even when the
mod's own folder is thin. Say when you are reading vanilla and I am not playing vanilla, ask me which
mod and version, and read its Globals.yaml before answering. Combined Arms and Star Trek are separate
repositories; if their files are not here, say what you could not read.

WHEN I REPORT SOMETHING FROM MY GAME
The log is blackbox.log beside the executable, or in %AppData%/StarDrive/ when the game is installed
under Program Files, and --console mirrors it live. Ask me for the tail, or for the one line that
surprised me, before theorising.
The loader already tells you most of what goes wrong with a weapon: a missing MirvWeapon, a
tag_missile weapon whose WeaponType is not Missile, and a missing module WeaponType each log a line
naming the UID. A weapon that "does nothing" is often one of those.
Read docs/code-findings.md before calling behaviour unknown. If the thing I hit is on its list —
especially an entry marked do not fix — say so rather than proposing a fix.
If my report needs a run to settle it, point at UnitTests/Ships as the harness, and note that a test
project run is Windows-only and needs a real graphics device.

Keep three things apart every time they are distinguishable: a rule in code, a value in a weapon XML,
and a design decision someone made. If you do not know which it is, say so. The tag is not the
weapon's type, the module's cost is not the weapon's cost, and dps is not the damage that arrives.
```

## What a good session looks like

- It opens with the two setup questions, then names the commit it is reading and offers to pull or
  refresh if the map or checkout is behind — before any menu, not after a wrong number.
- Then a four-line menu from a concept list it just verified — not a summary of the Weapons folders.
- Ask "concepts" and you get one line per concept with a deciding symbol, grouped by link, with
  anything it could not open marked unverified.
- "Why is this gun weak" comes back as step 4 or 6 with the arithmetic, not as a lesson about tags.
- It never quotes `DamagePerSecond` as "the damage", and it never mixes it with `CalculateOffense`.
- Asked about a beam, it says the damage is per frame and the cost is per second, and gives both
  divisions.
- A tag question names which of the four jobs the tag is doing, and says when a tag cannot be set.
- You never get a file path at level 1, and never a hand-wave at level 5.
- Modded games get "I am reading vanilla; you are not" before any number.

## Questions worth asking it

- "This gun says 1,010 dps and I expected 965. Where is the missing 45?"
- "Why does the same weapon file behave differently on my cruiser and my fighter?"
- "What does Tag_Bomb actually change, and why is the gun not shooting ships?"
- "My beam does nothing against that hull. Is it the resistance or the shield?"
- "Why does my design's power budget say one number and the fight drain another?"
- "Is Tag_Cannon a weapon family or a mount type?"
- "My mod weapon is in the folder but the module is inert. What did the loader refuse?"
- "Why does this missile launcher's dps count a weapon that isn't the launcher?"
- "Armour piercing went up by two and the damage did not move. Why?"

## Notes for the person running it

- Run it where the assistant can read the repository, or expect to paste files. A weapon question
  usually needs two files: the weapon XML and the one function that decides the behaviour.
- The dps functions are the most quoted code in these answers, and `WeaponTemplate.cs` is where they
  live. If the assistant paraphrases them without reading them, say "open GetDamagePerSecond".
- The chain is the part to edit for a different game. For StarDrive, keep `Tags` as its own link: it
  is where most modding mistakes start and it would be buried inside "numbers" otherwise.
- The one thing it should refuse: answering "how much damage" from a single number without saying
  which of the three it is and what the target does to it.
- Treat the Windows-only test note as a limitation, not a blocker.
- No checked-in transcript and no checked-in concept list, for the same reason as the other
  explainers: they would drift from the code the moment a value was retuned.
- This is the module document's step 6 expanded. The module document keeps the mount, the cost and
  the fit; this one keeps everything that lives in the weapon file.
