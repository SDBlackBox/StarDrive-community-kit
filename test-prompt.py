#!/usr/bin/env python3
"""Check the published moddable-content prompt against this checkout.

    python3 docs/kit/test-prompt.py

Run from anywhere. The test rebuilds the pages (build-moddable.py --audit) and then checks:

  1. the .md contains exactly one pasteable prompt block, and the block carries the instructions the
     guide depends on: state the token cost first, produce a rerunnable generator rather than edited
     HTML, audit its own counts, and treat a key with no reader as dead;
  2. every documentation path, content path and script the block names exists here;
  3. the rendered site (moddable-content.html, moddable/*.html, prompts/moddable-content.html)
     exists and embeds the current text, so an edited prompt cannot ship an old page;
  4. the generator runs, writes one page per section, and prints counts that parse.

Exit status is 0 only when every check passes.
"""

import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
MD = HERE / "moddable-content-explainer-prompt.md"
SITE = HERE / "prompts" / "moddable-content.html"
HUB = HERE / "moddable-content.html"
SECTIONS = HERE / "moddable"
GENERATOR = HERE / "build-moddable.py"

failures = []


def check(ok, message):
    print(("ok   " if ok else "FAIL ") + message)
    if not ok:
        failures.append(message)


def prompt_block(text):
    blocks = re.findall(r"^```text\n(.*?)^```", text, re.S | re.M)
    return blocks


def main():
    text = MD.read_text(encoding="utf-8")
    blocks = prompt_block(text)
    check(len(blocks) == 1, f"one pasteable ```text block in {MD.name} (found {len(blocks)})")
    if len(blocks) != 1:
        return
    block = blocks[0]
    check(len(block) > 6000, f"the block is a whole prompt ({len(block):,} chars)")

    required = [
        ("token cost", "the block warns that a deep answer is token-expensive"),
        ("build-moddable.py", "the block names the generator"),
        ("moddable-data.py", "the block names the prose/data modules it must produce"),
        ("moddable-data-world.py", "the block names the world data module"),
        ("moddable-notes.py", "the block names the long-form notes module"),
        ("moddable-sections.py", "the block names the section module"),
        ("--audit", "the block requires the audit counts"),
        ("the deliverable is a generator", "the page request produces a script, not HTML"),
        ("Do not add the pages to the game repository", "output location is stated"),
        ("This item has no function in game.", "a dead key has one fixed sentence"),
        ("no reader found", "an unreadable tag must be reported as such"),
        ("Ship_Game", "the block says the C# is read too"),
        ("audit log", "the block requires a log, not just printed counts"),
        ("enum member", "the block says an enum-keyed name is not a field"),
        ("closed set", "the block says a fixed value set must be shown in full"),
        ("catalogue", "the block says a catalogue family lists the entries a file can name"),
    ]
    for phrase, why in required:
        check(phrase in block, f"block contains {phrase!r} — {why}")

    check("Otherwise, write a self-contained hub" not in block,
          "the fallback no longer tells the assistant to hand-write the HTML")

    # Paths named in the block that should resolve from the repository root.
    named = set()
    for raw in re.findall(r"\b(?:docs|game|Ship_Game)/[A-Za-z0-9_./-]+", block):
        token = raw.rstrip(".,;:)")
        if "*" in token or "<" in token:
            continue
        named.add(token)
    for token in sorted(named):
        check((REPO / token).exists(), f"path named in the block exists: {token}")

    for mod in ("build-moddable.py", "moddable-data.py", "moddable-data-world.py",
                "moddable-notes.py", "moddable-sections.py"):
        check((HERE / mod).exists(), f"script exists: docs/kit/{mod}")

    # Generated site must be newer than nothing: it must embed this text.
    marker = "the deliverable is a generator"
    check(HUB.exists(), "hub page exists: docs/kit/moddable-content.html")
    check(SITE.exists(), "prompt page exists: docs/kit/prompts/moddable-content.html")
    if SITE.exists():
        check(marker in SITE.read_text(encoding="utf-8"),
              "the rendered prompt page embeds the current text (re-run build-site.py if not)")
    if HUB.exists():
        hub = HUB.read_text(encoding="utf-8")
        check("Moddable content" in hub and "moddable/" in hub, "hub links to the section pages")
    pages = sorted(p.name for p in SECTIONS.glob("*.html")) if SECTIONS.exists() else []
    check(len(pages) == 7, f"seven section pages under docs/kit/moddable/ (found {len(pages)})")

    # The landing page must point at the guide, and quote the hub's counts rather than its own.
    index = HERE / "index.html"
    if HUB.exists() and index.exists():
        idx = index.read_text(encoding="utf-8")
        hub_text = HUB.read_text(encoding="utf-8")
        linked = re.findall(r'href="moddable/([\w-]+)\.html"', idx)
        check(sorted(set(linked)) == sorted(p[:-5] for p in pages),
              f"the landing page links all seven section pages (found {len(set(linked))})")
        for label in ("content files", "tags described", "families"):
            m = re.search(re.escape(label) + r": <b>([\d,]+)</b>", hub_text)
            check(bool(m) and m.group(1) in idx,
                  f"the landing page quotes the hub's {label} count ({m.group(1) if m else '?'})")

    # The generator itself: run it from the repo root as the prompt tells an assistant to.
    proc = subprocess.run([sys.executable, str(GENERATOR), "--audit"], cwd=str(REPO),
                          capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    check(proc.returncode == 0, f"build-moddable.py --audit exits 0 ({proc.returncode})")
    if proc.returncode != 0:
        print(out[-2000:])
        return
    check("section pages" in out and "families" in out, "the build reports pages, families and files")
    m = re.search(r"and (\d+) section pages", out)
    check(bool(m) and m.group(1) == "7", "the build writes one page per section")
    check("conformance: prose level 3" in out, "the build prints its own conformance counts")
    check("audit: level-3 over" in out, "the build prints the sentence-cap audit")
    check("fields declared but never read outside the declaration" in out,
          "the build separates a declared field from one a reader uses")

    # A YAML card that accepts a closed set must list it, and a catalogue must list its entries.
    page = SECTIONS / "map-creation.html"
    check(page.exists(), "the planet and sun cards are on the map-creation page")
    if page.exists():
        html_page = page.read_text(encoding="utf-8")
        types = (REPO / "game/Content/PlanetTypes.yaml").read_text(encoding="utf-8-sig")
        names = re.findall(r"(?m)^\s+Name:\s*(\S+)", types)
        missing = [n for n in names if n not in html_page]
        check(not missing, f"every planet type is listed by name ({len(names)} names, missing {missing[:5]})")
        suns = (REPO / "game/Content/Suns.yaml").read_text(encoding="utf-8-sig")
        ids = re.findall(r"(?m)^\s+Id:\s*(\S+)", suns)
        missing = [s for s in ids if s not in html_page]
        check(not missing, f"every sun Id is listed ({len(ids)} ids, missing {missing[:5]})")
        cats = ["Barren", "Desert", "Steppe", "Tundra", "Terran",
                "Volcanic", "Ice", "Swamp", "Oceanic", "GasGiant"]
        check(all(f"<code>{c}</code>" in html_page for c in cats),
              "the ten planet categories are shown as values, not only named in prose")
        check("GasBlue" in html_page and "NoAtmosphere" in html_page,
              "the atmosphere preset ids are shown as values")

    log = HERE / "moddable-audit.txt"
    check(log.exists(), "audit log exists: docs/kit/moddable-audit.txt")
    if log.exists():
        head = log.read_text(encoding="utf-8").splitlines()[0]
        check("violations 0" in head, f"no contradiction left in the audit log ({head})")

    print()
    if failures:
        print(f"{len(failures)} check(s) failed")
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
