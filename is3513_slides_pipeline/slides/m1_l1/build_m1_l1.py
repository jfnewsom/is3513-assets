"""build_m1_l1.py - IS3513 Module 1, Lab 1.1 Walkthrough: Kali Environment Setup.

Renders the 14-slide walkthrough deck described in M1-L1_slide_guide.md (Phase 2
content pass, approved 2026-05-23). Output: /home/claude/M1-L1.pptx.

This is the first walkthrough deck (vs. the chapter decks M1-C1 and M1-C2). It
crawls the Lab 1.1 instruction sheet top to bottom, one slide per checkpoint
(two for the dense ones: CP3, CP4, CP6). No warning slot used; walkthroughs are
instructional, not doctrinal.

Slide map (matches the guide section by section):
     1. title    - Deck opener
     2. concept  - What This Deck Covers
     3. concept  - Before You Start (pre-flight: host specs + hypervisor + Neo)
     4. concept  - Checkpoint 1: Install VirtualBox
     5. concept  - Checkpoint 2: Download Kali Linux
     6. concept  - Checkpoint 3a: Create the VM
     7. concept  - Checkpoint 3b: Configure VM Settings
     8. concept  - Checkpoint 4a: Boot the Installer
     9. concept  - Checkpoint 4b: Hostname and User
    10. concept  - Checkpoint 5: Install and Verify Docker
    11. concept  - Checkpoint 6a: Confirm Your VM Identity
    12. concept  - Checkpoint 6b: Verify Your Tools
    13. guide    - Submitting Lab 1.1 (3 callouts)
    14. support  - What's Next

Pairs with: pages/labs/json/lab1_1_COMPLETE.json (after Patches A/B/C applied
in the same session, see M1-L1_phase2_patches.md).
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

OUT = '/home/claude/M1-L1.pptx'


def main():
    deck = DeckBuilder(
        png_out='/home/claude/m1_l1_pngs',
        work='/tmp/build_m1_l1',
    )

    # -----------------------------------------------------------------------
    # Slide 1 - Title
    # -----------------------------------------------------------------------
    deck.add_title_slide(
        course_id='IS3513',
        course_name='Information Assurance and Security',
        subtitle='Module 1, Lab 1.1: Kali Environment Setup',
        attribution='PROF. JOHN NEWSOM   \u00b7   SUMMER 2026   \u00b7   SECTION 0XX',
        notes=format_title_notes(
            'M1-L1',
            'Lab 1.1 Walkthrough: Kali Environment Setup',
            'Welcome to Lab 1.1. This is the only lab in the semester with no '
            'security content. It is environment setup, top to bottom. You will '
            'install VirtualBox, install Kali Linux, install Docker, and verify '
            'that everything works. Doing this lab carefully now is the single '
            'best investment you will make in the rest of the course. Every '
            'later lab assumes the environment built here is solid. Every '
            'screenshot you submit for the next fourteen weeks will be taken '
            'on the VM you build today. If the foundation is sloppy, the cost '
            'compounds. If the foundation is solid, every other lab gets '
            'easier. Let us walk through it.',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 2 - What This Deck Covers
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='What This Deck Covers',
        subhead='Six checkpoints, top to bottom',
        section_kicker='ORIENTATION',
        card_heading='Every later lab runs on the environment you build here.',
        lead='Lab 1.1 is the only assignment in Module 1 with no security '
             'content. It is pure environment setup. Doing it right now means '
             'every later lab works smoothly. Doing it wrong means you will be '
             'debugging instead of learning, for the rest of the semester.',
        bullets=[
            'Checkpoints 1 and 2: Install VirtualBox, download Kali Linux.',
            'Checkpoints 3 and 4: Create the VM, install the OS, lock in your hostname.',
            'Checkpoint 5: Install and verify Docker for the client targets.',
            'Checkpoint 6: System verification. Confirm everything works before Lab 1.2.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Here is the shape of the lab. Six checkpoints, total time '
                'estimate eighty-five minutes to two and a half hours '
                'depending on your download speed and your familiarity with '
                'installers. Checkpoints one and two are pre-flight. You '
                'install the hypervisor and you start the Kali download. You '
                'can run those in parallel because the Kali ISO is large and '
                'slow. Checkpoints three and four are where the VM actually '
                'comes to life. You create the virtual machine, you boot the '
                'installer, you click through the setup, and you set your '
                'hostname. That hostname is the single most consequential '
                'decision in this entire lab, because it shows up in every '
                'screenshot you submit for the rest of the semester. We will '
                'spend extra time there. Checkpoint five is Docker. Docker is '
                'what hosts the client targets you will engage with starting '
                'in Lab 1.3, so it needs to be working before the security '
                'work begins. Checkpoint six is verification. You run a '
                'sequence of commands that confirm the environment is wired '
                'correctly. Hostname right, network up, tools installed. If '
                'anything is wrong, this is where you find out, and the fixes '
                'are cheap because nothing else depends on the environment '
                'yet. Do not rush this lab. The students who treat Lab 1.1 '
                'as a checkbox have the worst semester. The students who '
                'treat it as the foundation it actually is have the smoothest.'
            ),
            key_terms=[
                ('VirtualBox',  'a free, cross-platform hypervisor from Oracle.'),
                ('Kali Linux',  'a Debian-based distribution preloaded with security tools.'),
                ('Docker',      'a containerization platform used in this course to host client targets.'),
                ('Hostname',    'the system name your VM reports to the network and to your screenshots.'),
            ],
            think_about=[
                'Why does the lab put environment setup in its own dedicated lab rather than bundling it into Lab 1.2?',
                'If you have done a VM install before, what is one thing you wish you had been more careful about the first time?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/labs/Lab1_1_Kali_Environment_Setup.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 3 - Before You Start (Pre-flight)
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Before You Start',
        subhead='Hardware and hypervisor decisions',
        section_kicker='PRE-FLIGHT',
        card_heading='VirtualBox is the path. Mac users have a special case.',
        lead='Two decisions before the first installer runs. What hardware do '
             'you have, and what hypervisor will you use? Getting these right '
             'means a smooth lab. Getting them wrong wastes hours you will not '
             'get back.',
        bullets=[
            'Host machine: 16 GB RAM minimum, 32 GB recommended (UTSA policy).',
            'VirtualBox is the supported hypervisor. Other options work but are your debugging problem.',
            'MacBook Neo (A18 Pro): VirtualBox installs but Kali will not boot. Use Parallels.',
            'Parallels Desktop has educational pricing around $50. Not free, but it works on day one.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Two decisions before you start clicking on installers. '
                'First decision, hardware. The official UTSA standard for '
                'this program is sixteen gigabytes of RAM minimum, '
                'thirty-two gigabytes recommended. If your laptop is below '
                'that, you can still get through this course, it just gets '
                'harder. The MacBook Neo is the interesting exception. The '
                'Neo ships with less than sixteen gigabytes of unified '
                'memory, which is below the official floor, but the Apple '
                'Silicon memory architecture is unusual enough that it '
                'actually works fine for this lab. Not optimally, but fine. '
                'So if you have a Neo, you are not blocked. Second '
                'decision, hypervisor. A hypervisor is the software that '
                'runs virtual machines on your host. There are several on '
                'the market, including VirtualBox, VMware Workstation, '
                'Parallels Desktop, UTM, and Hyper-V. The concepts are '
                'identical across all of them. The settings have slightly '
                'different names. The buttons are in slightly different '
                'places. If you know one, you can figure out another in '
                'fifteen minutes. For this course, VirtualBox is the '
                'supported hypervisor, which means this is the one I can '
                'troubleshoot for you in office hours. If you choose '
                'something else and it breaks, that is your problem to '
                'figure out. I cannot support every possible combination of '
                'host operating system and hypervisor and host hardware. '
                'Now the Mac-specific note. If you are on a MacBook Neo '
                'with the A18 Pro chip, VirtualBox will install cleanly '
                'and then fail to boot Kali. This is a known issue with '
                'the Neo chip. The fix is to use Parallels Desktop '
                'instead. Parallels has educational pricing for students, '
                'around fifty dollars. Not free, but it works on the Neo '
                'on day one without any of the workarounds. For any other '
                'Mac, you can use either VirtualBox or Parallels. Pick one '
                'and move on. With those two decisions made, you are ready '
                'for Checkpoint 1.'
            ),
            key_terms=[
                ('Hypervisor',         'software that creates and runs virtual machines on a host computer.'),
                ('A18 Pro',            'the system-on-chip in the MacBook Neo, with known VirtualBox compatibility issues.'),
                ('Parallels Desktop',  'a commercial hypervisor for Mac with educational pricing.'),
            ],
            think_about=[
                'Why does the course standardize on a single supported hypervisor instead of letting students use whatever they prefer?',
                'If you have a Mac other than a Neo, what would push you toward Parallels over VirtualBox, or vice versa?',
            ],
            source_url='https://www.utsa.edu/itsc/laptop-requirements.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 4 - Checkpoint 1: Install VirtualBox
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Install VirtualBox',
        subhead='Boring but essential. Accept the defaults and move on.',
        section_kicker='CHECKPOINT 1',
        card_heading='Get it installed. The interesting parts come later.',
        lead='VirtualBox is free, cross-platform, and supports everything this '
             'lab needs. Pull the current release from the official source, run '
             'the installer, accept defaults unless you know why you would '
             'change them.',
        bullets=[
            'Download from virtualbox.org. Official source only.',
            'Match your host OS: Windows, macOS Intel, macOS Apple Silicon, or Linux.',
            'Run the installer with administrator privileges.',
            'While VirtualBox installs, start the Kali ISO download from Checkpoint 2.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint one, install VirtualBox. There is nothing clever '
                'about this step. Go to virtualbox.org, that is the official '
                'source, and download the installer for your host operating '
                'system. Windows users, the Windows installer. macOS users, '
                'the macOS installer, and watch the architecture, because '
                'there are separate downloads for Intel and Apple Silicon. '
                'Linux users, your distribution probably has a package, but '
                'the official downloads are also fine. Run the installer. '
                'You will need administrator privileges, because VirtualBox '
                'installs kernel-level networking drivers that require '
                'elevated permissions to register. Accept the defaults. The '
                'installer will reset your network briefly when it installs '
                'the host-only networking adapter. That is normal. Do not '
                'panic if your Wi-Fi blinks. Now here is the time-saving '
                'move. The Kali ISO in Checkpoint 2 is approximately four '
                'gigabytes. On a residential broadband connection that is '
                'ten to thirty minutes of download time. Start that '
                'download in another browser tab while VirtualBox is '
                'installing. By the time you finish Checkpoint one, the '
                'Kali ISO should be most of the way done, and you can move '
                'to Checkpoint three without waiting. This is the only '
                'place in the lab where you can parallelize. After this, '
                'the work is sequential. When VirtualBox finishes '
                'installing, you may need to reboot. Do the reboot. '
                'Skipping it causes weird permission errors later that '
                'take twenty minutes to diagnose. Five minutes of reboot '
                'saves you twenty minutes of debugging.'
            ),
            key_terms=[
                ('VirtualBox',           "Oracle's free cross-platform hypervisor."),
                ('Host operating system', 'the OS running on your physical machine.'),
            ],
            think_about=[
                'Why does VirtualBox need administrator privileges to install when most applications do not?',
                'What would go wrong if you started the Kali ISO download before VirtualBox finished installing?',
            ],
            source_url='https://www.virtualbox.org/manual/UserManual.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 5 - Checkpoint 2: Download Kali Linux
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Download Kali Linux',
        subhead='Official source. Verify the hash.',
        section_kicker='CHECKPOINT 2',
        card_heading='Pull the official image. Verify the hash. Wait for the download.',
        lead='Kali Linux is a Debian-based distribution preloaded with security '
             'tooling. You will use it for the rest of the semester. Download '
             'once from the official source, verify the hash, never trust an '
             'image you have not verified.',
        bullets=[
            'Download from kali.org. Installer ISO, current release.',
            'Match your architecture: amd64 for Intel/AMD, arm64 for Apple Silicon (Parallels).',
            'Copy the SHA-256 hash from the download page before the file finishes downloading.',
            'Verify the hash matches your file. This is integrity from M1-C2 in practice.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint two, download Kali. Go to kali.org and find the '
                'installer ISO for the current release. Two things to get '
                'right. First, get the installer image, not the live image '
                'and not the virtual machine image. The installer is what '
                'you want for a clean VirtualBox install. Second, get the '
                'right architecture. Most of you are on amd64, which means '
                'Intel or AMD processors. That is the right choice for '
                'Windows, for Intel Macs, and for most Linux hosts. If you '
                'are on Apple Silicon using Parallels, you want the arm64 '
                'image. Pick wrong and the VM will fail to boot in a way '
                'that is not obvious. Get this one right. While the '
                'download is running, copy the SHA-256 hash from the '
                'download page. The hash is published right next to the '
                'download link. Paste it into a text file so you have it '
                'after the page closes. When the download finishes, you '
                'are going to verify that the file you got matches the '
                'hash that was published. This is your first encounter '
                'with the integrity leg of the CIA triad in practice. The '
                'hash on the website is what the official Kali release '
                'looks like. The hash you compute on your downloaded file '
                'is what you actually have. If they match, you have the '
                'real image. If they do not, something happened between '
                'the server and your disk, and you should not install '
                'from that file. The verification command depends on your '
                'operating system. Windows powershell uses Get-FileHash. '
                'macOS and Linux use shasum or sha256sum. The output is a '
                'long hex string. Compare it to what you copied from the '
                'website. If it matches, you are good. If it does not, '
                'redownload and try again.'
            ),
            key_terms=[
                ('ISO',         'a disk image file format used to distribute operating system installers.'),
                ('amd64 / arm64', 'the two architectures Kali Linux ships for. Intel/AMD versus Apple Silicon and other ARM-based machines.'),
                ('SHA-256',     'cryptographic hash function used to verify file integrity.'),
            ],
            think_about=[
                "What kinds of things could happen between Kali's servers and your downloaded file that the hash check would catch?",
                'If your computed hash does not match the published hash, what are the three or four most likely explanations?',
            ],
            source_url='https://www.kali.org/get-kali/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 6 - Checkpoint 3a: Create the VM
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Create the VM',
        subhead='New machine wizard, name it correctly',
        section_kicker='CHECKPOINT 3a',
        card_heading='The VM name is the first place you type kali-abc123.',
        lead="VirtualBox's New Machine wizard walks through the basics. The "
             'single most important field is the VM name. This is where your '
             'hostname convention begins. Get it right and every screenshot for '
             'the next fourteen weeks will be valid.',
        bullets=[
            'VirtualBox \u2192 New. Name the VM exactly: kali-abc123 (substitute your real abc123).',
            'Type: Linux. Version: Debian 64-bit (or arm64 on Apple Silicon).',
            'Select the Kali ISO from Checkpoint 2 as the install medium.',
            'Do not abbreviate. Do not capitalize. Do not add spaces.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint three is the first place the lab starts to feel '
                'like real configuration work. Open VirtualBox. Click New. '
                'The new machine wizard opens. The first field is the VM '
                'name. Type kali, dash, your abc123. So if your UTSA ID is '
                'jxn123, the VM name is kali-jxn123. All lowercase. No '
                'spaces. No capital letters. No underscores. Exactly the '
                'hostname convention I will be looking for on every '
                'screenshot you submit for the rest of the semester. This '
                'is the most important field in this lab. Type it '
                'carefully. Type it twice if you have to. The wizard '
                'probably auto-detects the OS type based on the name. '
                'Make sure it picks Linux as the Type. The Version should '
                'be Debian sixty-four-bit if you are on amd64, or Debian '
                'arm sixty-four-bit if you are on Apple Silicon under '
                'Parallels. Select the Kali ISO you downloaded in '
                'Checkpoint two as the install medium. The wizard might '
                'call this Image File or ISO Image or Optical Disk. Same '
                'thing across hypervisors with slightly different names. '
                'Browse to the ISO. Select it. Click Next. The remaining '
                'fields in the wizard are about resource allocation, and '
                'we are going to handle those in detail on the next slide, '
                'because the defaults are too small for what this lab '
                'needs. For now, you are done with the naming. The VM '
                'exists, but it is not yet configured. That is Checkpoint '
                'three part B.'
            ),
            key_terms=[
                ('VM name',            "the label VirtualBox uses to identify the virtual machine. In this course, must match your eventual hostname."),
                ('New Machine wizard', "VirtualBox's guided VM creation flow."),
            ],
            think_about=[
                'Why does this course require the VM name and the eventual hostname to match exactly?',
                'If you typed a typo into the VM name and only realize after install, what is the cost of fixing it now versus at the end of Module 1?',
            ],
            source_url='https://www.virtualbox.org/manual/UserManual.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 7 - Checkpoint 3b: Configure VM Settings
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Configure VM Settings',
        subhead='RAM, CPU, disk, network',
        section_kicker='CHECKPOINT 3b',
        card_heading='The defaults are too small. Adjust to what the lab needs.',
        lead='VirtualBox lets you adjust the resources the VM receives from '
             'your host. The wizard defaults are conservative to the point of '
             'being unusable. Bump them up before you boot.',
        bullets=[
            'RAM: 4096 MB minimum, 8192 MB recommended if your host has the room.',
            'CPU: 2 cores minimum.',
            'Virtual disk: VDI format, dynamically allocated, 80 GB.',
            'Screenshot: 01-vm-settings.png. VM name, RAM, CPU all visible.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint three part B is where you decide what resources '
                "to give your VM. VirtualBox's defaults are conservative "
                'because it does not know what kind of work the VM will do. '
                'For this course, the defaults are too small, so we are '
                'bumping them up. RAM. Allocate four gigabytes minimum, '
                'eight gigabytes if your host has the room. The lab JSON '
                'says four thousand ninety-six megabytes minimum and eight '
                'thousand one hundred ninety-two megabytes recommended. '
                'Same thing in different units. If your host is at the '
                'UTSA standard of sixteen gigabytes, give the VM eight. '
                'You will have eight left for the host operating system, '
                'which is plenty. If your host is at thirty-two gigabytes, '
                'give the VM eight or even twelve. If your host is below '
                'sixteen gigabytes, give the VM four and accept that the '
                'VM will feel sluggish. It will still work, it will just '
                'not be fast. CPU cores. Two cores minimum. Most modern '
                'laptops have at least four physical cores, often eight '
                'or more with hyperthreading. Give the VM two. You can '
                'experiment with more, but two is the floor. Virtual '
                "disk. VDI format, which is VirtualBox's native disk "
                'format. Dynamically allocated, which means the disk file '
                'on your host only grows as the VM actually uses storage. '
                'Eighty gigabytes maximum size, which is what the lab '
                'specifies. The dynamic allocation matters because Kali '
                'is going to take ten or fifteen gigabytes installed and '
                'the lab tools take another five or so. Eighty gives you '
                'headroom to install whatever else you want without '
                'rebuilding the VM. Network adapter. NAT is the safe '
                'default for this lab. NAT means your VM shares the '
                "host's network connection, and the host firewall "
                'protects the VM from inbound connections from the '
                'outside world. We will discuss bridged versus NAT later '
                'in the course. For now, NAT is right. When all of these '
                'settings are in place, take screenshot zero one dash vm '
                'dash settings dot png. The screenshot needs to show the '
                'VM name, the RAM allocation, and the processor count '
                'all in one frame. That is your first submission '
                'artifact for this lab. Save it to your Module1 '
                'underscore Screenshots folder using the exact filename.'
            ),
            key_terms=[
                ('VDI',                          "VirtualDisk Image, VirtualBox's native virtual disk format."),
                ('Dynamically allocated disk',   'a disk that grows on the host as the VM uses storage, rather than pre-allocating the full size.'),
                ('NAT',                          "Network Address Translation, the VirtualBox networking mode that shares the host's network connection."),
            ],
            think_about=[
                'If you have a sixteen-gigabyte laptop, what happens if you give the VM twelve gigabytes of RAM?',
                'Why does dynamic disk allocation matter for a lab VM but might not matter for a production database VM?',
            ],
            source_url='https://www.virtualbox.org/manual/UserManual.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 8 - Checkpoint 4a: Boot the Installer
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Boot the Installer',
        subhead='Click through the install wizard',
        section_kicker='CHECKPOINT 4a',
        card_heading='Most of this is defaults. Watch for the hostname slot in part B.',
        lead='Boot the VM with the ISO attached. The Kali installer walks you '
             'through language, location, keyboard, and disk partitioning. Most '
             'of these are click-through defaults.',
        bullets=[
            'Start the VM. The Kali installer should auto-boot from the ISO.',
            'Language: English. Location: United States. Keyboard: American English.',
            'Disk: Guided, use entire disk. Confirm when prompted.',
            'The installer reboots when done. Eject the ISO before the reboot.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint four is the OS install itself. Start the VM. '
                'VirtualBox will boot from the ISO you attached in '
                "Checkpoint three. You will see the Kali installer's boot "
                'menu. Pick Graphical Install. The graphical installer is '
                'friendlier than the text one and they do the same thing. '
                'Language, English. Location, United States. Keyboard, '
                'American English. These are all click-through defaults '
                'for most of you. If you are in a different region or you '
                'use a different keyboard layout, pick what fits. Network '
                'configuration runs next. The installer will try to '
                'autoconfigure DHCP. If the VM gets an IP address, it '
                'moves on. If it does not, that means your VirtualBox '
                'networking is misconfigured, and you should back up to '
                'Checkpoint three and check the network adapter setting. '
                'NAT, that was the answer. Disk partitioning is the next '
                'big screen. The lab says guided, use entire disk. The '
                'entire disk in this context is the eighty-gigabyte '
                'virtual disk you allocated, not your actual hard drive. '
                'The VM cannot see your host disk and cannot harm it. '
                'Accept the guided partitioning, accept All files in one '
                'partition, accept Write the changes to disk. The '
                'installer will copy a few thousand packages over the '
                'next ten to twenty minutes. This is the longest single '
                'step in the lab. Walk away. Get coffee. Come back when '
                'it is done. When the package copy finishes, the '
                'installer prompts about GRUB boot loader installation. '
                'Yes, install GRUB to the master boot record. Then it '
                'tells you to eject the install media and reboot. Eject '
                'the ISO before the reboot, otherwise the VM will boot '
                'back into the installer instead of into your new Kali '
                "install. VirtualBox has a Devices menu where you can "
                'unmount the optical drive. Do that, then reboot. Your '
                'VM is now a Kali Linux machine.'
            ),
            key_terms=[
                ('GRUB',                 'the Linux boot loader, installed during OS install.'),
                ('Guided partitioning',  "the installer's automated disk layout option."),
            ],
            think_about=[
                'Why does the Kali installer ask about disk partitioning when you have a single eighty-gigabyte virtual disk and nothing else?',
                'If the install hangs at the package copy stage for ninety minutes, what is your first diagnostic step?',
            ],
            source_url='https://www.kali.org/docs/installation/hard-disk-install/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 9 - Checkpoint 4b: Hostname and User
    # The longest video script in the deck (~350 words). The hostname rule
    # is the most consequential single beat in Lab 1.1; it earns the airtime.
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Hostname and User',
        subhead='The kali-abc123 moment of truth',
        section_kicker='CHECKPOINT 4b',
        card_heading='Hostname must match your VM name from Checkpoint 3a. Exactly.',
        lead='During install, you set the hostname and create a user account. '
             'The hostname must match your VM name from Checkpoint 3 exactly. '
             'If it does not, every Engagement Packet for the rest of the '
             'semester loses points on screenshot validation.',
        bullets=[
            'Hostname: kali-abc123. Same as your VM name. Same case. No typos.',
            'Domain: leave blank or accept default.',
            'Create user account: your name, abc123 username, strong password.',
            'Screenshot: 02-kali-desktop.png. Terminal open, hostname visible.',
        ],
        notes=format_concept_notes(
            video_script=(
                'This is the slide that matters most in this entire lab. '
                'Checkpoint four part B, hostname and user account. During '
                'the install wizard, somewhere between disk partitioning '
                'and the package copy, you get a screen titled Configure '
                'the network or similar. It asks you for a hostname. The '
                'hostname you type into this field is what shows up at the '
                'top of every terminal window for the rest of the time you '
                'use this VM. It is also what shows up in the corner of '
                'every screenshot you submit for every Engagement Packet '
                'in this course. The hostname must be exactly kali, dash, '
                'your abc123. The same string you typed as the VM name in '
                'Checkpoint three part A. If you typed kali-jxn123 as the '
                'VM name, you type kali-jxn123 as the hostname. Same case. '
                'Lowercase letters. No capitals, no underscores, no '
                'spaces. The cost of getting this wrong is large and the '
                'cost of getting it right is zero, so type carefully. Type '
                'it twice. The domain field comes next. Leave it blank or '
                'accept whatever default the installer suggests. Domain '
                'is not graded. Hostname is. User account creation '
                'follows. The installer asks for your full name, then a '
                'username, then a password. Full name, your real name. '
                'Username, your abc123. Same string again, lowercase. '
                'Password, something strong that you will remember. The '
                'student-grade rule is twelve characters minimum, mix of '
                'letters, numbers, and symbols. Do not use Password123 or '
                'any variant. You will remember this password ten weeks '
                'from now. Do not handicap your future self. The install '
                'finishes the package copy after this, installs GRUB, '
                'ejects the ISO if you did not eject it manually, and '
                'reboots. You log in with your username and password. '
                'You see the Kali desktop for the first time. Open a '
                'terminal. Type hostname and hit enter. The system '
                'should print back kali-abc123. If it does, you are '
                'golden. Take screenshot zero two dash kali dash desktop '
                'dot png. The screenshot needs to show the Kali desktop '
                'with a terminal window open and the hostname clearly '
                'visible. If hostname returns something other than '
                'kali-abc123, stop. Do not move on. The fix is easier '
                'now than it will ever be again. You can edit slash etc '
                'slash hostname, edit slash etc slash hosts to match, '
                'and reboot. Or, if you would rather, reinstall. The '
                'reinstall takes thirty minutes. The cost of leaving the '
                'hostname wrong is hundreds of dollars in tuition value '
                'over the rest of the semester. Take the thirty minutes.'
            ),
            key_terms=[
                ('Hostname',                  'the system name reported by the hostname command and visible in the terminal prompt.'),
                ('/etc/hostname and /etc/hosts', "the two Linux files that determine the system's hostname."),
            ],
            think_about=[
                'Why does the course require the hostname to match the VM name and the username convention so strictly?',
                'If you discover the hostname is wrong only in Module 3, what is the cost of fixing it then versus what it would have been here?',
            ],
            source_url='https://wiki.debian.org/HowTo/ChangeHostname',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 10 - Checkpoint 5: Install and Verify Docker
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Install and Verify Docker',
        subhead='Container runtime for client targets',
        section_kicker='CHECKPOINT 5',
        card_heading='Docker hosts the client targets. Install, add to group, verify.',
        lead='Docker provides lightweight isolation for the fictional client '
             'environments you will engage with starting in Lab 1.3. Install it '
             'from the Kali repositories, add yourself to the docker group, '
             'verify it runs.',
        bullets=[
            'Install: sudo apt update && sudo apt install -y docker.io.',
            'Add yourself to the docker group: sudo usermod -aG docker $USER.',
            'Log out, log back in. The group change requires a new session.',
            'Verify: docker --version and docker run hello-world. Capture 03-docker-version.png.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint five is Docker. Docker is a container runtime. '
                'Containers are lightweight isolated environments, lighter '
                'than full virtual machines, and Docker is the standard '
                'tool for running them on Linux. In this course, Docker is '
                'what hosts your client engagement targets. Brazos '
                'Financial Group, Gulf Coast Healthcare Partners, Alamo '
                'Industries, LoneStar DevOps. Those are fictional clients '
                'you will work against. They are not real companies and '
                'they are not real networks. They are Docker containers '
                'that I provide, running on your Kali VM. Lab 1.3 is the '
                'first time you will use one. You need Docker installed '
                'and working before then. Open a terminal. Run sudo apt '
                'update to refresh the package index. Then sudo apt '
                'install dash y docker dot io. The dot io variant is '
                "Debian's packaging of Docker, which is what is in the "
                'Kali repositories. There is also a separate Docker Inc '
                "package called docker-ce that you can install from "
                "Docker's own repository. Either works for this course. "
                'The dot io variant is simpler because it is already in '
                'the default package list. While you are at it, run the '
                'usermod command to add yourself to the docker group. '
                'Sudo, usermod, dash big A G, docker, dollar sign USER. '
                'That dollar sign USER expands to your current username '
                'at runtime. The reason you do this is that Docker by '
                'default requires root privileges to run, which means '
                'you would have to type sudo docker everything. Adding '
                'yourself to the docker group lets you run docker as '
                'your normal user without sudo. Important detail. The '
                'group change does not take effect in your current '
                'shell. You have to log out and log back in for your '
                'session to pick up the new group membership. If you '
                'skip this and try to run docker, you will get a '
                'permission denied error and waste twenty minutes '
                'debugging it. Log out. Log back in. Verify with docker '
                'dash dash version. You should get a version string '
                'like Docker version twenty-something. Then run docker '
                'run hello dash world. Docker will pull a small test '
                'container from Docker Hub and run it. The output is a '
                'friendly message confirming that Docker is installed '
                'correctly, the kernel networking is working, and the '
                'daemon can pull images. Take screenshot zero three '
                'dash docker dash version dot png showing both the '
                'version command and the hello-world output. That is '
                'your second submission artifact.'
            ),
            key_terms=[
                ('Docker',       'a container runtime for Linux.'),
                ('Container',    'a lightweight isolated environment using Linux kernel features (namespaces and cgroups).'),
                ('docker group', 'Linux group whose members can run Docker without sudo.'),
            ],
            think_about=[
                'Why does the course use Docker containers for client targets instead of separate full virtual machines?',
                'If docker run hello-world fails with a permission error, what is the most likely cause?',
            ],
            source_url='https://docs.docker.com/get-started/overview/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 11 - Checkpoint 6a: Confirm Your VM Identity
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Confirm Your VM Identity',
        subhead='Last chance to catch a hostname typo',
        section_kicker='CHECKPOINT 6a',
        card_heading='If your hostname is wrong, fix it now.',
        lead='The first set of verification commands prove your VM identity. '
             'Hostname, system info, network reachability. These are the '
             'cheapest fixes if anything is wrong, because nothing else '
             'depends on them yet.',
        bullets=[
            'hostname should return kali-abc123 exactly. No typos.',
            'uname -a confirms kernel and architecture.',
            'ip addr confirms network interface and IP.',
            'ping -c 3 8.8.8.8 confirms outbound network. Capture 04-system-verification.png.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint six is verification. We are going to confirm '
                'in two passes that the environment is wired correctly. '
                'The first pass is identity. Who is this VM, where is it, '
                'can it reach the internet. Open a terminal. Run '
                'hostname. The system prints back the hostname you set '
                'in Checkpoint four part B. It should be kali-abc123 '
                'with your real abc123. If it says anything else, stop '
                'and fix it now. This is your last cheap opportunity to '
                'fix a hostname typo. The cost goes up sharply once you '
                'start submitting Engagement Packets. Run uname dash a. '
                'This prints kernel name, kernel version, hostname, '
                'architecture, and a few other identifying bits about '
                'the machine. The output should include Linux at the '
                'start, kali-abc123 in the middle, and either x86 '
                'underscore 64 or aarch64 at the end depending on your '
                'architecture. This confirms you have a working Linux '
                'kernel running on the architecture you expected. Run '
                'ip addr. This prints all network interfaces and their '
                'addresses. You should see a loopback interface '
                'labeled lo with the address 127.0.0.1, and another '
                'interface, usually eth0 or enp0s3 depending on your '
                'VirtualBox version, with an IP address in the range '
                '10.0.2.something. That second address is what '
                'VirtualBox NAT gave you. If the IP address is missing '
                'or it is 169.254.something, your network is broken '
                'and you need to back up. Run ping dash c 3 8.8.8.8. '
                "This sends three ICMP echo requests to Google's "
                'public DNS server. If all three return successfully, '
                'your outbound network is working and DNS is '
                'irrelevant to this particular test. If they all time '
                'out, your NAT is misconfigured. Likely culprit, you '
                'have the network adapter set to something other than '
                'NAT in VirtualBox. When all four of those commands '
                'return clean output, take screenshot zero four dash '
                'system dash verification dot png. The screenshot '
                'needs to show all four command outputs and the '
                'hostname must be clearly visible in at least one of '
                'them. That is your third submission artifact and the '
                'most important one for hostname validation.'
            ),
            key_terms=[
                ('uname',   'command that prints kernel and system information.'),
                ('ip addr', 'command that prints network interface configuration.'),
                ('ICMP',    'the protocol that ping uses to test reachability.'),
            ],
            think_about=[
                'If hostname returns something correct but the prompt at the top of your terminal shows something different, where is the discrepancy?',
                'Why does ping not require root privileges on most modern Linux distributions when it used to?',
            ],
            source_url='https://manpages.debian.org/bookworm/coreutils/hostname.1.en.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 12 - Checkpoint 6b: Verify Your Tools
    # -----------------------------------------------------------------------
    deck.add_concept_slide(
        kicker='lab 1.1',
        title='Verify Your Tools',
        subhead='Catch missing packages now, not at midnight',
        section_kicker='CHECKPOINT 6b',
        card_heading='Run each command. They should all return a version.',
        lead='Run each version command. They should all return a version '
             'string. If any fail, install the missing package now. Kali ships '
             'with most of these but not all of them, and the gap is cheaper to '
             'close here than at the deadline of a future lab.',
        bullets=[
            'Recon: nmap --version, nc -h, dig -v.',
            'Service enumeration: nikto -Version, enum4linux -h, searchsploit -h.',
            'Network and crypto: wireshark --version, openssl version.',
            'Password cracking: john --help, hashcat --version.',
        ],
        notes=format_concept_notes(
            video_script=(
                'Checkpoint six part B is tool verification. Kali Linux '
                'ships with most of the tools this course uses, but not '
                'all of them, and which ones are missing depends on '
                'which Kali variant you installed. So we are going to '
                'run a version check on every tool you will need '
                'somewhere in Lab 1.2 through Lab 5.2. Ten commands. '
                'Each one should print a version string. If any of '
                'them fail with command not found, install the missing '
                'package now. The fix is sudo apt install dash y '
                'followed by the package name, and the package name is '
                'usually the same as the command name. The ten tools, '
                'in the order I have them on the slide. Reconnaissance '
                'tools first. nmap dash dash version, that is the '
                'network mapper. nc dash h, that is netcat. dig dash '
                'v, that is the DNS lookup tool. Service enumeration '
                'next. nikto dash big V dash Version, that is the web '
                'vulnerability scanner. enum4linux dash h, that prints '
                'SMB enumeration help. searchsploit dash h, that is '
                'the local Exploit-DB search tool. Network and crypto. '
                'wireshark dash dash version, that is the packet '
                'capture and analysis tool. You will use Wireshark '
                'heavily in Module three. openssl version, that is the '
                'crypto Swiss army knife. You will use it in Modules '
                'two and three. Finally, password cracking. john dash '
                'dash help, that is John the Ripper. hashcat dash dash '
                'version, that is the GPU-accelerated cracker. Both of '
                'those land in Module four. Run each of those '
                'commands. Confirm a version string comes back. If '
                'any are missing, install them, then rerun the command '
                'and confirm. There is no screenshot for this '
                'checkpoint, just confirmation. The point of '
                'verifying now is that fixing a missing package on a '
                'Tuesday afternoon in the first week of class is a '
                'five-minute job. Fixing it at midnight before a '
                'Module four deadline is a thirty-minute panic. Do '
                'the boring work now.'
            ),
            key_terms=[
                ('apt',          "Debian's package manager, used on Kali for installing tools."),
                ('Course tools', 'nmap, netcat, nikto, enum4linux, searchsploit, john, hashcat, wireshark, openssl, dig: the ten tools verified here.'),
            ],
            think_about=[
                'Why does the course want you to verify tools you will not use until Module 4 during Lab 1.1?',
                "If nmap --version works but nc -h does not, what does that tell you about Kali's default package selection?",
            ],
            source_url='https://www.kali.org/tools/',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 13 - Submitting Lab 1.1 (guide)
    # -----------------------------------------------------------------------
    deck.add_guide_slide(
        kicker='guide',
        title='Submitting Lab 1.1',
        subhead='Four screenshots, one quiz, a habit that starts now',
        callouts=[
            ('FOUR SCREENSHOTS', 'Save in Module1_Screenshots folder',
             '01-vm-settings.png, 02-kali-desktop.png, 03-docker-version.png, '
             '04-system-verification.png. Naming and hostname must match.'),
            ('CANVAS QUIZ', 'Take the Lab 1.1 Quiz with the VM running',
             'Quiz questions reference specific outputs you should have seen. '
             'Keep your VM open while you answer.'),
            ('RUNBOOK HABIT', 'Start documenting now',
             'Your Engagement Packet for Lab 1.3 includes a runbook. Start '
             'writing it now, while the commands are fresh. Future you will '
             'be grateful.'),
        ],
        notes=format_concept_notes(
            video_script=(
                'Submitting Lab 1.1. Three things to keep in mind. '
                'First, the screenshots. Four total. The filenames are '
                'fixed. Zero one dash vm dash settings dot png, zero '
                'two dash kali dash desktop dot png, zero three dash '
                'docker dash version dot png, zero four dash system '
                'dash verification dot png. Use those exact filenames. '
                'Save them to a folder called Module1 underscore '
                'Screenshots so you can find them in three weeks when '
                'Lab 1.3 needs them all in one place. Your hostname '
                'has to be visible in the screenshots that show '
                'terminals. If your hostname is wrong or missing, the '
                'screenshot will not validate during grading, and the '
                'penalty schedule applies. Second, the Canvas quiz. '
                'The Lab 1.1 quiz is in Canvas. Take it while your VM '
                'is still running, because some questions reference '
                'specific outputs you should have seen during the lab. '
                'You can have the VM open in one window and Canvas '
                'open in another. The quiz is the actual submission '
                'requirement for Lab 1.1. The screenshots get reused '
                'for Lab 1.3, but the quiz is what closes out Lab 1.1. '
                'Third, and this is a habit that pays off later. '
                'Start your runbook now. You do not turn it in until '
                'Lab 1.3 as part of the Engagement Packet, but the '
                'runbook is a record of what you did and why. The '
                'commands you ran. The settings you configured. The '
                'decisions you made. The things that broke and how '
                'you fixed them. Write that down today while you '
                'remember. Open a text file or a markdown document '
                'and just keep notes. When you sit down for Lab 1.3 '
                'in three weeks, the difference between students who '
                'started their runbook in week one and students who '
                'try to reconstruct it the night before is the '
                'difference between an Engagement Packet that reads '
                'like an analyst wrote it and one that reads like a '
                'panicked student wrote it. Start now.'
            ),
            think_about=[
                'Why is the submission requirement for Lab 1.1 a Canvas quiz rather than a written deliverable?',
                'If you start a runbook today and you do not need to turn it in for three weeks, what is the right format to use that you will actually maintain?',
            ],
            source_url='https://jfnewsom.github.io/is3513-assets/pages/labs/Lab1_1_Kali_Environment_Setup.html',
        ),
    )

    # -----------------------------------------------------------------------
    # Slide 14 - What's Next (support)
    # -----------------------------------------------------------------------
    deck.add_support_slide(
        kicker='support',
        title="What's Next",
        subhead='Environment done. The real work starts in Lab 1.2.',
        philo_kicker='READ, PRACTICE, ASK',
        philo_heading='The environment is the foundation. Now the security work begins.',
        philo_body='Take the Lab 1.1 Canvas quiz, then move to Lab 1.2: '
                   'Reconnaissance Tool Exploration. The vocabulary from M1-C2 '
                   'will land in practice. Discord for stuck moments, Calendly '
                   'for one-on-one.',
        channels=[
            ('READING',  'Conklin and White, Chapters 1 and 2'),
            ('DISCORD',  'Post in #module-1-help'),
            ('CALENDLY', 'One-on-one by appointment'),
            ('NEXT LAB', 'Lab 1.2: Reconnaissance Tool Exploration'),
        ],
        notes=format_concept_notes(
            video_script=(
                'That is Lab 1.1. Environment setup complete. Here is '
                'what to do next. First, if you have not already, take '
                'the Lab 1.1 quiz in Canvas. You need to do that to '
                'close out Lab 1.1. Keep your VM running while you '
                'answer. Some questions reference specific outputs. '
                'Second, move to Lab 1.2. Lab 1.2 is Reconnaissance '
                'Tool Exploration, and it is where the vocabulary from '
                'M1-C2 starts to land in practice. You are going to '
                'use the tools you just verified. You are going to '
                'practice on scanme.nmap.org, which is the authorized '
                'target the Nmap project maintains specifically for '
                'learning. You are going to write up what you found '
                "in a way that reads like an analyst's runbook, not a "
                "student's lab report. Third, the reading. Conklin "
                'and White Chapters one and two. Chapter one is the '
                'field overview that pairs with M1-C1. Chapter two is '
                'the vocabulary chapter that pairs with M1-C2. Read '
                'both before you sit down for Lab 1.2 if you have '
                'not already. The reading reinforces what the decks '
                'scaffolded. If you get stuck. Discord is the fastest '
                'path to a fix, because somebody in your section '
                'probably hit the same issue and already knows the '
                'solution. Post in #module-1-help. If your question '
                'is personal or you need one-on-one time, Calendly. '
                'No regular Zoom this semester. The course is '
                'asynchronous. Go set yourself up for a good '
                'semester. Get to it.'
            ),
            source_url='https://jfnewsom.github.io/is3513-assets/',
        ),
    )

    deck.save(OUT)
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    main()
