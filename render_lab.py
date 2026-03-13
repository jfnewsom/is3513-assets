#!/usr/bin/env python3
"""
render_lab.py — IS3513 Lab JSON → HTML renderer
Target format: CSS-class system (labs.css + nav.js)
Usage: python3 render_lab.py <path/to/lab_COMPLETE.json> [output.html]
"""

import json
import sys
from pathlib import Path

ASSETS = "https://jfnewsom.github.io/is3513-assets"

# ── Callout type → (css_class, icon, default_title) ──────────────────────────
CALLOUT_MAP = {
    "screenshot":        ("nx-blue",   "photo_camera",    "Screenshot"),
    "screenshotRange":   ("nx-blue",   "photo_camera",    "Screenshots"),
    "commonPitfalls":    ("nx-orange", "warning",         "Common Pitfalls"),
    "warning":           ("nx-orange", "warning",         "Warning"),
    "whatYouShouldHave": ("nx-green",  "check_circle",    "What You Should Have"),
    "textbookReference": ("nx-purple", "menu_book",       "Textbook Reference"),
    "digDeeper":         ("nx-yellow", "search",          "Dig Deeper"),
    "thatsAReference":   ("nx-green",  "menu_book",       "That&#8217;s a Reference!"),
    "tip":               ("nx-cyan",   "lightbulb",       "Pro Tip"),
    "proTip":            ("nx-cyan",   "lightbulb",       "Pro Tip"),
    "canvasSubmission":  ("nx-cyan",   "description",     "Canvas Submission"),
    "required":          ("nx-red",    "error",           "Required"),
    "error":             ("nx-red",    "error",           ""),
    "goBeyond":          ("nx-yellow", "search",          "Go Beyond"),
    "reportSections":    ("nx-purple", "description",     "Report Sections"),
    "reportStructure":   ("nx-purple", "description",     "Report Structure"),
    "blueTeamLearns":    ("nx-blue",   "security",        "What Blue Team Learns"),
    "purpleTeamConnection": ("nx-purple", "sync_alt",     "The Purple Team Connection"),
    "characterQuote":    ("nx-purple", None,              None),
    "nextSteps":         ("nx-blue",   "arrow_forward",   "Next Steps"),
    "cleanup":           ("nx-cyan",   "cleaning_services", "Cleanup"),
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def h(text):
    """Pass HTML entities and markup through unchanged."""
    return text or ""


def section(content, comment=None):
    c = f"\n<!-- {'═' * 50} {comment.upper()} -->\n" if comment else ""
    return f"{c}<div class=\"nx-section\">\n{content}</div>\n"


def header(kw, sec_text, sub, accent, extra_class=""):
    cls = f"nx-header{' ' + extra_class if extra_class else ''}"
    sec_part = f'\n      <div class="nx-sec">{h(sec_text)}</div>' if sec_text else ""
    sub_part  = f'\n    <div class="nx-sub">{h(sub)}</div>' if sub else ""
    return (
        f'  <div class="{cls}" style="--accent: {accent};">\n'
        f'    <div class="nx-header-top">\n'
        f'      <div class="nx-kw">{h(kw)}</div>{sec_part}\n'
        f'    </div>{sub_part}\n'
        f'  </div>\n'
    )


def card(inner, accent):
    return (
        f'  <div class="nx-card" style="--accent: {accent};">\n'
        f'{inner}'
        f'  </div>\n'
    )


def callout(css_class, icon, title, body_html):
    icon_html = f'<span class="material-icons" aria-hidden="true">{icon}</span>'
    return (
        f'    <div class="nx-callout {css_class}">\n'
        f'      <div class="nx-callout-icon">{icon_html}</div>\n'
        f'      <div class="nx-callout-body">\n'
        f'        <div class="nx-callout-title">{h(title)}</div>\n'
        f'{body_html}'
        f'      </div>\n'
        f'    </div>\n'
    )


def callout_p(css_class, icon, title, text):
    body = f'        <p>{h(text)}</p>\n' if text else ""
    return callout(css_class, icon, title, body)


def callout_ul(css_class, icon, title, items):
    lis = "".join(f'          <li>{h(i)}</li>\n' for i in items)
    body = f'        <ul>\n{lis}        </ul>\n'
    return callout(css_class, icon, title, body)


def render_callout_block(block):
    """Render a generic callout block from a checkpoint content array."""
    ct = block.get("calloutType", block.get("type", ""))
    cfg = CALLOUT_MAP.get(ct, ("nx-purple", "info", ""))
    css_class, default_icon, default_title = cfg

    # characterQuote is special
    if ct == "characterQuote":
        return render_char_quote(block)

    icon  = block.get("icon", default_icon) or default_icon
    title = block.get("title", default_title) or default_title

    # reportSections — special structured block
    if ct == "reportSections":
        return render_report_sections(block)

    # Items list
    items = block.get("items")
    if items:
        return callout_ul(css_class, icon, title, items)

    # Plain text
    text = block.get("text", block.get("body", ""))
    return callout_p(css_class, icon, title, text)


def render_char_quote(block):
    character = h(block.get("character", ""))
    role      = h(block.get("role", block.get("title", "")))
    headshot  = block.get("headshot", "")
    text      = h(block.get("text", block.get("quote", "")))
    img_src   = f"{ASSETS}/headshots/{headshot}"
    alt_name  = character.split(",")[0].strip()
    return (
        f'    <div class="nx-quote">\n'
        f'      <div class="nx-quote-main">\n'
        f'        <div class="nx-quote-avatar">\n'
        f'          <img src="{img_src}" alt="{alt_name}">\n'
        f'        </div>\n'
        f'        <div class="nx-quote-bubble">\n'
        f'          <p>&#8220;{text}&#8221;</p>\n'
        f'        </div>\n'
        f'      </div>\n'
        f'      <div class="nx-quote-attribution">\n'
        f'        <div class="nx-quote-name">{character}</div>\n'
        f'        <div class="nx-quote-title">{role}</div>\n'
        f'      </div>\n'
        f'    </div>\n'
    )


def render_report_sections(block):
    sections = block.get("sections", [])
    inner = ""
    for s in sections:
        label = h(s.get("label", ""))
        desc  = h(s.get("description", ""))
        inner += f'        <p><strong>{label}:</strong> {desc}</p>\n'
    return (
        f'    <div class="nx-callout nx-purple">\n'
        f'      <div class="nx-callout-icon">'
        f'<span class="material-icons" aria-hidden="true">description</span></div>\n'
        f'      <div class="nx-callout-body">\n'
        f'        <div class="nx-callout-title">Report Sections</div>\n'
        f'{inner}'
        f'      </div>\n'
        f'    </div>\n'
    )


def render_what_this_does(wtd):
    """Render a whatThisDoes object as a <details> block."""
    if not wtd:
        return ""
    inner = ""
    if wtd.get("concept"):
        inner += f'            <p><strong>Concept:</strong> {h(wtd["concept"])}</p>\n'
    if wtd.get("output"):
        inner += f'            <p><strong>In your output:</strong> {h(wtd["output"])}</p>\n'
    flags = wtd.get("flags")
    if flags:
        flag_items = "".join(
            f'              <li><code>{h(f["flag"])}</code> &#8212; {h(f["description"])}</li>\n'
            for f in flags
        )
        inner += f'            <p><strong>Flags:</strong></p>\n            <ul>\n{flag_items}            </ul>\n'
    if not inner:
        return ""
    return (
        f'        <details>\n'
        f'          <summary>What this does</summary>\n'
        f'          <div class="nx-details-body">\n'
        f'{inner}'
        f'          </div>\n'
        f'        </details>\n'
    )


def render_generic_table(block):
    """Render a generic data table (columns + rows) inside a checkpoint."""
    title   = block.get("title", "")
    columns = block.get("columns", [])
    rows    = block.get("rows", [])
    note    = block.get("note")

    out = ""
    if title:
        out += f'    <h3>{h(title)}</h3>\n'
    out += '    <table class="nx-time-table">\n'
    out += '      <thead><tr>\n'
    for col in columns:
        out += f'        <th>{h(col)}</th>\n'
    out += '      </tr></thead>\n'
    out += '      <tbody>\n'
    for row in rows:
        out += '        <tr>\n'
        for i, cell in enumerate(row):
            td_class = ' class="nx-time-label"' if i == 0 else ""
            out += f'          <td{td_class}>{h(cell)}</td>\n'
        out += '        </tr>\n'
    out += '      </tbody>\n    </table>\n'
    if note:
        out += f'    <p><em>{h(note)}</em></p>\n'
    return out


def render_steps_block(block):
    """Render a steps block as a numbered <ol> with nx-cmd blocks."""
    part  = block.get("part")
    start = block.get("start", 1)
    steps = block.get("steps", [])

    out = ""
    if part:
        out += f'    <h3>{h(part)}</h3>\n'

    start_attr = f' start="{start}"' if start != 1 else ""
    out += f'    <ol{start_attr}>\n'
    for step in steps:
        text      = h(step.get("text", ""))
        command   = step.get("command")
        wtd       = step.get("whatThisDoes")
        sub_items = step.get("subItems", [])
        # If step has no visible content at all, render wtd outside the ol entirely
        if not text and not command and not sub_items and wtd:
            out += f'    </ol>\n'
            out += render_what_this_does(wtd)
            out += f'    <ol start="{steps.index(step) + start + 1}">\n'
            continue
        out += f'      <li>{text}\n'
        if command:
            out += f'        <div class="nx-cmd">{command}</div>\n'
        if sub_items:
            out += '        <ul>\n'
            for si in sub_items:
                code  = si.get("code", "")
                label = h(si.get("label", ""))
                if code and label:
                    out += f'          <li><code>{code}</code> &#8212; {label}</li>\n'
                elif code:
                    out += f'          <li><code>{code}</code></li>\n'
                else:
                    out += f'          <li>{label}</li>\n'
            out += '        </ul>\n'
        if wtd:
            out += render_what_this_does(wtd)
        out += f'      </li>\n'
    out += f'    </ol>\n'
    return out


def render_narrative(block):
    """Render a narrative block (what you're doing / why it matters)."""
    doing   = h(block.get("whatYoureDoing", ""))
    matters = h(block.get("whyItMatters", ""))
    out = ""
    if doing:
        out += f'    <h3>What You&#8217;re Doing</h3>\n    <p>{doing}</p>\n'
    if matters:
        out += f'    <h3>Why It Matters</h3>\n    <p>{matters}</p>\n'
    return out


def render_conversion_table(block):
    """Render the Dec/Hex/Binary 0-15 conversion cheat sheet (two side-by-side tables)."""
    tip = block.get("tip", "To convert <strong>168</strong> to hex: 168 = 160 + 8 = A0 + 08 = <strong>A8</strong>. To convert <strong>252</strong>: 252 = 240 + 12 = F0 + 0C = <strong>FC</strong>.")

    def table_html(rows):
        hdr = (
            '        <thead><tr>\n'
            '          <th class="nx-conv-dec">Dec</th>\n'
            '          <th class="nx-conv-hex">Hex</th>\n'
            '          <th class="nx-conv-bin">Binary</th>\n'
            '        </tr></thead>\n'
            '        <tbody>\n'
        )
        body = ""
        for d in rows:
            body += (
                f'          <tr>'
                f'<td class="nx-conv-dec">{d}</td>'
                f'<td class="nx-conv-hex">{format(d, "X")}</td>'
                f'<td class="nx-conv-bin">{format(d, "04b")}</td>'
                f'</tr>\n'
            )
        return f'      <table class="nx-conv-table">\n{hdr}{body}        </tbody>\n      </table>\n'

    return (
        f'    <p class="nx-cidr-vis-intro">Memorize these 16 values (0&#8211;15) and you can convert anything:</p>\n'
        f'    <div class="nx-conv-wrap">\n'
        f'{table_html(range(8))}'
        f'{table_html(range(8, 16))}'
        f'    </div>\n'
        f'    <div class="nx-callout nx-cyan">\n'
        f'      <div class="nx-callout-icon"><span class="material-icons" aria-hidden="true">lightbulb</span></div>\n'
        f'      <div class="nx-callout-body">\n'
        f'        <div class="nx-callout-title">How to Use This Table</div>\n'
        f'        <p>{h(tip)}</p>\n'
        f'      </div>\n'
        f'    </div>\n'
    )


def render_cidr_visualizer(block):
    """Render color-coded 32-bit CIDR visualizer.
    JSON fields:
      title       – heading text (optional)
      intro       – paragraph before the box (optional)
      prefix      – int, network bits (required)
      subnetBits  – int, bits borrowed for subnetting (default 0 = 2-color mode)
      caption     – text below the bit row (optional; auto-generated if absent)
    """
    prefix      = int(block.get("prefix", 24))
    subnet_bits = int(block.get("subnetBits", 0))
    host_bits   = 32 - prefix - subnet_bits
    title       = block.get("title", "The Visual Count-Out Method")
    intro       = block.get("intro", "")
    caption     = block.get("caption", "")

    # Auto-caption when not provided
    if not caption:
        if subnet_bits:
            new_prefix = prefix + subnet_bits
            caption = f"New CIDR: /{new_prefix} ({prefix} original + {subnet_bits} borrowed = {new_prefix})"
        else:
            # Build subnet mask from prefix
            mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
            octets = [(mask_int >> (8 * i)) & 0xFF for i in [3, 2, 1, 0]]
            hex_parts = ".".join(f"{o:02X}" for o in octets)
            dec_parts = ".".join(str(o) for o in octets)
            caption = f"Subnet Mask: {dec_parts} ({hex_parts})"

    # Badge row
    badge_html = f'<span class="nx-cidr-badge nx-cidr-badge-net">Network: {prefix} bits</span>\n'
    if subnet_bits:
        badge_html += f'        <span class="nx-cidr-badge nx-cidr-badge-sub">Subnet: +{subnet_bits} bits</span>\n'
    badge_html += f'        <span class="nx-cidr-badge nx-cidr-badge-host">Host: {host_bits} bits</span>'

    # Bit spans — iterate all 32 bits, inserting dots between octets
    def bit_span(i):
        """Return the CSS class for bit position i (0 = leftmost)."""
        if i < prefix:
            return "nx-bit-net"
        elif i < prefix + subnet_bits:
            return "nx-bit-sub"
        else:
            return "nx-bit-host"

    bit_value = lambda i: "1" if i < prefix + subnet_bits else "0"

    bits_html = ""
    for i in range(32):
        if i > 0 and i % 8 == 0:
            bits_html += '        <span class="nx-bit-dot">.</span>\n'
        css = bit_span(i)
        val = bit_value(i)
        bits_html += f'        <span class="{css}">{val}</span>\n'

    title_html = f'    <h4 class="nx-cidr-vis-title">{title}</h4>\n' if title else ""
    intro_html = f'    <p class="nx-cidr-vis-intro">{h(intro)}</p>\n' if intro else ""

    return (
        f'    <div class="nx-cidr-vis">\n'
        f'{title_html}'
        f'{intro_html}'
        f'      <div class="nx-cidr-box">\n'
        f'        <div class="nx-cidr-badges">\n'
        f'        {badge_html}\n'
        f'        </div>\n'
        f'        <div class="nx-cidr-bits">\n'
        f'{bits_html}'
        f'        </div>\n'
        f'        <div class="nx-cidr-caption">{caption}</div>\n'
        f'      </div>\n'
        f'    </div>\n'
    )


def render_checkpoint_content(content_list):
    """Route each content block in a checkpoint to its renderer."""
    out = ""
    for block in content_list:
        btype = block.get("type", "")
        if btype == "narrative":
            out += render_narrative(block)
        elif btype == "table":
            out += render_generic_table(block)
        elif btype == "steps":
            out += render_steps_block(block)
        elif btype == "conversionTable":
            out += render_conversion_table(block)
        elif btype == "cidrVisualizer":
            out += render_cidr_visualizer(block)
        elif btype == "callout":
            out += render_callout_block(block)
        else:
            # fallback — try callout
            out += render_callout_block(block)
    return out


# ── Section renderers ─────────────────────────────────────────────────────────

def render_intro(data):
    meta  = data["meta"]
    intro = data["intro"]
    lab_type = meta.get("labType", "foundation")
    is_engagement = lab_type == "engagement"

    lab_id_parts = meta["labId"].split("_")
    kw_text  = "lab"
    sec_text = ".".join(lab_id_parts)   # e.g. "2.3"

    accent = "#7B68EE" if is_engagement else "#4169E1"
    nav_src = f'{ASSETS}/nav.js{"?context=lab" if is_engagement else ""}'

    inner = f'    <p class="nx-module-label">{h(meta["module"])}</p>\n\n'
    inner += f'    <h2>Overview</h2>\n    <p>{h(intro["overview"])}</p>\n\n'

    # Mentor quote
    mq = intro.get("mentorQuote")
    if mq:
        inner += render_char_quote({
            "character": mq["character"],
            "title":     mq["title"],
            "headshot":  mq["headshot"],
            "text":      mq.get("quote", mq.get("text", ""))
        })

    # Chapters
    chapters = meta.get("chapters", [])
    if chapters:
        inner += f'    <h2>Chapters Covered</h2>\n'
        inner += f'    <p>{" | ".join(h(c) for c in chapters)}</p>\n\n'

    # Client context (engagement labs)
    ctx = intro.get("clientContext")
    if ctx:
        desc = ctx.get("description", "")
        inner += f'    <h2>Client Context</h2>\n'
        if desc:
            inner += f'    <p><strong>{h(ctx["client"])}</strong> &#8212; {h(desc)}</p>\n'
        else:
            inner += f'    <p><strong>{h(ctx["client"])}</strong></p>\n'
        # contacts array or single contact via contactName/contactTitle
        contacts = ctx.get("contacts", [])
        if not contacts and ctx.get("contactName"):
            contacts = [{"name": ctx["contactName"], "title": ctx["contactTitle"], "quote": ""}]
        if contacts:
            inner += '    <ul>\n'
            for c in contacts:
                name  = h(c.get("name", c.get("contactName", "")))
                title = h(c.get("title", c.get("contactTitle", "")))
                quote = h(c.get("quote", ""))
                if quote:
                    inner += f'      <li><strong>{name}, {title}:</strong> &#8220;{quote}&#8221;</li>\n'
                else:
                    inner += f'      <li><strong>{name}, {title}</strong></li>\n'
            inner += '    </ul>\n'

    # Objectives
    objs = intro.get("objectives", [])
    if objs:
        inner += f'\n    <h2>Assignment Objectives</h2>\n    <ul>\n'
        inner += "".join(f'      <li>{h(o)}</li>\n' for o in objs)
        inner += '    </ul>\n'

    # Key concepts (foundation labs sometimes have these)
    # Focus areas / Key Concepts — always render when present
    focus = intro.get("focusAreas", [])
    if focus:
        inner += f'\n    <h2>Key Concepts</h2>\n    <ul>\n'
        for f in focus:
            if isinstance(f, dict):
                inner += f'      <li><strong>{h(f["title"])}:</strong> {h(f["description"])}</li>\n'
            else:
                inner += f'      <li>{h(f)}</li>\n'
        inner += '    </ul>\n'

    # Callouts (error banners etc.)
    for c_block in intro.get("callouts", []):
        ct = c_block.get("type", "")
        if ct == "characterQuote":
            inner += render_char_quote(c_block)
            continue
        cfg = CALLOUT_MAP.get(ct, ("nx-red", "error", ""))
        css_cls, default_icon, default_title = cfg
        icon  = c_block.get("icon", default_icon)
        title = c_block.get("title", default_title)
        text  = c_block.get("text", c_block.get("body", ""))
        inner += callout_p(css_cls, icon, title, text)

    hdr  = header(kw_text, sec_text, h(meta["title"]), accent)
    body = card(inner, accent)
    return nav_src, section(hdr + body, "lab header")


def render_you_already_have(data):
    yah = data.get("youAlreadyHave")
    if not yah:
        return ""
    accent = "#00BCD4"
    inner = f'    <p><strong>{h(yah.get("intro", "This is NOT starting from scratch."))}</strong></p>\n\n'

    for sec in yah.get("sections", []):
        title = h(sec.get("title", ""))
        badge = sec.get("badge")
        badge_html = f' <span class="nx-badge-new">{badge}</span>' if badge else ""
        inner += f'    <h2>{title}{badge_html}</h2>\n    <ul class="nx-checklist">\n'
        for item in sec.get("items", []):
            if badge:
                inner += f'      <li><span class="nx-badge-new">{badge}</span> {h(item)}</li>\n'
            else:
                inner += f'      <li><span class="nx-check">&#10004;</span> {h(item)}</li>\n'
        inner += '    </ul>\n\n'

    # Callouts
    for c_block in yah.get("callouts", []):
        ct    = c_block.get("calloutType", c_block.get("type", "tip"))
        cfg   = CALLOUT_MAP.get(ct, ("nx-cyan", "lightbulb", "Tip"))
        css_cls, default_icon, default_title = cfg
        icon  = c_block.get("icon", default_icon)
        title = c_block.get("title", default_title)
        text  = c_block.get("text", c_block.get("body", ""))
        inner += callout_p(css_cls, icon, title, text)

    hdr  = header("you already", "have", "Three-Week Engagement Model", accent)
    body = card(inner, accent)
    return section(hdr + body, "you already have")


def render_time_guide(data):
    tg = data.get("timeGuide", {})
    rows = tg.get("rows", [])
    total = tg.get("totalRow", {})
    note  = tg.get("timesheetNote")
    accent = "#FF9F1C"

    inner = (
        f'    <table class="nx-time-table">\n'
        f'      <thead><tr><th>Task</th><th>Est. Time</th></tr></thead>\n'
        f'      <tbody>\n'
    )
    for row in rows:
        inner += f'        <tr><td>{h(row["task"])}</td><td>{h(row["time"])}</td></tr>\n'
    if total:
        inner += (
            f'        <tr class="nx-total">'
            f'<td>{h(total.get("label", "TOTAL"))}</td>'
            f'<td>{h(total.get("time", ""))}</td></tr>\n'
        )
    inner += '      </tbody>\n    </table>\n'

    if note:
        inner += f'\n    <p>{h(note)}</p>\n'

    hdr  = header("time", "guide", "Estimated completion times per checkpoint", accent)
    body = card(inner, accent)
    return section(hdr + body, "time guide")


def render_checkpoint(cp):
    num   = cp["number"]
    title = cp["title"]
    accent = "#00D26A"

    inner = render_checkpoint_content(cp.get("content", []))

    hdr  = header("checkpoint", str(num), title, accent, extra_class="nx-checkpoint")
    body = card(inner, accent)
    return section(hdr + body, f"checkpoint {num}")


def render_purple_team(data):
    pt = data.get("purpleTeam")
    if not pt:
        return ""
    accent = "#7B68EE"
    inner = ""

    red  = pt.get("redTeam", {})
    blue = pt.get("blueTeam", {})
    conn = pt.get("connection")

    if red:
        items = red.get("items", [])
        inner += callout_ul("nx-red", "security", h(red.get("label", "What Red Team Learns")), items)

    if blue:
        items = blue.get("items", [])
        inner += callout_ul("nx-blue", "security", h(blue.get("label", "What Blue Team Learns")), items)

    if conn:
        inner += callout_p("nx-purple", "sync_alt", "The Purple Team Connection", conn)

    hdr  = header("purple", "team", "Both Sides of the Shield", accent)
    body = card(inner, accent)
    return section(hdr + body, "purple team")


def render_final_checklist(data):
    fc = data.get("finalChecklist", {})
    accent = "#00D26A"
    inner = ""

    # Screenshot table (foundation labs)
    ss_table = fc.get("screenshotTable")
    if ss_table:
        inner += f'    <h2>Screenshots</h2>\n    <ul class="nx-checklist">\n'
        for row in ss_table:
            fname = row.get("filename", row.get("file", ""))
            inner += f'      <li>&#9744; <code>{h(fname)}</code> &#8212; {h(row["description"])}</li>\n'
        inner += '    </ul>\n\n'

    # Checklist sections
    for sec in fc.get("sections", []):
        sec_title = h(sec.get("label", sec.get("title", "")))
        sec_type  = sec.get("type", "checklist")
        inner += f'    <h2>{sec_title}</h2>\n    <ul class="nx-checklist">\n'
        for item in sec.get("items", []):
            if isinstance(item, dict):
                if sec_type == "screenshotTable":
                    num  = h(str(item.get("number", "")))
                    desc = h(item.get("description", ""))
                    inner += f'      <li>&#9744; <strong>{num}.</strong> {desc}</li>\n'
                else:
                    # generic dict fallback — bold label + text
                    label = h(item.get("label", item.get("title", "")))
                    text  = h(item.get("text", item.get("description", "")))
                    inner += f'      <li>&#9744; <strong>{label}:</strong> {text}</li>\n'
            else:
                inner += f'      <li>&#9744; {h(item)}</li>\n'
        inner += '    </ul>\n\n'

    # Canvas submission callout
    canvas = fc.get("canvasSubmission")
    if canvas:
        canvas_text = canvas.get("text", canvas) if isinstance(canvas, dict) else canvas
        inner += callout_p("nx-cyan", "quiz", "Canvas Submission", canvas_text)

    # Final warning callout
    warn = fc.get("finalWarning")
    if warn:
        inner += callout_p("nx-red", "error", "Final Reminder", warn)

    hdr  = header("final", "checklist", "Verify all requirements before submitting", accent)
    body = card(inner, accent)
    return section(hdr + body, "final checklist")


def render_grading_standards(data):
    gs = data.get("gradingStandards")
    if not gs:
        return ""
    accent = "#FFF700"
    inner = ""

    ql = gs.get("qualityLadder", {})
    if ql:
        inner += f'    <h2 class="nx-accent">The Quality Ladder</h2>\n'
        inner += f'    <p><strong>Assignment Objectives ({h(ql.get("assignmentObjectives","40%"))}):</strong> Did you complete all checkpoints with evidence?</p>\n'
        inner += f'    <p><strong>Technical Documentation ({h(ql.get("technicalDocumentation","40%"))}):</strong> Could another student reproduce your work?</p>\n'
        inner += f'    <p><strong>Professional Communication ({h(ql.get("professionalCommunication","20%"))}):</strong> Is this report client-ready?</p>\n\n'

    penalties = gs.get("penalties", [])
    if penalties:
        inner += f'    <h2 class="nx-accent">Penalties</h2>\n    <ul>\n'
        for p in penalties:
            if isinstance(p, str):
                inner += f'      <li>{h(p)}</li>\n'
            else:
                amount = h(p.get("amount", p.get("penalty", "")))
                desc   = h(p.get("description", p.get("condition", "")))
                inner += f'      <li><strong>{amount}</strong> {desc}</li>\n'
        inner += '    </ul>\n\n'

    auto_zero = gs.get("automaticZero", "")
    if auto_zero:
        inner += f'    <h2 class="nx-accent">Automatic Zero</h2>\n    <p>{h(auto_zero)}</p>\n\n'

    bonus = gs.get("bonus")
    if bonus:
        inner += f'    <h2 class="nx-accent">Bonus Opportunity</h2>\n    <p>{h(bonus)}</p>\n\n'

    rubric = gs.get("rubricCallout") or gs.get("fullRubricCallout")
    if not rubric:
        rd = gs.get("keyFlags", {}).get("rubricDocument") or gs.get("rubricDocument")
        if rd:
            rubric = rd.get("text", rd) if isinstance(rd, dict) else rd
    if rubric:
        rubric_text = rubric.get("text", rubric) if isinstance(rubric, dict) else rubric
        inner += callout_p("nx-purple", "description", "Full Rubric", rubric_text)

    hdr  = header("grading", "standards", "How This Assignment Is Graded", accent)
    body = card(inner, accent)
    return section(hdr + body, "grading standards")


def render_need_help(data):
    nh = data.get("needHelp", {})
    accent = "#4169E1"
    inner = ""

    channels = nh.get("channels", [])
    if channels:
        inner += '    <h2>Getting Help</h2>\n    <ul>\n'
        for ch in channels:
            name   = h(ch.get("name", ch.get("label", "")))
            detail = h(ch.get("detail", ""))
            inner += f'      <li><strong>{name}:</strong> {detail}</li>\n'
        inner += '    </ul>\n\n'

    late = nh.get("lateWorkPolicy")
    if late:
        inner += f'    <h2>Late Work Policy</h2>\n    <p>{h(late)}</p>\n\n'

    genai = nh.get("genAI")
    if genai:
        inner += f'    <h2>GenAI Policy</h2>\n'
        permitted = genai.get("permitted", [])
        if permitted:
            inner += '    <p><strong>You may use AI tools</strong> to:</p>\n    <ul>\n'
            inner += "".join(f'      <li>{h(i)}</li>\n' for i in permitted)
            inner += '    </ul>\n'
        prohibited = genai.get("prohibited", [])
        if prohibited:
            inner += '    <p><strong>You may NOT use AI tools</strong> to:</p>\n    <ul>\n'
            inner += "".join(f'      <li>{h(i)}</li>\n' for i in prohibited)
            inner += '    </ul>\n'
        principle = genai.get("principle")
        if principle:
            inner += f'    <p><em>{h(principle)}</em></p>\n\n'

    # Academic integrity
    inner += (
        '    <h2>Academic Integrity</h2>\n'
        '    <p>This assignment must be your own work. You may reference the textbook '
        'and other cited sources. You may NOT copy from others, use AI to complete '
        'the work, or share your work with classmates.</p>\n\n'
    )

    # Custom callouts
    for c_block in nh.get("customCallouts", []):
        ct    = c_block.get("type", "tip")
        cfg   = CALLOUT_MAP.get(ct, ("nx-cyan", "lightbulb", ""))
        css_cls, default_icon, default_title = cfg
        icon  = c_block.get("icon", default_icon)
        title = c_block.get("title", default_title)
        text  = c_block.get("text", "")
        inner += callout_p(css_cls, icon, title, text)

    # What's next
    whats_next = nh.get("whatsNext")
    if whats_next:
        wn_text = whats_next.get("text", whats_next) if isinstance(whats_next, dict) else whats_next
        inner += callout_p("nx-blue", "arrow_forward", "What&#8217;s Next", wn_text)

    hdr  = header("need", "help?", "Support resources and course policies", accent)
    body = card(inner, accent)
    return section(hdr + body, "need help")


# ── Document shell ────────────────────────────────────────────────────────────

def render(data):
    meta  = data["meta"]
    title = meta["title"]
    lab_id_parts = meta["labId"].split("_")
    lab_num = ".".join(lab_id_parts)
    is_engagement = meta.get("labType") == "engagement"

    # Render sections
    nav_src, intro_html = render_intro(data)

    yah_html        = render_you_already_have(data) if is_engagement else ""
    time_html       = render_time_guide(data)
    checkpoints_html = "".join(render_checkpoint(cp) for cp in data.get("checkpoints", []))
    purple_html     = render_purple_team(data)
    checklist_html  = render_final_checklist(data)
    grading_html    = render_grading_standards(data) if is_engagement else ""
    help_html       = render_need_help(data)

    body_parts = [
        intro_html,
        yah_html,
        time_html,
        checkpoints_html,
        purple_html,
        checklist_html,
        grading_html,
        help_html,
    ]

    body = "\n".join(p for p in body_parts if p)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lab {lab_num} &#8212; {title}</title>
  <link rel="stylesheet" href="../../site.css">
</head>
<body>
<script src="{nav_src}"></script>
<h1 class="nx-sr-only">Lab {lab_num} &#8212; {title}</h1>

{body}
</body>
</html>"""


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: render_lab.py <lab_COMPLETE.json> [output.html]")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    with open(json_path) as f:
        data = json.load(f)

    html = render(data)

    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
        out_path.write_text(html)
        print(f"Written: {out_path}")
    else:
        print(html)
