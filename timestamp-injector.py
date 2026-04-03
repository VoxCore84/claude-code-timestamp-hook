#!/usr/bin/env python3
"""UserPromptSubmit hook: inject a timestamp into every user message.

Claude Code has no concept of time. No clock, no timestamps between messages,
no awareness of whether 30 seconds or 30 hours passed between turns. This hook
fixes that by injecting the current date/time as additionalContext on every
user prompt.

What this unlocks:
  - Claude can see elapsed time between messages (fatigue, AFK, next day)
  - Claude knows time-of-day (stop suggesting tasks at 2 AM)
  - Claude can track how long multi-step operations take across turns
  - Claude can calibrate urgency to your actual schedule

Install: See README.md or just copy this file to .claude/hooks/ and add the
hook entry to .claude/settings.local.json.
"""
import json
import sys
from datetime import datetime


def main():
    try:
        json.load(sys.stdin)  # consume stdin (required by hook protocol)
    except Exception:
        sys.exit(0)

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = now.strftime("%A")

    result = {
        "additionalContext": f"[TIMESTAMP] User message received: {day_of_week} {timestamp}"
    }
    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
