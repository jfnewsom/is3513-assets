"""build_m1_c2.py - IS3513 Module 1, Chapter 2: General Security Concepts.

Renders the 19-slide deck described in M1-C2_slide_guide.md (Phase 2 content
pass, approved 2026-05-23). Output: /home/claude/M1-C2.pptx.

Slide map (matches the guide section by section):
     1. title       - Deck opener
     2. concept     - What This Deck Covers
     3. concept     - Why Vocabulary Matters
     4. structure   - The CIA Triad (3-card row)
     5. concept     - Confidentiality
     6. concept     - Integrity and Non-repudiation
     7. concept     - Availability
     8. structure   - Authentication, Authorization, Accounting (3-card row)
     9. two_col     - Identification vs Authentication
    10. concept     - Authentication Factors
    11. concept     - What Is Access Control?
    12. two_col     - DAC vs MAC
    13. two_col     - RBAC vs ABAC
    14. concept     - Defense in Depth
    15. guide       - Prevent, Detect, Respond (3 stacked callouts)
    16. policy      - Core Security Principles (4 numbered rules)
    17. warning     - Security Through Obscurity Is Not Security
    18. concept     - What This Looks Like in Lab 1.2
    19. support     - Recap and Next Steps

Layouts first-used in this deck (none used in M1-C1): structure, guide, policy.
No extra_bullet slides. All concept slides hold to four bullets.
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

OUT = '/home/claude/M1-C2.pptx'


def main():
    deck = DeckBuilder(
        png_out='/home/claude/m1_c2_pngs',
        work='/tmp/build_m1_c2',
    )

    # -----------------------------------------------------------------------
    # Slide 1 - Title
    # -----------------------------------------------------------------------
    deck.add_title_slide(
        course_id='IS3513',
        course_name='Information Assurance and Security',
        subtitle='Module 1, Chapter 2: General Security Concepts',
        attribution='PROF. JOHN NEWSOM   \u00b7   SUMMER 2026   \u00b7   SECTION 0XX',
        notes=format_title_notes(
            'M1-C2',
            'General Security Concepts',
            'Welcome back. This is the second deck of Module 1. Chapter 1 gave you '
            'the lay of the land. Chapter 2 hands you the toolbox of formal vocabulary '
            'that the rest of the course depends on. The CIA triad, the AAA model, '
            'access control, the core security principles. By the end of this deck '
            'you should be able to use these words correctly in a sentence, recognize '
            'them in a job interview, and spot them in the wild during your lab work. '
            'Lab 1.2 is the practical companion to this deck. Watch this all the way '
            'through before you sit down to do that lab. Let us go.',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 2 - What This Deck Covers
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='What This Deck Covers',
        subhead='The conceptual furniture for everything that follows',
        section_kicker='ORIENTATION',
        card_heading='Four sets of words. Get them right.',
        lead='Chapter 1 told you why this field exists. Chapter 2 gives you the words '
             'to operate in it. These four sets of vocabulary are the load-bearing '
             'structure for the rest of the semester.',
        bullets=[
            'The CIA triad: confidentiality, integrity, availability. The three goals.',
            'The AAA model: authentication, authorization, accounting. The three questions.',
            'Access control models: DAC, MAC, RBAC, ABAC. How systems decide.',
            'Core security principles: least privilege, separation of duties, need to know, implicit deny.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Here is the layout of this deck. Four jobs. First, the CIA triad. '
                'Confidentiality, integrity, availability. These three words are the '
                'goals of every security control you will ever encounter. Encryption, '
                'backups, access lists, firewalls, monitoring \u2014 all of it traces '
                'back to one of these three. Second, the AAA model. Authentication, '
                'authorization, accounting. These are the three questions every system '
                'answers about every action. Who are you, what can you do, what did '
                'you do. Third, the access control models. Four of them. DAC, MAC, '
                'RBAC, ABAC. These are how systems actually make the access decisions. '
                'You will see all four of them in the wild. Fourth, the core security '
                'principles. Least privilege, separation of duties, need to know, '
                'implicit deny. These are the design rules that good security '
                'engineers internalize and bad ones learn the hard way after an '
                'incident. By the end of this deck, you should be able to define each '
                'of these in your own words and recognize them when they show up in a '
                'tool, a policy, or an interview question. Let us get into it.'
            ),
            key_terms=[
                ('CIA triad',     'the three foundational goals of information security.'),
                ('AAA',           'the three operational questions every access decision answers.'),
                ('Access control', 'the mechanism that enforces who can do what.'),
            ],
            think_about=[
                'Of the four areas in this deck, which one do you think gets misused most often in casual conversation?',
                'Why do you think professional certifications spend so much time on vocabulary before tools?',
            ],
            source_url='https://csrc.nist.gov/glossary',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 3 - Why Vocabulary Matters
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='Why Vocabulary Matters',
        subhead='The fastest way to lose credibility is to misuse the words',
        section_kicker='THE STAKES',
        card_heading='You will be judged on word choice as much as technique.',
        lead='Every term in this chapter has a formal definition. Use the wrong one '
             'in a client meeting or an interview and you signal that you do not '
             'actually know the field, regardless of how good your technical work is.',
        bullets=[
            'Mixing up authentication and authorization is the most common novice tell.',
            'Calling a vulnerability a risk costs you credibility on the first read of a report.',
            'Interview panels listen for precision. So do senior analysts on your team.',
            'The labs and the exams use these words on purpose. Imprecise answers lose points.',
        ],
        notes=format_concept_notes(
            video_script=(
                'I want to be direct about why a whole deck on vocabulary exists. The '
                'reason is that this field has formal definitions for words that '
                'sound interchangeable in casual conversation, and the people you '
                'will work with \u2014 clients, senior analysts, hiring managers '
                '\u2014 will judge your competence by how precisely you use them. If '
                'you tell a client that a missing patch is a risk, you have just used '
                'the wrong word. A missing patch is a vulnerability. The risk is what '
                'could happen if it gets exploited and how much it would cost. They '
                'are not the same thing. Same goes for authentication and '
                'authorization. Authentication is proving who you are. Authorization '
                'is what you are allowed to do once you have proven it. Most novice '
                'analysts use these interchangeably, and every senior analyst notices '
                'instantly. The good news is that the formal definitions are not '
                'hard to learn. The textbook gives them to you, this deck reinforces '
                'them, and the labs make you use them. The bad news is that there is '
                'no shortcut. If you cannot define these terms cleanly, you will not '
                'pass the Module 1 exam, you will not write a coherent client '
                'report, and you will not get past a technical interview. Treat this '
                'deck as the most important one in Module 1.'
            ),
            key_terms=[
                ('Vulnerability', 'a weakness in a system that could be exploited.'),
                ('Risk',          'the potential for loss, calculated from threat, vulnerability, and impact.'),
                ('Threat',        'a circumstance with the potential to cause harm.'),
            ],
            think_about=[
                'Why do you think clients judge analysts on vocabulary precision so heavily?',
                'Can you think of another field where the wrong word instantly marks someone as an outsider?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-12/rev-1/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 4 - The CIA Triad (structure)
    # -----------------------------------------------------------------------
    deck.add_structure_slide(
        kicker='chapter 2',
        title='The CIA Triad',
        subhead='Three goals that every security control serves',
        lead='Every security decision can be traced back to one of these three goals. '
             'When you cannot explain which leg of the triad a control protects, you '
             'do not actually understand the control.',
        cards=[
            ('C', 'Confidentiality',
             'Information reaches only the people authorized to see it. Encryption, '
             'access control, classification, redaction. All defenses on this leg.'),
            ('I', 'Integrity',
             'Data is not modified without authorization, and when it is, you can '
             'detect it. Hashes, signatures, version control, write protection.'),
            ('A', 'Availability',
             'Systems are up and reachable when users need them. Redundancy, backups, '
             'capacity planning, DDoS protection.'),
        ],
        notes=format_concept_notes(
            video_script=(
                'The CIA triad. Confidentiality, integrity, availability. Three '
                'goals. Every control in the security toolbox protects at least one '
                'of these legs, and most attacks target at least one of them. The '
                'triad has been the canonical model since the 1970s and it is still '
                'how analysts at every level frame their thinking. Confidentiality '
                'is what most people think of when they hear the word security. '
                'Keeping secrets secret. Encryption, file permissions, '
                'classification, redaction. All of that is confidentiality. '
                'Integrity is the leg that gets less attention but matters just as '
                'much. Integrity is the guarantee that what you stored is what you '
                'read back. If an attacker can change your data and you cannot '
                'detect the change, the data is worthless even if it is technically '
                'still there. Hashes, digital signatures, write-once storage, '
                'version control. All integrity controls. Availability is the leg '
                'analysts forget about because it is unglamorous. Keeping the '
                'system up. Most of an organization actual security spend goes to '
                'availability \u2014 backups, redundancy, capacity, disaster '
                'recovery. Ransomware is the obvious modern example. Ransomware '
                'attacks confidentiality by reading your files, integrity by '
                'encrypting them, and availability by making them unusable. One '
                'attack, three legs. We will spend a slide on each leg next, with '
                'concrete examples. For now, lock these three words in.'
            ),
            key_terms=[
                ('Confidentiality', 'protection from unauthorized disclosure.'),
                ('Integrity',       'protection from unauthorized modification.'),
                ('Availability',    'assurance of timely and reliable access.'),
            ],
            think_about=[
                'Of the three legs, which one do you think your personal data depends on most heavily right now?',
                'Why might a hospital prioritize availability differently than a defense contractor?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/fips/199/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 5 - Confidentiality
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='Confidentiality',
        subhead='Information reaches only the people authorized to see it',
        section_kicker='THE FIRST LEG',
        card_heading="Most of what looks like 'security' is confidentiality protection.",
        lead='Recon, eavesdropping, data theft, and insider exfiltration are all '
             'attacks on this leg. The controls that defend it are everywhere, and '
             'you will use most of them this semester.',
        bullets=[
            'TLS encrypts data in transit. The lock icon in your browser.',
            'AES-256 encrypts data at rest. Full-disk encryption, encrypted databases.',
            'NTFS and Linux file permissions enforce confidentiality at the OS level.',
            'Document classification and redaction protect confidentiality even after sharing.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Confidentiality. The first leg. When you say a system is secure, '
                'what you usually mean is that its confidential data stays '
                'confidential. Encryption is the workhorse here. TLS, the protocol '
                'behind the lock icon in your browser, encrypts data in transit so '
                'somebody sitting on the network between you and the server cannot '
                'read what is going by. AES-256, the standard symmetric cipher, '
                'encrypts data at rest so a stolen laptop or a stolen database '
                'backup is unreadable without the key. Beyond encryption, you have '
                'access control at the operating system level. NTFS permissions on '
                'Windows, POSIX permissions on Linux, ACLs on cloud storage. All of '
                'these enforce confidentiality by deciding who can read which '
                'files. There is also classification, which is the policy layer '
                'above the technical controls. Top Secret, Secret, Confidential, '
                'Public \u2014 labeling data by sensitivity and then applying '
                'controls that match the label. And there is redaction, which is '
                'the discipline of taking confidential information out of a '
                'document before you share it. Done wrong, redaction creates the '
                'classic news headline where the supposedly redacted text turns out '
                'to be selectable. Done right, redaction is the last line of '
                'defense for confidentiality when documents leave their original '
                'system. You will use most of these controls in your Module 1 lab '
                'work, particularly when you start scoping what data your client '
                'cares about protecting.'
            ),
            key_terms=[
                ('Encryption', 'transforming data so only the holder of a key can read it.'),
                ('TLS',        'Transport Layer Security, the protocol that secures most web traffic.'),
                ('AES-256',    'a widely used symmetric encryption standard.'),
            ],
            think_about=[
                'If a laptop is encrypted but the user is logged in when it is stolen, is the data still confidential?',
                'Why is classification policy harder to enforce than technical encryption?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-175b/rev-1/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 6 - Integrity and Non-repudiation
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='Integrity and Non-repudiation',
        subhead='What you stored is what you read back, and you know who put it there',
        section_kicker='THE SECOND LEG',
        card_heading='Detecting unauthorized change, and binding actions to identity.',
        lead='Integrity guarantees data has not been modified without authorization. '
             'Non-repudiation binds that data or action to a specific identity so the '
             'actor cannot deny it later.',
        bullets=[
            'SHA-256 hashes detect any change to a file, even a single bit.',
            'Git commits chain hashes so the entire history is tamper-evident.',
            'Code signing proves the binary you installed came from the vendor.',
            'Digital signatures provide non-repudiation: the signer cannot deny signing.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Integrity. The second leg. Integrity is the guarantee that what '
                'you stored is what you read back. If an attacker can quietly '
                'change your data, the data is worse than useless. It actively '
                'misleads you. The workhorse for integrity is the cryptographic '
                'hash. SHA-256 is the current standard. You compute the hash of a '
                'file when you store it. Later, you recompute the hash and '
                'compare. If even one bit changed, the hash changes completely. '
                'Git uses this idea to build an entire version control system '
                'around tamper-evident history. Every commit in Git is hashed, '
                'and every commit references the hash of its parent, so you '
                'cannot quietly rewrite history without invalidating every hash '
                'that depends on it. Code signing extends the same idea to '
                'software distribution. The vendor signs the installer with their '
                'private key. Your operating system verifies the signature with '
                'their public key. If the binary was tampered with after signing, '
                'the signature does not verify. That is the difference between a '
                'clean install and a supply-chain attack. Now, the related '
                'concept is non-repudiation. Non-repudiation is integrity plus '
                'identity. A digital signature on a contract or an email proves '
                'both that the document has not changed and that a specific '
                'person signed it. The signer cannot later claim they did not '
                'sign, because nobody else has their private key. Non-repudiation '
                'is what makes digital contracts legally enforceable. Integrity '
                'and non-repudiation are easy to confuse on an exam. Integrity is '
                'about the data. Non-repudiation is about the actor.'
            ),
            key_terms=[
                ('Hash',              'a fixed-length fingerprint of data that changes if the data changes.'),
                ('SHA-256',           'the dominant modern cryptographic hash algorithm.'),
                ('Digital signature', 'a hash encrypted with a private key, used to prove origin.'),
                ('Non-repudiation',   'the inability of an actor to deny having performed an action.'),
            ],
            think_about=[
                'If two files have the same SHA-256 hash, what does that tell you?',
                'Why does non-repudiation require both a hash and a private key, not just one?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 7 - Availability
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='Availability',
        subhead='Up and reachable when users need it',
        section_kicker='THE THIRD LEG',
        card_heading='The leg analysts forget about until the system goes down.',
        lead='Confidentiality and integrity get the spotlight. Availability drives '
             'the actual budget. Downtime costs money in real time, and the controls '
             'that prevent it are expensive.',
        bullets=[
            'Redundancy: multiple servers, multiple data centers, multiple ISPs.',
            'Hot, warm, and cold sites are tiers of disaster recovery readiness.',
            'CDNs and anti-DDoS services absorb traffic spikes and attacks.',
            'Backups are availability insurance. Ransomware is an availability attack.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Availability. The third leg, and the one most analysts '
                'underestimate. Confidentiality and integrity are the legs that '
                'get talked about in books and conferences. Availability is the '
                'leg that runs the actual business and consumes the actual '
                'budget. When your client is a hospital or a financial firm, '
                'every minute of downtime is measured in dollars or in patient '
                'safety. The controls for availability look different from '
                'confidentiality and integrity controls. Redundancy is the big '
                'one. Two of everything. Two servers, two data centers, two '
                'internet connections. If one fails, the other carries the load. '
                'Disaster recovery extends that idea to the worst case. A hot '
                'site is a second location that is fully operational and could '
                'take over in minutes. A warm site is partially configured and '
                'takes hours to bring up. A cold site is bare facilities and '
                'takes days or weeks. The trade-off is cost versus recovery '
                'time. Content delivery networks and anti-DDoS services are '
                'availability tools at internet scale. They absorb traffic '
                'spikes, including malicious traffic, so your origin server is '
                'not the single point of failure. And backups. Backups are '
                'availability insurance. If you have good backups and you have '
                'tested your restore process, ransomware is a recoverable '
                'event. If you do not, ransomware is an extinction-level '
                'event. The Colonial Pipeline incident in 2021 was an '
                'availability attack with national consequences, and it traced '
                'back to one credential and inadequate segmentation. That is '
                'what an availability failure costs.'
            ),
            key_terms=[
                ('Redundancy', 'duplicate components so that one failure does not stop the system.'),
                ('DDoS',       'distributed denial of service, a coordinated attack on availability.'),
                ('RTO / RPO',  'recovery time objective, recovery point objective. The two key metrics for backup planning.'),
            ],
            think_about=[
                'If a system is up but slow enough to be unusable, is availability still intact?',
                'Why might a small business prioritize backups over encryption?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-34/rev-1/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 8 - Authentication, Authorization, Accounting (structure)
    # -----------------------------------------------------------------------
    deck.add_structure_slide(
        kicker='chapter 2',
        title='Authentication, Authorization, Accounting',
        subhead='Three questions every system asks about every action',
        lead='If CIA is the goals of security, AAA is the operational mechanics. '
             'Every login, every file access, every API call passes through these '
             'three checks in some form.',
        cards=[
            ('A1', 'Authentication',
             'Who are you? The system verifies the identity you claim. Passwords, '
             'tokens, biometrics, certificates.'),
            ('A2', 'Authorization',
             'What can you do? Once your identity is proven, the system decides '
             'which actions you are allowed to perform.'),
            ('A3', 'Accounting',
             'What did you do? The system logs your actions so the audit trail can '
             'answer that question later.'),
        ],
        notes=format_concept_notes(
            video_script=(
                'The AAA model. Authentication, authorization, accounting. Three '
                'questions. Every access decision in every system passes through '
                'these three checks, even if the system is not explicit about '
                'naming them. Authentication is the first check. Who are you. '
                'The system takes the identity you claim and verifies it. The '
                'verification can be a password, a token, a fingerprint, a '
                'certificate. Authorization is the second check. What can you '
                'do. Once the system knows who you are, it consults the access '
                'control policy and decides which actions you are allowed to '
                'perform. Reading a file is one action. Writing to that file is '
                'a different action. Authorization decides each one. Accounting '
                'is the third check, and the one most often skipped in '
                'introductory treatments. Accounting is the audit trail. The '
                'system logs the action you took, tied to your authenticated '
                'identity, so somebody can answer the question what did you do '
                'later. Accounting is also what makes non-repudiation '
                'operational. If the log says your account performed an action, '
                'and the system has strong authentication, you cannot later '
                'claim it was not you. The three As have to work together. '
                'Authentication without authorization means anyone who logs in '
                'can do anything. Authorization without authentication means the '
                'system trusts whoever claims to be the right user. Either of '
                'those without accounting means there is no way to reconstruct '
                'what happened after an incident. All three. Every system. '
                'Every action.'
            ),
            key_terms=[
                ('AAA',       'authentication, authorization, accounting. The operational triad.'),
                ('Audit log', 'the record of who did what, when, used for accounting.'),
            ],
            think_about=[
                'Which of the three As is hardest to do well in your experience?',
                'Why might a security team prioritize improving accounting before improving authentication?',
            ],
            source_url='https://pages.nist.gov/800-63-4/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 9 - Identification vs Authentication (two_col)
    # -----------------------------------------------------------------------
    deck.add_two_column_slide(
        kicker='chapter 2',
        title='Identification vs Authentication',
        subhead='Claiming an identity is not proving it',
        left_kicker='CLAIM',
        left_heading='Identification',
        left_bullets=[
            'Asserting an identity. Username, email, employee ID.',
            'Anyone can type your username. That is not yet a problem.',
            'Identification is public-by-default in most systems.',
            'It is the question, not the answer.',
        ],
        right_kicker='PROOF',
        right_heading='Authentication',
        right_bullets=[
            'Proving the identity you just claimed.',
            'Password, token, biometric. Combined for real strength.',
            'Identification without authentication is anonymous access.',
            'Authentication strength is your real identity in the system.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Quick but important distinction. Identification and '
                'authentication are not the same thing. Identification is the '
                'moment you tell the system who you are. You type your '
                'username. You enter your email address. You scan your '
                'employee badge. That is identification. It is a claim. Anyone '
                'in the world can type your username. That is not a security '
                'problem yet, because typing somebody username does not let '
                'you do anything as them. Authentication is the next step. '
                'Authentication is when the system asks you to prove that the '
                'identity you just claimed is actually yours. Password. PIN. '
                'Hardware token. Fingerprint. Some combination. Authentication '
                'is what converts a claim into a proven identity. The reason '
                'this matters on an exam and in interviews is that the words '
                'get used interchangeably in casual speech, and they are not '
                'interchangeable in the field. A login screen is doing both. '
                'The username field is identification. The password field is '
                'authentication. If a system only did identification \u2014 if '
                'it just asked who you were and then trusted you \u2014 it '
                'would be a system with no security. That is the difference. '
                'One word is the question. The other is the proof.'
            ),
            key_terms=[
                ('Identification', 'the act of claiming an identity.'),
                ('Authentication', 'the act of proving a claimed identity.'),
            ],
            think_about=[
                'Is your email address a form of identification, authentication, or both?',
                'Why do many systems treat the username field as case-insensitive but the password field as case-sensitive?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-63a/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 10 - Authentication Factors
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='Authentication Factors',
        subhead='Three categories, combined across categories for real strength',
        section_kicker='MFA EXPLAINED',
        card_heading='True multi-factor combines categories. Not two of the same kind.',
        lead='A factor is something an attacker has to obtain or replicate to '
             'impersonate you. The strength of MFA comes from forcing the attacker '
             'to obtain things from different categories at once.',
        bullets=[
            'Something you know: passwords, PINs, passphrases. Replayable if stolen.',
            'Something you have: YubiKey, TOTP app, smart card. Possession is the proof.',
            'Something you are: fingerprint, face, iris. Convenient, unchangeable if leaked.',
            'Real MFA: at least two factors from different categories. Not two passwords.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Authentication factors. Three classical categories, and the '
                'rules for combining them into multi-factor authentication. '
                'Something you know is the first category. Passwords, PINs, '
                'passphrases. The thing you carry in your head. The weakness '
                'here is that anything you know can be stolen, phished, '
                'guessed, or extracted, and once it is stolen the attacker can '
                'replay it indefinitely. Something you have is the second '
                'category. A hardware token like a YubiKey. A TOTP app on your '
                'phone that generates a six-digit code every thirty seconds. '
                'A smart card. The proof is possession of the physical or '
                'virtual object. The strength is that an attacker who only '
                'steals your password cannot log in without also stealing the '
                'device. Something you are is the third category. Biometrics. '
                'Fingerprint, face, iris, voice. The strength is convenience '
                'and uniqueness. The weakness is that biometrics cannot be '
                'reset. If your password leaks, you change it. If your '
                'fingerprint leaks, you have ten fingers and then you are out '
                'of fingers. The whole point of multi-factor authentication is '
                'that an attacker has to defeat two different categories. '
                'Stealing a password is one type of attack. Stealing a YubiKey '
                'is a different type of attack, with different methods, '
                'different physical access, different supply chains. Combining '
                'categories means the attacker has to win both attacks '
                'simultaneously, which is dramatically harder than winning '
                'either one. Two passwords is not MFA. A password plus a '
                'security question is not MFA. They are the same category. A '
                'password plus a TOTP code is MFA. A password plus a '
                'fingerprint is MFA. That is the rule.'
            ),
            key_terms=[
                ('MFA',       'multi-factor authentication, combining factors from different categories.'),
                ('TOTP',      'time-based one-time password, the six-digit codes from authenticator apps.'),
                ('Biometric', 'an authentication factor based on a physical or behavioral trait.'),
            ],
            think_about=[
                'SMS codes are widely used for "MFA." Which category do they belong to, and why are they weaker than a TOTP app or hardware token?',
                'If biometrics cannot be reset when leaked, why have they become so widespread on phones?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-63b/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 11 - What Is Access Control?
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='What Is Access Control?',
        subhead='Subject acts on object. Policy decides if the action is allowed.',
        section_kicker='THE FRAMEWORK',
        card_heading='Every access decision is the same logic, with different policies.',
        lead='Whether you are looking at a Linux file system, a SQL database, or a '
             'cloud IAM console, the structure of an access decision is identical. '
             'Only the policy mechanism changes.',
        bullets=[
            'Subject: the user, process, or system requesting an action.',
            'Object: the file, resource, or data being acted on.',
            'Action: read, write, execute, delete, modify, create.',
            'Decision: allow or deny, based on the policy in force.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Access control. The framework that all four models we are '
                'about to compare are built on. Strip away the names and the '
                'marketing terms, and every access decision in every system is '
                'the same three-part structure. There is a subject. The '
                'subject is the entity requesting to do something. Could be a '
                'human user. Could be a service account. Could be a process '
                'running on the system. Does not matter. The subject is '
                'whoever is asking. There is an object. The object is the '
                'thing being acted on. A file. A database row. An API '
                'endpoint. A network port. The object is what the subject '
                'wants to touch. And there is an action. Read the file. '
                'Write to the file. Execute the program. Delete the row. Each '
                'action is a separate decision. The system then consults a '
                'policy and returns an answer. Allow, or deny. That is it. '
                'That is the whole framework. The four access control models '
                'we are about to look at \u2014 DAC, MAC, RBAC, ABAC \u2014 '
                'differ in one place: who writes the policy and what '
                'attributes the policy considers. The structure itself is the '
                'same in all four. Once you internalize this, the differences '
                'between the models become straightforward. You are just '
                'asking, for each model, who is allowed to write the rule and '
                'what information the rule is allowed to consider.'
            ),
            key_terms=[
                ('Subject', 'the actor requesting access.'),
                ('Object',  'the resource being accessed.'),
                ('Policy',  'the set of rules that determines allow or deny.'),
            ],
            think_about=[
                'Is a background service running as SYSTEM a subject? An object? Both?',
                'Why is it useful to treat all four access control models as the same framework with different policy mechanisms?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-192/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 12 - DAC vs MAC (two_col)
    # -----------------------------------------------------------------------
    deck.add_two_column_slide(
        kicker='chapter 2',
        title='DAC vs MAC',
        subhead='Who decides what gets accessed',
        left_kicker='OWNER DECIDES',
        left_heading='Discretionary Access Control',
        left_bullets=[
            'The data owner sets the permissions on their data.',
            'Windows NTFS permissions are DAC. Right-click, share.',
            'Linux file permissions are DAC. chmod is the command.',
            'Flexible. Easy to misconfigure.',
        ],
        right_kicker='POLICY DECIDES',
        right_heading='Mandatory Access Control',
        right_bullets=[
            'The system enforces policy. Owners cannot override.',
            'SELinux is MAC. Classified military systems use MAC.',
            'Labels on subjects and objects determine access.',
            'Strict. Harder to administer and easier to lock out.',
        ],
        notes=format_concept_notes(
            video_script=(
                'DAC and MAC. Two of the four access control models, and the '
                'two with the longest history. DAC stands for Discretionary '
                'Access Control. The word that matters is discretionary. The '
                'data owner has discretion to decide who can access their '
                'data. If you own a file on a Windows machine, you can '
                'right-click, go to properties, and grant or remove '
                'permissions for any user or group on the system. That is DAC '
                'in action. Linux file permissions work the same way. Owners '
                'decide. The strength of DAC is flexibility. Users can '
                'collaborate without filing tickets. The weakness is that '
                'users routinely make bad decisions. They grant everyone read '
                'access to a sensitive folder because it was easier than '
                'figuring out the right group. They share a directory with a '
                'contractor and forget to revoke access when the contract '
                'ends. DAC scales with culture, and most organizational '
                'cultures are not great at access hygiene. MAC stands for '
                'Mandatory Access Control. Mandatory because the system '
                'mandates the policy and the owner cannot override it. The '
                'canonical example is military classified systems. Every '
                'subject and every object has a label. Top Secret, Secret, '
                'Confidential, Unclassified. A subject can only access '
                'objects at or below their clearance level, and they cannot '
                'grant access to anyone at a lower level even if they want '
                'to. SELinux on Linux is a civilian implementation of MAC. '
                'The system administrator writes a policy. The system '
                'enforces it. Even root, traditionally the all-powerful '
                'user, cannot bypass it without rewriting the policy. The '
                'strength of MAC is that it works in environments where the '
                'cost of an access mistake is too high to leave it to user '
                'discretion. The weakness is that it is administratively '
                'heavy. Writing and maintaining a MAC policy is hard, and '
                'locking yourself out by writing the policy wrong is a real '
                'risk. Most organizations use DAC for most things and reach '
                'for MAC only where the stakes justify it.'
            ),
            key_terms=[
                ('DAC',     'Discretionary Access Control. Owner-set permissions.'),
                ('MAC',     'Mandatory Access Control. System-enforced policy.'),
                ('SELinux', 'a MAC implementation on Linux, widely deployed in hardened environments.'),
            ],
            think_about=[
                'If your home laptop uses DAC, who is the "owner" making the decisions?',
                'Why would a hospital choose DAC for general staff and MAC for the systems holding patient records?',
            ],
            source_url='https://csrc.nist.gov/projects/role-based-access-control',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 13 - RBAC vs ABAC (two_col)
    # -----------------------------------------------------------------------
    deck.add_two_column_slide(
        kicker='chapter 2',
        title='RBAC vs ABAC',
        subhead='How modern systems actually grant access',
        left_kicker='BY ROLE',
        left_heading='Role-Based Access Control',
        left_bullets=[
            'Permissions assigned to roles. Users get roles.',
            'AWS IAM groups. AD groups. Salesforce profiles.',
            'Scales well when job functions are stable.',
            'Granular exceptions get awkward fast.',
        ],
        right_kicker='BY CONTEXT',
        right_heading='Attribute-Based Access Control',
        right_bullets=[
            'Considers subject, object, action, and environment.',
            'AWS IAM conditions. Azure Conditional Access. Zero-trust.',
            '"Allow if HR role and corporate network and 9 to 5."',
            'Powerful. Policy logic gets complex.',
        ],
        notes=format_concept_notes(
            video_script=(
                'RBAC and ABAC. The two access control models you will '
                'actually encounter in modern enterprise environments. RBAC '
                'stands for Role-Based Access Control. The idea is that '
                'permissions are assigned to roles, not to individual users. '
                'A user gets one or more roles, and the permissions follow. '
                'Active Directory groups are RBAC. AWS IAM groups and IAM '
                'roles are RBAC. Salesforce profiles are RBAC. The strength '
                'of RBAC is that it scales beautifully when job functions '
                'are stable. You define a role called marketing analyst once, '
                'and every marketing analyst the company hires inherits the '
                'right permissions on day one. You revoke them all in one '
                'place when the role changes. The weakness shows up when you '
                'need granular exceptions. The CEO needs access to one '
                'specific Salesforce dashboard that nobody else in their '
                'role gets. Now you either invent a new role for one person '
                'or you bolt on individual permissions, and the model starts '
                'to fray. ABAC stands for Attribute-Based Access Control. '
                'ABAC decisions consider attributes of four things: the '
                'subject, the object, the action, and the environment. The '
                'user department is an attribute. The file classification '
                'level is an attribute. The current time is an environmental '
                'attribute. The network the user is on is an environmental '
                'attribute. A policy might say, allow read access if the '
                'user is in HR and the document is classified at HR-Internal '
                'and the action is read and the time is between 9 AM and 5 '
                'PM and the user is connecting from the corporate network. '
                'That entire decision is ABAC. AWS IAM policy conditions are '
                'ABAC. Azure Conditional Access is ABAC. Modern zero-trust '
                'architectures are essentially ABAC at internet scale. The '
                'strength of ABAC is expressiveness. You can write policies '
                'that match real business rules instead of approximating '
                'them with roles. The weakness is policy complexity. Once '
                'you start combining attributes, the logic gets hard to '
                'reason about, and debugging why was this request denied '
                'becomes a real engineering problem. Most organizations end '
                'up using RBAC for the easy 80% and ABAC for the hard 20%.'
            ),
            key_terms=[
                ('RBAC',       'Role-Based Access Control. Permissions assigned to roles.'),
                ('ABAC',       'Attribute-Based Access Control. Decisions based on attributes.'),
                ('Zero trust', 'a security model that assumes no implicit trust based on network location.'),
            ],
            think_about=[
                'Why is RBAC easier to audit than ABAC?',
                'Could a system use RBAC and ABAC at the same time? What would that look like?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-162/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 14 - Defense in Depth
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='Defense in Depth',
        subhead='Layered controls that fail independently',
        section_kicker='THE DESIGN PATTERN',
        card_heading='No single control stops every attack.',
        lead='Defense in depth is the architectural pattern that runs through every '
             'serious security design. Multiple controls, working independently, so '
             'a single failure does not mean total compromise.',
        bullets=[
            'Perimeter firewall, network segmentation, intrusion detection.',
            'MFA on every account. Strong password policy. Privileged access management.',
            'EDR on every endpoint. Email filtering. User training and phishing simulations.',
            'Backups, tested restores, and an incident response runbook.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Defense in depth. The architectural pattern that you will '
                'see in every serious security design. The idea is borrowed '
                'from military history. You do not put all your defenses at '
                'the city wall. You have the wall, then a moat behind it, '
                'then the inner keep, then the trained garrison inside. If '
                'the wall falls, the moat slows the attacker. If the moat is '
                'bridged, the keep holds. If the keep is breached, the '
                'garrison fights. Each layer can fail without the whole '
                'defense failing. The same idea applies to information '
                'security, and it has to, because no single security control '
                'is going to stop every attack. Firewalls miss things. EDR '
                'misses things. User training misses things. Backups get '
                'corrupted. If your security depends on any one control '
                'working perfectly, you have a single point of failure, and '
                'attackers find single points of failure for a living. So '
                'you stack. Take a typical engagement at Brazos Financial '
                'Group, the client you will see in Module 1. The perimeter '
                'has a firewall and an IDS watching the traffic. Behind '
                'that, the network is segmented so a compromise in the user '
                'network does not immediately reach the database. Every '
                'account requires MFA, so a phished password is not enough. '
                'Every endpoint runs EDR, so malware that gets through '
                'email is likely to get caught at execution time. Users get '
                'phishing training. Privileged access is managed separately '
                'with tighter controls. Backups are tested regularly, so '
                'ransomware is a recoverable event. That is defense in '
                'depth. Six or seven controls, each one independent, each '
                'one capable of failing without destroying the whole '
                'defense. As an attacker doing reconnaissance, you are '
                'looking for the spots where the layers are thin. As a '
                'defender writing recommendations, you are looking for the '
                'same thing.'
            ),
            key_terms=[
                ('Defense in depth',     'layered security so individual failures do not cascade.'),
                ('EDR',                  'endpoint detection and response, the modern descendant of antivirus.'),
                ('Network segmentation', 'dividing a network into zones with controls between them.'),
            ],
            think_about=[
                'If a determined attacker will eventually get through any single control, why are perimeter firewalls still worth deploying?',
                'Which layer of a defense-in-depth stack do you think is most often neglected, and why?',
            ],
            source_url='https://media.defense.gov/2021/Sep/27/2002863184/-1/-1/0/JOINT_GUIDE_TO_NETWORK_DEFENSE.PDF',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 15 - Prevent, Detect, Respond (guide)
    # -----------------------------------------------------------------------
    deck.add_guide_slide(
        kicker='guide',
        title='Prevent, Detect, Respond',
        subhead='Security as a continuous process, not a one-time install',
        callouts=[
            ('PREVENT', 'Stop the easy attacks first',
             'Firewalls, patching, MFA, hardening, training. Force adversaries to '
             'work harder than your neighbor and most will go elsewhere.'),
            ('DETECT', 'See what got through',
             'Logs, SIEM, EDR, IDS, network monitoring. You cannot respond to what '
             'you cannot see. Detection is the gap between prevention failing and '
             'an incident becoming a disaster.'),
            ('RESPOND', 'Contain, eradicate, recover',
             'Incident response runbook, forensics, restore from clean backups. '
             'Then loop back: improve prevention and detection based on what '
             'happened.'),
        ],
        notes=format_concept_notes(
            video_script=(
                'The operational model. Prevent, detect, respond. Three '
                'phases that run continuously, not a checklist you complete '
                'once. Prevention is what most introductory security '
                'treatments focus on, and it is the cheapest leg per attack '
                'prevented. Firewalls. Patching. MFA. Hardening '
                'configurations. User training. The goal of prevention is '
                'to make the easy attacks unprofitable so adversaries go '
                'find a softer target. You will not stop everything, but a '
                'well-tuned prevention layer stops the volume attacks '
                '\u2014 the script kiddies, the opportunistic worms, the '
                'commodity ransomware. Detection is the leg most '
                'organizations under-invest in until they get hit and '
                'discover their logs are useless. Detection assumes '
                'prevention will fail sometimes and asks the question, '
                'when it does, will we know. Logs, SIEM, EDR, IDS, network '
                'flow monitoring. The whole apparatus exists to answer '
                'that question fast. The gap between a prevention failure '
                'and detection is where small incidents become '
                'catastrophic ones. The 2013 Target breach was detectable '
                'in real time. Their tools fired alerts. Nobody escalated. '
                'Detection without response is detection wasted. Response '
                'is the leg with the most variance in maturity across '
                'organizations. A mature response capability has an '
                'incident response runbook, a defined chain of command, '
                'forensics tooling, tested backup restores, and a culture '
                'that treats incidents as learning opportunities rather '
                'than blame events. A weak response capability looks like '
                'panic, finger-pointing, and irreversible decisions made '
                'under pressure. The thing that ties these three legs '
                'together is the feedback loop. Every incident teaches '
                'you something about where prevention failed and where '
                'detection should have caught it earlier. Mature programs '
                'feed that knowledge back into the prevention and '
                'detection layers. That is what continuous improvement '
                'looks like in security.'
            ),
            think_about=[
                'Which of the three legs do you think your university invests most heavily in?',
                'Why might an organization deliberately prioritize detection over prevention?',
            ],
            source_url='https://www.nist.gov/cyberframework',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 16 - Core Security Principles (policy)
    # -----------------------------------------------------------------------
    deck.add_policy_slide(
        kicker='chapter 2',
        title='Core Security Principles',
        subhead='The design rules good engineers internalize',
        rules_kicker='FOUR PRINCIPLES',
        rules=[
            ('Least Privilege',
             'Every user, process, and system gets the minimum permissions needed '
             'to do its job. Nothing more. When in doubt, deny by default and add '
             'permissions only when the need is demonstrated.'),
            ('Separation of Duties',
             'Split sensitive operations across multiple people. The person who '
             'approves a payment cannot be the person who initiates it. Combine '
             'with job rotation and mandatory vacations to surface quiet collusion '
             'or single-person fraud.'),
            ('Need to Know',
             'Even when a person has the appropriate clearance, share information '
             'only when their role actually requires it. Compartmentalization '
             'limits the blast radius of a compromised account or insider threat.'),
            ('Implicit Deny',
             'If a rule does not explicitly allow it, the answer is no. Default '
             'deny. Allow lists, not block lists. Firewall rules end with a '
             'deny-all line for a reason.'),
        ],
        notes=format_concept_notes(
            video_script=(
                'Four principles. Internalize these and you will recognize '
                'them in every well-designed security control you encounter '
                'for the rest of your career. Least privilege. The first '
                'principle and the most cited. The idea is that every '
                'account, every service, every process gets the minimum '
                'permissions needed to do its job. Nothing more. A web '
                'server does not need the ability to read every database '
                'in the organization. A service account for a backup job '
                'does not need administrator rights everywhere. Least '
                'privilege is the design pattern that contains damage when '
                'something gets compromised. If the compromised account '
                'only has access to one folder, the attacker only gets one '
                'folder. If it has access to everything, the attacker gets '
                'everything. Separation of duties is the second principle. '
                'The idea is that sensitive operations should be split '
                'across multiple people so no one person can carry out a '
                'fraudulent action alone. The classic example is finance. '
                'The person who initiates a payment is not the person who '
                'approves it. The person who approves it is not the person '
                'who reconciles the books. Each pair of eyes is a friction '
                'point that catches fraud and mistakes. Job rotation and '
                'mandatory vacations are the operational extensions of '
                'this principle. Rotating people through positions and '
                'forcing them to take time off surfaces problems that the '
                'original holder of the position was quietly hiding. Need '
                'to know is the third principle. Different from least '
                'privilege in an important way. Least privilege is about '
                'technical permissions. Need to know is about information '
                'sharing. Even if a person has the appropriate clearance '
                'to see a piece of information, you only share it with '
                'them if their role actually requires it. Classified '
                'intelligence operations use need to know constantly. So '
                'do corporate legal teams handling sensitive matters. '
                'Implicit deny is the fourth principle. The default '
                'answer to any access decision should be no. The system '
                'should only allow an action if there is an explicit rule '
                'allowing it. The opposite, default allow, is how systems '
                'end up exposing things by accident. Firewall rules end '
                'with a deny-all line for exactly this reason. The '
                'principle generalizes far beyond firewalls. When you '
                'design any access control system, the safe default is '
                'no, and you build up from there.'
            ),
            key_terms=[
                ('Least privilege',      'minimum permissions necessary, nothing more.'),
                ('Separation of duties', 'dividing sensitive operations across multiple actors.'),
                ('Need to know',         'limiting information access to role-required cases.'),
                ('Job rotation',         'moving people through positions to surface hidden issues.'),
                ('Implicit deny',        'default deny, with explicit allow rules added only as needed.'),
            ],
            think_about=[
                'Which of these four principles do you think is most often violated in everyday consumer software?',
                'Why does mandatory vacation policy exist in banking but not in tech companies?',
            ],
            source_url='https://csrc.nist.gov/publications/detail/sp/800-160/vol-1-rev-1/final',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 17 - Security Through Obscurity Is Not Security (warning)
    # The single warning slot in this deck.
    # -----------------------------------------------------------------------
    deck.add_warning_slide(
        kicker='warning',
        title='Security Through Obscurity Is Not Security',
        subhead='The most expensive misconception in the field',
        banner='READ THIS TWICE',
        banner_line='Hiding how it works is not protection.',
        rule_kicker="KERCKHOFFS'S PRINCIPLE",
        rule_oneliner='Hide the key, not the algorithm.',
        rule_body='Kerckhoffs wrote this in 1883 about military ciphers. It still holds '
                  'in 2026 about every cryptosystem, protocol, and security control in '
                  'use. The strength of the system must rest in the secrecy of the key, '
                  'not in the secrecy of the design. Any system that depends on '
                  'adversaries not knowing how it works is one disclosure away from '
                  'total failure.',
        bullets=[
            'Open algorithms get peer review. Secret algorithms get exploited.',
            'Renaming SSH to port 2222 is convenience, not security.',
            'Custom crypto written without expert review is broken crypto.',
        ],
        notes=format_concept_notes(
            video_script=(
                'This slide gets its own warning slot in this deck because '
                'the misconception it addresses costs companies real money '
                'every year. Security through obscurity is the belief that '
                'hiding how a system works will protect it. It does not. '
                'The principle that contradicts it is named after Auguste '
                "Kerckhoffs, a Dutch cryptographer who wrote about military "
                'ciphers in 1883. The principle is simple: a secure system '
                'should remain secure even if everything about its design '
                'is public, except the key. Hide the key. Do not bother '
                'hiding the algorithm, because you cannot keep the '
                'algorithm secret indefinitely, and the moment it leaks, '
                'your entire security model collapses. AES, the modern '
                'symmetric encryption standard, is completely public. The '
                'algorithm is published. Anyone can read it. It is secure '
                'because the key is secret and the algorithm has survived '
                'decades of public peer review. That is not a coincidence. '
                'The algorithm became trustworthy because it was public. '
                'Custom crypto written by somebody who thought it would be '
                'safer if nobody else saw it has been broken every single '
                'time it has been tested. Renaming SSH to port 2222 '
                'instead of 22 is a related mistake on a smaller scale. '
                'It does not actually protect the SSH service. A '
                'determined attacker scans all ports, finds yours in '
                'seconds, and proceeds. What it does is make routine '
                'logging and monitoring slightly harder, because port 22 '
                'is the well-known port and analysts expect to see it. '
                'Obscurity is not security. Sometimes it is convenience, '
                'sometimes it is a configuration tweak with marginal '
                'value, but it is never the primary defense. When you see '
                'a vendor selling a product and refusing to disclose how '
                'it works, that should be a red flag, not a reassurance. '
                'Real security can withstand public scrutiny. Anything '
                'that cannot, will not.'
            ),
            key_terms=[
                ("Kerckhoffs's principle",     'the security of a system should depend only on the secrecy of the key.'),
                ('Security through obscurity', 'the mistaken belief that hiding design provides protection.'),
            ],
            think_about=[
                'Why might a software vendor still refuse to publish their algorithm even though Kerckhoffs\'s principle says they should?',
            ],
            source_url='https://en.wikipedia.org/wiki/Kerckhoffs%27s_principle',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 18 - What This Looks Like in Lab 1.2
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='chapter 2',
        title='What This Looks Like in Lab 1.2',
        subhead='The vocabulary you just learned is what you will be practicing',
        section_kicker='THE BRIDGE',
        card_heading='Every concept on this deck shows up in Lab 1.2.',
        lead='Reconnaissance is where this vocabulary becomes practice. Use these '
             'words while you do the work. Your runbook should read like an analyst '
             'wrote it, not a student.',
        bullets=[
            'Authorization: scanme.nmap.org is authorized. The rest of the internet is not.',
            'Confidentiality: recon is an attack on the confidentiality leg of CIA.',
            'Accounting: your runbook is the audit trail. Log every command you run.',
            'Defense in depth: every port, service, version, and patch level is a layer.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Bridge slide. Where does the vocabulary from this deck '
                'show up in Lab 1.2. The lab is a guided reconnaissance '
                'walkthrough against scanme.nmap.org and a couple of '
                'similar authorized targets. Every concept on this deck '
                'appears in that work, and you should be able to name '
                'them as you go. Authorization first. scanme.nmap.org is '
                'explicitly authorized as a scanning target. The site '
                'exists for this purpose. Everything else on the internet '
                'is not authorized, regardless of how tempting it looks. '
                'The legal frame from M1-C1 carries forward here. You '
                'scan the authorized target. You do not scan the random '
                'IP that looked interesting. Confidentiality next. '
                'Reconnaissance is, in CIA triad terms, an attack on the '
                'confidentiality leg. You are gathering information about '
                'a target that the target did not intend to publish. '
                'Open ports, service versions, software stacks, exposed '
                'directories. None of it is secret in the formal sense, '
                'but all of it is information the target probably did '
                'not consciously decide to share. As an analyst, when '
                'you write up your findings, you are documenting where '
                'the client confidentiality posture is leaking. '
                'Accounting third. The runbook you produce for Lab 1.2 '
                'is the practical embodiment of the accounting leg of '
                'AAA. Every command you ran, every piece of output you '
                'captured, every decision you made about what to do '
                'next. The runbook is the audit trail. It is also what '
                'makes your work reproducible, which is the entire point '
                'of the Foundation Lab pattern. Defense in depth fourth. '
                'Every layer of information you uncover during recon '
                'corresponds to a layer of the target defense in depth. '
                'The fact that you can see port 80 open is the first '
                'layer. The web server version is the second. The '
                'framework running on top is the third. The known '
                'vulnerabilities for that framework version are the '
                'fourth. Each layer either holds or does not. As you '
                'write up Lab 1.2, you are documenting where the layers '
                'are thin. Use the vocabulary on this deck deliberately '
                'when you write your runbook and your reflection. That '
                'is how you signal to a reader, including me, that you '
                'actually understand the work and are not just running '
                'tools.'
            ),
            key_terms=[
                ('Reconnaissance', 'information gathering on a target, the first phase of an engagement.'),
                ('Runbook',        'documentation that allows another analyst to reproduce your work.'),
            ],
            think_about=[
                'If recon is an attack on confidentiality, what defenses can a target deploy to reduce their recon footprint?',
                'Why does writing a good runbook matter even on a lab where nobody will actually rerun your commands?',
            ],
            source_url='https://nmap.org/book/legal-issues.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 19 - Recap and Next Steps (support)
    # -----------------------------------------------------------------------
    deck.add_support_slide(
        kicker='support',
        title='Recap and Next Steps',
        subhead='Where to go from here this week',
        philo_kicker='READ, PRACTICE, ASK',
        philo_heading='The vocabulary is the multiplier.',
        philo_body='Read Conklin and White Chapter 2. Then start Lab 1.2. Practice '
                   'using these words while you work. Discord for stuck moments, '
                   'Calendly for one-on-one time.',
        channels=[
            ('READING',  'Conklin and White, Chapter 2'),
            ('DISCORD',  'Post in #lab-help'),
            ('CALENDLY', 'One-on-one by appointment'),
            ('LAB 1.2',  'Authorized recon walkthrough'),
        ],
        notes=format_concept_notes(
            video_script=(
                'That is Chapter 2. Vocabulary chapter. The most important '
                'deck in Module 1 because every other module references '
                'these concepts. Here is what you do this week. Read '
                'Conklin and White Chapter 2. The deck gave you the '
                'scaffolding and the concrete examples. The chapter fills '
                'in the detail. Make a habit of looking up the formal '
                'NIST definitions for any term that still feels fuzzy. '
                'csrc.nist.gov has a searchable glossary. Then start Lab '
                '1.2. The lab is the recon walkthrough on scanme.nmap.org. '
                'As you work through it, deliberately use the vocabulary '
                'from this deck in your runbook. Do not write I found '
                'some open ports. Write what you actually did using the '
                'right words. Authorized target. Service enumeration. '
                'Version detection. Confidentiality exposure. That '
                'language is what makes your work read like an analyst '
                'work instead of a student work. If you get stuck, '
                'Discord. Lab-help is the channel. Posting there is '
                'faster than emailing me because somebody else probably '
                'hit the same issue and already knows the fix. If the '
                'problem is personal or you need one-on-one time, '
                'Calendly. No regular Zoom this semester. By next week '
                'you should be done with Lab 1.2 and starting to think '
                'about Lab 1.3, the Brazos Financial engagement, which '
                'is where you put all of this together for a real client '
                'deliverable. Get to it.'
            ),
            source_url='https://jfnewsom.github.io/is3513-assets/',
        ),
    )

    deck.save(OUT)
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    main()
