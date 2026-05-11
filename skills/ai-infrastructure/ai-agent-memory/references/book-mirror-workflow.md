# book-mirror Workflow

## What It Does

Take any book (EPUB/PDF) → produce a brain page at `media/books/<slug>-personalized.md`
with two-column tables: left = chapter content, right = your actual life using your
own words from the brain.

NOT a generic book summary. The right column is the value — it makes the book read
like a therapist who knows you.

## Trust Contract

book-mirror runs as a CLI command (`gbrain book-mirror`), NOT as a pure markdown skill.
The CLI submits N read-only subagent jobs (one per chapter). Each subagent has
`allowed_tools: ['get_page', 'search']` only — they CANNOT call put_page or any mutating op.
They produce markdown analysis via their final message. The CLI reads each child's
`job.result`, assembles the final two-column page, and writes it via one operator-trust
`put_page`. Untrusted EPUB/PDF content cannot prompt-inject any `people/*` page.

## Pipeline

```
1. ACQUIRE   → User has EPUB/PDF locally (manual)
2. EXTRACT   → Pull chapter text from EPUB/PDF into one .txt per chapter
3. CONTEXT   → Gather everything the brain knows about the reader
4. ANALYZE   → gbrain book-mirror fans out N read-only subagents
5. ASSEMBLE  → CLI reads each child result and writes one put_page
6. PDF       → Optional: render via brain-pdf
```

## Step 1: Acquiring the Book

book-mirror does NOT include book acquisition. User drops EPUB/PDF manually.

```bash
# Check what's already in the brain
ls $BRAIN_DIR/media/books/

# Resolve brain dir
BRAIN_DIR=$(gbrain config get sync.repo_path)
```

## Step 2: Text Extraction

### EPUB

```bash
SLUG="this-book"  # kebab-case
WORK="$(mktemp -d)/$SLUG"
mkdir -p "$WORK/chapters"
unzip -o path/to/book.epub -d "$WORK/unpacked"

# Find content files (XHTML/HTML), sorted (chapter order = sort order)
find "$WORK/unpacked" -name "*.xhtml" -o -name "*.html" | sort > "$WORK/files.txt"

# Strip HTML to text per chapter
python3 - <<'PY'
from bs4 import BeautifulSoup
import os, sys
work = os.environ['WORK']
files = open(f'{work}/files.txt').read().splitlines()
for i, path in enumerate(files, 1):
    html = open(path, encoding='utf-8', errors='replace').read()
    text = BeautifulSoup(html, 'html.parser').get_text('\n')
    text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    with open(f'{work}/chapters/{i:02d}.txt', 'w') as f:
        f.write(text)
PY
```

If `bs4` missing: `pip3 install beautifulsoup4 lxml`

### PDF

```bash
pdftotext -layout path/to/book.pdf "$WORK/full.txt"
# Then split by chapter heading ("Chapter N", "CHAPTER N", all-caps title)
# using awk or python
```

### Quality Check

For each chapter file:
- Word count > 1500 (typical chapter: 2k–8k words)
- No HTML tags
- Paragraphs preserved with `\n\n`

Save `chapters/INDEX.md` mapping chapter number → title → file → word count.

## Step 3: Context Gathering (CRITICAL)

This determines right-column quality. Gather:

1. **USER.md and SOUL.md** if they exist (templates at `templates/USER.md`, `templates/SOUL.md`)
2. **Recent daily memory** — last 14 days of brain pages under `wiki/personal/reflections/`
3. **Topic-relevant brain searches** tuned to book's themes:
   - `gbrain query "marriage"` for a marriage book
   - `gbrain query "founders"` for a business book
   - `gbrain query "shame"` for a psychology book
4. **Brain pages for relevant entities** — people who will likely appear
5. **Standing patterns** — recurring themes in user's reflections or originals

### Assemble Context Pack

```bash
CONTEXT="$WORK/context.md"
{
  echo "## USER.md (if any)"
  [ -f "$BRAIN_DIR/USER.md" ] && cat "$BRAIN_DIR/USER.md"
  echo
  echo "## SOUL.md (if any)"
  [ -f "$BRAIN_DIR/SOUL.md" ] && cat "$BRAIN_DIR/SOUL.md"
  echo
  echo "## Recent reflections (last 14 days)"
  # Adapt to user's filing scheme
  echo
  echo "## Topic-relevant brain pages"
  # gbrain query the book's key themes
  echo
  echo "## Themes & cruxes"
  # 1-page agent-written summary calling out:
  # - What's active in user's life that intersects the book
  # - Specific quotes from user that map to book themes
  # - People and dates for the right column
} > "$CONTEXT"
```

Make it dense. It's read by every chapter subagent.

## Step 4: Analysis — invoke gbrain book-mirror

```bash
gbrain book-mirror \
  --chapters-dir "$WORK/chapters" \
  --context-file "$CONTEXT" \
  --slug "$SLUG" \
  --title "Book Title Goes Here" \
  --author "Author Name" \
  --model claude-opus-4-7
```

CLI:
1. Validates inputs
2. Prints cost estimate (~$0.30/chapter at Opus), prompts to confirm (TTY) or requires `--yes`
3. Submits N child subagent jobs (read-only allowed_tools)
4. Waits for all children
5. Reads each `job.result`, assembles two-column page
6. Writes ONE `put_page` to `media/books/<slug>-personalized.md`
7. Reports JSON: `{"slug": "...", "chapters_total": N, "chapters_completed": N, "chapters_failed": 0}`

**Model: Opus by default.** Sonnet works but right-column quality drops noticeably.

**Idempotency**: retry is cheap — idempotency keys (`book-mirror:<slug>:ch-<N>`) deduplicate
completed chapters at the queue level.

## Step 5: PDF (optional)

After brain page lands, render to PDF:

```bash
# See skills/brain-pdf/SKILL.md for the make-pdf invocation
# gstack make-pdf binary required
P="$HOME/.claude/skills/gstack/make-pdf/dist/pdf"
CONTAINER=1 "$P" generate "$CLEAN" /tmp/output.pdf
```

## Step 6: Fact-Check and Cross-Link

After page lands, run a fact-check pass on factual claims about the reader
(parents, siblings, marriage history, jobs, heritage). Common errors:
- Conflating reader's parents' relationship with patterns in extended family
- Inventing therapy backstory when reader's parents are still together
- Wrong number/age of children, wrong spouse/kid/sibling names

If you can't verify a claim, remove it. Better to lose texture than introduce a falsehood.

Cross-link entities in the analysis to their brain pages. For every person the right
column references, add back-link from `people/<slug>` to `media/books/<slug>-personalized`.

## Output Quality Bar

**Left column must:**
- Preserve the author's actual stories, statistics, frameworks, examples
- Quote memorable phrases verbatim
- Be detailed enough the reader could skip the book and not lose much

**Right column must:**
- Use reader's *actual quoted words* from the context pack
- Reference *specific* dates, situations, people by name
- Read like a therapist who knows you're leaving notes in the margins
- Be plain about direct hits ("This is exactly the [name a real situation]")
- Be honest about misses ("This chapter is less directly relevant because...")

**Anti-patterns:**
- ❌ Skimming chapters — preserve detail
- ❌ Generic right column — "This might apply if you've ever felt..." → kill on sight
- ❌ Factual errors about the reader's life
- ❌ Giving subagent put_page access — trust contract is read-only
- ❌ Forcing connections — if a chapter doesn't apply, say so plainly
- ❌ Sycophancy or moralizing in the right column — no "you should...", no "consider..."
- ❌ Truncating the LEFT column

## Alternative: strategic-reading (one problem, not whole life)

book-mirror personalizes to the reader's whole life. strategic-reading personalizes
to ONE specific problem. Same shape, different lens.

For a decision you're facing: use `strategic-reading` instead.
For a book you want to deeply internalize: use `book-mirror`.