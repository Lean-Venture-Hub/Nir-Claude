#!/usr/bin/env python3
"""One-time migration: convert existing gallery feedback to multi-user format.
Run locally, then upload the result to the server.

Usage: python3 feedback-api/migrate-existing.py
"""
import json
import os

INPUT = "feedback/gallery-feedback-2026-03-15.json"
OUTPUT = "feedback/gallery-feedback-migrated.json"

with open(INPUT) as f:
    old = json.load(f)

# Convert likes: { key: true } → { "nir": { key: true } }
old_likes = old.get("gallery", {}).get("likes", {})
# Convert comments: { key: [{text, timestamp}] } → { key: [{user: "nir", text, timestamp}] }
old_comments = old.get("gallery", {}).get("comments", {})

new_comments = {}
for key, clist in old_comments.items():
    new_comments[key] = [
        {"user": "nir", "text": c["text"], "timestamp": c["timestamp"]}
        for c in clist
    ]

# Build like counts
like_counts = {}
for key, val in old_likes.items():
    if val:
        like_counts[key] = 1

migrated = {
    "likes": {"nir": old_likes},
    "comments": new_comments,
    "summary": {
        "templateLikeCounts": like_counts,
        "totalComments": sum(len(v) for v in new_comments.values()),
        "lastUpdated": old.get("exportDate", ""),
    },
}

with open(OUTPUT, "w") as f:
    json.dump(migrated, f, indent=2, ensure_ascii=False)

print(f"Migrated {len(old_likes)} likes and {migrated['summary']['totalComments']} comments → {OUTPUT}")
print(f"\nTo deploy: scp -i ~/.ssh/test_env_ec2.pem {OUTPUT} ubuntu@18.184.97.242:/var/www/lp.scalefox.ai/feedback/gallery-feedback.json")
