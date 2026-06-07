#!/usr/bin/env python3
"""
lint_course.py — IS3513 course-content linter.

Run from repo root at the start of every session and before every push.
Goal: zero ERRORs. WARNINGs are advisory.

Checks (per project standards):
  E  Invalid JSON (won't parse)
  E  Canvas referenced as a FILE SOURCE ("download from Canvas", etc.)
  E  Raw numeric point values in student-facing content (NO-POINTS rule)
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

# A bare point value in student-facing prose: "40 points", "worth 12 pts", "(5 pts)".
# We allow %  (e.g. "40%") and deliberately do NOT flag "10 references", "Chapter 2",
# screenshot counts, etc. Only the literal point/pt(s) unit triggers it.
POINTS_RE = re.compile(r"\b\d{1,3}\s*(?:points?|pts?)\b", re.IGNORECASE)

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


def check_no_points(path, data):
    for s in iter_strings(data):
        for m in POINTS_RE.finditer(s):
            # skip if it's clearly a percentage context already handled
            err(path, f'raw point value "{m.group(0).strip()}" — use % weights '
                      f'(…{s[max(0,m.start()-25):m.end()+15].strip()}…)')


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
        check_no_points(rel, data)
        check_canvas_files(rel, data)
        check_textbook_reference(rel, data)
        check_file_links(rel, data)
        check_double_subheading(jp, data)

        # lab-specific checks
        if "/labs/json/" in rel and jp.name.startswith("lab"):
            lab_id = data.get("meta", {}).get("labId", "").replace(".", "_")
            check_lab_rendered(rel, data)
            check_client_present(rel, data, lab_id)

    # Cross-cutting: at least one GH Pages link should exist somewhere in support pages
    # (file distribution policy). Soft check.
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
