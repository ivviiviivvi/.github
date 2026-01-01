#!/bin/bash
set -e

# Deprecated: This script uses directory-based locking which is prone to stale locks.
# New code should rely on quota_manager.py's internal fcntl-based locking.
# This script is kept for backward compatibility if any external tools rely on it,
# but it now warns about deprecation.

LOCK_DIR=".github/state.lock"

function acquire_lock {
  echo "WARNING: scripts/manage_lock.sh is deprecated. Use quota_manager.py internal locking."
  # Try to create a lock directory. If it already exists, another process holds the lock.
  # We'll wait for a short period for it to be released.
  timeout=60 # seconds
  start_time=$(date +%s)

  while ! mkdir "$LOCK_DIR" 2>/dev/null; do
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if [ "$elapsed_time" -ge "$timeout" ]; then
      echo "Error: Lock directory has been held for too long. Aborting."
      # Optionally, remove the stale lock file
      # rmdir "$LOCK_DIR"
      exit 1
    fi

    echo "Waiting for lock..."
    sleep 5
  done

  echo "Lock acquired."
}

function release_lock {
  # Remove the lock directory
  rmdir "$LOCK_DIR" 2>/dev/null || true
  echo "Lock released."
}

# The main logic of the script
if [ "$1" == "acquire" ]; then
  acquire_lock
elif [ "$1" == "release" ]; then
  release_lock
else
  echo "Usage: $0 {acquire|release}"
  exit 1
fi
