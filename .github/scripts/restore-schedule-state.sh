#!/usr/bin/env bash
# restore-schedule-state.sh — restore state without conflating absence with retrieval failure.
set -euo pipefail

FILE="${1:?schedule file required}"
BRANCH="${2:?state branch required}"
REPO="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY required}"
API="${GITHUB_API_URL:-https://api.github.com}"

for tool in curl jq base64; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "::error::restore-schedule-state requires $tool" >&2
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

AUTH=(-H "Accept: application/vnd.github+json" -H "Authorization: Bearer ${GITHUB_TOKEN:?GITHUB_TOKEN required}")
response=$(mktemp)
trap 'rm -f "$response"' EXIT

if ! http_code=$(curl -sS "${AUTH[@]}" --get \
  --data-urlencode "ref=$BRANCH" \
  -o "$response" \
  -w '%{http_code}' \
  "$API/repos/$REPO/contents/$FILE"); then
  echo "::error::failed to retrieve schedule state" >&2
  exit 1
fi

case "$http_code" in
  200)
    mkdir -p "$(dirname "$FILE")"
    if ! jq -er 'select(.type == "file") | .content' "$response" \
      | tr -d '\n' \
      | decode_base64 > "$FILE"; then
      rm -f "$FILE"
      echo "::error::schedule-state response could not be decoded" >&2
      exit 1
    fi
    echo "restored schedule from $BRANCH"
    ;;
  404)
    rm -f "$FILE"
    echo "state branch or schedule file does not exist yet — starting from empty state"
    ;;
  *)
    message=$(jq -r '.message // "unknown GitHub API error"' "$response" 2>/dev/null || true)
    echo "::error::schedule-state retrieval failed (HTTP $http_code): $message" >&2
    exit 1
    ;;
esac
