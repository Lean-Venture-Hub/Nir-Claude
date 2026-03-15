# Template Feedback

Feedback from the gallery and section builder auto-syncs to the server. No manual export needed.

## How it works

1. Open the gallery or section builder on the production URL
2. Enter your name when prompted (stored in browser, sent with every action)
3. Like templates, add comments, rate sections, flag bugs — all synced automatically
4. Feedback is stored at `/var/www/lp.scalefox.ai/feedback/` on the server

## Server files

- `gallery-feedback.json` — likes (per user) + comments (with user attribution)
- `sections-feedback.json` — ratings (per user) + bugs (per user)
- `feedback-log.jsonl` — append-only audit trail of all actions

## Reading feedback from Claude Code

```bash
ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242 "cat /var/www/lp.scalefox.ai/feedback/gallery-feedback.json"
ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242 "cat /var/www/lp.scalefox.ai/feedback/sections-feedback.json"
```

## Offline fallback

If the API is unreachable, feedback saves to localStorage and works locally. The green dot in the nav turns red when offline.
