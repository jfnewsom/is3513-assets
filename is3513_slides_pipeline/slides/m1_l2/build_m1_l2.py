"""build_m1_l2.py - IS3513 Module 1, Lab 1.2 Walkthrough: Reconnaissance Tool Exploration.

Renders the 11-slide walkthrough deck described in M1-L2_slide_guide.md (Phase 2
content pass, approved 2026-05-23). Output: /home/claude/M1-L2.pptx.

Second walkthrough deck (after M1-L1). Crawls the Lab 1.2 sheet top to bottom, one
slide per checkpoint, with a warning slot for authorized targets.

Slide map (matches the guide section by section):
     1. title    - Deck opener
     2. concept  - What This Deck Covers
     3. warning  - Your Authorized Targets
     4. concept  - Checkpoint 1: nmap (Network Scanning)
     5. concept  - Checkpoint 2: netcat (Banner Grabbing)
     6. concept  - Checkpoint 3: dirb (Directory Discovery)
     7. concept  - Checkpoint 4: nikto (Web Vulnerability Scanning)
     8. concept  - Checkpoint 5: enum4linux (SMB Enumeration)
     9. concept  - Checkpoint 6: searchsploit (Exploit Research)
    10. guide    - Submitting Lab 1.2 (3 callouts)
    11. support  - What's Next

Pairs with: pages/labs/json/lab1_2_COMPLETE.json (after Patch L2-A applied in the
same session; see M1-L2_phase2_patches.md).
"""
import sys
from pathlib import Path

# Make build_lib (sibling slides/ directory) importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from build_lib import (  # noqa: E402
    DeckBuilder,
    format_concept_notes,
    format_title_notes,
)

OUT = '/home/claude/M1-L2.pptx'


def main():
    deck = DeckBuilder(
        png_out='/home/claude/m1_l2_pngs',
        work='/tmp/build_m1_l2',
    )

    # -----------------------------------------------------------------------
    # Slide 1 - Title
    # -----------------------------------------------------------------------
    deck.add_title_slide(
        course_id='IS3513',
        course_name='Information Assurance and Security',
        subtitle='Module 1, Lab 1.2: Reconnaissance Tool Exploration',
        attribution='PROF. JOHN NEWSOM   \u00b7   SUMMER 2026   \u00b7   SECTION 0XX',
        notes=format_title_notes(
            'M1-L2',
            'Lab 1.2 Walkthrough: Reconnaissance Tool Exploration',
            'Welcome to Lab 1.2. Last lab you built your environment. This lab '
            'you use it for the first time. Six tools, six checkpoints, two '
            'authorized targets. By the end of this lab you will have run the '
            'same workflow professional penetration testers run on day one of '
            'every engagement. You will not be doing anything novel, you will '
            'not be doing anything advanced. You will be practicing the boring '
            'competent version of reconnaissance against two systems that '
            'exist specifically for you to practice on. That is the entire '
            'point. Get the fundamentals locked in before Lab 1.3.',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 2 - What This Deck Covers
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.2',
        title='What This Deck Covers',
        subhead='Six tools, one workflow',
        section_kicker='ORIENTATION',
        card_heading='This is where the M1-C2 vocabulary becomes practice.',
        lead='Six checkpoints, one per tool, ninety minutes to two hours of '
             'work. Same Module1_Screenshots folder you started in Lab 1.1. '
             'Seven new screenshots numbered 07 through 13. Continue the '
             'runbook you started last lab.',
        bullets=[
            'Checkpoints 1 and 2: nmap and netcat. Find what is listening, ask politely.',
            'Checkpoints 3 and 4: dirb and nikto. Map the web layer.',
            'Checkpoints 5 and 6: enum4linux and searchsploit. SMB and exploit research.',
            'Seven new screenshots (07 through 13) into Module1_Screenshots.',
        ],
        notes=format_concept_notes(
            video_script=(
                'The shape of this lab. Six checkpoints, one tool each. '
                'Ninety minutes to two hours depending on how fast the '
                'targets respond, which is mostly out of your control. '
                'First two checkpoints, nmap and netcat. nmap is the '
                'network scanner. Netcat is the manual confirmation tool. '
                'Together they answer the first reconnaissance question: '
                'what services are listening, and what versions are they. '
                'Next two checkpoints, dirb and nikto. Both work against '
                'web servers. dirb finds directories the developers did '
                'not link to. nikto checks for thousands of known web '
                'vulnerabilities. Two different views of the same web '
                'layer. Last two checkpoints, enum4linux and searchsploit. '
                'enum4linux is for SMB, the Windows file-sharing protocol, '
                'which matters more for internal targets than the external '
                'ones in this lab. We will be honest about that when we '
                'get there. searchsploit is your offline Exploit-DB. The '
                'bridge from "I found this version" to "is there a known '
                'exploit." Seven screenshots come out of this lab, '
                'numbered 07 through 13. They go in the same Module 1 '
                'underscore Screenshots folder you started last week. The '
                'runbook you started in Lab 1.1 keeps going. The commands '
                'you run here are exactly what Lab 1.3 Engagement Packet '
                'will need to reproduce. Write them down as you go, with '
                'the reason you ran each one, not just the bash history.'
            ),
            key_terms=[
                ('Reconnaissance',     'information gathering on a target before any active engagement.'),
                ('Service enumeration', 'identifying services running on open ports and their versions.'),
                ('Banner',             'text identifying a service and version, returned on initial connection.'),
            ],
            think_about=[
                'Why does the lab spend time on six tools instead of just teaching the one or two you would use most often?',
                'What would you expect to be different between practicing on scanme.nmap.org and doing this work on a real client?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/labs/Lab1_2_Reconnaissance_Tool_Exploration.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 3 - Your Authorized Targets (WARNING SLOT)
    # The single warning slide in this deck. Authorization stops being theoretical here.
    # -----------------------------------------------------------------------
    deck.add_warning_slide(
        kicker='warning',
        title='Your Authorized Targets',
        subhead='Two targets, two reasons, no exceptions',
        banner='STAY IN SCOPE',
        banner_line='The CFAA does not care that you were learning.',
        rule_kicker='TWO TARGETS',
        rule_oneliner='scanme.nmap.org and testphp.vulnweb.com. Nothing else.',
        rule_body='scanme.nmap.org is the Nmap project official learning target. '
                  'testphp.vulnweb.com is the Acunetix intentionally vulnerable demo '
                  'site. Both are authorized in writing on their respective project '
                  'pages. Every other system on the internet is not authorized for '
                  'you. The cost of getting curious is your career. The cost of '
                  'asking before testing is five minutes.',
        bullets=[
            "Your roommate's laptop is not authorized.",
            "Your employer's network is not authorized.",
            'Random IPs that "look interesting" are not authorized.',
        ],
        notes=format_concept_notes(
            video_script=(
                'This slide gets the warning slot in this deck because Lab '
                '1.2 is the first lab where you point real tools at real '
                'systems. The legal frame stops being theoretical. M1-C1 '
                'covered authorization as a concept. M1-C2 covered '
                'authorization as the practical scoping decision before '
                'reconnaissance. This is the moment authorization becomes '
                'the difference between this lab and a federal crime. '
                'Your two authorized targets for this lab are '
                'scanme.nmap.org and testphp.vulnweb.com. scanme.nmap.org '
                'is operated by the Nmap project. It exists for exactly '
                'this purpose. The site has documentation explaining what '
                'kinds of scanning are welcome and what kinds are not. '
                'Read that page if you have not. testphp.vulnweb.com is '
                'operated by Acunetix, the commercial web vulnerability '
                'scanner company. It is an intentionally broken demo '
                'site, set up so people learning web security can '
                'practice against something that has actual findings. '
                'Both targets are authorized in writing by their owners. '
                'That is what makes them legal to scan. Every other '
                'system on the internet, including ones that look like '
                'obvious practice targets, is not authorized for you. '
                'Your roommate laptop, your old high school website, '
                'your employer systems, your parents router, that '
                'interesting-looking service you noticed yesterday. '
                'None of it is authorized. The Computer Fraud and Abuse '
                'Act does not require damage. It does not require '
                'malicious intent. It requires unauthorized access. '
                'The bar is low and the consequences are not. Stay in '
                'scope. The two targets I named. Nothing else.'
            ),
            key_terms=[
                ('scanme.nmap.org',     'Nmap project official authorized learning target.'),
                ('testphp.vulnweb.com', 'Acunetix intentionally vulnerable demo web application.'),
                ('Scope',               'the systems explicitly authorized for testing in an engagement.'),
                ('CFAA',                'Computer Fraud and Abuse Act, the US federal statute on unauthorized access.'),
            ],
            think_about=[
                'If you are unsure whether a target is authorized, what is the right next step?',
            ],
            source_url='https://nmap.org/book/legal-issues.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 4 - Checkpoint 1: nmap
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.2',
        title='nmap (Network Scanning)',
        subhead='The tool that defines the field',
        section_kicker='CHECKPOINT 1',
        card_heading='The first thing you do on any target. Map what is listening.',
        lead='nmap is the network scanner that defines the field. Every recon '
             'engagement starts with some form of nmap scan. You verified it '
             'works in Lab 1.1. Now you use it.',
        bullets=[
            'nmap -sV runs service and version detection.',
            'nmap -sC runs default safe scripts (NSE) for info gathering.',
            'Two screenshots: 07-nmap-version.png, 08-nmap-scripts.png.',
            'Slow scans are not stuck. Read the scan timing.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint one. nmap. Network mapper. The single most '
                'important tool in reconnaissance, and probably the '
                'most-used security tool in the world. Two flag '
                'combinations to run in this checkpoint. nmap dash s big '
                'V, which runs version detection. nmap dash s big C, '
                'which runs the default Nmap Scripting Engine scripts. '
                'The dash s big V scan tries to identify the service '
                'and the version running on each open port. Apache '
                '2.4.7. OpenSSH 7.6p1. Whatever it finds. The dash s '
                'big C scan runs default NSE scripts, which are '
                'categorized as safe by the Nmap project. These pull '
                'additional information about each service. HTTP titles, '
                'SSH algorithms, SSL certificate details. Both produce '
                'screenshots. 07 dash nmap dash version dot png and 08 '
                'dash nmap dash scripts dot png. Two important things '
                'to know while these run. First, scans take time. The '
                'default nmap behavior is to be respectful of the '
                'target, which means it does not flood the network '
                'with requests. A scan against scanme.nmap.org might '
                'take three to five minutes. That is not the scan '
                'being stuck. That is the scan being polite. Read the '
                'progress indicator if you have one. Second, the '
                'output is sometimes wrong. nmap guesses at versions '
                'based on response signatures. Sometimes the guess is '
                'wrong. When the guess is wrong, you confirm by hand '
                'with netcat, which is the next checkpoint. nmap is '
                'fast and broad. netcat is slow and exact. They are '
                'complements, not duplicates.'
            ),
            key_terms=[
                ('nmap',              'the dominant network scanner.'),
                ('NSE',               'Nmap Scripting Engine. Pluggable scripts that run during a scan.'),
                ('Service detection', 'identifying what software is listening on a port.'),
                ('Version detection', 'identifying which version of that software.'),
            ],
            think_about=[
                'Why does nmap run scans at a deliberate pace by default instead of as fast as possible?',
                "If nmap -sV reports 'Apache 2.4.7' but netcat returns a server banner showing 'nginx,' which do you trust and why?",
            ],
            source_url='https://nmap.org/book/man.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 5 - Checkpoint 2: netcat
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.2',
        title='netcat (Banner Grabbing)',
        subhead='The manual version',
        section_kicker='CHECKPOINT 2',
        card_heading='When automated tools fail, netcat gets you the answer by hand.',
        lead='netcat is the universal TCP/UDP tool. For recon, you connect to a '
             'port and read what the service sends back. No scanning logic, no '
             'version database, just you and the protocol.',
        bullets=[
            'Connect to a port. Read the banner that comes back.',
            'SSH, HTTP, FTP, SMTP, and more announce themselves on connect.',
            'Screenshot: 09-netcat-banner.png.',
            'When nmap is wrong about a service, netcat confirms or contradicts.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint two. netcat. Sometimes called nc on the '
                'command line. The Swiss army knife of TCP and UDP. '
                'For our purposes in this lab, netcat is a banner '
                'grabber. You connect to a port. The service on the '
                'other end usually announces itself in the first few '
                'bytes. You read what it says. That is banner '
                'grabbing. Most network services are chatty by '
                'default. An SSH server returns its software name and '
                'version on connection. An HTTP server returns headers '
                'including a Server header that names the software. '
                'An FTP server returns its name and version in the '
                'welcome banner. An SMTP server returns its '
                'identification in the initial greeting. The banner '
                'is information the service is volunteering. You are '
                'not exploiting anything. You are reading what the '
                'service tells anyone who connects. The command you '
                'will run in this lab is something like nc, the '
                'target hostname, the port number. The connection '
                'opens. The service speaks. You record what it said. '
                'Screenshot 09 dash netcat dash banner dot png. The '
                'reason to learn netcat alongside nmap is that nmap '
                'version detection is sometimes wrong. nmap looks at '
                'response patterns and matches them against a '
                'database of known signatures. Most of the time the '
                'match is right. Sometimes the match is misleading, '
                'especially when administrators have modified or '
                'hidden their banners deliberately. netcat does not '
                'match against a database. netcat just shows you what '
                'came back. When the two disagree, netcat is usually '
                'closer to the truth, because it has no opinion. It '
                'is just reading bytes. That makes netcat the '
                'verification tool. nmap is fast and gets you most of '
                'the way. netcat confirms the things that matter.'
            ),
            key_terms=[
                ('netcat / nc',         'TCP/UDP connection tool, the Swiss army knife of networking.'),
                ('Banner grabbing',     'reading the identifying text a service sends on initial connection.'),
                ('Banner modification', 'when administrators hide or fake their service banners as a weak defense.'),
            ],
            think_about=[
                'Why is banner grabbing considered reconnaissance and not an attack?',
                'If a service has its banner removed or modified, what does that tell you about the administrator?',
            ],
            source_url='https://man7.org/linux/man-pages/man1/ncat.1.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 6 - Checkpoint 3: dirb
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.2',
        title='dirb (Directory Discovery)',
        subhead='Find what they did not link to',
        section_kicker='CHECKPOINT 3',
        card_heading='Web servers rarely tell you about hidden directories. dirb asks.',
        lead='dirb brute-forces a web server by trying common directory and '
             'file names from a wordlist. /admin, /backup, /test, /old. Things '
             'developers forgot to remove or never linked from the front page.',
        bullets=[
            'Brute-force against a wordlist of common paths.',
            'Discovers admin panels, backup files, leftover test directories.',
            'Screenshot: 10-dirb-results.png.',
            'Loud. Logs every request. Authorization is non-negotiable.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint three. dirb. Directory brute-forcer. Web '
                'servers serve whatever path the client requests, even '
                'if no link on the public site points to that path. If '
                'you request slash admin and there is an admin '
                'directory there, the server returns it. If you '
                'request slash old slash backup dot zip and there is a '
                'file at that location, the server returns it. The '
                'question dirb answers is what paths exist that the '
                'public site does not advertise. dirb does this by '
                'running through a wordlist of common path names. The '
                'default Kali wordlist has a few thousand entries. '
                'Admin, login, backup, test, dev, staging, old, '
                'archive, all the predictable names that developers '
                'and administrators use for things they meant to be '
                'temporary. dirb sends an HTTP request for each one '
                'and notes which ones the server returns content for. '
                'The screenshot is 10 dash dirb dash results dot png. '
                'Two important things about dirb. First, it is loud. '
                'Every single request is logged by the web server. If '
                'you ran dirb against a real client without telling '
                'them, the security operations team would see '
                'thousands of suspicious requests from your IP within '
                'minutes. You would be blocked, and depending on the '
                'client, possibly reported. This is why authorization '
                'is non-negotiable for dirb and why we practice on '
                'authorized targets only. Second, dirb finds the '
                'obvious stuff. If you actually need to find hidden '
                'directories on a real engagement, modern tools like '
                'gobuster and feroxbuster are faster and more '
                'thorough. dirb is on the exam because it is the '
                'classic. The newer tools work the same way with '
                'better defaults. Once you understand what dirb does, '
                'the newer tools take ten minutes to pick up.'
            ),
            key_terms=[
                ('Directory brute-forcing', 'requesting common path names against a web server to find unlisted content.'),
                ('Wordlist',                'a file of candidate path names to test.'),
                ('gobuster / feroxbuster',  'modern alternatives to dirb, faster and more configurable.'),
            ],
            think_about=[
                'Why does dirb work at all? Why do web servers not refuse to respond to paths that do not exist on the published site map?',
                'If you find a directory called /backup that returns a downloadable .zip file, what is your next step?',
            ],
            source_url='https://www.kali.org/tools/dirb/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 7 - Checkpoint 4: nikto
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.2',
        title='nikto (Web Vulnerability Scanning)',
        subhead='The loud web scanner',
        section_kicker='CHECKPOINT 4',
        card_heading='nikto checks for thousands of known web issues fast.',
        lead='nikto is a web vulnerability scanner with a database of over '
             '6,000 dangerous files, known misconfigurations, and outdated '
             'server versions. Quick and dirty: point it at a target, read '
             'the report.',
        bullets=[
            'Database of common server misconfigurations and known vulnerabilities.',
            'Reports specific CVEs and CVE-eligible findings.',
            'Screenshot: 11-nikto-results.png.',
            'Generates obvious traffic. Modern WAFs flag nikto signatures instantly.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint four. nikto. Web vulnerability scanner. '
                'nikto job is to check a target web server against a '
                'database of known issues. Dangerous default files '
                'left over from installation. Outdated software '
                'versions with known CVEs. Common server '
                'misconfigurations. Authentication endpoints that '
                'respond to default credentials. The database is over '
                'six thousand entries. Point nikto at a target, wait '
                'a few minutes, read the report. The output is a list '
                'of findings, each one tagged with what nikto thinks '
                'it found, sometimes with a CVE number, sometimes '
                'with an OSVDB reference, sometimes with a link to '
                'more information. Screenshot 11 dash nikto dash '
                'results dot png. Two things you need to know about '
                'nikto. First, it is loud. Even louder than dirb. '
                'Every single check is a separate HTTP request, and '
                'the requests pattern-match obvious nikto signatures. '
                'The user agent string says nikto. The request paths '
                'follow predictable orderings. Any modern web '
                'application firewall recognizes nikto traffic in '
                'the first few requests and blocks it. So running '
                'nikto against a real production target without '
                'authorization will not even complete. The WAF will '
                'cut you off, and the security operations team will '
                'have an incident report on their desk. Authorization '
                'is non-negotiable. Second, nikto produces a lot of '
                'false positives. It checks for the existence of '
                'files that may or may not actually be vulnerable. '
                'A file existing at slash admin slash backup dot zip '
                'might be a real backup, or it might be a default '
                'file the framework ships with, or it might be a '
                'deliberate honeypot. nikto reports the existence, '
                'not the exploitability. The analyst job is to '
                'validate. Read every finding. Confirm what is '
                'actually exposed. Discard the noise.'
            ),
            key_terms=[
                ('nikto',          'command-line web vulnerability scanner.'),
                ('WAF',            'Web Application Firewall, which inspects and filters HTTP traffic.'),
                ('False positive', 'a reported finding that turns out not to be exploitable.'),
                ('CVE',            'Common Vulnerabilities and Exposures, the standard ID system for security flaws.'),
            ],
            think_about=[
                'If nikto reports twenty findings and ten turn out to be false positives, what is your responsibility as the analyst writing this up for a client?',
                'Why would an organization deliberately leave a "honeypot" file at a path nikto will detect?',
            ],
            source_url='https://cirt.net/Nikto2',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 8 - Checkpoint 5: enum4linux (honest framing per John's instruction)
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.2',
        title='enum4linux (SMB Enumeration)',
        subhead='Mostly for internal targets',
        section_kicker='CHECKPOINT 5',
        card_heading='You are verifying the tool works. The real value lands later.',
        lead='enum4linux extracts information from Windows file-sharing '
             'services. Hostname, OS version, shares, users, password policy. '
             'Internet-facing targets rarely expose SMB, so the practice here '
             'is mostly help-output verification. The tool earns its place in '
             'Lab 1.3 and Module 4.',
        bullets=[
            'Designed for Windows SMB and Samba enumeration.',
            'Returns hostnames, shares, users, group memberships, password policy.',
            'Screenshot: 12-enum4linux-help.png (help output only).',
            'Real value: Brazos internal network in Lab 1.3, Alamo in Module 4.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint five. enum4linux. I want to be honest with '
                'you about this checkpoint. Of the six tools in this '
                'lab, this is the one that fits least naturally with '
                'the external scanme.nmap.org and testphp.vulnweb.com '
                'targets. enum4linux is designed for SMB enumeration. '
                'SMB is the Windows file-sharing protocol. It runs on '
                'internal corporate networks. Sometimes it is exposed '
                'to the internet by accident, but on a well-configured '
                'external surface, you should not find SMB. Neither '
                'of our authorized targets exposes SMB. So what you '
                'are actually doing in this checkpoint is running '
                'enum4linux dash h to see the help output, and '
                'verifying that the tool is installed and runs. That '
                'is the screenshot, 12 dash enum4linux dash help dot '
                'png. You are not getting useful intelligence in this '
                'checkpoint. You are confirming the tool works. The '
                'reason it is on the exam, and the reason you verify '
                'it works now, is that enum4linux is one of the '
                'workhorse tools you will use in Lab 1.3 against '
                'Brazos Financial internal network, where SMB does '
                'exist, and again in Module 4 against Alamo '
                'Industries for password security work, where SMB '
                'user enumeration is part of the workflow. Catching '
                'a missing or broken enum4linux now, on the help '
                'command, is much cheaper than catching it the night '
                'before Lab 1.3 is due. Take the screenshot. Move on. '
                'The real demonstration of enum4linux value is two '
                'weeks from now. In your runbook, write down that '
                'you verified the tool works against the help output, '
                'and note that you have not yet tested it against a '
                'real SMB target. That note is the kind of thing a '
                'senior analyst writes. The kind of analyst you are '
                'training to be.'
            ),
            key_terms=[
                ('SMB',        'Server Message Block, the Windows file-sharing protocol.'),
                ('Samba',      'the open-source Linux implementation of SMB.'),
                ('enum4linux', 'tool that extracts identifying information from SMB / Samba services.'),
            ],
            think_about=[
                'Why is SMB typically not exposed to the internet on a well-configured network?',
                'If you ran enum4linux against an internal corporate target and it returned a full user list and password policy, what would that tell you about the target defensive posture?',
            ],
            source_url='https://www.kali.org/tools/enum4linux/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 9 - Checkpoint 6: searchsploit
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.2',
        title='searchsploit (Exploit Research)',
        subhead='From finding to exploiting',
        section_kicker='CHECKPOINT 6',
        card_heading='The bridge from "I found this version" to "is there an exploit."',
        lead='searchsploit is the local search interface to Exploit-DB. Every '
             'recon engagement eventually asks: I found Apache 2.4.7, is there '
             'a known exploit? searchsploit answers in milliseconds, offline.',
        bullets=[
            'Local mirror of Exploit-DB. Works offline.',
            'Search by service name, version, CVE, or keyword.',
            'Screenshot: 13-searchsploit-apache.png.',
            'Update with searchsploit -u. The database evolves daily.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint six. searchsploit. The last checkpoint in '
                'this lab and the bridge to everything that comes '
                'after. searchsploit is the local search tool for '
                'Exploit-DB. Exploit-DB is the canonical public '
                'database of proof-of-concept exploits. Maintained by '
                'Offensive Security, the same organization that runs '
                'OSCP. searchsploit is a Kali utility that searches a '
                'local mirror of the database. You do not need '
                'internet connectivity to use it after the initial '
                'sync. The workflow is simple. You ran nmap. You got '
                'back a service and a version. Apache 2.4.7. OpenSSH '
                '5.3. PHP 5.6. Whatever. You search searchsploit for '
                'that service and version. You get back a list of '
                'known exploits, each one with a path to the exploit '
                'code, the type, the platform, and a publication '
                'date. If there are no results, the version you '
                'found is probably patched against publicly known '
                'issues, or at least nobody has published one. If '
                'there are results, you have a starting point. The '
                'screenshot for this checkpoint is 13 dash '
                'searchsploit dash apache dot png. The lab has you '
                'search for Apache, since the targets are running '
                'Apache. You will see dozens of results, because '
                'Apache has had a lot of CVEs over the years, and '
                'Exploit-DB has accumulated proof-of-concept code '
                'for many of them. The important habit to '
                'internalize here is searchsploit dash u. That '
                'command updates the local database. Exploit-DB '
                'grows daily as new exploits are published. If your '
                'local mirror is six months old, your searchsploit '
                'results are six months out of date. Run '
                'searchsploit dash u once a week, or before any '
                'engagement, so you are looking at current data. '
                'That is the entire workflow. nmap finds the '
                'version. searchsploit checks if it is exploitable. '
                'The Module 4 password lab, the Module 5 '
                'vulnerability assessment, the Lab 1.3 client work, '
                'all of it leans on this pattern.'
            ),
            key_terms=[
                ('Exploit-DB',   'public database of proof-of-concept exploits, maintained by Offensive Security.'),
                ('searchsploit', 'local search tool for Exploit-DB, ships with Kali.'),
                ('CVE',          'Common Vulnerabilities and Exposures, the standardized ID for known security flaws.'),
            ],
            think_about=[
                'If searchsploit returns a proof-of-concept exploit dated 2017 for a service version your target is running, what does that tell you about the target patch management?',
                'Why is it important to update searchsploit (`searchsploit -u`) before any engagement?',
            ],
            source_url='https://www.exploit-db.com/searchsploit',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 10 - Submitting Lab 1.2 (guide)
    # -----------------------------------------------------------------------
    deck.add_guide_slide(
        kicker='guide',
        title='Submitting Lab 1.2',
        subhead='Seven screenshots, one quiz, runbook continues',
        callouts=[
            ('SEVEN SCREENSHOTS', 'Numbered 07-13 in Module1_Screenshots',
             '07-nmap-version, 08-nmap-scripts, 09-netcat-banner, 10-dirb-results, '
             '11-nikto-results, 12-enum4linux-help, 13-searchsploit-apache. '
             'Hostname visible in every terminal screenshot.'),
            ('CANVAS QUIZ', 'Take with VM running',
             'Questions reference specific outputs from the tools you just ran. '
             'Keep your terminal open.'),
            ('RUNBOOK', 'This week is the meat of it',
             'The commands you ran here are exactly what your Lab 1.3 EP runbook '
             'needs to reproduce. Write them down with context, not just the '
             'bash history.'),
        ],
        notes=format_concept_notes(
            video_script=(
                'Submitting Lab 1.2. Three things. First, the '
                'screenshots. Seven of them this lab, numbered 07 '
                'through 13. The filenames are fixed. 07 dash nmap '
                'dash version dot png. 08 dash nmap dash scripts dot '
                'png. 09 dash netcat dash banner dot png. 10 dash '
                'dirb dash results dot png. 11 dash nikto dash '
                'results dot png. 12 dash enum4linux dash help dot '
                'png. 13 dash searchsploit dash apache dot png. Same '
                'Module 1 underscore Screenshots folder you started '
                'in Lab 1.1, so you end this week with eleven '
                'screenshots in there. Every terminal screenshot '
                'needs your kali-abc123 hostname visible. If your '
                'prompt does not show your hostname, the screenshot '
                'does not validate during grading, and the penalty '
                'schedule applies. Second, the Canvas quiz. The Lab '
                '1.2 quiz references specific outputs from the tools '
                'you just ran. Take the quiz while your VM is still '
                'running and your terminal still has the scrollback '
                'from this lab. The quiz is the actual submission '
                'requirement for Lab 1.2. Third, and this is the '
                'one that pays off in two weeks. The runbook habit. '
                'Last lab I told you to start it. This week is when '
                'the runbook actually becomes useful. The commands '
                'you ran in this lab are the literal core of what '
                'Lab 1.3 Engagement Packet will need to reproduce. '
                'Not the bash history. Bash history is just '
                'commands. The runbook is commands plus reasons. '
                'Why did you run nmap dash s big V before dash s '
                'big C. What did you do with the banner that '
                'netcat returned. Why did you focus on the Apache '
                'findings in nikto and not the others. Those '
                'decisions are what a senior analyst writes down. '
                'That is the kind of runbook that reads like an '
                'analyst wrote it. Start the section for Lab 1.2 '
                'in your runbook now, while the commands are fresh.'
            ),
            think_about=[
                'If you forget to take one of the seven screenshots, what is the actual cost in points, and what is the cost in your Lab 1.3 EP?',
                'What is the difference between a bash history dump and a runbook entry that is actually useful?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/labs/Lab1_2_Reconnaissance_Tool_Exploration.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 11 - What's Next (support)
    # Channel order matches M1-C2 / M1-L1 safe pattern: new label, DISCORD,
    # CALENDLY, new label - avoids _replace_text collisions.
    # -----------------------------------------------------------------------
    deck.add_support_slide(
        kicker='support',
        title="What's Next",
        subhead='Authorized targets become a real client',
        philo_kicker='READ, PRACTICE, ASK',
        philo_heading='The training wheels come off in Lab 1.3.',
        philo_body='Take the Lab 1.2 Canvas quiz, then move to Lab 1.3: Brazos '
                   'Financial Reconnaissance Engagement. The two practice '
                   'targets become one real client. Discord for stuck moments, '
                   'Calendly for one-on-one.',
        channels=[
            ('READING',  'Conklin and White, Chapters 1 and 2'),
            ('DISCORD',  'Post in #module-1-help'),
            ('CALENDLY', 'One-on-one by appointment'),
            ('NEXT LAB', 'Lab 1.3: Brazos Financial Engagement'),
        ],
        notes=format_concept_notes(
            video_script=(
                'That is Lab 1.2. Six tools, seven screenshots, one '
                'workflow you will use for the rest of the course. '
                'Here is what to do next. First, take the Lab 1.2 '
                'quiz in Canvas. Keep your VM running while you '
                'answer. Some questions reference specific outputs. '
                'Second, move to Lab 1.3. Lab 1.3 is the Brazos '
                'Financial Reconnaissance Engagement, and it is '
                'where the training wheels come off. You take the '
                'same six tools, the same workflow, the same '
                'documentation discipline, and you apply them to '
                'Brazos Financial Group. Brazos is a fictional '
                'client, but the engagement is real work. You will '
                'produce an Engagement Packet at the end of Lab 1.3. '
                'That packet is your first piece of client-facing '
                'professional output in this course. It will reuse '
                'the screenshots from this lab and the runbook you '
                'have been writing. If you have been doing the '
                'runbook properly week to week, Lab 1.3 is mostly '
                'assembly. If you have been blowing off the runbook, '
                'Lab 1.3 will be hard. Third, the reading. Conklin '
                'and White Chapters 1 and 2 if you have not done '
                'them yet. The vocabulary from those chapters is '
                'what M1-C1 and M1-C2 scaffolded, and it is what '
                'your runbook should be using. If you get stuck. '
                'Discord, hashtag module 1 help. Faster than '
                'emailing me, because somebody else in your section '
                'almost certainly hit the same issue and posted the '
                'fix. If you need one-on-one time, Calendly. No '
                'regular Zoom. Course is asynchronous. Get to it.'
            ),
            source_url='https://jfnewsom.github.io/is3513-assets/',
        ),
    )

    deck.save(OUT)
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    main()
