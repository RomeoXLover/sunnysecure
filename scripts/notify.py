#!/usr/bin/env python3
"""Discord webhook notification helper for file-by-file updates."""

import json
import os
import sys
import httpx

WEBHOOK_URL = "https://discord.com/api/webhooks/1561431216513880075/5RpOjKOJs6XNv6Ir3c5IJ2iOdag4SO9g46zhCgVGR_pmvcPq-xeX8S9H66U_l_mCLu6H"

REPO_URL = "https://github.com/RomeoXLover/sunnysecure"
MAINTAINER = "Romeo"

COLORS = {
    "ADDED": 5793266,
    "MODIFIED": 3447004,
    "FIXED": 5763719,
    "IMPROVED": 15811146,
    "TESTED": 4527487,
}


def notify(
    file_path: str,
    action: str,
    summary: str,
    reason: str,
    features: str,
    validation: str,
    commit_hash: str,
    commit_msg: str,
    push_status: str = "SUCCESS",
    discord_status: str = "SUCCESS",
) -> bool:
    color = COLORS.get(action, 5793266)

    payload = {
        "username": "SunnySecure Bot",
        "embeds": [
            {
                "title": f"📦 File Update — SunnySecure ({action})",
                "description": summary,
                "color": color,
                "fields": [
                    {"name": "File", "value": f"`{file_path}`", "inline": False},
                    {"name": "Action", "value": action, "inline": True},
                    {"name": "Validation", "value": validation, "inline": True},
                    {"name": "Push Status", "value": push_status, "inline": True},
                    {"name": "Reason", "value": reason, "inline": False},
                    {"name": "Features", "value": features, "inline": False},
                    {
                        "name": "Git Commit",
                        "value": f"`{commit_hash[:10]}`\n{commit_msg}",
                        "inline": False,
                    },
                    {
                        "name": "GitHub Link",
                        "value": f"{REPO_URL}/commit/{commit_hash}",
                        "inline": False,
                    },
                    {
                        "name": "Discord Delivery",
                        "value": discord_status,
                        "inline": True,
                    },
                    {"name": "Maintainer", "value": MAINTAINER, "inline": True},
                ],
                "footer": {"text": f"Maintained by {MAINTAINER}"},
            }
        ],
    }

    try:
        resp = httpx.post(WEBHOOK_URL, json=payload, timeout=15.0)
        if resp.status_code in (200, 204):
            return True
        print(f"Discord webhook failed: {resp.status_code} — {resp.text}", file=sys.stderr)
        return False
    except httpx.HTTPError as e:
        print(f"Discord webhook error: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # CLI usage: python3 scripts/notify.py <file> <action> <summary> <reason> <features> <validation> <commit_hash> <commit_msg> <push_status> <discord_status>
    args = sys.argv[1:]
    if len(args) >= 8:
        notify(*args[:8], push_status=args[8] if len(args) > 8 else "SUCCESS",
               discord_status=args[9] if len(args) > 9 else "SUCCESS")
