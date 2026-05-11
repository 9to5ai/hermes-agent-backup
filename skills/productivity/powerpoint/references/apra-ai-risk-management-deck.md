# APRA AI risk-management policy deck — session notes

Use this reference when Jun asks for APRA / prudential-regulator AI risk-management research, policy options, or a PowerPoint deck.

## User corrections from the session

- “SingaporeAir” was a mishearing / typo; the intended comparator is **Singapore MAS**, especially MAS FEAT, Veritas, Project MindForge, and AI risk-management toolkit work. Do not reference Singapore Airlines unless explicitly asked.
- Jun disliked a decorative / pastel first draft as “ugly”; for this class of deck use a restrained **enterprise / board-pack / consulting** style.
- Jun wanted **different policy options**, not only the final recommendation. Present options before the preferred path.
- Jun found fonts “weird and hard to read.” Use safe, widely available typography and verify readability through rendered images/contact sheets.

## APRA content pattern that worked

Frame AI as a cross-cutting technology that can create or amplify existing prudential risks rather than as a wholly new risk category. Preserve APRA’s principles-driven architecture:

- **CPS 220**: risk-management governance, Board oversight, accountabilities, risk appetite, assurance.
- **CPS 230**: operational resilience, critical operations, service providers, third-party AI dependencies, business continuity and fallback.
- **CPS 234**: information security, cyber controls, data protection, technology control environment.

Recommended options set used successfully:

- **Option A**: supervisory letters and thematic reviews only.
- **Option B**: standalone AI Prudential Standard.
- **Option C**: targeted amendments to CPS 220 / CPS 230 / CPS 234.
- **Option D**: cross-industry AI and model-risk CPG.
- **Option E**: CPG + toolkit + thematic supervision.

Preferred conclusion used in the deck: **Option E** scores highest; **Option D** is the minimum viable lower-intervention path; avoid a standalone AI CPS for now unless future evidence shows existing standards cannot carry the risk.

## Peer-regulator anchors

- **Singapore MAS**: FEAT / Veritas / MindForge / AI risk-management toolkit; useful for practical implementation tools and responsible-AI governance without collapsing into prescriptive technology rules.
- **BoE / PRA**: SS1/23 model risk-management principles; useful for model inventory, tiering/materiality, validation, governance, and lifecycle assurance.
- **OSFI E-23 and US model-risk guidance**: useful for model-risk inventory, validation, independent review, and ongoing monitoring.
- **HKMA / FINMA / IOSCO / EU AI Act**: useful for supervisory themes and external control expectations; avoid over-importing rules that would break APRA’s architecture.

## Design/readability pattern that worked

- Use an IBM Carbon-like enterprise palette: near-black / white / restrained blue accent; sharp hierarchy; minimal decoration.
- Use **Arial** or another safe system font when generated decks render oddly; custom fonts can substitute poorly in LibreOffice/PowerPoint.
- Keep body text roughly 13–16pt for live presentation decks; avoid relying on 9–11pt copy inside narrow cards.
- If contact sheets show dense text, shorten copy rather than only increasing font size.
- Dense slides to watch: decision matrix, evidence-spine, roadmap, draft policy language, and source list.

## QA pattern that worked

1. Generate with `pptxgenjs`.
2. Validate slide count and scan extracted text for placeholders/blank slides with `python3` + `python-pptx` if `markitdown` is unavailable.
3. Render with LibreOffice to PDF.
4. Convert to slide images with `pdftoppm`.
5. Build contact sheets and visually inspect both slide groups and individual problem slides.
6. Patch font size, copy length, and layout; regenerate and re-inspect before sending.
