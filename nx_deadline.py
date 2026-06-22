#!/usr/bin/env python3
"""
nx_deadline.py — Single source of truth for the "due times" deadline callout.

Every student-facing surface (labs, engagement packets, exams, module overviews)
renders the deadline reminder from the constants and helper below, so the wording
can never drift across pages. Do NOT hand-paste this HTML into a renderer or a
JSON; import render_deadline_callout() instead.

House rules applied here (do not change without John's say-so):
  - Spell out "US Central Time." Never the bare abbreviation "CT."
  - First mention names the home time zone of UT San Antonio.
  - No em dashes. Oxford comma.
  - Uses the existing site.css .nx-callout system (nx-blue variant + Material
    Icons "schedule" clock glyph). No CSS changes required.

Verified against IS3513_Summer_2026_Calendar.md (LOCKED):
  - Lab and Engagement Packet deadlines: 11:59 p.m. US Central Time on due date.
  - Module exams: open Sunday, close the following Tuesday, 11:59 p.m. US
    Central Time (students get Sunday, Monday, and Tuesday to take the exam).
"""

DEADLINE_CALLOUT_TITLE = "All Due Times Are 11:59 p.m. US Central Time"

DEADLINE_CALLOUT_BODY = (
    "Lab and Engagement Packet deadlines are <strong>11:59 p.m. US Central "
    "Time</strong> (the home time zone of UT San Antonio) on their due date, "
    "no matter where you are located. Module exams open Sunday and close the "
    "following Tuesday at the same 11:59 p.m. US Central Time. Canvas enforces "
    "this cutoff automatically, so submit early to be safe."
)


def render_deadline_callout():
    """Return the deadline reminder as an .nx-callout nx-blue block.

    Uses the Material Icons "schedule" clock glyph, matching the icon mechanism
    used across every IS3513 page type (labs, exams, module overviews all link
    site.css and the Material Icons font).
    """
    return (
        '    <div class="nx-callout nx-blue">\n'
        '      <div class="nx-callout-icon">'
        '<span class="material-icons" aria-hidden="true">schedule</span></div>\n'
        '      <div class="nx-callout-body">\n'
        f'        <div class="nx-callout-title">{DEADLINE_CALLOUT_TITLE}</div>\n'
        f'        <p>{DEADLINE_CALLOUT_BODY}</p>\n'
        '      </div>\n'
        '    </div>\n'
    )
