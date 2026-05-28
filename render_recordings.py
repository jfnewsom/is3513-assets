#!/usr/bin/env python3
"""
render_recordings.py — Shared rendering for the Recordings section that
appears on Home.html (aggregated, all 5 modules) and on each Module_N.html
(just that module's rows).

Single source of truth: pages/support/json/support_pages/recordings.json

Imported by:
  - render_home.py            — calls render_home_recordings_block(...)
  - render_module_overview.py — calls render_module_recordings_block(...)

This module is NOT meant to be run directly. To re-render pages after
editing recordings.json, run render_home.py and render_module_overview.py
(or render_all.sh, which now wires both in).

Visual model:
  - Each module has its own `themeColor` (Module 1=gold, Module 2=cyan, 3=green,
    4=red, 5=purple). The module header on the Home page uses that color for
    a left-bar accent and bold uppercase title — making the boundary between
    modules unmistakable when scanning.
  - Foundation labs (X.1, X.2, and 5.1) render with a neutral left-border and
    show both Chapter Notes + Lab Walkthrough buttons.
  - Engagement labs (X.3, 5.2) render with a colored left-border (the module's
    themeColor) and show ONLY the Lab Walkthrough button — no Chapter Notes
    slot at all. The engagement row also gets a small "Engagement" tag so its
    different role is visible at a glance.
"""
import json
import os


def _load_recordings(base_dir=None):
    """Load recordings.json from its canonical location."""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(
        base_dir, "pages", "support", "json", "support_pages", "recordings.json"
    )
    with open(path) as f:
        return json.load(f)


def _hex_to_rgb_triple(hex_color):
    """'#FEC52E' -> '254, 197, 46' — for use in rgba() CSS values."""
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def _render_button(url, label):
    """Render one Chapter Notes / Lab Walkthrough button.

    If url is set, render as a clickable <a class="nx-rec-btn nx-rec-btn--active">.
    If url is null/missing, render as a disabled <span class="nx-rec-btn nx-rec-btn--placeholder">.
    """
    if url:
        return (
            f'<a class="nx-rec-btn nx-rec-btn--active" href="{url}" '
            f'target="_blank" rel="noopener">'
            f'<span class="material-icons nx-rec-btn__icon" aria-hidden="true">play_circle</span>'
            f'{label}</a>'
        )
    return (
        f'<span class="nx-rec-btn nx-rec-btn--placeholder" '
        f'title="Recording will be posted as it&rsquo;s produced.">'
        f'<span class="material-icons nx-rec-btn__icon" aria-hidden="true">hourglass_empty</span>'
        f'{label}</span>'
    )


def _render_row(row, theme_color="#FF9F1C"):
    """Render one recording row.

    Foundation rows:
      [Lab label]  [Chapter Notes btn]  [Lab Walkthrough btn]
      Neutral left border.

    Engagement rows (X.3, Lab 5.2):
      [Lab label] [Engagement tag]  [Lab Walkthrough btn]
      Colored left border using the module's themeColor.
      No Chapter Notes slot at all — the engagement lab is compilation
      and client-facing work, not new chapter content.
    """
    is_engagement = (row.get("type") == "engagement")
    rgb = _hex_to_rgb_triple(theme_color)

    sub_html = ""
    if row.get("labTitle"):
        sub_html = f'<span class="nx-rec-lab-label__sub">{row["labTitle"]}</span>'

    walkthrough_btn = _render_button(row.get("lab_walkthrough_url"), "Lab Walkthrough")

    if is_engagement:
        tag_html = (
            f'<span class="nx-rec-tag" '
            f'style="--tag-color: {theme_color}; --tag-rgb: {rgb};">Engagement</span>'
        )
        return (
            f'      <div class="nx-rec-row nx-rec-row--engagement" '
            f'style="--row-color: {theme_color}; --row-rgb: {rgb};">\n'
            f'        <div class="nx-rec-lab-label">{row["labLabel"]}{sub_html}</div>\n'
            f'        {tag_html}\n'
            f'        {walkthrough_btn}\n'
            f'      </div>'
        )

    chapter_label = row.get("chapter_notes_label", "Chapter Notes")
    chapter_btn = _render_button(row.get("chapter_notes_url"), chapter_label)
    return (
        f'      <div class="nx-rec-row">\n'
        f'        <div class="nx-rec-lab-label">{row["labLabel"]}{sub_html}</div>\n'
        f'        {chapter_btn}\n'
        f'        {walkthrough_btn}\n'
        f'      </div>'
    )


def _render_module_header(module):
    """Big, color-coded module header for the Home page's aggregated section.

    Uses the module's themeColor for a thick left bar and matching uppercase
    title. Plays the same role as a section divider — clear visual break
    between Module N and Module N+1 when scrolling.
    """
    color = module.get("themeColor", "#FF9F1C")
    rgb = _hex_to_rgb_triple(color)
    return (
        f'      <div class="nx-rec-mod-header" '
        f'style="--mod-color: {color}; --mod-rgb: {rgb};">\n'
        f'        <div class="nx-rec-mod-header__kicker">Module {module["num"]}</div>\n'
        f'        <div class="nx-rec-mod-header__title">{module["title"]}</div>\n'
        f'      </div>'
    )


def render_module_recordings_block(module_num, accent="#FF9F1C", base_dir=None):
    """Render the Recordings section for a single Module_N.html page.

    Returns the HTML block, or an empty string if no data exists for this
    module (graceful no-op so module pages don't error if recordings.json
    is missing or doesn't include this module).
    """
    try:
        data = _load_recordings(base_dir)
    except FileNotFoundError:
        return ""

    module = next(
        (m for m in data.get("modules", []) if m.get("num") == module_num),
        None,
    )
    if not module or not module.get("rows"):
        return ""

    theme_color = module.get("themeColor", "#FF9F1C")
    intro_html = data.get(
        "moduleIntro_html",
        "<p>Recordings for this module are posted here as they&rsquo;re produced.</p>",
    )
    rows_html = "\n".join(_render_row(r, theme_color) for r in module["rows"])

    return f"""    <div class="nx-recordings-block">
      <div class="nx-section-label nx-section-label--orange">Recordings</div>
      <div class="nx-recordings-block__intro">{intro_html}</div>
{rows_html}
    </div>"""


def render_home_recordings_block(base_dir=None):
    """Render the aggregated Recordings section for Home.html.

    One section containing all 5 modules. Each module gets a colored module
    header followed by its lab rows. Module headers use distinct themeColors
    so the visual boundary between modules is unmistakable.

    Returns an empty string if recordings.json is missing.
    """
    try:
        data = _load_recordings(base_dir)
    except FileNotFoundError:
        return ""

    modules = data.get("modules", [])
    if not modules:
        return ""

    intro_html = data.get(
        "homeIntro_html",
        "<p>Recordings are posted here as they&rsquo;re produced. "
        "Same buttons live on each module overview page.</p>",
    )

    blocks = []
    for module in modules:
        blocks.append(_render_module_header(module))
        theme_color = module.get("themeColor", "#FF9F1C")
        for row in module.get("rows", []):
            blocks.append(_render_row(row, theme_color))

    rows_html = "\n".join(blocks)

    return f"""    <div class="nx-section-label nx-section-label--orange">Recordings</div>
    <div class="nx-recordings-block">
      <div class="nx-recordings-block__intro">{intro_html}</div>
{rows_html}
    </div>"""


if __name__ == "__main__":
    # Smoke test: print both blocks if invoked directly.
    print("=== Home Recordings Block ===")
    print(render_home_recordings_block())
    print()
    print("=== Module 1 Recordings Block ===")
    print(render_module_recordings_block(1))
