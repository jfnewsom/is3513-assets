# IS3513 Module 1, Chapter 1 Slide Guide

**Deck ID:** M1-C1
**Title:** Introduction and Security Trends
**Source structure:** Conklin & White Ch 1, sections 1 to 7
**Source content:** NIST SPs, CISA advisories, MITRE ATT&CK, (ISC)² Code of Ethics
**Target length:** 20 slides
**Last updated:** 2026-05-22

---

## Slide 1: Title

**Layout:** title

### Slide content
- `course_id`: "IS3513"
- `course_name`: "Information Assurance and Security"
- `subtitle`: "Module 1, Chapter 1: Introduction and Security Trends"
- `attribution`: "PROF. JOHN NEWSOM   ·   SUMMER 2026   ·   SECTION 0XX"

### Video Script

Welcome to Module 1. You are about to start your first week at NEXUS Security as a Junior Analyst, and the first thing you need is a working vocabulary. This deck is the orientation: what computer security actually means as a discipline, who the adversaries are, how they think, and the rules of the road for the people who defend systems. Chapter 1 of your textbook frames the field, and this deck walks you through it the way I want you to think about it. Take the reading after you watch this. The deck gives you the scaffolding. The chapter fills it in with detail. By the time you sit down for Lab 1.1, you should be able to define a threat, name the categories of threat actors, and explain why "I had permission" is the difference between a job and a felony. That last point matters more than any tool you will learn this semester. Let's get started.

---

## Slide 2: What This Deck Covers

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "What This Deck Covers"
- `subhead`: "The mental scaffolding for everything that follows"
- `section_kicker`: "ORIENTATION"
- `card_heading`: "Vocabulary first, tools second."
- `lead`: "You cannot defend what you cannot name. This chapter is the vocabulary chapter. Get the words right and the rest of the semester gets easier."

### Bullets
- Define the foundational terms: threat, vulnerability, risk, exploit.
- Identify the major categories of threat actors and what motivates them.
- Recognize attack categories: opportunistic vs targeted, active vs passive.
- Understand the ethical and legal frame that governs everything we do.

### Video Script

Here is what we are doing in this deck. Four jobs, in this order. First, lock in the foundational vocabulary. Threat, vulnerability, risk, exploit. These four words get misused constantly in the field, and if you misuse them in a client report, you lose credibility fast. A senior analyst will spot it on the first read. Second, identify the categories of threat actors and what motivates them. A script kiddie is not a nation-state, and treating them the same way in a risk assessment means you are wasting the client's money. The motivation matters as much as the technique. Third, learn the attack categories. Was this an opportunistic drive-by, or was your client specifically targeted? Was the attacker passively listening, or actively probing? Those answers shape your defensive posture and your prioritization. Fourth, and this is the most important one, the ethical and legal frame that governs the work. You will spend this semester learning techniques that are illegal to use without authorization. Knowing where the line is, and never crossing it, is part of the job description. By the end of this deck, you should be able to define the core terms cleanly, name the threat actor categories from memory, and explain to a non-technical colleague why authorization is the entire ball game.

### Key Terms

- Threat: a circumstance or event with the potential to cause harm.
- Vulnerability: a weakness that could be exploited by a threat.
- Risk: the potential for loss when a threat exploits a vulnerability.
- Exploit: code or a technique that takes advantage of a vulnerability.

### Think About This

1. Why do you think the textbook spends a whole chapter on vocabulary before any tools?
2. If you had to explain "risk" to your grandparent in one sentence, what would you say?

*Source: https://csrc.nist.gov/glossary*

---

## Slide 3: The Computer Security Problem

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "The Computer Security Problem"
- `subhead`: "Why this field exists and why it keeps growing"
- `section_kicker`: "THE LANDSCAPE"
- `card_heading`: "The defender's job has gotten harder, not easier."
- `lead`: "Every new technology adds attack surface. Every new connection between systems adds another way in. Defenders inherit complexity they did not design."

### Bullets
- The attack surface of a typical organization doubles every few years.
- Most breaches involve human factors, not novel technical exploits.
- Adversaries reuse old techniques because they still work.
- Defenders win when they make the easy attacks unprofitable.

### Video Script

When the textbook talks about "the computer security problem," what it really means is this: the defender's job is structurally harder than the attacker's. An attacker has to find one way in. A defender has to close every way in. As we add more devices, more cloud services, more third-party integrations, the defender's surface area grows and grows. That is the field's core asymmetry, and it is not going away. But here is the part that gets missed when people imagine cybersecurity. Most successful breaches do not involve some brilliant new zero-day. They involve a phished credential, a missing patch from six months ago, an exposed S3 bucket, a default password somebody forgot to change. The Verizon Data Breach Investigations Report puts the human-factor share of breaches above seventy percent year after year, and that number has been stable for a decade. What that tells you as a defender is that you do not need to be brilliant to make a real difference. You need to be consistent. Patch what is known. Train your people on phishing. Verify your configurations. Audit your access. The goal is not to make attacks impossible. The goal is to make the easy attacks unprofitable. Force the attacker to work harder than your neighbor. Most of them will go find an easier target. That is the actual game you are playing.

### Key Terms

- Attack surface: the sum of all the points where an unauthorized user can attempt to enter or extract data.
- Defense in depth: layered security controls so that the failure of one does not mean total compromise.

### Think About This

1. If most breaches use known techniques, why do organizations still get breached?
2. What does "make the easy attacks unprofitable" mean for how you would prioritize a defender's budget?

*Source: https://www.verizon.com/business/resources/reports/dbir/*

---

## Slide 4: Foundational Vocabulary

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Threat, Vulnerability, Risk, Exploit"
- `subhead`: "The four words you will misuse if you are not careful"
- `section_kicker`: "DEFINITIONS"
- `card_heading`: "Precision in vocabulary signals precision in thinking."
- `lead`: "These four words get used interchangeably in casual conversation. In a client deliverable, they have specific meanings. Get them right."

### Bullets
- Threat: a potential cause of an unwanted incident.
- Vulnerability: a weakness that a threat could exploit.
- Risk: the combination of likelihood and impact when threat meets vulnerability.
- Exploit: the actual technique or code that turns a vulnerability into a breach.

### Video Script

Four words. They are not synonyms even though casual conversation treats them like they are. A threat is the bad thing that could happen. A flood is a threat. A ransomware gang is a threat. A disgruntled employee is a threat. Threats exist independently of your systems. They exist whether or not you have any vulnerabilities at all. A vulnerability is a weakness in your system that a threat could take advantage of. An unpatched server is a vulnerability. A weak password is a vulnerability. An employee who has not had phishing training is a vulnerability. Vulnerabilities exist independently of any specific threat. Risk is what happens when those two combine. The likelihood that a real threat finds a real vulnerability, multiplied by the impact if it does. Risk is a calculation. It is the metric that lets you decide which problems to fix first when you cannot fix them all. And you can never fix them all. Exploit is the most concrete of the four. It is the actual code, the actual technique, the actual sequence of commands that uses a vulnerability to do real damage. Metasploit modules are exploits. The proof-of-concept script attached to a CVE is an exploit. When you write up a finding in your Engagement Packet, you will use all four of these words. The client deserves to see them used correctly. Practice this until it is automatic.

### Key Terms

- Threat: potential cause of an unwanted incident (NIST SP 800-30).
- Vulnerability: a weakness in a system that could be exploited (NIST SP 800-30).
- Risk: likelihood times impact when a threat exploits a vulnerability.
- Exploit: code or technique used to take advantage of a vulnerability.

### Think About This

1. A server running an outdated version of Apache: which of the four words describes it?
2. If you had to pick the single most overloaded word in this list, which one and why?

*Source: https://csrc.nist.gov/pubs/sp/800/30/r1/final*

---

## Slide 5: Attack Surface and Attack Vectors

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Attack Surface and Attack Vectors"
- `subhead`: "What attackers see when they look at your client"
- `section_kicker`: "THE ATTACKER VIEW"
- `card_heading`: "Reconnaissance is mapping the attack surface."
- `lead`: "When you scan a target in Lab 1.3, you are not hacking yet. You are documenting what an attacker would see. That document is what risk management is built on."

### Bullets
- Attack surface: every system, service, port, and human that can be reached.
- Attack vector: a specific path an attacker uses to reach a target.
- External attack surface is what the internet can see without credentials.
- Internal attack surface emerges after the first compromise.

### Video Script

Attack surface and attack vector. These two terms sound similar but mean different things, and you will use both in your Lab 1.3 deliverable. Attack surface is the sum total of everything an attacker could potentially reach. Every port that is open. Every web application that is exposed. Every email address that could be phished. Every API endpoint that returns data. Attack surface is a noun. It describes a state. The attack surface gets bigger when you add a new service. It gets smaller when you decommission one. Attack vector is a verb made into a noun. It is the specific path an attacker takes through the surface to reach a target. A phishing email leading to a credential capture leading to a VPN login leading to a database dump. That chain is one attack vector. The same attack surface has multiple possible vectors crossing it. A good penetration test report will document the surface and then walk through the most plausible vectors. In Module 1 you are going to do external reconnaissance against Brazos Financial. What you are really doing is documenting their external attack surface and identifying the most likely vectors. That document becomes the foundation of every recommendation you make to the client. They are not paying you to break in. They are paying you to tell them what an attacker would see and what an attacker would try. The map is the deliverable.

### Key Terms

- Attack surface: total set of points where an attacker could attempt entry.
- Attack vector: a specific path used to attempt a compromise.
- External attack surface: reachable from the public internet without credentials.

### Think About This

1. If a company moves from on-prem to fully cloud, does the attack surface get bigger or smaller? Why?
2. What is the difference between an attack surface and a vulnerability assessment?

*Source: https://attack.mitre.org/tactics/TA0043/*

---

## Slide 6: Zero-Day Attacks

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Zero-Day Attacks"
- `subhead`: "The exploits with no patch and no signature"
- `section_kicker`: "THE WORST CASE"
- `card_heading`: "Zero-day is a state, not a class of attack."
- `lead`: "A zero-day is just a vulnerability the defender did not know existed. The clock starts at zero on the day it goes public. Everything before that, defenders are flying blind."

### Bullets
- Zero-day: a vulnerability unknown to the vendor and the public.
- N-day: a vulnerability that is known and patched, but not patched everywhere.
- Most "zero-day" headlines are actually n-days that defenders ignored.
- CISA maintains the Known Exploited Vulnerabilities (KEV) catalog for this reason.

### Video Script

You will hear the term "zero-day" used all over the place. Most of the time it is being used wrong. A real zero-day is a vulnerability that nobody knows about except the attacker. No patch exists. No signature exists. Defenders are flying blind because they do not even know what to look for. Those are rare and they are expensive. Nation-state actors stockpile them. Commercial brokers sell them for six and seven figures. The headlines that say "zero-day exploited in the wild" are sometimes accurate, but more often they are describing what we call an n-day. An n-day is a vulnerability that has been disclosed and patched, but the patch has not been applied everywhere. CISA tracks these in something called the Known Exploited Vulnerabilities catalog, or KEV. When a CVE shows up in KEV, it means CISA has direct evidence that attackers are actively using it against US targets. As a defender, KEV is your prioritization list. If a vulnerability you have is in KEV, fix it now. As a junior analyst, when you find a CVE in your Lab 1.3 reconnaissance, you check KEV before you write the finding. The catalog tells you whether the threat is theoretical or active.

### Key Terms

- Zero-day: vulnerability unknown to the vendor at the time it is exploited.
- N-day: vulnerability that is publicly known and has a patch available.
- KEV (Known Exploited Vulnerabilities): CISA's catalog of CVEs with active exploitation.

### Think About This

1. Why are zero-days more valuable to attackers than n-days, even though n-days work on more systems?
2. If a CVE has a patch but the patch has not been deployed at the client, is it still a zero-day to them?

*Source: https://www.cisa.gov/known-exploited-vulnerabilities-catalog*

---

## Slide 7: Indicators of Compromise

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Indicators of Compromise (IoCs)"
- `subhead`: "The evidence that something has already gone wrong"
- `section_kicker`: "WHAT DEFENDERS HUNT"
- `card_heading`: "Reconnaissance leaves a trail. So does compromise."
- `lead`: "IoCs are the forensic artifacts of an attacker who has already been inside. Blue teams hunt them. Red teams try not to leave them. As an analyst, you need to recognize both sides."

### Bullets
- File hashes, IP addresses, domain names, registry keys.
- Behavioral indicators: unusual login times, lateral movement patterns.
- IoCs are shared between organizations via STIX, TAXII, and threat intel feeds.
- An IoC is a hypothesis, not a verdict.

### Video Script

Indicators of compromise. IoCs. These are the breadcrumbs an attacker leaves behind. They come in two flavors, and you should know both. Atomic indicators are concrete artifacts. A file hash. An IP address. A domain name. A specific registry key. These are easy to share between organizations and easy to feed into automated detection tools. The catch is that attackers can change them. A new build of malware has a new hash. A rotating C2 infrastructure has new IP addresses every week. Behavioral indicators are harder to evade. A user logging in from two countries in the same hour. A service account suddenly accessing files it never touched before. Lateral movement patterns. These are harder to detect because they require context and baselining, but they are also harder for the attacker to change because they reflect actual attack tradecraft. NIST SP 800-150 covers how organizations share threat intel including IoCs. The big thing to internalize is this: an IoC is a hypothesis. Finding one means "look here, something might be wrong." It is not the conclusion of an investigation. It is the start of one. When you write findings in Lab 1.3, you will not be hunting IoCs, but you will see the other side of this: you will be generating the kind of activity that defenders use IoCs to find.

### Key Terms

- IoC (Indicator of Compromise): forensic artifact suggesting a system has been breached.
- Atomic indicator: a specific value like a hash, IP, or domain.
- Behavioral indicator: a pattern of activity rather than a fixed artifact.
- STIX / TAXII: standardized formats for sharing threat intel.

### Think About This

1. Why would a sophisticated attacker prefer "living off the land" tools like PowerShell over custom malware?
2. If atomic indicators are easy to change, why do organizations still rely on them so heavily?

*Source: https://csrc.nist.gov/pubs/sp/800/150/final*

---

## Slide 8: Threat Actors, Part 1

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Threat Actors: The Opportunists"
- `subhead`: "Script kiddies, hacktivists, organized crime"
- `section_kicker`: "WHO ATTACKS"
- `card_heading`: "Motivation drives method."
- `lead`: "The first three categories of threat actor share one thing: they are not specifically targeting your client. They are looking for the easiest path to whatever they want. Understanding the motivation tells you what to protect."

### Bullets
- Script kiddie: low skill, uses prebuilt tools, motivated by curiosity or status.
- Hacktivist: ideologically motivated, often defacement or DDoS, name on a website matters more than payout.
- Organized crime: financially motivated, professional, runs a business.
- All three exploit the same vulnerabilities. They differ in scale and persistence.

### Video Script

Three categories of threat actor, all of them opportunistic. Script kiddies first. These are low-skill attackers using tools they did not write, often against targets they picked from a list. They are mostly noise, but they generate real damage when they get lucky. A script kiddie running an automated scanner against your client will find the same unpatched Apache that a sophisticated attacker would find. Hacktivists next. Ideologically motivated. They want a message delivered. Their attacks are usually defacement, denial of service, or data leaks that embarrass their target. The damage is reputational more than operational. Anonymous and its various offshoots are the long-running example. Organized crime is the third and by far the most dangerous of the opportunists. These are professionals running a business. Ransomware-as-a-service operators have customer support hotlines. They have brand reputations to maintain because they need future victims to believe that paying gets the data back. Conti, LockBit, ALPHV, Cl0p, Scattered Spider. These are not basement hackers. They are functioning criminal enterprises. The thing to remember about all three is that they are mostly opportunistic. They exploit the same vulnerabilities. They are looking for the easiest target that matches their goal. As a defender, your job is to not be the easiest target.

### Key Terms

- Script kiddie: unskilled attacker using prebuilt tools, often for status or curiosity.
- Hacktivist: ideologically motivated attacker, targeting for political or social impact.
- Organized crime: financially motivated criminal enterprises, often running ransomware operations.

### Think About This

1. If three different threat actors use the same exploit, does the risk to the client change based on which one finds them first?
2. Which of these three would be hardest for a small business to defend against, and why?

*Source: https://www.cisa.gov/topics/cyber-threats-and-advisories*

---

## Slide 9: Threat Actors, Part 2

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Threat Actors: The Patient Ones"
- `subhead`: "Nation-states, insiders, competitors"
- `section_kicker`: "WHO ATTACKS"
- `card_heading`: "Some attackers do not move on."
- `lead`: "The second three categories are not opportunistic. They picked your client on purpose. They have time, resources, and a specific objective. They are also the hardest to detect."

### Bullets
- Nation-state (APT): well-resourced, mission-driven, dwell time measured in months.
- Insider threat: authorized access, hardest to detect, often missed entirely.
- Competitor: corporate espionage, IP theft, often via insider recruitment.
- These three are why "defense in depth" and "zero trust" exist as concepts.

### Video Script

Now the patient ones. Three categories that do not give up when the first attempt fails. Nation-state actors first. Advanced Persistent Threat is the formal term. APT. The word "advanced" is contested because plenty of nation-state campaigns use unsophisticated tools. The word that matters is "persistent." These actors are mission-driven. They have a target list assigned to them, and they keep working that list until they get in or they get reassigned. Dwell time, the amount of time between initial compromise and discovery, can run into months or years. MITRE ATT&CK was built specifically to catalog the techniques these groups use. Insider threats next. The hardest category to detect because the access is authorized. The classic case is the disgruntled employee with privileged credentials. But insider threat also covers the well-meaning employee who clicks a phishing link, and the third-party contractor who has been granted too much access. CERT's insider threat center estimates that the average insider incident takes more than 200 days to detect. Competitors are the last category. Corporate espionage is real and underreported because public disclosure is bad for the victim's stock price. Trade secret theft, recruitment of disaffected employees, supply chain infiltration. These three patient categories are why defense in depth and zero trust exist as concepts. You cannot keep them out. You can only make them work harder, and detect them sooner.

### Key Terms

- APT (Advanced Persistent Threat): typically nation-state actor with long campaigns and specific objectives.
- Dwell time: time between initial compromise and detection.
- Insider threat: malicious or negligent action by someone with authorized access.
- MITRE ATT&CK: knowledge base of adversary tactics, techniques, and procedures.

### Think About This

1. If dwell time is measured in months for an APT, what does that say about prevention versus detection as a strategy?
2. Why might an organization underreport a competitor-attributed breach?

*Source: https://attack.mitre.org/groups/*

---

## Slide 10: Hacker Classifications

**Layout:** two_col

### Card content
- `kicker`: "chapter 1"
- `title`: "Hacker Classifications"
- `subhead`: "The hat colors that signal intent and authorization"
- `left_kicker`: "AUTHORIZED"
- `left_heading`: "White hat"
- `right_kicker`: "UNAUTHORIZED"
- `right_heading`: "Black hat (and gray hat)"

### Left bullets
- Permission in writing before any testing.
- Scope is defined and documented.
- Findings disclosed to the owner.
- This is what you are training to be.

### Right bullets
- No permission. Sometimes no malice either (gray hat).
- May claim "I was helping" after the fact.
- Legal consequences are the same regardless of intent.
- The hat color does not change the law.

### Video Script

The colored hats. White hat, black hat, gray hat. The classification system comes from the old Western movie convention where the good guys wore white hats and the bad guys wore black. In security, the line between them is authorization. A white hat hacker has permission in writing, a defined scope, and a clear disclosure path. That is what you are training to be. You will spend your career getting paid to break things, and the thing that makes it legal is the contract and the scope of work. A black hat has none of that. They break in because they want to. Money, ideology, ego, whatever. They are committing a crime. The gray hat is the interesting case. A gray hat acts without permission but claims to be doing it for benign reasons. They find a vulnerability in your system, they exploit it just enough to prove it works, and then they email you about it and maybe ask for a bounty. The intent is not malicious. The legal status is the same as the black hat. Hat color does not change the law. The Computer Fraud and Abuse Act in the US, and equivalents internationally, do not care about your motivations. They care about authorization. That is the line. Authorization is what separates a career from a conviction.

### Key Terms

- White hat: ethical hacker working with explicit authorization.
- Black hat: malicious hacker operating without authorization.
- Gray hat: unauthorized hacker claiming benign intent.
- CFAA (Computer Fraud and Abuse Act): US federal statute on unauthorized computer access.

### Think About This

1. If a gray hat reports a real vulnerability they found without permission, should the company prosecute them?
2. Why might a company prefer a bug bounty program over relying on gray hats finding things and reporting them?

*Source: https://www.justice.gov/criminal/criminal-ccips*

---

## Slide 11: Disclosure: Responsible vs Full

**Layout:** two_col

### Card content
- `kicker`: "chapter 1"
- `title`: "Vulnerability Disclosure"
- `subhead`: "How findings get from finder to fix"
- `left_kicker`: "COORDINATED"
- `left_heading`: "Responsible disclosure"
- `right_kicker`: "PUBLIC"
- `right_heading`: "Full disclosure"

### Left bullets
- Finder notifies vendor privately.
- Vendor gets a fixed timeline (often 90 days).
- Patch released, then details published.
- Bug bounty programs operationalize this.

### Right bullets
- Finder publishes the vulnerability immediately.
- Public knows. So do attackers.
- Argument: forces vendors to patch fast.
- Reality: defenders scramble while attackers move first.

### Video Script

When somebody finds a vulnerability, there is a decision about how to disclose it. Two models. Responsible disclosure, also called coordinated disclosure, is the model most security professionals follow. You find a bug. You contact the vendor privately. You give them a reasonable amount of time to fix it, often 90 days. They release a patch. Then everybody publishes the details together. Bug bounty programs are responsible disclosure with a payment attached. The finder gets a check. The vendor gets a fix. The users get protected without a public window where attackers know about the bug but defenders cannot patch yet. Full disclosure is the opposite. The finder publishes everything immediately. The argument for full disclosure is that vendors only act under pressure. If the public knows, the vendor cannot bury the issue, and users can take their own mitigation steps even before a patch ships. The argument against is obvious. If you publish a working exploit on Monday, defenders cannot deploy a patch by Tuesday, and attackers absolutely will. CISA publishes guidance on coordinated vulnerability disclosure that is worth reading. As a NEXUS analyst, you will follow coordinated disclosure with clients, and you will encounter situations where a client wants to delay disclosure longer than is responsible. Knowing where the line is part of your job.

### Key Terms

- Responsible disclosure: notify vendor privately, allow time to patch, then publish.
- Full disclosure: publish vulnerability details immediately without coordination.
- Bug bounty: financial reward for responsible disclosure to a participating vendor.
- CVD (Coordinated Vulnerability Disclosure): CISA's preferred model.

### Think About This

1. If a vendor refuses to patch within 90 days, what should the finder do?
2. Why might a researcher choose full disclosure even knowing the risks?

*Source: https://www.cisa.gov/coordinated-vulnerability-disclosure-process*

---

## Slide 12: Attack Categories

**Layout:** two_col

### Card content
- `kicker`: "chapter 1"
- `title`: "Attack Categories"
- `subhead`: "Two ways to slice every attack you will see"
- `left_kicker`: "INTENT"
- `left_heading`: "Opportunistic vs targeted"
- `right_kicker`: "BEHAVIOR"
- `right_heading`: "Active vs passive"

### Left bullets
- Opportunistic: scanning the internet for low-hanging fruit.
- Targeted: specifically picked your client and stuck with it.
- Same exploit, different threat model.
- Same defense priorities feel very different in each case.

### Right bullets
- Passive: listening, watching, gathering. No packets sent.
- Active: probing, scanning, interacting. Detectable.
- Reconnaissance is mostly passive, then active.
- Detection focus differs based on which one you fear.

### Video Script

Two ways to slice every attack. First slice is intent. Opportunistic attackers scan large swaths of the internet looking for anything vulnerable. They are fishing. If your client is exposed, the attacker is happy to take them. If not, the attacker moves on. Most ransomware affiliates work this way. Most botnet recruitment works this way. Targeted attackers picked your client specifically. They have a reason. They will not move on when the first thing fails. They will try harder, longer, and with more creativity. APTs are targeted by definition. So are most corporate espionage cases. So is the disgruntled former employee. Second slice is behavior. Passive attacks listen and watch without sending packets to the target. Reading public records. Scraping LinkedIn. Pulling DNS history. Passive activity is almost impossible to detect because there is no interaction with your systems. Active attacks send packets to the target. Port scans. Login attempts. Anything that touches the wire. Active attacks are detectable in principle, though most organizations are not actually watching their logs closely enough to catch them. In Module 1 you are going to start with passive reconnaissance against scanme.nmap.org and then move to active reconnaissance against the Brazos Financial container. Both slices apply to you. You are opportunistic in your training and targeted in your engagement. You are passive when you Google the target and active when you nmap them.

### Key Terms

- Opportunistic attack: attacker is not specifically targeting this victim.
- Targeted attack: attacker has selected this victim on purpose.
- Passive reconnaissance: information gathering without sending packets to the target.
- Active reconnaissance: information gathering that interacts with the target.

### Think About This

1. If a defender can only invest in detecting one of these four types, which has the highest payoff?
2. Why is passive reconnaissance described as "almost impossible to detect" rather than "impossible"?

*Source: https://attack.mitre.org/tactics/TA0043/*

---

## Slide 13: Security Trends

**Layout:** concept (uses `extra_bullet=` exception path for the 5th item)

### Card content
- `kicker`: "chapter 1"
- `title`: "Security Trends That Matter Right Now"
- `subhead`: "Four incidents in twelve months, one structural pattern"
- `section_kicker`: "THE LANDSCAPE TODAY"
- `card_heading`: "The breach is no longer at one company. It is at a node in a supply chain."
- `lead`: "Use this slide to ground the trend in incidents students will recognize. The Canvas breach hit personally. The other three show the same pattern at industry scale."

### Bullets (4 standard + 1 extra)
- Canvas breach (April to May 2026): ShinyHunters extorted Instructure; data on ~275M users across ~9,000 schools. You were in one of them.
- Salesforce / Salesloft Drift: same threat actor pattern; OAuth tokens from one SaaS vendor reached hundreds of corporate Salesforce tenants.
- Ingram Micro ransomware (July 2025): one distributor outage froze tech procurement worldwide for a week.
- UK retail wave (M&S, Co-op, Harrods): Scattered Spider social-engineered a third-party provider to reach three major chains.
- `extra_bullet`: The lesson: your client's security is now downstream of every vendor they trust.

### Video Script

I want to lead with one you will recognize. Late April this year, Canvas, the learning management system this course runs on, was breached by a group called ShinyHunters. Instructure detected unauthorized access on April 29. The attacker came back through a different Canvas vulnerability on May 7 and defaced the login pages some students saw. By mid-May the group was claiming data on roughly 275 million users across nearly 9,000 schools and universities. Names, email addresses, student ID numbers, and student-to-teacher messages. Instructure reportedly paid the ransom. You were in one of the affected institutions. Why does this matter for Chapter 1? Three reasons. First, it is the textbook example of a supply chain attack. ShinyHunters did not attack the schools. They attacked the vendor that 41 percent of North American higher education depends on, and the blast radius rippled outward. Second, ShinyHunters is the same group behind the Salesforce and Salesloft Drift compromise from last year. Same threat actor, multiple campaigns, escalating impact. That is what organized cybercrime looks like operationally. Third, the UK retail wave that hit Marks and Spencer, the Co-op, and Harrods was a different group, Scattered Spider, using the same shape of attack: compromise a trusted third-party provider, reach into multiple downstream organizations. Different attacker. Same playbook. Ingram Micro is the outlier on this slide because it was a direct ransomware hit rather than a supply chain attack, but the impact story is the same: one distributor down for a week, tech procurement worldwide stalled. The lesson is structural. The breach is no longer at one company. The breach is at a node in a supply chain, and the damage propagates outward. When you write Lab 1.3 recommendations for Brazos, you are not just thinking about Brazos. You are thinking about every third party Brazos depends on, and every customer Brazos depends on.

### Key Terms

- Supply chain attack: compromise of a third party used to reach the actual target.
- OAuth token theft: stealing authorization tokens to gain access without credentials.
- ShinyHunters: financially motivated threat group; tied to the Canvas, Salesloft Drift, and other major 2025 and 2026 supply-chain compromises.
- Scattered Spider: financially motivated threat group active in 2024 and 2025, known for help-desk social engineering.

### Think About This

1. Canvas told institutions there was nothing for them to do. Was that reassuring or worrying, and why?
2. If your client uses 200 SaaS vendors, how many of them are part of your client's attack surface?

*Source: https://www.cisa.gov/news-events/cybersecurity-advisories*
*Source: https://www.instructure.com/incident_update*

---

## Slide 14: Approaches to Computer Security

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Approaches to Computer Security"
- `subhead`: "Risk-based thinking is the only approach that scales"
- `section_kicker`: "THE FRAME"
- `card_heading`: "You cannot fix everything. So you fix the right things."
- `lead`: "Every organization has more vulnerabilities than it has budget to fix. Risk management is the discipline of choosing which ones matter most."

### Bullets
- Identify: know what you have and what threatens it.
- Protect: implement controls proportionate to the risk.
- Detect: assume some attacks will succeed; see them quickly.
- Respond and recover: have a plan before you need it.

### Video Script

The textbook calls this section "approaches to computer security." What it is really describing is the risk-management mindset. Every organization has more vulnerabilities than it has budget to fix. That is just the math. Risk management is the discipline of choosing which ones matter most. NIST's Cybersecurity Framework organizes this into five functions, and these are worth memorizing because they will come up in every module of this course. Identify. Know what you have. Know what threatens it. Know what you cannot afford to lose. Protect. Implement controls proportionate to the risk. Not every system needs the same protection. Not every employee needs the same training. Detect. Assume that some attacks will succeed. The goal is to see them quickly. Mean time to detect is one of the most important metrics in security, and it is consistently terrible across the industry. Respond. When you find an incident, you need a plan. Containment, eradication, recovery. Recover. Get back to business and learn from what happened. The NIST CSF 2.0 added a sixth function called Govern, which sits across all of these. The point of the framework is to make the abstract job of "doing security" into something you can actually plan and budget for. Module 5 returns to this in depth. For now, internalize the five functions. They are the spine.

### Key Terms

- NIST CSF (Cybersecurity Framework): risk-based framework with five core functions plus Govern.
- Identify, Protect, Detect, Respond, Recover: the five CSF functions.
- Govern: added in CSF 2.0, covers organizational context and oversight.
- Mean time to detect (MTTD): average time between compromise and detection.

### Think About This

1. If you had to cut budget across the five functions, which would you cut last and why?
2. Why did NIST add Govern as a sixth function in CSF 2.0?

*Source: https://www.nist.gov/cyberframework*

---

## Slide 15: Ethics in Cybersecurity

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "Ethics in Cybersecurity"
- `subhead`: "The line between job and crime is one signed document"
- `section_kicker`: "THE RULES OF THE ROAD"
- `card_heading`: "Authorization is everything. Everything else is detail."
- `lead`: "You will spend this semester learning techniques that are illegal to use without permission. Knowing the line is part of the work. Crossing it ends careers."

### Bullets
- Get authorization in writing before touching any system you do not own.
- Stay within scope. Document the scope before you start.
- Disclose findings to the owner. Never sell, leak, or sit on them.
- The (ISC)² Code of Ethics is the industry baseline. Read it.

### Video Script

This is the slide I want you to remember if you forget every other slide in this deck. Ethics in cybersecurity is not abstract. It is the difference between a career and a federal conviction. Every technique you will learn in this course is illegal to use without authorization. Nmap against scanme.nmap.org is fine because that target exists specifically to be scanned. Nmap against your roommate's laptop is not fine even if your roommate would not notice. The Computer Fraud and Abuse Act has been used to prosecute people for technical access that caused no damage and that the prosecution itself agreed was harmless. Authorization is the line. Four rules. Get authorization in writing before you touch any system you do not own. Verbal agreements do not protect you. An email from your manager does not protect you. A signed scope-of-work document protects you. Stay within scope. If your engagement is for the external attack surface and you find a way into the internal network, you stop and you call. You do not keep going because it is interesting. Disclose findings to the owner. Never sell them, leak them, or sit on them while you decide what to do. The owner gets them, and then you and the owner decide together what happens next. Read the (ISC)² Code of Ethics. It is short. It is the baseline that the entire profession operates on. I will quiz you on this in the exam.

### Key Terms

- Authorization: written, scoped permission to test a system.
- Scope of work: documented limits of what you may test and how.
- Computer Fraud and Abuse Act (CFAA): US federal statute, primary legal frame for unauthorized access.
- (ISC)² Code of Ethics: industry-standard ethical baseline for security professionals.

### Think About This

1. A friend asks you to test the security of their small business. They are happy to verbally agree but reluctant to sign anything. What do you do?
2. During an engagement you discover something illegal happening at the client. Is that a finding for the client, a finding for law enforcement, or both?

*Source: https://www.isc2.org/ethics*

---

## Slide 16: Authorization Is The Line

**Layout:** warning

### Card content
- `kicker`: "warning"
- `title`: "Authorization Is Non-Negotiable"
- `subhead`: "The one rule that defines this profession"
- `banner`: "READ THIS TWICE"
- `banner_line`: "No authorization means it is a crime. Full stop."
- `rule_kicker`: "THE RULE"
- `rule_oneliner`: "Never run security tooling against any system you do not have written permission to test."
- `rule_body`: "Every tool you learn this semester is legal to use on authorized targets and illegal everywhere else. The Computer Fraud and Abuse Act does not care about your intent. It cares about your authorization. The signed scope-of-work is what makes you a professional rather than a defendant."

### Bullets
- scanme.nmap.org and the Brazos container are explicitly authorized.
- Nothing else is, by default. Ask before you test.
- Curiosity is not a defense in court.

### Video Script

I am putting this on its own slide because I want it to land. Authorization is the line. No exceptions. No gray areas. No "but I was just curious." If you run a tool against a system you do not have permission to test, you have potentially committed a federal crime in the United States, and equivalents exist in every country with cybercrime law. The Computer Fraud and Abuse Act does not require damage. It does not require malicious intent. It requires unauthorized access. That is the bar, and it is low. In this course, you have two explicitly authorized targets. The first is scanme.nmap.org, which exists for exactly this purpose and welcomes scanning. The second is the Brazos Financial Docker container that we provide. That container runs on your machine. You have permission. Everything else is off limits, including, and I want to be specific here, your roommate's laptop, your old high school's website, your employer's systems, your parents' router, and any "interesting" service you happen to notice on the internet. If you want to test something else, ask first. The cost of asking is five minutes. The cost of not asking can be your career and your freedom. This is the rule I will not negotiate on. Take this seriously and you have a future in this field. Do not, and you will not.

### Key Terms

- Authorized target: a system with written permission to be tested.
- Scope-of-work: signed document defining the limits of authorization.

### Think About This

1. Why is "I had good intentions" not a legal defense under the CFAA?

*Source: https://www.justice.gov/criminal/criminal-ccips/file/442156/dl*

---

## Slide 17: How This Connects to Module 1

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "How This Connects to Module 1"
- `subhead`: "The chapter is the why. The labs are the how."
- `section_kicker`: "THE BRIDGE"
- `card_heading`: "Every concept on this deck shows up in your lab work."
- `lead`: "The vocabulary you just learned is not theoretical. You will use it three times in the next three weeks."

### Bullets
- Lab 1.1: build and document your attack platform. You define your own scope.
- Lab 1.2: practice reconnaissance on authorized public targets.
- Lab 1.3: engagement against Brazos Financial. Apply everything.
- Module exam: tests both concepts and lab work together.

### Video Script

Quick map of how this chapter content connects to what you are about to do in the labs. Lab 1.1, you build and document your Kali attack platform. The vocabulary from this deck shows up immediately. You are documenting attack surface, in this case your own toolkit. You are defining scope, in this case what you are authorized to test. You are practicing the documentation discipline that the rest of the course depends on. Lab 1.2, you practice reconnaissance on scanme.nmap.org. The site exists specifically as an authorized target. You will use the six tools we expect you to know by Lab 1.3. Nmap, netcat, dirb, nikto, enum4linux, and searchsploit. Each one maps to one of the concepts in this deck. Lab 1.3 is the Brazos Financial engagement. This is where you apply everything. You will be doing active reconnaissance, mapping their external attack surface, and documenting the findings the way a professional would document them for a client. The Engagement Packet you submit is the deliverable. The Module 1 exam will test both the concepts you saw here and the lab work. If you can explain what you did and why, in your own words, the exam will not be hard. If you cannot, no amount of memorizing will help you.

### Key Terms

- Engagement Packet: the deliverable for Lab X.3, combining timesheet, runbook, and client report.
- Foundation Lab: weekly verification of hands-on work (Labs X.1 and X.2).

### Think About This

1. Which of the four labs in Module 1 sounds most like the work you would want to do for a career?
2. What is one thing from this deck you expect to use in Lab 1.2 next week?

*Source: https://jfnewsom.github.io/is3513-assets/pages/support/module_1_overview.html*

---

## Slide 18: For Your Study Sheet

**Layout:** guide

### Card content
- `kicker`: "guide"
- `title`: "For Your Study Sheet"
- `subhead`: "What to lock in before the Module 1 exam"

### Callouts
- (`DO THIS`, `Memorize the four words`, "Threat, vulnerability, risk, exploit. If you can use these four correctly in a sentence, half the exam goes easier.")
- (`HEADS UP`, `Threat actor categories will be tested`, "Both the opportunistic three and the patient three. Know motivation, capability, and what they target. The exam will give you a scenario and ask which category.")
- (`USEFUL TO KNOW`, `Ethics questions are exam staples`, "Expect at least one scenario question on authorization or disclosure. The right answer is always the one that respects the scope and the law.")

### Video Script

Three things to lock in before the Module 1 exam. First, memorize the four foundational words. Threat, vulnerability, risk, exploit. If you can use these correctly in a sentence, half the exam questions get easier because the wrong answers usually misuse them and the right answer uses them correctly. Practice writing two-sentence descriptions of real incidents using all four words. Second, know the threat actor categories cold. All six of them. The opportunistic three were script kiddie, hacktivist, organized crime. The patient three were nation-state, insider, competitor. The exam will give you a scenario and ask you to pick the most likely category. The way to get these right is to think about motivation, capability, and target selection. A script kiddie does not have nation-state capability. A nation-state actor does not bother with random small-business defacement. Third, expect at least one ethics question. Probably a scenario. You will see something like, "an analyst discovers a vulnerability in a system they were not contracted to test. What is the correct next step?" The right answer is always the one that respects the scope of the original authorization and the rights of the system owner. Curiosity is not a defense, even on an exam. Read the study worksheet before the exam. It is on the support page. It maps directly to what I am going to ask.

### Think About This

1. If you had to pick three terms from this entire deck to drill until you could define them in your sleep, which three?
2. How would you teach the threat actor categories to a friend who is not in the course?

*Source: https://jfnewsom.github.io/is3513-assets/pages/support/study_worksheets/module_1_worksheet.html*

---

## Slide 19: The NEXUS Frame

**Layout:** concept

### Card content
- `kicker`: "chapter 1"
- `title`: "The NEXUS Frame"
- `subhead`: "Why we teach both sides of the table"
- `section_kicker`: "THE MINDSET"
- `card_heading`: "You cannot defend what you do not understand how to attack."
- `lead`: "NEXUS does purple team work. Red team to find the gaps. Blue team to close them. This course teaches both because the field needs both."

### Bullets
- Red team thinks like an attacker, finds the gaps.
- Blue team builds the defenses, watches the logs, responds to incidents.
- Purple team puts both perspectives in the same room.
- By Module 5 you will have practiced both.

### Video Script

One more frame before we close out this deck. NEXUS is a purple team consulting firm. The red and blue references come from military exercises. Red team plays the adversary. Blue team plays the defender. Purple team is what happens when you put them in the same room and have them learn from each other. The premise of this course, the premise of the whole NEXUS model, is that you cannot defend what you do not understand how to attack. If you have never sat in front of a network and tried to find the way in, you have a hard time predicting where attackers will go. And if you have never tried to detect that activity in a SOC, you have a hard time understanding what your attacks look like from the defender's chair. By the end of this semester, you will have done both jobs in some form. Module 1 you do reconnaissance against Brazos Financial. That is red work. Module 3 you do live traffic analysis for Gulf Coast Healthcare. That is blue work. Module 4 you crack passwords on Alamo Industries. That is red work that informs blue defenses. Module 5 you assess risk for LoneStar DevOps. That is the integration. Some of you will discover this semester that you love one side more than the other. That is fine. The CPTC team is the red side. The CCDC team is the blue side. We recruit from this course for both.

### Key Terms

- Red team: adversary-simulation role, focused on offensive techniques.
- Blue team: defender role, focused on detection, response, and hardening.
- Purple team: integration of red and blue, often as a single engagement model.
- CPTC / CCDC: UTSA's competition teams (Collegiate Penetration Testing Competition; Collegiate Cyber Defense Competition).

### Think About This

1. Which side of the table sounds more interesting to you right now, before you have done any of the lab work?
2. Why might a person who is good at red team work struggle to be good at blue team work, and vice versa?

*Source: https://attack.mitre.org/*

---

## Slide 20: What's Next

**Layout:** support

### Card content
- `kicker`: "support"
- `title`: "What's Next"
- `subhead`: "Where to go from here this week"
- `philo_kicker`: "READ, PRACTICE, ASK"
- `philo_heading`: "The deck is the scaffolding. The chapter is the detail."
- `philo_body`: "This week: read Conklin and White Chapter 1, work through the Module 1 study worksheet, and start Lab 1.1. Get on Discord if you get stuck. Calendly for one-on-one time."

### Channels
- (`STUDY SHEET`, `Module 1 Worksheet on the support page`)
- (`DISCORD`, `Post in #lab-help`)
- (`CALENDLY`, `One-on-one by appointment`)
- (`NEXT DECK`, `M1-C2: General Security Concepts`)

### Video Script

That is Chapter 1. Here is what you do this week. Read the chapter. Pages 1 through 20 in Conklin and White. The deck gave you the scaffolding. The reading fills it in. Then work through the Module 1 study worksheet. Link is on the support page. It tracks directly to what I will ask on the exam, and it is the single most useful thing you can do to prepare. Then start Lab 1.1, which is environment setup. Get Kali installed, get Docker running, verify the six tools. The lab page has everything you need. If you get stuck, get on Discord. Lab-help is the channel. Posting there is faster than emailing me because your classmates probably hit the same issue and somebody already knows the fix. For anything personal or anything you do not want public, email or Calendly. I do not have a regular Zoom this semester. The next deck in this sequence is M1-C2, General Security Concepts. That covers the CIA triad, security principles, access control, and the rest of Chapter 2. It pairs with Lab 1.2. Watch that one before you start Lab 1.2. For now, you have enough to read the chapter and start Lab 1.1. Get to it.

### Think About This

(none, this is the closer)

*Source: https://jfnewsom.github.io/is3513-assets/*

---

# Build Notes

When this guide is translated to `build_m1_c1.py`:

- The `module_slide` (slide layout 10) is **not used** in M1-C1. Module overview is for a separate deck if we choose to make one, or could replace slide 17 if you want a more visual lab-by-lab grid.
- The `intro_slide`, `team_slide`, `stats_slide`, `structure_slide`, and `policy_slide` layouts are not used in M1-C1. They will likely be used in lab walkthrough decks and the first-day welcome deck.
- Slide 16 (warning) is the **only** warning slide in this deck. Per locked rule: use sparingly.
- Slide 18 uses the **guide** layout (three stacked callouts).
- Slide 20 uses the **support** layout (the deck closer).
- Slides 10, 11, 12 use the **two_col** layout to break visual monotony from the long concept run (slides 2 through 9 and 13 through 15).

Source URL placement: each concept slide carries one authoritative source link in its speaker notes. No textbook page references in slide content, so the deck survives textbook deprecation.
