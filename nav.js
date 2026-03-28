/**
 * nav.js — IS3513 Information Assurance & Security
 * Top horizontal navigation bar with dropdown menus.
 *
 * Context is determined by the ?context= query parameter in the URL:
 *
 *   No parameter (direct open)   → full nav (all sections + assignments)
 *   ?context=module              → slim nav suppressed (Canvas iframe embed)
 *   ?context=lab                 → reference sidebar only (no full nav)
 *
 * This means the same HTML file behaves correctly whether opened
 * directly by a student or embedded in a Canvas iframe.
 */

(function () {
  'use strict';

  /* ── Context detection ──────────────────────────────────── */
  const inIframe = window.self !== window.top;
  const params   = new URLSearchParams(window.location.search);
  const ctx      = params.get('context'); // null | 'module' | 'lab'

  if (inIframe && ctx !== 'lab') return; // non-lab iframes: no nav

  const showFull = !inIframe && ctx !== 'lab';
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
    body { padding-top: 42px; }
    #is3513-nav a { text-decoration: none; }

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
      gap: 10px;
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
    #is3513-nav .dd-red    { background: #FF2641; }

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
      color: #778087;
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
    #is3513-nav .lab-ref-sep {
      color: #333;
    }

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

  /* ── Modules dropdown ───────────────────────────────────── */
  const modulesDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Modules <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Module Overviews</div>
        ${link('Module 1 &mdash; Reconnaissance',       S + '/Module_1.html',  'dd-purple')}
        ${link('Module 2 &mdash; Cryptography &amp; Auth', S + '/Module_2.html', 'dd-purple')}
        ${link('Module 3 &mdash; Networks &amp; Cloud', S + '/Module_3.html',  'dd-purple')}
        ${link('Module 4 &mdash; Threats &amp; Attacks',S + '/Module_4.html',  'dd-purple')}
        ${link('Module 5 &mdash; Risk &amp; Infrastructure', S + '/Module_5.html', 'dd-purple')}
        <div class="drop-label">Lab Assignments</div>
        <div class="drop-sub">Module 1 &mdash; Reconnaissance</div>
        ${link('Lab 1.1 &mdash; Kali Environment Setup',       L + '/Lab1_1_Kali_Environment_Setup.html',                      'dd-cyan')}
        ${link('Lab 1.2 &mdash; Reconnaissance Tools',         L + '/Lab1_2_Reconnaissance_Tool_Exploration.html',              'dd-cyan')}
        ${link('Lab 1.3 &mdash; Brazos Engagement',            L + '/Lab1_3_Brazos_Financial_Reconnaissance_Engagement.html',   'dd-cyan')}
        <div class="drop-sub">Module 2 &mdash; Cryptography &amp; Auth</div>
        ${link('Lab 2.1 &mdash; Cryptographic Foundations',    L + '/Lab2_1_Cryptographic_Foundations.html',                   'dd-cyan')}
        ${link('Lab 2.2 &mdash; Authentication Systems',       L + '/Lab2_2_Authentication_Systems.html',                      'dd-cyan')}
        ${link('Lab 2.3 &mdash; Gulf Coast Engagement',        L + '/Lab2_3_Gulf_Coast_Certificate_Remediation.html',           'dd-cyan')}
        <div class="drop-sub">Module 3 &mdash; Networks &amp; Cloud</div>
        ${link('Lab 3.1 &mdash; Network Addressing',           L + '/Lab3_1_Network_Addressing_Fundamentals.html',              'dd-cyan')}
        ${link('Lab 3.2 &mdash; Protocol Analysis',            L + '/Lab3_2_Protocol_Analysis_Tools.html',                     'dd-cyan')}
        ${link('Lab 3.3 &mdash; Network Analysis Engagement',  L + '/Lab3_3_Network_Analysis_Engagement.html',                  'dd-cyan')}
        <div class="drop-sub">Module 4 &mdash; Threats &amp; Attacks</div>
        ${link('Lab 4.1 &mdash; Windows Password Cracking',    L + '/Lab4_1_Windows_Password_Cracking.html',                   'dd-cyan')}
        ${link('Lab 4.2 &mdash; Linux Password Cracking',      L + '/Lab4_2_Linux_Password_Cracking.html',                     'dd-cyan')}
        ${link('Lab 4.3 &mdash; Password Security Assessment', L + '/Lab4_3_Password_Security_Assessment.html',                 'dd-cyan')}
        <div class="drop-sub">Module 5 &mdash; Risk &amp; Infrastructure</div>
        ${link('Lab 5.1 &mdash; Vulnerability Scanning',       L + '/Lab5_1_Vulnerability_Discovery_Scanning.html',             'dd-cyan')}
        ${link('Lab 5.2 &mdash; Risk Assessment',              L + '/Lab5_2_Risk_Assessment_Prioritization.html',               'dd-cyan')}
        ${link('Lab 5.3 &mdash; LoneStar Engagement',          L + '/Lab5_3_Risk_Vulnerability_Assessment_Report.html',         'dd-cyan')}
      </div>
    </div>` : '';

  /* ── Reading dropdown ───────────────────────────────────── */
  const readingDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Reading <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Chapter Guides</div>
        <div class="drop-sub">Module 1 &mdash; Ch. 1&ndash;2</div>
        ${link('Chapter 1 &mdash; Intro &amp; Security Trends',       R + '/CH01-Reading.html', 'dd-yellow')}
        ${link('Chapter 2 &mdash; General Security Concepts',         R + '/CH02-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 2 &mdash; Ch. 6 &amp; 11</div>
        ${link('Chapter 6 &mdash; Applied Cryptography',              R + '/CH06-Reading.html', 'dd-yellow')}
        ${link('Chapter 11 &mdash; Authentication &amp; Remote Access',R + '/CH11-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 3 &mdash; Ch. 9, 13 &amp; 18</div>
        ${link('Chapter 9 &mdash; Network Fundamentals',              R + '/CH09-Reading.html', 'dd-yellow')}
        ${link('Chapter 13 &mdash; IDS &amp; Network Security',       R + '/CH13-Reading.html', 'dd-yellow')}
        ${link('Chapter 18 &mdash; Cloud Computing',                  R + '/CH18-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 4 &mdash; Ch. 15 &amp; 16</div>
        ${link('Chapter 15 &mdash; Types of Attacks',                 R + '/CH15-Reading.html', 'dd-yellow')}
        ${link('Chapter 16 &mdash; Security Tools &amp; Techniques',  R + '/CH16-Reading.html', 'dd-yellow')}
        <div class="drop-sub">Module 5 &mdash; Ch. 10 &amp; 20</div>
        ${link('Chapter 10 &mdash; Infrastructure Security',          R + '/CH10-Reading.html', 'dd-yellow')}
        ${link('Chapter 20 &mdash; Risk Management',                  R + '/CH20-Reading.html', 'dd-yellow')}
      </div>
    </div>` : '';

  /* ── Nav HTML ───────────────────────────────────────────── */
  let navHTML = '';

  if (isLab) {
    /* Lab reference sidebar */
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
        <a class="nav-discord" href="${S}/Discord.html?context=lab">Discord</a>
      </div>`;
  } else {
    /* Full nav */
    navHTML = `
      <div class="nav-inner">
        <a class="nav-logo" href="${S}/Home.html">
          <span class="nav-logo-label">IS3513</span>
        </a>

        <div class="nav-menu">

          <div class="nav-item">
            <div class="nav-trigger">Course Info <span class="nav-caret">&#9660;</span></div>
            <div class="nav-dropdown">
              <div class="drop-label">Getting Started</div>
              ${link('Start Here',             S + '/StartHere.html',              'dd-green')}
              ${link('Kali VM Setup',          S + '/Kali_VM_Setup.html',          'dd-green')}
              ${link('Course Schedule',        S + '/Course_Schedule.html',        'dd-green')}
              ${link('Textbook Info',          S + '/Textbook.html',               'dd-green')}
              <div class="drop-label">Policies</div>
              ${link('Grading Info',           S + '/Grading_Info.html',           'dd-yellow')}
              ${link('GenAI Policy',           S + '/GenAI_Policy.html',           'dd-yellow')}
              ${link('How to Get Help',        S + '/How_To_Get_Help.html',        'dd-yellow')}
              <div class="drop-label">Reference</div>
              ${link('Engagement Packet Guide',S + '/Engagement_Packet_Guide.html','dd-cyan')}
              ${link('Screenshot Requirements',S + '/Screenshot_Requirements.html','dd-cyan')}
              ${link('Citations',              S + '/Citations.html',              'dd-cyan')}
            </div>
          </div>

          ${modulesDropdown}
          ${readingDropdown}

          <div class="nav-item">
            <div class="nav-trigger">NEXUS World <span class="nav-caret">&#9660;</span></div>
            <div class="nav-dropdown">
              <div class="drop-label">NEXUS World</div>
              ${link('NEXUS Security', S + '/NEXUS_Security.html', 'dd-purple')}
              ${link('Meet the Team',  S + '/Meet_The_Team.html',  'dd-purple')}
              ${link('Our Clients',    S + '/Our_Clients.html',    'dd-purple')}
            </div>
          </div>

        </div>

        <a class="nav-discord" href="${S}/Discord.html">Discord</a>
      </div>`;
  }

  /* ── Mount nav + footer ─────────────────────────────────── */
  function mount() {
    const style = document.createElement('style');
    style.id = 'is3513-nav-styles';
    style.textContent = css;
    document.head.appendChild(style);

    const nav = document.createElement('nav');
    nav.id = 'is3513-nav';
    nav.setAttribute('aria-label', 'Course navigation');
    nav.innerHTML = navHTML;
    document.body.insertBefore(nav, document.body.firstChild);

    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML =
      '<img class="site-footer__logo"' +
      ' src="https://jfnewsom.github.io/is3513-assets/branding/UTSanAntonio_H_Logo_Dual_TM_RGB.png"' +
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
