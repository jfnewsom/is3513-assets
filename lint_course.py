#!/usr/bin/env python3
"""
lint_course.py — IS3513 course-content linter.

Run from repo root at the start of every session and before every push.
Goal: zero ERRORs. WARNINGs are advisory.

Checks (per project standards):
  E  Invalid JSON (won't parse)
  E  Canvas referenced as a FILE SOURCE ("download from Canvas", etc.)
  E  Lab JSON with no corresponding rendered HTML (stale / never rendered)
  E  Textbook listed as a valid/counting reference (contradicts Citations policy)
  W  File reference without an accompanying GitHub Pages link
  W  Expected client name absent from a client-facing lab
  W  Known structural bug: two "subheading" keys in one named_section object
  W  HTML output older than its source JSON (needs re-render)

Usage:
    python3 lint_course.py            # lint everything
    python3 lint_course.py --quiet    # only print ERRORs + final summary
Exit code is the number of ERRORs (0 = clean), so it can gate a push.
"""

import html as html_mod
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
QUIET = "--quiet" in sys.argv

GITHUB_PAGES = "jfnewsom.github.io/is3513-assets"
EXPECTED_CLIENTS = [
    "Brazos Financial",
    "Gulf Coast Healthcare",
    "LoneStar DevOps",
    "Alamo Industries",
]

errors = []
warnings = []


def err(where, msg):
    errors.append((where, msg))


def warn(where, msg):
    warnings.append((where, msg))


# ── helpers ──────────────────────────────────────────────────────────────────

def iter_strings(obj):
    """Yield every string value anywhere in a nested JSON structure."""
    if isinstance(obj, dict):
        for v in obj.values():
            yield from iter_strings(v)
    elif isinstance(obj, list):
        for i in obj:
            yield from iter_strings(i)
    elif isinstance(obj, str):
        yield obj


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"
    except Exception as e:  # noqa: BLE001
        return None, f"could not read: {e}"


# ── content checks ─────────────────────────────────────────────────────────────

# Canvas as an ASSET source. Only fires when a downloadable course asset
# (file/template/dossier/hash/resource/zip/pcap) is tied to Canvas — NOT for
# legitimate mentions like "syllabus in Canvas navigation" or "submit on Canvas".
CANVAS_ASSET = r"(file|files|download|template|dossier|hash|resource|\.zip|\.txt|\.pcap|\.docx)"
CANVAS_FILE_RE = re.compile(
    rf"\bcanvas\b[^.]{{0,40}}{CANVAS_ASSET}"
    rf"|{CANVAS_ASSET}[^.]{{0,40}}\bcanvas\b",
    re.IGNORECASE,
)

# RETIRED 2026-08-07. The NO-POINTS rule was killed by John's 2026-07-20 ruling:
# raw point values in student-facing material are ALLOWED and expected, because
# students need to see how they performed in each rubric category and why.
# See DECISIONS_LOCKED.md. Do not reinstate this check.

# A string that directs students to retrieve a NEXUS COURSE ASSET (something that
# must come from GitHub Pages). Deliberately excludes external-tool downloads
# (VirtualBox/Wireshark/etc.) and shell-command filenames (patient.txt, rockyou.txt).
COURSE_ASSET_RE = re.compile(
    r"\b(download|grab|get|obtain|retrieve|provided|pre-?formatted|use\s+the)\b"
    r"[^.]{0,50}"
    r"\b(template|dossier|hash\s*file|hashes\s+file|resource\s+pack|"
    r"engagement\s+packet\s+template|starter\s+(?:file|pack)|worksheet\s+file)\b",
    re.IGNORECASE,
)

# A bare external-tool download we should NOT flag (used to suppress false hits).
EXTERNAL_TOOL_RE = re.compile(
    r"\b(virtualbox|wireshark|kali|vmware|parallels|installer|iso|"
    r"software\s+download|wireshark\.org|github\.com|raw\.githubusercontent)\b",
    re.IGNORECASE,
)

# Textbook asserted as a counting/valid reference (the contradiction we just fixed)
TEXTBOOK_COUNTS_RE = re.compile(
    r"textbook[^.]{0,60}\b(counts?\s+toward|all\s+count|is\s+a\s+valid\s+reference)\b"
    r"|\b(and|,)\s+textbook\s+chapters\s+all\s+count"
    r"|textbook\s+chapters\s+cited\s+correctly",
    re.IGNORECASE,
)


# ── RETIRED-VALUE DENYLIST ───────────────────────────────────────────────────
#
# THE ONE PLACE TO ADD A RETIRED VALUE.
#
# When a number, phrase, or URL is superseded, add it here. The linter then
# refuses to let it back into the repo — in JSON *or* in rendered HTML — so a
# stale copy-paste, an old document, or an AI session working from a superseded
# source cannot quietly reintroduce it. This is the mechanism that turns "purge
# it again" into "it cannot come back."
#
# severity: "error" gates the push (exit code). "warn" is advisory — use it for
# values that are still legitimately present somewhere you haven't cleaned yet,
# then promote to "error" once the repo is clear.
#
# Each pattern is matched against tag-stripped, entity-decoded text, so a value
# split across table cells (<td>Reference missing</td><td>−10</td>) still hits.

DASH = r"[-−–]"          # hyphen, minus sign, en dash
NUM_END = r"(?![\d.])"   # don't let -5 match inside -50 or -2.5

DENYLIST = [
    {
        "id": "REF-RATE",
        "severity": "error",
        "why": "retired Spring 2026 reference rate. Canonical: −5 per missing reference.",
        "patterns": [
            rf"{DASH}\s*10\s*(?:%|\s*points?)?\s*(?:each|per)\b[^.;:\n]{{0,30}}\b(?:reference|citation)s?\b",
            rf"\b(?:missing|per|each)\s+(?:reference|citation)s?\b[^.;:\n]{{0,30}}{DASH}\s*10{NUM_END}",
            rf"\b(?:reference|citation)s?\s+(?:missing|absent)\b[^.;:\n]{{0,30}}{DASH}\s*10{NUM_END}",
            rf"\|\s*(?:reference|citation)[^|\n]{{0,40}}\|\s*{DASH}\s*10{NUM_END}",
        ],
    },
    {
        "id": "SHOT-RATE",
        "severity": "error",
        "why": "retired Spring 2026 screenshot rate. Canonical: −2.5 per qualifying screenshot short of 20.",
        "patterns": [
            rf"{DASH}\s*5\s*(?:%|\s*points?)?\s*(?:each|per)\b[^.;:\n]{{0,30}}\b(?:screenshot|capture)s?\b",
            rf"\b(?:missing|per|each|unverifiable)\s+(?:screenshot|capture)s?\b[^.;:\n]{{0,30}}{DASH}\s*5{NUM_END}",
            rf"\b(?:screenshot|capture)s?\s+(?:missing|absent)\b[^.;:\n]{{0,40}}{DASH}\s*5{NUM_END}",
            rf"\|\s*screenshot[^|\n]{{0,60}}\|\s*{DASH}\s*5{NUM_END}",
        ],
    },
    {
        "id": "SHOT-FLOOR",
        "severity": "error",
        "why": ("screenshot count other than the 20 floor, or the retired coverage wording. "
                "Ruled 2026-11-25 (what Fall 2026 was graded against): every module's floor is "
                "20. Twenty qualifying screenshots earns full credit, -2.5 for each one short of "
                "20, and extras earn nothing unless they evidence a stretch goal. Any other "
                "published count (25+, 30, per-lab splits, per-module tables) contradicts the "
                "floor, and so does the coverage model it replaced ('individually required', "
                "'silently absent', 'coverage, not count')."),
        "patterns": [
            # Any number other than 20 in front of screenshots/captures, with or without a
            # "+" ("25+ screenshots" slipped past the old rule in Labs 2.3 and 4.3 and the EP
            # Guide). Lookbehind skips lab numbers ("Lab 5.1 screenshots") and callout
            # numbers ("#11 screenshots").
            r"(?<![\d.#])\b(?!20\b)\d{1,3}\+?\s+(?:[\w-]+\s+){0,2}(?:screenshot|capture)s\b",
            r"\(\s*(?!20\b)\d{1,3}\s+(?:screenshot|capture)s?\s*\)",
            r"(?:screenshot|capture)[^.]{0,80}\(\s*(?!20\b)\d{1,3}\s+total\s*\)",
            # Per-module tables: "Required captures by module: 20 (M1), 25 (M2), ..."
            r"\b(?:screenshot|capture)s?\s+by\s+module\b",
            r"\b\d{1,3}\s*\(M\d\)",
            r"\bfloor\s+for\s+module\s+\d",
            # The retired coverage model.
            r"\bindividually\s+required\b",
            r"\bsilently[\s-]+absent\b",
            r"\bcoverage,?\s+not\s+(?:a\s+)?(?:raw\s+)?count\b",
            r"\bevery\s+numbered\s+(?:screenshot\s+)?capture",
        ],
    },
    {
        "id": "QUIZ-POINTS",
        "severity": "error",
        "why": ("retired quiz scoring. Every quiz in this course totals exactly 100: "
                "Foundation Labs 20 questions x 5, Module Exams 25 questions x 4. "
                "99.9 / 6.66 are the old 15-question Foundation Lab values and drew "
                "student complaints; they must never reappear."),
        "patterns": [
            r"\b99\.9\b",
            r"\b6\.66\b",
        ],
    },
    {
        "id": "BRITISH-SPELLING",
        "severity": "error",
        "why": ("British spelling in a US course. Use the American form. Found and purged "
                "2026-08-15 (offence/defence, recognise, maximise, memorise, grey). "
                "Add new pairs to this pattern list as they turn up."),
        "patterns": [
            r"\b(?:colour|behaviour|favour|honour|labour|neighbour|humour|armour|flavour|vapour|vigour|endeavour)s?\b",
            r"\b(?:organis|recognis|realis|apologis|authoris|categoris|characteris|criticis|customis|emphasis"
            r"|familiaris|finalis|generalis|initialis|minimis|maximis|normalis|optimis|prioritis|randomis"
            r"|specialis|standardis|summaris|synthesis|utilis|visualis|digitis|memoris|sanitis|virtualis)"
            r"(?:e|es|ed|ing|ation|ations)\b",
            r"\banalys(?:e|es|ed|ing|er)\b",
            r"\b(?:centre|metre|litre|theatre|fibre|calibre|spectre|lustre)s?\b",
            r"\b(?:defence|offence|licence|pretence|practise)s?\b",
            r"\b(?:travelled|travelling|labelled|labelling|modelling|signalling|fuelled|marvellous|counsellor)\b",
            r"\b(?:whilst|amongst|learnt|spelt|dreamt|aluminium|sulphur|storey|kerb|plough|draught|cheque|aeroplane|programme|manoeuvre|ageing)\b",
            r"\bgrey\b",
        ],
    },
    {
        "id": "TERM-LENGTH",
        "severity": "error",
        "why": 'the NEXUS engagement is SEMESTER-long, not year-long.',
        "patterns": [r"year[-\s]?long"],
    },
    {
        "id": "TEXTBOOK-YEAR",
        "severity": "error",
        "why": "course textbook is Conklin & White (2022), verified against the copyright page.",
        "patterns": [r"White,?\s*G\.?[^)\n]{0,20}\(\s*2021"],
    },
    {
        "id": "STALE-SYLLABUS-URL",
        "severity": "error",
        "why": "links the Summer 2026 Simple Syllabus. Point at the Fall doc.",
        "patterns": [r"Summer-2026-IS-3513"],
    },
    # ── advisory: real but not yet cleaned up ────────────────────────────────
    {
        "id": "PLACEHOLDER-10",
        "severity": "error",
        "why": ("the −10 placeholder-text deduction was pulled for Fall 2026 (Fall runs the "
                "Summer rubric). Purged from the EP Guide 2026-08-14. Do not reintroduce it "
                "in student-facing copy."),
        "patterns": [
            rf"(?:placeholder|demo\s+content|template\s+text)[^.;:\n]{{0,60}}{DASH}\s*10{NUM_END}",
            rf"{DASH}\s*10{NUM_END}[^.;:\n]{{0,60}}(?:placeholder|demo\s+content)",
        ],
    },
    {
        "id": "LAB-COUNT",
        "severity": "error",
        "why": ("Lab 1.0 is a graded Foundation Lab as of 2026-08-14. There are 10 Foundation "
                "Labs and the drop is 1 of 10."),
        "patterns": [
            r"\b9\s+(?:Foundation|Training)\s+Labs\b",
            r"\b1\s+of\s+9\b",
        ],
    },
    {
        "id": "EP-NAME",
        "severity": "error",
        "why": ("Renamed 2026-11-27. The culminating assignment is the Module N Engagement Packet "
                "(short form EP N), never Lab 1.3 / 2.3 / 3.3 / 4.3 / 5.2 or Lab X.3. Labs X.1 and X.2 "
                "are Training Labs (full name Module N Training Lab M), not Foundation Labs. File URLs "
                "and labIds (Lab1_3_..., 1_3) stay as they are."),
        "patterns": [
            r"\bLabs?\s+[1-4]\.3\b",
            r"\bLab\s+5\.2\b",
            r"\bLabs?\s+X\.3\b",
            r"(?-i:\b[Ff]oundation\s+[Ll]abs?\b)(?!\s*\d)",
        ],
    },
]

for _rule in DENYLIST:
    _rule["compiled"] = [re.compile(p, re.IGNORECASE) for p in _rule["patterns"]]


def _flatten_markup(text):
    """Entity-decode and strip tags so a value split across HTML elements or
    table cells still matches as one string."""
    text = html_mod.unescape(text)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"[ \t ]+", " ", text)


def check_retired_values(path, text):
    """Run the denylist over one blob of already-flattened text."""
    for rule in DENYLIST:
        for rx in rule["compiled"]:
            m = rx.search(text)
            if not m:
                continue
            start = max(0, m.start() - 30)
            snippet = text[start:m.end() + 30].strip().replace("\n", " ")
            msg = f'[{rule["id"]}] {rule["why"]} (…{snippet}…)'
            (err if rule["severity"] == "error" else warn)(path, msg)
            break  # one hit per rule per file is enough to act on


def check_canvas_files(path, data):
    # Submission / quiz language is legitimate Canvas use — never flag it.
    SUBMIT_OK = re.compile(
        r"\b(submit|upload|turn\s+in|quiz|exam|assignment|gradebook|grad)",
        re.IGNORECASE,
    )
    for s in iter_strings(data):
        if CANVAS_FILE_RE.search(s) and not SUBMIT_OK.search(s):
            err(path, f'Canvas referenced as a file source — replace with a '
                      f'{GITHUB_PAGES} link (…{s[:90].strip()}…)')


def check_textbook_reference(path, data):
    for s in iter_strings(data):
        low = s.lower()
        if "does not count" in low or "does not \u2014" in low:
            continue  # already the corrected, negated form
        if TEXTBOOK_COUNTS_RE.search(s):
            err(path, f'textbook described as a valid/counting reference — '
                      f'contradicts Citations policy (…{s[:90].strip()}…)')


def check_file_links(path, data):
    """Flag only if a file references a NEXUS course asset but the whole file
    contains no GitHub Pages link at all. Text ('Use the template') and the URL
    routinely live in separate JSON fields, so the check is file-level, not
    per-string. External-tool downloads and shell filenames never trigger it."""
    asset_strings = [
        s for s in iter_strings(data)
        if COURSE_ASSET_RE.search(s) and not EXTERNAL_TOOL_RE.search(s)
    ]
    if not asset_strings:
        return
    if GITHUB_PAGES in json.dumps(data):
        return  # link exists somewhere in the file — good enough
    sample = asset_strings[0][:90].strip()
    warn(path, f'course asset referenced but no {GITHUB_PAGES} link anywhere in '
               f'file (…{sample}…)')


def check_double_subheading(path, data):
    """Known bug: two 'subheading' keys collapse to one in render_named_section.
    JSON dedupes duplicate keys on load, so detect it in the raw text instead."""
    try:
        raw = Path(path).read_text()
    except Exception:  # noqa: BLE001
        return
    # crude but effective: a named_section object with 2+ "subheading": occurrences
    for block in re.findall(r"\{[^{}]*\"subheading\"[^{}]*\}", raw):
        if block.count('"subheading"') >= 2:
            warn(path, 'two "subheading" keys in one object — only the last '
                       'renders (engagement_packet_guide known bug)')
            break


def check_client_present(path, data, lab_id):
    """Engagement labs declare their client in intro.clientContext.client.
    Verify (a) that field exists, (b) it names at least one known client, and
    (c) that client name actually appears in the body content."""
    intro = data.get("intro", {})
    ctx = intro.get("clientContext") if isinstance(intro, dict) else None
    if not ctx or not ctx.get("client"):
        return  # not a client-facing lab
    declared = ctx["client"]
    # may name multiple clients ("Brazos Financial Group & Alamo Industries")
    matched = [c for c in EXPECTED_CLIENTS if c in declared]
    if not matched:
        warn(path, f'clientContext.client "{declared}" matches no known NEXUS client')
        return
    blob = json.dumps(data)
    # Foundation (training) labs set client context for narrative framing but the
    # work is internal — low client frequency is expected. Only enforce body
    # presence on engagement labs.
    lab_type = data.get("meta", {}).get("labType", "")
    if lab_type == "engagement":
        for c in matched:
            if blob.count(c) < 2:
                warn(path, f'client "{c}" declared in clientContext but barely '
                           f'appears in body of this engagement lab')


# ── render-freshness checks ──────────────────────────────────────────────────

def derive_lab_html(json_path, data):
    meta = data.get("meta", {})
    lab_id = meta.get("labId", "").replace(".", "_")
    title = meta.get("title", Path(json_path).stem)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    name = f"Lab{lab_id}_{safe}.html"
    return Path(json_path).parent.parent / name


def check_lab_rendered(json_path, data):
    html = derive_lab_html(json_path, data)
    if not html.exists():
        err(json_path, f"no rendered HTML found (expected {html.name}) — run render_lab.py")
        return
    if html.stat().st_mtime < Path(json_path).stat().st_mtime:
        warn(json_path, f"{html.name} is older than its JSON — re-render before push")


# ── main ─────────────────────────────────────────────────────────────────────

def lint():
    json_files = sorted((REPO / "pages").rglob("*.json"))
    if not json_files:
        err("repo", "no JSON files found under pages/ — wrong working directory?")
        return

    for jp in json_files:
        rel = str(jp.relative_to(REPO))
        data, parse_err = load_json(jp)
        if parse_err:
            err(rel, parse_err)
            continue

        # universal content checks
        check_canvas_files(rel, data)
        check_textbook_reference(rel, data)
        check_file_links(rel, data)
        check_double_subheading(jp, data)
        check_retired_values(rel, _flatten_markup(" \n".join(iter_strings(data))))

        # lab-specific checks
        if "/labs/json/" in rel and jp.name.startswith("lab"):
            lab_id = data.get("meta", {}).get("labId", "").replace(".", "_")
            check_lab_rendered(rel, data)
            check_client_present(rel, data, lab_id)

    # Rendered HTML gets the denylist too. JSON is the source, but a stale render
    # is what students actually read — and the retired rates have historically
    # survived in exactly that gap.
    for hp in sorted((REPO / "pages").rglob("*.html")):
        rel = str(hp.relative_to(REPO))
        try:
            raw = hp.read_text(errors="replace")
        except Exception:  # noqa: BLE001
            continue
        check_retired_values(rel, _flatten_markup(raw))
        check_swallowed_placeholders(rel, raw)

    return


# Added 2026-11-21. A placeholder written as <your abc123> or <tool-name> in a JSON
# string is emitted raw by the renderers, and the browser parses it as an unknown
# tag and shows nothing. Students read "Name your VM kali-, where your abc123 is...".
# Found in 18 places across 8 labs and the EP Guide, all on the naming rule. Write
# placeholders as &lt;your abc123&gt; in the JSON.
_HTML_TAGS = set("""a abbr address area article aside audio b base bdi bdo blockquote
body br button canvas caption cite code col colgroup data datalist dd del details dfn
dialog div dl dt em embed fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head
header hgroup hr html i iframe img input ins kbd label legend li link main map mark menu
meta meter nav noscript object ol optgroup option output p param picture pre progress q
rp rt ruby s samp script section select slot small source span strong style sub summary
sup table tbody td template textarea tfoot th thead time title tr track u ul var video
wbr svg path g circle rect line polyline polygon text tspan defs use symbol
lineargradient radialgradient stop clippath mask pattern filter ellipse foreignobject
marker""".split())


def check_swallowed_placeholders(path, raw):
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    for m in re.finditer(r"<\s*/?\s*([A-Za-z][\w\-]*)[^>]*>", body):
        if m.group(1).lower() not in _HTML_TAGS:
            snippet = body[max(0, m.start() - 30):m.end() + 10].replace("\n", " ")
            err(path, f"[PLACEHOLDER-TAG] text in angle brackets is not an HTML tag, so the "
                      f"browser hides it. Write it as &lt;...&gt; in the source JSON. (…{snippet}…)")
            return


def report():
    if not QUIET:
        for where, msg in warnings:
            print(f"  WARNING  {where}: {msg}")
        if warnings:
            print()
    for where, msg in errors:
        print(f"  ERROR    {where}: {msg}")
    print()
    print(f"Lint complete: {len(errors)} error(s), {len(warnings)} warning(s).")
    if errors:
        print("FAIL — resolve all ERRORs before pushing.")
    else:
        print("PASS — zero errors.")


if __name__ == "__main__":
    lint()
    report()
    sys.exit(len(errors))
