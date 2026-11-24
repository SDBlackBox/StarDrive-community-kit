#!/usr/bin/env python3
"""Build the moddable-content reference: a hub plus one page per section.

    python3 docs/kit/build-moddable.py
    python3 docs/kit/build-moddable.py --audit

Counts, tag coverage and the "In vanilla" value summaries come from the checkout under
game/Content, so the page cannot claim a tag exists that does not or hide one it never described.
The prose lives in moddable-data.py, moddable-data-world.py, moddable-notes.py and
moddable-sections.py. Re-run this script after editing content or prose; do not edit the HTML.

--audit additionally lists every level-3 entry above the five-sentence soft cap, every
level-1 line that is not exactly one sentence, every card with no prose level 3, and every
numeric field with no Allowed range.
"""

import html
import importlib.util
import os
import pathlib
import re
import subprocess
import sys
from collections import Counter

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent


def star_drive_root():
    """The StarDrive checkout: $STARDRIVE_ROOT, else the checkout this kit sits inside."""
    env = os.environ.get("STARDRIVE_ROOT")
    candidates = [pathlib.Path(env).expanduser()] if env else []
    candidates.append(HERE.parent.parent)
    for candidate in candidates:
        if (candidate / "game" / "Content").is_dir():
            return candidate.resolve()
    sys.exit(
        "star_drive_root: no StarDrive checkout found in "
        + ", ".join(str(c) for c in candidates)
        + "; set STARDRIVE_ROOT=/path/to/StarDrive"
    )

REPO = star_drive_root()
CONTENT = REPO / "game" / "Content"
OUT = HERE / "moddable-content.html"
SECTION_DIR = HERE / "moddable"
CAP = 5
escape = html.escape


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def families():
    a = load("md_ships", HERE / "moddable-data.py")
    b = load("md_world", HERE / "moddable-data-world.py")
    return a.FAMILIES + b.FAMILIES


def sections():
    return load("md_sections", HERE / "moddable-sections.py").SECTIONS


def notes():
    return load("md_notes", HERE / "moddable-notes.py").NOTES


def files_of(fam):
    found = []
    for p in fam["paths"]:
        target = CONTENT / p
        if target.is_file():
            found.append(target)
        elif target.is_dir():
            ext = fam.get("ext")
            for f in target.rglob("*"):
                if f.is_file() and (ext is None or f.suffix.lower() == ext):
                    found.append(f)
    return found


XML_VALUE = re.compile(r"<([A-Za-z_][\w.\-]*)(?:\s[^<>]*)?>([^<>]*)</\1>")
KEY_VALUE = re.compile(r"(?m)^\s*([A-Za-z_][\w]*)\s*[=:]\s*(.*?)\s*$")


def harvest(fam, files):
    """(counts per tag, quotable samples per tag, comment above a YAML key).

    Every occurrence counts, so coverage matches the old tag scan; only short single-line values
    are kept as samples, because an "In vanilla" line cannot quote a paragraph. The comment above
    a YAML key is often the only statement of what the value means, so it is kept too.
    """
    counts, samples, comments = {}, {}, {}
    roots = set(fam.get("roots", []))
    for f in files:
        suf = f.suffix.lower()
        if suf not in (".xml", ".hull", ".design", ".yaml"):
            continue
        try:
            text = f.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        rel = str(f.relative_to(CONTENT))
        if suf == ".xml":
            pairs = XML_VALUE.findall(text)
        else:
            pairs = [(m.group(1), m.group(2)) for m in KEY_VALUE.finditer(text)]
        if suf == ".yaml":
            pending, gap = [], 0
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("#"):
                    pending.append(s.lstrip("#").strip())
                    gap = 0
                elif not s:
                    gap += 1
                    if gap > 1:
                        pending = []
                else:
                    m = re.match(r'\s*([A-Za-z_]\w*)\s*:', line)
                    if m and pending:
                        comments.setdefault(m.group(1),
                                            (rel, " ".join(p for p in pending if p)[:700]))
                    pending, gap = [], 0
        for name, value in pairs:
            if name in roots or name == "string" or name.startswith("ArrayOf"):
                continue
            counts[name] = counts.get(name, 0) + 1
            value = " ".join(value.split())
            if suf == ".yaml":
                value = re.sub(r"\s+#.*$", "", value).strip()
            if value and len(value) <= 48:
                samples.setdefault(name, []).append((rel, value))
    return counts, samples, comments


def documented(fam):
    names, prefixes, suffixes = [], [], []
    for g in fam["groups"]:
        for t in g["tags"]:
            for part in t["name"].split("/"):
                part = part.strip()
                if not part:
                    continue
                if part.startswith("*"):
                    suffixes.append(part[1:].lower())
                elif part.endswith("*"):
                    prefixes.append(part[:-1].lower())
                else:
                    names.append(part.lower())
    return names, prefixes, suffixes


def is_documented(tag, pats):
    t = tag.lower()
    names, prefixes, suffixes = pats
    return (t in names or any(t.startswith(p) for p in prefixes)
            or any(t.endswith(s) for s in suffixes))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


NUM = re.compile(r"-?\d+(?:\.\d+)?")


def fmt_num(x):
    return f"{x:,.6g}" if abs(x) < 1e6 else f"{x:.0f}"


def snippet(path, tag, value):
    """The line a modder would type, in the syntax of the file it came from."""
    suffix = pathlib.Path(path).suffix.lower()
    if suffix == ".xml":
        return f"<{tag}>{value}</{tag}>"
    if suffix in (".yaml", ".yml"):
        return f"{tag}: {value}"
    return f"{tag}={value}"


def stat_line(entries, tag=None, fmt=""):
    """Which vanilla files set a tag and the values each one actually uses.

    No range, median or "common value" summary: those hid the only fact a modder needs, which is
    the value written beside a named entry. The per-tag NOTES can override this line with
    vanilla=... where the file alone does not say what the entry is or what the number computes to.

    A tag every file sets exactly once describes the file itself, like a race's StartingScout or a
    hull's HullName. One file is quoted in its own syntax, and the rest are counted, instead of
    repeating "1 entry: ..." for 125 near-identical lines and closing with "122 more files".
    """
    per = {}
    for p, v in entries:
        per.setdefault(p, []).append(v)
    vals = {p: list(dict.fromkeys(v)) for p, v in per.items()}
    if (tag and re.fullmatch(r"[A-Za-z_][\w.\-]*", tag) and len(per) > 3
            and all(len(v) == 1 for v in vals.values())):
        counts = Counter(v[0] for v in vals.values())
        # The value most files share, but tie-break on the file name so the quoted example stays
        # the same from one build to the next.
        best = max(counts.values())
        path, value = min((p, v[0]) for p, v in vals.items() if counts[v[0]] == best)
        tail = (f"all {len(per)} files set it the same way." if len(counts) == 1
                else f"the other {len(per) - 1} files set their own.")
        return f"In vanilla: {path} \u2014 {snippet(path, tag, value)}; {tail}"
    bits = []
    for p in sorted(per)[:3]:
        vals = []
        for v in per[p]:
            if v not in vals:
                vals.append(v)
        shown = ", ".join(vals[:4])
        if len(vals) > 4:
            shown += f", +{len(vals) - 4} more"
        n = len(per[p])
        bits.append(f"{p} \u2014 {n} entr{'y' if n == 1 else 'ies'}: {shown}")
    if len(per) > 3:
        bits.append(f"{len(per) - 3} more files")
    return "In vanilla: " + "; ".join(bits) + "."


def sentence_count(text):
    t = text
    for abbr in ("e.g.", "i.e.", "etc.", "vs.", "No.", "cf."):
        t = t.replace(abbr, abbr.replace(".", "\u2024"))
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"\u201c(\[])", t)
    return len([p for p in parts if p.strip()])


CSS = """
:root{--bg:#14171c;--panel:#1b1f26;--ink:#e6e8ea;--dim:#8b949e;--line:#2b313a;--gold:#ffd479;--link:#8ecbff;--ok:#8ad06a;--warn:#e0a070}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 Georgia,serif}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
code,.mono{font:12.5px ui-monospace,monospace;color:#c9d1d9;background:#20252d;padding:0 3px;border-radius:3px}
.bar{position:sticky;top:0;z-index:9;background:rgba(20,23,28,.96);border-bottom:1px solid var(--line)}
.bar .in{max-width:1200px;margin:0 auto;padding:9px 24px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.btn{display:inline-block;font:12px ui-monospace,monospace;padding:5px 11px;border:1px solid #3a424e;border-radius:999px;background:var(--panel);color:var(--ink);cursor:pointer}
.btn:hover{border-color:var(--link);text-decoration:none}
.btn.on{border-color:var(--gold);color:var(--gold)}
input#q{flex:1;min-width:220px;font:12.5px ui-monospace,monospace;color:var(--ink);background:#0f1216;border:1px solid #3a424e;border-radius:999px;padding:6px 12px}
.head{max-width:1200px;margin:0 auto;padding:32px 24px 4px}
h1{font-size:27px;margin:0 0 8px;line-height:1.25}
p.lede{color:var(--dim);max-width:86ch;margin:0 0 12px}
.wrap{max-width:1200px;margin:0 auto;padding:6px 24px 70px}
.facts{display:flex;gap:16px;flex-wrap:wrap;font:12px ui-monospace,monospace;color:#c9d1d9;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px 12px;margin:12px 0}
.facts b{color:var(--gold);font-weight:normal}
h2{font-size:13px;text-transform:uppercase;letter-spacing:1.1px;font-family:ui-monospace,monospace;color:#c9d1d9;margin:34px 0 12px;border-bottom:1px solid var(--line);padding-bottom:6px}
h3{font-size:15px;margin:22px 0 8px}
details{border:1px solid var(--line);border-radius:7px;background:var(--panel);margin:0 0 8px}
details>summary{cursor:pointer;padding:10px 13px;list-style:none}
details>summary::-webkit-details-marker{display:none}
details>summary:before{content:"\\25B6";display:inline-block;width:16px;color:var(--dim);font-size:10px;transform:translateY(-1px)}
details[open]>summary:before{content:"\\25BC"}
.fam{margin:0 0 12px;background:#171b21}
.fam>summary{padding:13px 15px}
.fam>summary .t{font-size:17px;color:var(--gold)}
.body{padding:2px 15px 14px}
.pill{font:10.5px ui-monospace,monospace;text-transform:uppercase;letter-spacing:.4px;border:1px solid #4a5260;border-radius:9px;padding:1px 7px;color:var(--dim);margin-left:7px}
.pill.t1{border-color:#6b5a2b;color:var(--gold)}.pill.t2{border-color:#2f5a6b;color:#8ecbff}.pill.t3{border-color:#3a4a3a;color:var(--ok)}
.pill.idx{border-color:#6b4a2b;color:var(--warn)}
.l1{color:#cfd6dd}
.meta{font:11.5px ui-monospace,monospace;color:var(--dim);margin:6px 0 10px}
.meta b{color:#c9d1d9;font-weight:normal}
.lv2{color:#c3cbd3;margin:4px 0 6px}
details.lv3,details.note{border-color:#232a33;background:#161a20;margin:6px 0 10px}
details.lv3>summary,details.note>summary{font:11.5px ui-monospace,monospace;color:var(--dim);padding:6px 10px}
details.lv3 .in,details.note .in{padding:0 11px 9px;color:#b9c2cb}
details.lv3 .in p{margin:6px 0}
.vanilla{font:11.5px/1.55 ui-monospace,monospace;color:#9fb0a6;background:#141a17;border-left:2px solid #3d5a46;padding:6px 8px;margin:8px 0 2px}
.range{font-size:13.5px;color:#c8d3c0;border-left:2px solid #3d5a46;padding-left:8px;margin:6px 0}
.crit{border-color:#6b4a2b;background:#201a14}
pre.code{font:12px/1.55 ui-monospace,monospace;background:#0f1216;border:1px solid var(--line);border-radius:6px;padding:10px 12px;overflow:auto;color:#c9d1d9;margin:8px 0}
.grp{background:#181d23;margin:8px 0}
.grp>summary .g{font-size:14px;color:#e6e8ea}
.tags{margin:8px 0 0;padding:0;list-style:none}
.tag{background:#1b2027;margin:5px 0;border-color:#242b34}
.tag>summary{padding:6px 10px;font-size:13.5px}
.tag .nm{font:12.5px ui-monospace,monospace;color:var(--gold)}
.tag .ty{font:10.5px ui-monospace,monospace;color:var(--dim);margin-left:7px}
.tag .tx{padding:0 11px 8px;color:#b9c2cb;font-size:14px}
table{border-collapse:collapse;width:100%;font:12.5px ui-monospace,monospace;margin:6px 0 12px}
th,td{text-align:left;padding:6px 9px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--dim);font-weight:normal}
td.n{white-space:nowrap;color:var(--gold)}
.note-p{color:var(--dim);font-size:13px}
ol,ul{padding-left:22px}
li{margin:0 0 5px}
.missing{font:11.5px ui-monospace,monospace;color:var(--warn)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px;margin:10px 0}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px 16px}
.card:hover{border-color:var(--link);text-decoration:none}
.card .ct{font-size:17px;color:var(--gold);display:block;margin-bottom:4px}
.card .cb{color:var(--dim);font-size:13.5px;display:block;margin-bottom:8px}
.card .cf{font:11px ui-monospace,monospace;color:#c9d1d9;display:block}
.foot{border-top:1px solid var(--line);margin-top:34px;padding-top:10px;font:12px ui-monospace,monospace;color:var(--dim)}
.vals{border-collapse:collapse;width:100%;margin:10px 0;font-size:13.5px}
.vals caption{text-align:left;color:var(--dim);font-size:12.5px;padding-bottom:6px}
.vals th{text-align:left;color:var(--gold);font-weight:600;border-bottom:1px solid var(--line);padding:4px 8px}
.vals td{border-bottom:1px solid var(--line);padding:4px 8px;vertical-align:top}
.vals td:first-child{white-space:nowrap}
.miss{color:#d98c8c;font-style:italic}
.toc{columns:2;column-gap:34px;font-size:14px}
@media(max-width:760px){.toc{columns:1}}
"""

JS = """
const q = document.getElementById('q');
const fams = [...document.querySelectorAll('details.fam')];
const tags = [...document.querySelectorAll('details.tag')];
function apply() {
  const s = q.value.trim().toLowerCase();
  for (const t of tags) t.hidden = !!s && !t.textContent.toLowerCase().includes(s);
  for (const f of fams) {
    const hit = !s || f.textContent.toLowerCase().includes(s);
    f.hidden = !hit;
    if (hit && s) f.open = true;
  }
}
q.addEventListener('input', apply);
document.getElementById('open').onclick = () => fams.forEach(f => f.open = true);
document.getElementById('close').onclick = () => fams.forEach(f => f.open = false);
"""


STUB_L3 = re.compile(r"(?i)^(vanilla\s+[-\d.,]+|[-+]?\d[\d.,]*)\s*\.?$")


def detail_of(t):
    """The prose level 3, or empty when the field only carries a value restated elsewhere."""
    l3 = (t.get("l3") or "").strip()
    return "" if not l3 or STUB_L3.match(l3) else l3


def dead_key(t):
    """The card whose entry is the fixed dead-key sentence, wherever the author put it."""
    return (t.get("l1") or "").strip() == DEAD_ENTRY or detail_of(t) == DEAD_ENTRY


def unexplained(t, keyed, elsewhere="", quote=("", "")):
    """True for the cards that print "Not explained anywhere in this guide yet."

    One predicate for both the page and the log: the block is the page advertising a gap, so any
    card that reaches it has to be counted as an error in the same run. Dead-key cards are entries,
    not gaps, and say so instead.
    """
    return (not detail_of(t) and not dead_key(t) and not keyed
            and not (quote[1] if quote else "") and not elsewhere)


def values_badge(t, keyed):
    """The "values only" pill: no prose and no map, so the card can only list vanilla's numbers.

    The pill is the page admitting it has nothing to say about what to put in the field, so it is
    an error in the log (``values-only``), not a neutral badge.
    """
    return not detail_of(t) and not dead_key(t) and not keyed


def span_of(entries, ty):
    """Smallest and largest numeric value the content writes for a field.

    A card with no traced prose still tells a modder something checkable: the span vanilla itself stays
    inside. It is not a bound the code enforces, so the label says span, not range.
    """
    if not entries or not re.search(r"\b(int|float|double)\b", ty):
        return ""
    nums = []
    for _, v in entries:
        try:
            nums.append(float(v))
        except ValueError:
            continue
    if len(nums) < 3:
        return ""
    lo, hi = min(nums), max(nums)
    if lo == hi:
        return ""
    return f"{fmt_num(lo)} to {fmt_num(hi)} across {len(nums)} vanilla values"


UNTRACED = {"explained": 0, "not": 0}
NO_L2 = [0]
NOT_EXPLAINED = {"field": 0, "nofield": 0}
UNREAD = [0]
CODE = None


def strip_comments(text):
    """Blank out C# comments while keeping strings and line numbers.

    A regex cannot do this: `/*` inside a string literal is not a comment, and treating it as one
    silently deletes the rest of the file, which would make live fields look unread.
    """
    out = list(text)
    i, n = 0, len(text)
    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = " "
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
        elif text[i] == '@' and i + 1 < n and text[i + 1] == '"':
            i += 2
            while i < n:
                if text[i] == '"':
                    if i + 1 < n and text[i + 1] == '"':
                        i += 2
                        continue
                    i += 1
                    break
                i += 1
        elif text[i] in "\"'":
            q = text[i]
            i += 1
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == q:
                    i += 1
                    break
                i += 1
        else:
            i += 1
    return "".join(out)


def code_index():
    """Public fields, string literals and enum members declared in the game code.

    A content key can only change the game if something in the code consumes it. A class field of the
    same name is the strongest evidence, because the XML and YAML loaders bind by name. A string
    literal is weaker evidence but still a reader. Neither means nothing reads the key at all, which
    a modder has to be told rather than left to guess.
    """
    global CODE
    if CODE is None:
        fields, strings, enums, members, tokens = {}, set(), {}, {}, set()
        reads = {}
        # The type may contain spaces inside generics (`Map<ShipCosts, float>`); without that a map
        # field is invisible and the key that binds into it looks unread.
        decl = re.compile(r'^\s*(?:\[[^\]]*\]\s*)*(?:public|protected|internal)\s+'
                          r'(?:readonly\s+|static\s+)*([\w<>\[\],\.\?\s]+?)\s+(\w+)\s*(?:[;={])')
        # A local declaration of the same name (`const float GlowScale = 0.5f` in another class) is
        # a different symbol. Counting it would credit the content field with a reader that never
        # sees it, and the card would name the wrong file.
        local_decl = re.compile(r'\b(?:const\s+)?(?:float|double|int|uint|bool|string|byte|var)\s+(\w+)\s*[;=]')
        enum_re = re.compile(r'\benum\s+(\w+)\s*(?::\s*\w+)?\s*\{(.*?)\}', re.S)
        ident = re.compile(r'[A-Za-z_]\w*')
        paths = list((REPO / "Ship_Game").rglob("*.cs"))
        decl_names = {}
        for p in paths:
            text = p.read_text(encoding="utf-8", errors="ignore")
            rel = p.relative_to(REPO).as_posix()
            code = strip_comments(text)
            owner = ""
            for i, line in enumerate(code.splitlines(), 1):
                m = re.search(r'\b(?:class|struct)\s+(\w+)', line)
                if m:
                    owner = m.group(1)
                d = decl.match(line)
                if d:
                    fields.setdefault(d.group(2), []).append((owner, d.group(1), rel, i))
                    decl_names.setdefault((rel, i), set()).add(d.group(2))
            strings.update(re.findall(r'"([^"\n]{2,80})"', text))
            tokens.update(ident.findall(code))
            for m in enum_re.finditer(code):
                vals = []
                for part in m.group(2).split(","):
                    mm = re.match(r'\s*(\w+)\s*(?:=\s*(.+))?$', part.strip())
                    if mm:
                        vals.append((mm.group(1), (mm.group(2) or "").strip()))
                        members.setdefault(mm.group(1), set()).add(m.group(1))
                enums.setdefault(m.group(1), vals)
        # A declaration is not a reader: a field nobody uses outside its own declaration cannot
        # change anything, and a key bound to it is as inert as one with no field at all.
        for p in paths:
            rel = p.relative_to(REPO).as_posix()
            code = strip_comments(p.read_text(encoding="utf-8", errors="ignore"))
            for i, line in enumerate(code.splitlines(), 1):
                declared = decl_names.get((rel, i), ())
                local = set(local_decl.findall(line))
                for name in set(ident.findall(line)).intersection(fields).difference(declared).difference(local):
                    n, first = reads.get(name, (0, ""))
                    reads[name] = (n + 1, first or f"{rel}:{i}")
        CODE = dict(fields=fields, strings=strings, enums=enums, members=members, tokens=tokens,
                    reads=reads)
    return CODE


def field_of(name, roots=()):
    """The (class, type, file, line) declaring this key, or None.

    A dotted key such as `Mod.UseVanillaTechs` is a nesting path, so its last segment is the field.
    Names are not unique across the codebase (`Category` also exists on a sound effect), so a
    declaration on the family's own root class wins before the first one found.
    """
    fields = code_index()["fields"]
    cands = fields.get(name) or fields.get(name.rsplit(".", 1)[-1]) or []
    for c in cands:
        if c[0] in roots:
            return c
    return cands[0] if cands else None


def reads_of(name):
    """(count, first path:line) of uses of this field outside its own declaration."""
    return code_index()["reads"].get(name.rsplit(".", 1)[-1]) or (0, "")


def evidence_for(t, fam):
    """What the build says about this key: the field, its readers, its enum values, or that nothing
    reads it. A field declared but never used is reported as inert, not as a working key."""
    name = t["name"]
    leaf = name.rsplit(".", 1)[-1]
    idx = code_index()
    fi = field_of(name, fam.get("roots") or ())
    if fi:
        cls, ty, rel, line = fi
        n, first = reads_of(leaf)
        if not n:
            UNREAD[0] += 1
        out = (f'<p class="where"><b>Declared in the code as</b> <code>{escape(cls)}.{escape(leaf)}</code> '
               f'({escape(ty)}) at <code>{escape(rel)}:{line}</code>')
        vals = idx["enums"].get(ty)
        if vals:
            listed = ", ".join(f'<code>{escape(v)}</code>' + (f' = {escape(n)}' if n else "")
                               for v, n in vals)
            out += f'. The type is an enum, so these are the only values the loader accepts: {listed}'
        if n:
            out += (f'. <b>Referenced</b> in {n} place{"s" if n != 1 else ""} outside the declaration, '
                    f'the first at <code>{escape(first)}</code>')
        else:
            out += ('. <b>No code outside the declaration reads it</b>, so a file may set the key but '
                    'changing it cannot change the game')
        return out + '.</p>'
    owner_enums = sorted(idx["members"].get(leaf) or ())
    if owner_enums:
        # `Support` and `Bomber` are members of several enums; naming whichever came first would
        # attribute the key to an unrelated type, which is worse than saying it is ambiguous.
        if len(owner_enums) == 1:
            who = f'a member of <code>{escape(owner_enums[0])}</code>'
        else:
            listed = ", ".join(f'<code>{escape(e)}</code>' for e in owner_enums[:4])
            if len(owner_enums) > 4:
                listed += f" and {len(owner_enums) - 4} more"
            who = (f'a member of {len(owner_enums)} enums the code declares ({listed}), and nothing '
                   'here ties the key to one of them')
        return (f'<p class="where"><b>Not a field: an enum member.</b> The name is {who}. A key that '
                'sets an enum is resolved by the loader as that name, so the map it lands in is the '
                'thing to read, not a field of this name.</p>')
    if leaf in idx["strings"] or leaf in idx["tokens"]:
        return ('<p class="where"><b>No field of this name.</b> The name occurs in the code but not as '
                'a field or property, so something may read it through a lookup; nothing here has '
                'traced that.</p>')
    return ('<p class="where"><b>No reader.</b> No field, property, enum member, string or identifier '
            'in the build matches this name, so nothing consumes the key: the content may write it, '
            'but changing it cannot change the game.</p>')


ENUM_MAP = {}


def enum_map_field(enum):
    """The field declared `Map<enum, …>`: where a key of this enum lands at load time."""
    if enum not in ENUM_MAP:
        # Several maps can be keyed by one enum: `WeaponTags` in EmpireData holds modifiers, not the
        # content weights, so the float-valued map is the one a Research.yaml key lands in.
        strict = re.compile(r'\bMap<\s*' + re.escape(enum) + r'\s*,\s*float\s*>')
        loose = re.compile(r'\bMap<\s*' + re.escape(enum) + r'\s*,')
        ENUM_MAP[enum] = None
        for pat in (strict, loose):
            for name, cands in code_index()["fields"].items():
                for c in cands:
                    if pat.search(c[1]):
                        ENUM_MAP[enum] = (name, c)
                        break
                if ENUM_MAP[enum]:
                    break
            if ENUM_MAP[enum]:
                break
    return ENUM_MAP[enum]


def key_evidence(t):
    """A key of an enum-keyed map: the fields it binds into and the names the loader accepts.

    `ShipCostModifiers` is `Map<ShipCosts, float>`, so its keys are enum names the loader resolves,
    not fields. Looking the name up as a field finds nothing, and looking it up as an enum member
    can find an unrelated enum of the same name. The map declaration is the only honest trace, and
    a name such as `GroundCombat` sits in three different maps, so all of them are listed.
    """
    keys = t.get("key") or ()
    if isinstance(keys, str):
        keys = (keys,)
    idx = code_index()
    maps, accepted, all_names, primary = [], [], set(), None
    for enum in keys:
        vals = idx["enums"].get(enum) or []
        if not vals:
            continue
        names = [v for v, _ in vals]
        all_names.update(names)
        found = enum_map_field(enum)
        if found:
            field, (cls, ty, rel, line) = found
            maps.append(f'<code>{escape(cls)}.{escape(field)}</code> '
                        f'(<code>{escape(ty)}</code> at <code>{escape(rel)}:{line}</code>)')
            if primary is None:
                primary = field
        else:
            maps.append(f'an unnamed <code>Map&lt;{escape(enum)}, …&gt;</code>')
        accepted.append(f'<code>{escape(enum)}</code>: '
                        + ", ".join(f'<code>{escape(v)}</code>' for v in names))
    if not accepted:
        return ""
    out = [f'<p class="where"><b>Key of</b> ' + "; ".join(maps) + '. The loader resolves the name as '
           'an enum member, so the only names these maps read are ' + "; ".join(accepted) + '.']
    if primary:
        n, first = reads_of(primary)
        if n:
            out.append(f' <b>Referenced</b> in {n} place{"s" if n != 1 else ""} outside the '
                       f'declaration, the first at <code>{escape(first)}</code>')
    out.append('</p>')
    if t["name"] not in all_names:
        out.append(f'<p class="where"><b>Not one of them.</b> <code>{escape(t["name"])}</code> is not '
                   'a member of any of those enums, so the loader does not read this key as a '
                   'setting.</p>')
    return "".join(out)


def _yaml_section_ids(rel, key):
    """Every `Id` inside a top-level `key:` block of a content YAML file, in file order.

    An id list defined in content is as closed as an enum: `AtmosphereType` only resolves against
    the presets under `AtmosphereTypes`, and a name that is not there logs an error and does nothing.
    """
    p = CONTENT / rel
    if not p.is_file():
        return []
    lines = p.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    start = indent = None
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*)' + re.escape(key) + r':\s*(?:#.*)?$', line)
        if m:
            start, indent = i + 1, len(m.group(1))
            break
    if start is None:
        return []
    out = []
    for line in lines[start:]:
        if line.strip() and not line.startswith(" " * (indent + 1)):
            break
        m = re.search(r'\bId:\s*"?([A-Za-z_][\w.-]*)"?', line)
        if m:
            out.append(m.group(1))
    return out


def _yaml_key_values(rel, key):
    """The distinct scalar values a key takes in one content file, in first-seen order.

    A numeric stage (DysonRings Type) is not an enum: its closed set is whatever stages the file
    defines, and a card that lists none leaves a modder guessing which numbers exist.
    """
    p = CONTENT / rel
    if not p.is_file():
        return []
    text = p.read_text(encoding="utf-8-sig", errors="replace")
    out = []
    for m in re.finditer(r'(?m)^\s+' + re.escape(key) + r':\s*(\S+)', text):
        v = re.sub(r'\s+#.*$', '', m.group(1)).strip().strip('"')
        if v and v not in out:
            out.append(v)
    return out


def values_source(src):
    """(where the closed set comes from, [(value, …)]) for a declared values= source."""
    if src.startswith("key:"):
        _, rel, key = src.split(":", 2)
        return (f'<code>{escape(key)}</code> in <code>{escape(rel)}</code>',
                [(v, "") for v in _yaml_key_values(rel, key)])
    if src.startswith("enum:"):
        enum = src[5:]
        return (f"the <code>{escape(enum)}</code> enum in the code",
                [(v, n) for v, n in code_index()["enums"].get(enum, ())])
    if src.startswith("ids:"):
        _, rel, key = src.split(":", 2)
        return (f"<code>{escape(key)}</code> in <code>{escape(rel)}</code>",
                [(v, "") for v in _yaml_section_ids(rel, key)])
    return ("", [])


def values_table(t):
    """Every value the loader accepts for this field, each with what choosing it does."""
    spec = t.get("values")
    if not spec:
        return ""
    src, gloss = spec if isinstance(spec, tuple) else (spec, {})
    where, expected = values_source(src)
    if not expected:
        return ""
    rows = []
    for name, _ in expected:
        why = (gloss.get(name) or "").strip()
        body = escape(why) if why else '<span class="miss">no explanation yet</span>'
        rows.append(f'<tr><td><code>{escape(name)}</code></td><td>{body}</td></tr>')
    return (f'<table class="vals"><caption>The {len(expected)} values the loader accepts here, from '
            f'{where}</caption><tr><th>value</th><th>what choosing it does</th></tr>'
            + "".join(rows) + '</table>')


def values_problem(t, fi):
    """A closed set with no value list, or a list that disagrees with the loader.

    A YAML field that accepts an enum, an array of one, or an id list defined in another content
    file can only take those names. A card that describes the field and never says which names it
    takes leaves the reader to guess, which is the failure this rule exists to catch.
    """
    spec = t.get("values")
    if spec:
        src, gloss = spec if isinstance(spec, tuple) else (spec, {})
        _, expected = values_source(src)
        names = [v for v, _ in expected]
        declared = list(gloss)
        missing = [n for n in names if n not in declared]
        unknown = [n for n in declared if n not in names]
        if missing or unknown:
            return ("violation", "value-set-wrong",
                    "the card's value list does not match the loader's",
                    f'source={src} missing={",".join(missing) or "-"} '
                    f'unknown={",".join(unknown) or "-"}')
        unglossed = [n for n in names if not (gloss.get(n) or "").strip()]
        if unglossed:
            return ("violation", "value-unexplained",
                    f"{len(unglossed)} of {len(names)} accepted values have no explanation",
                    f'values={",".join(unglossed)}')
        return None
    ty = (fi[1].replace("[]", "").strip() if fi else "")
    members = [v for v, _ in code_index()["enums"].get(ty, ())] if ty else []
    if (t.get("ty") or "").strip() == "enum" or members:
        return ("violation", "values-missing",
                "a closed set of values is accepted here and the card lists none of them",
                f'enum={ty or "unresolved field type"}')
    return None


def catalogue_records(fam):
    """One record per entry in a catalogue family, read from the shipped content.

    A family whose file is a list of named entries (planet types, suns) has no fixed tag set: the
    values a modder needs are the entries themselves, and they are only correct if they are read
    from the files rather than remembered.
    """
    spec = fam.get("catalogue")
    if not spec:
        return []
    recs = []
    for f in files_of(fam):
        try:
            text = f.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        starts = list(re.finditer(r'(?m)^(\s*)-\s+[A-Za-z_]\w*:\s*$', text))
        for i, m in enumerate(starts):
            end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
            rec = {}
            for fm in re.finditer(r'(?m)^\s+([A-Za-z_]\w*):\s*(\S.*?)\s*$', text[m.end():end]):
                rec.setdefault(fm.group(1),
                               re.sub(r'\s+#.*$', '', fm.group(2)).strip().strip('"'))
            if rec.get(spec["key"]):
                recs.append(rec)
    return recs


def catalogue_html(fam):
    """The catalogue as a table of the values a file can name, with what each one is."""
    spec = fam.get("catalogue")
    if not spec:
        return "", []
    recs = catalogue_records(fam)
    rows = []
    for r in recs:
        facts = [f"{label} {r[f]}" if label else r[f]
                 for f, label in spec.get("fields", []) if r.get(f)]
        body = escape(", ".join(facts)) if facts else '<span class="miss">no facts</span>'
        rows.append(f'<tr><td><code>{escape(r[spec["key"]])}</code></td><td>{body}</td></tr>')
    title = spec.get("title") or "Every value in vanilla"
    note = spec.get("note") or ""
    table = (f'<details class="note" open><summary>{escape(title)} ({len(recs)})</summary>'
             '<div class="in">'
             + (f'<p class="note-p">{escape(note)}</p>' if note else "")
             + '<table class="vals"><tr><th>value</th><th>what it is in vanilla</th></tr>'
             + "".join(rows) + '</table></div></details>')
    return table, recs


def _mentions(text, name):
    """Whole-word match, so a tag name inside a longer word does not count."""
    return bool(text) and re.search(r'(?<![\w])' + re.escape(name) + r'(?![\w])', text) is not None


def explained_elsewhere(name, fam, group, sec):
    """The prose above that already discusses this tag, as an anchor, or empty.

    A card with no traced reader is not necessarily unexplained by the page: the family notes,
    the example box and the section introduction often cover the field in passing. Say where,
    so the card points at the explanation instead of claiming there is none.
    """
    aid = fam["id"]
    notch = (fam.get("notation") or {}).get("body", "")
    sources = [
        (f'<a href="#{aid}">the {escape(fam["title"])} family notes</a>',
         [fam.get("l2", ""), fam.get("l3", "")]),
        (f'<a href="#{aid}">the worked example for this family</a>', [notch]),
        (f'<a href="#{aid}">the group notes</a>',
         [group.get("l2", ""), group.get("l3", "")]),
        (f'<a href="#{sec["id"]}">the section introduction</a>',
         [sec.get("intro", ""), sec.get("l3", ""), sec.get("notes", "")]) if sec else ("", []),
    ]
    for where, texts in sources:
        if any(_mentions(x, name) for x in texts):
            return f'{where} mention <code>{escape(name)}</code>; read that before changing it'
    return ""


AUDIT = []
# A level 2 that is still one of these has not been written for this key. A fragment such as
# "Multiplier." or "Per delivery." is the same defect in a different shape, so it is caught by the
# word count and sentence-ending test in classify() rather than by listing every stub.
GENERIC_L2 = {"free text used by code lookups."}
DEAD_ENTRY = "This item has no function in game."
KNOWN_FILE = HERE / "moddable-audit-known.txt"
AUDIT_FILE = HERE / "moddable-audit.txt"


def audit_add(sec, fam, t, cls, code, msg, ev="", qual=""):
    """One row per card. Two cards in a family can share a tag name (a cue's Volume and a category's
    Volume), and a shared id would make the two lines in the log indistinguishable."""
    ident = f'{sec}/{fam["id"]}/{t["name"]}' + (f' [{qual}]' if qual else '')
    AUDIT.append(dict(id=ident, cls=cls, code=code, msg=msg, ev=ev))


def classify(t, fam, entries=()):
    """Every issue on this card: contradictions, then a missing or generic entry, then readers.

    A card with no authored level 3 does not explain its key, whatever the generated one-liner says:
    that is a violation, because the page would otherwise present the field name as coverage. Only
    relationships the index can prove are checked. A level-3 that was written by hand is not
    re-checked here: whether its bound is the right bound needs a reader, and pretending a string
    check could decide it is how a guide ends up confident and wrong.
    """
    name = t["name"]
    leaf = name.rsplit(".", 1)[-1]
    idx = code_index()
    # The fixed dead-key sentence is an entry, not a gap: the prompt tells the author to stop there.
    if dead_key(t):
        return []
    keys = t.get("key") or ()
    if isinstance(keys, str):
        keys = (keys,)
    if keys:
        missing = [k for k in keys if k not in idx["enums"]]
        if missing:
            return [("violation", "key-unknown-enum",
                     f'key names no enum in the code: {", ".join(missing)}', f'key={",".join(keys)}')]
        allowed = set()
        for k in keys:
            allowed.update(v for v, _ in idx["enums"][k])
        if name not in allowed:
            return [("violation", "key-not-a-member",
                     f'{name} is not a member of {", ".join(keys)}', f'key={",".join(keys)}')]
        if not any(enum_map_field(k) for k in keys):
            return [("violation", "key-no-map", "no Map<enum, ...> field reads this enum",
                     f'key={",".join(keys)}')]
        return []
    # Values are structural too: a field accepting a closed set must say which names it takes, and
    # an authored paragraph is exactly where an unlisted value hides.
    fi = field_of(name, fam.get("roots") or ())
    if str(fam.get("fmt", "")).upper().startswith("YAML"):
        found = values_problem(t, fi)
        if found:
            return [found]
    # A keyed card is checked even when prose was written for it: the map is the evidence, and an
    # authored paragraph is exactly where an unattributed key hides.
    detail = detail_of(t)
    issues = []
    ev = f"{fi[0]}.{leaf} at {fi[2]}:{fi[3]}" if fi else ""
    if not detail:
        issues.append(("violation", "values-only",
                       "no authored entry: the card can only be marked 'values only', so it says "
                       "nothing about what to put in the field or what the code does with it", ev))
    else:
        l2 = (t["l2"] or "").strip()
        if not l2:
            issues.append(("violation", "entry-no-l2",
                           "the card has an entry but no level-2 summary", ev))
        elif l2.lower() in GENERIC_L2:
            issues.append(("violation", "generic-blurb",
                           "level-2 is a canned one-liner, not what reads the value", ev))
        elif len(re.findall(r"[A-Za-z][\w'-]*", l2)) < 6 or not re.search(r"[.!?]$", l2):
            issues.append(("violation", "generic-blurb",
                           "level-2 is a fragment, not what reads the value", ev))
        return issues
    members = sorted(idx["members"].get(leaf) or ())
    if fi:
        cls, ty, rel, line = fi
        n, first = reads_of(leaf)
        if not n:
            issues.append(("finding", "inert-field",
                           "declared but nothing outside the declaration reads it", ev))
        return issues
    if members and str(fam.get("fmt", "")).upper().startswith("YAML") \
            and any(re.fullmatch(r"-?\d+(?:\.\d+)?", v.strip()) for _, v in entries) \
            and any(enum_map_field(e) for e in members):
        # A YAML key that is one float, is a member of an enum some Map<Enum, float> reads, and is
        # not annotated with key= is the shape that produced a card claiming Support belonged to
        # GameText. A name that merely equals an enum value elsewhere (FireArc, Tutorials) is not.
        issues.append(("violation", "enum-name-unclaimed",
                       "name is an enum member but the card claims no map",
                       f'enums={",".join(members[:4])}'))
        return issues
    if leaf in idx["strings"] or leaf in idx["tokens"]:
        return issues
    issues.append(("finding", "no-reader",
                   "no field, enum member, string or identifier matches this name", ""))
    return issues


def report_audit():
    """Write the log the next pass reads, and fail under --audit while an error survives.

    A violation is the page disagreeing with the code, or claiming an explanation it does not have:
    a card with no authored entry is an error, not coverage. Findings stay a backlog for keys that
    are explained but carry a known reader problem.
    """
    known = {}
    if KNOWN_FILE.exists():
        for line in KNOWN_FILE.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                known[parts[0]] = parts[1]
    for a in AUDIT:
        if a["cls"] == "finding" and a["id"] in known:
            a["cls"] = "known"
    AUDIT.sort(key=lambda a: (a["cls"] != "violation", a["id"], a["code"]))
    viol = [a for a in AUDIT if a["cls"] == "violation"]
    new = [a for a in AUDIT if a["cls"] == "finding"]
    kn = [a for a in AUDIT if a["cls"] == "known"]
    lines = [f"# violations {len(viol)} | findings {len(new)} | known {len(kn)}"]
    for a in viol + new + kn:
        lines.append(f'{a["id"]}\t{a["cls"]}\t{a["code"]}\t{a["msg"]}\t{a["ev"]}')
    AUDIT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  audit log: {AUDIT_FILE.name} — violations {len(viol)}, "
          f"findings {len(new)}, known {len(kn)}")
    for a in viol[:20]:
        print(f"    VIOLATION {a['id']}: {a['code']} — {a['msg']}")
    if len(viol) > 20:
        print(f"    ... {len(viol) - 20} more violations in the log")
    if viol and "--audit" in sys.argv:
        sys.exit(1)


def render_tag(t, stats, span="", elsewhere="", evidence="", keyed=False, quote=("", "")):
    detail = detail_of(t)
    dead = dead_key(t)
    # A key of an enum-keyed map is traced through the map, so it is not a values-only card.
    badge = '<span class="pill idx">values only</span>' if values_badge(t, keyed) else ""
    out = [f'<details class="tag"><summary><span class="nm">{escape(t["name"])}</span>'
           f'<span class="ty">{escape(t["ty"])}</span>{badge}'
           f' <span class="l1">{escape(t["l1"])}</span></summary>']
    if t["l2"]:
        out.append(f'<div class="tx">{escape(t["l2"])}</div>')
    if t.get("range"):
        out.append(f'<p class="range"><b>Allowed range:</b> {escape(t["range"])}</p>')
    elif span:
        out.append(f'<p class="range"><b>Vanilla span:</b> {escape(span)}.</p>')
    # Even a card with no prose, no values and no level-2 summary gets this block: the absence
    # has to be visible, or the card reads as if nothing were missing.
    label = ("Level 3 &mdash; the detail" if detail
             else "Level 3 &mdash; the key and its map" if keyed
             else "Level 3 &mdash; what the key does" if dead
             else "Level 3 &mdash; the values, and what is missing")
    out.append(f'<details class="lv3"><summary>{label}</summary><div class="in">')
    vals = values_table(t)
    if vals:
        out.append(vals)
    if detail:
        out.append(f'<p>{escape(detail)}</p>')
    elif dead:
        out.append(f'<p>{escape(DEAD_ENTRY)}</p>')
    elif quote[1]:
        out.append(f'<p class="where"><b>The file explains it.</b> <code>{escape(quote[0])}</code> has '
                   f'this comment above the key: &ldquo;{escape(quote[1])}&rdquo;</p>')
    elif elsewhere:
        out.append(f'<p class="note-p"><b>Explained elsewhere:</b> {elsewhere}. There is still no '
                   'traced reader on this card, so the unit and the behaviour at 0 or an extreme '
                   'value are not stated here.</p>')
    elif unexplained(t, keyed, elsewhere, quote):
        out.append('<p class="note-p"><b>Not explained anywhere in this guide yet.</b> The line below '
                   'says whether the code reads the key at all; neither it nor this card gives a unit, '
                   'a bound or a failure symptom. Start from a vanilla file, change one value, then '
                   'try 0 and the extremes and watch what the game does.</p>')
    if evidence:
        out.append(evidence)
    if not t["l2"] and not keyed and not dead:
        out.append('<p class="note-p">This card also has no level-2 summary: nothing beyond the one '
                   'sentence above has been written for this tag.</p>')
    if stats:
        out.append(f'<p class="vanilla">{escape(stats)}</p>')
    out.append('</div></details>')
    out.append("</details>")
    return "".join(out)


def render_family(fam, count, seen, samples, pats, sec=None, comments=None):
    comments = comments or {}
    extra = {k: v for k, v in seen.items() if not is_documented(k, pats)}
    by_lower = {k.lower(): v for k, v in samples.items()}
    tier = fam["tier"]
    o = [f'<details class="fam" id="{fam["id"]}">',
         f'<summary><span class="t">{escape(fam["title"])}</span>'
         f'<span class="pill t{tier}">Tier {tier}</span>'
         f'<span class="pill">{count} file{"s" if count != 1 else ""}</span>'
         f'<div class="l1">{escape(fam["l1"])}</div></summary>',
         '<div class="body">',
         f'<p class="meta"><b>{escape(fam["fmt"])}</b> &middot; {escape(fam["loader"])}</p>',
         f'<p class="lv2">{escape(fam["l2"])}</p>']
    if fam["l3"]:
        o.append('<details class="lv3"><summary>Level 3 &mdash; the detail</summary>'
                 f'<div class="in"><p>{escape(fam["l3"])}</p></div></details>')
    if fam.get("notation"):
        n = fam["notation"]
        o.append(f'<details class="note" open><summary>{escape(n["title"])}</summary>'
                 f'<div class="in">{n["body"]}</div></details>')
    o.append(f'<p class="meta"><b>Override:</b> {escape(fam["override"])}</p>')
    cat_html, cat_recs = catalogue_html(fam)
    if fam.get("catalogue"):
        spec = fam["catalogue"]
        key = spec["key"]
        where = sec["id"] if sec else fam["id"]
        if not cat_recs:
            audit_add(where, fam, dict(name=key), "violation", "catalogue-empty",
                      f"a catalogue of {key} values lists none",
                      f'paths={",".join(fam["paths"])}')
        else:
            thin = [r[key] for r in cat_recs
                    if not any(r.get(f) for f, _ in spec.get("fields", []))]
            if thin:
                audit_add(where, fam, dict(name=key), "violation", "catalogue-unexplained",
                          f"{len(thin)} of {len(cat_recs)} {key} values carry no fact",
                          f'ids={",".join(thin[:6])}')
    if cat_html:
        o.append(cat_html)

    card_names = {}
    for g in fam["groups"]:
        for t in g["tags"]:
            card_names[t["name"]] = card_names.get(t["name"], 0) + 1
    for g in fam["groups"]:
        o.append('<details class="grp"><summary><span class="g">%s</span> '
                 '<span class="pill">%d tags</span><div class="l1">%s</div></summary>'
                 % (escape(g["title"]), len(g["tags"]), escape(g["l1"])))
        o.append(f'<div class="body"><p class="lv2">{escape(g["l2"])}</p>')
        if g["l3"]:
            o.append('<details class="lv3"><summary>Level 3 &mdash; the detail</summary>'
                     f'<div class="in"><p>{escape(g["l3"])}</p></div></details>')
        o.append('<ul class="tags">')
        for t in g["tags"]:
            entries = by_lower.get(t["name"].lower(), [])
            st = "" if fam["id"] in ("gametext", "codex") else (
                t.get("vanilla") or (stat_line(entries, t["name"], fam["fmt"])
                                     if entries else ""))
            span = "" if t.get("range") else span_of(entries, t.get("ty", ""))
            ex, ev, quote = "", "", ("", "")
            keyed = False
            detail = detail_of(t)
            if t.get("key"):
                ev = key_evidence(t)
                keyed = bool(ev)
            if keyed:
                # The map is the reader, so it is shown on every keyed card, prose or not.
                UNTRACED["keyed"] = UNTRACED.get("keyed", 0) + 1
                if not detail:
                    quote = comments.get(t["name"], ("", ""))
            elif not detail:
                    ex = explained_elsewhere(t["name"], fam, g, sec)
                    ev = evidence_for(t, fam)
                    UNTRACED["explained" if ex else "not"] += 1
                    if not ex:
                        NOT_EXPLAINED["field" if field_of(t["name"], fam.get("roots") or ()) else "nofield"] += 1
                    if not t["l2"]:
                        NO_L2[0] += 1
            found = classify(t, fam, entries)
            qual = t["l1"] if card_names[t["name"]] > 1 else ""
            for issue in found:
                audit_add(sec["id"] if sec else fam["id"], fam, t, *issue, qual=qual)
            # The "Not explained anywhere" block and the "values only" pill are the page
            # advertising a gap. Neither may render without the violation row that counts it, or
            # the log undercounts what the page itself says is missing.
            if not any(i[0] == "violation" for i in found):
                if unexplained(t, keyed, ex, quote):
                    raise SystemExit(f'{fam["id"]}/{t["name"]}: renders as unexplained with no '
                                     f'violation logged — classify() must flag this card')
                if values_badge(t, keyed):
                    raise SystemExit(f'{fam["id"]}/{t["name"]}: marked values only with no '
                                     f'violation logged — classify() must flag this card')
            o.append("<li>" + render_tag(t, st, span, ex, ev, keyed, quote) + "</li>")
        o.append("</ul></div></details>")

    if extra:
        listed = len(extra) <= 300
        o.append('<details class="note"><summary>Also present in these files'
                 + (f', not described above ({len(extra)})' if listed
                    else f' ({len(extra)} distinct keys)')
                 + '</summary><div class="in">')
        if listed:
            o.append('<p class="note-p">These tags appear in the content but no entry above names them. '
                     'Most are legacy fields the loader ignores, or a spelling it reads through a second '
                     'name. Confirm against the loader before relying on one.</p><p class="missing">'
                     + escape(", ".join(f"{k} ({v})" for k, v in sorted(extra.items())))
                     + '</p>')
        else:
            o.append('<p class="note-p">This family has one entry per id rather than a fixed tag set, so '
                     'the keys are not listed. They are ids, not fields: the value is the text or rule for '
                     'that id.</p>')
        o.append('</div></details>')
    o.append("</div></details>")
    return "\n".join(o)


def nav(current):
    if current is None:
        home = '<a class="btn" href="index.html">&larr; Kit index</a>'
        prefix = "moddable/"
    else:
        home = '<a class="btn" href="../index.html">&larr; Kit index</a>'
        prefix = ""
    secs = "".join(
        f'<a class="btn{" on" if s["id"] == current else ""}" href="{prefix}{s["id"]}.html">'
        f'{escape(s["short"])}</a>' for s in sections())
    prompt = ("prompts/moddable-content.html" if current is None else "../prompts/moddable-content.html")
    return (f'<nav class="bar"><div class="in">{home}'
            f'<a class="btn" href="{"../moddable-content.html" if current else "moddable-content.html"}">Hub</a>'
            f'{secs}<a class="btn" href="{prompt}">Prompt</a>'
            '<input id="q" placeholder="Filter families and tags&hellip;" aria-label="Filter">'
            '<button class="btn" id="open">Expand all</button>'
            '<button class="btn" id="close">Collapse all</button></div></nav>')


def page(title, body, current):
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)}</title><style>{CSS}</style></head>'
            f'<body>{nav(current)}{body}<script>{JS}</script></body></html>\n')


LEVELS = """<p>Every collapsed line is <b>level 1</b>: one sentence, no identifier, enough to decide whether to
open it. Opening it gives <b>level 2</b>: several sentences on what the thing does, what reads it, and
what you would notice in play. A nested <b>level 3</b> gives the field, formula, path or gotcha a
modder would quote, plus a generated <span class="vanilla">In vanilla</span> line naming each file and
the values it writes. Level 3 is written to a soft cap of five
sentences; where an entry runs longer, it is because the numbers or the failure mode need the room.</p>
<p class="note-p">Nothing here is written for engine contributors, and there is no level 4.</p>"""

RULES = """<table>
<tr><th>rule</th><th>what it means for a mod</th></tr>
<tr><td class="n">folder is the root</td><td><code>Mods/&lt;Name&gt;/</code> is the content root. A
 <code>Content/</code> subfolder inside it throws on load.</td></tr>
<tr><td class="n">file name wins</td><td>XML, hull and design files are matched by file name anywhere
 under the tree. A mod's <code>Battleship.hull</code> replaces vanilla's even from another folder.</td></tr>
<tr><td class="n">UID is the join key</td><td>References use names, not paths: <code>Hull</code>,
 <code>ModuleUID</code>, <code>WeaponType</code>, tech <code>UID</code>, design <code>Name</code>.</td></tr>
<tr><td class="n">relative path</td><td>Images, models and audio replace by the same relative path under
 <code>Content/</code>.</td></tr>
<tr><td class="n">inherit flags</td><td><code>UseVanillaShips/Techs/Weapons/Modules/Buildings/Races</code>
 default true. Turning one off drops vanilla for that family only.</td></tr>
<tr><td class="n">all-or-nothing</td><td>A few directories (solar systems, loading screens, models) drop
 every vanilla file once the mod supplies one there.</td></tr>
<tr><td class="n">version gate</td><td><code>FormatVersion</code> must be 1;
 <code>SupportedBlackBoxVersions</code> is substring-matched against the running version.</td></tr>
<tr><td class="n">silent drops</td><td>Unknown XML elements and unknown hull/design keys load without a
 warning. A typo looks like "the value did nothing".</td></tr>
</table>"""

STATIC = """<p>Most assets degrade: a missing texture logs and draws a red placeholder. Four groups do not.
Do not delete these while trimming a mod:</p>
<ul>
<li><b>Fonts.</b> Loaded by name from UI code. A missing compiled <code>.xnb</code> fails when that font
is first used. Keep each <code>.spritefont</code> and its <code>.xnb</code> together.</li>
<li><b>Compiled shaders.</b> <code>Effects/Simple.mgfxo</code>, <code>MeshLighting.mgfxo</code>,
<code>SkinnedEffect.mgfxo</code>, <code>Distort</code>/<code>BeamFX</code> and their XNB pairs are loaded
by hardcoded name; a <code>.fx</code> alone is not enough.</li>
<li><b>UI element ids.</b> Layouts are hot-reloadable, but code finds buttons and panels by id. Renaming
one removes its behaviour even though the screen still draws.</li>
<li><b><code>Content.mgcb</code>.</b> Build-time only: it compiles fonts, effects, videos and tutorials
into the XNB/MGFXO the runtime loads. A new font or shader needs an entry there.</li>
</ul>
<p class="note-p">Everything else under <code>Textures</code>, <code>Model</code>, <code>Audio</code>,
<code>Flags</code>, <code>Cursors</code>, <code>LoadingScreen</code> and <code>Video</code> is
replaceable by relative path, and a missing file degrades that one screen or object.</p>"""


def main():
    fams = families()
    secs = sections()
    deep = notes()

    # Replace short tag details with the deep notes before rendering or auditing.
    # A note is either the level-3 text or a dict that replaces l1/l2/l3 together.
    for fam in fams:
        for g in fam["groups"]:
            for t in g["tags"]:
                note = deep.get((fam["id"], t["name"]))
                if note is None:
                    continue
                if isinstance(note, dict):
                    for field in ("l1", "l2", "l3", "range", "vanilla"):
                        if field in note:
                            t[field] = note[field]
                else:
                    t["l3"] = note

    by_id = {f["id"]: f for f in fams}
    assigned = [fid for s in secs for fid in s["families"]]
    missing = [fid for fid in by_id if fid not in assigned]
    dupes = [fid for fid in set(assigned) if assigned.count(fid) > 1]
    unknown = [fid for fid in assigned if fid not in by_id]
    if missing or dupes or unknown:
        raise SystemExit(f"section map is wrong: missing={missing} dupes={dupes} unknown={unknown}")

    try:
        commit = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                                         text=True).strip()
    except Exception:
        commit = "unknown"

    total_files = total_tags = 0
    rows = {}
    for f in fams:
        fs = files_of(f)
        seen_counts, samples, comments = harvest(f, fs)
        pats = documented(f)
        total_files += len(fs)
        total_tags += sum(len(g["tags"]) for g in f["groups"])
        rows[f["id"]] = (f, len(fs), seen_counts, samples, pats, comments)

    # Hub
    cards = []
    for s in secs:
        srows = [rows[fid] for fid in s["families"]]
        sf = sum(r[1] for r in srows)
        st = sum(len(g["tags"]) for r in srows for g in r[0]["groups"])
        cards.append(
            f'<a class="card" href="moddable/{s["id"]}.html"><span class="ct">{escape(s["title"])}</span>'
            f'<span class="cb">{escape(s["blurb"])}</span>'
            f'<span class="cf">{len(srows)} families &middot; {sf:,} files &middot; {st} tags</span></a>')
    hub = f"""
<header class="head">
 <h1>Moddable content &mdash; what a mod can replace</h1>
 <p class="lede">Every file family and tag under <code>game/Content</code>, grouped the way a modder works:
 game options, map creation, ships, tech, races and diplomacy, colonies, and UI. Each entry opens from one
 sentence to how it behaves, then to the field, the units, the failure symptom and the values vanilla
 actually uses.</p>
 <div class="facts"><span>families: <b>{len(fams)}</b></span><span>content files: <b>{total_files:,}</b></span>
 <span>tags described: <b>{total_tags}</b></span><span>sections: <b>{len(secs)}</b></span>
 <span>generated from: <b>{escape(commit)}</b></span></div>
</header>
<div class="wrap">
<h2>How to read an entry</h2>
{LEVELS}
<h2>The seven sections</h2>
<div class="cards">{''.join(cards)}</div>
<h2>Replace or inherit</h2>
{RULES}
<h2>Static files the game expects</h2>
{STATIC}
<h2>Two-pass depth</h2>
<p>Level 3 is drafted long first, then cut to about five sentences. The draft carries the number, its unit,
the formula it feeds and a vanilla example; the cut keeps those and drops the rest. The
<span class="vanilla">In vanilla</span> line is not prose at all: the generator reads every matching file
and reports the values each one actually sets, so a claim about "typical" can be checked against the
checkout rather than remembered. A tag each file sets once, such as a race's
<code>StartingScout</code> or a hull's <code>HullName</code>, is quoted from one file in that file's own
syntax, with the number of other files that set their own, rather than 125 identical lines. A field whose number needs arithmetic also carries an
<span class="range">Allowed range</span> line: the bounds the code accepts and what the formula returns
at each one. A style or id is described by its readers, not only its home file: the build list, the
tech gate, the UI that sorts by it and the text or name keys it selects all belong in the entry.</p>
<p class="note-p">A card marked <span class="pill idx">values only</span> has no prose level 3 yet:
it shows the files and the values they set, and says that the unit, bounds and failure symptom are
not documented, rather than presenting a restated value as an explanation. Where the family notes,
the worked example or the section introduction already discuss the tag, the card links there
instead of repeating them; where nothing on the page does, it says so and marks that the card has no
level-2 summary either. A key inside an enum-keyed map such as <code>ShipCostModifiers</code> is not a
field at all: its card names the map, the declared type and the member names the loader accepts, and
quotes the file's own comment where one exists, because a name that resolves to an enum has no field
whose readers could be counted.</p>
<p class="note-p">Coverage is measured per family: each one ends with the tags it contains that no entry
above names. A tag listed there is a warning, not an instruction. <code>GameText.yaml</code> and
<code>Codex*.yaml</code> are id-to-text maps and are intentionally not enumerated key by key.</p>
<p class="foot">Generated by <code>docs/kit/build-moddable.py</code> from <code>game/Content</code> at
<code>{escape(commit)}</code> and the prose in <code>moddable-*.py</code>. Re-run the script after editing
content or prose; do not hand-edit this page.</p>
</div>"""
    OUT.write_text(page("Moddable content &mdash; StarDrive BlackBox", hub, None), encoding="utf-8")

    # Section pages
    SECTION_DIR.mkdir(exist_ok=True)
    sizes = []
    for s in secs:
        srows = [rows[fid] for fid in s["families"]]
        sf = sum(r[1] for r in srows)
        st = sum(len(g["tags"]) for r in srows for g in r[0]["groups"])
        toc = " &middot; ".join(f'<a href="#{r[0]["id"]}">{escape(r[0]["title"])}</a>' for r in srows)
        body = f"""
<header class="head">
 <h1>{escape(s["title"])}</h1>
 <p class="lede">{escape(s["l1"])}</p>
 <div class="facts"><span>families: <b>{len(srows)}</b></span><span>files: <b>{sf:,}</b></span>
 <span>tags: <b>{st}</b></span><span>generated from: <b>{escape(commit)}</b></span></div>
</header>
<div class="wrap">
{s.get("intro", "")}
<p class="lv2">{escape(s["l2"])}</p>
<details class="lv3" open><summary>Level 3 &mdash; how this section works</summary>
<div class="in"><p>{escape(s["l3"])}</p>{s.get("notes", "")}</div></details>
<h2>Families in this section</h2>
<p class="toc">{toc}</p>        {''.join(render_family(r[0], r[1], r[2], r[3], r[4], s, r[5]) for r in srows)}
<p class="foot">Generated by <code>docs/kit/build-moddable.py</code> from <code>game/Content</code> at
<code>{escape(commit)}</code>. <a href="../moddable-content.html">Back to the hub</a>.</p>
</div>"""
        p = SECTION_DIR / f"{s['id']}.html"
        p.write_text(page(f"{s['title']} &mdash; moddable content", body, s["id"]), encoding="utf-8")
        sizes.append((p, p.stat().st_size))

    # Audit
    over = []
    bad_l1 = []
    thin_l2 = 0
    skeletons = []
    numeric_no_range = []
    for f in fams:
        for label, text in (("family", f["l3"]),):
            if text and sentence_count(text) > CAP:
                over.append((f["id"], label, sentence_count(text), text[:70]))
        for g in f["groups"]:
            if g["l3"] and sentence_count(g["l3"]) > CAP:
                over.append((f["id"], g["title"], sentence_count(g["l3"]), g["l3"][:70]))
            for t in g["tags"]:
                detail = detail_of(t)
                if sentence_count(t["l1"]) != 1:
                    bad_l1.append((f["id"], t["name"], sentence_count(t["l1"])))
                if detail and sentence_count(detail) > CAP:
                    over.append((f["id"], t["name"], sentence_count(detail), detail[:70]))
                if not detail:
                    skeletons.append((f["id"], t["name"]))
                if sentence_count(t["l2"] or "") < 2:
                    thin_l2 += 1
                if re.search(r"\b(int|float|double)\b", t.get("ty", "")) and not t.get("range"):
                    numeric_no_range.append((f["id"], t["name"]))

    print(f"wrote {OUT.name} and {len(sizes)} section pages: "
          f"{len(fams)} families, {total_files:,} files, {total_tags} described tags")
    for p, n in sizes:
        print(f"  {p.relative_to(HERE)}  {n/1024:6.1f} KB")
    print(f"  audit: level-3 over {CAP} sentences: {len(over)}; level-1 not one sentence: {len(bad_l1)}")
    print(f"  untraced cards: {UNTRACED['explained'] + UNTRACED['not']} "
          f"(explained in prose above: {UNTRACED['explained']}, not explained anywhere: {UNTRACED['not']} "
          f"= {NOT_EXPLAINED['field']} with a field in the code + {NOT_EXPLAINED['nofield']} with no field); "
          f"of those, cards with no level-2 summary: {NO_L2[0]}; "
          f"enum-map keys traced through their map: {UNTRACED.get('keyed', 0)}")
    print(f"  fields declared but never read outside the declaration: {UNREAD[0]}")
    print(f"  conformance: prose level 3 {total_tags - len(skeletons)}/{total_tags}; "
          f"level 2 under two sentences {thin_l2}/{total_tags}; "
          f"numeric tags with no Allowed range {len(numeric_no_range)}")
    report_audit()
    if "--audit" in sys.argv:
        for fid, label, n, text in sorted(over, key=lambda r: -r[2])[:60]:
            print(f"    {n}  {fid:16s} {label:28s} {text}")
        for fid, name, n in bad_l1[:40]:
            print(f"    L1={n}  {fid:16s} {name}")
        print(f"  index-only cards (no prose level 3): {len(skeletons)}")
        for fid, name in skeletons[:20]:
            print(f"    {fid:16s} {name}")
        print(f"  numeric tags with no Allowed range: {len(numeric_no_range)}")
        for fid, name in numeric_no_range[:20]:
            print(f"    {fid:16s} {name}")
    for fid in sorted(rows):
        f, n, seen_counts, _, pats, _ = rows[fid]
        extra = sorted(k for k in seen_counts if not is_documented(k, pats))
        if extra:
            print(f"  {fid:16s} files={n:5d} seen={len(seen_counts):3d} undescribed={len(extra):3d}"
                  + (f"  {', '.join(extra[:8])}" if len(extra) <= 20 else "  (id map)"))


if __name__ == "__main__":
    main()
