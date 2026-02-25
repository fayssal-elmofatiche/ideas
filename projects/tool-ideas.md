# Tool Ideas

Practical CLI and developer tools — inspired by gaps in the current AI-assisted development workflow.


## Active

### resumake
Build styled CV documents from a single YAML source. Themes, AI translation, job tailoring, ATS analysis.
- Status: published (PyPI)
- Repo: https://github.com/fayssal-elmofatiche/resumake

### konto
Personal finance terminal — bank sync via Enable Banking, spending analysis, contract detection. CLI + web UI.
- Status: planning
- Stack: Python, FastAPI, Svelte, SQLite, Enable Banking API


### claudio
Developer dashboard for Claude Code users. Combines session intelligence, cost tracking, code impact analysis, and codebase health monitoring into one tool. Name: "Claude I/O."
- Status: idea
- Features:
  - Session intelligence — search, extract knowledge, surface decisions and patterns from ~/.claude/ sessions
  - Cost awareness — token usage and cost per session, per project, over time
  - Code impact — cross git history with sessions to attribute commits, measure AI-assisted code ratio, track refactor/revert rates
  - Codebase health — lightweight complexity and structure trend tracking
- Differentiator vs agentsview: Claude-deep, focused on actionable insights rather than agent-agnostic session viewing
- Stack: Go, cobra, go-sqlite3/FTS5, gjson, fsnotify, Svelte (embedded via go:embed)
- Concept doc: projects/claudio/README.md


## Backlog

### tokenmeter
AI spending tracker across all providers. Aggregates usage from Claude, OpenAI, Gemini, Copilot — API calls, token counts, costs. Answers "how much did I spend this week on AI?" and "what's my cost per project?"
- Why: every developer using multiple AI tools has no idea what they're actually spending
- Inspiration: agentsview by Wes McKinney (observability for AI agents)

### codewatch
Architectural health monitor for codebases. Tracks complexity trends, coupling, dependency graph changes, test coverage drift over time. Flags when the codebase is degrading — whether commits come from a human or an AI. Runs in CI or on demand.
- Why: "AI amplifies both good and bad structure" (Chris Lattner). As AI-generated code scales, someone needs to watch the structural health.
- Inspiration: Lattner's CCC article, agentsview analytics

### codedelta
AI code attribution and quality tracker. Crosses git history with agent sessions to measure: what percentage of the codebase is AI-generated? Which AI-generated code gets refactored or reverted most? Bug rates by source.
- Why: teams adopting AI coding agents have no visibility into the actual impact on code quality over time
- Inspiration: agentsview session data + git blame

### sessionmind
Extracts knowledge from AI agent sessions — design decisions, debugging steps, architectural reasoning — and organizes them into searchable decision records, runbooks, or documentation drafts.
- Why: valuable context is buried in throwaway conversations that nobody revisits
- Inspiration: agentsview search + AI insights feature

### promptvault
Mines agent sessions for patterns: which prompts led to the best outputs, which approaches got reverted. Builds a personal library of effective prompts and workflows organized by task type.
- Why: developers repeat the same mistakes and rediscover the same tricks across sessions
- Inspiration: agentsview session analytics
