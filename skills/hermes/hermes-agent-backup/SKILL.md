---
name: hermes-agent-backup
description: Full Hermes Agent state backup to GitHub and restore on a new machine. Covers repo setup, what to include/exclude, rsync-based incremental sync, and the nightly cron job.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, backup, github, cron, restore]
    related_skills: [hermes-agent, github-auth, github-repo-management]
---

# Hermes Agent Backup & Restore

Backs up your full Hermes Agent state (skills, memories, plans, scripts, profiles, config) to a private GitHub repo every night, and restores it on a new machine.

## When to Run

- On first setup of a new machine
- Whenever `memory` says "restore me" or the user asks to restore
- After any major skill authoring or config session

---

## Architecture

```
~/.hermes/hermes-agent-backup/   ← git repo (GitHub: 9to5ai/hermes-agent-backup)
├── skills/
├── memories/
├── plans/
├── scripts/
├── profiles/
├── config.yaml
├── SOUL.md
├── architecture-notes.md
├── channel_directory.json
└── backup.sh              ← rsync + git push, called by cron
```

**What is NOT backed up** (large/binary/transient):
- `state.db` + `-shm` + `-wal` (400MB+ SQLite)
- `sessions/` (transcript history)
- `cache/`, `logs/`, `audio_cache/`, `image_cache/`
- `.env` (credentials)
- `kanban.db`
- `youtube_cookies.txt`
- `processes.json`, `gateway.lock`, `gateway.pid`

---

## Step 1: Create the GitHub Repo

```bash
# Authenticate first (gh must be logged in)
gh auth status

# Create and clone in one shot — clone destination is determined by gh
gh repo create hermes-agent-backup \
  --public \
  --description "Hermes Agent full backup: skills, memories, plans, scripts, config" \
  --clone
```

**Note:** `gh repo clone owner/repo` clones into `./repo/` relative to `pwd`. Run from `~/.hermes/` so the repo lands at `~/.hermes/hermes-agent-backup/`. This is the correct location.

---

## Step 2: First-Time Sync

From `~/.hermes/hermes-agent-backup/`:

```bash
# Set .gitignore first
cat > .gitignore << 'EOF'
state.db
state.db-shm
state.db-wal
.DS_Store
.env
.youtube_cookies.txt
kanban.db
cache/
logs/
audio_cache/
image_cache/
sessions/
processes.json
gateway.lock
gateway.pid
*.pid
*.lock
EOF

# Create target directories
mkdir -p skills memories plans scripts profiles bin hooks platforms plugins

# Copy from parent .hermes/ into the backup repo
cp -r ../skills/* skills/
cp -r ../memories/* memories/
cp -r ../plans/* plans/
cp -r ../scripts/* scripts/
cp -r ../profiles/* profiles/
cp -r ../bin/* bin/
cp -r ../hooks/* hooks/
cp -r ../platforms/* platforms/
cp -r ../plugins/* plugins/
cp ../config.yaml .
cp ../SOUL.md .
cp ../architecture-notes.md .
cp ../channel_directory.json .

# Commit and push
git add .
git commit -m "Full Hermes Agent backup - $(date '+%Y-%m-%d %H:%M')"
git push -u origin main
```

---

## Step 3: backup.sh (rsync Incremental Sync)

Save as `~/.hermes/hermes-agent-backup/backup.sh`:

```bash
#!/bin/bash
set -e
cd /Users/momo/.hermes/hermes-agent-backup

git checkout main 2>/dev/null || true
git pull origin main 2>/dev/null || true

rsync -av --delete \
  --exclude='state.db*' \
  --exclude='.DS_Store' \
  --exclude='.env' \
  --exclude='youtube_cookies.txt' \
  --exclude='kanban.db' \
  --exclude='cache/' \
  --exclude='logs/' \
  --exclude='audio_cache/' \
  --exclude='image_cache/' \
  --exclude='sessions/' \
  --exclude='processes.json' \
  --exclude='gateway.lock' \
  --exclude='gateway.pid' \
  ../skills/ ./skills/

rsync -av --delete --exclude='.DS_Store' ../memories/ ./memories/
rsync -av --delete --exclude='.DS_Store' ../plans/ ./plans/
rsync -av --delete --exclude='.DS_Store' ../scripts/ ./scripts/
rsync -av --delete --exclude='.DS_Store' ../profiles/ ./profiles/
rsync -av --delete ../bin/ ./bin/
rsync -av --delete ../hooks/ ./hooks/
rsync -av --delete ../platforms/ ./platforms/
rsync -av --delete ../plugins/ ./plugins/
rsync -av \
  ../config.yaml \
  ../SOUL.md \
  ../architecture-notes.md \
  ../channel_directory.json \
  ./

if ! git diff --quiet; then
  git add -A
  git commit -m "Nightly backup - $(date '+%Y-%m-%d %H:%M')"
  git push origin main
  echo "Backup pushed: $(date '+%Y-%m-%d %H:%M')"
else
  echo "No changes to push - backup up to date"
fi
```

Make executable: `chmod +x backup.sh`

---

## Step 4: Schedule Nightly Cron

```bash
hermes cron create \
  --name hermes-nightly-github-backup \
  --prompt "Run the backup.sh script in /Users/momo/.hermes/hermes-agent-backup/ using bash. Return a summary of what was done (backup pushed / no changes)." \
  --schedule "0 2 * * *" \
  --workdir /Users/momo/.hermes/hermes-agent-backup \
  --repeat forever
```

Runs at 2 AM nightly. Cron job ID: `dd5d09e989f4`.

---

## Restore on a New Machine

```bash
# 1. Clone the repo
gh repo clone 9to5ai/hermes-agent-backup
# Repo lands at ./hermes-agent-backup/ — move to ~/.hermes/
mv hermes-agent-backup ~/.hermes/

# 2. Restore key directories into ~/.hermes/
cp -r hermes-agent-backup/skills/* ~/.hermes/skills/
cp -r hermes-agent-backup/memories/* ~/.hermes/memories/
cp -r hermes-agent-backup/plans/* ~/.hermes/plans/
cp -r hermes-agent-backup/scripts/* ~/.hermes/scripts/
cp -r hermes-agent-backup/profiles/* ~/.hermes/profiles/
cp hermes-agent-backup/config.yaml ~/.hermes/
cp hermes-agent-backup/SOUL.md ~/.hermes/
cp hermes-agent-backup/architecture-notes.md ~/.hermes/
cp hermes-agent-backup/channel_directory.json ~/.hermes/

# 3. Re-create the cron job (re-run Step 4 on the new machine)
# 4. Re-install any tools referenced in skills (node, gh, LibreOffice, etc.)
```

**State files NOT restored** — `state.db`, `sessions/`, etc. are intentionally excluded. Hermes will regenerate them fresh.

---

## Pitfalls

- **`gh repo clone` destination**: `gh clone owner/repo` places the repo at `./repo` relative to current working directory, NOT `$HOME/repo`. Always `cd` to `~/.hermes/` before cloning so it lands in the right place.
- **Embedded git repos in skills**: Skills like `humanizer` are full git repos. `git add .` will warn about embedded repos — this is fine, they track as-is. Do not `git rm --cached` them unless you want to flatten the submodule.
- **`.env` excluded**: Never back up `.env` — it contains credentials. If you rely on env vars stored there, record the key names in a `REFERENCES.md` or `scripts/setup-env.sh` template instead.
- **`state.db` is huge**: At ~400MB+ it's impractical to version. Exclude it — Hermes rebuilds state from sessions on startup.
