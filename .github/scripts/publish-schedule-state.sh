#!/usr/bin/env bash
# publish-schedule-state.sh — persist the staggered schedule WITHOUT pushing to protected `main`.
#
# THE DEFECT THIS REPLACES. `staggered-scheduling.yml` committed the schedule and ran a bare
# `git push` at two sites. `main` is protected behind a merge queue with 8 required checks, so
# every push was rejected — `GH006: Protected branch update failed ... Changes must be made
# through the merge queue` — and the "Save schedule" step had no fail-open guard, so the job
# failed on EVERY scheduled run and would have forever. The second site (`Update schedule
# status`) was already tolerant (`git push || echo ...`), so it failed silently instead: the
# same defect, only quieter.
#
# WHY A BRANCH AND NOT THE MERGE QUEUE. The schedule is cross-run automation state, not
# reviewable source. Routing a daily bot commit through a queue with 8 required checks would
# spend CI on a machine-written JSON file and pile up an unmergeable PR per day. State belongs
# on its own unprotected branch.
#
# WHY THE CONTENTS API AND NOT `git push`. Publishing to another branch with git would mean
# checking it out, which swaps the working tree out from under the later steps that still need
# `src/automation/scripts/` and `repos_today.txt`. The Contents API writes a branch without
# touching the checkout at all. `contents: write` is already granted by the workflow.
#
#   publish-schedule-state.sh <file> <branch> <commit-message>
set -euo pipefail

FILE="${1:?schedule file required}"
BRANCH="${2:?state branch required}"
MESSAGE="${3:?commit message required}"
REPO="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY required}"
API="${GITHUB_API_URL:-https://api.github.com}"
DEFAULT_BRANCH="${GITHUB_DEFAULT_BRANCH:-main}"

if [ ! -f "$FILE" ]; then
  echo "publish-schedule-state: $FILE does not exist — nothing to publish"
  exit 0
fi

AUTH=(-H "Accept: application/vnd.github+json" -H "Authorization: Bearer ${GITHUB_TOKEN:?GITHUB_TOKEN required}")

for tool in curl jq base64; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "::error::publish-schedule-state requires $tool" >&2
    exit 1
  fi
done

decode_base64() {
  if base64 --help 2>&1 | grep -q -- '--decode'; then
    base64 --decode
  else
    base64 -D
  fi
}

# Create the state branch off the default branch on first use.
if ! curl -fsS "${AUTH[@]}" "$API/repos/$REPO/git/ref/heads/$BRANCH" >/dev/null 2>&1; then
  base_sha=$(curl -fsS "${AUTH[@]}" "$API/repos/$REPO/git/ref/heads/$DEFAULT_BRANCH" | jq -r '.object.sha')
  curl -fsS -X POST "${AUTH[@]}" "$API/repos/$REPO/git/refs" \
    -d "$(jq -n --arg ref "refs/heads/$BRANCH" --arg sha "$base_sha" '{ref: $ref, sha: $sha}')" >/dev/null
  echo "created state branch $BRANCH"
fi

# The blob sha is REQUIRED to update an existing file and must be OMITTED to create one —
# sending an empty sha is a 422, so the payload is built conditionally below.
existing=$(curl -fsS "${AUTH[@]}" "$API/repos/$REPO/contents/$FILE?ref=$BRANCH" 2>/dev/null || echo '{}')
existing_sha=$(printf '%s' "$existing" | jq -r '.sha // empty')

# Skip a no-op write so the branch does not accumulate an empty commit per day.
if [ -n "$existing_sha" ]; then
  if ! remote=$(printf '%s' "$existing" | jq -r '.content // empty' | tr -d '\\n' | decode_base64 2>/dev/null); then
    echo "::error::existing schedule state could not be decoded" >&2
    exit 1
  fi
  if [ "$remote" = "$(cat "$FILE")" ]; then
    echo "schedule unchanged — nothing to publish"
    exit 0
  fi
fi

# base64 -w0 is GNU; macOS/BSD base64 has no -w and already emits a single line.
encoded=$(base64 -w0 < "$FILE" 2>/dev/null || base64 < "$FILE" | tr -d '\n')

payload=$(jq -n \
  --arg message "$MESSAGE" \
  --arg content "$encoded" \
  --arg branch "$BRANCH" \
  --arg sha "$existing_sha" \
  '{message: $message, content: $content, branch: $branch}
   + (if $sha == "" then {} else {sha: $sha} end)')

curl -fsS -X PUT "${AUTH[@]}" "$API/repos/$REPO/contents/$FILE" -d "$payload" >/dev/null
echo "published $FILE to $BRANCH"
