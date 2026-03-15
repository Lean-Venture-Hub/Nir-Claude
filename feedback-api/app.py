#!/usr/bin/env python3
"""Feedback API — tiny Flask service for gallery & section builder feedback.
Runs on port 5111 behind nginx reverse proxy.
"""
import fcntl
import json
import os
import time
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

FEEDBACK_DIR = os.environ.get("FEEDBACK_DIR", "/var/www/lp.scalefox.ai/feedback")
VALID_TOOLS = {"gallery", "sections"}


def _path(tool):
    return os.path.join(FEEDBACK_DIR, f"{tool}-feedback.json")


def _log_path():
    return os.path.join(FEEDBACK_DIR, "feedback-log.jsonl")


def _read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.flush()
        fcntl.flock(f, fcntl.LOCK_UN)


def _append_log(entry):
    os.makedirs(FEEDBACK_DIR, exist_ok=True)
    with open(_log_path(), "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)


def _rebuild_summary(data, tool):
    """Rebuild summary block from current data."""
    now = datetime.now(timezone.utc).isoformat()
    if tool == "gallery":
        like_counts = {}
        for user, likes in data.get("likes", {}).items():
            for key, val in likes.items():
                if val:
                    like_counts[key] = like_counts.get(key, 0) + 1
        total_comments = sum(len(v) for v in data.get("comments", {}).values())
        data["summary"] = {
            "templateLikeCounts": like_counts,
            "totalComments": total_comments,
            "lastUpdated": now,
        }
    elif tool == "sections":
        all_ratings = {}
        for user, ratings in data.get("ratings", {}).items():
            for key, val in ratings.items():
                all_ratings.setdefault(key, []).append(val)
        avg_ratings = {k: round(sum(v) / len(v), 1) for k, v in all_ratings.items()}
        total_bugs = sum(
            1
            for user_bugs in data.get("bugs", {}).values()
            for b in user_bugs.values()
            if b.get("flagged")
        )
        data["summary"] = {
            "avgRatings": avg_ratings,
            "totalRated": len(all_ratings),
            "totalBugs": total_bugs,
            "lastUpdated": now,
        }
    return data


# ── Routes ──

@app.route("/api/feedback/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/api/feedback/<tool>", methods=["GET"])
def get_feedback(tool):
    if tool not in VALID_TOOLS:
        return jsonify({"error": f"Unknown tool: {tool}"}), 400
    data = _read_json(_path(tool))
    return jsonify(data)


@app.route("/api/feedback", methods=["POST"])
def post_feedback():
    body = request.get_json(force=True)
    tool = body.get("tool")
    user = body.get("user", "").strip()
    action = body.get("action")
    key = body.get("key", "")
    value = body.get("value")

    if tool not in VALID_TOOLS:
        return jsonify({"error": f"Unknown tool: {tool}"}), 400
    if not user:
        return jsonify({"error": "user is required"}), 400
    if not action:
        return jsonify({"error": "action is required"}), 400

    path = _path(tool)
    data = _read_json(path)

    # ── Gallery actions ──
    if tool == "gallery":
        if action == "like":
            data.setdefault("likes", {}).setdefault(user, {})[key] = bool(value)
            # Clean up false likes
            if not value:
                data["likes"][user].pop(key, None)
        elif action == "comment":
            data.setdefault("comments", {}).setdefault(key, []).append({
                "user": user,
                "text": str(value),
                "timestamp": int(time.time() * 1000),
            })
        elif action == "delete_comment":
            comments = data.get("comments", {}).get(key, [])
            idx = body.get("index")
            if isinstance(idx, int) and 0 <= idx < len(comments):
                if comments[idx].get("user") == user:
                    comments.pop(idx)
        elif action == "bulk_sync":
            # Full sync of a user's likes + any new comments
            if "likes" in body:
                data.setdefault("likes", {})[user] = body["likes"]
            if "comments" in body:
                for ckey, clist in body["comments"].items():
                    existing = data.setdefault("comments", {}).setdefault(ckey, [])
                    existing_timestamps = {c["timestamp"] for c in existing}
                    for c in clist:
                        if c.get("timestamp") not in existing_timestamps:
                            existing.append({**c, "user": user})
        else:
            return jsonify({"error": f"Unknown action: {action}"}), 400

    # ── Sections actions ──
    elif tool == "sections":
        if action == "rate":
            data.setdefault("ratings", {}).setdefault(user, {})[key] = value
        elif action == "bug":
            data.setdefault("bugs", {}).setdefault(user, {})[key] = value
        elif action == "bulk_sync":
            if "ratings" in body:
                data.setdefault("ratings", {})[user] = body["ratings"]
            if "bugs" in body:
                data.setdefault("bugs", {})[user] = body["bugs"]
        else:
            return jsonify({"error": f"Unknown action: {action}"}), 400

    data = _rebuild_summary(data, tool)
    _write_json(path, data)

    # Audit log
    _append_log({
        "ts": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "user": user,
        "action": action,
        "key": key,
    })

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5111, debug=False)
