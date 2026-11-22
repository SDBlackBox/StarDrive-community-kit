#!/usr/bin/env python3
"""Generate the kit's GitHub Pages site: the landing page and one page per prompt.

    python3 docs/kit/build-site.py

Reads the table below and the prompt files beside it, and writes docs/kit/index.html plus
docs/kit/prompts/<slug>.html. Each prompt page embeds its file verbatim, so Copy works offline and
with no fetch: re-run this after editing a prompt, and the page follows the file.

Edit the table here, not the generated HTML.
"""

import html
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE
OUT = HERE / "prompts"

BLOB = "https://github.com/SDBlackBox/StarDrive-community-kit/blob/main/"
REPO = "https://github.com/TeamStarDrive/StarDrive"
KITREPO = "https://github.com/SDBlackBox/StarDrive-community-kit"
VETTED = "f575899fe"
CHECKED = "2026-11-17"

escape = html.escape

# group: explainer | tool | reference
PROMPTS = [
    dict(
        slug="game-logic", file="game-logic-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="The game, end to end",
        blurb="Why a fleet lost, where a decision is made, what a number does.",
        title="The game, end to end",
        lede=("The general guide, and the one to start with. It opens with three topics and an "
              "&ldquo;other&rdquo;, asks once whether you want code and at what depth, then answers one question "
              "at a time and offers the next three."),
        how=[
            "One question at a time: after each answer you get three new topics and an &ldquo;other&rdquo;.",
            "Depth is asked once. You can raise it on a single subject without changing it for the rest of the session.",
            "It works on a local clone or the public repo: file bodies come from <code>raw.githubusercontent.com</code>, "
            "the file list from the GitHub tree API.",
            "It says plainly what a browserless read cannot answer &mdash; a measurement, a native submodule, a stack trace.",
        ],
        needs="A checkout, or just the public repository. Nothing to install.",
    ),
    dict(
        slug="empire", file="empire-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="What an empire is made of",
        blurb="The race file, the traits, the starting kit, what it can see.",
        title="What an empire is made of",
        lede=("The document the other explainers point at: the race file behind a people, what each trait "
              "actually changes, what it starts the game with, and where the numbers that make one empire "
              "different from another are written."),
        how=[
            "Separates the saved race (<code>EmpireData</code>, matched by field name) from the live "
            "<code>Empire</code> that owns colonies, research, fleets and diplomacy, and asks which half a question is about.",
            "Treats a trait as a number with a reader, not a label: roughly eighty fields on <code>RacialTrait</code>, "
            "most of them read directly by the game.",
            "Answers what a people starts with and what it is allowed to see, which is what the tech and era documents assume.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="tech-logic", file="tech-logic-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="The tech tree",
        blurb="Gated, priced, paid out &mdash; and who picks the order.",
        title="The tech tree",
        lede=("Research narrowed to one system: what a tech is, whether your empire can even see it, what gates "
              "it, what it costs, where the points come from, what unlocking it pays out, and who chooses the order."),
        how=[
            "Every answer names its link on a chain of seven: <em>exists, shows, gates, costs, accrues, pays out, chooses</em>.",
            "The concept list is rebuilt from the code each session, not shipped with the prompt; stale entries are deleted, not explained.",
            "Before the first menu it names the commit it is reading, compares the kit's vetted commit, and offers "
            "pull / refresh / continue without pulling on its own.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="module-logic", file="module-logic-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="Ship modules",
        blurb="Why a module shows, fits, costs what it costs, and breaks.",
        title="Ship modules",
        lede=("What a module is, why it is or is not in your palette, why it will not fit a cell, what it costs in "
              "credits, mass, power and health, what it actually does, and what happens when it is hit."),
        how=[
            "A chain of seven again: <em>exists, shows, fits, costs, draws, pays out, breaks</em>.",
            "Concept list discovered from the remote commit, the content files and the tests.",
            "Checks it is reading current code, and offers pull / refresh / continue before the first menu.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="weapon-logic", file="weapon-logic-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="A gun",
        blurb="Tags, the three damage numbers, and what a shot costs.",
        title="A gun",
        lede=("The second half of the module explainer: which template decides a weapon, what its tags do, how many "
              "damage numbers it has and which one the screen is showing, what one shot costs in power and ordnance, "
              "and what the damage meets on the way in."),
        how=[
            "It starts where the module explainer stops &mdash; at &ldquo;pays out&rdquo;, because a module only names a weapon UID.",
            "Treats the tag vocabulary as four unrelated jobs: family decides bonuses and resistance, delivery decides "
            "flight and interception, role decides point defence, and behaviour flags decide the rest.",
            "Keeps the three damage numbers apart, and prices a shot in power per second, which is the number a beam fleet is really spending.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="ship-design", file="ship-design-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="Ship designs",
        blurb="The .design file, its layout, role, warnings and build gate.",
        title="Ship designs",
        lede=("The <code>.design</code> file, the hull under it, the numbers the shipyard derives, why its role and "
              "category change, why the shipyard warns, and why a finished design is or is not buildable."),
        how=[
            "Chain of seven: <em>hull, layout, numbers, role, warnings, unlock, build</em>.",
            "The role is derived from modules as a share of the hull's slot count, not read from a field &mdash; the "
            "prompt follows that derivation rather than the label.",
            "Concept list discovered each session; freshness check before the first menu.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="ship-chooser", file="ship-chooser-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="Which ships get built",
        blurb="Pool, want, budget, rank, pick, place, renew.",
        title="Which ships get built",
        lede=("How an empire decides what to build: which designs it may build, how many of each role it wants, what "
              "upkeep it will carry, which role is next, which design inside that role, which planet lays the hull "
              "down, and when it refits or scraps instead."),
        how=[
            "Chain of seven: <em>pool, want, budget, rank, pick, place, renew</em>.",
            "Answers the question a design screen cannot: why a legal, cheap ship is never laid down.",
            "Concept list from the code each session; freshness check before the first menu.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="ship-combat", file="ship-combat-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="Space combat",
        blurb="Knowing, wanting, choosing, closing, firing, hurting, dying.",
        title="Space combat",
        lede=("How a ship finds an enemy, decides which one, closes, fires, and what a hit does to the hull &mdash; "
              "which is the answer to &ldquo;why did my fleet lose&rdquo;."),
        how=[
            "Chain of seven: <em>knowing, wanting, choosing, closing, firing, hurting, dying</em>.",
            "Concept list discovered, not shipped; stale entries deleted rather than explained.",
            "Names the commit it reads and offers pull / refresh before answering.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="fleet-creation", file="fleet-creation-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="How a fleet forms",
        blurb="Goal, task, requirement, pool, extract, form, sustain.",
        title="How the empire forms a fleet",
        lede=("Which goal asks for a fleet, how that goal becomes a military task and what strength it demands, how a "
              "set is extracted from the pool of available ships, what turns the set into a named fleet, and what "
              "happens to it when the task ends."),
        how=[
            "Chain of seven: <em>goal, task, requirement, pool, extract, form, sustain</em>.",
            "Separates the task's demand from the ships that answer it, which is where most &ldquo;it sent the wrong "
            "ships&rdquo; questions actually live.",
            "Concept list from the code each session; freshness check before the first menu.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="planet-capture", file="planet-capture-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="Taking a planet",
        blurb="Who decides, who carries the troops, what the ground fight rolls.",
        title="Taking a planet",
        lede=("How a planet changes hands: who decides to take it, where the troops come from, which hulls carry them, "
              "how they land, what the ground fight rolls, and what the planet looks like the moment it flips."),
        how=[
            "Chain of seven: <em>want, build, load, fly, land, fight, capture</em>.",
            "Asks two setup questions before it starts, then one question at a time.",
            "Concept list rebuilt from the code; freshness check before the first menu.",
        ],
        needs="A checkout, or the public repository.",
    ),
    dict(
        slug="colonization-ai", file="colonization-ai-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="AI colonization",
        blurb="Why the AI settles the planet it settles, in plain language.",
        title="How the AI decides where to colonize",
        lede=("Why the AI settles the planet it settles, where each decision is made in the code, and how a race's "
              "traits change the answer. Written for people who do not know this codebase and may not write code at all."),
        how=[
            "The pipeline is short and deterministic &mdash; a handful of gates, one score per planet, one target per "
            "run &mdash; but spread over five code files and two content files; this is the map for it.",
            "Plain language with the symbol named beside it, so the claim can be checked without reading C#.",
            "Meant to be interrupted: it is a walk-through, not a page you read in one go.",
        ],
        needs="A checkout, or the public repository. No C# required.",
    ),
    dict(
        slug="time-and-space", file="time-and-space-explainer-prompt.md", group="explainer",
        kind="Explainer",
        short="How far, how long",
        blurb="Distances and speeds turned into minutes, turns and roles.",
        title="How far, how long, and what it buys",
        lede=("The distances and speeds the game actually generates &mdash; system sizes, the gaps between systems, "
              "map extents, sublight against warp &mdash; turned into minutes, turns and roles. It answers what the "
              "design screen cannot: can this hull reach the fight in time to matter?"),
        how=[
            "Puts the two scales side by side: a system reaches 150,000 units, systems sit 350,000 apart, a Medium map "
            "is 6,000,000 across; sublight tops out at 1,500, warp bottoms out at 3,000.",
            "Treats speed as conditional rather than a property: halved inside enemy projection, unusable inside an "
            "inhibitor with a 5&nbsp;s hangover, and capped per jump by the power the hull can hold.",
            "Ends in the division &mdash; distance over speed at a stated game speed &mdash; not in an adjective.",
        ],
        needs="A checkout, or the public repository. No C# required.",
    ),
    dict(
        slug="era-explorer", file="era-explorer-prompt.md", group="tool",
        kind="Tool",
        short="The era explorer",
        blurb="Cuts the tech tree into research-cost bands for one mod and one race.",
        title="The era explorer",
        lede=("A guide to <em>when</em> things happen, where &ldquo;when&rdquo; is research cost rather than turns. It "
              "cuts the tree into brackets for one content root and one race, says what each bracket changes, and hands "
              "the rest of the question to the document that owns it."),
        how=[
            "Refuses to guess the two things that rewrite the tree first: the mod (files unify by name, the mod wins) and "
            "the race (<code>Secret</code>, <code>UnlockedAtGameStart</code>, <code>HiddenFrom</code>).",
            "A band is a span of research points, not a span of game time; it says so wherever a number could be mistaken for turns.",
            "The engine is <code>docs/era-explorer/era-scan.py</code> in the game repository, so the cut is recomputed for "
            "your content rather than remembered.",
        ],
        needs="A checkout and Python 3. The scan reads <code>game/Content</code> and never writes to it.",
    ),
    dict(
        slug="ai-test", file="ai-test-explainer-prompt.md", group="tool",
        kind="Tool",
        short="Testing AI behaviour",
        blurb="A belief about the AI turned into one runnable scenario.",
        title="Testing AI behaviour on a ship",
        lede=("Turns a belief about the AI &mdash; &ldquo;it should build this&rdquo;, &ldquo;it should use it like a "
              "carrier&rdquo; &mdash; into one scenario that can be run and a result that can be read."),
        how=[
            "Settles the rung first: <code>--fix-roles</code>, the build gate, the research picker, the fleet planner, "
            "the hangar and combat code are ordered by cost, and most &ldquo;tests&rdquo; stop at the cheapest one.",
            "Settles the two arms of the experiment before anything runs, so a result can distinguish the change from the baseline.",
            "Settles the output shape too: CSV, markdown, JSON or an HTML chart.",
        ],
        needs="A checkout. Running the harness needs Windows and a graphics device.",
    ),
    dict(
        slug="concept-map", file="concept-map-prompt.md", group="tool",
        kind="Tool",
        short="The concept map",
        blurb="Writes docs/concept-map.md &mdash; and re-checks every address later.",
        title="Building and refreshing the concept map",
        lede=("Produces <code>docs/concept-map.md</code>: roughly forty-six entries, each saying what a player-visible "
              "part of the game means, where the decision is made, and where the numbers live. The same prompt doubles as "
              "the refresh procedure."),
        how=[
            "An address book, not an explanation: formulas stay in the content reference, walkthroughs in the explainer prompts, "
            "known problems in <code>code-findings.md</code>.",
            "Run it again later and it verifies every address and reports what moved, instead of rewriting what is still true.",
            "It writes a file, so it belongs in a checkout rather than a browser tab.",
        ],
        needs="A checkout &mdash; it writes <code>docs/concept-map.md</code>.",
    ),
    dict(
        slug="ship-strategy-brief", file="ship-strategy-brief.md", group="tool",
        kind="Tool",
        short="The strategy brief",
        blurb="Makes the AI ask what the fleet is for before it designs.",
        title="The strategy brief",
        lede=("A prompt that makes an AI ship-builder ask what your fleet is <em>for</em> before it designs anything, "
              "then hold that answer for the whole tech progression."),
        how=[
            "The question comes first, in writing, and no hull is proposed until it has been answered.",
            "The written answer is the brief &mdash; the thing you re-read when a design looks wrong.",
            "Mechanics stay in the content reference; this is the conversation that decides which mechanics to spend.",
        ],
        needs="A checkout. The build and combat checks it names need Windows.",
    ),
    dict(
        slug="clone-setup", file="clone-setup-prompt.md", group="tool",
        kind="Tool",
        short="Local clone (Windows)",
        blurb="A checkout that builds, with both submodules.",
        title="Local clone setup &mdash; Windows",
        lede=("A single prompt that gets a working StarDrive BlackBox checkout on a new machine: it asks where the repo "
              "should go, checks the basics, shows the layout, and only then clones &mdash; with both submodules."),
        how=[
            "The submodules are the quiet failure: a plain clone leaves <code>SDNative/NanoMesh</code> and "
            "<code>SDNative/ReCpp</code> empty and the native build fails on include files.",
            "<code>NanoMesh</code> comes from a fork on purpose, so <code>--recurse-submodules</code> is the whole difference.",
            "Shows the directory layout before writing anything, so the destination is agreed before the clone.",
        ],
        needs="Git and a shell. Building the game itself needs Windows with the C++ workload.",
    ),
    dict(
        slug="clone-setup-linux", file="clone-setup-prompt-linux.md", group="tool",
        kind="Tool",
        short="Local clone (Linux/macOS)",
        blurb="A checkout for reading and editing &mdash; not for building.",
        title="Local clone setup &mdash; Linux and macOS",
        lede=("The same guided clone, adjusted for Linux and macOS, and clear about the limit: a Linux checkout is for "
              "reading, editing and git work, not for building the game."),
        how=[
            "Explains why the build stops: every project targets <code>net8.0-windows</code> with "
            "<code>UseWindowsForms</code>, and the solution carries MSVC-only projects.",
            "The test harness additionally needs a real graphics device &mdash; that is a port, not a flag.",
            "Checks the filesystem and disk space before cloning, with both submodules as the Windows prompt does.",
        ],
        needs="Git and a shell on Linux or macOS. Read and edit only.",
    ),
    dict(
        slug="moddable-content", file="moddable-content-explainer-prompt.md", group="reference",
        kind="Reference",
        short="Moddable content",
        blurb="Every file family and every tag a mod can replace, in seven sections and three depths.",
        title="Moddable content &mdash; files, tags and values",
        lede=("What a mod can replace under <code>game/Content</code>: each file family, what its tags do, "
              "how override and inheritance resolve, and which files are static furniture the game expects. "
              "Seven section pages, each entry opening from one sentence to a numeric detail with the values "
              "vanilla actually uses."),
        how=[
            "Sections follow the way a modder works: game options, map creation, ships, tech, races and diplomacy, colonies, UI and assets.",
            "Level 1 is a sentence, level 2 several on behaviour, level 3 the field, unit, formula, vanilla example and failure symptom.",
            "Counts, coverage and every In-vanilla value summary are generated from the checkout, so a missing entry or a stale number is visible.",
            "Token-heavy by design: a deep answer reads hundreds of content files plus the C# that loads them. The prompt states the cost first and offers one section or one family at a time.",
            "Asking for the local pages produces a rerunnable generator &mdash; <code>build-moddable.py</code> and its data modules &mdash; not a hand-written HTML file.",
        ],
        needs=("A checkout for the prompt. The rendered reference starts at "
               "<a href=\"../moddable-content.html\">moddable-content.html</a>; rebuild hub and sections with "
               "<code>python3 docs/kit/build-moddable.py --audit</code>. The existing pages are the cheap "
               "path: they already hold the generated values for every family."),
    ),
    dict(
        slug="ship-content-reference", file="ship-content-reference.md", group="reference",
        kind="Reference",
        short="Ship content reference",
        blurb="Every content field, the code that reads it, and the formulas.",
        title="Ship content reference &mdash; data files to code",
        lede=("How the ship content under <code>game/Content</code> is read, what every field does, and the formulas "
              "derived from them: strength, cost, mass, speed, power, role, research cost."),
        how=[
            "Read once, then used as a lookup &mdash; it exists to be quoted from.",
            "Pinned to commit <code>" + VETTED + "</code>; every link is a permalink, so a change to a cited method means "
            "updating the link and the formula in the same PR.",
            "Deliberately out of scope: mesh and texture pipelines, the AI that picks designs, combat resolution.",
        ],
        needs="Nothing &mdash; this one is read, not pasted. It is the mechanics the other prompts defer to.",
    ),
]

CSS = """
:root{--bg:#14171c;--panel:#1b1f26;--ink:#e6e8ea;--dim:#8b949e;--line:#2b313a;--gold:#ffd479;--link:#8ecbff;--ok:#8ad06a}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 Georgia,serif}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
code{font:12.5px ui-monospace,monospace;color:#c9d1d9;background:#20252d;padding:0 3px;border-radius:3px}
.bar{position:sticky;top:0;z-index:9;background:rgba(20,23,28,.94);border-bottom:1px solid var(--line)}
.bar .in{max-width:1240px;margin:0 auto;padding:10px 28px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.btn{display:inline-block;font:12px ui-monospace,monospace;padding:5px 12px;border:1px solid #3a424e;border-radius:999px;background:var(--panel);color:var(--ink);cursor:pointer}
.btn:hover{border-color:var(--link);text-decoration:none}
.btn.primary{border-color:#6b5a2b;background:#2a261b;color:var(--gold)}
.head{max-width:1240px;margin:0 auto;padding:34px 28px 6px}
h1{font-size:27px;margin:0 0 8px;line-height:1.25}
p.lede{color:var(--dim);max-width:82ch;margin:0 0 12px}
p{margin:0 0 10px}
.shell{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:40px;max-width:1240px;margin:0 auto;padding:8px 28px 70px;align-items:start}
@media(max-width:920px){.shell{grid-template-columns:1fr;gap:26px}}
h2{font-size:12.5px;margin:30px 0 10px;color:#c9d1d9;text-transform:uppercase;letter-spacing:1.2px;font-family:ui-monospace,monospace}
h2 .count{color:var(--dim);letter-spacing:0}
ul{margin:0 0 10px;padding-left:20px}li{margin:0 0 7px}
table{border-collapse:collapse;width:100%;font:12.5px ui-monospace,monospace;margin:4px 0 10px}
th,td{text-align:left;padding:6px 9px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--dim);font-weight:normal}
td.n{white-space:nowrap;color:var(--gold)}
.note{color:var(--dim);font-size:13px}
.facts{display:flex;gap:20px;flex-wrap:wrap;font:12px ui-monospace,monospace;color:#c9d1d9;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:9px 13px;margin:14px 0 0}
.facts b{color:var(--gold);font-weight:normal}
aside{position:sticky;top:56px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:4px 16px 14px;max-height:calc(100vh - 80px);overflow:auto}
@media(max-width:920px){aside{position:static;max-height:none}}
aside h2{margin:14px 0 6px}
aside p.ai{color:var(--dim);font-size:12.5px;margin:12px 0 2px}
.nav a{display:block;padding:6px 0;border-bottom:1px solid #232a33}
.nav a:last-child{border-bottom:0}
.nav b{font-weight:normal;color:var(--ink);display:block}
.nav span{display:block;color:var(--dim);font-size:12.5px;line-height:1.4}
.kicker{font:12px ui-monospace,monospace;color:var(--dim);margin:0 0 10px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.chip{font:10.5px ui-monospace,monospace;letter-spacing:.6px;text-transform:uppercase;border:1px solid #4a5260;border-radius:9px;padding:1px 7px;color:var(--dim)}
.acts{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 4px}
.msg{font:12px ui-monospace,monospace;color:var(--dim);min-height:1.4em;margin:6px 0 0}
.msg.ok{color:var(--ok)}.msg.err{color:#e07070}
pre#text{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:14px;max-height:62vh;overflow:auto;white-space:pre-wrap;font:12px ui-monospace,monospace;color:#c9d1d9}
.meta{font:12px ui-monospace,monospace;color:var(--dim);border-top:1px solid var(--line);margin-top:30px;padding-top:10px}
"""

JS = r"""
const btn = document.getElementById('copy');
const show = document.getElementById('show');
const pre = document.getElementById('text');
const msg = document.getElementById('msg');

function say(t, cls) { msg.className = 'msg' + (cls ? ' ' + cls : ''); msg.innerHTML = t; }

function legacyCopy(t) {
  const ta = document.createElement('textarea');
  ta.value = t;
  ta.setAttribute('readonly', '');
  ta.style.position = 'fixed';
  ta.style.top = '-1000px';
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  ta.remove();
  return ok;
}

btn.addEventListener('click', async () => {
  const text = pre.textContent;
  if (!text.trim()) {
    say('This page has no prompt text on it.', 'err');
    return;
  }
  let ok = false;
  if (navigator.clipboard && window.isSecureContext) {
    try { await navigator.clipboard.writeText(text); ok = true; } catch (e) { ok = false; }
  }
  if (!ok) ok = legacyCopy(text);
  if (!ok) {
    say('The clipboard is blocked here. Press <b>Show prompt</b> and select the text.', 'err');
    return;
  }
  say('Copied ' + text.length.toLocaleString() + ' characters. Paste the whole file, then ask your question.', 'ok');
  const label = btn.textContent;
  btn.textContent = 'Copied \u2713';
  setTimeout(() => { btn.textContent = label; }, 2000);
});

show.addEventListener('click', () => {
  pre.hidden = !pre.hidden;
  show.textContent = pre.hidden ? 'Show prompt' : 'Hide prompt';
  say('');
});
"""


def page(title, bar, body, script=""):
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{escape(title)}</title><style>{CSS}</style></head><body>'
        f'<nav class="bar"><div class="in">{bar}</div></nav>'
        f'{body}'
        + (f'<script>{script}</script>' if script else '')
        + '</body></html>\n'
    )


def sidebar(prefix):
    out = ['<p class="ai">Paste a prompt into a chat with a checkout in front of it. Each page has a '
           'copy button.</p>']
    for group, label in (("explainer", "Explainers"), ("tool", "Tools"), ("reference", "Reference")):
        items = [p for p in PROMPTS if p["group"] == group]
        out.append(f'<h2>{label} <span class="count">{len(items)}</span></h2>')
        out.append('<div class="nav">')
        for p in items:
            out.append(
                f'<a href="{prefix}{p["slug"]}.html"><b>{p["short"]}</b>'
                f'<span>{p["blurb"]}</span></a>'
            )
        out.append('</div>')
    return "\n".join(out)


def moddable_section():
    """The content guide's block on the landing page.

    The counts are read back out of the generated hub instead of being written here, so the landing
    page cannot quote a coverage figure the guide no longer has. With no hub beside this script the
    block degrades to the paragraph and the link.
    """
    try:
        hub = (HERE / "moddable-content.html").read_text(encoding="utf-8")
    except OSError:
        hub = ""

    facts = {}
    for key in ("families", "content files", "tags described", "sections", "generated from"):
        m = re.search(re.escape(key) + r": <b>(.*?)</b>", hub)
        if m:
            facts[key] = m.group(1)
    rows = re.findall(
        r'<a class="card" href="moddable/([\w-]+)\.html"><span class="ct">(.*?)</span>'
        r'<span class="cb">(.*?)</span><span class="cf">(.*?)</span></a>', hub)

    factline = ""
    if facts:
        factline = ('<div class="facts">'
                    + "".join(f"<span>{k}: <b>{v}</b></span>" for k, v in facts.items())
                    + "</div>")
    table = ""
    if rows:
        table = ("<table>\n<tr><th>section</th><th>what it covers</th><th>size</th></tr>\n"
                 + "".join(f'<tr><td><a href="moddable/{cid}.html">{title}</a></td>'
                           f'<td>{blurb}</td><td>{meta}</td></tr>'
                           for cid, title, blurb, meta in rows)
                 + "\n</table>")

    total = facts.get("content files", "the whole content tree")
    return f"""
<h2>What a mod can replace</h2>
<p>Every file family and every structured tag under <code>game/Content</code>, split into seven
sections the way a modder works. A card opens from one sentence to how the value behaves, then to the
tag, the unit, the formula and the values vanilla actually uses. The generator indexes
<code>Ship_Game</code> for the field behind every key and counts the places that read it, so a key
that nothing consumes says so on the card instead of being given an invented function.</p>
{factline}
{table}
<p class="note">The expensive prompt: a deep answer reads hundreds of content files plus the C# that
loads them, and a full pass reads all {total}. It says so before it starts and offers one section or
one family; these pages already hold the generated values, which is the cheap way to look one up.</p>
<p><a class="btn primary" href="moddable-content.html">Open the content guide</a>
<a class="btn" href="prompts/moddable-content.html">The prompt</a></p>
"""


INDEX_BAR = (
    '<a class="btn primary" href="weapon-tech-human.html">Era map &mdash; Human</a>\n'
    '<a class="btn primary" href="#prompts">The 20 prompts</a>\n'
    '<a class="btn primary" href="moddable-content.html">Moddable content</a>\n'
    f'<a class="btn" href="{REPO}">Game repository &nearr;</a>\n'
)


def index_body():
    return f"""
<header class="head">
 <h1>StarDrive BlackBox</h1>
 <p class="lede">The ship programme, the numbers behind it, and a kit of prompts that reads the code
 with you. Human first, vanilla content, one race per pass &mdash; and every figure here is research
 cost, not turns.</p>
 <div class="facts"><span>race: <b>Human / Terran</b></span><span>bands: <b>5</b></span>
 <span>weapon chains: <b>10</b></span><span>content: <b>vanilla</b></span>
 <span>pinned: <b>{VETTED}</b></span><span>checked: <b>{CHECKED}</b></span></div>
</header>
<div class="shell">
<main>

<h2>The five bands &mdash; where the tech actually lands</h2>
<table>
<tr><th>band</th><th>research cost</th><th>weapons</th><th>what lands</th></tr>
<tr><td>B1</td><td class="n">0 &ndash; 1,830</td><td>48</td>
 <td>the free opening (14 techs, seven weapons); the first real choice at 200&ndash;530; the main-gun
 line's first rung at 1,830</td></tr>
<tr><td>B2</td><td class="n">2,470 &ndash; 4,400</td><td>12</td>
 <td>four of the twelve are point defence (2,470, 2,620); <code>Aegis</code> 1,227 dps at 3,600, the
 strongest weapon in the band</td></tr>
<tr><td>B3</td><td class="n">5,140</td><td>2</td>
 <td>one line: <code>Polaron Cannons</code>, 222 / 533 dps</td></tr>
<tr><td>B4</td><td class="n">6,390</td><td>1</td>
 <td><code>BigCannon</code> 1,010 dps at 12,500</td></tr>
<tr><td>B5</td><td class="n">8,700 &ndash; 10,140</td><td>5</td>
 <td>capstones &mdash; <code>LRM3</code> 8,700, <code>MassivePhasorTurret</code> 9,160,
 <code>Disintegrator</code> 1,680 dps at 9,260, <code>BasicTorpedo</code> 9,640,
 <code>MassivePolaronCannon</code> 10,140</td></tr>
</table>
<p class="note"><b>A band is research points, not turns.</b> &ldquo;0&ndash;1,830&rdquo; is everything
reachable for 1,830 points after the free opening. What that costs in turns depends on the empire's
net research per turn &mdash; colonies, research stations, alliances &mdash; which is an income
question, not a tree question.</p>

<h2>What the map already says</h2>
<ul>
<li><b>Beam is the largest type (20 of 95) and the strongest at the top.</b> <code>Disintegrator</code>
is 1,680 dps at 9,260 with 11,000 range. Beam pays in power rather than points: it draws 2,556/s the
whole time it fires, so a beam fleet is a reactor budget.</li>
<li><b>Above 5,000 an era is one research line wide.</b> Band 3 is <code>Polaron Cannons</code> alone
and band 4 is <code>BigCannon</code> alone; eight of the ten weapon chains advance in neither.</li>
<li><b>Point defence finishes at 2,620 and is defence, not a damage lane.</b> All six Human PD weapons
are <code>TruePD</code>: they engage missiles and torpedoes and cannot fire at a ship at all.</li>
<li><b>Hull gates are cheaper than the plan first assumed.</b> A 3&times;8 waits for the 1,600 station
or the 1,680 <code>LightCarrier</code>, and a 4&times;4 turret fits the 480 <code>Gunboat</code>.
Late-game themes are limited by cells and power, not by having bought the big hull.</li>
<li><b>A gap band is where defence and support tech go.</b> Shields, armour, point defence, repair,
inhibitor, carrier, power, engines &mdash; four kinds of line on four budgets, not one.</li>
</ul>

<h2>The two results</h2>
<a class="card" href="weapon-tech-human.html"><b>The era map &mdash; weapon tech on a research-cost axis</b>
<span>One lane per weapon-tag family, the five bands, the module view and the ships by role. Vanilla
content, Human, generated by <code>docs/era-explorer/era-scan.py</code> in the game repository.</span></a>
<div class="card"><b>Milestones M0&ndash;M10 &mdash; live status</b>
<span>The tracker cites files in the game repository, so it lives there beside the era scanner:
<code>docs/milestones.html</code> in <a href="{REPO}">TeamStarDrive/StarDrive</a>, read from a
checkout rather than from this site. It carries what each milestone's &ldquo;done when&rdquo; is, the
ten chains with the hull that mounts each peak, and the M2 era grid.</span></div>

<h2>Where the numbers come from</h2>
<table>
<tr><th>what</th><th>command or file</th></tr>
<tr><td>the era map, weapon costs, module and design bills</td>
 <td><code>python3 docs/era-explorer/era-scan.py --race Human [--html out.html]</code></td></tr>
<tr><td>hull gates, the M2 grid</td><td><code>python3 docs/era-explorer/hull-gates.py</code></td></tr>
<tr><td>acquisition-only lines</td><td><code>python3 docs/era-explorer/acquisition.py</code></td></tr>
<tr><td>milestone status</td><td><code>docs/milestones.html</code> in the game repository</td></tr>
</table>
<p class="note">The mod and the race are arguments, not assumptions: a mod unifies content by file name
and wins, and a race's secret, free and hidden techs change the ladder before any cost is quoted.
Nothing on these pages is fetched at runtime, so a page that is out of date is out of date in the
file.</p>

{moddable_section()}

<h2>The kit &mdash; {len(PROMPTS)} prompts</h2>
<p>Each entry in the sidebar is a prompt you paste into a chat that has this repository in front of it.
They are not wiki pages: they ask what you already know, read named files, answer from symbols rather
than memory, and finish by reporting what they checked and what they could not.</p>
<p>This page and the prompt pages beside it are the kit's own repository. Clone it into a checkout
with <code>git clone https://github.com/SDBlackBox/StarDrive-community-kit.git docs/kit</code> and each
prompt sits where its citations expect it. Every prompt page has a <b>Copy prompt</b> button that puts
the whole file on your clipboard &mdash; paste it, then ask your question. The text is embedded when
the page is built, so the button needs no network and the page reads with JavaScript off.</p>

<p class="meta">Generated by <code>build-site.py</code> in this folder from the table in it and the
prompt files beside it, which the pages embed at build time. Re-run <code>python3 build-site.py</code>
after editing a prompt. Vetted against <code>StarDrive@{VETTED}</code> on {CHECKED}; a page whose
numbers disagree with the code is a bug in the page.</p>

</main>
<aside id="prompts">
{sidebar('prompts/')}
</aside>
</div>
"""


def prompt_body(p):
    blob = BLOB + p["file"]
    how = "".join(f"<li>{h}</li>" for h in p["how"])
    bar = (
        '<a class="btn" href="../index.html">&larr; Index</a>\n'
        '<a class="btn" href="../weapon-tech-human.html">Era map</a>\n'
        f'<a class="btn" href="{REPO}">Game repository &nearr;</a>\n'
    )
    body = f"""
<header class="head">
 <p class="kicker"><span class="chip">{p['kind']}</span><code>{p['file']}</code></p>
 <h1>{p['title']}</h1>
 <p class="lede">{p['lede']}</p>
 <div class="acts">
  <button class="btn primary" id="copy">Copy prompt</button>
  <button class="btn" id="show">Show prompt</button>
  <a class="btn" href="{blob}">In the kit repo &nearr;</a>
 </div>
 <p class="msg" id="msg"></p>
</header>
<div class="shell">
<main>
<h2>How it works</h2>
<ul>{how}</ul>

<h2>What it needs</h2>
<p>{p['needs']}</p>

<h2>The prompt</h2>
<p class="note">{len(p['text']):,} characters, copied verbatim from <code>{p['file']}</code> at
build time. Copy takes the whole file, because that is what the prompt expects you to paste.</p>
<pre id="text" hidden>{escape(p['text'])}</pre>
</main>
<aside>
{sidebar("")}
</aside>
</div>
"""
    return page(p["short"] + " — StarDrive BlackBox", bar, body, JS)


def main():
    if not KIT.is_dir():
        sys.exit(f"missing {KIT} — the prompt pages are described from the kit")
    missing = [p["file"] for p in PROMPTS if not (KIT / p["file"]).is_file()]
    if missing:
        sys.exit("missing kit files: " + ", ".join(missing))
    OUT.mkdir(parents=True, exist_ok=True)

    (HERE / "index.html").write_text(page("StarDrive BlackBox", INDEX_BAR, index_body()), encoding="utf-8")
    for p in PROMPTS:
        p["text"] = (KIT / p["file"]).read_text(encoding="utf-8")
        (OUT / f"{p['slug']}.html").write_text(prompt_body(p), encoding="utf-8")
    print(f"wrote index.html and {len(PROMPTS)} pages in prompts/")


if __name__ == "__main__":
    main()
