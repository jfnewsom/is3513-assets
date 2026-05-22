# IS3513 Slide Decks

This directory holds the build scripts for every IS3513 slide deck.

Decks fall into three families that share the same library and template but
differ in content shape:

- **Chapter overviews** (`m<N>_c<chapter>/`) - textbook chapter coverage.
  Structure follows Conklin & White; content draws from NIST publications,
  MITRE ATT&CK, OWASP, RFCs, and similar authoritative sources.
- **Foundation Lab walkthroughs** (`m<N>_l<unit>/`) - tool-focused walkthroughs.
  The Lab assignment sheet on GitHub Pages is the source of truth.
- **Engagement Packet walkthroughs** (`m<N>_l3/`) - consulting-deliverable
  walkthroughs. The EP assignment sheet and the Engagement Packet Guide are
  the source of truth.

## Layout

```
slides/
├── build_lib.py              shared deck-assembly library
├── README.md                 this file
├── smoke_test/
│   └── build_smoke.py        exercises every add_*_slide method (no content)
├── m1_c1/                    future: Module 1, Chapter 1 overview
│   ├── M1-C1_slide_guide.md  markdown slide guide (source of truth)
│   └── build_m1_c1.py        per-deck build script
├── m1_l1/                    future: Module 1, Lab 1.1 walkthrough
│   ├── Lab1-1_slide_guide.md
│   └── build_m1_l1.py
└── ...
```

## How to build a deck

```bash
python3 slides/m1_c1/build_m1_c1.py
```

The script writes the finished `.pptx` to `/home/claude/M1-C1.pptx` and any
rendered PNGs (for shell-command snippets) to `/home/claude/m1_c1_pngs/`.
Both paths are configurable at the top of the per-deck script.

## How to create a new deck

```bash
cp -r slides/smoke_test slides/m1_c1
mv slides/m1_c1/build_smoke.py slides/m1_c1/build_m1_c1.py
```

Then in the new script:

1. Update `OUT` at the top to your deck's output filename.
2. Write the slide guide markdown first (`M1-C1_slide_guide.md` in the same
   folder). Get the structure reviewed before writing Python.
3. Replace every `deck.add_*_slide(...)` call's content with the deck's real
   content. The order of calls determines slide order in the final deck.
4. Run it.

The first call should always be `deck.add_title_slide(...)`. Per the locked
deck-build rules, every deck opens with the title-slide layout.

## What the library provides

`build_lib.py` exposes one `DeckBuilder` plus an `add_*_slide` method for
each of the 12 layouts in the v6 template. All methods take an optional
`notes=` parameter for speaker notes (mandatory in real decks).

| Method | Template slide | Use for |
|---|---|---|
| `add_title_slide` | 1 | Deck opener with course ID and subtitle. |
| `add_concept_slide` | 2 | Workhorse: kicker + title + heading + lead + 4 bullets. |
| `add_two_column_slide` | 3 | Side-by-side comparison (4 bullets per side). |
| `add_intro_slide` | 4 | Mentor or instructor profile with portrait area. |
| `add_team_slide` | 5 | Five-mentor grid for module openers. |
| `add_stats_slide` | 6 | Three stat tiles + supporting body. |
| `add_structure_slide` | 7 | Three-card row (Unit 1/2/3 or any 3-way split). |
| `add_warning_slide` | 8 | Hard-rule callout. Use sparingly. |
| `add_support_slide` | 9 | Contact channels grid. Usually deck closer. |
| `add_module_slide` | 10 | Module overview with 3-lab grid. |
| `add_guide_slide` | 11 | Three stacked callouts (Do This / Heads Up / FYI). |
| `add_policy_slide` | 12 | Four numbered rules. |

Notes formatters:

- `format_title_notes(deck_id, deck_title, opening_line=None)` - title slide notes.
- `format_concept_notes(video_script, key_terms=None, think_about=None, source_url=None)`
  - composes notes for concept/content slides. `source_url` is the per-slide
    authoritative source link (NIST SP, MITRE ATT&CK page, RFC, etc.).
- `format_demo_notes(code, instructor_notes)` - for any future demo slides
  (shell commands + reminder text).
- `format_output_notes(output_text, instructor_notes)` - for any future output
  slides (terminal output + reminder text).

## How it works

1. **Unpack.** The template `.pptx` (default: `ppt/IS3513_Template_v6.pptx`)
   is unzipped into a working directory.
2. **Duplicate.** Each `add_*_slide` call uses `pptx/scripts/add_slide.py`
   to duplicate the appropriate template slide into the slide sequence.
   The 12 example slides in the v6 template act as canonical layouts.
3. **Populate.** Text is substituted into the duplicated slide's XML via
   targeted string replacements against known placeholder text. The
   placeholder text strings are defined in `build_lib.PH`. If the template
   gets re-authored, regenerate `PH` to match the new placeholder text.
4. **Pack.** The unpacked deck is re-zipped via `pptx/scripts/office/pack.py`.
5. **Inject notes.** The packed deck is opened with `python-pptx` and
   speaker notes are written to the notes pane of each slide.
6. **Save.** Final `.pptx` written to the script's `OUT` path.

## Conventions (locked)

These carry over from IS2053. All decks honor these unless explicitly noted:

- **Slide naming.** Filenames are `M<N>-C<chapter>.pptx` for chapter overviews
  and `M<N>-L<unit>.pptx` for lab walkthroughs. Examples: `M1-C1.pptx`,
  `M3-L2.pptx`. Student-facing references say "Module 1, Chapter 1" and
  "Lab 1.1".
- **Title prefixes.** Slide titles do NOT carry "Slide N:" prefixes. Just
  the topic. If a future demo slide layout is added, demo/output slides
  keep their `Demo:` / `Output:` prefix per template convention.
- **Speaker notes.** Mandatory on every slide. Composed from the slide
  guide markdown's Video Script, Key Terms, Think About This, and Source
  URL blocks via the `format_*_notes` helpers.
- **Em-dashes.** Banned in all slide content and speaker notes. Use colons.
- **Title slide first.** Every deck opens with `add_title_slide(...)`.
- **Deck length cap.** Target 20 slides per deck, 22 if absolutely needed
  to adequately cover content. Don't cover every topic in the source chapter
  - only what appears on the study sheet or gets used in a paired assignment.

## Source authority per deck family

| Deck family | Structure source | Content source |
|---|---|---|
| Chapter overview | Conklin & White chapter sectioning | NIST SPs, MITRE ATT&CK, OWASP, RFCs, vendor docs |
| Foundation Lab walkthrough | Lab assignment sheet (X.1 / X.2) on GitHub Pages | Same as the lab |
| Engagement Packet walkthrough | EP assignment sheet (X.3) and EP Guide | Same as the EP |

Per-concept-slide footer URL: the authoritative source link goes in
`format_concept_notes(source_url=...)`. For chapter overviews this is
typically a NIST SP URL or OWASP page. For lab walkthroughs it is usually
the matching section of the lab page on `jfnewsom.github.io/is3513-assets`.

## Slide guide markdown

The human-readable slide guide markdown (e.g.,
`IS3513_<YYYY-MM-DD>_M1-C1_Slide_Guide.md`) is the source-of-truth document
that gets reviewed before the script is written. The build script is a
direct Python translation of the slide guide. They are kept in sync
manually; the build script does not consume the markdown.

Per-slide blocks follow the IS2053 format:

```markdown
## Slide N: Topic Title

### Key Points
- Bullet one
- Bullet two
...

### Video Script
200 to 260 words. Conversational. NEXUS Junior Analyst frame: the senior
analyst (instructor) speaking to the junior analyst (student).

### Key Terms
- term: definition
- term: definition

### Think About This
1. Question one.
2. Question two.

*Source: <authoritative URL>*
```

## Per-deck script anatomy

See `smoke_test/build_smoke.py` for the canonical example exercising every
method. The shape is:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build_lib import DeckBuilder, format_concept_notes, format_title_notes

OUT = '/home/claude/M1-C1.pptx'

def main():
    deck = DeckBuilder(png_out='/home/claude/m1_c1_pngs', work='/tmp/build_m1_c1')

    deck.add_title_slide(
        course_id='IS3513',
        course_name='Information Assurance and Security',
        subtitle='Module 1, Chapter 1: Security Trends',
        notes=format_title_notes('M1-C1', 'Security Trends',
                                  'Welcome to the first chapter overview.'),
    )

    deck.add_concept_slide(
        kicker='chapter 1',
        title='What This Chapter Covers',
        subhead='The threat landscape in one paragraph',
        section_kicker='THE BIG IDEA',
        card_heading='Threats keep changing, fundamentals do not.',
        lead='One or two sentences setting up the topic.',
        bullets=[
            'Bullet one.',
            'Bullet two.',
            'Bullet three.',
            'Bullet four.',
        ],
        notes=format_concept_notes(
            video_script='...',
            key_terms=[('CIA Triad', 'Confidentiality, Integrity, Availability')],
            think_about=['Question one?', 'Question two?'],
            source_url='https://csrc.nist.gov/...',
        ),
    )

    # ... more slides ...

    deck.save(OUT)

if __name__ == '__main__':
    main()
```

Content (bullets, video scripts, key terms, questions, source URLs) all
lives inline in the per-deck script as Python string literals. The library
does no parsing of external files.

## Known issues

- **Template v6, slide 10 (module).** The dotted "CLIENT LOGO" image
  placeholder peeks behind the client-name text when no client logo is
  supplied. Cosmetic; address in v7 template cleanup along with em-dash
  scrub from placeholder strings.
- **Em-dashes in template placeholder strings.** The v6 template's
  placeholder example text contains em-dashes. They get fully overwritten
  by build-time content so they never reach a student-facing deck, but
  the template itself should get scrubbed in v7 so it stops being a
  source of drift.
