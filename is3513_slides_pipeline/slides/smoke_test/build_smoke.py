"""Smoke test for build_lib.py: produces a 12-slide deck exercising every method."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build_lib import DeckBuilder, format_concept_notes, format_title_notes

OUT = '/home/claude/IS3513_Smoke_Test.pptx'

def main():
    deck = DeckBuilder(png_out='/home/claude/smoke_pngs', work='/tmp/build_smoke')

    deck.add_title_slide(
        course_id='IS3513',
        course_name='Information Assurance and Security',
        subtitle='Smoke Test \u2014 All Layouts',
        notes=format_title_notes('SMOKE', 'All-layouts smoke test',
                                  'This deck exercises every method in build_lib.'),
    )

    deck.add_concept_slide(
        kicker='topic',
        title='Concept Slide Test',
        subhead='Card layout with kicker, heading, lead, and bullets',
        section_kicker='THE BIG IDEA',
        card_heading='Concept slides are the workhorse layout.',
        lead='One or two sentences setting up the slide topic. The bullets below carry the structured points.',
        bullets=[
            'Bullet one: short and concrete.',
            'Bullet two: parallel grammar to bullet one.',
            'Bullet three: about one line each.',
            'Bullet four: cap at four; split to a second slide if more.',
        ],
        notes=format_concept_notes(
            video_script='This is the concept slide. Walk through the four bullets.',
            think_about=['What makes a bullet too long?', 'When do you split into two slides?'],
            source_url='https://example.org/concept',
        ),
    )

    deck.add_two_column_slide(
        kicker='topic',
        title='Two-Column Test',
        subhead='Side-by-side parallel content',
        left_kicker='WHAT IT IS',
        left_heading='The shape of the left side',
        left_bullets=['Left one', 'Left two', 'Left three', 'Left four'],
        right_kicker='WHAT IT ISN\u2019T',
        right_heading='The shape of the right side',
        right_bullets=['Right one', 'Right two', 'Right three', 'Right four'],
    )

    deck.add_intro_slide(
        kicker='intro',
        title='Intro Slide Test',
        subhead='Mentor portrait + facts',
        role_kicker='ROLE TAG',
        name='Test Mentor',
        tagline='A one-line italic tagline that captures their voice.',
        facts=['Fact one', 'Fact two', 'Fact three', 'Fact four'],
        pullquote='A short pull-quote that captures perspective.',
    )

    deck.add_team_slide(
        kicker='team',
        title='Team Slide Test',
        subhead='Five mentors',
        members=[
            ('Maya Rodriguez',  'Senior Pentester'),
            ('Marcus Chen',     'NEXUS Founder'),
            ('Carmen Vega',     'OSINT Lead'),
            ('Ray Jimenez',     'Cloud Architect'),
            ('Derek Mitchell',  'Risk Manager'),
        ],
        framing='These are the voices you will hear throughout the semester.',
    )

    deck.add_stats_slide(
        kicker='stats',
        title='Stats Slide Test',
        subhead='Quantitative anchor',
        stats=[
            ('MODULES',          '5'),
            ('FOUNDATION LABS',  '9'),
            ('ENG. PACKETS',     '5'),
        ],
        lead='This is the supporting paragraph that frames the numbers above.',
        bullets=['Bullet about stat one.', 'Bullet about stat two.', 'Bullet about stat three.'],
    )

    deck.add_structure_slide(
        kicker='structure',
        title='Structure Slide Test',
        subhead='Three-card row',
        lead='Each module breaks into three units. This is the layout to show that.',
        cards=[
            ('UNIT 1', 'Training',     'Foundation work and environment setup.'),
            ('UNIT 2', 'Training+',    'Applied work with fewer guardrails.'),
            ('UNIT 3', 'Engagement',   'Client deliverable: the Engagement Packet.'),
        ],
    )

    deck.add_warning_slide(
        kicker='warning',
        title='Warning Slide Test',
        subhead='Use sparingly',
        banner='READ THIS TWICE',
        banner_line='A hard rule that needs to land.',
        rule_kicker='THE RULE',
        rule_oneliner='State the rule once, clearly, no softening.',
        rule_body='Explain the rationale and what happens if the rule is ignored. Body text stays calm.',
        bullets=['Consequence one.', 'Safety net one.', 'Where the line is.'],
    )

    deck.add_support_slide(
        kicker='support',
        title='Support Slide Test',
        subhead='How to reach the instructor',
        philo_kicker='DISCORD FIRST, EMAIL FOR ANYTHING PERSONAL',
        philo_heading='How we talk to each other',
        philo_body='Discord for general questions and peer help. Email for FERPA-sensitive matters.',
        channels=[
            ('DISCORD',   'Post in #course-questions'),
            ('EMAIL',     'john.newsom@utsa.edu'),
            ('CALENDLY',  '1:1 by appointment'),
            ('ZOOM',      'Async \u2014 no weekly Zoom'),
        ],
    )

    deck.add_module_slide(
        number='1',
        title='Threat Intelligence and Reconnaissance',
        labs_value='3 Labs',
        chap_value='Ch 1 & 2',
        client_value='Brazos Financial',
        overview='Module 1 introduces the NEXUS analyst role and the reconnaissance workflow.',
        labs=[
            ('LAB 1.1', 'Environment Setup',       'Internal Training'),
            ('LAB 1.2', 'OSINT Fundamentals',      'Internal Training'),
            ('LAB 1.3', 'Brazos Recon Engagement', 'Client Billable'),
        ],
    )

    deck.add_guide_slide(
        kicker='guide',
        title='Guide Slide Test',
        subhead='Three stacked callouts',
        callouts=[
            ('DO THIS',         'Take action now',     'A specific, time-bounded action item.'),
            ('HEADS UP',        'Watch out for this',  'A common pitfall that trips students up.'),
            ('USEFUL TO KNOW',  'Why this matters',    'The background context that helps the rest stick.'),
        ],
    )

    deck.add_policy_slide(
        kicker='policy',
        title='Policy Slide Test',
        subhead='Four numbered rules',
        rules_kicker='THE FOUR RULES',
        rules=[
            ('Submit DOCX only',     'PDF submissions cannot be parsed and will not be graded.'),
            ('Hostname on screenshots', 'Every screenshot must show your VM hostname kali-abc123.'),
            ('20 screenshots minimum', 'Below 20 triggers per-screenshot penalties.'),
            ('10 references minimum',  'Below 10 triggers per-reference penalties.'),
        ],
    )

    deck.save(OUT)

if __name__ == '__main__':
    main()
