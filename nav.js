(function () {
  const BASE = 'https://jfnewsom.github.io/is3513-assets/pages';
  const S = BASE + '/support';

  // ── Context detection (mirrors IS2053 behavior) ──────────────
  // Primary gate: iframe detection.
  // Assignment pages (labs, reading, exams, module overviews) are
  // embedded in Canvas as plain iframes — they get no nav at all.
  // Support pages embedded in Canvas use ?context=support in the
  // iframe src to opt into the nav.
  // Direct URL access (student navigates to the page) gets full nav.
  const inIframe = window.self !== window.top;
  const ctx = new URLSearchParams(window.location.search).get('context');

  // In a Canvas iframe without ?context=support → silent exit, no nav
  if (inIframe && ctx !== 'support') return;

  // IS3513-specific: reference docs linked from engagement labs
  // open in a new tab with ?context=lab — show the compact lab nav.
  const isLab = !inIframe && ctx === 'lab';

  // showFull: true when accessed directly in browser; false in support iframe.
  // Labs and Reading dropdowns only render when showFull is true.
  const showFull = !inIframe;

  /* ── Google Fonts ───────────────────────────────────────────── */
  const fontLink = document.createElement('link');
  fontLink.rel = 'stylesheet';
  fontLink.href = 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Roboto+Slab:wght@500;700&family=Roboto+Mono:wght@400;500&display=swap';
  document.head.appendChild(fontLink);

  const iconsLink = document.createElement('link');
  iconsLink.rel = 'stylesheet';
  iconsLink.href = 'https://fonts.googleapis.com/icon?family=Material+Icons';
  document.head.appendChild(iconsLink);

  /* ── Shared styles ─────────────────────────────────────────── */
  const css = `
    #nexus-nav {
      position: sticky;
      top: 0;
      z-index: 9999;
      background: #ffffff;
      border-bottom: 1px solid #e0e4ef;
      font-family: 'Roboto', sans-serif;
      font-size: 13px;
      user-select: none;
    }
    #nexus-nav a { text-decoration: none; }
    #nexus-nav .nav-inner {
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 0 16px;
      height: 40px;
    }

    /* ── Logo ── */
    #nexus-nav .nav-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #1a1a2e;
      font-family: 'Roboto Slab', serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.02em;
      padding: 0 12px 0 0;
      margin-right: 4px;
      white-space: nowrap;
      flex-shrink: 0;
      transition: color 0.15s;
    }
    #nexus-nav .nav-logo:hover { color: #4169E1; }

    /* ── Dropdown menus ── */
    #nexus-nav .nav-menu {
      display: flex;
      align-items: center;
      gap: 2px;
      flex: 1;
    }
    #nexus-nav .nav-item { position: relative; }
    #nexus-nav .nav-trigger {
      display: flex;
      align-items: center;
      gap: 5px;
      color: #4a5568;
      padding: 0 10px;
      height: 40px;
      cursor: pointer;
      border-radius: 4px;
      transition: color 0.15s, background 0.15s;
      white-space: nowrap;
      font-weight: 500;
    }
    #nexus-nav .nav-trigger:hover {
      color: #1a1a2e;
      background: #f5f6fa;
    }
    #nexus-nav .nav-trigger .caret {
      font-size: 9px;
      opacity: 0.4;
      transition: transform 0.15s, opacity 0.15s;
    }
    #nexus-nav .nav-item:hover .caret {
      transform: rotate(180deg);
      opacity: 0.8;
    }
    #nexus-nav .nav-dropdown {
      display: none;
      position: absolute;
      top: calc(100% + 1px);
      left: 0;
      min-width: 210px;
      background: #ffffff;
      border: 1px solid #e0e4ef;
      border-radius: 0 0 6px 6px;
      padding: 6px 0;
      box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    #nexus-nav .nav-item:hover .nav-dropdown { display: block; }
    #nexus-nav .nav-dropdown a {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 16px;
      color: #4a5568;
      transition: color 0.12s, background 0.12s;
      line-height: 1.3;
      font-size: 13px;
    }
    #nexus-nav .nav-dropdown a:hover {
      color: #1a1a2e;
      background: #f5f6fa;
    }
    #nexus-nav .nav-dropdown .drop-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    #nexus-nav .nav-dropdown .drop-label {
      font-family: 'Roboto Slab', serif;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 8px 16px 4px;
      color: #b0b8c4;
    }
    #nexus-nav .nav-dropdown .drop-sub {
      font-family: 'Roboto', sans-serif;
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 6px 16px 2px;
      color: #4a5568;
    }

    /* ── Discord button ── */
    #nexus-nav .nav-discord {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #5865f2;
      color: #ffffff !important;
      padding: 5px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
      transition: background 0.15s;
      white-space: nowrap;
      flex-shrink: 0;
    }
    #nexus-nav .nav-discord:hover { background: #4752c4; }

    /* ── Lab context nav ── */
    #nexus-nav .lab-nav {
      display: flex;
      align-items: center;
      flex: 1;
    }
    #nexus-nav .lab-back {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #4a5568;
      padding: 0 12px 0 0;
      margin-right: 10px;
      height: 40px;
      border-right: 1px solid #e0e4ef;
      cursor: pointer;
      transition: color 0.15s;
      white-space: nowrap;
      flex-shrink: 0;
      font-weight: 500;
    }
    #nexus-nav .lab-back:hover { color: #4169E1; }
    #nexus-nav .lab-back .back-arrow { font-size: 15px; line-height: 1; }
    #nexus-nav .lab-ref-label {
      font-family: 'Roboto Slab', serif;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #b0b8c4;
      padding-right: 10px;
      white-space: nowrap;
      flex-shrink: 0;
    }
    #nexus-nav .lab-links {
      display: flex;
      align-items: center;
      gap: 2px;
      flex-wrap: wrap;
    }
    #nexus-nav .lab-links a {
      color: #4a5568;
      padding: 4px 10px;
      border-radius: 4px;
      transition: color 0.12s, background 0.12s;
      white-space: nowrap;
      font-weight: 500;
    }
    #nexus-nav .lab-links a:hover {
      color: #1a1a2e;
      background: #f5f6fa;
    }

    /* accent dot colors */
    .nav-dd-green  { background: #00D26A; }
    .nav-dd-yellow { background: #fec618; }
    .nav-dd-cyan   { background: #00bcd4; }
    .nav-dd-purple { background: #7b68ee; }

    /* ── Injected footer ────────────────────────────────── */
    .site-footer {
      border-top: 1px solid #e0e4ef;
      padding: 24px 40px 20px 40px;
      margin-top: 0;
      text-align: center;
      background: #fff;
    }
    .site-footer__logo {
      height: 48px;
      display: block;
      margin: 0 auto 16px auto;
    }
    .site-footer__citation {
      display: inline-flex;
      align-items: baseline;
      gap: 10px;
      border: 1px solid #2a2a2a;
      border-left: 3px solid #4169E1;
      padding: 6px 14px;
      margin-bottom: 14px;
    }
    .site-footer__citation-label {
      font-family: 'Roboto', sans-serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #4169E1;
      white-space: nowrap;
    }
    .site-footer__citation-text {
      font-family: 'Roboto', sans-serif;
      font-size: 11px;
      color: #555;
    }
    .site-footer__copyright {
      font-family: 'Roboto', sans-serif;
      font-size: 11px;
      color: #888;
    }
  `;

  /* ── Inject styles ──────────────────────────────────────────── */
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  /* ── Helper: dropdown link ──────────────────────────────────── */
  function link(label, url) {
    return `<a href="${url}"><span class="drop-dot nav-dd-cyan"></span>${label}</a>`;
  }

  /* ── Modules dropdown (direct browser only) ───────────────────── */
  const L = BASE + '/labs/';
  const M = BASE + '/support/';
  const modulesDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Modules <span class="caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Module Overviews</div>
        <a href="${M}Module_1.html"><span class="drop-dot nav-dd-purple"></span>Module 1 &mdash; Reconnaissance</a>
        <a href="${M}Module_2.html"><span class="drop-dot nav-dd-purple"></span>Module 2 &mdash; Cryptography &amp; Auth</a>
        <a href="${M}Module_3.html"><span class="drop-dot nav-dd-purple"></span>Module 3 &mdash; Networks &amp; Cloud</a>
        <a href="${M}Module_4.html"><span class="drop-dot nav-dd-purple"></span>Module 4 &mdash; Threats &amp; Attacks</a>
        <a href="${M}Module_5.html"><span class="drop-dot nav-dd-purple"></span>Module 5 &mdash; Risk &amp; Infrastructure</a>
        <div class="drop-label">Lab Assignments</div>
        <div class="drop-sub">Module 1 &mdash; Reconnaissance</div>
        ${link('Lab 1.1 &mdash; Kali Environment Setup',       L + 'Lab1_1_Kali_Environment_Setup.html')}
        ${link('Lab 1.2 &mdash; Reconnaissance Tools',         L + 'Lab1_2_Reconnaissance_Tool_Exploration.html')}
        ${link('Lab 1.3 &mdash; Brazos Engagement',            L + 'Lab1_3_Brazos_Financial_Reconnaissance_Engagement.html')}
        <div class="drop-sub">Module 2 &mdash; Cryptography &amp; Auth</div>
        ${link('Lab 2.1 &mdash; Cryptographic Foundations',    L + 'Lab2_1_Cryptographic_Foundations.html')}
        ${link('Lab 2.2 &mdash; Authentication Systems',       L + 'Lab2_2_Authentication_Systems.html')}
        ${link('Lab 2.3 &mdash; Gulf Coast Engagement',        L + 'Lab2_3_Gulf_Coast_Certificate_Remediation.html')}
        <div class="drop-sub">Module 3 &mdash; Networks &amp; Cloud</div>
        ${link('Lab 3.1 &mdash; Network Addressing',           L + 'Lab3_1_Network_Addressing_Fundamentals.html')}
        ${link('Lab 3.2 &mdash; Protocol Analysis',            L + 'Lab3_2_Protocol_Analysis_Tools.html')}
        ${link('Lab 3.3 &mdash; Network Analysis Engagement',  L + 'Lab3_3_Network_Analysis_Engagement.html')}
        <div class="drop-sub">Module 4 &mdash; Threats &amp; Attacks</div>
        ${link('Lab 4.1 &mdash; Windows Password Cracking',    L + 'Lab4_1_Windows_Password_Cracking.html')}
        ${link('Lab 4.2 &mdash; Linux Password Cracking',      L + 'Lab4_2_Linux_Password_Cracking.html')}
        ${link('Lab 4.3 &mdash; Password Security Assessment', L + 'Lab4_3_Password_Security_Assessment.html')}
        <div class="drop-sub">Module 5 &mdash; Risk &amp; Infrastructure</div>
        ${link('Lab 5.1 &mdash; Vulnerability Scanning',       L + 'Lab5_1_Vulnerability_Discovery_Scanning.html')}
        ${link('Lab 5.2 &mdash; Risk Assessment',              L + 'Lab5_2_Risk_Assessment_Prioritization.html')}
        ${link('Lab 5.3 &mdash; LoneStar Engagement',          L + 'Lab5_3_Risk_Vulnerability_Assessment_Report.html')}
      </div>
    </div>` : '';

  /* ── Reading dropdown (direct browser only) ─────────────────── */
  const R = BASE + '/reading/';
  const readingDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Reading <span class="caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Chapter Guides</div>
        <div class="drop-sub">Module 1 &mdash; Ch. 1&ndash;2</div>
        <a href="${R}CH01-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 1 &mdash; Intro &amp; Security Trends</a>
        <a href="${R}CH02-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 2 &mdash; General Security Concepts</a>
        <div class="drop-sub">Module 2 &mdash; Ch. 6 &amp; 11</div>
        <a href="${R}CH06-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 6 &mdash; Applied Cryptography</a>
        <a href="${R}CH11-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 11 &mdash; Authentication &amp; Remote Access</a>
        <div class="drop-sub">Module 3 &mdash; Ch. 9, 13 &amp; 18</div>
        <a href="${R}CH09-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 9 &mdash; Network Fundamentals</a>
        <a href="${R}CH13-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 13 &mdash; IDS &amp; Network Security</a>
        <a href="${R}CH18-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 18 &mdash; Cloud Computing</a>
        <div class="drop-sub">Module 4 &mdash; Ch. 15 &amp; 16</div>
        <a href="${R}CH15-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 15 &mdash; Types of Attacks</a>
        <a href="${R}CH16-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 16 &mdash; Security Tools &amp; Techniques</a>
        <div class="drop-sub">Module 5 &mdash; Ch. 10 &amp; 20</div>
        <a href="${R}CH10-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 10 &mdash; Infrastructure Security</a>
        <a href="${R}CH20-Reading.html"><span class="drop-dot nav-dd-yellow"></span>Chapter 20 &mdash; Risk Management</a>
      </div>
    </div>` : '';

  /* ── Build nav HTML ─────────────────────────────────────────── */
  let html = '';

  if (isLab) {
    html = `
      <div class="nav-inner">
        <a class="nav-logo" href="${S}/Home.html">IS3513</a>
        </a>
        <div class="lab-nav">
          <span class="lab-back" onclick="history.back()">
            <span class="back-arrow">&#8592;</span> Back to Lab
          </span>
          <span class="lab-ref-label">Reference Docs</span>
          <div class="lab-links">
            <a href="${S}/Grading_Info.html?context=lab">Grading Info</a>
            <a href="${S}/Engagement_Packet_Guide.html?context=lab">Engagement Packet Guide</a>
            <a href="${S}/GenAI_Policy.html?context=lab">GenAI Policy</a>
            <a href="${S}/Screenshot_Requirements.html?context=lab">Screenshot Requirements</a>
            <a href="${S}/Citations.html?context=lab">Citations</a>
          </div>
        </div>
        <a class="nav-discord" href="${S}/Discord.html?context=lab">Discord</a>
      </div>
    `;
  } else {
    html = `
      <div class="nav-inner">
        <a class="nav-logo" href="${S}/Home.html">IS3513</a>
        </a>
        <div class="nav-menu">

          <div class="nav-item">
            <div class="nav-trigger">Course Info <span class="caret">&#9660;</span></div>
            <div class="nav-dropdown">
              <div class="drop-label">Getting Started</div>
              <a href="${S}/StartHere.html"><span class="drop-dot nav-dd-green"></span>Start Here</a>
              <a href="${S}/Kali_VM_Setup.html"><span class="drop-dot nav-dd-green"></span>Kali VM Setup</a>
              <a href="${S}/Course_Schedule.html"><span class="drop-dot nav-dd-green"></span>Course Schedule</a>
              <a href="${S}/Textbook.html"><span class="drop-dot nav-dd-green"></span>Textbook Info</a>
              <div class="drop-label">Policies</div>
              <a href="${S}/Grading_Info.html"><span class="drop-dot nav-dd-yellow"></span>Grading Info</a>
              <a href="${S}/GenAI_Policy.html"><span class="drop-dot nav-dd-yellow"></span>GenAI Policy</a>
              <a href="${S}/How_To_Get_Help.html"><span class="drop-dot nav-dd-yellow"></span>How to Get Help</a>
              <div class="drop-label">Reference</div>
              <a href="${S}/Engagement_Packet_Guide.html"><span class="drop-dot nav-dd-cyan"></span>Engagement Packet Guide</a>
              <a href="${S}/Screenshot_Requirements.html"><span class="drop-dot nav-dd-cyan"></span>Screenshot Requirements</a>
              <a href="${S}/Citations.html"><span class="drop-dot nav-dd-cyan"></span>Citations</a>
            </div>
          </div>

          ${modulesDropdown}
          ${readingDropdown}

          <div class="nav-item">
            <div class="nav-trigger">NEXUS World <span class="caret">&#9660;</span></div>
            <div class="nav-dropdown">
              <div class="drop-label">NEXUS World</div>
              <a href="${S}/NEXUS_Security.html"><span class="drop-dot nav-dd-purple"></span>NEXUS Security</a>
              <a href="${S}/Meet_The_Team.html"><span class="drop-dot nav-dd-purple"></span>Meet the Team</a>
              <a href="${S}/Our_Clients.html"><span class="drop-dot nav-dd-purple"></span>Our Clients</a>
            </div>
          </div>

        </div>
        <a class="nav-discord" href="${S}/Discord.html">Discord</a>
      </div>
    `;
  }

  /* ── Mount nav + footer ─────────────────────────────────────── */
  function mount() {
    const nav = document.createElement('nav');
    nav.id = 'nexus-nav';
    nav.innerHTML = html;
    document.body.insertBefore(nav, document.body.firstChild);

    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML =
      '<img class="site-footer__logo"' +
      ' src="https://jfnewsom.github.io/is2053-assets/branding/UTSanAntonio_H_Logo_Dual_TM_RGB.png"' +
      ' alt="UT San Antonio">' +
      '<div class="site-footer__citation">' +
      '<span class="site-footer__citation-label">Textbook</span>' +
      '<span class="site-footer__citation-text"><em>Principles of Computer Security: CompTIA Security+ and Beyond</em>, 6th Edition' +
      ' &middot; Conklin &amp; White &middot; McGraw-Hill &middot; ISBN 978-1-260-47431-2</span>' +
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

  /* ── Copy buttons for .nx-cmd blocks ───────────────────────── */
  function initCopyButtons() {
    document.querySelectorAll('.nx-cmd').forEach(function(block) {
      const btn = document.createElement('button');
      btn.className = 'nx-copy-btn';
      btn.setAttribute('aria-label', 'Copy command');
      btn.innerHTML = '<span class="material-icons" aria-hidden="true">content_copy</span>';
      btn.addEventListener('click', function() {
        const text = block.innerText.replace(/\n$/, '').trim();
        navigator.clipboard.writeText(text).then(function() {
          btn.innerHTML = '<span class="material-icons" aria-hidden="true">check</span>';
          btn.classList.add('copied');
          setTimeout(function() {
            btn.innerHTML = '<span class="material-icons" aria-hidden="true">content_copy</span>';
            btn.classList.remove('copied');
          }, 1500);
        });
      });
      block.appendChild(btn);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCopyButtons);
  } else {
    initCopyButtons();
  }

})();
