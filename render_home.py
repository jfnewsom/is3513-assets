#!/usr/bin/env python3
"""
render_home.py
Renders Home page JSON → class-based HTML using site.css.
No inline styles, no external SVG images.

Usage:
  python3 render_home.py                       # uses default paths
  python3 render_home.py <src.json> <out.html>

Source:  pages/support/json/home.json
Output:  pages/support/Home.html
"""
import json, sys, os
from render_recordings import render_home_recordings_block

CSS_PATH = "../../site.css"
ASSETS   = "https://jfnewsom.github.io/is3513-assets"


def render_cta(cta):
    """Yellow CTA button at the top of the card."""
    return f'    <a href="{cta["href"]}" class="nx-cta-btn">{cta["text"]}</a>'


def render_video_story(story):
    """TV-news-style welcome video teaser.

    Two-column layout: video on the left (~25% width), text on the right.
    Stacks on mobile. The iframe markup itself is authored in the JSON
    (with the nx-video-embed__iframe class already applied) so the embed
    code can be regenerated/replaced from Panopto without touching the
    renderer.
    """
    return f"""    <div class="nx-video-story">
      <div class="nx-video-story__media">
        <div class="nx-video-embed">
          {story['embed']}
        </div>
      </div>
      <div class="nx-video-story__text">
        <div class="nx-video-story__kicker">{story['kicker']}</div>
        <h1 class="nx-video-story__headline">{story['headline']}</h1>
        <p class="nx-video-story__dek">{story['dek']}</p>
        <p class="nx-video-story__caption">{story['caption']}</p>
      </div>
    </div>"""


def render_narrative_intro(intro):
    """NEXUS narrative intro: left-justified tagline + body, with logo floated right.

    Sits between the CTA and the client showcase.
    Establishes the consulting-firm framing before any course mechanics.

    Layout: tagline on top (full width, left-justified), then logo floats right
    while body text wraps around it on the left.

    Triple-defense logo sizing (HTML attrs + inline style + doubled-specificity CSS)
    because SVGs without intrinsic dimensions can render at viewBox size otherwise.
    """
    logo_url = f'{ASSETS}/{intro["logo"]}'
    return f"""    <div class="nx-narrative-intro">
      <div class="nx-narrative-intro__tagline">{intro['tagline']}</div>
      <img class="nx-narrative-intro__logo nx-logo-glow" src="{logo_url}" alt="{intro['logoAlt']}" width="180" height="180" style="width:180px;height:auto;">
      <div class="nx-narrative-intro__body">{intro['body']}</div>
    </div>"""


def render_client_showcase(showcase):
    """2x2 grid of client cards: logo + name + modules + engagement summary.

    Each card uses the client's brand accent color (matches Module overviews).
    Triple-defense logo sizing (HTML attrs + inline style + doubled-specificity CSS).
    """
    cards = []
    for client in showcase["clients"]:
        logo_url = f'{ASSETS}/{client["logo"]}'
        cards.append(
            f"""      <div class="nx-client-card" style="--client-color: {client['color']};">
        <div class="nx-client-card__logo-frame">
          <img class="nx-client-card__logo" src="{logo_url}" alt="{client['logoAlt']}">
        </div>
        <div class="nx-client-card__name">{client['name']}</div>
        <div class="nx-client-card__modules">{client['modules']}</div>
        <p class="nx-client-card__engagement">{client['engagement']}</p>
      </div>"""
        )
    return f"""    <div class="nx-section-label nx-section-label--purple">{showcase['heading']}</div>
    <div class="nx-client-grid">
{chr(10).join(cards)}
    </div>"""


def render_instructor(inst, accent):
    """Instructor block: photo + name + title + note."""
    return f"""      <div class="nx-home-col">
        <div class="nx-section-label" style="--accent: {accent};">Your Instructor</div>
        <div class="nx-instructor">
          <img class="nx-instructor__photo" src="{inst['photo']}" alt="{inst['name']}">
          <div class="nx-instructor__bio">
            <div class="nx-instructor__name">{inst['name']}</div>
            <div class="nx-instructor__title">{inst['title']}</div>
            <div class="nx-instructor__note">{inst['note']}</div>
          </div>
        </div>
      </div>"""


def render_quick_links(links):
    """Quick Links column: icon + colored link + optional note."""
    items = []
    for link in links:
        target = ' target="_blank"' if link.get("external") else ''
        note = (f' <span class="nx-link-list__note">{link["note"]}</span>'
                if link.get("note") else '')
        items.append(
            f"""          <div class="nx-link-list__item">
            <span class="material-icons nx-inline-icon nx-inline-icon--{link['color']}">{link['icon']}</span>
            <a href="{link['href']}"{target} class="nx-link--{link['color']}">{link['label']}</a>{note}
          </div>"""
        )
    return f"""      <div class="nx-home-col">
        <div class="nx-section-label" style="--accent: #7B68EE;">Quick Links</div>
        <div class="nx-link-list">
{chr(10).join(items)}
        </div>
      </div>"""


def render_kv_list(items):
    """Renders a list of {label, value, optional href} dicts."""
    rows = []
    for item in items:
        if item.get("href"):
            target = ' target="_blank"' if item.get("external") else ''
            link_color = item.get("linkColor", "")
            link_class = f' class="nx-link--{link_color}"' if link_color else ''
            value = f'<a href="{item["href"]}"{target}{link_class}>{item["value"]}</a>'
        else:
            value = item["value"]
        rows.append(
            f'          <div class="nx-link-list__item"><strong>{item["label"]}:</strong> {value}</div>'
        )
    return "\n".join(rows)


def render_contact(contact_items):
    """Contact Details column."""
    rows = render_kv_list(contact_items)
    return f"""      <div class="nx-home-col">
        <div class="nx-section-label nx-section-label--cyan">Contact Details</div>
        <div class="nx-link-list">
{rows}
        </div>
      </div>"""


def render_format(format_items):
    """Course Format column."""
    rows = render_kv_list(format_items)
    return f"""      <div class="nx-home-col">
        <div class="nx-section-label nx-section-label--green">Course Format</div>
        <div class="nx-link-list">
{rows}
        </div>
      </div>"""


def render_stats(stats):
    """Stat bar: 4 large numeric stats."""
    items = []
    for s in stats:
        items.append(
            f"""      <div class="nx-info-stat">
        <div class="nx-info-stat__label nx-info-stat__label--{s['color']}">{s['label']}</div>
        <div class="nx-info-stat__value nx-info-stat__value--lg">{s['value']}</div>
      </div>"""
        )
    return f"""    <div class="nx-stat-bar">
{chr(10).join(items)}
    </div>"""


def render_cycle_callout(callout):
    """Purple callout describing the Unit cycle."""
    return f"""    <div class="nx-callout nx-purple">
      <div class="nx-callout-icon"><span class="material-icons" aria-hidden="true">sync_alt</span></div>
      <div class="nx-callout-body">
        <div class="nx-callout-title">{callout['title']}</div>
        <p>{callout['body']}</p>
      </div>
    </div>"""


def render_resource_cards(cards):
    """4-card resource grid."""
    cards_html = []
    for card in cards:
        links_html = "\n".join(
            f'          <div><a href="{l["href"]}">{l["label"]}</a></div>'
            for l in card["links"]
        )
        cards_html.append(
            f"""      <div class="nx-resource-card">
        <div class="nx-info-stat__label nx-info-stat__label--{card['color']}">{card['heading']}</div>
        <div class="nx-resource-links">
{links_html}
        </div>
      </div>"""
        )
    return f"""    <div class="nx-section-label nx-section-label--orange">Course Resources</div>
    <div class="nx-resource-grid">
{chr(10).join(cards_html)}
    </div>"""


def render_modules(modules, accent):
    """Module cards row (5 small clickable cards)."""
    cards = []
    for m in modules:
        cards.append(
            f"""      <div class="nx-module-card">
        <a href="{m['href']}">
          <div class="nx-module-card__title">{m['number']}</div>
          <div class="nx-info-stat__label">{m['title']}</div>
        </a>
      </div>"""
        )
    return f"""    <div class="nx-section-label" style="--accent: {accent};">Modules</div>
    <div class="nx-module-row">
{chr(10).join(cards)}
    </div>"""


def render(data):
    accent      = data["accent"]
    title       = data["title"]
    course_code = data["courseCode"]
    term        = data["term"]

    parts = [
        render_cta(data["cta"]),
        render_video_story(data["videoStory"]),
        render_narrative_intro(data["narrativeIntro"]),
        render_client_showcase(data["clientShowcase"]),
        f"""    <div class="nx-home-row">

{render_instructor(data["instructor"], accent)}

{render_quick_links(data["quickLinks"])}

    </div>""",
        f"""    <div class="nx-home-row">

{render_contact(data["contact"])}

{render_format(data["format"])}

    </div>""",
        render_stats(data["stats"]),
        render_cycle_callout(data["cycleCallout"]),
        render_resource_cards(data["resourceCards"]),
        render_modules(data["modules"], accent),
        render_home_recordings_block(),
        f'    <div class="nx-page-footer">{data["footer"]}</div>',
    ]

    body = "\n\n".join(filter(None, parts))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/png" href="{ASSETS}/favicon.png">
  <title>{course_code} - Information Assurance and Security</title>
  <link rel="stylesheet" href="{CSS_PATH}">
  <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
</head>
<body>

<div class="nx-page">

  <div class="nx-section nx-section--flush">
    <div class="nx-header" style="--accent: {accent};">
      <div class="nx-header-top">
        <div class="nx-kw">{course_code}</div>
        <div class="nx-sec">{title}</div>
      </div>
      <div class="nx-sub">{term}</div>
    </div>
  </div>

  <div class="nx-card" style="--accent: {accent};">

{body}

  </div>

</div>

<script src="{ASSETS}/nav.js"></script>
</body>
</html>"""


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) == 3:
        src, dst = sys.argv[1], sys.argv[2]
    else:
        src = os.path.join(base, "pages", "support", "json", "support_pages", "home.json")
        dst = os.path.join(base, "pages", "support", "Home.html")

    with open(src) as f:
        data = json.load(f)
    html = render(data)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as f:
        f.write(html)
    print(f"Rendered: {dst}")


if __name__ == "__main__":
    main()
