/**
 * nav.js — IS3513 Information Assurance & Security
 * Top horizontal navigation bar with dropdown menus.
 *
 * Behavior is determined by where the page is loaded and what context= is set:
 *
 *   Direct open (not in iframe)          → full nav (all dropdowns)
 *   /pages/support/* in Canvas iframe    → slim nav (Course + NEXUS + Reading)
 *   Other paths in Canvas iframe         → no nav (assignment iframes)
 *   ?context=lab (anywhere)              → lab reference sidebar only
 *
 * The slim-nav opt-in is path-based: any page under /pages/support/ loaded
 * inside an iframe automatically renders the slim nav. No ?context=support
 * param required in the iframe src or on internal links — students can
 * click through Home.html → StartHere.html → Grading_Info.html and the
 * slim nav persists as the iframe navigates between support pages.
 */

(function () {
  'use strict';

  /* ── Context detection ──────────────────────────────────── */
  const inIframe = window.self !== window.top;
  const params   = new URLSearchParams(window.location.search);
  let   ctx      = params.get('context');

  // Path-based slim-nav opt-in: support pages in an iframe get the slim
  // nav automatically. This makes Canvas embedding zero-config — no query
  // params needed in the iframe src or on inline content links.
  if (inIframe && !ctx && window.location.pathname.includes('/pages/support/')) {
    ctx = 'support';
  }

  // Anything else in an iframe (labs, readings, exams) → silent exit.
  if (inIframe && ctx !== 'support' && ctx !== 'lab') return;

  const showFull = !inIframe && ctx !== 'lab';   // direct open, full menu
  const isLab    = ctx === 'lab';

  /* ── Base URLs ──────────────────────────────────────────── */
  const BASE = 'https://jfnewsom.github.io/is3513-assets';
  const S    = BASE + '/pages/support';
  const L    = BASE + '/pages/labs';
  const R    = BASE + '/pages/reading';

  /* ── Fonts ──────────────────────────────────────────────── */
  if (!document.querySelector('link[href*="Roboto+Slab"]') &&
      !document.querySelector('link[href*="fonts.googleapis"]')) {
    const f = document.createElement('link');
    f.rel  = 'stylesheet';
    f.href = 'https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&family=Roboto:wght@400;500;700&display=swap';
    document.head.prepend(f);
  }

  /* ── Styles ─────────────────────────────────────────────── */
  const css = `
    #is3513-nav {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 9999;
      background: #0d0d0d;
      border-bottom: 1px solid #1e1e1e;
      font-family: 'Roboto', sans-serif;
      font-size: 13px;
      user-select: none;
    }
    #is3513-nav a { text-decoration: none; }

    /* Push body down by nav height; nx-page margin adds scrollable breathing room */
    body    { padding-top: 42px; }
    .nx-page { margin-top: 40px; }

    #is3513-nav .nav-inner {
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 0 20px;
      height: 42px;
    }

    /* Logo */
    #is3513-nav .nav-logo {
      display: flex;
      align-items: center;
      padding-right: 16px;
      margin-right: 6px;
      border-right: 1px solid #222;
      flex-shrink: 0;
      white-space: nowrap;
    }
    #is3513-nav .nav-logo-label {
      font-family: 'Roboto Slab', serif;
      font-size: 13px;
      font-weight: 700;
      color: #5865F2;
      letter-spacing: 0.03em;
    }
    #is3513-nav .nav-logo:hover .nav-logo-label { color: #7B8BF5; }

    /* Nav menu */
    #is3513-nav .nav-menu {
      display: flex;
      align-items: center;
      gap: 2px;
      flex: 1;
    }
    #is3513-nav .nav-item { position: relative; }
    #is3513-nav .nav-trigger {
      display: flex;
      align-items: center;
      gap: 5px;
      color: #778087;
      padding: 0 10px;
      height: 42px;
      cursor: pointer;
      font-weight: 500;
      white-space: nowrap;
      transition: color 0.12s, background 0.12s;
      border-radius: 3px;
    }
    #is3513-nav .nav-trigger:hover {
      color: #F5F5F5;
      background: rgba(255,255,255,0.04);
    }
    #is3513-nav .nav-caret {
      font-size: 8px;
      opacity: 0.35;
      transition: transform 0.12s, opacity 0.12s;
    }
    #is3513-nav .nav-item:hover .nav-caret {
      transform: rotate(180deg);
      opacity: 0.7;
    }

    /* Dropdown panel */
    #is3513-nav .nav-dropdown {
      display: none;
      position: absolute;
      top: calc(100% + 1px);
      left: 0;
      min-width: 220px;
      background: #111;
      border: 1px solid #222;
      border-top: 2px solid #7B68EE;
      padding: 6px 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    #is3513-nav .nav-item:hover .nav-dropdown { display: block; }

    #is3513-nav .nav-dropdown a {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 16px;
      color: #778087;
      font-size: 13px;
      transition: color 0.1s, background 0.1s;
      line-height: 1.3;
    }
    #is3513-nav .nav-dropdown a:hover {
      color: #F5F5F5;
      background: rgba(255,255,255,0.04);
    }
    #is3513-nav .nav-dropdown a:hover .drop-dot { opacity: 1; }

    #is3513-nav .drop-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      flex-shrink: 0;
      opacity: 0.6;
    }
    #is3513-nav .drop-label {
      font-family: 'Roboto Slab', serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #7B68EE;
      padding: 8px 16px 3px 16px;
    }
    #is3513-nav .drop-divider {
      border: none;
      border-top: 1px solid #1a1a1a;
      margin: 4px 0;
    }
    #is3513-nav .drop-sub {
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: #7B68EE;
      padding: 6px 16px 2px 16px;
    }

    /* Dot colors */
    #is3513-nav .dd-green  { background: #00D26A; }
    #is3513-nav .dd-yellow { background: #FFF700; }
    #is3513-nav .dd-cyan   { background: #00BCD4; }
    #is3513-nav .dd-purple { background: #7B68EE; }
    #is3513-nav .dd-orange { background: #FF9F1C; }

    /* Site search (2026-11-27) */
    #is3513-nav .nav-search { position: relative; margin-left: auto; margin-right: 10px; flex-shrink: 1; min-width: 120px; }
    #is3513-nav .nav-search__input { width: 220px; max-width: 100%; box-sizing: border-box; background: #1a1f2e; color: #F5F5F5;
      border: 1px solid #2f3646; border-radius: 3px; padding: 5px 10px; font: 13px 'Roboto', sans-serif; }
    #is3513-nav .nav-search__input:focus { outline: none; border-color: #4169E1; }
    #is3513-nav .nav-search__results { position: absolute; right: 0; top: calc(100% + 6px); width: min(520px, 92vw); max-height: 70vh;
      overflow-y: auto; background: #0d0d0d; border: 1px solid #2f3646; border-radius: 4px; box-shadow: 0 8px 24px rgba(0,0,0,.5); z-index: 10000; }
    #is3513-nav .nav-search__item { display: block; padding: 9px 12px; border-bottom: 1px solid #1e1e1e; color: #C9CED6; }
    #is3513-nav .nav-search__item:hover, #is3513-nav .nav-search__item.is-active { background: #1a1f2e; }
    #is3513-nav .nav-search__title { display: block; color: #ffffff; font-weight: 700; font-size: 13px; margin-bottom: 3px; }
    #is3513-nav .nav-search__snip { display: block; font-size: 12px; line-height: 1.45; color: #9aa3b2; }
    #is3513-nav .nav-search__snip mark { background: #FEC618; color: #000; padding: 0 2px; border-radius: 2px; }
    #is3513-nav .nav-search__none { padding: 10px 12px; font-size: 12px; color: #9aa3b2; }

    /* Discord button */
    #is3513-nav .nav-discord {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #5865F2;
      color: #ffffff !important;
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      white-space: nowrap;
      transition: background 0.12s;
      flex-shrink: 0;
      border-radius: 3px;
    }
    #is3513-nav .nav-discord:hover { background: #4752C4; }

    /* ── Lab reference sidebar (context=lab) ── */
    #is3513-nav .lab-ref-nav {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 0 20px;
      height: 42px;
      font-size: 12px;
      font-weight: 500;
    }
    #is3513-nav .lab-ref-nav a {
      color: #778087;
      transition: color 0.12s;
    }
    #is3513-nav .lab-ref-nav a:hover { color: #F5F5F5; }
    #is3513-nav .lab-ref-label {
      font-family: 'Roboto Slab', serif;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #5865F2;
      margin-right: 4px;
    }
    #is3513-nav .lab-ref-sep { color: #333; }

    /* ── Injected footer ── */
    .site-footer {
      background: #f8f9fa;
      border-top: 1px solid #e0e4ef;
      padding: 24px 40px;
      text-align: center;
      font-family: 'Roboto', sans-serif;
    }
    .site-footer__logo {
      height: 36px;
      margin-bottom: 12px;
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
    .site-footer__citation {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 8px;
    }
    .site-footer__citation-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #4169E1;
      background: rgba(65,105,225,0.08);
      padding: 2px 8px;
      border-radius: 3px;
    }
    .site-footer__citation-text {
      font-size: 13px;
      color: #444;
    }
    .site-footer__copyright {
      font-size: 11px;
      color: #888;
      margin-top: 4px;
    }
  `;

  /* ── Helper: dropdown link ──────────────────────────────── */
  function link(label, url, color, external) {
    const target = external ? ' target="_blank" rel="noopener"' : '';
    return `<a href="${url}"${target}><span class="drop-dot ${color}"></span>${label}</a>`;
  }

  /* ── Course dropdown ────────────────────────────────────── */
  const courseDropdown = `
    <div class="nav-item">
      <div class="nav-trigger">Course <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Getting Started</div>
        ${link('Start Here',              S + '/StartHere.html',              'dd-green')}
        ${link('Course Schedule',         S + '/Course_Schedule.html',        'dd-green')}
        ${link('Textbook Info',           S + '/Textbook.html',               'dd-green')}
        <div class="drop-label">Policies</div>
        ${link('Grading Info',            S + '/Grading_Info.html',           'dd-yellow')}
        ${link('GenAI Policy',            S + '/GenAI_Policy.html',           'dd-yellow')}
        ${link('How to Get Help',         S + '/How_To_Get_Help.html',        'dd-yellow')}
        <div class="drop-label">Reference</div>
        ${link('Engagement Packet Guide', S + '/Engagement_Packet_Guide.html','dd-cyan')}
        ${link('Scoring Your Findings',   S + '/Scoring_Guide.html',           'dd-cyan')}
        ${link('Screenshot Requirements', S + '/Screenshot_Requirements.html','dd-cyan')}
        ${link('Citations',               S + '/Citations.html',              'dd-cyan')}
      </div>
    </div>`;

  /* ── NEXUS dropdown ─────────────────────────────────────── */
  const nexusDropdown = `
    <div class="nav-item">
      <div class="nav-trigger">NEXUS <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">NEXUS World</div>
        ${link('NEXUS Security', S + '/NEXUS_Security.html', 'dd-purple')}
        ${link('Meet the Team',  S + '/Meet_The_Team.html',  'dd-purple')}
        ${link('Our Clients',    S + '/Our_Clients.html',    'dd-purple')}
      </div>
    </div>`;

  /* ── Modules dropdown ───────────────────────────────────── */
  const modulesDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Modules <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-sub">Module 1 &mdash; Reconnaissance</div>
        ${link('Overview',        S + '/Module_1.html',                   'dd-purple')}
        ${link('Study Worksheet', S + '/module-1-study-worksheet.html',   'dd-purple')}
        <div class="drop-sub">Module 2 &mdash; Cryptography &amp; Auth</div>
        ${link('Overview',        S + '/Module_2.html',                   'dd-purple')}
        ${link('Study Worksheet', S + '/module-2-study-worksheet.html',   'dd-purple')}
        <div class="drop-sub">Module 3 &mdash; Networks &amp; Cloud</div>
        ${link('Overview',        S + '/Module_3.html',                   'dd-purple')}
        ${link('Study Worksheet', S + '/module-3-study-worksheet.html',   'dd-purple')}
        <div class="drop-sub">Module 4 &mdash; Threats &amp; Attacks</div>
        ${link('Overview',        S + '/Module_4.html',                   'dd-purple')}
        ${link('Study Worksheet', S + '/module-4-study-worksheet.html',   'dd-purple')}
        <div class="drop-sub">Module 5 &mdash; Risk &amp; Infrastructure</div>
        ${link('Overview',        S + '/Module_5.html',                   'dd-purple')}
        ${link('Study Worksheet', S + '/module-5-study-worksheet.html',   'dd-purple')}
      </div>
    </div>` : '';

  /* ── Labs dropdown ──────────────────────────────────────── */
  const labsDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Labs <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-sub">Module 1 &mdash; Reconnaissance</div>
        ${link('Lab 1.1 &mdash; Kali Environment Setup',        L + '/Lab1_1_Kali_Environment_Setup.html',                    'dd-cyan')}
        ${link('Lab 1.2 &mdash; Reconnaissance Tools',          L + '/Lab1_2_Reconnaissance_Tool_Exploration.html',            'dd-cyan')}
        ${link('EP 1 &mdash; Brazos Engagement',                L + '/Lab1_3_Brazos_Financial_Reconnaissance_Engagement.html', 'dd-cyan')}
        <div class="drop-sub">Module 2 &mdash; Cryptography &amp; Auth</div>
        ${link('Lab 2.1 &mdash; Cryptographic Foundations',     L + '/Lab2_1_Cryptographic_Foundations.html',                  'dd-cyan')}
        ${link('Lab 2.2 &mdash; Authentication Systems',        L + '/Lab2_2_Authentication_Systems.html',                     'dd-cyan')}
        ${link('EP 2 &mdash; Gulf Coast Engagement',            L + '/Lab2_3_Gulf_Coast_Certificate_Remediation.html',         'dd-cyan')}
        <div class="drop-sub">Module 3 &mdash; Networks &amp; Cloud</div>
        ${link('Lab 3.1 &mdash; Network Addressing',            L + '/Lab3_1_Network_Addressing_Fundamentals.html',            'dd-cyan')}
        ${link('Lab 3.2 &mdash; Protocol Analysis',             L + '/Lab3_2_Protocol_Analysis_Tools.html',                    'dd-cyan')}
        ${link('EP 3 &mdash; Network Analysis Engagement',      L + '/Lab3_3_Network_Analysis_Engagement.html',                'dd-cyan')}
        <div class="drop-sub">Module 4 &mdash; Threats &amp; Attacks</div>
        ${link('Lab 4.1 &mdash; Windows Password Cracking',     L + '/Lab4_1_Windows_Password_Cracking.html',                  'dd-cyan')}
        ${link('Lab 4.2 &mdash; Linux Password Cracking',       L + '/Lab4_2_Linux_Password_Cracking.html',                    'dd-cyan')}
        ${link('EP 4 &mdash; Password Security Assessment',     L + '/Lab4_3_Password_Security_Assessment.html',               'dd-cyan')}
        <div class="drop-sub">Module 5 &mdash; Risk &amp; Infrastructure</div>
        ${link('Lab 5.1 &mdash; Vulnerability Assessment &amp; Risk Analysis', L + '/Lab5_1_Vulnerability_Assessment_Risk_Analysis.html',    'dd-cyan')}
        ${link('EP 5 &mdash; LoneStar Engagement',                           L + '/Lab5_2_Risk_Vulnerability_Assessment_Report.html',      'dd-cyan')}
      </div>
    </div>` : '';

  /* ── Reading dropdown ───────────────────────────────────── */
  const readingDropdown = `
    <div class="nav-item">
      <div class="nav-trigger">Reading <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-sub">Module 1 &mdash; Ch. 1&ndash;2</div>
        ${link('Chapter 1 &mdash; Intro &amp; Security Trends',         R + '/CH01-Reading.html', 'dd-yellow')}
        ${link('Chapter 2 &mdash; General Security Concepts',           R + '/CH02-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 2 &mdash; Ch. 6 &amp; 11</div>
        ${link('Chapter 6 &mdash; Applied Cryptography',                R + '/CH06-Reading.html', 'dd-yellow')}
        ${link('Chapter 11 &mdash; Authentication &amp; Remote Access', R + '/CH11-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 3 &mdash; Ch. 9, 13 &amp; 18</div>
        ${link('Chapter 9 &mdash; Network Fundamentals',                R + '/CH09-Reading.html', 'dd-yellow')}
        ${link('Chapter 13 &mdash; IDS &amp; Network Security',         R + '/CH13-Reading.html', 'dd-yellow')}
        ${link('Chapter 18 &mdash; Cloud Computing',                    R + '/CH18-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 4 &mdash; Ch. 15 &amp; 16</div>
        ${link('Chapter 15 &mdash; Types of Attacks',                   R + '/CH15-Reading.html', 'dd-yellow')}
        ${link('Chapter 16 &mdash; Security Tools &amp; Techniques',    R + '/CH16-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 5 &mdash; Ch. 10 &amp; 20</div>
        ${link('Chapter 10 &mdash; Infrastructure Security',            R + '/CH10-Reading.html', 'dd-yellow')}
        ${link('Chapter 20 &mdash; Risk Management',                    R + '/CH20-Reading.html', 'dd-yellow')}
      </div>
    </div>`;

  /* ── Nav HTML ───────────────────────────────────────────── */
  let navHTML = '';

  if (isLab) {
    navHTML = `
      <div class="lab-ref-nav">
        <a href="${S}/Home.html"><span class="nav-logo-label">IS3513</span></a>
        <span class="lab-ref-sep">|</span>
        <span class="lab-ref-label">Reference</span>
        <a href="${S}/Grading_Info.html?context=lab">Grading Info</a>
        <a href="${S}/Engagement_Packet_Guide.html?context=lab">Engagement Packet Guide</a>
        <a href="${S}/GenAI_Policy.html?context=lab">GenAI Policy</a>
        <a href="${S}/Screenshot_Requirements.html?context=lab">Screenshot Requirements</a>
        <a href="${S}/Citations.html?context=lab">Citations</a>
        <div class="nav-search"><input type="search" class="nav-search__input" placeholder="Search the course" aria-label="Search the course site" autocomplete="off"><div class="nav-search__results" role="listbox" hidden></div></div>
        <a class="nav-discord" href="${S}/Discord.html?context=lab">Discord</a>
      </div>`;
  } else {
    navHTML = `
      <div class="nav-inner">
        <a class="nav-logo" href="${S}/Home.html">
          <span class="nav-logo-label">IS3513</span>
        </a>

        <div class="nav-menu">
          ${courseDropdown}
          ${nexusDropdown}
          ${modulesDropdown}
          ${labsDropdown}
          ${readingDropdown}
        </div>

        <div class="nav-search"><input type="search" class="nav-search__input" placeholder="Search the course" aria-label="Search the course site" autocomplete="off"><div class="nav-search__results" role="listbox" hidden></div></div>
        <a class="nav-discord" href="${S}/Discord.html">Discord</a>
      </div>`;
  }


  /* ── Site search ────────────────────────────────────────────
     search-index.json is written by build_search_index.py (render_all.sh).
     It loads the first time someone focuses the box. Every word typed must
     appear in a result; title matches rank first. */
  function initSearch(nav) {
    const box = nav.querySelector('.nav-search__input');
    const list = nav.querySelector('.nav-search__results');
    if (!box) return;
    let index = null, loading = null, hits = [], active = -1;
    const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
    const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    function load() {
      if (!loading) loading = fetch(BASE + '/search-index.json').then(r => r.json()).then(d => {
        index = d.map(e => ({ ...e, tl: e.t.toLowerCase(), xl: e.x.toLowerCase() }));
      }).catch(() => { index = []; });
      return loading;
    }
    function snippet(e, terms) {
      const p = e.xl.indexOf(terms.join(' '));
      const i = Math.max(0, p >= 0 ? p : e.xl.search(new RegExp('(^|[^a-z0-9])' + reEsc(terms[0]))));
      const start = Math.max(0, i - 60), end = Math.min(e.x.length, i + 140);
      let s = esc((start ? '… ' : '') + e.x.slice(start, end) + (end < e.x.length ? ' …' : ''));
      terms.forEach(t => { s = s.replace(new RegExp('(^|[^a-z0-9])(' + reEsc(esc(t)) + ')', 'ig'), '$1<mark>$2</mark>'); });
      return s;
    }
    function run() {
      const q = box.value.trim().toLowerCase();
      if (q.length < 2 || !index) { list.hidden = true; return; }
      const terms = q.split(/\s+/).filter(Boolean);
      // Words match from their start ("ps" finds "ps", not "steps"); the
      // whole query as a phrase ranks highest.
      const res = terms.map(t => new RegExp('(^|[^a-z0-9])' + reEsc(t), 'g'));
      hits = index.map(e => {
        let score = e.xl.includes(q) ? 25 : 0;
        for (const re of res) {
          const inT = (e.tl.match(re) || []).length, inX = (e.xl.match(re) || []).length;
          if (!inT && !inX) return null;
          score += (inT ? 10 : 0) + Math.min(5, inX);
        }
        return { e, score };
      }).filter(Boolean).sort((a, b) => b.score - a.score).slice(0, 8);
      active = -1;
      list.innerHTML = hits.length
        ? hits.map((h, k) => '<a class="nav-search__item" role="option" data-k="' + k + '" href="' + BASE + '/' + h.e.u + '">' +
            '<span class="nav-search__title">' + esc(h.e.t) + '</span>' +
            '<span class="nav-search__snip">' + snippet(h.e, terms) + '</span></a>').join('')
        : '<div class="nav-search__none">No matches. Try fewer or different words.</div>';
      list.hidden = false;
    }
    function mark(k) {
      const items = list.querySelectorAll('.nav-search__item');
      items.forEach((a, i) => a.classList.toggle('is-active', i === k));
      if (items[k]) items[k].scrollIntoView({ block: 'nearest' });
      active = k;
    }
    let timer;
    box.addEventListener('focus', () => { load().then(run); });
    box.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(() => load().then(run), 120); });
    box.addEventListener('keydown', ev => {
      const n = hits.length;
      if (ev.key === 'ArrowDown' && n) { ev.preventDefault(); mark((active + 1) % n); }
      else if (ev.key === 'ArrowUp' && n) { ev.preventDefault(); mark((active - 1 + n) % n); }
      else if (ev.key === 'Enter' && n) { ev.preventDefault(); location.href = BASE + '/' + hits[Math.max(active, 0)].e.u; }
      else if (ev.key === 'Escape') { list.hidden = true; box.blur(); }
    });
    document.addEventListener('click', ev => { if (!nav.querySelector('.nav-search').contains(ev.target)) list.hidden = true; });
  }

  /* ── Mount nav + footer ─────────────────────────────────── */
  function mount() {
    const touchIcon = document.createElement('link');
    touchIcon.rel   = 'apple-touch-icon';
    touchIcon.sizes = '180x180';
    touchIcon.href  = BASE + '/apple-touch-icon.png';
    document.head.appendChild(touchIcon);

    const style = document.createElement('style');
    style.id = 'is3513-nav-styles';
    style.textContent = css;
    document.head.appendChild(style);

    const nav = document.createElement('nav');
    nav.id = 'is3513-nav';
    nav.setAttribute('aria-label', 'Course navigation');
    nav.innerHTML = navHTML;
    document.body.insertBefore(nav, document.body.firstChild);
    initSearch(nav);

    // Dark pages (the tabbed lab layout) use the UT San Antonio logo made for a
    // dark background; if that file is missing, fall back to the standard logo.
    const LOGO_LIGHT = BASE + '/branding/UTSanAntonio_H_Logo_Dual_TM_RGB.png';
    const LOGO_DARK  = BASE + '/branding/UTSanAntonio_Reg_Logo_Rev_TM_RGB.svg';
    const darkPage   = document.body.classList.contains('nx-tabbed');

    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML =
      '<img class="site-footer__logo"' +
      ' src="' + (darkPage ? LOGO_DARK : LOGO_LIGHT) + '"' +
      (darkPage ? ' onerror="this.onerror=null;this.src=\'' + LOGO_LIGHT + '\'"' : '') +
      ' alt="UT San Antonio">' +
      '<div class="site-footer__citation">' +
      '<span class="site-footer__citation-label">Textbook</span>' +
      '<span class="site-footer__citation-text"><em>Principles of Computer Security: CompTIA Security+ and Beyond</em>' +
      ', 6th Edition &middot; Conklin &amp; White &middot; McGraw-Hill &middot; ISBN 978-1-260-47431-2</span>' +
      '</div>' +
      '<div class="site-footer__copyright">' +
      '&copy; 2026 The University of Texas at San Antonio. Developed by John Newsom' +
      ' for IS3513: Information Assurance and Security. All rights reserved.' +
      '</div>';
    document.body.appendChild(footer);
  }

  if (document.body) {
    mount();
  } else {
    document.addEventListener('DOMContentLoaded', mount);
  }

})();