(function () {
  const BASE = 'https://jfnewsom.github.io/is3513-assets/pages';
  const S = BASE + '/support';
  const SC = BASE + '/scenario';

  const params = new URLSearchParams(window.location.search);
  const isLab = params.get('context') === 'lab';

  /* ── Shared styles ─────────────────────────────────────────── */
  const css = `
    #nexus-nav {
      position: sticky;
      top: 0;
      z-index: 9999;
      background: #060a12;
      border-bottom: 1px solid #1e2538;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      font-size: 13px;
      user-select: none;
    }
    #nexus-nav a {
      text-decoration: none;
    }
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
      color: #ffffff;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.04em;
      padding: 0 10px 0 0;
      margin-right: 4px;
      border-right: 1px solid #1e2538;
      white-space: nowrap;
      flex-shrink: 0;
    }
    #nexus-nav .nav-logo .logo-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #4169E1;
      flex-shrink: 0;
    }
    #nexus-nav .nav-logo:hover .logo-dot {
      background: #7b68ee;
    }

    /* ── Dropdown menus ── */
    #nexus-nav .nav-menu {
      display: flex;
      align-items: center;
      gap: 2px;
      flex: 1;
    }
    #nexus-nav .nav-item {
      position: relative;
    }
    #nexus-nav .nav-trigger {
      display: flex;
      align-items: center;
      gap: 5px;
      color: #8892a4;
      padding: 0 10px;
      height: 40px;
      cursor: pointer;
      border-radius: 4px;
      transition: color 0.15s, background 0.15s;
      white-space: nowrap;
    }
    #nexus-nav .nav-trigger:hover {
      color: #ffffff;
      background: #0f1523;
    }
    #nexus-nav .nav-trigger .caret {
      font-size: 9px;
      opacity: 0.5;
      transition: transform 0.15s, opacity 0.15s;
    }
    #nexus-nav .nav-item:hover .caret {
      transform: rotate(180deg);
      opacity: 1;
    }
    #nexus-nav .nav-dropdown {
      display: none;
      position: absolute;
      top: calc(100% + 1px);
      left: 0;
      min-width: 200px;
      background: #0a0e17;
      border: 1px solid #1e2538;
      border-radius: 0 0 6px 6px;
      padding: 6px 0;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    #nexus-nav .nav-item:hover .nav-dropdown {
      display: block;
    }
    #nexus-nav .nav-dropdown a {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 16px;
      color: #8892a4;
      transition: color 0.12s, background 0.12s;
      line-height: 1.3;
    }
    #nexus-nav .nav-dropdown a:hover {
      color: #ffffff;
      background: #0f1523;
    }
    #nexus-nav .nav-dropdown .drop-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    #nexus-nav .nav-dropdown .drop-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 8px 16px 4px;
      color: #3a4258;
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
    #nexus-nav .nav-discord:hover {
      background: #4752c4;
    }

    /* ── Lab context nav ── */
    #nexus-nav .lab-nav {
      display: flex;
      align-items: center;
      gap: 0;
      flex: 1;
    }
    #nexus-nav .lab-back {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #8892a4;
      padding: 0 12px 0 0;
      margin-right: 8px;
      height: 40px;
      border-right: 1px solid #1e2538;
      cursor: pointer;
      transition: color 0.15s;
      white-space: nowrap;
      flex-shrink: 0;
    }
    #nexus-nav .lab-back:hover {
      color: #ffffff;
    }
    #nexus-nav .lab-back .back-arrow {
      font-size: 15px;
      line-height: 1;
    }
    #nexus-nav .lab-ref-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #3a4258;
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
      color: #8892a4;
      padding: 4px 10px;
      border-radius: 4px;
      transition: color 0.12s, background 0.12s;
      white-space: nowrap;
    }
    #nexus-nav .lab-links a:hover {
      color: #ffffff;
      background: #0f1523;
    }

    /* accent colors per section */
    .nav-dd-green  { background: #00D26A; }
    .nav-dd-yellow { background: #fec618; }
    .nav-dd-cyan   { background: #00bcd4; }
    .nav-dd-purple { background: #7b68ee; }
  `;

  /* ── Inject styles ──────────────────────────────────────────── */
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  /* ── Build nav HTML ─────────────────────────────────────────── */
  let html = '';

  if (isLab) {
    /* LAB CONTEXT NAV */
    html = `
      <div class="nav-inner">
        <a class="nav-logo" href="${S}/Home.html">
          <span class="logo-dot"></span>NEXUS
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
            <a href="${S}/citations.html?context=lab">Citations</a>
          </div>
        </div>
        <a class="nav-discord" href="${S}/Discord.html?context=lab">Discord</a>
      </div>
    `;
  } else {
    /* MINI-SITE NAV */
    html = `
      <div class="nav-inner">
        <a class="nav-logo" href="${S}/Home.html">
          <span class="logo-dot"></span>IS3513 Home
        </a>
        <div class="nav-menu">

          <div class="nav-item">
            <div class="nav-trigger">
              Getting Started <span class="caret">&#9660;</span>
            </div>
            <div class="nav-dropdown">
              <div class="drop-label">Getting Started</div>
              <a href="${S}/StartHere.html">
                <span class="drop-dot nav-dd-green"></span>Start Here
              </a>
              <a href="${S}/Kali_VM_Setup.html">
                <span class="drop-dot nav-dd-green"></span>Kali VM Setup
              </a>
              <a href="${S}/Course_Schedule.html">
                <span class="drop-dot nav-dd-green"></span>Course Schedule
              </a>
              <a href="${S}/Textbook.html">
                <span class="drop-dot nav-dd-green"></span>Textbook Info
              </a>
            </div>
          </div>

          <div class="nav-item">
            <div class="nav-trigger">
              Policies &amp; Grading <span class="caret">&#9660;</span>
            </div>
            <div class="nav-dropdown">
              <div class="drop-label">Policies &amp; Grading</div>
              <a href="${S}/Grading_Info.html">
                <span class="drop-dot nav-dd-yellow"></span>Grading Info
              </a>
              <a href="${S}/GenAI_Policy.html">
                <span class="drop-dot nav-dd-yellow"></span>GenAI Policy
              </a>
              <a href="${S}/How_To_Get_Help.html">
                <span class="drop-dot nav-dd-yellow"></span>How to Get Help
              </a>
            </div>
          </div>

          <div class="nav-item">
            <div class="nav-trigger">
              Documentation <span class="caret">&#9660;</span>
            </div>
            <div class="nav-dropdown">
              <div class="drop-label">Documentation</div>
              <a href="${S}/Engagement_Packet_Guide.html">
                <span class="drop-dot nav-dd-cyan"></span>Engagement Packet Guide
              </a>
              <a href="${S}/Screenshot_Requirements.html">
                <span class="drop-dot nav-dd-cyan"></span>Screenshot Requirements
              </a>
              <a href="${S}/citations.html">
                <span class="drop-dot nav-dd-cyan"></span>Citations
              </a>
            </div>
          </div>

          <div class="nav-item">
            <div class="nav-trigger">
              NEXUS World <span class="caret">&#9660;</span>
            </div>
            <div class="nav-dropdown">
              <div class="drop-label">NEXUS World</div>
              <a href="${SC}/NEXUS_Security.html">
                <span class="drop-dot nav-dd-purple"></span>NEXUS Security
              </a>
              <a href="${SC}/Meet_The_Team.html">
                <span class="drop-dot nav-dd-purple"></span>Meet the Team
              </a>
              <a href="${SC}/Our_Clients.html">
                <span class="drop-dot nav-dd-purple"></span>Our Clients
              </a>
            </div>
          </div>

        </div>
        <a class="nav-discord" href="${S}/Discord.html">Discord</a>
      </div>
    `;
  }

  /* ── Mount nav ──────────────────────────────────────────────── */
  const nav = document.createElement('nav');
  nav.id = 'nexus-nav';
  nav.innerHTML = html;
  document.body.insertBefore(nav, document.body.firstChild);

})();
