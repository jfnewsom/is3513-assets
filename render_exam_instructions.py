#!/usr/bin/env python3
"""
render_exam_instructions.py
Renders Exam Instructions JSON → class-based HTML using site.css.
No inline styles, no external SVG images.
All exams use #E63946 red accent — consistent across all 5.

Usage:
  python3 render_exam_instructions.py                        # all 5 exams
  python3 render_exam_instructions.py <src.json> <out.html> # single file
"""
import json, sys, os, glob

CSS_PATH = "../../site.css"
ASSETS   = "https://jfnewsom.github.io/is3513-assets"
ACCENT   = "#E63946"


def shell(module_num, module_title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Module {module_num} Exam &#8211; IS3513</title>
  <link rel="stylesheet" href="{CSS_PATH}">
</head>
<body>
<script src="{ASSETS}/nav.js"></script>

<div class="nx-page">

<div class="nx-section">

  <!-- Header -->
  <div class="nx-header" style="--accent: {ACCENT};">
    <div class="nx-header-top">
      <div class="nx-kw">exam</div>
      <div class="nx-sec">{module_num}</div>
    </div>
    <div class="nx-sub">{module_title}</div>
  </div>

  <!-- Main card -->
  <div class="nx-card nx-card--sym" style="--accent: {ACCENT};">

{body}

  </div>

</div>

</div>
</body>
</html>"""


def render(data):
    module_num   = data["module"]
    module_title = data["moduleTitle"]
    stats        = data["stats"]

    # Stat blocks
    stat_blocks = f"""    <div class="nx-info-bar nx-info-bar--lg">
      <div class="nx-info-stat">
        <div class="nx-info-stat__label nx-info-stat__label--purple">Questions</div>
        <div class="nx-info-stat__value nx-info-stat__value--lg">{stats['questions']}</div>
      </div>
      <div class="nx-info-stat">
        <div class="nx-info-stat__label nx-info-stat__label--orange">Time Limit</div>
        <div class="nx-info-stat__value nx-info-stat__value--lg">{stats['timeLimit']}</div>
      </div>
      <div class="nx-info-stat">
        <div class="nx-info-stat__label nx-info-stat__label--red">Attempts</div>
        <div class="nx-info-stat__value nx-info-stat__value--lg">{stats['attempts']}</div>
      </div>
    </div>"""

    # Chapters list
    chapters_html = "\n".join(
        f'          <div class="nx-exam-chapter"><strong>{c["number"]}</strong> &#8212; {c["title"]}</div>'
        for c in data["chapters"]
    )

    # Tips list
    tips_html = "\n".join(
        f'          <li>{t}</li>'
        for t in data["tips"]
    )

    # Two-column layout
    two_col = f"""    <div class="nx-two-col">

      <!-- Left column -->
      <div class="nx-two-col__col">

        <div class="nx-exam-section">
          <div class="nx-section-label">Chapters Covered</div>
          <div class="nx-exam-list">
{chapters_html}
          </div>
        </div>

        <div class="nx-exam-section">
          <div class="nx-section-label nx-section-label--green">Allowed Materials</div>
          <div class="nx-exam-body">{data['allowed']}</div>
        </div>

        <div class="nx-exam-section">
          <div class="nx-section-label nx-section-label--red">Not Allowed</div>
          <div class="nx-exam-body">{data['notAllowed']}</div>
        </div>

      </div>

      <!-- Right column -->
      <div class="nx-two-col__col">

        <div class="nx-exam-section">
          <div class="nx-section-label nx-section-label--cyan">Tips for Success</div>
          <ul class="nx-exam-tips">
{tips_html}
          </ul>
        </div>

        <div class="nx-exam-section">
          <div class="nx-section-label nx-section-label--orange">Time Management</div>
          <div class="nx-exam-body">{data['timeManagement']}</div>
        </div>

      </div>

    </div>"""

    # Academic integrity bar
    integrity = f"""    <div class="nx-client-ctx" style="--client-color: {ACCENT}; --client-rgb: 230, 57, 70;">
      <span class="nx-client-ctx__label">Academic Integrity:</span>
      <span class="nx-client-ctx__body"> This is an individual assessment. All work must be your own. Violations result in a zero and referral to Student Conduct.</span>
    </div>"""

    # Footer
    footer = f'    <div class="nx-page-footer">{data["readyMessage"]} <strong>Good luck, analyst!</strong></div>'

    body = "\n\n".join([stat_blocks, two_col, integrity, footer])
    return shell(module_num, module_title, body)


def main():
    if len(sys.argv) == 3:
        src, dst = sys.argv[1], sys.argv[2]
        with open(src) as f:
            data = json.load(f)
        with open(dst, "w") as f:
            f.write(render(data))
        print(f"Rendered: {dst}")
    else:
        base    = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(base, "json", "exam_instructions")
        out_dir = os.path.join(base, "output", "exams")
        os.makedirs(out_dir, exist_ok=True)
        for src in sorted(glob.glob(os.path.join(src_dir, "exam_module_*.json"))):
            with open(src) as f:
                data = json.load(f)
            n   = data["module"]
            dst = os.path.join(out_dir, f"exam-module-{n}.html")
            with open(dst, "w") as f:
                f.write(render(data))
            print(f"Rendered: exam-module-{n}.html")


if __name__ == "__main__":
    main()
