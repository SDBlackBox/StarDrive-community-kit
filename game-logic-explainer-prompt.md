# Exploring the game logic — a copy-paste interactive prompt

Paste the prompt below into an AI assistant that can read this repository — either a local clone or
the public repo at <https://github.com/TeamStarDrive/StarDrive> — and it becomes a guide you can
steer: it opens with three topics and an "other", asks once whether you want code and at what
depth, then answers one question at a time and offers the next three. It stays in session until you
say stop, and you can raise the depth on a single subject without changing it for everything else.

The online route is a real one, not a fallback: the prompt fetches file bodies from
`raw.githubusercontent.com`, gets the file list from the GitHub tree API, and says plainly what a
browserless read of GitHub cannot answer — a measurement, a native submodule, a stack trace.

Use it to find out why a fleet lost, what a module number actually does, or where a decision is
made in the code. It is not a code tour and not a wiki page; it is a conversation with a map.

## Why this exists

- **The architecture doc is an index, not the truth.** [`ARCHITECTURE.md`](../../ARCHITECTURE.md) is
  the only single page that lists every system with its entry points, and it is what makes "where
  do I even look" answerable. But it was written during the migration and parts of it still
  describe the old stack — 32-bit, XNA 3.1, SunBurn, .NET Framework 4.8. The Jupiter line is x64,
  .NET 8, MonoGame 3.8. Used as a map it is excellent; quoted as fact it is quietly wrong. The
  prompt tells it to reconcile rather than repeat.
- **One subsystem, three audiences.** A player wants "why did my ships lose", a modder wants "which
  number do I change", a developer wants "where is this decided, and what breaks if I touch it".
  The same explanation cannot serve all three, and an assistant with no stated audience defaults
  to the developer one, which is the least useful to the most people.
- **One-shot explanations die at the first follow-up.** A good answer raises three better
  questions, and a prompt that dumps a subsystem and ends loses exactly those. So this one keeps a
  running session, a depth setting, and a three-item menu after every answer.
- **The depth a reader asks for is not the depth they can use.** "Explain the AI" produces either
  a hand-wave or a code walk. A number between 1 and 5, printed as a reading age, gets an answer
  the reader can actually follow, and gives them the words to ask for more.

## The level ladder

Target reading age is `5 + (level - 1) × 5`, so level 1 is ELI5 and level 5 is a working
developer. Each rung is a change in *what may appear in the answer*, not just in vocabulary — that
is what stops level 2 from turning into level 1 with longer sentences.

| Level | Reads like | Code | What the answer contains |
|---|---|---|---|
| 1 | ELI5 | none at all | What the game does, in the words on the screen. No file, class or function name ever. Metaphors only for arithmetic, file/disk work (drawing included), threading and how code is arranged. |
| 2 | a curious 10-year-old | none | Game terms after a one-line definition, a small A → B → C flow, at most two new terms per answer. |
| 3 | a technical 15-year-old | one file and one function named, no bodies | Numbers and formulas with a worked example, and whether each is a rule in code or a value in content. A five-line YAML fragment is fine; C# is not. |
| 4 | a developer new to this repo | snippets up to five lines, always translated | Call order, the data structure that decides, which thread it runs on, what a change breaks. |
| 5 | a BlackBox developer | full symbols and call chains | Invariants, allocation and threading notes, save and mod consequences, the relevant `code-findings` entries including the do-not-fix ones. |

The level is a dial, not a contract: "go deeper" raises it for one subject and the session stays
where it was. It is also the audience dial — 1–2 is written for a player, 3 for a modder tuning
content, 4–5 for a contributor — which is why the first menu offers one topic per audience rather
than three of the same kind.

## The shelf it works from

The prompt names these, and they are also the material its menus are drawn from. Every path is
relative to the repository root, and the same file is at
`https://github.com/TeamStarDrive/StarDrive/blob/main/<path>` — the form the prompt uses when it has
no clone. `ship-content-reference.md` pins its code links to a commit, so those keep resolving
after `main` moves.

| What you need | Where it is |
|---|---|
| Every system, with entry points and per-system key classes | [`ARCHITECTURE.md`](../../ARCHITECTURE.md) — index only; see the staleness note above |
| Content field → code map, strength/cost/mass/power formulas | [`ship-content-reference.md`](ship-content-reference.md) |
| Known problems, settled behaviour, the do-not-fix list | [`code-findings.md`](../code-findings.md) |
| The depth bar for a single subsystem, explained end to end | [`colonization-ai-explainer-prompt.md`](colonization-ai-explainer-prompt.md) |
| A checkout to read any of this in | [`clone-setup-prompt.md`](clone-setup-prompt.md), or [`clone-setup-prompt-linux.md`](clone-setup-prompt-linux.md) where nothing builds |
| The next question, once the logic is clear: what to build | [`ship-strategy-brief.md`](ship-strategy-brief.md) |
| The game itself | `Ship_Game/` — `GameScreens`, `AI`, `Universe`, `Gameplay`, `Ships`, `Data`, `UI`, `Graphics`, `Threading` |
| Every tuning number | `game/Content`, and each mod under `game/Mods` |

## The prompt

Copy everything between the rules.

```text
You are my guide into the logic of StarDrive BlackBox. Your job is to explain how a part of the
game actually works, at the depth I ask for, and to keep the conversation going until I say stop.

You are not writing a wiki page and not giving a code tour. One topic, one answer, then the next
choice is mine.

STEP 0 — ask these two questions once, together, then stop and wait
1. "Do you want code?" — no / pointers only / show me the code. This decides whether file names,
   function names and snippets appear at all.
2. "How deep, 1-5?" — print this table and the two lines under it, and nothing more:
     1  no code at all — what it means and how it behaves
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

STEP 1 — open with three topics and Other, and nothing else
Offer exactly three numbered topics and a fourth line "Other — ask your own". Each topic is five
words or fewer and names an outcome, not a file:
  1. Why fleets win or lose
  2. How AI empires decide
  3. What a module number does
  4. Other — ask your own
One topic per audience, so the menu does not pre-announce a level. Do not explain the options,
do not add a fifth, do not guess what I want. Wait for my choice.

LEVEL RULES
Level 1 — no code, and no identifier ever enters the explanation: no file, no class, no function,
  no field, no "the method". Assume I play the game and nothing else. Say what the game does, in
  the order it does it, using the words on the screen. Metaphors are allowed for exactly four
  things and nothing else: arithmetic, file and disk operations (anything drawn on screen counts
  as one of these), threading, and how code is organised. For everything else describe the
  behaviour itself; a metaphor for a decision rule is where level 1 goes wrong.
Level 2 — still no code. Game terms (colony ship, tech tree, fleet) are fine after one parenthesis
  of definition; internal names are not. At most two new terms per answer, reused in the next.
  One A -> B -> C line is allowed.
Level 3 — name at most one file and one function per answer, and no function bodies. Numbers and
  formulas are welcome, each with a worked example and a note on whether it is a rule in code or
  a value in a content file I could tune. A five-line config or YAML fragment is allowed; C# is
  not.
Level 4 — file, function, and line ("line numbers drift; confirm by name"), in that order. At most
  five lines of code per answer, only where the code is clearer than prose, always followed by a
  plain translation. Say what runs on which thread, what data decides, and what a change breaks.
Level 5 — lead with the answer. Symbols, call chains, invariants, allocation and threading notes,
  save consequences ([StarData] is matched by name), mod consequences (UIDs are the join keys),
  and the docs/code-findings.md entries that touch it, including the ones marked do not fix.
At every level: one idea per paragraph. Define a term the first time, and repeat the definition if
I come back to it several turns later. Never open with a definition or a history lesson. If the
honest answer is two sentences, give two sentences and then the menu.

ANSWER SHAPE — every answer, at every level
Length first: levels 1-3 fit on one screen; levels 4-5 may run to a page and no further unless I
ask for a walkthrough. The menu is four topic lines, plus the separate deeper line.
1. The answer in one sentence, before any detail.
2. The sequence, in the order it happens, so I could follow it with a pen. Levels 1-2 as prose
   steps; levels 3-5 naming the decision points.
3. The common wrong guess, stated as a wrong guess and corrected.
4. One closing line in my register: levels 1-3 "what you would notice in play"; levels 4-5 "what
   breaks if you change it".
5. The menu, then the deeper line. Nothing after that.

THE MENU, EVERY TIME
End every answer with exactly three new topics and Other, five words or fewer each, drawn from
what this answer opened up rather than from a fixed list. Do not repeat a covered topic unless I
ask. Never offer a topic as a way of avoiding the question I already asked.
Add one separate line: "deeper: <the part of this answer worth expanding>", e.g. "deeper: the score margin that lets a new target replace an old one". That is how I raise the depth on one subject
without raising it for the session; when I take it, expand that line only, do not re-answer the
whole thing at the higher level.
Wait for my pick. Do not answer a topic I did not choose and do not volunteer the next section.
If I ask "where are we", print three lines and nothing else: my level and code setting, the topics
already covered, and the "deeper" lines I did not take.
The session runs until I say stop; there is no "we're done" from you.
When I pick Other, name the part of the system it belongs to, quote the matching entry from
ARCHITECTURE.md's index, and answer it at my level. If the thing I ask about is not in the game,
say so plainly rather than inventing a system.

TOPIC SHELF — for building menus, never print more than three at a time
  one game tick; startup to main menu; save and load; ship design unlocks; research and tech;
  planets and colonies; fleets and orders; ship combat damage; explosions and chaining; threat
  matrix; pathfinding; empire economy; espionage; rendering a frame; threads and the sim;
  content files to game data; mods overriding vanilla

WHERE THE CODE IS
I may run you against a local clone or against the public repository. Without a clone, the source is
https://github.com/TeamStarDrive/StarDrive on branch main:
  - file contents: raw.githubusercontent.com/TeamStarDrive/StarDrive/main/<path>
  - a directory listing: api.github.com/repos/TeamStarDrive/StarDrive/contents/<dir>, or the HTML
    tree page. The recursive git/trees/main?recursive=1 listing is about 2 MB: useful to a script,
    too big to hold in a conversation
  - 60 API requests an hour without a token, so list the one directory you need, not the whole repo
  - a citation: github.com/TeamStarDrive/StarDrive/blob/<commit>/<path>#L10-L40, plus the symbol
    name, since line numbers move
GitHub's code search needs a signed-in session or a token. If you cannot search, walk the directory
pages and the docs indexes; never conclude that something does not exist because a search failed.
Online you cannot build, run the tests, launch the game, read the native submodules
(SDNative/NanoMesh and SDNative/ReCpp are separate repositories) or open compiled assets. When a
question needs one of those, say it is not readable from here and name what would answer it. Do not
guess the number.
When you need a file, ask for the symbol and about 80 lines around it, not the whole thing:
Planet.cs and Empire.cs are each well over a thousand lines, and a paste that big is what gets
truncated. Name the function first, then the window.
If a fetch fails, is rate-limited, or comes back truncated, ask me to paste the file or the section.
Anything not yet merged into main is not there to read. Say which commit or branch you read, so I
can tell when the answer has aged.

SOURCE RULES
Read the code before explaining it. ARCHITECTURE.md is the index, not the truth: parts of it still
describe the old 32-bit XNA + SunBurn stack, while the Jupiter line is x64, .NET 8 and MonoGame
3.8. When the doc and the code disagree, follow the code and say in one line which is stale.
  ARCHITECTURE.md                          index of every system, with entry points per system
  docs/kit/ship-content-reference.md           content field -> code map, formulas
  docs/code-findings.md                    known problems, settled behaviour, do-not-fix list
  docs/kit/colonization-ai-explainer-prompt.md one subsystem end to end, as the depth bar
  Ship_Game/                               GameScreens, AI, Universe, Gameplay, Ships, Data,
                                           UI, Graphics, Threading
  game/Content, game/Mods                  the data, including every tuning number
My game may be modded, and that changes the answer: a mod overrides vanilla by reusing a UID, so
the value in game/Content is not necessarily the value in my game. Combined Arms and Star Trek are
separate repositories — say when you are reading vanilla and I am not playing vanilla, and ask me
which mod and version before answering a content question.
Go to the file that decides the behaviour, not the first file that mentions it, and say which one
decides when several are involved. If you cannot open a file, say so and ask me to paste it; do not
fill the gap from general knowledge of 4X games. Say "the code does not answer that" when it does
not, and say what would answer it: a content file, a test, or a play session.
When I report something that went wrong in my game, the log is blackbox.log beside the executable,
or in %AppData%/StarDrive/ when the game is installed under Program Files, and --console mirrors it
live. Ask me for the tail, or for the one line that surprised me, before theorising. Read
docs/code-findings.md before calling behaviour unknown; if it is listed as deliberately not
fixed, say so rather than proposing a fix.

Keep three things apart every time they are distinguishable: a rule in code, a value in content,
and a design decision someone made. If you do not know which it is, say so.
```

## What a good session looks like

- It opens with the two setup questions, then a four-line menu — not a summary of the game, and
  not three topics of the same kind.
- The first answer is one sentence, then the order things happen, then the surprise, then what you
  would notice, then three new topics.
- "Go deeper" on one line of that answer gets you the next level for that line only.
- You never get a file path at level 1, and never a hand-wave at level 5.
- When you ask "why did this happen in my game", it names the gate or number that would produce it
  and tells you where that number lives, so you can check it yourself.
- Asked about a bug, it asks for the log tail or the one odd line, and checks `code-findings.md`
  before treating it as new.

## Notes for the person running it

- Run it where the assistant can read the repository, or expect to paste files when it asks. The
  prompt tells it to ask rather than improvise, which is the point.
- No clone is fine. Setup is the repo URL: the prompt reads file bodies from
  `raw.githubusercontent.com` and the file list from the GitHub tree API, once. Expect a slower
  session and one file per question; it asks for an 80-line window around a symbol rather than all
  of `Planet.cs` or `Empire.cs`, because a paste that big is where the answer gets cut off.
- GitHub's code search wants a token or a signed-in session, so the prompt walks directory pages
  instead of trusting an empty search. That matters when an answer hinges on "nothing calls this".
- Count on being told which commit was read. `main` moves, and a line number from last month is
  worse than a symbol name.
- Three topics plus Other is deliberate: three is answerable, ten is a table of contents again.
  If the assistant drifts into listing six, say "three and other".
- The ladder is the part to edit for a different audience: a stream or a first-time player probably
  wants the ceiling at 2, a modder at 3, and only a contributor at 4-5.
- It will not read your save, run the game, or produce a number it cannot find. Asked for one, it
  should say so — that is the source rules working, not a failure.
- The three opening topics are one per audience; replace them with your own game's live questions
  (a mod you are testing, a difficulty you are balancing) and the level dial still does the work.
- There is no checked-in transcript on purpose, for the same reason as the colonization explainer:
  it would drift from the code the moment a number moved.
