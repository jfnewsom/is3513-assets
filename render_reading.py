#!/usr/bin/env python3
"""
render_reading.py
Renders Reading Assignment JSON → class-based HTML using site.css.

Usage:
  python3 render_reading.py                          # render all in pages/reading/json/
  python3 render_reading.py pages/reading/json/CH01_reading.json
"""

import json, sys, os, glob, re

ASSETS   = "https://jfnewsom.github.io/is3513-assets"
CSS_PATH = "../../site.css"


def h(text):
    """Pass HTML entities and markup through unchanged."""
    return text or ""


def render(data):
    ch       = data["chapter"]
    title    = data["title"]
    module   = data["module"]
    assign   = data["assignment"]
    partial  = data.get("partial", False)
    partial_note = data.get("partialNote", "")
    read_sec = data.get("readSections", [])
    skip_sec = data.get("skipSections", [])
    focus    = data.get("focusAreas", "")
    secplus  = data.get("secplus", "")

    # ── Partial warning callout ───────────────────────────────────
    partial_html = ""
    if partial:
        note = h(partial_note) or "This is a <strong>partial chapter</strong>. Read only the sections listed below."
        partial_html = f"""
    <div class="nx-callout nx-orange">
      <div class="nx-callout-icon"><span class="material-icons" aria-hidden="true">warning</span></div>
      <div class="nx-callout-body">
        <div class="nx-callout-title">Partial Reading Assignment</div>
        <p>{note}</p>
      </div>
    </div>
"""

    # ── Read sections list ────────────────────────────────────────
    read_label = "Read These Sections" if skip_sec else "Key Sections"
    read_lis   = "".join(f"        <li>{h(s)}</li>\n" for s in read_sec)
    read_html  = f"""        <h3 class="nx-reading-h3">{read_label}</h3>
        <ul class="nx-reading-list">
{read_lis}        </ul>
""" if read_sec else ""

    # ── Skip sections list ────────────────────────────────────────
    skip_lis  = "".join(f"        <li>{h(s)}</li>\n" for s in skip_sec)
    skip_html = f"""        <h3 class="nx-reading-h3 nx-reading-h3--skip">Skip These Sections</h3>
        <ul class="nx-reading-skip">
{skip_lis}        </ul>
""" if skip_sec else ""

    # ── Focus areas ───────────────────────────────────────────────
    focus_html = f"""        <h3 class="nx-reading-h3">Focus Areas</h3>
        <p class="nx-reading-text">{h(focus)}</p>
""" if focus else ""

    # ── Full page ─────────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter {ch} Reading &#8212; {h(title)}</title>
  <link rel="stylesheet" href="{CSS_PATH}">
  <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
</head>
<body>

<div class="nx-page">

  <div class="nx-section nx-section--flush">
    <div class="nx-header" style="--accent: #4169E1;">
      <div class="nx-header-top">
        <div class="nx-kw">chapter</div>
        <div class="nx-sec">{ch}</div>
      </div>
      <div class="nx-sub">{h(title)}</div>
    </div>
  </div>

  <div class="nx-card" style="--accent: #4169E1;">

    <p class="nx-module-label">{h(module)}</p>
{partial_html}
    <div class="nx-reading-layout">

      <div class="nx-reading-content">
        <h3 class="nx-reading-h3">Assignment</h3>
        <p class="nx-reading-text">Read <strong style="color: #ffffff;">{h(assign)}</strong></p>
{read_html}{skip_html}{focus_html}
      </div>

      <div class="nx-reading-cover">
        <img src="{ASSETS}/third-party/cover.jpg" alt="Principles of Computer Security, 6th Edition">
      </div>

    </div>

    <div class="nx-callout nx-purple">
      <div class="nx-callout-icon"><span class="material-icons" aria-hidden="true">menu_book</span></div>
      <div class="nx-callout-body">
        <div class="nx-callout-title">Security+ Exam Alignment</div>
        <p>{h(secplus)}</p>
      </div>
    </div>

  </div>

</div>

</body>
</html>"""


def out_path_for(json_path):
    """Derive output HTML path from JSON path."""
    base   = os.path.splitext(os.path.basename(json_path))[0]  # e.g. CH01_reading
    ch_num = re.search(r'CH(\d+)', base, re.I)
    fname  = f"CH{ch_num.group(1)}-Reading.html" if ch_num else base + ".html"
    return os.path.join(os.path.dirname(json_path), "..", fname)


def render_file(json_path):
    with open(json_path) as f:
        data = json.load(f)
    html     = render(data)
    out      = os.path.normpath(out_path_for(json_path))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(html)
    print(f"Written: {out}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        render_file(sys.argv[1])
    else:
        base    = os.path.dirname(os.path.abspath(__file__))
        pattern = os.path.join(base, "pages", "reading", "json", "*.json")
        files   = sorted(glob.glob(pattern))
        if not files:
            print(f"No JSON files found at {pattern}")
            sys.exit(1)
        for f in files:
            render_file(f)
