#!/usr/bin/env python3
"""
render_study_worksheet.py
Renders Study Worksheet JSON → class-based HTML using site.css.
No inline styles; all visual rules live in site.css under .nx-worksheet-* classes.

Section types handled:
  intro_callout, worksheet_section (with content blocks below),
  closing_callout
Content block types (inside worksheet_section.content):
  subheading, bullet_list, fill_table, fill_equation,
  key_question, concept_questions, tool_versions, section_intro

Usage:
  python3 render_study_worksheet.py                                  # all 5 worksheets
  python3 render_study_worksheet.py <src.json> <out.html>            # single file

Source filename convention: module_N_worksheet.json
Output filename convention: module-N-study-worksheet.html
"""
import json, sys, os, glob

ASSETS   = "https://jfnewsom.github.io/is3513-assets"
CSS_PATH = "../../site.css"


# ── Page shell ────────────────────────────────────────────────────────────────

def shell(html_title, module_num, module_label, accent, subtitle, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_title}</title>
  <link rel="icon" type="image/png" href="{ASSETS}/favicon.png">
  <link rel="stylesheet" href="{CSS_PATH}">
</head>
<body class="nx-worksheet-body">

<div class="nx-page">

<div class="nx-section">

  <!-- Page header: 'study guide' / N / subtitle -->
  <div class="nx-header" style="--accent: {accent};">
    <div class="nx-header-top">
      <div class="nx-kw">study guide</div>
      <div class="nx-sec">{module_num}</div>
    </div>
    <div class="nx-sub">{subtitle}</div>
  </div>

{body}

</div>

</div>
<script src="{ASSETS}/nav.js"></script>
</body>
</html>"""


# ── Content block renderers (used inside worksheet_section) ────────────────────

def render_subheading(b):
    return f"      <h3>{b['text']}</h3>"


def render_section_intro(b):
    return f'      <p class="nx-worksheet-intro">{b["text"]}</p>'


def render_bullet_list(b):
    items = "".join(f"        <li>{item}</li>\n" for item in b["items"])
    return f"      <ul>\n{items}      </ul>"


def render_fill_table(b):
    headers = b.get("headers", ["Question", "Answer"])
    rows_html = []
    for row in b["rows"]:
        rows_html.append(
            f'          <tr><td>{row}</td><td class="nx-worksheet-answer-cell"></td></tr>'
        )
    return (
        f'      <table class="nx-worksheet-table">\n'
        f'        <thead><tr><th>{headers[0]}</th><th>{headers[1]}</th></tr></thead>\n'
        f'        <tbody>\n' + "\n".join(rows_html) + '\n'
        f'        </tbody>\n'
        f'      </table>'
    )


def render_fill_equation(b):
    """One-line equation with blanks. Schema: { prefix: 'Protection =', blanks: 3, sep: ' + ' }"""
    prefix = b.get("prefix", "")
    n = b.get("blanks", 1)
    sep = b.get("sep", " + ")
    blanks = sep.join('<span class="nx-worksheet-blank">&nbsp;</span>' for _ in range(n))
    return f'      <p>{prefix} {blanks}</p>'


def render_key_question(b):
    return (
        f'      <div class="nx-worksheet-key">'
        f'<strong>{b.get("label", "Key question:")}</strong> {b["text"]}'
        f'</div>'
    )


def render_concept_questions(b):
    """Numbered question rows. Schema: { items: ["q1", "q2", ...], start: 1 }"""
    start = b.get("start", 1)
    rows = []
    for i, q in enumerate(b["items"]):
        rows.append(
            f'      <div class="nx-worksheet-concept-q">'
            f'<strong>{start + i}.</strong> {q}'
            f'</div>'
        )
    return "\n".join(rows)


def render_tool_versions(b):
    items_html = []
    for tool in b["tools"]:
        items_html.append(
            f'        <div class="nx-worksheet-tool-version-item">'
            f'<code>{tool}</code> '
            f'<span class="nx-worksheet-blank" style="min-width:100px;">&nbsp;</span>'
            f'</div>'
        )
    return (
        f'      <div class="nx-worksheet-tool-versions">\n'
        + "\n".join(items_html) + '\n'
        f'      </div>'
    )


def render_paragraph(b):
    """Free-form paragraph (rare; for prose that doesn't fit other types)."""
    return f'      <p>{b["text"]}</p>'


def render_answer_line(b):
    """Unnumbered single-answer prompt like 'Answer: ____'."""
    # Replace ___ tokens with a real blank span
    text = b["prompt"].replace("___", '<span class="nx-worksheet-blank">&nbsp;</span>')
    return f'      <div class="nx-worksheet-concept-q">{text}</div>'


BLOCK_RENDERERS = {
    "subheading":         render_subheading,
    "section_intro":      render_section_intro,
    "bullet_list":        render_bullet_list,
    "fill_table":         render_fill_table,
    "fill_equation":      render_fill_equation,
    "key_question":       render_key_question,
    "concept_questions":  render_concept_questions,
    "tool_versions":      render_tool_versions,
    "paragraph":          render_paragraph,
    "answer_line":        render_answer_line,
}


def render_content_blocks(blocks):
    out = []
    for b in blocks:
        t = b.get("type")
        fn = BLOCK_RENDERERS.get(t)
        if fn:
            out.append(fn(b))
        else:
            out.append(f"      <!-- UNKNOWN BLOCK TYPE: {t} -->")
    return "\n\n".join(out)


# ── Section-level renderers ────────────────────────────────────────────────────

def render_intro_callout(sec, accent):
    """The 'How to Use This Worksheet' block at the top, before numbered sections."""
    return f"""  <div class="nx-worksheet-section">
    <div class="nx-card nx-card--sym" style="--accent: {accent};">
      <div class="nx-callout nx-blue" style="--callout-color:{accent}; --callout-rgb:{sec.get('accentRgb', '65,105,225')};">
        <div class="nx-callout-icon"><span class="material-icons">school</span></div>
        <div class="nx-callout-body">
          <div class="nx-callout-title">{sec.get('title', 'How to Use This Worksheet')}</div>
          <p>{sec['body']}</p>
        </div>
      </div>
    </div>
  </div>"""


def render_worksheet_section(sec, num, accent):
    """A numbered section: its own header + card with content blocks.

    Auto-classifies as 'major' or 'checkpoint' based on section title.
    Major sections (Lab Knowledge / Professional Application / Concept Check) get
    a full-size header. Other sections get the compact checkpoint treatment.
    """
    # Auto-classify by title prefix (handles "Lab Knowledge — Networking" etc.)
    title_lower = sec["title"].lower()
    major_prefixes = ("lab knowledge", "professional application", "concept check")
    is_major = any(title_lower.startswith(p) for p in major_prefixes)

    header_class = "nx-header" if is_major else "nx-header nx-checkpoint"

    content_html = render_content_blocks(sec.get("content", []))
    return f"""  <div class="nx-worksheet-section">
    <div class="{header_class}" style="--accent: {accent};">
      <div class="nx-header-top">
        <div class="nx-kw">{num}</div>
        <div class="nx-sec">{sec['title']}</div>
      </div>
    </div>
    <div class="nx-card nx-worksheet-card" style="--accent: {accent};">

{content_html}

    </div>
  </div>"""


def render_closing_callout(sec, accent):
    """Final closing block — uses nx-page-footer pattern."""
    return f"""    <div class="nx-page-footer" style="--accent: {accent};">{sec['body']}</div>"""


# ── Main render ────────────────────────────────────────────────────────────────

def render(data):
    accent       = data["accentColor"]
    module_num   = data["module"]
    title        = data["title"]
    subtitle     = data["subtitle"]
    html_title   = data.get("htmlTitle", f"Module {module_num} Study Guide – IS3513")

    parts = []

    # Intro callout (How to Use) is rendered immediately after page header
    if data.get("intro"):
        parts.append(render_intro_callout(data["intro"], accent))

    # Numbered worksheet sections — uniform accent per worksheet (no per-section color)
    for i, sec in enumerate(data.get("sections", []), start=1):
        parts.append(render_worksheet_section(sec, i, accent))

    # Closing callout
    if data.get("closing"):
        parts.append(render_closing_callout(data["closing"], accent))

    body = "\n\n".join(parts)
    return shell(html_title, module_num, title, accent, subtitle, body)


# ── File entry points ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) == 3:
        src, dst = sys.argv[1], sys.argv[2]
        with open(src) as f:
            data = json.load(f)
        with open(dst, "w") as f:
            f.write(render(data))
        print(f"Rendered: {dst}")
    else:
        base    = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(base, "pages", "support", "json", "study_worksheets")
        out_dir = os.path.join(base, "pages", "support")
        os.makedirs(out_dir, exist_ok=True)
        for src in sorted(glob.glob(os.path.join(src_dir, "module_*_worksheet.json"))):
            with open(src) as f:
                data = json.load(f)
            n = data["module"]
            dst = os.path.join(out_dir, f"module-{n}-study-worksheet.html")
            with open(dst, "w") as f:
                f.write(render(data))
            print(f"Rendered: module-{n}-study-worksheet.html")


if __name__ == "__main__":
    main()
