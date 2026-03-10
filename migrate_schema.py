#!/usr/bin/env python3
"""
migrate_schema.py — Normalize all IS3513 lab JSONs to canonical v2 schema.

Usage:
    python3 migrate_schema.py <input_dir> <output_dir>
    python3 migrate_schema.py migrated/ normalized/   # default

Changes made (all lossless — no content is dropped, only reshaped):
  meta:
    - Remove _gap, screenshotPrefix, screenshotNote, subtitle (orphan fields)
  intro.clientContext:
    - Normalize flat contactName/contactTitle to contacts[] array
  checkpoints[].content[type=steps].steps[]:
    - Remove block_note, part, role, embeddedTable (unused by renderer)
  checkpoints[].content[type=callout] characterQuote:
    - Normalize role -> title; text -> quote
  checkpoints[].content[type=table]:
    - Normalize headers -> columns
  purpleTeam.redTeam / blueTeam:
    - Normalize content (flat string) -> items [{label, text}]
  youAlreadyHave:
    - Normalize weeks[] + newThisWeek[] -> sections[]
    - Normalize callout (single dict) + tipCallout -> callouts[]
    - Normalize section items: {text, badge} dicts -> strings (badge -> section.badge)
    - Normalize sections[].label -> sections[].title
  gradingStandards.penalties[]:
    - Normalize all dict shapes and plain strings -> {penalty, condition}
  finalChecklist.sections[]:
    - Normalize label -> title
  finalChecklist.canvasSubmission:
    - Normalize plain string -> {text: string}
  finalChecklist.screenshotTable[]:
    - Normalize filename -> file
  needHelp.channels[]:
    - Normalize name -> label
  needHelp.whatsNext / whatNext:
    - Normalize plain string -> {text: string}; canonicalize key to whatsNext
"""

import json
import os
import sys
import copy
from pathlib import Path


# ── Helpers ────────────────────────────────────────────────────────────────────

def migrate_meta(meta):
    """Remove orphan fields; keep canonical set."""
    REMOVE = {'_gap', 'screenshotPrefix', 'screenshotNote', 'subtitle'}
    return {k: v for k, v in meta.items() if k not in REMOVE}


def migrate_client_context(cc):
    """Normalize flat contactName/contactTitle -> contacts[]."""
    if not isinstance(cc, dict):
        return cc
    cc = dict(cc)
    flat_name  = cc.pop('contactName', None)
    flat_title = cc.pop('contactTitle', None)
    if flat_name and 'contacts' not in cc:
        cc['contacts'] = [{'name': flat_name, 'title': flat_title or '', 'quote': ''}]
    return cc


def migrate_step(step):
    """Remove orphan step-level fields unused by renderer."""
    REMOVE = {'block_note', 'part', 'role', 'embeddedTable'}
    return {k: v for k, v in step.items() if k not in REMOVE}


def migrate_callout(item):
    """Normalize callout items."""
    item = dict(item)
    ct = item.get('calloutType', '')

    # characterQuote: role -> title, text -> quote
    if ct == 'characterQuote':
        if 'role' in item and 'title' not in item:
            item['title'] = item.pop('role')
        elif 'role' in item:
            item.pop('role')
        if 'text' in item and 'quote' not in item:
            item['quote'] = item.pop('text')
        elif 'text' in item:
            item.pop('text')

    # table-type callout: normalize headers -> columns
    if item.get('type') == 'table':
        if 'headers' in item and 'columns' not in item:
            item['columns'] = item.pop('headers')
        elif 'headers' in item:
            item.pop('headers')

    return item


def migrate_content_item(item):
    """Route content items to their specific migrators."""
    t = item.get('type', '')
    if t == 'steps':
        item = dict(item)
        item['steps'] = [migrate_step(s) for s in item.get('steps', [])]
        return item
    elif t == 'callout':
        return migrate_callout(item)
    elif t == 'table':
        item = dict(item)
        if 'headers' in item and 'columns' not in item:
            item['columns'] = item.pop('headers')
        elif 'headers' in item:
            item.pop('headers')
        return item
    return item


def migrate_checkpoint(cp):
    """Migrate a single checkpoint."""
    cp = dict(cp)
    cp['content'] = [migrate_content_item(item) for item in cp.get('content', [])]
    return cp


def migrate_purple_team_side(side):
    """Normalize purpleTeam.redTeam / blueTeam: content string -> items[]."""
    if not isinstance(side, dict):
        return side
    side = dict(side)
    if 'content' in side and 'items' not in side:
        # Single flat-string content — wrap as one item
        raw = side.pop('content')
        side['type'] = 'items'
        side['items'] = [{'label': side.get('label', ''), 'text': raw}]
    elif 'content' in side:
        side.pop('content')
    return side


def migrate_purple_team(pt):
    if not isinstance(pt, dict):
        return pt
    pt = dict(pt)
    if 'redTeam' in pt:
        pt['redTeam'] = migrate_purple_team_side(pt['redTeam'])
    if 'blueTeam' in pt:
        pt['blueTeam'] = migrate_purple_team_side(pt['blueTeam'])
    return pt


def normalize_yah_item(item):
    """Normalize a youAlreadyHave section item to a plain string."""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return item.get('text', str(item))
    return str(item)


def migrate_you_already_have(yah):
    """
    Normalize youAlreadyHave to canonical shape:
      { intro, sections[{title, badge, items[string]}], callouts[] }
    Absorbs: weeks[], newThisWeek[], callout (single), tipCallout
    """
    if not isinstance(yah, dict):
        return yah
    yah = dict(yah)

    # ── Build canonical sections[] ────────────────────────────────────────────
    # Strategy: if sections[] is already present and populated, keep it
    # (it's the richer structure). Weeks/newThisWeek are parallel data.
    # After normalization, only sections[] remains.

    existing_sections = yah.get('sections', [])
    weeks             = yah.get('weeks', [])
    new_this_week     = yah.get('newThisWeek', [])

    if existing_sections:
        # Normalize each section
        canonical_sections = []
        for sec in existing_sections:
            sec = dict(sec)
            # Normalize label -> title
            if 'label' in sec and 'title' not in sec:
                sec['title'] = sec.pop('label')
            elif 'label' in sec:
                sec.pop('label')
            # Normalize items to plain strings
            sec['items'] = [normalize_yah_item(i) for i in sec.get('items', [])]
            canonical_sections.append(sec)
    else:
        # Build sections from weeks + newThisWeek
        canonical_sections = []
        for wk in weeks:
            wk = dict(wk)
            title = wk.get('label', '')
            items = [normalize_yah_item(i) for i in wk.get('items', [])]
            canonical_sections.append({'title': title, 'badge': None, 'items': items})
        if new_this_week:
            items = [normalize_yah_item(i) for i in new_this_week]
            canonical_sections.append({'title': 'NEW This Week', 'badge': 'NEW', 'items': items})

    yah['sections'] = canonical_sections

    # ── Build canonical callouts[] ────────────────────────────────────────────
    existing_callouts = yah.get('callouts', [])
    single_callout    = yah.get('callout')
    tip_callout       = yah.get('tipCallout')

    canonical_callouts = list(existing_callouts)
    if single_callout and isinstance(single_callout, dict):
        canonical_callouts.append(single_callout)
    if tip_callout and isinstance(tip_callout, dict):
        canonical_callouts.append(tip_callout)

    if canonical_callouts:
        yah['callouts'] = canonical_callouts
    elif 'callouts' in yah:
        pass  # keep empty list

    # ── Remove absorbed keys ──────────────────────────────────────────────────
    for k in ('weeks', 'newThisWeek', 'callout', 'tipCallout', 'headerSvg'):
        yah.pop(k, None)

    return yah


def normalize_penalty(p):
    """Normalize a gradingStandards penalty to {penalty, condition}."""
    if isinstance(p, str):
        # Plain string — best-effort split on first space after amount
        parts = p.split(' ', 1)
        if len(parts) == 2 and parts[0].endswith('%'):
            return {'penalty': parts[0], 'condition': parts[1]}
        return {'penalty': '', 'condition': p}
    if isinstance(p, dict):
        # Various dict shapes -> canonical
        penalty   = p.get('penalty') or p.get('amount') or ''
        condition = (p.get('condition')
                     or p.get('description')
                     or p.get('trigger')
                     or '')
        return {'penalty': penalty, 'condition': condition}
    return {'penalty': '', 'condition': str(p)}


def migrate_grading_standards(gs):
    if not isinstance(gs, dict):
        return gs
    gs = dict(gs)
    if 'penalties' in gs:
        gs['penalties'] = [normalize_penalty(p) for p in gs['penalties']]
    return gs


def migrate_final_checklist(fc):
    if not isinstance(fc, dict):
        return fc
    fc = dict(fc)

    # sections[].label -> title
    canonical_sections = []
    for sec in fc.get('sections', []):
        sec = dict(sec)
        if 'label' in sec and 'title' not in sec:
            sec['title'] = sec.pop('label')
        elif 'label' in sec:
            sec.pop('label')
        sec.pop('_gap', None)
        canonical_sections.append(sec)
    fc['sections'] = canonical_sections

    # screenshotTable[].filename -> file
    tbl = fc.get('screenshotTable')
    if tbl:
        canonical_tbl = []
        for row in tbl:
            if row is None:
                continue
            row = dict(row)
            if 'filename' in row and 'file' not in row:
                row['file'] = row.pop('filename')
            elif 'filename' in row:
                row.pop('filename')
            canonical_tbl.append(row)
        fc['screenshotTable'] = canonical_tbl

    # canvasSubmission: string -> {text}
    cs = fc.get('canvasSubmission')
    if isinstance(cs, str):
        fc['canvasSubmission'] = {'text': cs}

    return fc


def migrate_need_help(nh):
    if not isinstance(nh, dict):
        return nh
    nh = dict(nh)

    # channels[].name -> label
    canonical_channels = []
    for ch in nh.get('channels', []):
        ch = dict(ch)
        if 'name' in ch and 'label' not in ch:
            ch['label'] = ch.pop('name')
        elif 'name' in ch:
            ch.pop('name')
        canonical_channels.append(ch)
    nh['channels'] = canonical_channels

    # whatsNext / whatNext: string -> {text}; canonicalize key
    wn = nh.pop('whatNext', None) or nh.pop('whatsNext', None)
    if wn is not None:
        if isinstance(wn, str):
            wn = {'text': wn}
        nh['whatsNext'] = wn

    return nh


def migrate_lab(data):
    """Apply all migrations to a lab dict. Returns new dict (original unchanged)."""
    data = copy.deepcopy(data)

    # meta
    if 'meta' in data:
        data['meta'] = migrate_meta(data['meta'])

    # intro
    intro = data.get('intro', {})
    if isinstance(intro, dict):
        if 'clientContext' in intro and intro['clientContext']:
            intro['clientContext'] = migrate_client_context(intro['clientContext'])
        data['intro'] = intro

    # timeGuide — no changes needed, already consistent

    # checkpoints
    data['checkpoints'] = [migrate_checkpoint(cp) for cp in data.get('checkpoints', [])]

    # purpleTeam
    if 'purpleTeam' in data:
        data['purpleTeam'] = migrate_purple_team(data['purpleTeam'])

    # youAlreadyHave (X.3 only)
    if 'youAlreadyHave' in data:
        data['youAlreadyHave'] = migrate_you_already_have(data['youAlreadyHave'])

    # gradingStandards (X.3 only)
    if 'gradingStandards' in data:
        data['gradingStandards'] = migrate_grading_standards(data['gradingStandards'])

    # finalChecklist
    if 'finalChecklist' in data:
        data['finalChecklist'] = migrate_final_checklist(data['finalChecklist'])

    # needHelp
    if 'needHelp' in data:
        data['needHelp'] = migrate_need_help(data['needHelp'])

    return data


# ── Validation ─────────────────────────────────────────────────────────────────

def validate_lab(data, lab_id):
    """Run post-migration checks. Returns list of (severity, message)."""
    issues = []

    def warn(msg): issues.append(('WARN', msg))
    def err(msg):  issues.append(('ERR',  msg))

    meta = data.get('meta', {})

    # meta required fields
    for k in ('labId', 'title', 'labType', 'module', 'chapters', 'headerSvg', 'screenshotStart'):
        if not meta.get(k) and meta.get(k) != 0:
            warn(f"meta.{k} missing or null")

    # orphan meta fields should be gone
    for k in ('_gap', 'screenshotPrefix', 'screenshotNote'):
        if k in meta:
            err(f"meta.{k} should have been removed")

    # checkpoints
    for i, cp in enumerate(data.get('checkpoints', [])):
        for j, item in enumerate(cp.get('content', [])):
            t = item.get('type')
            if t == 'steps':
                for bad in ('block_note', 'part', 'embeddedTable'):
                    for step in item.get('steps', []):
                        if bad in step:
                            err(f"CP{i+1} step has orphan field '{bad}'")
            if t == 'callout':
                ct = item.get('calloutType', '')
                if ct == 'characterQuote':
                    if 'role' in item:
                        err(f"CP{i+1} characterQuote still has 'role' (should be 'title')")
                    if 'text' in item and 'quote' not in item:
                        err(f"CP{i+1} characterQuote still has 'text' (should be 'quote')")

    # purpleTeam — no content keys should remain
    pt = data.get('purpleTeam', {})
    for side_key in ('redTeam', 'blueTeam'):
        side = pt.get(side_key, {})
        if isinstance(side, dict) and 'content' in side and 'items' not in side:
            err(f"purpleTeam.{side_key} still has flat 'content' without items")

    # youAlreadyHave (engagement labs)
    yah = data.get('youAlreadyHave', {})
    if yah:
        for bad in ('weeks', 'newThisWeek', 'callout', 'tipCallout', 'headerSvg'):
            if bad in yah:
                err(f"youAlreadyHave.{bad} should have been removed")
        for sec in yah.get('sections', []):
            if 'label' in sec:
                err(f"youAlreadyHave section still has 'label' key (should be 'title')")
            for item in sec.get('items', []):
                if not isinstance(item, str):
                    err(f"youAlreadyHave section item is not a string: {repr(item)[:60]}")

    # gradingStandards penalties
    for p in data.get('gradingStandards', {}).get('penalties', []):
        if not isinstance(p, dict):
            err(f"gradingStandards penalty is not a dict: {repr(p)[:60]}")
        elif 'penalty' not in p or 'condition' not in p:
            err(f"gradingStandards penalty missing penalty/condition keys: {p}")

    # finalChecklist
    fc = data.get('finalChecklist', {})
    for sec in fc.get('sections', []):
        if 'label' in sec:
            err(f"finalChecklist section still has 'label' key")
    cs = fc.get('canvasSubmission')
    if cs is not None and not isinstance(cs, dict):
        err(f"finalChecklist.canvasSubmission is not a dict: {repr(cs)[:40]}")

    # needHelp
    nh = data.get('needHelp', {})
    for ch in nh.get('channels', []):
        if 'name' in ch and 'label' not in ch:
            err(f"needHelp channel still has 'name' key (should be 'label')")
    if 'whatNext' in nh:
        err(f"needHelp still has 'whatNext' key (should be 'whatsNext')")
    wn = nh.get('whatsNext')
    if wn is not None and not isinstance(wn, dict):
        err(f"needHelp.whatsNext is not a dict: {repr(wn)[:40]}")

    return issues


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    in_dir  = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('migrated')
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('normalized')
    out_dir.mkdir(exist_ok=True)

    files = sorted(in_dir.glob('*_COMPLETE.json'))
    if not files:
        print(f"No *_COMPLETE.json files found in {in_dir}")
        sys.exit(1)

    print(f"Migrating {len(files)} labs from {in_dir}/ -> {out_dir}/\n")

    total_errs = 0
    total_warns = 0

    for path in files:
        lab_id = path.stem.replace('_COMPLETE','').replace('_','.')
        with open(path) as f:
            original = json.load(f)

        migrated = migrate_lab(original)
        issues   = validate_lab(migrated, lab_id)

        errs  = [m for s,m in issues if s == 'ERR']
        warns = [m for s,m in issues if s == 'WARN']
        total_errs  += len(errs)
        total_warns += len(warns)

        status = "✓" if not errs else "✗"
        print(f"  {status} {lab_id}  {migrated['meta'].get('title','?')}")
        for m in errs:
            print(f"      ERR  {m}")
        for m in warns:
            print(f"      warn {m}")

        out_path = out_dir / path.name
        with open(out_path, 'w') as f:
            json.dump(migrated, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(files)} files written to {out_dir}/")
    print(f"  Errors: {total_errs}   Warnings: {total_warns}")
    if total_errs:
        print("  ⚠  Errors indicate incomplete migration — review above.")
    else:
        print("  ✓  All files passed validation.")


if __name__ == '__main__':
    main()
