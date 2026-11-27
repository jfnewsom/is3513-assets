#!/usr/bin/env python3
"""build_search_index.py - site search index for the nav bar search box.

Reads the RENDERED pages (pages/**/*.html) so the index always matches what
students see, and writes search-index.json at the repo root:
    [{"t": title shown in results, "u": url from the site root, "x": page text}, ...]
Tabbed lab pages get one entry per tab, with a #tab link, so a result opens
the right checkpoint. Other pages get one entry each.
nav.js loads the file only when someone clicks into the search box.
Run by render_all.sh after every render.
"""
import glob
import html
import json
import re

MAX_TEXT = 12000          # characters of text kept per entry
SKIP = ("pages/labs/json", "pages/support/json", "pages/reading/json", "pages/exams/json")


def text_of(fragment):
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<pre\b", " <pre", fragment)
    t = re.sub(r"<[^>]+>", " ", fragment)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def page_title(src):
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    t = html.unescape(m.group(1)).strip() if m else ""
    return re.sub(r"\s*[|–-]\s*IS3513\s*$", "", t)


def entries_for(path):
    src = open(path, encoding="utf-8").read()
    title = page_title(src)
    if 'class="nx-tabbed"' in src:
        tabs = dict(re.findall(r'<a class="nx-tb-tab[^"]*" role="tab" href="#[a-z0-9]+" data-tab="([a-z0-9]+)"[^>]*>([^<]+)</a>', src))
        out = []
        for m in re.finditer(r'<section class="nx-tb-panel[^"]*" id="p-([a-z0-9]+)".*?(?=<section class="nx-tb-panel|</main>)', src, re.S):
            tid, frag = m.group(1), m.group(0)
            sub = re.search(r'<div class="nx-sub">(.*?)</div>', frag, re.S)
            label = tabs.get(tid, tid)
            if tid.startswith("cp") and sub:
                label = f"{label}: {text_of(sub.group(1))}"
            out.append({"t": f"{title} › {label}", "u": f"{path}#{tid}", "x": text_of(frag)[:MAX_TEXT]})
        return out
    body = re.search(r"<body\b.*?</body>", src, re.S)
    return [{"t": title, "u": path, "x": text_of(body.group(0) if body else src)[:MAX_TEXT]}]


def main():
    index = []
    for path in sorted(glob.glob("pages/**/*.html", recursive=True)):
        if path.startswith(SKIP):
            continue
        index.extend(e for e in entries_for(path) if e["x"])
    with open("search-index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    print(f"search-index.json: {len(index)} entries")


if __name__ == "__main__":
    main()
