#!/usr/bin/env python3
"""
render_support_page.py
Renders Support Page JSON → class-based HTML using site.css.
No inline styles, no external SVG images.

Section types handled:
  intro, callout_bar, stat_blocks, two_column, info_box,
  named_section, platform_cards, two_col_specs, button_row,
  rules_list, acknowledgment_box, footer

Usage:
  python3 render_support_page.py                      # all support pages
  python3 render_support_page.py <src.json> <out.html>
"""
import json, sys, os, glob, re

ASSETS   = "https://jfnewsom.github.io/is3513-assets"
CSS_PATH = "../../site.css"


# ── Helpers ────────────────────────────────────────────────────────────────────

def slug(title):
    """Convert page title to output filename."""
    return re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_') + ".html"


def section_label(text, color, extra_class=""):
    cls = f"nx-section-label {extra_class}".strip()
    return f'<div class="{cls}" style="--accent: {color}; color: {color}; border-bottom-color: {color};">{text}</div>'


# ── Section renderers ──────────────────────────────────────────────────────────

def render_intro(sec):
    return f'  <p class="nx-support-intro">{sec["html"]}</p>'


def render_callout_bar(sec):
    color    = sec["color"]
    rgb      = sec.get("colorRgb", "")
    label    = sec["label"]
    html     = sec["html"]
    heading  = sec.get("headingStyle", False)
    label_html = f'<span class="nx-client-ctx__label{"--heading" if heading else ""}">{label}</span>'
    return (
        f'  <div class="nx-client-ctx" style="--client-color: {color}; --client-rgb: {rgb};">\n'
        f'    {label_html}\n'
        f'    <span class="nx-client-ctx__body">{html}</span>\n'
        f'  </div>'
    )


def render_stat_blocks(sec):
    blocks_html = ""
    for b in sec["blocks"]:
        blocks_html += (
            f'      <div class="nx-info-stat">\n'
            f'        <div class="nx-info-stat__label" style="color: {b["labelColor"]};">{b["label"]}</div>\n'
            f'        <div class="nx-info-stat__value nx-info-stat__value--lg">{b["value"]}</div>\n'
            f'      </div>\n'
        )
    return f'  <div class="nx-info-bar nx-info-bar--lg">\n{blocks_html}  </div>'


def render_two_column(sec):
    style = sec.get("style", "simple")
    left  = sec["left"]
    right = sec["right"]

    def col(side, detailed):
        color = side["color"]
        label = side["label"]
        items = side["items"]
        lbl   = section_label(label, color)
        if detailed:
            rows = "".join(
                f'          <div class="nx-two-col__item">'
                f'<span class="nx-two-col__item-title">{i["title"]}</span>'
                f'<span class="nx-two-col__item-desc"> — {i["desc"]}</span>'
                f'</div>\n'
                for i in items
            )
        else:
            rows = "".join(
                f'          <div class="nx-two-col__item">{i}</div>\n'
                for i in items
            )
        return (
            f'      <div class="nx-two-col__col">\n'
            f'        {lbl}\n'
            f'        <div class="nx-two-col__list">\n'
            f'{rows}'
            f'        </div>\n'
            f'      </div>'
        )

    detailed = (style == "detailed")
    return (
        f'  <div class="nx-two-col">\n'
        f'{col(left, detailed)}\n'
        f'{col(right, detailed)}\n'
        f'  </div>'
    )


def render_info_box(sec):
    color = sec["color"]
    label = sec["label"]
    paras = "".join(f'        <p>{p}</p>\n' for p in sec["paragraphs"])
    return (
        f'  <div class="nx-info-box">\n'
        f'    <div class="nx-info-box__label" style="color: {color};">{label}</div>\n'
        f'    <div class="nx-info-box__body">\n'
        f'{paras}'
        f'    </div>\n'
        f'  </div>'
    )


def render_named_section(sec):
    color   = sec["color"]
    label   = sec["label"]
    parts   = []

    lbl = section_label(label, color)
    parts.append(f'    {lbl}')

    for p in sec.get("paragraphs", []):
        parts.append(f'    <p class="nx-exam-body">{p}</p>')

    if sec.get("subheading"):
        parts.append(f'    <p class="nx-named-subheading">{sec["subheading"]}</p>')

    if sec.get("items"):
        items_html = "".join(f'      <li>{i}</li>\n' for i in sec["items"])
        parts.append(f'    <ul class="nx-exam-tips">\n{items_html}    </ul>')

    if sec.get("code_block"):
        parts.append(f'    <div class="nx-cmd">{sec["code_block"]}</div>')

    if sec.get("tip"):
        parts.append(f'    <p class="nx-named-tip">{sec["tip"]}</p>')

    if sec.get("email_card"):
        ec = sec["email_card"]
        parts.append(
            f'    <div class="nx-email-card">\n'
            f'      <a href="mailto:{ec["address"]}" class="nx-email-card__addr">{ec["address"]}</a>\n'
            f'      <div class="nx-email-card__note">{ec["note"]}</div>\n'
            f'    </div>'
        )

    if sec.get("button"):
        b = sec["button"]
        text_color = b.get("textColor", "#ffffff")
        _tgt = ' target="_blank"' if b["href"].startswith("http") else ""
        parts.append(
            f'    <a href="{b["href"]}"{_tgt} class="nx-btn" '
            f'style="background: {b["color"]}; color: {text_color};">{b["label"]}</a>'
        )

    if sec.get("html_blocks"):
        for block in sec["html_blocks"]:
            parts.append(f'    {block}')

    if sec.get("expandables"):
        for ex in sec["expandables"]:
            summary = ex["summary"]
            body    = ex.get("bodyHtml", "")
            kind    = ex.get("kind", "neutral")
            cls     = f"nx-expand nx-expand--{kind}" if kind != "neutral" else "nx-expand"
            parts.append(
                f'    <details class="{cls}">\n'
                f'      <summary>{summary}</summary>\n'
                f'      <div class="nx-expand__body">\n'
                f'{body}\n'
                f'      </div>\n'
                f'    </details>'
            )

    if sec.get("word_tip"):
        wt = sec["word_tip"]
        title = wt["title"]
        items_html = "".join(
            f'        <p class="nx-word-tip__item">{item}</p>\n'
            for item in wt.get("items", [])
        )
        parts.append(
            f'    <div class="nx-word-tip">\n'
            f'      <div class="nx-word-tip__badge">W</div>\n'
            f'      <div class="nx-word-tip__content">\n'
            f'        <div class="nx-word-tip__title">{title}</div>\n'
            f'{items_html}'
            f'      </div>\n'
            f'    </div>'
        )

    if sec.get("examples"):
        ex = sec["examples"]
        ok    = ex.get("ok", {})
        notok = ex.get("notOk", {})

        def ex_col(side):
            items_html = "".join(f'        <li>{i}</li>\n' for i in side["items"])
            return (
                f'      <div class="nx-two-col__col">\n'
                f'        {section_label(side["label"], side["color"])}\n'
                f'        <ul class="nx-exam-tips">\n'
                f'{items_html}'
                f'        </ul>\n'
                f'      </div>'
            )

        parts.append(
            f'    <div class="nx-two-col">\n'
            f'{ex_col(ok)}\n'
            f'{ex_col(notok)}\n'
            f'    </div>'
        )

    return f'  <div class="nx-named-section">\n' + "\n".join(parts) + '\n  </div>'


def render_platform_cards(sec):
    color = sec["color"]
    label = sec["label"]
    cards_html = ""
    for c in sec["cards"]:
        lines_html = "".join(f'        <div class="nx-platform-card__line">{l}</div>\n' for l in c["lines"])
        cards_html += (
            f'      <div class="nx-platform-card">\n'
            f'        <div class="nx-platform-card__title">{c["title"]}</div>\n'
            f'{lines_html}'
            f'        <div class="nx-platform-card__status" style="color: {c["statusColor"]};">{c["status"]}</div>\n'
            f'      </div>\n'
        )
    return (
        f'  <div class="nx-named-section">\n'
        f'    {section_label(label, color)}\n'
        f'    <div class="nx-platform-cards">\n'
        f'{cards_html}'
        f'    </div>\n'
        f'  </div>'
    )


def render_two_col_specs(sec):
    color = sec["color"]
    label = sec["label"]

    def specs(items):
        return "".join(
            f'          <div class="nx-spec-row">'
            f'<span class="nx-spec-key">{i["key"]}</span>'
            f'<span class="nx-spec-value">{i["value"]}</span>'
            f'</div>\n'
            for i in items
        )

    return (
        f'  <div class="nx-named-section">\n'
        f'    {section_label(label, color)}\n'
        f'    <div class="nx-two-col">\n'
        f'      <div class="nx-two-col__col">\n'
        f'        <div class="nx-spec-list">\n'
        f'{specs(sec["left"])}'
        f'        </div>\n'
        f'      </div>\n'
        f'      <div class="nx-two-col__col">\n'
        f'        <div class="nx-spec-list">\n'
        f'{specs(sec["right"])}'
        f'        </div>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </div>'
    )


def render_button_row(sec):
    label       = sec["label"]
    label_color = sec["labelColor"]
    btns = ""
    for b in sec["buttons"]:
        text_color = b.get("textColor", "#ffffff")
        _tgt = ' target="_blank"' if b["href"].startswith("http") else ""
        btns += (
            f'      <a href="{b["href"]}"{_tgt} class="nx-btn" '
            f'style="background: {b["color"]}; color: {text_color};">{b["label"]}</a>\n'
        )
    return (
        f'  <div class="nx-info-box">\n'
        f'    <div class="nx-info-box__label" style="color: {label_color};">{label}</div>\n'
        f'    <div class="nx-btn-row">\n'
        f'{btns}'
        f'    </div>\n'
        f'  </div>'
    )


def render_rules_list(sec):
    color = sec["color"]
    label = sec["label"]
    rules_html = ""
    for i, rule in enumerate(sec["rules"], 1):
        subitems = ""
        if rule.get("subitems"):
            lis = "".join(f'            <li>{s}</li>\n' for s in rule["subitems"])
            subitems = f'          <ul class="nx-rules-subitems">\n{lis}          </ul>\n'
        warning = ""
        if rule.get("warning"):
            warning = f'          <div class="nx-rules-warning">{rule["warning"]}</div>\n'
        rules_html += (
            f'      <div class="nx-rule">\n'
            f'        <div class="nx-rule__body">'
            f'<strong>{i}. {rule["title"]}</strong> {rule["body"]}'
            f'</div>\n'
            f'{subitems}'
            f'{warning}'
            f'      </div>\n'
        )
    return (
        f'  <div class="nx-named-section">\n'
        f'    {section_label(label, color)}\n'
        f'    <div class="nx-rules-list">\n'
        f'{rules_html}'
        f'    </div>\n'
        f'  </div>'
    )


def render_acknowledgment_box(sec):
    accent  = sec["accentColor"]
    heading = sec["heading"]
    items_html = "".join(f'          &bull; {i}<br>\n' for i in sec.get("items", []))
    warn_html  = "".join(
        f'          <strong class="nx-ack-warning">&bull; {w}</strong><br>\n'
        for w in sec.get("warningItems", [])
    )
    b = sec["button"]
    text_color = b.get("textColor", "#ffffff")
    _tgt = ' target="_blank"' if b["href"].startswith("http") else ""
    return (
        f'  <div class="nx-ack-box" style="--ack-color: {accent};">\n'
        f'    <div class="nx-ack-box__heading">{heading}</div>\n'
        f'    <div class="nx-ack-box__items">\n'
        f'{items_html}'
        f'{warn_html}'
        f'    </div>\n'
        f'    <a href="{b["href"]}"{_tgt} class="nx-btn" '
        f'style="background: {b["color"]}; color: {text_color};">{b["label"]}</a>\n'
        f'  </div>'
    )


def render_footer(sec):
    return f'  <div class="nx-page-footer">{sec["html"]}</div>'


# ── Dispatch ───────────────────────────────────────────────────────────────────

SECTION_RENDERERS = {
    "intro":            render_intro,
    "callout_bar":      render_callout_bar,
    "stat_blocks":      render_stat_blocks,
    "two_column":       render_two_column,
    "info_box":         render_info_box,
    "named_section":    render_named_section,
    "platform_cards":   render_platform_cards,
    "two_col_specs":    render_two_col_specs,
    "button_row":       render_button_row,
    "rules_list":       render_rules_list,
    "acknowledgment_box": render_acknowledgment_box,
    "footer":           render_footer,
}


def render_sections(sections):
    out = []
    for sec in sections:
        t = sec.get("type")
        fn = SECTION_RENDERERS.get(t)
        if fn:
            out.append(fn(sec))
        else:
            out.append(f'  <!-- UNKNOWN SECTION TYPE: {t} -->')
    return "\n\n".join(out)


# ── Shell ──────────────────────────────────────────────────────────────────────

def shell(html_title, accent, keyword, secondary, subtitle, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_title}</title>
  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is3513-assets/favicon.png">
  <link rel="stylesheet" href="{CSS_PATH}">
</head>
<body>

<div class="nx-page">

<div class="nx-section">

  <!-- Header -->
  <div class="nx-header" style="--accent: {accent};">
    <div class="nx-header-top">
      <div class="nx-kw">{keyword}</div>
      <div class="nx-sec">{secondary}</div>
    </div>
    <div class="nx-sub">{subtitle}</div>
  </div>

  <!-- Main card -->
  <div class="nx-card nx-card--sym" style="--accent: {accent};">

{body}

  </div>

</div>

</div>
<script src="{ASSETS}/nav.js"></script>
</body>
</html>"""


def render(data):
    accent    = data["accentColor"]
    keyword   = data.get("headerKeyword",   data["title"].split("–")[0].split("—")[0].strip().lower())
    secondary = data.get("headerSecondary", "")
    subtitle  = data.get("headerSubtitle",  "")
    body      = render_sections(data["sections"])
    return shell(data["htmlTitle"], accent, keyword, secondary, subtitle, body)


# ── Entry point ────────────────────────────────────────────────────────────────

# Canonical output filenames — must match existing repo filenames exactly.
# home.json is excluded: Home.html is hand-coded, outside the renderer pipeline.
SUPPORT_FILENAME_MAP = {
    "citations":              "Citations.html",
    "course_schedule":        "Course_Schedule.html",
    "discord":                "Discord.html",
    "engagement_packet_guide":"Engagement_Packet_Guide.html",
    "genai_policy":           "GenAI_Policy.html",
    "grading_info":           "Grading_Info.html",
    "how_to_get_help":        "How_To_Get_Help.html",
    "kali_vm_setup":          "Kali_VM_Setup.html",
    "meet_the_team":          "Meet_The_Team.html",
    "nexus_security":         "NEXUS_Security.html",
    "our_clients":            "Our_Clients.html",
    "screenshot_requirements":"Screenshot_Requirements.html",
    "start_here":             "StartHere.html",
    "textbook":               "Textbook.html",
}

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
        src_dir = os.path.join(base, "pages", "support", "json", "support_pages")
        out_dir = os.path.join(base, "pages", "support")
        os.makedirs(out_dir, exist_ok=True)
        for src in sorted(glob.glob(os.path.join(src_dir, "*.json"))):
            stem = os.path.splitext(os.path.basename(src))[0]
            if stem not in SUPPORT_FILENAME_MAP:
                print(f"Skipped: {stem}.json (not in SUPPORT_FILENAME_MAP)")
                continue
            with open(src) as f:
                data = json.load(f)
            dst = os.path.join(out_dir, SUPPORT_FILENAME_MAP[stem])
            with open(dst, "w") as f:
                f.write(render(data))
            print(f"Rendered: {os.path.basename(dst)}")


if __name__ == "__main__":
    main()
