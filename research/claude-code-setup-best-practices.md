# Claude Code Setup Best Practices
**TL;DR:** Your current setup has the right MCP stack, good skills/agents structure, but `settings.local.json` is a 177-line mess with zero deny rules — the single highest-leverage fix. Below is a practical guide tuned for the dental marketing / US expansion workflow.

**Date:** 2026-03-11 | **Sources:** Perplexity Deep Research, Anthropic docs, community survey

---

## 1. Most Useful MCP Servers (Ranked by Value for This Use Case)

| Server | What it does | Relevance to You | Priority |
|--------|-------------|-----------------|----------|
| **Sequential Thinking** | Offloads multi-step reasoning to file, saves context | Long research + pipeline tasks | HIGH |
| **Memory** | Persists knowledge graph across sessions | Re-using clinic data, decisions, patterns | HIGH |
| **Supabase** | Direct DB query + schema awareness | Lead gen dashboards, clinic data | HIGH |
| **GitHub MCP** | Issues, PRs, commit history in-context | EC2 deploy workflow, multi-branch | HIGH |
| **Ref / Context7** | Extracts only relevant parts of web pages (~80% less tokens than raw fetch) | Competitor research, docs | MEDIUM |
| **Filesystem** | Scoped file ops with per-project permissions | Already handled via Claude Code native | LOW (built-in) |
| **Slack** | Read/write Slack for notifications/archiving | If you move to team or want deploy alerts | LOW |
| **PostgreSQL/SQLite** | Direct DB access without Supabase abstraction | Only if you self-host DB on EC2 | SITUATIONAL |

**Already in use and keep:** Playwright, Perplexity, Gemini, Apify, Figma — all high value for this workflow.

**What to add next:** Sequential Thinking + Memory MCP are the two highest-ROI additions not yet in use. They directly address context bloat across long sessions.

**Key principle:** Every MCP adds tool definitions to the context window even when idle. Fewer active servers = better performance in long sessions.

---

## 2. Community Plugins Worth Using

| Plugin | What it does | Useful for you? |
|--------|-------------|----------------|
| **commit-commands** | `/commit`, `/pr`, `/push` workflows | Yes — cleaner git ops |
| **pr-review-toolkit** | Subagent reviews PRs for security + patterns | Yes — EC2 deploy safety |
| **code-intelligence** | LSP-based jump-to-definition for TS/JS | Yes — for booking widget / dashboard |
| **monorepo-management** | Optimizes multi-package build pipelines | Yes — templates + widget + dashboard |
| **database-optimization** | Expert DB schema review | Yes — once Supabase is central |
| **deep-researcher** (custom) | Already exists in your agents! | Already covered |

**Plugin marketplace:** `~/.claude/plugins/` or `.claude/plugins/` per project.
**Reality check:** Your existing 30 skills + 27 agents already cover most of what generic plugins offer. Focus on gaps, not duplication.

---

## 3. Agents vs Skills: When to Use Which

### The Mental Model
- **Skills** = domain knowledge containers (the "what we know and how we work")
- **Agents** = parallel workers (the "run this independently with its own context")
- **Workflows** = step-by-step procedures nested inside skills

### Decision Framework

| Situation | Use |
|-----------|-----|
| Work stays in one functional domain | Skill |
| Task A output feeds into Task B | Skill workflow (sequential) |
| 3+ independent data sources to pull simultaneously | Agents (parallel) |
| Task requires deep exploration of a large surface | Subagent (preserve main context) |
| Reusable domain expertise across projects | Skill in `~/.claude/skills/` |
| Project-specific knowledge | Skill in `.claude/skills/` |

### Recommended Skill Structure for This Workflow

```
~/.claude/skills/                    ← GLOBAL (all projects)
  08-prompt-engineering-master/      ← already exists, good
  deep-researcher/                   ← already exists

.claude/skills/                      ← PROJECT-LEVEL (dentist SaaS)
  lead-generation/
    Workflows/
      capture.md       ← form ingestion, Apify sources
      score.md         ← scoring logic
      nurture.md       ← follow-up sequences
  website-templates/
    Workflows/
      create.md        ← new template from brief
      deploy.md        ← push to EC2
      test.md          ← Playwright cross-browser
  content/
    Workflows/
      research.md      ← competitive + SEO research
      write.md         ← blog/copy with brand voice
      publish.md       ← schedule + distribute
  analytics/
    Workflows/
      dashboard.md     ← build reporting views
      report.md        ← generate clinic owner summaries
```

### When to Use Agents (Parallel)
- Daily business digest: pull Slack + analytics + tasks simultaneously
- Competitive research: analyze 10+ competitor clinic sites in parallel
- Bulk report generation: generate 5 clinic reports simultaneously
- Multi-city market research: parallel scrapes per city

### Current Setup Assessment
Your 27 agents are well-named but likely **overlap with skills**. Agents like `analyst.md`, `copywriter.md`, `seo-specialist.md` read more like roles/skills than true parallel workers. Consider:
- Keep as agents: tasks that should run with **fresh isolated context**
- Convert to skills: domain expertise that should **inform** the main session

---

## 4. Permissions: settings.local.json — Fix This First

### Current Problem
Your `settings.local.json` is 177 lines of accumulated one-off `allow` rules with **zero deny rules**. Problems:
1. Allows `rm:*` with no restrictions — can delete anything
2. Allows `curl:*` unrestricted — could exfiltrate or download anything
3. Allows `ssh:*` unrestricted — full server access
4. Hundreds of one-off `WebFetch(domain:...)` rules should be replaced with a permissive global WebFetch allow
5. Long shell pipeline snippets hardcoded as allowed commands (lines 58-74) — these are junk

### Recommended Clean settings.local.json

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(python3 *)",
      "Bash(pip3 *)",
      "Bash(node *)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(mv *)",
      "Bash(cp *)",
      "Bash(find *)",
      "Bash(grep *)",
      "Bash(rg *)",
      "Bash(cat *)",
      "Bash(wc *)",
      "Bash(sort *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(chmod *)",
      "Bash(touch *)",
      "Bash(echo *)",
      "Bash(sed *)",
      "Bash(curl *)",
      "Bash(ssh *)",
      "Bash(scp *)",
      "Bash(docker *)",
      "Bash(make *)",
      "Bash(open *)",
      "Bash(kill *)",
      "Bash(lsof *)",
      "Bash(pgrep *)",
      "Bash(pkill *)",
      "Bash(rm *)",
      "Bash(sqlite3 *)",
      "Bash(ffmpeg *)",
      "Bash(gh *)",
      "WebFetch(*)",
      "WebSearch",
      "Write(*)",
      "Read(*)",
      "mcp__perplexity__*",
      "mcp__gemini__*",
      "mcp__apify__*",
      "mcp__playwright__*",
      "mcp__figma__*"
    ],
    "deny": [
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/secrets/**)",
      "Read(**/.aws/credentials)",
      "Read(**/.ssh/id_rsa)",
      "Edit(**/.env)",
      "Edit(**/.env.*)",
      "Edit(**/secrets/**)",
      "Bash(rm -rf /)",
      "Bash(sudo rm -rf *)"
    ]
  }
}
```

This is ~60 lines vs 177, covers everything you actually need, and adds critical deny rules for secrets. The glob `mcp__perplexity__*` replaces 4 individual MCP entries.

### Project-level .claude/settings.json (commit to git)
```json
{
  "permissions": {
    "deny": [
      "Read(**/.env*)",
      "Read(**/secrets/**)",
      "Edit(**/secrets/**)"
    ]
  }
}
```
Keep project settings minimal and focused on secrets protection.

### Permission Precedence (highest to lowest)
`managed → CLI args → local → project → user`
Deny rules always win regardless of level.

---

## 5. Global vs Project-Level: What Goes Where

### ~/.claude/CLAUDE.md (Global)
Should be **stable for years**. Contains:
- Your identity as a developer (solo, building dental SaaS, US market focus)
- Universal code style preferences (language, formatting, naming)
- Response style preferences (brief by default, no emoji, files over walls of text)
- Debugging philosophy
- Default tools you always use
- The "one-person $10M company" operating context

**Keep it under 500 lines. Yours already exists and looks solid.**

### .claude/CLAUDE.md (Project-level, committed)
Should document **this specific project**. Contains:
- System architecture (widget → backend API → EC2)
- Data model summary (clinics, leads, campaigns, templates)
- Key technology choices + WHY (e.g., "Supabase over raw Postgres: managed infra priority")
- Deployment procedure (git push → GitHub Actions → EC2)
- Known limitations (e.g., analytics cap at X leads)
- External integrations in use
- EC2 server details (IP, SSH key location reference)
- Testing standards

### What NOT to put in CLAUDE.md
- Credentials or IPs in plaintext
- Content that changes weekly (put in progress-log.md instead)
- Full code examples (link to files)
- Duplicates of global preferences

### Directory Structure Best Practice
```
.claude/
  settings.json          ← committed, team-safe rules
  settings.local.json    ← gitignored, personal rules
  agents/                ← role-based agents (analyst, copywriter, etc.)
  skills/                ← domain knowledge (lead-gen, templates, etc.)
  hooks/                 ← automation scripts
CLAUDE.md                ← project context (committed)
```

---

## 6. Recommended Hooks

Hooks fire at: `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Stop`

### Hook 1: Block Secrets Writes (PreToolUse) — HIGHEST PRIORITY
```bash
#!/bin/bash
# .claude/hooks/block-secrets.sh
TOOL="$1"
INPUT="$2"

if [[ "$TOOL" == "Edit" || "$TOOL" == "Write" ]]; then
    FILE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('path',''))" 2>/dev/null)
    if [[ "$FILE" == *".env"* || "$FILE" == *"secrets"* || "$FILE" == *"credentials"* ]]; then
        echo "BLOCKED: Cannot write to secrets files" >&2
        exit 2
    fi
fi
exit 0
```

### Hook 2: Confirm Before EC2 Deployment (PreToolUse)
```bash
#!/bin/bash
# .claude/hooks/confirm-deploy.sh
INPUT="$2"
if [[ "$INPUT" == *"ssh"*"ec2"* ]] || [[ "$INPUT" == *"scp"*".pem"* ]]; then
    echo '{"hookSpecificOutput": {"permissionDecision": "ask"}}'
    exit 0
fi
exit 0
```

### Hook 3: Filter Test Output (PostToolUse) — Saves Context
```bash
#!/bin/bash
# .claude/hooks/filter-test-output.sh
TOOL="$1"
OUTPUT="$2"
if [[ "$TOOL" == "Bash" && ${#OUTPUT} -gt 5000 ]]; then
    FAILURES=$(echo "$OUTPUT" | grep -E "FAIL|Error:|failed|✗" -A 3)
    if [[ -n "$FAILURES" ]]; then
        echo "=== Test Failures Only ==="
        echo "$FAILURES"
    else
        echo "All tests passed (full output filtered)"
    fi
    exit 0
fi
exit 0
```

### Hook 4: Auto-log Tool Calls (PreToolUse)
```bash
#!/bin/bash
# .claude/hooks/audit-log.sh
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "$TIMESTAMP | $1 | $(echo $2 | head -c 200)" >> ~/.claude/tool-audit.log
exit 0
```

### Hook Registration (settings.json)
```json
{
  "hooks": {
    "PreToolUse": [
      {"command": ".claude/hooks/block-secrets.sh"},
      {"command": ".claude/hooks/confirm-deploy.sh"},
      {"command": ".claude/hooks/audit-log.sh"}
    ],
    "PostToolUse": [
      {"command": ".claude/hooks/filter-test-output.sh"}
    ]
  }
}
```

---

## 7. Actionable Priority List

| Priority | Action | Impact |
|----------|--------|--------|
| 1 | **Clean settings.local.json** — replace 177 lines with ~60, add deny rules | Security + maintainability |
| 2 | **Add Sequential Thinking MCP** — offloads reasoning, saves context in long sessions | Context efficiency |
| 3 | **Add Memory MCP** — persist cross-session knowledge (clinic data, decisions) | Productivity |
| 4 | **Implement block-secrets.sh hook** — safety net for .env/secrets writes | Security |
| 5 | **Implement confirm-deploy.sh hook** — prompt before EC2 SSH/SCP | Avoid accidents |
| 6 | **Restructure skills into domain folders** (lead-gen, templates, content, analytics) vs current numbered list | Clarity |
| 7 | **Add project-level CLAUDE.md** for Dentists project with architecture + EC2 docs | Context quality |
| 8 | **Add Supabase MCP** once backend moves off SQLite | DB debugging speed |

---

## Sources
1. Perplexity Deep Research — Claude Code MCP best practices (2026-03-11)
2. https://code.claude.com/docs/en/settings
3. https://code.claude.com/docs/en/permissions
4. https://code.claude.com/docs/en/hooks
5. https://code.claude.com/docs/en/best-practices
6. https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents
7. https://scottspence.com/posts/optimising-mcp-server-context-usage-in-claude-code
8. https://diamantai.substack.com/p/youre-using-claude-code-wrong-and
9. https://uxplanet.org/claude-md-best-practices-1ef4f861ce7c
10. https://github.com/MCP-Mirror/win4r_Awesome-Claude-MCP-Servers
11. https://dev.to/jennyouyang/best-mcp-servers-for-claude-code-replace-your-workflow-keep-your-brain-401l
