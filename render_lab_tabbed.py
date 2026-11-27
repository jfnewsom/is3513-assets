"""render_lab_tabbed.py - Tabbed IS3513 lab sheet (Spring 2027 layout).

Ported 2026-11-27 from IS2053's render_lab_tabbed.py (itself from the Sep 29
low-fi redesign prototype). Same lab JSON and the same render_lab.py block
renderers and site.css classes, so the NEXUS look carries over; only the
layout changes.

render_lab.py calls this for any lab whose meta has "layout": "tabs".

Layout (IS3513_Lab_Page_Redesign.md):
  tabs      Overview . CP1 ... CPn . Wrap-up
  checkpoint  header, What You're Doing as the lead, Why It Matters, steps and
              every other block in order, then ONE capture section (each
              screenshot with a camera icon, then What You Should Have), then a
              sideways card row of help callouts, one panel open at a time.
  stays on screen  warnings, required callouts, character quotes, tables, key
              flags, and any callout with "inline": true.
"""
import html as H
import re

import render_lab as R

# Help callouts that move behind a card click (unless "inline": true).
CARD_TYPES = ["tip", "proTip", "commonPitfalls", "textbookReference", "digDeeper",
              "thatsAReference", "goBeyond"]
CARD_ORDER = ["tip", "proTip", "commonPitfalls", "aiAssist", "textbookReference",
              "digDeeper", "goBeyond", "thatsAReference"]
CAPTURE_TYPES = {"screenshot", "screenshotRange", "whatYouShouldHave"}

GREEN, BLUE, PURPLE = "#00D26A", "#4169E1", "#7B68EE"
SHOT_RE = re.compile(r"[\w.-]+\.png")


def card_inner(section_html):
    """Contents of a section's nx-card, dropping the header and wrappers."""
    start = section_html.index('<div class="nx-card"')
    start = section_html.index(">", start) + 1
    end = section_html.rstrip().rfind("</div>")          # nx-section
    end = section_html.rfind("</div>", 0, end)           # nx-card
    return section_html[start:end]


def callout_body(callout_html):
    """A rendered callout with its title removed, for use inside a card panel."""
    return re.sub(r'\s*<div class="nx-callout-title">.*?</div>', "", callout_html, count=1, flags=re.S)


def card_button_icon(ctype, block):
    css, icon, title = R.CALLOUT_MAP.get(ctype, ("nx-purple", "info", ""))
    if ctype == "aiAssist":
        css, icon, title = "nx-purple", block.get("icon", "smart_toy"), block.get("title", "AI Assist")
    return css, icon, block.get("title") or title or "More"


def cards_row(cards):
    """cards: list of (css_class, icon, title, panel_html)."""
    if not cards:
        return ""
    btns = panels = ""
    for i, (css, icon, title, body) in enumerate(cards):
        btns += (f'<button type="button" class="nx-tb-card {css}" data-i="{i}" aria-expanded="false">'
                 f'<span class="material-icons nx-tb-card__icon" aria-hidden="true">{icon}</span>'
                 f'<span>{title}</span></button>')
        panels += f'<div class="nx-tb-cardpanel" data-i="{i}" hidden>{body}</div>'
    return (f'\n    <div class="nx-tb-cards"><div class="nx-tb-cards__row">{btns}</div>'
            f'{panels}</div>\n')


def capture_section(shots, wysh):
    if not shots and not wysh:
        return ""
    out = '\n    <div class="nx-tb-capture">\n'
    if shots:
        out += '      <h3>Capture</h3>\n      <ul class="nx-tb-shots">\n'
        for b in shots:
            body = b.get("body") or b.get("text") or ""
            files = SHOT_RE.findall(re.sub("<[^>]+>", "", body))
            name = files[0] if files else ""
            label = f'<code>{name}</code> ' if name else ""
            out += ('        <li><span class="material-icons" aria-hidden="true">photo_camera</span>'
                    f'<div>{label}{body}</div></li>\n')
        out += '      </ul>\n'
    for b in wysh:
        title = b.get("title") or "What You Should Have"
        body = b.get("body") or b.get("text") or ""
        out += f'      <h3>{title}</h3>\n      <p class="nx-tb-wysh">{body}</p>\n'
        items = b.get("items")
        if items:
            out += "      <ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>\n"
    return out + '    </div>\n'


def checkpoint_panel(cp):
    content = cp.get("content", [])
    body, shots, wysh, cards = "", [], [], []
    for b in content:
        t, ct = b.get("type"), b.get("calloutType")
        if t == "narrative":
            doing, matters = b.get("whatYoureDoing", ""), b.get("whyItMatters", "")
            if doing:
                body += f'    <p class="nx-tb-lead">{doing}</p>\n'
            if matters:
                body += f'    <h3>Why It Matters</h3>\n    <p>{matters}</p>\n'
        elif t == "callout" and ct in CAPTURE_TYPES:
            (wysh if ct == "whatYouShouldHave" else shots).append(b)
        elif t == "callout" and ct in CARD_TYPES and not b.get("inline"):
            css, icon, title = card_button_icon(ct, b)
            cards.append((ct, css, icon, title, callout_body(R.render_callout_block(b))))
        elif t == "aiAssist" and not b.get("inline"):
            css, icon, title = card_button_icon("aiAssist", b)
            cards.append(("aiAssist", css, icon, title, callout_body(R.render_ai_assist(b))))
        else:
            body += R.render_checkpoint_content([b])
    body += capture_section(shots, wysh)
    cards.sort(key=lambda c: CARD_ORDER.index(c[0]) if c[0] in CARD_ORDER else 99)
    body += cards_row([c[1:] for c in cards])
    hdr = R.header("checkpoint", str(cp["number"]), cp["title"], GREEN, extra_class="nx-checkpoint")
    return hdr, R.card(body, GREEN)


def build(data):
    meta = data["meta"]
    lab_num = ".".join(meta["labId"].split("_"))
    is_eng = meta.get("labType") == "engagement"
    lab_col = PURPLE if is_eng else BLUE
    tabs = []

    # Overview: the intro card, What You Already Have (engagement labs), and
    # the Time Guide behind a card.
    _, intro_sec = R.render_intro(data)
    ov = card_inner(intro_sec)
    if is_eng:
        yah = R.render_you_already_have(data)
        if yah:
            ov += "    <h2>What You Already Have</h2>\n" + card_inner(yah)
    tg = R.render_time_guide(data)
    if tg:
        ov += cards_row([("nx-orange", "schedule", "Time Guide", card_inner(tg))])
    tabs.append(("overview", "Overview", lab_col,
                 R.header("lab", lab_num, meta["title"], lab_col), R.card(ov, lab_col)))

    for cp in data.get("checkpoints", []):
        hdr, body = checkpoint_panel(cp)
        tabs.append((f'cp{cp["number"]}', f'CP{cp["number"]}', GREEN, hdr, body, cp["title"]))

    # Wrap-up: everything that used to follow the checkpoints, unchanged.
    wrap = "".join(p for p in (R.render_final_checklist(data), R.render_purple_team(data),
                               R.render_grading_standards(data) if is_eng else "",
                               R.render_need_help(data)) if p)
    tabs.append(("wrapup", "Wrap-up", lab_col,
                 R.header("lab", lab_num, "Before You Submit", lab_col), wrap, True))
    return tabs


def page(data, tabs):
    meta = data["meta"]
    lab_num = ".".join(meta["labId"].split("_"))
    order = [t[0] for t in tabs]
    buttons = panels = ""
    for i, t in enumerate(tabs):
        tid, name, col, hdr, body = t[:5]
        extra = t[5] if len(t) > 5 else None
        is_sections = extra is True                  # Wrap-up body is whole sections
        tip = f' title="{H.escape(re.sub("<[^>]+>", "", extra), quote=True)}"' if isinstance(extra, str) else ""
        dark = col == GREEN
        buttons += (f'<a class="nx-tb-tab{" nx-tb-tab--dark" if dark else ""}" role="tab" href="#{tid}" '
                    f'data-tab="{tid}" style="--tab:{col}"{tip}>{name}</a>')
        back = nxt = ""
        if i > 0:
            p = tabs[i - 1]
            back = f'<a class="nx-tb-back" href="#{p[0]}" data-tab="{p[0]}">&larr; Back: {p[1]}</a>\n'
        if i < len(tabs) - 1:
            n = tabs[i + 1]
            nxt = f'<a class="nx-tb-next" href="#{n[0]}" data-tab="{n[0]}">Next: {n[1]} &rarr;</a>'
        inner = R.section(hdr + body) if not is_sections else body   # Wrap-up sections carry their own headers
        panels += (f'<section class="nx-tb-panel" id="p-{tid}" data-tab="{tid}" role="tabpanel" hidden>\n'
                   f'{back}{inner}<div class="nx-tb-botnav">{nxt}</div>\n</section>\n')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lab {lab_num}: {meta["title"]}</title>
  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is3513-assets/favicon.png">
  <link rel="stylesheet" href="../../site.css">
</head>
<body class="nx-tabbed">
<h1 class="nx-sr-only">Lab {lab_num}: {meta["title"]}</h1>
<div class="nx-tb-bar">
  <div class="nx-tb-scroller">
    <button type="button" class="nx-tb-fade l" aria-label="More tabs to the left">&lsaquo;</button>
    <nav class="nx-tb-tabs" role="tablist" aria-label="Lab sections">{buttons}</nav>
    <button type="button" class="nx-tb-fade r" aria-label="More tabs to the right">&rsaquo;</button>
  </div>
  <a class="nx-tb-newtab" id="nx-tb-newtab" href="#" target="_blank" rel="noopener" hidden>Open in new tab &#8599;</a>
</div>
<main class="nx-tb-main">
{panels}</main>
<script>
(function(){{
const nav=document.querySelector('.nx-tb-tabs'), inIframe=window.self!==window.top, pos={{}}; let cur=null;
function show(id,push){{
  if(!document.getElementById('p-'+id)) id='{order[0]}';
  if(cur) pos[cur]=scrollY;
  document.querySelectorAll('.nx-tb-panel').forEach(p=>p.hidden=p.dataset.tab!==id);
  document.querySelectorAll('.nx-tb-tab').forEach(t=>t.setAttribute('aria-selected',t.dataset.tab===id));
  cur=id;
  const a=nav.querySelector('[aria-selected=true]'); if(a) a.scrollIntoView({{block:'nearest',inline:'center'}});
  scrollTo(0,pos[id]||0);
  if(push) history.replaceState(null,'','#'+id);
  document.getElementById('nx-tb-newtab').href=location.href.split('#')[0]+'#'+id;
  fades();
}}
document.addEventListener('click',e=>{{
  const a=e.target.closest('a[data-tab]'); if(a){{e.preventDefault();show(a.dataset.tab,true);return;}}
  const c=e.target.closest('.nx-tb-card'); if(!c) return;
  const box=c.closest('.nx-tb-cards'), open=c.getAttribute('aria-expanded')==='true';
  box.querySelectorAll('.nx-tb-card').forEach(b=>b.setAttribute('aria-expanded','false'));
  box.querySelectorAll('.nx-tb-cardpanel').forEach(p=>p.hidden=true);
  if(!open){{c.setAttribute('aria-expanded','true');box.querySelector('.nx-tb-cardpanel[data-i="'+c.dataset.i+'"]').hidden=false;}}
}});
const L=document.querySelector('.nx-tb-fade.l'),Rt=document.querySelector('.nx-tb-fade.r');
function fades(){{L.classList.toggle('on',nav.scrollLeft>4);Rt.classList.toggle('on',nav.scrollLeft+nav.clientWidth<nav.scrollWidth-4);}}
nav.addEventListener('scroll',fades); addEventListener('resize',fades);
L.onclick=()=>nav.scrollBy({{left:-nav.clientWidth*.7,behavior:'smooth'}});
Rt.onclick=()=>nav.scrollBy({{left:nav.clientWidth*.7,behavior:'smooth'}});
if(inIframe) document.getElementById('nx-tb-newtab').hidden=false;
addEventListener('hashchange',()=>show(location.hash.slice(1),false));
show(location.hash.slice(1)||'{order[0]}',false);
}})();
</script>
<script src="https://jfnewsom.github.io/is3513-assets/nav.js"></script>
</body>
</html>"""


def render_tabbed(data):
    """Return the tabbed page HTML for one lab JSON dict."""
    return page(data, build(data))
