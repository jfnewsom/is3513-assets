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
(or render_all.sh — note that render_all.sh does not currently include
render_home.py, so Home.html must be re-rendered separately).
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


def _render_row(row):
    """Render one recording row: lab label + Chapter Notes + Lab Walkthrough.

    Engagement rows (Lab X.3, Lab 5.2) render an invisible placeholder in the
    Chapter Notes slot because no new chapter is introduced. The slot is kept
    (not removed) so the Lab Walkthrough column aligns vertically across all
    rows in the same module — treating the rows like a table where the
    engagement row has an empty cell.
    """
    is_engagement = (row.get("type") == "engagement")
    chapter_label = row.get("chapter_notes_label", "Chapter Notes")
    if is_engagement:
        chapter_btn = (
            f'<span class="nx-rec-btn nx-rec-btn--empty" aria-hidden="true">'
            f'{chapter_label}</span>'
        )
    else:
        chapter_btn = _render_button(row.get("chapter_notes_url"), chapter_label)
    walkthrough_btn = _render_button(row.get("lab_walkthrough_url"), "Lab Walkthrough")

    sub_html = ""
    if row.get("labTitle"):
        sub_html = f'<span class="nx-rec-lab-label__sub">{row["labTitle"]}</span>'

    return (
        f'      <div class="nx-rec-row">\n'
        f'        <div class="nx-rec-lab-label">{row["labLabel"]}{sub_html}</div>\n'
        f'        {chapter_btn}\n'
        f'        {walkthrough_btn}\n'
        f'      </div>'
    )


def render_module_recordings_block(module_num, accent="#FF9F1C", base_dir=None):
    """Render the Recordings section for a single Module_N.html page.

    Returns the HTML block, or an empty string if no data exists for this
    module (graceful no-op so module pages don't error if recordings.json
    is missing).

    Designed to be inserted alongside the other sections in
    render_module_overview.py — same block-level structure as the
    nx-readings-block.
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

    intro_html = data.get(
        "moduleIntro_html",
        "<p>Recordings for this module are posted here as they&rsquo;re produced.</p>",
    )
    rows_html = "\n".join(_render_row(r) for r in module["rows"])

    return f"""    <div class="nx-recordings-block">
      <div class="nx-section-label nx-section-label--orange">Recordings</div>
      <div class="nx-recordings-block__intro">{intro_html}</div>
{rows_html}
    </div>"""


def render_home_recordings_block(base_dir=None):
    """Render the aggregated Recordings section for Home.html.

    One section containing all 5 modules. Each module gets a yellow
    `.nx-rec-mod-label` header (Module N: <thematic title>) followed by its
    lab rows. Same button rendering as the per-module section — active
    anchors for set URLs, disabled placeholder spans otherwise.

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
        header = f'Module {module["num"]}: {module["title"]}'
        blocks.append(f'      <div class="nx-rec-mod-label">{header}</div>')
        for row in module.get("rows", []):
            blocks.append(_render_row(row))

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
