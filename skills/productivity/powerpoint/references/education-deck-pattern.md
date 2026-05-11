# Options Education Deck — Session Reference

Created: May 2025  
Purpose: Comprehensive 18-slide options trading education deck for Jun M (tech stocks: NVDA, TSLA, RBLX, TEM, AVAV)

---

## Deck Structure (18 slides)

| # | Slide Type | Layout |
|---|------------|--------|
| 1 | Title | Dark bg + diagonal accent shapes + left accent bar |
| 2 | Agenda | 2×4 card grid (numbered topic cards) |
| 3 | Definition + Two-column comparison | Call vs Put side-by-side cards |
| 4 | Worked example (NVDA) | Dark card + key-value row grid |
| 5 | Strategy overview | 3 vertical strategy cards (Hedge/Speculate/Income) |
| 6 | Concept + diagram | Left: numbered steps, Right: payoff diagram (axes + floor line) |
| 7 | Real scenarios | 3 scenario cards (bull/bear/flat with P&L math) |
| 8 | Concept + example | Left: steps, Right: TSLA example with key-value rows |
| 9 | Comparison table | Header row + alternating rows |
| 10 | Section divider | Dark bg + diagonal accent (simple) |
| 11 | Stock-specific: NVDA | 2×2 card grid for 4 step cards |
| 12 | Stock-specific: TSLA | Two-panel (collar trade + sizing guide) |
| 13 | Stock-specific: RBLX/TEM/AVAV | 3-column stock cards |
| 14 | Position sizing | Table + 3 tier boxes at bottom |
| 15 | Decision framework | 4 row cards (question + options + answer) |
| 16 | Risk cards | 2×3 grid of risk cards |
| 17 | Glossary | 2-column table (18 terms) |
| 18 | Summary | Dark bg + takeaways left + numbered steps right |

---

## Color Palette Used (Finance/Green theme)

```
darkBg:    "0F1F0F"   // deep forest (dark slides)
darkBg2:   "132113"   // slightly lighter dark
cardBg:    "1A2E1A"   // card on dark
accent:    "4ADE80"   // bright mint green
accent2:   "22C55E"   // slightly darker green
gold:      "FACC15"   // yellow highlight
text:      "F0FFF0"   // near-white on dark
textMuted: "86EFAC"   // muted green text
lightBg:   "F7FAF7"   // very light green-white (content slides)
darkText:  "1A2E1A"   // dark text on light bg
darkMuted: "4B5563"   // muted gray-green
white:     "FFFFFF"
red:       "EF4444"
orange:    "F97316"
blue:      "3B82F6"
```

Sandwich structure: dark slides for title/conclusion, light slides for content in between.

---

## Layout Patterns

### Dark title slides
- Diagonal accent shapes (rotated rectangles) in top-right corner
- Left vertical accent bar (0.12" wide, full height)
- Large title (44pt Arial Black), subtitle (22pt), divider line, tagline

### Light content slides
- Dark green header bar (1.1" height) with slide title in accent color
- Card-based layouts with shadows (makeShadow helper)
- Left accent bars on cards for visual hierarchy
- Consistent 0.5" margins

### Numbered step layouts
- Circular number badges (OVAL with accent2 fill, white text)
- Step text to the right of the badge
- 0.68" vertical spacing between steps

### Payoff diagrams (conceptual)
- Draw axes with LINE shapes
- Y-axis on left, X-axis at bottom
- Floor line as dashed horizontal line
- Annotations as text boxes

### Scenario cards
- 3 cards in a row
- Color-coded headers (green/yellow/red for bull/flat/bear)
- Key-value rows for P&L breakdown
- Bottom note in italics

### Stock-specific cards
- Colored ticker header (RBLX=blue, TEM=green, AVAV=gold)
- Strategy badge below header
- Bullet point content

### Glossary
- 2-column layout (9 rows each column = 18 terms)
- Alternating row background colors
- Term in bold accent2, definition in regular text

---

## Key Technical Notes

### makeShadow helper (use every time to avoid mutation bug)
```javascript
const makeShadow = () => ({
  type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.2,
});
// Always call makeShadow() fresh per shape — never reuse
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
```

### Card with left accent bar
```javascript
slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.white }, shadow: makeShadow() });
slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h, fill: { color: accentColor }, ... });
```

### Dark panel layout
```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x, y, w, h,
  fill: { color: C.darkBg }, line: { color: C.darkBg, width: 0 },
  shadow: makeShadow(),
});
```

### Scenario card structure
```
card (white, shadow)
  header bar (color, transparent)
  price line (bold)
  3 key-value rows
  divider
  italic note
```

---

## Sizing Reference

- Slide: 10" × 5.625" (LAYOUT_16x9)
- Header bar: y=0, h=1.1
- Content start: y=1.2
- Bottom margin: y=5.15+ (leave 0.475" from bottom)
- Card gap: minimum 0.3" between cards
- Left margin: 0.5"
- Right margin: 0.5" (so max content width = 9")

---

## QA Fixes Applied (May 2025 session)

- `markitdown` not available as `__main__` — use `pip install "markitdown[pptx]"` then invoke differently if needed
- LibreOffice `soffice.py` wrapper path varies — use `/Applications/LibreOffice.app/Contents/MacOS/soffice` directly on macOS
- soffice converts to PDF: `--headless --convert-to pdf input.pptx --outdir /tmp/out/`
- `pdftoppm -jpeg -r 150 input.pdf slide` produces numbered `slide-01.jpg` etc.