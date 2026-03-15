---
name: end-session
description: Close out a Claude Code session cleanly — log work to SESSIONS.md, sync PLAN.md, audit CLAUDE.md for dead references, prune stale memory, clean up orphaned task lists, and flag uncommitted changes. Run this before closing any Claude Code window.
---

# End Session — Full Cleanup & Sync

Close out the current session and clean all persistent state files. This is the only skill that maintains hygiene across CLAUDE.md, PLAN.md, SESSIONS.md, and memory.

## Trigger

- User says "end session", "close session", "wrap up", "clean up session"
- User runs `/end-session`
- Before closing a Claude Code window

## No Inputs Required

The skill auto-detects everything from the current conversation context and filesystem.

---

## Step 1: Gather Current State (parallel reads)

Read all of these in parallel:
1. `SESSIONS.md`
2. `PLAN.md`
3. `CLAUDE.md`
4. Memory index: `memory/MEMORY.md` (auto-memory path from system)
5. `git status --short` (uncommitted changes)
6. `git log --oneline -1` (last commit)
7. `ls ~/.claude/tasks/` (stale task lists)
8. `ls ~/.claude/teams/` (stale teams)
9. `TaskList` (current session tasks)

---

## Step 2: Log This Session to SESSIONS.md

### 2a: Update current session row
- Set Status → "Done"
- Set Last Action → summary of what was accomplished (1 line)
- Set Next Step → what the next session should pick up (be specific)

### 2b: Clean the Current Sessions table
- Remove rows with Status "Done" that are older than 3 days
- Move their summaries to "Recently Completed Work" section (if not already there)

### 2c: Clean Recently Completed Work
- Remove entries older than 7 days — they should already be in PLAN.md
- If they're NOT in PLAN.md, add them before removing

### 2d: Flag stale sessions
- Any row in Current Sessions that hasn't been updated in 2+ days → add "(STALE?)" to Status
- Print these to chat so user can close those windows

---

## Step 3: Sync PLAN.md with Reality

### 3a: Check completed phases
- Scan for phases/tasks marked "IN PROGRESS" or "TODO"
- Cross-reference with SESSIONS.md "Recently Completed Work"
- If work was done that advances a task → update its status in PLAN.md

### 3b: Verify counts and facts
- Template counts: `ls templates/*/website/ | wc` per vertical vs what PLAN.md says
- Verify "Deployed" column by checking `servers/lp-scalefox-ai.md`
- Fix any mismatches

### 3c: Update timestamp
- Set "**Updated:**" to today's date

### 3d: Prune completed phases
- Phases marked DONE for 14+ days → collapse to a single summary line (not full task tables)
- Keep the phase name and completion date, remove task-level detail

---

## Step 4: Audit CLAUDE.md for Hygiene

### 4a: Dead references
Check every file path and URL mentioned in CLAUDE.md:
- `[PROJECTS.md](./PROJECTS.md)` → does it exist?
- `servers/lp-scalefox-ai.md` → does it exist?
- `SESSIONS.md` → does it exist?
- `templates/PLACEHOLDER_CONTRACT.md` → does it exist?
- `design-inspiration/web-design-playbook.md` → does it exist?
- `design-inspiration/sites.csv` → does it exist?
- `design-inspiration/inspiration-sources.md` → does it exist?
- `lessonslearned.md` → does it exist?

For each missing file: either create a stub, remove the reference, or flag to user.

### 4b: Outdated information
- Check if the pipeline table (Steps 1-10) still matches actual skills available in `.claude/skills/`
- Check if vertical naming examples match actual folders in `templates/`
- Check if "Key reference files" section lists files that exist

### 4c: Bloat check
- If CLAUDE.md exceeds 5KB, flag sections that could be moved to separate reference files
- Suggest specific moves (e.g., "Pipeline table → PIPELINE.md, referenced from CLAUDE.md")

**Print findings as a checklist. Only make fixes for dead references and clearly wrong data. Ask user before restructuring.**

---

## Step 5: Memory Audit

### 5a: Read all memory files
Read each file listed in `memory/MEMORY.md`.

### 5b: Check relevance
For each memory file:
- Is the information still accurate? (e.g., does the server IP still match?)
- Is this information now redundant with CLAUDE.md or PLAN.md?
- Is this a feedback memory that's already been incorporated into a skill?
- Is this a project memory about work that's been completed and archived?

### 5c: Report
Print a table:

| Memory | Status | Action |
|--------|--------|--------|
| server_scalefox.md | Current | Keep |
| feedback_templates_love.md | Still relevant | Keep |
| ... | Redundant with CLAUDE.md | Suggest remove |

**Only delete memories with explicit user approval.**

---

## Step 6: Clean Up Orphaned State

### 6a: Stale task lists
```bash
ls ~/.claude/tasks/
```
- Count directories
- These are from old sessions and serve no purpose
- **Ask user**: "Found {N} orphaned task lists from previous sessions. Delete them? (They contain no useful data — tasks are session-scoped)"
- If approved: `rm -rf ~/.claude/tasks/*`

### 6b: Stale teams
```bash
ls ~/.claude/teams/
```
- Same approach — ask before deleting

### 6c: Current session tasks
- Check `TaskList` for any pending/in-progress tasks
- If found: log them to SESSIONS.md "Next Step" column before closing

---

## Step 7: Git Status Check

### 7a: Uncommitted changes
```bash
git status --short
```
- If changes exist → print summary and ask: "Commit before closing?"
- If yes → create commit with session summary as message
- If no → note in SESSIONS.md: "WARNING: uncommitted changes left in working tree"

### 7b: Unpushed commits
```bash
git log origin/main..HEAD --oneline
```
- If unpushed commits exist → ask: "Push to remote?"

---

## Step 8: Output Summary

Print a concise report to chat:

```
Session closed.

Logged: {1-line summary of work done}
SESSIONS.md: updated (removed {N} stale rows)
PLAN.md: synced ({changes made or "no changes needed"})
CLAUDE.md: {N dead refs fixed / "clean"}
Memory: {N files checked, N flagged}
Orphaned tasks: {N deleted / "none"}
Git: {committed + pushed / uncommitted changes remain / clean}

Stale sessions found:
- {session focus} (last updated {date}) — close that window

Next session should: {next step from SESSIONS.md}
```

---

## Error Handling

- **Can't read a file**: Skip it, note in report as "SKIPPED — file not found"
- **SESSIONS.md doesn't exist**: Create it with the template from CLAUDE.md instructions
- **PLAN.md doesn't exist**: Flag as critical — this should always exist
- **No meaningful work done this session**: Still run cleanup steps 3-7, just log session as "Cleanup only"
- **Multiple stale sessions**: List all of them — user needs to close those windows manually
