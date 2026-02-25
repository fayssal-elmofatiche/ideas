# Claudio

**Claude I/O — A developer dashboard for Claude Code users.**

Claudio parses your local Claude Code session data and turns it into actionable insights: what you spent, what you built, what patterns work, and whether your codebase is getting better or worse over time.

One tool. Local-first. No accounts, no cloud, no telemetry.


## The Problem

Claude Code stores every conversation as JSONL files in `~/.claude/projects/`. Rich data — token counts, model info, tool calls, git context, timestamps — sitting in hidden directories that nobody looks at.

You have no idea:
- How much a session cost you
- Which projects consume the most tokens
- What percentage of your codebase Claude helped write
- Whether AI-assisted code gets refactored more often
- What decisions were made three weeks ago in a session you forgot about

agentsview (by Wes McKinney) solves the viewing problem across multiple agents. Claudio goes deeper on Claude specifically — not just viewing, but extracting cost awareness, code impact metrics, and reusable knowledge.


## Who It's For

- Developers who use Claude Code daily and want to understand their usage
- Tech leads tracking AI-assisted development across a team's projects
- Anyone who wants to know if their AI-generated code is holding up over time


## Data Source

Claude Code stores session data locally:

```
~/.claude/
  projects/
    -Users-alice-code-my-app/          # encoded project path
      sessions-index.json              # metadata index
      a1b2c3d4-....jsonl               # session transcript
      a1b2c3d4-.../
        subagents/
          agent-a03dc4....jsonl        # subagent sessions
  stats-cache.json                     # aggregated usage stats
  history.jsonl                        # global command history
```

Each JSONL line is a message with:

```
type            "user" | "assistant" | "file-history-snapshot"
message.role    "user" | "assistant"
message.content [{type: "text", text: "..."}, {type: "tool_use", name: "Bash", ...}]
message.model   "claude-opus-4-6" (assistant messages only)
message.usage   {input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens}
timestamp       ISO-8601
sessionId       UUID
cwd             working directory
gitBranch       branch at time of message
toolUseResult   {durationMs, numFiles, filenames} (tool result messages)
parentUuid      links to previous message for threading
```

The `sessions-index.json` per project provides fast lookups: session ID, message count, first prompt, created/modified timestamps, git branch, project path.

The `stats-cache.json` has pre-aggregated daily totals: message counts, session counts, tool call counts, and token usage broken down by model.


## Features

### 1. Cost Tracking

Every assistant message includes token usage with input, output, and cache breakdown. Claudio aggregates this into:

```
claudio costs                          # total spend this month
claudio costs --by project             # cost per project
claudio costs --by model               # cost per model (opus vs sonnet)
claudio costs --by session             # most expensive sessions
claudio costs --last 7d --daily        # daily spend over the past week
```

Pricing is configurable (per-model rates in a config file) so it stays accurate as Anthropic updates pricing. Cache tokens are accounted for separately since they cost less.

Output example:
```
February 2026

  Total: $47.82 across 34 sessions

  By project:
    resumake          $18.40  (38%)  ████████
    konto             $12.10  (25%)  ██████
    dexter             $9.55  (20%)  █████
    ideas              $4.22   (9%)  ██
    other              $3.55   (7%)  ██

  By model:
    claude-opus-4-6   $41.20  (86%)
    claude-sonnet-4-5  $6.62  (14%)
```

### 2. Session Intelligence

Search, browse, and extract knowledge from past sessions.

```
claudio sessions                       # list recent sessions
claudio sessions --project resumake    # filter by project
claudio search "enable banking"        # full-text search across all sessions
claudio search "why sqlite" --context  # show surrounding messages
claudio recap <session-id>             # AI-generated summary of a session
claudio decisions --last 30d           # extract design decisions from recent sessions
```

The search uses SQLite FTS5 for instant full-text search across all messages. The `recap` and `decisions` commands use Claude to analyze session transcripts and extract structured insights.

### 3. Code Impact

Crosses Claude Code sessions with git history to understand AI-assisted development patterns.

```
claudio impact                         # overview: commits, files, lines touched via Claude
claudio impact --project resumake      # per-project breakdown
claudio impact --attribution           # human vs AI-assisted commit ratio
claudio impact --churn                 # AI-generated code that got reverted or heavily refactored
```

How it works:
- Session timestamps and git branch info are matched against `git log`
- Tool calls of type Edit, Write, Bash (git commit) identify which files Claude touched
- Commit timestamps within active session windows are attributed as AI-assisted
- Subsequent commits that modify the same lines are tracked as churn

Output example:
```
resumake (last 30 days)

  Commits: 47 total, 38 AI-assisted (81%)
  Files touched by Claude: 62
  Lines added via Claude: 3,420
  Lines later refactored: 180 (5.3% churn)

  Most AI-dependent files:
    resumake/html_builder.py    98% AI-assisted
    resumake/ats_cmd.py         95% AI-assisted
    resumake/tailor.py          72% AI-assisted
```

### 4. Codebase Health

Lightweight structural monitoring that tracks trends over time.

```
claudio health                         # current snapshot
claudio health --trend                 # how metrics changed over last 30 days
claudio health --project resumake      # per-project
```

Metrics tracked:
- **Complexity**: average function complexity (via radon or AST analysis)
- **File sizes**: distribution, outliers, growth trend
- **Dependency count**: number of imports/dependencies over time
- **Test ratio**: test files vs source files, test coverage if available
- **Duplication**: near-duplicate code blocks (simple AST hash comparison)

This is intentionally lightweight — not a full static analysis suite. The value is in the trend lines: is the codebase getting simpler or more complex over time? Are AI-assisted sessions increasing or decreasing structural health?


## Architecture

```
claudio/
  cmd/
    claudio/
      main.go            # CLI entrypoint (cobra)
  internal/
    parser/
      session.go         # JSONL session parser (gjson, zero-alloc)
      message.go         # message type handling
    sync/
      engine.go          # incremental sync (file watcher + worker pool)
      skip_cache.go      # persistent skip cache for unchanged files
    db/
      db.go              # SQLite with FTS5, WAL mode, reader/writer separation
      schema.sql         # tables: sessions, messages, tool_calls, costs, health_snapshots
    git/
      log.go             # git log parsing
      attribution.go     # session-commit matching, churn analysis
    health/
      analyze.go         # codebase health metrics (tree-sitter or shell out to radon)
    cost/
      pricing.go         # model pricing config and cost calculation
    server/
      server.go          # HTTP server (stdlib net/http)
      routes.go          # REST API + SSE endpoints
      embed.go           # go:embed for Svelte frontend
  frontend/
    (Svelte app)         # dashboard UI, embedded at build time
  claudio.toml           # default config (pricing, paths)
```

### Sync Engine

On first run, claudio walks `~/.claude/projects/`, parses all JSONL files, and loads them into a local SQLite database. Subsequent runs use incremental sync:

- Check file mtime against last sync
- For changed files, read only new lines (JSONL is append-only)
- Batch inserts for efficiency
- File watcher (fsnotify) for live updates
- Periodic full sync as safety net

The database is disposable — it can always be rebuilt from the source JSONL files. No migrations needed.

### SQLite Schema (core tables)

```sql
sessions (
  id TEXT PRIMARY KEY,
  project TEXT,
  project_path TEXT,
  first_prompt TEXT,
  git_branch TEXT,
  message_count INTEGER,
  created_at TEXT,
  modified_at TEXT,
  total_input_tokens INTEGER,
  total_output_tokens INTEGER,
  total_cache_read_tokens INTEGER,
  total_cache_creation_tokens INTEGER,
  estimated_cost_usd REAL
)

messages (
  id TEXT PRIMARY KEY,
  session_id TEXT REFERENCES sessions(id),
  ordinal INTEGER,
  role TEXT,
  content TEXT,
  model TEXT,
  input_tokens INTEGER,
  output_tokens INTEGER,
  timestamp TEXT
)

messages_fts USING fts5 (content, content=messages)

tool_calls (
  id TEXT PRIMARY KEY,
  message_id TEXT REFERENCES messages(id),
  session_id TEXT,
  tool_name TEXT,
  tool_category TEXT,
  input_summary TEXT,
  duration_ms INTEGER,
  files_touched TEXT,
  timestamp TEXT
)

costs (
  date TEXT,
  project TEXT,
  model TEXT,
  input_tokens INTEGER,
  output_tokens INTEGER,
  cache_tokens INTEGER,
  estimated_cost_usd REAL,
  PRIMARY KEY (date, project, model)
)

health_snapshots (
  id INTEGER PRIMARY KEY,
  project TEXT,
  timestamp TEXT,
  avg_complexity REAL,
  total_files INTEGER,
  total_lines INTEGER,
  test_ratio REAL,
  dependency_count INTEGER
)
```

### Web Dashboard

A Svelte frontend embedded into the Go binary via `go:embed` and served by the built-in HTTP server. Dark theme, monospace numbers, terminal-inspired aesthetic. Key views:

- **Overview**: total spend, sessions today, active projects
- **Costs**: time series chart, breakdown by project/model, most expensive sessions
- **Sessions**: searchable list, click to expand, AI-generated recaps
- **Impact**: git attribution visualization, churn tracking, per-project breakdown
- **Health**: trend lines for complexity, file sizes, test ratio


## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Go | Single binary, fast JSONL parsing, native concurrency for sync/watch/SSE |
| CLI | cobra | Standard Go CLI framework, subcommand-based |
| JSONL parsing | gjson | Zero-allocation JSON traversal, proven in agentsview |
| Database | go-sqlite3 (CGO) + FTS5 | Local, WAL mode, separate reader/writer connections |
| HTTP server | net/http (stdlib) | No framework needed, Go 1.22+ method routing |
| Frontend | Svelte | Fast, small bundle, embedded into binary via go:embed |
| Git analysis | os/exec (git CLI) | Shell out to git log, blame, diff — simple and reliable |
| Code health | tree-sitter or shell to radon | Complexity metrics, language-agnostic via tree-sitter |
| File watching | fsnotify | Cross-platform file system events, proven in agentsview |
| Distribution | Single binary | brew, GitHub releases, or just download — zero deps for the user |


## Implementation Phases

### Phase 1: Core + Cost Tracking
- JSONL parser for Claude Code sessions
- Incremental sync engine with SQLite
- Cost calculation with configurable model pricing
- CLI: `claudio sync`, `claudio costs`
- This alone is immediately useful

### Phase 2: Session Intelligence
- FTS5 full-text search across messages
- CLI: `claudio sessions`, `claudio search`
- AI-powered recap and decision extraction
- CLI: `claudio recap`, `claudio decisions`

### Phase 3: Code Impact
- Git log parsing and session-commit matching
- Attribution analysis (human vs AI-assisted)
- Churn tracking
- CLI: `claudio impact`

### Phase 4: Web Dashboard
- HTTP server exposing all data via REST
- Svelte frontend embedded via go:embed
- Cost charts, session browser, impact viz
- Live updates via SSE

### Phase 5: Codebase Health
- AST-based complexity analysis
- Trend tracking with periodic snapshots
- CLI: `claudio health`
- Dashboard integration


## Differentiation vs agentsview

| | agentsview | claudio |
|---|-----------|---------|
| Agents | 5 (Claude, Codex, Copilot, Gemini, OpenCode) | Claude Code only |
| Focus | Session viewing and search | Actionable insights (costs, impact, health) |
| Cost tracking | No | Yes — per session, project, model |
| Git integration | No | Yes — commit attribution, churn analysis |
| Code health | No | Yes — complexity trends, structural monitoring |
| Knowledge extraction | Basic AI summaries | Decision records, pattern mining |
| Language | Go | Go |
| Distribution | Single binary | Single binary (brew, GitHub releases) |

Claudio is not a competitor to agentsview — it's complementary. agentsview is the multi-agent session browser. Claudio is the Claude-specific analytics and intelligence layer.
