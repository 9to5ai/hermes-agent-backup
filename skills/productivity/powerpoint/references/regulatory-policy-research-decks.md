# Regulatory policy research decks — session pattern

Use this reference when creating a PowerPoint deck from regulatory / policy research where the user asks for recommendations and options.

## Proven workflow

1. **Anchor in primary sources first**
   - Download or extract the core regulatory documents before drafting.
   - Keep copies of key PDFs in the working directory and return them as `MEDIA:` files when useful.
   - For APRA-style work, explicitly map recommendations to the existing prudential architecture rather than proposing a new regime by default.

2. **Treat newly supplied regulator letters as baseline context**
   - If the user provides a fresh letter / consultation / speech URL, extract it even if similar content was already researched earlier.
   - Pull out direct implications for the deck: changed baseline, supervisory signal, enforcement posture, gaps observed, and minimum expectations.

3. **Structure recommendations as options, not just conclusions**
   - Include a clear executive answer, then a comparison of policy options with pros/cons and recommended path.
   - Include rationale for rejected options, especially where the user cares about preserving existing architecture.

4. **Use a strong evidence spine**
   - Core architecture slides: current obligations and where the new issue fits.
   - International scan slides: jurisdiction-by-jurisdiction, with explicit “what to borrow / what to avoid”.
   - Recommendation slides: package, implementation roadmap, draft wording, open decision points.
   - Source slide: concise primary sources used.

5. **Design for executive policy readability**
   - Avoid dense text-only slides; use cards, process flows, comparison rows, and callout boxes.
   - Include one visual element per slide, but do not let decoration obscure policy content.
   - Long quotes should be split into multiple text boxes with generous margins.
   - Long source lists are more readable in two columns.

6. **QA loop that worked**
   - Generate PPTX with `pptxgenjs`.
   - Extract text using `python-pptx` if `markitdown` is unavailable.
   - Render with LibreOffice: `soffice --headless --convert-to pdf --outdir render deck.pptx`.
   - Convert to images with `pdftoppm -jpeg -r 100 render/deck.pdf render/slide`.
   - Build contact sheets with PIL for visual inspection.
   - Use vision inspection to find overlap/cutoff/cramped text.
   - Patch and re-render affected slides.

## Common pitfalls

- Do not stop at a written answer when the user asked for a deck; create the `.pptx` immediately if enough context exists.
- Do not ask clarifying questions before creating a useful first draft when defaults are obvious. Ask refinement questions after delivering the draft.
- In regulatory architecture decks, avoid recommending a standalone standard unless the evidence supports it; first test whether guidance, supplements, supervisory letters, or toolkits preserve the existing framework.
- Contact-sheet thumbnails exaggerate text-size concerns. Fix obvious overlap/cutoff first; then improve high-value readability issues such as crowded quotes and source lists.

## Example deck outline for regulatory AI-risk recommendations

1. Title
2. Executive answer
3. New regulator letter / consultation implications
4. Architecture framing: new technology as amplifier of existing risks
5. Current standards / obligations
6. International scan
7. Deep dives into closest peer jurisdictions
8. Options comparison
9. Recommended package
10. Definitions and materiality
11. Governance / Board accountability
12. Inventory and risk tiering
13. Lifecycle controls
14. Operational resilience implications
15. Information security implications
16. Incident / notification clarification
17. Implementation roadmap
18. Draft policy wording
19. Decision points
20. Sources
