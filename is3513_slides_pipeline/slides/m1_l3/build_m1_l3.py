"""build_m1_l3.py - IS3513 Module 1, Lab 1.3 Walkthrough: Brazos Financial Reconnaissance Engagement.

Renders the 12-slide walkthrough deck described in M1-L3_slide_guide.md, reconciled
against the canonical Lab 1.3 JSON state in the repo (post-detour, May 25 2026).
Output: /home/claude/M1-L3.pptx.

Third walkthrough deck. The first Engagement Packet deck — CP3 splits into three
deck slides (Part I / Part II / Quality Pass) because compilation is half the
lab's time.

Slide map:
     1. title    - Deck opener
     2. concept  - What This Deck Covers
     3. concept  - Welcome to Brazos Financial Group
     4. concept  - The Engagement Packet
     5. warning  - Integrity (THIS IS YOUR NAME ON IT)
     6. concept  - CP1: Deploy Brazos Container
     7. concept  - CP2: Full Reconnaissance Workflow
     8. concept  - CP3a: Building Part I (Internal)
     9. concept  - CP3b: Building Part II (Client Deliverable)
    10. concept  - CP3c: Quality Pass
    11. guide    - Submitting Lab 1.3 (3 callouts)
    12. support  - What's Next

Pairs with: pages/labs/json/lab1_3_COMPLETE.json (current canonical, post-detour).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from build_lib import (  # noqa: E402
    DeckBuilder,
    format_concept_notes,
    format_title_notes,
)

OUT = '/home/claude/M1-L3.pptx'


def main():
    deck = DeckBuilder(
        png_out='/home/claude/m1_l3_pngs',
        work='/tmp/build_m1_l3',
    )

    # -----------------------------------------------------------------------
    # Slide 1 - Title
    # -----------------------------------------------------------------------
    deck.add_title_slide(
        course_id='IS3513',
        course_name='Information Assurance and Security',
        subtitle='Module 1, Lab 1.3: Brazos Financial Reconnaissance Engagement',
        attribution='PROF. JOHN NEWSOM   \u00b7   SUMMER 2026   \u00b7   SECTION 0XX',
        notes=format_title_notes(
            'M1-L3',
            'Lab 1.3 Walkthrough: Brazos Financial Reconnaissance Engagement',
            'Welcome to Lab 1.3. Training is over. Brazos Financial Group has '
            'hired NEXUS to assess their external attack surface ahead of an '
            'SEC examination, and you are the analyst assigned to the '
            'engagement. This lab is four to five hours of work that produces '
            'your first professional client deliverable. You will deploy the '
            'Brazos environment, run the full reconnaissance workflow against '
            'it, and compile your findings into a two-part Engagement Packet. '
            'Part I is your internal documentation. Part II is what the '
            'client sees. Both go into one Word document. By the end of this '
            'lab, you have produced something an actual junior analyst would '
            'produce at an actual consulting firm. That is the point.',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 2 - What This Deck Covers
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='What This Deck Covers',
        subhead='Three checkpoints, four to five hours, one .docx',
        section_kicker='ORIENTATION',
        card_heading='Training is over. This is client work.',
        lead='Lab 1.3 is structurally different from 1.1 and 1.2. Two '
             'checkpoints are technical execution (deploy, reconnaissance). '
             'The third checkpoint is half the lab\u2019s time: assemble '
             'everything into a two-part Engagement Packet.',
        bullets=[
            'CP1: Deploy the Brazos Docker container (15 min).',
            'CP2: Full reconnaissance workflow against Brazos (90 min).',
            'CP3: Compile Engagement Packet \u2014 Part I + Part II (120 min).',
            'Submit one .docx to Canvas. Manually graded, 40/60 split.',
        ],
        notes=format_concept_notes(
            video_script=(
                'The shape of Lab 1.3. Three checkpoints, four to five hours, '
                'one single Word document at the end. Checkpoint one is fast. '
                'You pull a Docker image, you start the container, you verify '
                'it is reachable. Fifteen minutes. Checkpoint two is the '
                'technical heart of the lab. You take everything you practiced '
                'in Lab 1.2, the six tools and the workflow, and you apply '
                'them to Brazos as a real client target. Ninety minutes. '
                'Checkpoint three is the part that surprises students. '
                'Compilation. Two hours. Half the lab time. That number is '
                'correct, not a typo. Producing a professional deliverable '
                'takes as long as the technical work that generated the data. '
                'If you are not used to that ratio, it is what real consulting '
                'looks like. The Engagement Packet has two parts. Part I is '
                'internal documentation, the working notes a senior analyst '
                'would expect to see. Timesheet, runbook, analyst reflection. '
                'Part II is the client deliverable. Cover, executive summary, '
                'methodology, findings, risk analysis, recommendations, '
                'appendix. Both parts go in one Word document. You upload that '
                'document to Canvas before the deadline. Grading is manual. '
                'Not auto-graded like the Foundation Labs. A human reads your '
                'packet end to end. The grading split is forty percent Part I, '
                'sixty percent Part II. Sub-weights for each section are in '
                'the lab sheet. Read them.'
            ),
            key_terms=[
                ('Engagement Packet',                   'the two-part deliverable produced by every X.3 lab (Internal + Client).'),
                ('Foundation Lab vs. Engagement Packet', 'Lab 1.1 and 1.2 are Foundation Labs (auto-graded). Lab 1.3 is the Engagement Packet (manually graded).'),
                ('Manual grading',                      'a human grader reads your work end to end against the rubric.'),
            ],
            think_about=[
                'If you have never produced a professional client deliverable before, what is the most common reason students underestimate how long compilation takes?',
                'What is the difference between work that is technically correct and work that is professionally presentable?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/labs/Lab1_3_Brazos_Financial_Reconnaissance_Engagement.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 3 - Welcome to Brazos Financial Group
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='The Client: Brazos Financial Group',
        subhead='Dallas wealth management firm, SEC examination prep',
        section_kicker='CLIENT CONTEXT',
        card_heading='50 things to fix. Budget for 10. Help Ray pick the right 10.',
        lead='Brazos Financial Group is a $2.8B wealth management firm in '
             'Dallas with 450 employees. SEC cybersecurity examination in six '
             'months. They hired NEXUS to assess their external attack '
             'surface so the new CTO can prioritize his fixes. You are the '
             'analyst on the engagement.',
        bullets=[
            'Brazos Financial Group: Dallas, 450 employees, $2.8B AUM, post-merger.',
            'Ray Jimenez, CTO: practical, budget-constrained, frustrated by inherited tech debt.',
            'Engagement scope: external attack surface only. No internal pivoting.',
            'Deliverable: prioritized findings Ray can present to the board.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Your client is Brazos Financial Group. Dallas, Texas. '
                'Mid-sized wealth management firm. Two point eight billion '
                'dollars in assets under management. Four hundred fifty '
                'employees. Founded in 1987. Recently merged with an Austin '
                'firm, which created integration headaches and the technical '
                'debt you are about to enumerate. The reason Brazos hired '
                'NEXUS is they have an SEC cybersecurity examination in six '
                'months and they need to demonstrate reasonable security '
                'controls. Your engagement is the kickoff for that work. '
                'External attack surface assessment. What can an attacker '
                'discover about Brazos without any insider access. Your '
                'primary contact is Ray Jimenez. Ray is the Chief Technology '
                'Officer. He came in post-merger to modernize infrastructure, '
                'and he is dealing with what he describes as fifty things to '
                'fix and budget for ten. The quote in the lab sheet is his '
                'actual signature line: "I have got a list of fifty things '
                'to fix and budget for ten. Help me pick the right ten." '
                'That is your job. Not produce a list of fifty findings. '
                'Produce a prioritized list Ray can present to the board to '
                'justify spending. The board does not care about every '
                'detail. The board cares about the few things that could '
                'cost Brazos a client trust failure or an SEC finding. Your '
                'job is to find them, prioritize them, and write them up in '
                'a way Ray can defend in a budget meeting. Scope. External '
                'only. You are not pivoting into the internal network. You '
                'are not exploiting anything. You are documenting what an '
                'attacker could see from the outside. That is the scope Ray '
                'agreed to and the scope the engagement letter specifies. '
                'Stay in scope.'
            ),
            key_terms=[
                ('AUM',                              'Assets Under Management. The total value of client investments a firm manages.'),
                ('SEC cybersecurity examination',    'regulatory review of an investment adviser\u2019s security program, mandated for SEC-registered firms.'),
                ('External attack surface',          'the systems, services, and information visible to an attacker without insider access.'),
                ('Engagement letter',                'the contract between consulting firm and client that defines scope.'),
            ],
            think_about=[
                'Why would a wealth management firm care more about reputation impact than technical impact when reviewing your findings?',
                'If Ray has budget for 10 fixes and you give him 50 findings, what is his next email to you?',
            ],
            source_url='project: NEXUS_Fictional_Clients_Master',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 4 - The Engagement Packet
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='The Engagement Packet',
        subhead='Part I (Internal) + Part II (Client). One document.',
        section_kicker='EP STRUCTURE',
        card_heading='Same structure in every X.3 lab. Learn it once here.',
        lead='The Engagement Packet is the deliverable for every X.3 lab in '
             'this course. Lab 1.3, Lab 2.3, Lab 3.3, Lab 4.3, Lab 5.2. Same '
             'shape every time. Get the structure into your bones now.',
        bullets=[
            'Part I (40% of grade): Timesheet + Runbook + Analyst Reflection.',
            'Part II (60% of grade): Cover, Executive Summary, Methodology, Findings, Risk, Recommendations, Appendix.',
            'Part I is the analyst\u2019s working file. Part II is what the client reads.',
            'Both parts in one .docx, submitted to Canvas.',
        ],
        notes=format_concept_notes(
            video_script=(
                'The Engagement Packet. This is the structure for every Lab '
                'X.3 in this course, so the time you spend learning it now '
                'pays off four more times this semester. There are two parts. '
                'Part one is internal documentation. Part two is the client '
                'deliverable. Both live in the same Word document. Part one '
                'has three subsections. Timesheet, which logs your hours '
                'across the three units of the module split between internal '
                'training and client billable time. The template will be in '
                'the support pages. Runbook, which is your methodology in '
                'detail. Think of it as a man page for the tools you used. '
                'Each tool gets an entry. What the command is. What it does. '
                'The switches you used and why. The switches you did not use '
                'this time but might use in the future. How you actually used '
                'it and what came back. Future you should be able to '
                'reproduce this engagement from your runbook alone. '
                'Future-other-analyst should be able to pick up your runbook '
                'and continue the work. That is the bar. Analyst Reflection. '
                'The lab structures this into three named pieces, so do not '
                'write one essay. Timesheet self-audit. Professional '
                'reflection. AI methodology reflection. We will spend a slide '
                'on Part one structure to walk through each. Part two is the '
                'client deliverable. Cover page identifying you, the '
                'engagement, the client, the date. Executive Summary, which '
                'we will spend a slide on because it is the hardest section '
                'to do well. Methodology, which is a high-level narrative of '
                'how you approached the engagement, in language Ray and his '
                'board can follow without a security background. Findings, '
                'the technical core. Each finding numbered, titled, '
                'described, with evidence, and an impact assessment. Risk '
                'Analysis, which layers business context on top of the '
                'findings. Recommendations, prioritized into things Ray '
                'could do Monday morning and things that belong in next '
                'quarter budget. Appendix with raw outputs, additional '
                'screenshots, and references. Both parts in one .docx. You '
                'upload to Canvas before the deadline. Grading is manual. '
                'Forty percent on Part one, sixty percent on Part two. '
                'Sub-weights for individual sections are in the lab sheet.'
            ),
            key_terms=[
                ('Part I (Internal Packet)',     'Timesheet, Runbook, Analyst Reflection. 40% of the grade.'),
                ('Part II (Client Deliverable)', 'Cover through Appendix. 60% of the grade.'),
                ('Single .docx',                 'both parts in one Word document, no PDFs.'),
                ('Manual grading',               'a human grader, not an auto-grader.'),
            ],
            think_about=[
                'Why does the same EP structure repeat in every X.3 lab? What is the design intent?',
                'If you were Ray, would you read Part I or Part II first? Why?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/support/Engagement_Packet_Guide.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 5 - Integrity (WARNING SLOT)
    # -----------------------------------------------------------------------
    deck.add_warning_slide(
        kicker='warning',
        title='Integrity',
        subhead='What will zero your grade',
        banner='THIS IS YOUR NAME ON IT',
        banner_line='Your first client deliverable. Set the standard now.',
        rule_kicker='AUTOMATIC ZERO',
        rule_oneliner='Fabricated screenshots, AI-written sections, shared work, PDF instead of .docx.',
        rule_body='AI as a tutor is encouraged. AI as a ghostwriter is not. The '
                  'difference matters and it is visible in the writing. '
                  'Fabricated screenshots \u2014 VM hostnames pasted in, tool '
                  'outputs invented \u2014 get caught by graders who have run '
                  'the same commands. Shared work, including identical phrasing '
                  'with a classmate, is a code-of-conduct violation. Submit '
                  'your own work, in .docx, with hostname visible in every '
                  'terminal screenshot. Those four rules are not negotiable.',
        bullets=[
            'Fabricated screenshots = automatic zero.',
            'AI-generated content (not the same as AI-assisted) = automatic zero.',
            'Shared work or PDF submission = automatic zero.',
        ],
        notes=format_concept_notes(
            video_script=(
                'This slide gets the warning slot because Lab 1.3 is the '
                'first piece of client-facing professional output you put '
                'your name on in this course. Some rules. First, fabricated '
                'screenshots are an automatic zero. The grader has run the '
                'same commands against the same targets and knows what real '
                'output looks like. A faked screenshot is obvious within '
                'seconds. Pretending a tool returned results it did not '
                'return is academic dishonesty, and it cascades into a '
                'worse problem: when Ray\u2019s board sees a finding that '
                'does not match reality, your name is on it. Second, AI as '
                'a writing assistant is permitted. AI as a ghostwriter is '
                'not. The difference is whether the words on the page '
                'reflect your understanding or someone else\u2019s '
                'pattern-matching. Graders read a lot of EPs. They can '
                'tell the difference. The honest move, when you used AI, '
                'is to say so in the Analyst Reflection. Describe what you '
                'used it for and how you validated the output. That is '
                'professional practice and it earns credit. Hiding AI use '
                'that is obvious in the writing loses you credit twice '
                '\u2014 once for the deception and once for the writing '
                'itself, because AI-pattern writing is not what we are '
                'teaching you to produce. Third, shared work is automatic '
                'zero. Two students submitting identical phrasing, '
                'identical screenshots, identical structures, both get '
                'zeros. The Discord channel is for asking clarifying '
                'questions, not for sharing answers. Fourth, the file must '
                'be .docx. Microsoft Word format. Not PDF. Not Google '
                'Docs. Not OpenOffice .odt. If your tool only exports PDF, '
                'learn the .docx export workflow before you start writing. '
                'Wrong format is automatic zero. These four rules are the '
                'floor. Everything else is grading-rubric territory.'
            ),
            key_terms=[
                ('Academic integrity',           'the professional standard of submitting your own work and citing AI or other assistance honestly.'),
                ('Fabricated screenshot',        'an image showing a tool output that did not actually happen on your system.'),
                ('AI-assisted vs. AI-authored',  'assistance is permitted and disclosed. Authorship is not.'),
            ],
            think_about=[
                'If you used AI to clean up the grammar in your Executive Summary, what should you write in the Analyst Reflection?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/support/Engagement_Packet_Guide.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 6 - Checkpoint 1: Deploy Brazos Container
    # Canonical commands from lab1_3_COMPLETE.json
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='Deploy Brazos Container',
        subhead='Pull the image, start the container, verify the target',
        section_kicker='CHECKPOINT 1',
        card_heading='Fifteen minutes. The container runs on your VM.',
        lead='Docker pull and run. The Brazos image is a single container '
             'that simulates the firm\u2019s external infrastructure. Once it '
             'starts, it exposes a set of services on your VM, reachable from '
             'localhost on a known port range.',
        bullets=[
            'docker pull jfnewsom/brazos-financial:latest',
            'docker run with -p flags for ports 80, 443, 22, 445, 8443.',
            'Verify with docker ps. Screenshot 14-brazos-container.png.',
            'Container is now your engagement target on localhost.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint one. Fast checkpoint. Fifteen minutes. You are '
                'deploying the Brazos Financial container on your VM. The '
                'container is a single Docker image that I publish from my '
                'Docker Hub account. It simulates the external surface of '
                'Brazos\u2019s infrastructure. Pull the image with docker pull '
                'jfnewsom slash brazos dash financial colon latest. Then run '
                'the container with docker run dash d and dash p flags for '
                'ports 80, 443, 22, 445, and 8443. The port list is in the '
                'lab sheet exactly. Eighty and four-forty-three are HTTP and '
                'HTTPS. Twenty-two is SSH. Four-forty-five is SMB. '
                'Eighty-four-forty-three is the secondary HTTPS service. '
                'Five services total, all on localhost once the container is '
                'up. Verify the container is up with docker ps. You should '
                'see one container in the running state with all five ports '
                'mapped. Screenshot is fourteen dash brazos dash container '
                'dot png. That is your first screenshot of this lab and it '
                'goes in the same Module 1 underscore Screenshots folder you '
                'started in Lab 1.1. If the container is not running, check '
                'the logs with docker logs brazos. Most common failures are '
                'port collisions, which means something else on your VM is '
                'bound to one of the ports the container wants. The fix is '
                'to stop whatever else is using the port. The lab sheet has '
                'a troubleshooting callout. Once docker ps shows healthy, '
                'you are in business. Brazos is now your engagement target. '
                'From here forward, everything you do is billable time on '
                'the engagement. Note the timestamp in your runbook.'
            ),
            key_terms=[
                ('Docker pull', 'download a container image from a registry.'),
                ('Docker run',  'start a container from an image with specified configuration.'),
                ('Port mapping', 'associating a host port with a container port so services are reachable.'),
            ],
            think_about=[
                'Why does the engagement use a Docker container on your VM instead of giving you a public IP to scan?',
                'If `docker ps` shows the container running but `nmap` can\u2019t see the services, where do you look first?',
            ],
            source_url='https://docs.docker.com/engine/reference/commandline/run/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 7 - Checkpoint 2: Full Reconnaissance Workflow
    # Canonical commands from lab1_3_COMPLETE.json
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='Full Reconnaissance Workflow',
        subhead='All six tools, against one target, with documentation',
        section_kicker='CHECKPOINT 2',
        card_heading='Ninety minutes. The Lab 1.2 workflow against a real client.',
        lead='You ran each of the six tools against scanme.nmap.org in '
             'isolation last lab. Now you run all six against Brazos in '
             'sequence, as one engagement. The technical work is the same. '
             'The documentation discipline is what this checkpoint teaches.',
        bullets=[
            'All six tools in sequence: nmap, netcat, dirb, nikto, enum4linux, searchsploit.',
            'Canonical: nmap -sV -sC -A localhost / dirb http://localhost / nikto -h http://localhost / enum4linux -a localhost.',
            'Minimum 8 screenshots from this checkpoint. Hostname visible.',
            'Document services and versions, not just vulnerabilities.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint two. Ninety minutes. The full reconnaissance '
                'workflow against Brazos. The technical work is the same '
                'workflow you ran in Lab 1.2 against scanme.nmap.org. Six '
                'tools in sequence. The lab sheet has the canonical commands. '
                'First, nmap dash s big V dash s big C dash big A localhost. '
                'That\u2019s service version detection, default scripts, and '
                'aggressive OS detection in one run. Heavy scan, takes a few '
                'minutes, returns everything you need to know about what is '
                'listening. Second, netcat banner grabs on the interesting '
                'services nmap found. Lab does not give you specific netcat '
                'commands because they depend on what nmap returned, so you '
                'adapt from the Lab 1.2 workflow. Third, dirb http colon '
                'slash slash localhost for directory discovery on the web '
                'layer. Fourth, nikto dash h http colon slash slash '
                'localhost for known web vulnerabilities. Fifth, enum4linux '
                'dash a localhost against any exposed SMB. The lab uses '
                'port 445, so SMB is exposed and enum4linux will return '
                'actual results this time, unlike Lab 1.2 where you just '
                'verified the help output. Sixth, searchsploit on every '
                'version you identified in nmap. The minimum is eight '
                'screenshots from this checkpoint. The lab sheet says '
                '"minimum eight" and that is a floor, not a target. If you '
                'take twelve, you have more material for Part two. Every '
                'screenshot needs the kali-abc123 hostname visible. While '
                'you run, document. Not just bash history. Commands plus '
                'reasoning plus results. That goes into your runbook '
                'section of Part one. Severity. Every finding you record '
                'needs an honest severity assessment. Critical, high, '
                'medium, low, informational. You will refine these in '
                'checkpoint three when you do the formal risk analysis. '
                'Cross-reference. When you find a version, searchsploit it. '
                'When you find a CVE, note the CVSS score. The Common '
                'Pitfalls callout in the lab sheet is blunt about this: '
                'incomplete coverage means missing findings. Run all six '
                'tools. Document services and versions, not just the '
                'things that look exploitable.'
            ),
            key_terms=[
                ('Severity', 'Critical, High, Medium, Low, Informational. The standard taxonomy for security findings.'),
                ('CVSS',     'Common Vulnerability Scoring System. The standard 0\u201310 numeric severity score.'),
                ('Evidence', 'the screenshot, command output, or document excerpt that proves a finding is real.'),
            ],
            think_about=[
                'If you identify the same vulnerability through nmap and through nikto, do you write it up once or twice?',
                'What turns a "finding" into something Ray can act on?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/labs/Lab1_3_Brazos_Financial_Reconnaissance_Engagement.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 8 - Checkpoint 3a: Building Part I (Internal Packet)
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='Building Part I (Internal)',
        subhead='Timesheet, Runbook, Analyst Reflection',
        section_kicker='CHECKPOINT 3a',
        card_heading='The analyst\u2019s working file. 40% of the grade.',
        lead='Part I is what a senior analyst would expect from a junior '
             'analyst on the engagement. Working documentation. Three '
             'subsections, each with its own purpose and its own grading weight.',
        bullets=[
            'Timesheet (5%): hours across all three units, internal training vs. client billable.',
            'Runbook (20%): man-page entry per tool used across Labs 1.1, 1.2, and 1.3.',
            'Analyst Reflection (15%): Timesheet Self-Audit, Professional Reflection, AI Methodology Reflection.',
            'Total Part I = 40% of grade.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint three is compilation. The first slide of three. '
                'Building Part one of the Engagement Packet. Part one is '
                'internal documentation. Three subsections. Timesheet first. '
                'The template will be in the support pages. You log hours '
                'across all three units of Module one. Lab one point one was '
                'internal training time, you and the environment. Lab one '
                'point two was internal training time, you and the tools. '
                'Lab one point three has two categories. Internal training, '
                'which is your reading and preparation. And client billable, '
                'which is the actual time you spent working on Brazos. The '
                'split tells Ray, indirectly, how much time was prep and how '
                'much was billable. Five percent of the grade. Quick to do. '
                'Easy to get right. Easy to get wrong if you make up hours '
                'after the fact. Track time as you go. Runbook second. '
                'Twenty percent of the grade. This is the biggest single '
                'chunk of Part one and the one students underestimate. The '
                'format is something like a man page. Each tool gets its '
                'own entry. What the command is. What it does. The switches '
                'you used in this engagement, with a brief description of '
                'what each switch does. The switches you did not use this '
                'time but might use in a future engagement, with notes on '
                'when. How you actually used it on Brazos. What came back. '
                'What you did with the result. Future you should be able to '
                'reproduce the engagement from the runbook alone. A new '
                'analyst joining the engagement should be able to pick up '
                'your runbook and continue. That is the bar. Analyst '
                'Reflection third. Fifteen percent. The lab sheet structures '
                'this into three named pieces, so do not write one essay. '
                'Write three. First, Timesheet Self-Audit. Was there a task '
                'or section that took disproportionately long? Describe what '
                'made it slow. Unfamiliar tool. Unclear instructions. '
                'Troubleshooting an error. Then say what you would do '
                'differently next time. End with this question: if Maya '
                'Rodriguez reviewed your timesheet alongside this '
                'engagement, what would she conclude about your efficiency? '
                'Second, Professional Reflection. What worked. What did '
                'not. If you ran this engagement against Brazos again next '
                'semester with what you know now, what would you do '
                'differently? Be specific. "I would communicate findings '
                'earlier" is useful. "I would be more organized" is not. '
                'Third, AI Methodology Reflection. Where AI helped you on '
                'this engagement and how you validated what it told you. '
                'Strong answers describe a specific moment of help and the '
                'verification step that followed. "I asked Claude to '
                'explain a service banner. I confirmed against the vendor '
                'documentation before writing my finding." That is the '
                'pattern. If you did not use AI, write N slash A. But do '
                'not claim N slash A if your runbook is full of '
                'AI-generated explanations. The grader can tell. No word '
                'floor. No required structure beyond the three pieces. '
                'Honest reflection earns credit. Filler does not.'
            ),
            key_terms=[
                ('Internal training time', 'hours spent on preparation, reading, or skill-building, billed to NEXUS overhead.'),
                ('Client billable time',   'hours spent on engagement-specific work, billed to the client.'),
                ('Man-page style',         'structured per-tool entry with name, description, options, and usage examples.'),
            ],
            think_about=[
                'If you spent two hours debugging a Docker container issue in CP1, is that internal training time or client billable? Why?',
                'The Reflection asks "did you have expectations." If you had no specific expectations going in, is that a problem to admit?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/support/Engagement_Packet_Guide.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 9 - Checkpoint 3b: Building Part II (Client Deliverable)
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='Building Part II (Client Deliverable)',
        subhead='What Ray reads. 60% of the grade.',
        section_kicker='CHECKPOINT 3b',
        card_heading='Five graded sections. The Executive Summary is the money page.',
        lead='Part II is the client deliverable. Different audience than '
             'Part I \u2014 Ray and his board, not a senior analyst. '
             'Different voice \u2014 professional, board-readable, '
             'prioritized. Four additive sections plus mechanical (Cover, '
             'TOC, Appendix) that are graded by deduction.',
        bullets=[
            'Executive Summary (12%): 1 page MAX. Exceeding it = -10% deduction. The money page.',
            'Methodology (7%) + Findings (22%) + Risk Analysis (11%) + Recommendations (8%) = the technical core.',
            'Cover, TOC, Appendix: mechanical. Graded by deductions only (-5%, -5%, -20%).',
            'Total Part II = 60% additive + deductions for missing mechanical sections.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint three b. Building Part two. The client '
                'deliverable. Different audience than Part one. Ray and his '
                'board read this. Not a senior analyst. Seven subsections, '
                'but only four of them are scored on the additive scale. '
                'Cover, table of contents, and appendix are mechanical '
                'sections \u2014 you either have them or you do not. '
                'Missing cover page is a five percent deduction. Missing or '
                'hand-typed table of contents is five percent. Missing '
                'appendix is twenty percent. Those are not graded on '
                'quality; they are graded on existence. The four sections '
                'that get additive scoring are Executive Summary, '
                'Methodology, Findings, and Risk Analysis, plus '
                'Recommendations. Executive Summary. Twelve percent. This '
                'is the hardest section to do well and the most important '
                'section to get right. One page, hard limit. Exceeding one '
                'page is a ten percent deduction on top of the twelve '
                'percent you can earn, so a sloppy long executive summary '
                'loses both ways. The page should not look anemic. Half a '
                'page of sparse bullets reads as "I did not have anything '
                'to say." A full page of dense, well-organized content '
                'reads as "this analyst knows what matters." Required '
                'elements. Overall risk posture in one or two sentences. '
                'Count of findings by severity. Top two or three '
                'recommendations with business framing. Board-readable: '
                'no first person, no command output, no jargon. The money '
                'page for Ray. Every line should tie to business risk or '
                'financial exposure. If you have more than one page of '
                'content, cut the least important things first. Cutting '
                'from the ES does not mean dropping them from the '
                'Engagement Packet. They still appear in Findings. The ES '
                'is curation, not selection. Methodology. Seven percent. '
                'Three to four paragraph narrative of how you approached '
                'the engagement. Phases. Scope. Tools at a high level. '
                'Written for the client, not for security peers. Per-flag '
                'detail belongs in your Runbook in Part one, not here. '
                'Findings. Twenty-two percent. The biggest single chunk '
                'of Part two. Each finding gets a structured entry. '
                'Number sequentially. Descriptive title. Severity. '
                'Affected hosts or services. Description with specific '
                'CVE or vulnerability identifiers where applicable. '
                'Evidence referencing your screenshots or tool output. '
                'Impact in business terms. One-line per-finding '
                'recommendation. Order by severity, highest first. Risk '
                'Analysis. Eleven percent. This is where you layer '
                'business context on top of the technical findings. '
                'Per-finding likelihood times impact. Brazos has '
                'long-tenured high-net-worth clients. A breach of the '
                'client portal is a reputation event, not just a '
                'compliance event. Reference a risk framework where '
                'helpful \u2014 NIST SP 800-30, OWASP risk rating, FAIR. '
                'Differentiated reasoning per finding. Avoid uniform '
                '"high risk" labels with no logic. Recommendations. '
                'Eight percent. Prioritized list of fixes. Monday-morning '
                'fixes versus next-quarter budget items. Each '
                'recommendation specific: what to do, what effort, what '
                'priority window. Each maps to one or more findings. '
                'Where applicable, indicate the control framework \u2014 '
                'CIS Controls, NIST CSF. Why this matters. Ray told us '
                'he has fifty things to fix and budget for ten. Help him '
                'pick the right ten.'
            ),
            key_terms=[
                ('Executive Summary',    'one-page summary written for executive decision-makers, focused on business impact and top recommendations.'),
                ('Methodology (Part II)', 'the client-facing narrative of how you approached the engagement. Distinct from the Runbook (Part I).'),
                ('Findings',             'structured technical issues \u2014 Number, Title, Severity, Affected Hosts, Description, Evidence, Impact.'),
                ('Risk Analysis',        'business context layered on top of technical findings.'),
            ],
            think_about=[
                'If you have eight findings and your Executive Summary only fits four, which four do you cut from the ES?',
                'What is the difference between the Methodology section (Part II) and the Runbook section (Part I)? Why do both exist?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/support/Engagement_Packet_Guide.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 10 - Checkpoint 3c: Quality Pass
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.3',
        title='Quality Pass',
        subhead='Last hour before submission',
        section_kicker='CHECKPOINT 3c',
        card_heading='Do this before you submit. Catches the easy mistakes.',
        lead='The last hour of Lab 1.3 is the quality pass. Ten minutes of '
             'polishing the document mechanically saves you points across '
             'multiple rubric categories. Skipping it is one of the most '
             'common ways to lose easy points.',
        bullets=[
            'Ctrl+A then F9 updates TOC, captions, cross-references, bibliography. Fields not updated = -5%.',
            'Every terminal screenshot: hostname visible (kali-abc123). Missing screenshots = -5% each, floor 20.',
            'References must hit 10 minimum. Each missing = -10%. Vendor docs / RFCs / NIST / CVEs / man pages.',
            'Read the ES out loud. If it doesn\u2019t sound like Ray would read it, rewrite.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint three c. Quality pass. The last hour before '
                'submission. Students who skip this lose easy points across '
                'multiple categories. Students who spend the hour pick up '
                'two to five points. The quality pass is mechanical. Open '
                'the .docx. Select all with Control A. Press F9. That '
                'keyboard shortcut updates every field in the document. '
                'Table of Contents. Figure captions and cross-references. '
                'Bibliography. Any computed values. If you wrote the '
                'document properly using Word fields, this single keystroke '
                'makes everything current and consistent. If you did not '
                'use fields, this is the moment you discover your TOC is '
                'wrong. Note for next semester: use the fields. Screenshots '
                'check. Every terminal screenshot needs your kali-abc123 '
                'hostname visible at the top of the terminal. The grader is '
                'going to check this. A screenshot without the hostname '
                'counts as missing under the penalty schedule. Open every '
                'screenshot. Confirm hostname is there. Fix any that are '
                'missing. References check. Open the Appendix. Count your '
                'references. Minimum ten. They have to meet the source '
                'quality standard. Vendor documentation, RFCs, NIST '
                'publications, CVE entries, the man pages for your tools. '
                'Things that have a stable, authoritative source. Wikipedia '
                'does not count. Tutorial blog posts do not count. The '
                'textbook can count for a couple. Ten quality references is '
                'the floor and it is achievable from your tool runs alone. '
                'Executive Summary check. Read it out loud. Yes, out loud. '
                'If it does not sound like Ray would read it to a board, '
                'rewrite. If you find yourself stumbling over a sentence, '
                'rewrite. The Executive Summary is the section the grader '
                'reads most carefully and the section Ray will scan first. '
                'Time spent here is high-leverage. Final check. Make sure '
                'it is .docx, not .pdf, not .odt, not a Google Drive link. '
                'Upload to Canvas. Done.'
            ),
            key_terms=[
                ('Word fields',            'dynamic content elements (TOC, captions, cross-references) that update when fields are refreshed.'),
                ('Ctrl+A then F9',         'the Microsoft Word keyboard shortcut to update all fields in a document.'),
                ('Source quality standard', 'published documentation, RFCs, NIST publications, peer-reviewed sources. Excludes Wikipedia and tutorial sites.'),
            ],
            think_about=[
                'If your TOC shows page numbers that do not match the actual page numbers, what happened?',
                'Why does reading the Executive Summary out loud catch problems that reading silently does not?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/support/Citations.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 11 - Submitting Lab 1.3 (guide)
    # -----------------------------------------------------------------------
    deck.add_guide_slide(
        kicker='guide',
        title='Submitting Lab 1.3',
        subhead='One .docx, uploaded to Canvas, before the deadline',
        callouts=[
            ('MUST BE DOCX', 'Microsoft Word format only',
             'PDF submissions are an automatic zero. If your authoring tool only '
             'exports PDF, learn the .docx export workflow before you start. '
             'Canvas renames the file on upload, so the local filename does not '
             'matter \u2014 the format does.'),
            ('UPLOAD TO CANVAS', 'Lab 1.3 assignment, before deadline',
             'Late work is not accepted. The drop policy exists for emergencies. '
             'Upload early \u2014 Canvas accepts revisions until the deadline, '
             'so submit a draft if you are worried about technical issues, then '
             'replace it with the final version.'),
            ('BONUS: +5%', 'Additional Recon Tool',
             'Document one reconnaissance tool not covered in Lab 1.2 (gobuster, '
             'theHarvester, feroxbuster, whatweb, sublist3r, etc.) and '
             'demonstrate it against the training targets (scanme.nmap.org or '
             'testphp.vulnweb.com). Include purpose, syntax, example output, '
             'and when you would use it.'),
        ],
        notes=format_concept_notes(
            video_script=(
                'Submitting Lab 1.3. Three things to remember. First, the '
                'format. It must be a .docx. Microsoft Word. Not PDF. Not '
                'Google Docs link. Not .odt. If your authoring tool only '
                'exports PDF, figure out the .docx workflow before you '
                'start writing, not the night before submission. Canvas '
                'renames the file you upload, so do not worry about the '
                'local filename on your machine. The format is what '
                'matters. Wrong format is an automatic zero, full stop. '
                'Second, the upload. Go to the Lab 1.3 assignment in '
                'Canvas. Upload the .docx. Canvas accepts revisions until '
                'the deadline, which means if you have a draft you are '
                'nervous about, upload the draft now and replace it with '
                'the final version later. Late work is not accepted, so '
                'the safest move is to have something uploaded before the '
                'deadline and refine it if you have time. Third, the '
                'bonus. Five percent extra credit for documenting an '
                'additional reconnaissance tool. Not one of the six in '
                'Lab 1.2. Something new. gobuster is a great choice and '
                'natural follow-on to dirb. theHarvester is a great '
                'choice for OSINT-style recon. feroxbuster, whatweb, '
                'sublist3r, dnsrecon, all good. Pick one. Install it on '
                'your VM. Run it against the training targets from Lab '
                '1.2 \u2014 scanme.nmap.org or testphp.vulnweb.com \u2014 '
                'same authorization rules apply. Document it in your '
                'runbook the same way you document the six required '
                'tools. Include purpose, syntax, example output, and '
                'when you would use it. Five points is a lot of grade '
                'for a tool you can pick up in an hour. If you are '
                'sitting on the line between a B and an A, the bonus is '
                'your friend.'
            ),
            think_about=[
                'If you submit a PDF by mistake and realize it before the deadline, what do you do?',
                'The bonus is +5% \u2014 what kind of student should consider doing it?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/labs/Lab1_3_Brazos_Financial_Reconnaissance_Engagement.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 12 - What's Next (support)
    # Safe channel ordering pattern (READING, DISCORD, CALENDLY, NEXT LAB)
    # -----------------------------------------------------------------------
    deck.add_support_slide(
        kicker='support',
        title="What's Next",
        subhead='Module 2: Gulf Coast Healthcare',
        philo_kicker='READ, PRACTICE, ASK',
        philo_heading='New client, new theme. Same Engagement Packet structure.',
        philo_body='Module 2 is Cryptography and Authentication. Your client '
                   'is Gulf Coast Healthcare Partners in Houston. Lab 2.1 is '
                   'Cryptographic Foundations. Lab 2.2 is Authentication '
                   'Systems. Lab 2.3 is the Gulf Coast Certificate '
                   'Remediation engagement \u2014 same Part I + Part II '
                   'structure you just built. Read Conklin & White Chapters '
                   '6 and 11 before Lab 2.1 opens.',
        channels=[
            ('READING',  'Conklin and White, Chapters 6 and 11'),
            ('DISCORD',  'Post in #module-2-help once it opens'),
            ('CALENDLY', 'One-on-one by appointment'),
            ('NEXT LAB', 'Lab 2.1: Cryptographic Foundations'),
        ],
        notes=format_concept_notes(
            video_script=(
                'That is Lab 1.3. Your first Engagement Packet is done. Here '
                'is what to do next. First, breathe. Then upload to Canvas '
                'if you have not. Then move to Module 2. Module 2 is '
                'Cryptography and Authentication. Your new client is Gulf '
                'Coast Healthcare Partners. Twelve thousand employees, '
                'hospital system in Houston. Different industry, different '
                'regulatory environment, different stakes. The clinical '
                'impact of a healthcare breach is materially different from '
                'a financial firm breach, and you will see that in the '
                'engagement framing. The reading for Module 2 is Conklin '
                'and White, Chapters six and eleven. Chapter six is '
                'Applied Cryptography. Chapter eleven is Authentication '
                'and Remote Access. About eighty pages combined. Read both '
                'before Lab 2.1 opens. Module 2 first Foundation Lab is '
                'Lab 2.1, Cryptographic Foundations. The structure of the '
                'module mirrors Module 1. Two Foundation Labs, then one '
                'Engagement Packet at the end. Lab 2.2 is Authentication '
                'Systems. Lab 2.3 is Gulf Coast Certificate Remediation, '
                'where you fix a broken certificate on a patient portal '
                'server. Same Part I plus Part II Engagement Packet '
                'structure you just built. The investment you made in '
                'understanding the EP structure here pays off four more '
                'times this semester. If you got stuck on something in '
                'this lab, post in module-1-help on Discord. Other '
                'students hit the same issues. If you need one-on-one '
                'time, Calendly is open. Lab 1.3 is the first big project '
                'of the course. The second through fifth get easier '
                'because the structure is the same. Get to it.'
            ),
            source_url='https://jfnewsom.github.io/is3513-assets/',
        ),
    )

    deck.save(OUT)
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    main()
