#!/usr/bin/env bash

# This script cancels all your jobs that are currently running, pending, or queued.

set -euo pipefail

# Run `squeue | grep sibwang` and capture output
output="$(squeue | grep sibwang || true)"

# Capture all regex matches of (\d{8}) (unique) - these are job IDs
# This can be improved upon as squeue supports generating outputs in user-specified
# formats. But for now this works and we might need to change 8 to 9 as the global
# job count increases.
matches=()
if [[ -n "$output" ]]; then
  mapfile -t matches < <(printf '%s\n' "$output" | grep -Eo '([0-9]{8})' | sort -u)
fi

# Print prompt for confirmation
count="${#matches[@]}"
echo "Found $count currently running, pending, or queued jobs. Cancel all of them? [y/N]"

# If user confirms, scancel each match
read -r ans
if [[ "$count" -gt 0 && "$ans" =~ ^[yY]$ ]]; then
  for jobid in "${matches[@]}"; do
    echo "Cancelling job $jobid ..."
    scancel "$jobid"
  done
  echo "Done."
else
  echo "No jobs canceled."
fi
