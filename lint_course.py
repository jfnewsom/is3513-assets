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
        "why": "retired Spring 2026 screenshot rate. Canonical: −2.5 per silently-absent capture.",
        "patterns": [
            rf"{DASH}\s*5\s*(?:%|\s*points?)?\s*(?:each|per)\b[^.;:\n]{{0,30}}\b(?:screenshot|capture)s?\b",
            rf"\b(?:missing|per|each|unverifiable)\s+(?:screenshot|capture)s?\b[^.;:\n]{{0,30}}{DASH}\s*5{NUM_END}",
            rf"\b(?:screenshot|capture)s?\s+(?:missing|absent)\b[^.;:\n]{{0,40}}{DASH}\s*5{NUM_END}",
            rf"\|\s*screenshot[^|\n]{{0,60}}\|\s*{DASH}\s*5{NUM_END}",
        ],
    },
    {
        "id": "SHOT-QUOTA",
        "severity": "error",
        "why": ("screenshot QUOTA language — there is no screenshot count in this course, for "
                "any module. The rule is coverage: take the captures the labs ask for, where "
                "they ask for them; −2.5 for each callout silently unmet. Publishing a total "
                "(a floor, a minimum, or a per-module count) re-creates the count model that "
                "was retired in July, because readers treat the total as the requirement. "
                "State the rule, never a number."),
        "patterns": [
            r"\b(?:at\s+least|minimum(?:\s+of|\s*:)?|floor(?:\s+of|\s*:)?|need|require[sd]?)"
            r"\s*:?\s*\d{1,3}\s+(?:\w+\s+){0,2}(?:screenshot|capture)s?\b",
            r"\b\d{1,3}\s+(?:\w+\s+){0,2}(?:screenshot|capture)s?\s+"
            r"(?:minimum|floor|required|total|in\s+total)\b",
            r"(?:screenshot|capture)s?\s*[—–-]\s*\d{1,3}\s+(?:minimum|required|total)",
            # noun form, but only when asserted — "there is no screenshot quota" is the
            # correct sentence and must not trip the rule.
            r"\b(?:screenshot|capture)\s+(?:floor|quota)\s+(?:is|of|for|remains|stays)\b",
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
        "severity": "warn",
        "why": ("the −10 placeholder-text deduction was pulled for Fall 2026 (Fall runs the "
                "Summer rubric). Still live in the EP Guide and the five EP lab Clean Up "
                "callouts — purge those, then promote this rule to severity 'error'."),
        "patterns": [
            rf"(?:placeholder|demo\s+content|template\s+text)[^.;:\n]{{0,60}}{DASH}\s*10{NUM_END}",
            rf"{DASH}\s*10{NUM_END}[^.;:\n]{{0,60}}(?:placeholder|demo\s+content)",
        ],
    },
    {
        "id": "LAB-COUNT",
        "severity": "warn",
        "why": ("Lab 1.0 is a graded Foundation Lab as of 2026-08-14 — there are 10, and the "
                "drop is 1 of 10. Promote to 'error' once every page is updated."),
        "patterns": [
            r"\b9\s+Foundation\s+Labs\b",
            r"\b1\s+of\s+9\b",
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
