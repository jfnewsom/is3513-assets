#!/usr/bin/env python3
"""
render_module_overview.py
Renders Module Overview JSON → class-based HTML using site.css.
No inline styles, no external SVG images.
Header generated via .nx-header CSS classes (same as labs).

Usage:
  python3 render_module_overview.py                                  # all 5 modules
  python3 render_module_overview.py <src.json> <out.html>            # single file

Source filename convention: module_N_overview.json
Output filename convention: Module_N.html
"""
import json, sys, os, glob

CSS_PATH = "../../site.css"   # relative from pages/support/ to repo root

CLIENT_RGB = {
    "#FF9F1C": "255, 159, 28",
    "#00BCD4": "0, 188, 212",
    "#00D26A": "0, 210, 106",
    "#E63946": "230, 57, 70",
    "#7B68EE": "123, 104, 238",
}


def shell(module_num, title, accent, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Module {module_num}: {title} &#8211; IS3513</title>
  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is3513-assets/favicon.png">
  <link rel="stylesheet" href="{CSS_PATH}">
</head>
<body>

<div class="nx-page">

<div class="nx-section">

  <!-- Header — generated from JSON, no external SVG -->
  <div class="nx-header" style="--accent: {accent};">
    <div class="nx-header-top">
      <div class="nx-kw">module</div>
      <div class="nx-sec">{module_num}</div>
    </div>
    <div class="nx-sub">{title}</div>
  </div>

  <!-- Main card -->
  <div class="nx-card nx-card--sym" style="--accent: {accent};">

{body}

  </div>

</div>

</div>
<script src="https://jfnewsom.github.io/is3513-assets/nav.js"></script>
</body>
</html>"""


ASSETS = "https://jfnewsom.github.io/is3513-assets"


def render_client_logo(logo):
    """Optional client logo(s), floated right of overview paragraph.

    Schema:
      "logo": {                                  # single logo
        "src": "branding/brazos-financial-dark.svg",
        "alt": "Brazos Financial Group logo",
        "cssClass": "nx-logo-glow"   # optional
      }
      OR
      "logo": [ {...}, {...} ]                   # multiple logos, stacked vertically
    """
    if not logo:
        return ""

    # Normalize to list
    logos = logo if isinstance(logo, list) else [logo]

    def one(item):
        src = item.get("src", "")
        if src and not src.startswith("http"):
            src = f"{ASSETS}/{src.lstrip('/')}"
        alt = item.get("alt", "")
        cls = "nx-module-logo"
        if item.get("cssClass"):
            cls += f" {item['cssClass']}"
        # width attribute is intentional: SVGs without intrinsic dimensions can
        # otherwise render at the container's full width if CSS fails to load.
        return f'<img class="{cls}" src="{src}" alt="{alt}" width="160" height="160" style="width:160px;height:auto;">'

    if len(logos) == 1:
        return one(logos[0])

    # Multiple logos: wrap in a floated stack container so they share one float column
    inner = "".join(one(l) for l in logos)
    return f'<div class="nx-module-logo-stack">{inner}</div>'


def render_stakeholder_quote(s):
    """One stakeholder concern bubble (reuses .nx-quote-* lab pattern).

    Schema:
      {
        "name": "Ray Jimenez",
        "title": "CTO, Brazos Financial",
        "portrait": "headshots/ray-jimenez.png",
        "concern": "I need ammunition for my budget presentation to the board."
      }
    """
    portrait = s.get("portrait", "")
    if portrait and not portrait.startswith("http"):
        portrait = f"{ASSETS}/{portrait.lstrip('/')}"
    name = s.get("name", "")
    title = s.get("title", "")
    concern = s.get("concern", "")
    return f"""      <div class="nx-quote">
        <div class="nx-quote-main">
          <div class="nx-quote-avatar"><img src="{portrait}" alt="{name} portrait"></div>
          <div class="nx-quote-bubble"><p>&ldquo;{concern}&rdquo;</p></div>
        </div>
        <div class="nx-quote-attribution">
          <div class="nx-quote-name">{name}</div>
          <div class="nx-quote-title">{title}</div>
        </div>
      </div>"""


def load_chapter_metadata(chapter_num, base_dir=None):
    """Load reading metadata for a given chapter number from its JSON file.

    Returns a dict with title, assignment, partial, or None if the chapter
    JSON isn't found. Renderer is forgiving: missing chapters render as
    "Ch.N — (not found)" rather than erroring.
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "pages", "reading", "json", f"CH{chapter_num:02d}_reading.json")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        data = json.load(f)
    return {
        "title":      data.get("title", ""),
        "assignment": data.get("assignment", ""),
        "partial":    data.get("partial", False),
    }


def render_readings_block(chapter_nums, accent):
    """Render the 'Reading Assignments' block between Client Context and Skills.

    Each row links to the chapter's rendered reading page and shows:
      Ch.N — Title · assignment string
    Plus a 'partial' tag where applicable.

    Schema in module overview JSON:
      "readings": [9, 13, 18]
    """
    if not chapter_nums:
        return ""

    rows = []
    for ch in chapter_nums:
        meta = load_chapter_metadata(ch)
        if meta is None:
            # Graceful fallback when chapter JSON is missing
            rows.append(
                f"""      <div class="nx-reading-row">
        <div class="nx-reading-row__chnum">Ch.{ch}</div>
        <div class="nx-reading-row__body">
          <div class="nx-reading-row__title">(reading not found)</div>
        </div>
      </div>"""
            )
            continue

        title = meta["title"]
        assignment = meta["assignment"]
        partial = meta["partial"]
        url = f"../reading/CH{ch:02d}-Reading.html"

        partial_tag = ('<span class="nx-reading-row__tag">partial</span>'
                       if partial else '')

        rows.append(
            f"""      <a class="nx-reading-row" href="{url}">
        <div class="nx-reading-row__chnum">Ch.{ch}</div>
        <div class="nx-reading-row__body">
          <div class="nx-reading-row__title">{title}{partial_tag}</div>
          <div class="nx-reading-row__assignment">{assignment}</div>
        </div>
      </a>"""
        )

    return f"""    <div class="nx-readings-block">
      <div class="nx-section-label" style="--accent: {accent}; color: {accent}; border-bottom-color: {accent};">Reading Assignments</div>
{chr(10).join(rows)}
    </div>"""


def render(data):
    accent       = data["accentColor"]
    client_color = data["clientColor"]
    client_rgb   = CLIENT_RGB.get(client_color, "255, 159, 28")
    n            = data["module"]
    title        = data["title"]

    # Info bar (now "Labs" instead of "Units")
    info_bar = f"""    <div class="nx-info-bar">
      <div class="nx-info-stat">
        <div class="nx-info-stat__label">Labs</div>
        <div class="nx-info-stat__value">{data['units']}</div>
      </div>
      <div class="nx-info-stat">
        <div class="nx-info-stat__label">Chapters</div>
        <div class="nx-info-stat__value">{data['chapters']}</div>
      </div>
      <div class="nx-info-stat" style="--client-color: {client_color};">
        <div class="nx-info-stat__label">Client</div>
        <div class="nx-info-stat__value nx-info-stat__value--client">{data['client']}</div>
      </div>
    </div>"""

    # Overview with optional floated logo
    logo_html = render_client_logo(data.get("logo"))
    overview = f'    <div class="nx-module-overview-block">{logo_html}<p>{data["overview"]}</p></div>'

    # Notice (optional)
    notice_html = ""
    if data.get("notice"):
        notice = data["notice"]
        notice_html = f"""    <div class="nx-client-ctx" style="--client-color: {notice['color']}; --client-rgb: {notice['colorRgb']};">
      <span class="nx-client-ctx__label">{notice['label']}</span>
      <span class="nx-client-ctx__body"> {notice['body']}</span>
    </div>"""

    # Lab breakdown (field name in JSON remains units_breakdown for backward compat;
    # the unitLabel values now say "LAB X.1" etc.)
    week_rows = []
    for week in data["units_breakdown"]:
        badge_color = week["badgeColor"]
        badge_text  = "#0A0E17" if week["type"] == "foundation" else "#ffffff"
        week_rows.append(
            f"""      <div class="nx-week-row" style="--badge-color: {badge_color}; --badge-text: {badge_text};">
        <div class="nx-week-badge">{week['unitLabel']}</div>
        <div class="nx-week-info">
          <div class="nx-week-title">{week['labTitle']}</div>
          <div class="nx-week-desc">{week['labDesc']}</div>
        </div>
        <div class="nx-week-type">{week['badgeLabel']}</div>
      </div>"""
        )

    week_section = f"""    <div class="nx-week-list">
      <div class="nx-section-label">This Module</div>
{chr(10).join(week_rows)}
    </div>"""

    # Client context (prose) + optional stakeholder bubbles below
    ctx = data["clientContext"]
    client_ctx_prose = f"""    <div class="nx-client-ctx" style="--client-color: {client_color}; --client-rgb: {client_rgb};">
      <div class="nx-client-ctx__label">{ctx['label']}</div>
      <div class="nx-client-ctx__body">{ctx['body']}</div>
    </div>"""

    stakeholders = data.get("stakeholders", [])
    if stakeholders:
        bubbles = "\n".join(render_stakeholder_quote(s) for s in stakeholders)
        client_ctx_bubbles = f"""    <div class="nx-stakeholder-quotes">
{bubbles}
    </div>"""
        client_ctx = client_ctx_prose + "\n\n" + client_ctx_bubbles
    else:
        client_ctx = client_ctx_prose

    # Reading Assignments (between Client Context and Skills)
    readings_section = render_readings_block(data.get("readings", []), accent)

    # Skills
    skills_left  = "\n          ".join(f"&bull; {s}<br>" for s in data["skills"]["left"])
    skills_right = "\n          ".join(f"&bull; {s}<br>" for s in data["skills"]["right"])
    skills_section = f"""    <div>
      <div class="nx-section-label nx-section-label--green">Skills You&#8217;ll Build</div>
      <div class="nx-skills">
        <div class="nx-skills-col">
          {skills_left}
        </div>
        <div class="nx-skills-col">
          {skills_right}
        </div>
      </div>
    </div>"""

    # Footer
    footer = f'    <div class="nx-page-footer">{data["footer"]}</div>'

    body = "\n\n".join(filter(None, [info_bar, overview, notice_html, week_section, client_ctx, readings_section, skills_section, footer]))
    return shell(n, title, accent, body)


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
        src_dir = os.path.join(base, "pages", "support", "json", "module_overviews")
        out_dir = os.path.join(base, "pages", "support")
        os.makedirs(out_dir, exist_ok=True)
        for src in sorted(glob.glob(os.path.join(src_dir, "module_*_overview.json"))):
            with open(src) as f:
                data = json.load(f)
            n   = data["module"]
            dst = os.path.join(out_dir, f"Module_{n}.html")
            with open(dst, "w") as f:
                f.write(render(data))
            print(f"Rendered: Module_{n}.html")


if __name__ == "__main__":
    main()
