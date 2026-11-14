# The strategy brief — an interactive prompt for AI ship-building

A copy-paste prompt that makes an AI ship-builder *ask you what your fleet is for* before it
designs anything, then hold that answer for the whole tech progression.

Use it with the reference doc: [`ship-content-reference.md`](ship-content-reference.md) is the
mechanics. This file is the conversation that decides which mechanics to spend.

## Why this exists

A design generator given no strategy produces the average of every design it has seen. It will
give you a frigate with a bit of everything, at every tech era, forever. The output is legal and
forgettable. The reason is not a knowledge gap — the AI knows the fields — it is that **a design is
an answer, and it was never told the question.**

So the question comes first, in writing, and the AI is not allowed to propose a hull until you have
answered it. That written answer is the *strategy brief*, and it is the thing you re-read when a
design looks wrong.

## Is "ships are characters" the right frame?

Half right, and worth keeping the useful half.

Where the metaphor earns its place: a fleet that reads as a *cast* — a scout who is quick and
nervous, an old battleship nobody replaces, a cheap escort built to be lost — produces designs that
differ from each other on purpose. Names, silhouettes, roles and refits then have somewhere to hang.
That is real, and it is what makes a fleet feel authored instead of enumerated.

Where it misleads: a character can be interesting while being useless. In this game every design is
scored, costed and bought by an AI opponent that does not care about its personality. Two hard
mechanics decide whether your cast survives contact:

- **Strength is the game's own opinion of your ship** (§7.1 of the reference). It is
  defence-aware but offence-weighted: a hull whose defence exceeds its offence *and* whose weapons
  cover under 10% of its surface area scores as `2·offence + 0.1·defence`. A deliberately
  turtle-ish "character" reads to the enemy AI as a weak ship and gets attacked. If you want a
  defensive doctrine, it has to be defensive *and* offensively credible, or it has to be something
  the enemy cannot profitably attack at all (range, speed, screening).
- **A design that no tech lists is invisible** (§5.3). Unlockability is derived by walking module →
  tech → prerequisites, with no field anywhere that says "this design exists now". Your cast only
  appears on stage if the tech ladder is written to bring it on.

So: keep the cast, but the load-bearing sentence is not "who is this ship" — it is **"what problem
does this ship solve that the previous era's ships could not, and what does it make obsolete?"**
That is a sentence a design can be wrong about, which the character framing never is.

## The prompt

Paste everything between the rules into a fresh conversation, with the reference doc attached or
linked. It is written to run over several turns; it will refuse to design until Phase 0 is answered.

---

You are helping me build a fleet **as a strategy made concrete**, for StarDrive BlackBox.

Attached is `ship-content-reference.md`: the authoritative mapping from content files to game code,
including the strength, cost, mass, power and role formulas, the slot-restriction rules, and the
invariants that break a design silently. Treat it as the mechanics. Do not contradict it, and cite
the section number when a rule constrains a design decision.

Your job is not to generate ship ideas. Your job is to extract **my** strategy from me, then express
it as a tech-ordered sequence of ship designs, and then check that sequence against the mechanics
before I build any of it.

### Rules for you, the assistant

1. **One question at a time.** No questionnaires, no numbered lists of ten questions. Ask the
   single most load-bearing question, wait, then ask the next. Every question offers a default
   guess so I can say "yes" and move on.
2. **No designs before Phase 0 is complete.** If I ask for a ship early, say which unanswered
   question blocks it and ask that.
3. **Prefer my words over your taste.** If I say "cheap and expendable", a design that is merely
   adequate is a failure, and you should say so plainly.
4. **Every design must name the era it appears in, the problem it solves, and the earlier design
   it replaces or the gap it fills.** If it does none of those, delete it.
5. **Cite mechanics, never invent them.** Hull role legality, module restrictions, command modules,
   PD coverage, hangar launch chains and the strength formula are all in the reference. If a
   question needs a number the reference does not have, say so instead of guessing.
6. **Keep a running brief** in a single Markdown block you reprint when it changes: one sentence of
   premise, then the era table. I will copy it out.
7. **When I contradict myself, stop and name the contradiction** rather than averaging the two
   answers into a design that is bad at both.

### Phase 0 — the interrogation

Get answers to all of these before designing. Ask them in whatever order the conversation makes
natural, but do not skip any.

- **The premise.** In one sentence: how does this empire win? Not "conquer" — the actual mechanism,
  e.g. "hold three chokepoints until the enemy's economy starves", "out-range everything and never
  take a fair fight", "arrive with more hulls than they can shoot".
- **The enemy's answer.** Who beats that plan, and what do they field? If my premise has no counter,
  the premise is wrong — say so.
- **What I refuse to do.** The doctrine's prohibitions matter more than its goals: no carriers, no
  capitals before turn N, nothing that needs a hull I do not own. These become hard constraints.
- **The economy this has to fit in.** Which resources am I rich in, and what is my per-ship cost
  ceiling at each era? Designs are bought, not awarded.
- **Tempo.** Do I want to be dangerous at era 2 and spend eras 4–6 catching up, or the reverse?
  This decides whether a design is an *interim* (cheap, obsolete soon, must not cost tech) or a
  *keystone* (expensive, must stay relevant for three eras).
- **The refit story.** Which ships am I willing to keep building for the whole game, and which are
  disposable? A design that nobody would ever want a second of is a mistake unless it is meant to
  be lost.
- **The voice.** Names, factions, the aesthetic the cast belongs to — this is where the character
  framing lives. It costs nothing and it makes the fleet legible to a human reading it.

### Phase 1 — the era ladder

Convert the premise into **eras defined by tech, not by turns.** For each era, produce a row:

| Era | Techs taken (and why) | Modules that become legal | Designs that appear | Designs that die | Cost ceiling |

Rules for this table:

- **Order matters and closure is real.** A design is only unlockable if every module it uses is
  reachable through some tech's prerequisites, and the design's research cost is the sum over that
  closure (reference §5.3). A design using one module from the far end of the tree drags the whole
  path into its cost. If the ladder says "era 3 frigate", every module on it must be reachable by
  era 3 — check it, do not assume.
- **Each era must answer a threat the previous era could not.** If two eras' designs solve the same
  problem, merge them and say which one you deleted.
- **Name the module class, not the module.** "PD that can actually kill missiles", "a command
  module that is not the cockpit", "shields above X". Then I will pick the exact UIDs.
- **Respect the hull.** Slot count *is* surface area (§2.2), which is the denominator of both the
  strength formula and the PD-coverage warning (§7.8). A hull with few slots cannot carry a
  broadside no matter what the brief wants.

### Phase 2 — the design briefs

For each design that survives Phase 1, produce exactly this block. No prose before it.

```
DESIGN: <name>            ERA: <n>   HULL: <Style/HullName>   ROLE INTENT: <role>
SENTENCE: <what problem this solves, and what it replaces>
ENEMY IT IS BUILT TO BEAT: <specific threat, from Phase 0>
MUST HAVE:     <modules/effects that define it — the things whose absence makes it a different ship>
MUST NOT HAVE: <what would make it an average ship>
COST TARGET:   <ceiling from the era table>   MASS/POWER NOTE: <if the hull is tight>
FAILS IF:      <the single most likely way this design silently breaks>
CHECK:         <which invariants from reference §8 apply here, by number>
```

Then, for the set as a whole, one paragraph: **what the fleet cannot do.** A doctrine with no stated
blind spot has not been decided, only described.

### Phase 3 — the audit

Before I build anything, audit your own output:

1. Does every design appear in an era where all of its modules are actually reachable?
2. Does every design pass reference §8 — one command module, one command module *plus* a backup on
   large hulls, legal restrictions per slot, PD coverage on anything with 500+ slot area, targeting
   coverage (anti-fighter *and* anti-capital) on large craft?
3. Does any design's strength profile read as weak under §7.1 — defence-heavy with under 10% of
   surface area in weapons? If yes, either justify why that is the point, or fix it.
4. Do the hangars launch things that exist *earlier* than the carrier that launches them? A carrier
   whose fighter is a later era than itself is a bug, not a plan.
5. If I deleted the cheapest design in each era, would the doctrine still work? If yes, that design
   is decoration.
6. Is there a design whose only purpose is a number going up? Delete it.

Report the audit as a list of findings, each either CLEAN or a specific defect with the design name.

### Phase 4 — handoff

Produce, in this order: the one-sentence premise, the era table, the design blocks, the blind-spot
paragraph, the audit. Then stop and ask me which single design to build first — not all of them.

---

## After the brief: making it true

The brief is paper. Three things turn it into ships, and they answer different questions.

**1. Does it parse and score as intended?** Compute cost, mass, power, role and strength offline
from the text files (reference §9), then confirm the role with `StarDrive.exe --fix-roles` — the
game's own derivation is the only authority on what your design *is*. This catches the ten silent
failures in §8 and nothing else.

**2. Does it arrive at the right time?** Jump the tech ladder and look. `ResearchDebugUnlocks`
(`Ship_Game/GameScreens/Universe/Debug/ResearchDebugUnlocks.cs`) already does this, as debug hotkeys
plus static methods callable from a test: unlock everything, unlock one race's tree, run the AI's own
research planner, or unlock only the current topic. The planner run is the useful one — if the AI's
research order disagrees with your era table, your ladder is a wish, not a plan.

**3. Does it actually fight?** This is a different question, and it is not answerable from a
spreadsheet. A design can pass every invariant and still lose to the thing it was built to beat.

There is no need to add an in-game API for this — the project already has a headless combat harness
in `UnitTests/`:

- `UnitTests/StarDriveTest.cs` builds a universe, one player and one enemy empire, optionally at war
  (`CreateUniverseAndPlayerEmpire`), a sandbox of any galaxy size with extra ships per empire
  (`CreateCustomUniverseSandbox`), and loads only the content you ask for (`LoadStarterShips`,
  `LoadAllGameData`).
- `UnitTests/AITests/Ships/ShipAICombatTests.cs` is a working example of exactly the loop you want:
  spawn ships at chosen positions with `SpawnShip(name, empire, pos)`, disable firing with
  `AI.SetCombatTriggerDelay`, step the world a fixed amount with `RunObjectsSim` / `RunSimWhile`, and
  read the outcome off ship health, module state and combat logs. `TestShip` wraps a spawned ship and
  exposes its weapons for inspection — including temporary overrides, which is how you isolate one
  variable instead of rebalancing the world.

So the shape of a design experiment is: **one test method per hypothesis**, two arms differing in one
thing, a fixed number of simulated seconds, and an assertion on the result rather than a screenshot.

### What has to be compiled, and what does not

There are two different loops here and it is worth being clear which one costs a build.

**The design is data.** Tests do not contain ships. `StarDriveTestContext` sets the working directory
to `game/`, and `ResourceManager.LoadStarterShipsForTesting` scans
`Content/ShipDesigns/**` with `GatherFilesUnified("ShipDesigns", "design")`, caching each design
under its **file name**. `LoadStarterShips("My Escort mk1")` then loads `My Escort mk1.design` from
that scan, and throws `FileNotFoundException` naming the folder if it cannot find it. So a design is
referenced by the file name, which must match the design's own `Name` — the writer guarantees that,
hand-edits do not.

- **Editing a ship — no compile.** Drop the `.design` in `game/Content/ShipDesigns/`, run the test,
  read the result. Only the content is re-read.
- **Changing the experiment — compile.** A test is C#, and this project sets
  `EnableDefaultCompileItems=false`, so a new file needs its own
  `<Compile Include="Ships\MyTests.cs" />` in `UnitTests/SDUnitTests.csproj`, or it silently does
  not exist.

That is the honest answer to "do we write the tests by hand and compile them": yes for the
scenario, which you write once per hypothesis; no for the ships, which is where the iteration volume
actually is.

### A minimal experiment

```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;
using UnitTests.Ships;
using Vector2 = SDGraphics.Vector2;

[TestClass]
public class MyDesignMatchupTests : StarDriveTest
{
    public MyDesignMatchupTests()
    {
        LoadStarterShips("My Escort mk1", "My Raider mk1");
        CreateUniverseAndPlayerEmpire("Human");
        UState.Objects.EnableParallelUpdate = false; // determinism beats speed here
    }

    [TestMethod]
    public void EscortSurvivesTheRaider()
    {
        TestShip escort = SpawnShip("My Escort mk1", Player, new Vector2(0, 0));
        TestShip raider = SpawnShip("My Raider mk1", Enemy,  new Vector2(0, -800));
        escort.AI.SetCombatTriggerDelay(0f); // 0 = weapons hot now
        raider.AI.SetCombatTriggerDelay(0f);

        RunSimWhile((simTimeout: 60, fatal: false), () => raider.Active, () =>
        {
            Assert.IsTrue(escort.Active, "escort died before the raider");
        });

        Assert.IsFalse(raider.Active, "raider survived 60 simulated seconds");
    }
}
```

Run it with `dotnet test UnitTests/SDUnitTests.csproj --filter "FullyQualifiedName~MyDesignMatchupTests"`.
Every step is a fixed `1/60` second (`TestSimStep`), there is no simulation thread, and the outcome is
read off `TestShip`'s own counters (`NumDieCalls`, `NumModuleDeaths`, `DeadModules`) or plain ship
state rather than a rendering.

Two practical notes. Compare arms **within one run**, not across runs: the universe has its own random
state and floats drift. And `Log.Write` inside a test lands in the game log, so a failing run can be
re-read after the fact rather than re-run with prints added.

### Platform caveat

The test project targets `net8.0-windows` with MonoGame `WindowsDX` and copies `SDNative.dll` and
`libfbxsdk.dll` from `game/`, so this harness runs on **Windows on x64 only**. It does not run on
Linux or macOS, and it needs a real graphics device even though `TestGameDummy` creates a hidden
window. If the experiment loop needs to run somewhere else, that is a port, not a flag.

If the scenario count grows past a handful, the next step is one compiled test that reads an
**experiment file** (two design names, spawn distance, seconds, expected outcome) and writes a CSV row
per run. Then a new experiment is data, the harness is compiled once, and an AI can propose, run and
tabulate trials without touching C#.

Keep the brief and the evidence apart. The brief says what you meant; the fight says whether you
were right. When they disagree, the brief is what you change — after you understand why.
