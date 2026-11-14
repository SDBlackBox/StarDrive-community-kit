# How the AI decides where to colonize — a copy-paste explainer prompt

Paste the prompt below into an AI assistant that can read this repository, and it will walk you
through the AI's colonization logic in plain language — why the AI settles the planet it settles,
where each decision is made in the code, and how a race's traits change the answer. It is written
for people who do not know this codebase and may not write code at all, and it is meant to be
interrupted with questions.

## Why this exists

In play, AI expansion looks arbitrary: it sails past a fertile world and settles a barren rock two
systems away. Underneath, it is a short deterministic pipeline — a handful of gates, one score per
planet, one target per run — spread over five code files and two content files. Read cold, the
pipeline is hard to assemble; asked cold, an AI tends to answer "the AI scores planets by value"
and stop there. This prompt supplies the map, the audience rules and the traits angle, so the
explanation is specific instead of generic.

## Where the logic lives

Every link is pinned to the commit this document was written against
(`f575899`), so the line numbers stay valid. The same list is inside the prompt as plain paths.

| What it does | Where it is |
|---|---|
| The loop, the gates, picking the best planet | [`ExpansionPlanner.RunExpansionPlanner`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/ExpansionAI/ExpansionPlanner.cs#L124) |
| How many colonies the AI wants | [`DesiredColonyGoals`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/ExpansionAI/ExpansionPlanner.cs#L67), [`AtColonyGoalCap`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/ExpansionAI/ExpansionPlanner.cs#L187) |
| The two "not yet" gates: population and difficulty timer | [`CanConsiderExpanding`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/ExpansionAI/ExpansionPlanner.cs#L91) |
| Which planets are even allowed | [`CanBeColonized`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/ExpansionAI/ExpansionPlanner.cs#L306) |
| The score, the distance and enemy penalties, the "don't settle their space" rule | [`PlanetRanker`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/ExpansionAI/PlanetRanker.cs#L32), [`IsColonizeBlockedByMorals`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/ExpansionAI/PlanetRanker.cs#L58) |
| What a planet is actually worth | [`Planet.ColonyPotentialValue`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Universe/SolarBodies/Planet/Planet.cs#L545) |
| The six-step "go build a colony ship and take the planet" routine | [`MarkForColonization`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Commands/Goals/MarkForColonization.cs#L27) |
| Traits: cybernetics, home environment, expansion personality | [`Empire.IsCybernetic`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Empire.cs#L222), [`Empire.IsExpansionists`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Empire.cs#L237), [`RacialEnvModifer`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Empire.cs#L506) |
| Where the trait numbers come from | [`RacialTraits.xml`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/game/Content/RacialTraits/RacialTraits.xml#L175) (Cybernetic), [Aquatic](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/game/Content/RacialTraits/RacialTraits.xml#L420), [Explorers](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/game/Content/RacialTraits/RacialTraits.xml#L447), [`EconomicResearchStrategies.yaml`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/game/Content/EconomicResearchStrategies.yaml#L3) |
| Difficulty knobs (goal counts, how often it checks) | [`DifficultyModifiers`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/EmpireDifficultyModifers.cs#L7) |
| The tag that makes a ship a colony ship | [`ShipDesign_Stats.IsColonyShip`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/Ships/ShipDesign_Stats.cs#L130) |
| Which colony ship the AI builds | [`ShipBuilder.PickColonyShip`](https://github.com/TeamStarDrive/StarDrive/blob/f575899fe199f9b622bc47146d68ce4e2e75ff14/Ship_Game/AI/EmpireAI/ShipBuilder.cs#L187) |

## The prompt

Everything between the rules; the reader does not need to edit anything.

```text
You are explaining StarDrive BlackBox's AI colonization logic to me, a person who does not know this
codebase and may not write code at all. I want to understand the logic, not learn C#. Assume I know
the game — planets, colony ships, races, traits — but nothing about how it is implemented.

We will go through it in sections and I will ask questions as we go. Do not dump the whole thing in
one message.

SOURCE OF TRUTH
This is the StarDrive repository at commit f575899fe199f9b622bc47146d68ce4e2e75ff14. Read the code
before you explain it; do not work from general knowledge of 4X games. These are the files, in the
order they matter:

  Ship_Game/AI/EmpireAI/EmpireAI.cs                                  (call site, lines 159-160)
  Ship_Game/AI/ExpansionAI/ExpansionPlanner.cs                      (the whole decision loop)
  Ship_Game/AI/ExpansionAI/PlanetRanker.cs                          (scoring one planet)
  Ship_Game/Universe/SolarBodies/Planet/Planet.cs                   (what a planet is worth, ~line 545)
  Ship_Game/Commands/Goals/MarkForColonization.cs                   (turning a target into a colony)
  Ship_Game/Empire.cs                                               (IsCybernetic 222, IsExpansionists 237,
                                                                      RacialEnvModifer 506, AutoColonize 144)
  Ship_Game/Empire_Relationship.cs                                  (GetExpansionRatio, line 131)
  Ship_Game/EmpireDifficultyModifers.cs                             (per-difficulty numbers)
  Ship_Game/Data/RacialTrait.cs                                     (trait fields, 80-104)
  game/Content/RacialTraits/RacialTraits.xml                        (trait values: Cybernetic 175, Aquatic 420,
                                                                      Explorers 447)
  game/Content/EconomicResearchStrategies.yaml                      (Expansionists)
  game/Content/Globals.yaml                                         (RequiredExpansionPopRatio, line 23)
  Ship_Game/Ships/ShipDesign_Stats.cs                               (IsColonyShip, line 130)
  Ship_Game/AI/EmpireAI/ShipBuilder.cs                               (PickColonyShip, line 187)

If you cannot open a file, say so and ask me to paste it — do not fill the gap from memory.

AUDIENCE RULES
- Explain the logic as a sequence of decisions a person could follow with a pen: "first it asks X,
  if no it stops, otherwise it does Y". Name the game concept, not the variable, unless the variable
  name is the point ("the game calls this ColonyPotentialValue").
- Define every piece of jargon once, in a parenthesis, the first time you use it.
- Never show more than five lines of code at a time, and only when the code is clearer than prose.
  Always follow it with a plain-language translation.
- Use one concrete example with a made-up planet pair when a rule is numeric, and say the numbers are
  illustrative unless the code gives exact ones.
- End every section with "what this means in play": one or two sentences on the effect a player
  would notice.
- Keep a running glossary. Repeat a term's definition if I come back to it after a while.
- If something is a design choice rather than a derived rule, say so, and say which file you know it
  from. If you do not know, say "the code does not answer that" and tell me what would.

SECTION 1 — the shape of it
Give me the one-paragraph summary first: the AI keeps a small number of colonization goals alive, and
on each AI turn it may add one new goal, which is then carried out by a separate goal object. Say
where the turn-level call happens (EmpireAI, lines 159-160: RunExpansionPlanner then
SwitchColonyGoalsToFoundPlanets) and that only one new target is created per run.
Then stop and ask if the shape makes sense before going into detail.

SECTION 2 — the gates, in order
Walk the decision in the order the code runs it, and say what happens at each gate when the answer is
"no":
  1. Is this the player? If so, nothing happens unless AutoColonize is on (Empire.cs 144).
  2. Keep enough idle colony ships around (StandbyColonyShip goals) so a target can be acted on.
  3. CanConsiderExpanding (ExpansionPlanner.cs 91): a difficulty timer (ExpansionCheckInterval —
     every 7 / 5 / 3 / 1 turns), then a population gate — the empire must use a fraction of the
     population it could support (RequiredExpansionPopRatio, 0.4 in content/Globals.yaml, scaled by
     difficulty), and Expansionists get a 25% discount on that requirement.
  4. AtColonyGoalCap (187) against DesiredColonyGoals (67): base goal count by difficulty, plus a
     race/strategy term, plus 2 for cybernetic empires, plus a catch-up term when the empire is
     behind on planet count (after star date 1002).
  5. Gather candidates: every legal planet in systems it already owns, plus legal planets in nearby
     systems it has explored (the number of systems checked grows over time; Expansionists check
     roughly a quarter more per pass).
  6. Score every candidate, throw away the ones flagged "don't colonize", take the highest, and turn
     it into a goal. Explain that already-targeted planets are skipped, so the AI does not send two
     colony ships to one world.
Explain "legal" precisely, from CanBeColonized (306): explored, habitable, far enough from the star's
radiation, not in another empire's post-loss grace window, and either unowned or held by a minor
faction it can take. Also explain StrongEnoughToClaim, which compares the enemy strength it knows
about in that system against its own offensive strength.
Stop and ask me which gate surprised me.

SECTION 3 — the score
This is the heart, so take it slowly. Explain Planet.ColonyPotentialValue (545) as "what this planet is
worth to THIS empire":
  - organic empires: fertility potential squared times 50, plus a little for mineral richness;
  - cybernetic empires: mineral richness times 10 plus a bonus per volcano, and fertility is ignored;
  - both: special commodities, potential maximum population scaled by how much of the planet is
    habitable, and a bonus if the system has a Dyson swarm.
Then explain PlanetRanker (32): if the planet is in a system the empire already owns, the score stands
as is; otherwise it is divided by a distance factor and by an enemy-strength factor, each clamped
between 1 and 10, so a far or well-defended world can be worth at most a tenth of its raw value.
Also explain the hard floor: a world outside the empire's own systems is only considered if its raw
value clears 20, or — for cybernetic empires — if its mineral richness is above 1.5.
Then explain the morals rule (IsColonizeBlockedByMorals, 58): the AI refuses to settle a system that
another empire already holds planets in, unless it has warned them off, has open borders, or is at war
with them; minor factions and unsettled systems are exempt.
Stop here; this is the section people most want to argue with.

SECTION 4 — from target to colony
Explain the six steps of MarkForColonization (27) as a checklist with a failure path at each step:
claim the system militarily if there is enemy presence (and ask for a guard fleet on harder
difficulties), re-check the target is still legal, find an idle colony ship or queue one at a
suitable port (rush-building it if the treasury allows), wait for it, send it, wait for the landing.
Mention that when a target stops being legal the goal is failed and the ship is released rather than
wasted, and that the goal can change target until it is committed.
Also explain the mid-run correction: scouts report planets as they explore; next turn a newly found
planet may replace the weakest existing target, but only if it scores more than a quarter higher
(1.25 in SwitchColonyGoalsToFoundPlanets, 207) — and the player gets a notification when that
happens. Explain why the two-turn delay exists (the threat memory needs to catch up with what the
scout saw).

SECTION 5 — racial traits
This is the part I care most about. Do not go trait by trait through the whole file; group by the
mechanism, and for each group say exactly which line of logic changes, then give one worked example.
Cover at least:
  a) Cybernetic (RacialTraits.xml 175; Empire.IsCybernetic 222). It changes the value formula itself
     (richness and volcanoes instead of fertility), gives +2 colony goals, adds 1 to the expansion
     ratio, lets a mineral-rich world pass the value floor, and changes what a new colony does with
     its workers (food allocation is zero; production and research split the rest). Consequence:
     cybernetic empires settle different worlds than organic ones do, not merely more of them.
  b) Home environment traits — Aquatic is the clean example (RacialTraits.xml 420): PreferredEnv plus
     a multiplier per planet type. Trace it: RacialEnvModifer (Empire.cs 506) multiplies fertility
     (Planet.cs 145) and potential maximum population (Planet.cs 159 and following), and both feed
     the score. Show the arithmetic for an Aquatic empire looking at an Oceanic world and a Desert
     world, and note the same multiplier also decides how big the colony can eventually grow.
  c) Economic personality — Expansionists (EconomicResearchStrategies.yaml, Empire.IsExpansionists
     237). It lowers the population gate by 25%, makes the AI scan more systems per pass, adds to the
     desired goal count, makes it rush colony ships at a worse credit rating, and gives colony ships a
     better place in build queues. Be explicit that this is a multiplier on how hard the AI pushes,
     not a change to what it values.
  d) Traits that only matter indirectly: combat-oriented traits change the strength comparisons in
     StrongEnoughToClaim and the claim fleet, and exploration traits (Explorers: three times the
     exploration radius, two extra scouts) change how fast planets become known at all — which gates
     everything, because the AI cannot target an unexplored planet.
  e) Difficulty is not a trait but sits alongside them (EmpireDifficultyModifers.cs): goal count,
     check interval, starting-colony threshold, standby ships and whether colony ships jump the build
     queue all come from there. Say which of the five settings you see differ.
After the groups, tell me which single trait changes the AI's behaviour the most, and why.

SECTION 6 — where modules and tags bite
Keep this short; I do not want a module tour. Explain only the three places where ship data changes
this logic:
  - the Colony module type sets IsColonyShip (ShipDesign_Stats.cs 130) — no such design means the goal
    fails outright, so "can we expand" is partly a ship-design question;
  - ShipBuilder.PickColonyShip (187) chooses which colony ship to build, scoring designs and refusing
    the best one if it takes more than a few turns longer, so an expensive or slow colony ship slows
    expansion even though the planet score never sees it;
  - a module's DeployBuildingOnColonize places a building on landing, and the colony module's
    colonists/food/equipment payload seeds the new colony, which is why one colony ship can start a
    healthier colony than another.
Do not explain module stats, weapons or hulls.

SECTION 7 — the honest limits
Tell me what this logic does not do: no long-term planning beyond the goal count, no memory of
"that planet would have been good but was taken", no explicit valuation of a planet's strategic
position, and any place where the behaviour is a tuning number in content rather than a rule in code.
Point me at docs/ for anything already written down, and at the unit tests that pin the behaviour
(UnitTests/Planets/ColonyTargetSwitchTests.cs, UnitTests/Planets/StarRadiationTests.cs,
UnitTests/Planets/ColonyGraceTests.cs) so I know the behaviour is intentional.

INTERACTION RULES
- After each section, stop and ask "any questions before we continue?" and actually wait.
- When I ask a question, answer it from the code and cite the file and function. If the answer is
  spread over several places, say which one decides.
- If I ask "why did the AI do X in my game", explain the gate or score that would produce X, and tell
  me which of the numbers I could check in my save or in the game's logs (the expansion planner logs a
  "Running Expansion for ..." line, a "Colonize n/m | planet" line and a "Colonize switch" line).
- If I ask you to compare two races, do it quantitatively with the same example planets.
- Do not tell me to read the code myself as the answer. Give the explanation, then optionally the
  pointer.
- If I say "go deeper", show the real code for that one decision, up to ten lines, and translate it.
- Never speculate about modding consequences unless I ask; if I do, mark clearly what is data and what
  is hardcoded.
```

## What the reader should be able to answer afterwards

- Why the AI settled a mediocre planet and skipped the lush one next door. (Distance and known enemy
  strength divide the score outside its own systems; inside them, they do not.)
- Why expansion stalls for a while and then resumes. (Population-ratio gate, difficulty check
  interval, goal cap, or no legal target left.)
- Why a cybernetic race behaves nothing like an organic one. (Different value formula, two extra
  goals, a mineral-richness shortcut past the value floor, different colony start.)
- Why an aquatic race beelines ocean worlds and ignores deserts. (The per-environment multiplier
  feeds fertility, maximum population and therefore the score.)
- What has to be true before a planet is even a candidate. (Explored, habitable, clear of stellar
  radiation, out of grace, not someone else's system, and affordable to defend.)
- Why two colony ships of the same race can leave the AI expanding at different speeds. (Which design
  the AI picks to build, and what that design carries.)

## Questions worth asking it

- "Show me the exact numbers for my current race and tell me which worlds it would prefer."
- "What would change if this empire were Expansionists *and* cybernetic?"
- "Walk me through a game where the AI has four colony goals and only two are progressing."
- "Which line makes the AI give up on a target?"
- "Why does difficulty change where the AI expands, and not just how fast?"
- "What part of this is content I could tune in a mod, and what part is code?"
- "Which of these rules would a player notice first, and which are invisible?"

## Notes for the person running it

- Run it where the assistant can read the repository (an editor agent, or a clone with the files
  attached), or expect to paste files by hand. The prompt tells it to ask rather than improvise.
- The links above are pinned to `f575899`; if `main` has moved, ask the assistant to confirm by
  function name, not line number.
- Expect 20–40 minutes with questions. Sections 3 and 5 are where the arguing happens; that is the
  point.
- This document is the prompt. The explanation it produces is not checked in, on purpose: it would
  drift from the code the moment someone retunes a difficulty number.
