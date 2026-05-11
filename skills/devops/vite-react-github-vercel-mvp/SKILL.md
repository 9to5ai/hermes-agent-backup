---
name: vite-react-github-vercel-mvp
description: Build, test, push, and deploy a React web app (Vite, Next.js, Remix, etc.) to GitHub and Vercel from a handoff spec. Use when the user asks to create a web app, publish it to GitHub, and deploy it to Vercel.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vite, nextjs, react, typescript, github, vercel, deployment, mvp]
    related_skills: [github-auth, github-repo-management, test-driven-development]
---

# Vite React GitHub + Vercel MVP Deployment

Use this workflow when a user gives a spec/handoff document for a simple client-only web app and asks to build, push to GitHub, and deploy to Vercel.

## When to use this skill vs. simpler alternatives

- **Use this skill (full Node/React scaffold)** when you have a React, Vite, or Next.js app that needs building, testing, and deploying.
- **Use STATIC HTML DEPLOYMENT (below)** when the deliverable is a single `index.html` with optional `assets/` folder — no build step, no npm, just HTML files.

---

## Static HTML → Vercel Deployment

When the deliverable is a static HTML file (e.g. a magazine-style PPT built from a skill like `guizang-ppt-skill`):

1. **Project layout** (example):
   ```
   ~/Projects/<project>/       ← root (linked to Vercel)
     └── ppt/
         ├── index.html        ← main file (must be named index.html)
         └── assets/           ← JS/CSS/fonts
             └── motion.min.js
   ```
   Or a flat layout:
   ```
   ~/Projects/<project>/       ← root
     ├── index.html
     └── assets/
   ```

2. **Deploy directly** (no `vercel build` needed):
   ```bash
   cd ~/Projects/<project>
   zsh -lc 'vercel --prod --yes'
   ```
   Vercel auto-detects no framework → serves files as-is from the root.

3. **Subdirectory deployment** (if `index.html` is not at root):
   Add `vercel.json` at project root:
   ```json
   {"rewrites": [{"source": "/(.*)", "destination": "/ppt/$1"}]}
   ```
   Then deploy from the project root.

4. **Skip GitHub** unless the user asks for it. Static HTML projects often don't need version control for the deployment itself.

5. **Verify**:
   ```bash
   curl -s --max-time 10 "https://<project>.vercel.app" | grep -o "<title>.*</title>"
   ```

---

## Prerequisites

Load these related skills first if relevant:
- `github-auth`
- `github-repo-management`
- `test-driven-development`

Verify tools/auth:

```bash
zsh -lc 'pwd && git --version && node --version && npm --version && gh --version | head -2 && gh auth status && vercel whoami && vercel --version'
```

Pitfall on Jun's macOS environment: non-login bash commands may not have Homebrew Node/npm on PATH, causing `npm: command not found` or `env: node: No such file or directory`. Prefer wrapping Node/GitHub/Vercel shell commands with `zsh -lc '...'`.

## Procedure

1. **Pick/create project folder**

```bash
mkdir -p /Users/momo/<project-name>
cd /Users/momo/<project-name>
```

2. **Scaffold app (or use existing project)**

```bash
zsh -lc 'npm create vite@latest . -- --template react-ts && npm install'
```

Install test deps when scoring/business logic needs tests:

```bash
zsh -lc 'npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom'
```

3. **Use TDD for deterministic logic**

For local scoring/decision engines:
- Write `src/test/*.test.ts` first.
- Run and watch it fail because the implementation is missing.
- Implement the data and scoring code.
- Run tests again and confirm green.

For client-only “AI-style” output features, do not add an API unless explicitly requested. Implement deterministic local helpers, e.g. `src/lib/prompt.ts`, and test that outputs include the required verdict, score, dimension labels, top issues, recommendations, and distinct text for each outcome. If a public label changes but internal keys are stable, keep the internal key and map it through a `dimensionLabels` object in UI/output code.

Add a test script if missing:

```json
"test": "vitest run"
```

4. **Build app structure**

Typical structure:

```txt
src/
  App.tsx
  main.tsx
  styles.css
  data/
  lib/
  components/
  test/
```

For single-session apps, keep routing in local state, e.g. `home | assessment | results`. Avoid persistence unless requested.

5. **Verify locally**

Run all checks before pushing:

```bash
zsh -lc 'npm test && npm run build && npm run lint'
```

For a quick live check, start Vite in the background:

```bash
zsh -lc 'npm run dev -- --host 127.0.0.1'
```

Then verify HTTP if browser/CDP is unavailable:

```bash
zsh -lc 'curl -s -I http://127.0.0.1:5173 | head'
```

6. **Create GitHub repo and push**

**CRITICAL: Exclude node_modules and .next from git FIRST**, before any commit. Create `.gitignore` before running `git add .`:

```bash
# Create .gitignore BEFORE adding files
echo 'node_modules
.next
.vercel
.env*.local' > .gitignore
git add .gitignore
git commit -m "Initial commit"
```

Then create and push in two steps (the `--push` flag on `gh repo create` can time out on large repos):

```bash
# Step A: create repo
gh repo create <repo> --public --source . --description "<description>"
# Step B: push separately (run in background if large)
git remote add origin https://github.com/<owner>/<repo>.git 2>/dev/null || git remote set-url origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

If the repo was already created (even if push timed out), just add the remote and push — do NOT re-create the repo.

7. **Deploy to Vercel**

For Vite/static apps:

```bash
zsh -lc 'vercel --prod --yes'
```

Vercel auto-detects Next.js, Vite, and Remix. It may also auto-connect the GitHub repo. A `.vercel/` directory is created — it goes in `.gitignore` automatically. If `.gitignore` changes after the initial commit, commit and push that update separately.

8. **Redeploy after final metadata/polish**

If you edit `index.html`, metadata, README, etc. after first deployment:

```bash
zsh -lc 'npm test && npm run build && npm run lint && git add . && git commit -m "Polish deployment metadata" && git push && vercel --prod --yes'
```

9. **Verify production URL**

Use the stable Vercel alias from CLI output, usually `https://<project>.vercel.app`:

```bash
zsh -lc 'curl -s -L https://<project>.vercel.app | grep -o "<expected title>" | head -1'
```

Also verify GitHub:

```bash
zsh -lc 'git status --short && gh repo view <owner>/<repo> --json url,visibility,defaultBranchRef --jq "{url:.url, visibility:.visibility, branch:.defaultBranchRef.name}"'
```

## Deliverables to user

Return:
- Live Vercel URL
- GitHub repo URL
- Concise list of what was built
- Verification commands/results: tests, build, lint, production URL loaded

## Common pitfalls

- `npm` missing in shell: use `zsh -lc` on macOS/Homebrew setups.
- **node_modules/.next accidentally committed**: Always create `.gitignore` BEFORE `git add .`. If already committed, use `git rm -r --cached node_modules .next` to unstage, then recommit.
- **`gh repo create --push` timeout**: Large repos (with many node_modules already present) can time out during the push phase. Create the repo first without `--push`, then run `git push` separately.
- Vercel may require `--yes`; otherwise it stops for confirmation.
- First Vercel deployment may produce both an immutable deployment URL and a stable alias; send the stable alias.
- If `.vercel` modifies `.gitignore` after commit, commit the `.gitignore` change but never commit `.vercel/`.
- Browser CDP may fail even when local dev server works; use `curl` as a fallback for availability checks.
- **Next.js static export**: Next.js `app/` router defaults to full SSR. If Vercel deployment fails to detect it, add `"output": "standalone"` to `next.config.js` or ensure `vercel.json` is not forcing static export.
