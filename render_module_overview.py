#!/usr/bin/env python3
"""
render_module_overview.py
Renders Module Overview JSON → class-based HTML using site.css.
No inline styles, no external SVG images.
Header generated via .nx-header CSS classes (same as labs).

Usage:
  python3 render_module_overview.py                          # all 5 modules
  python3 render_module_overview.py <src.json> <out.html>   # single file
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
<script src="https://jfnewsom.github.io/is3513-assets/nav.js"></script>

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
</body>
</html>"""


def render(data):
    accent       = data["accentColor"]
    client_color = data["clientColor"]
    client_rgb   = CLIENT_RGB.get(client_color, "255, 159, 28")
    n            = data["module"]
    title        = data["title"]

    # Info bar
    info_bar = f"""    <div class="nx-info-bar">
      <div class="nx-info-stat">
        <div class="nx-info-stat__label">Weeks</div>
        <div class="nx-info-stat__value">{data['weeks']}</div>
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

    # Overview
    overview = f"    <p>{data['overview']}</p>"

    # Notice (optional)
    notice_html = ""
    if data.get("notice"):
        notice = data["notice"]
        notice_html = f"""    <div class="nx-client-ctx" style="--client-color: {notice['color']}; --client-rgb: {notice['colorRgb']};">
      <span class="nx-client-ctx__label">{notice['label']}</span>
      <span class="nx-client-ctx__body"> {notice['body']}</span>
    </div>"""

    # Week breakdown
    week_rows = []
    for week in data["weeks_breakdown"]:
        badge_color = week["badgeColor"]
        badge_text  = "#0A0E17" if week["type"] == "foundation" else "#ffffff"
        week_rows.append(
            f"""      <div class="nx-week-row" style="--badge-color: {badge_color}; --badge-text: {badge_text};">
        <div class="nx-week-badge">{week['weekLabel']}</div>
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

    # Client context
    ctx = data["clientContext"]
    client_ctx = f"""    <div class="nx-client-ctx" style="--client-color: {client_color}; --client-rgb: {client_rgb};">
      <div class="nx-client-ctx__label">{ctx['label']}</div>
      <div class="nx-client-ctx__body">{ctx['body']}</div>
    </div>"""

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

    body = "\n\n".join(filter(None, [info_bar, overview, notice_html, week_section, client_ctx, skills_section, footer]))
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
        src_dir = os.path.join(base, "json", "module_overviews")
        out_dir = os.path.join(base, "output", "modules")
        os.makedirs(out_dir, exist_ok=True)
        for src in sorted(glob.glob(os.path.join(src_dir, "module_*.json"))):
            with open(src) as f:
                data = json.load(f)
            n   = data["module"]
            dst = os.path.join(out_dir, f"Module_{n}.html")
            with open(dst, "w") as f:
                f.write(render(data))
            print(f"Rendered: Module_{n}.html")


if __name__ == "__main__":
    main()
