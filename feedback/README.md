# Template Feedback

Drop exported feedback JSON files here. The `template-creator` skill reads them before designing new templates.

## Expected files

- `gallery-feedback.json` — exported from the gallery (likes + comments)
- `sections-feedback.json` — exported from the sections builder (ratings + bugs)

## How to use

1. In the gallery, click hearts on templates you like, add comments with design notes
2. In the sections builder, rate sections and flag bugs
3. Click "Export Feedback" in either tool to download a JSON file
4. Place the downloaded file in this `feedback/` folder
5. The `template-creator` skill will read these files in Step 0.5 when designing new templates
