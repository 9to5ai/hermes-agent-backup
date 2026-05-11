#!/bin/bash
# Hermes Agent nightly backup to GitHub
# Run from ~/.hermes/hermes-agent-backup

set -e

cd /Users/momo/.hermes/hermes-agent-backup

# Pull latest (in case of changes from other sessions)
git checkout main 2>/dev/null || true
git pull origin main 2>/dev/null || true

# Sync the key directories (excluding large/binary/state files)
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
rsync -av --delete \
  --exclude='.DS_Store' \
  ../memories/ ./memories/
rsync -av --delete \
  --exclude='.DS_Store' \
  ../plans/ ./plans/
rsync -av --delete \
  --exclude='.DS_Store' \
  ../scripts/ ./scripts/
rsync -av --delete \
  --exclude='.DS_Store' \
  ../profiles/ ./profiles/
rsync -av --delete \
  ../bin/ ./bin/
rsync -av --delete \
  ../hooks/ ./hooks/
rsync -av --delete \
  ../platforms/ ./platforms/
rsync -av --delete \
  ../plugins/ ./plugins/
rsync -av \
  ../config.yaml \
  ../SOUL.md \
  ../architecture-notes.md \
  ../channel_directory.json \
  ./

# Commit and push
if ! git diff --quiet; then
  git add -A
  git commit -m "Nightly backup - $(date '+%Y-%m-%d %H:%M')"
  git push origin main
  echo "Backup pushed: $(date '+%Y-%m-%d %H:%M')"
else
  echo "No changes to push - backup up to date"
fi