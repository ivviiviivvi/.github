#!/bin/bash
set -e

LOCK_FILE=".github/state.lock"

function acquire_lock {
  # Try to create a lock file. If it already exists, another process holds the lock.
  # We'll wait for a short period for it to be released.
  timeout=60 # seconds
  start_time=$(date +%s)

  while [ -f "$LOCK_FILE" ]; do
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if [ "$elapsed_time" -ge "$timeout" ]; then
      echo "Error: Lock file has been held for too long. Aborting."
      # Optionally, remove the stale lock file
      # rm -f "$LOCK_FILE"
      exit 1
    fi

    echo "Waiting for lock..."
    sleep 5
  done

  # Create the lock file
  touch "$LOCK_FILE"
}

function release_lock {
  # Remove the lock file
  rm -f "$LOCK_FILE"
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
