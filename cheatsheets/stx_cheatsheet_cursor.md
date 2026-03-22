# Cursor IDE — Complete Reference Guide (March 21, 2026)

> Official sources: [cursor.com/docs](https://cursor.com/docs) + [changelog](https://cursor.com/changelog)
> Current version: ~2.4 — Built on VS Code

---

## What is Cursor?

Cursor is an **AI-powered code editor** built on top of VS Code. Unlike a simple chatbot or a CLI tool, Cursor embeds AI directly into a full IDE: it can read your code, modify files across your project, run terminal commands, search the web, and even control a browser — all within the familiar VS Code interface. Think of it as VS Code with a senior developer sitting next to you who can see your screen, understand your codebase, and make changes on your behalf.

**Fundamental concepts to understand:**

- **Agent**: the AI assistant that works inside Cursor. It can autonomously read files, search code, execute commands, and edit multiple files to accomplish a task. It operates in different **modes** depending on what you need.
- **Context**: the information the agent has access to when answering. Cursor automatically gathers context (codebase search, linter errors, git history), but you can also explicitly attach files, folders, or documentation using **@ mentions**.
- **Tab completion**: AI-powered code suggestions that appear as grayed-out text while you type. Unlike traditional autocomplete, it can predict multi-line edits and coordinated changes across a file.
- **Rules**: instructions you write (in `.cursor/rules/` or global settings) that customize how the agent behaves — coding style, preferred libraries, project conventions.
- **MCP (Model Context Protocol)**: a standard that lets Cursor connect to external tool servers, extending the agent's capabilities (databases, APIs, cloud services, etc.).

---

## 1. Chat Modes (how the agent works)

When you open the agent panel (`Cmd+I`), you can choose how the agent operates. Each mode has a different level of autonomy.

| Mode | Description | When to use |
|------|-------------|-------------|
| **Agent** | Full autonomous mode (default). The agent reads files, searches code, runs commands, edits files, browses the web — whatever it takes to accomplish your task. | Most tasks: implement features, fix bugs, refactor code |
| **Plan** | Research-only mode. The agent investigates your codebase, asks clarifying questions, and produces a detailed step-by-step implementation plan — but does **not** make any changes. | Before complex tasks where you want to review the approach before any code is written |
| **Debug** | Systematic bug investigation. The agent adds instrumentation/logging, asks for reproduction steps, analyzes runtime data, fixes the root cause, then cleans up the debugging code. | When you have a bug but aren't sure where it comes from |
| **Ask** | Read-only mode. The agent can read and search but cannot modify anything. | When you just want to understand code without risking any changes |

**Switching modes**: use the dropdown in the Agent panel, press `Shift+Tab` to cycle, or use `/plan` and `/ask` slash commands in the CLI.

---

## 2. Keyboard Shortcuts

These are the essential shortcuts for AI features. All standard VS Code shortcuts also work.

### Agent & Chat

| Action | Mac | Windows / Linux |
|--------|-----|-----------------|
| Open Agent panel | `Cmd+I` | `Ctrl+I` |
| Toggle between modes (Plan/Agent/Debug) | `Shift+Tab` | `Shift+Tab` |
| Switch AI model | `Cmd+/` | `Ctrl+/` |
| Queue a follow-up message (while agent runs) | `Enter` | `Enter` |
| Send immediately (bypass queue) | `Cmd+Enter` | `Ctrl+Enter` |
| Open Cursor Settings | `Cmd+Shift+J` | `Ctrl+Shift+J` |
| Open MCP Logs (Output panel) | `Cmd+Shift+U` | `Ctrl+Shift+U` |

### Tab Completion

| Action | Mac | Windows / Linux |
|--------|-----|-----------------|
| Accept full suggestion | `Tab` | `Tab` |
| Reject suggestion | `Escape` | `Escape` |
| Accept word-by-word | `Cmd+→` | `Ctrl+→` |
| Jump to next edit location | `Tab` (after accepting) | `Tab` (after accepting) |

---

## 3. Slash Commands

Slash commands are typed directly in the chat input or CLI.

### In Editor Chat

| Command | Description |
|---------|-------------|
| `/create-rule` | Create a new rule file. Describe the behavior you want, and the agent generates a `.mdc` file in `.cursor/rules/` |
| `/migrate-to-skills` | Convert existing dynamic rules and slash commands into the Skills format (Cursor 2.4+) |
| `/<skill-name>` | Invoke a specific skill by name |
| `/<subagent-name> <prompt>` | Delegate a task to a specific subagent |

### In CLI

| Command | Description |
|---------|-------------|
| `/plan` | Switch to Plan Mode |
| `/ask` | Switch to Ask Mode |
| `/sandbox` | Interactive sandbox configuration menu |
| `/max-mode [on\|off]` | Toggle Max Mode (enhanced capability for supported models) |
| `/mcp enable <name>` | Enable an MCP server |
| `/mcp disable <name>` | Disable an MCP server |

---

## 4. @ Symbols (Context Providers)

@ symbols let you explicitly attach context to your prompt. Type `@` in the chat input to see the list.

### Manually Attachable

| Symbol | Description | Example |
|--------|-------------|---------|
| `@file` | Reference a specific file — its content is included in the prompt | `@auth.ts explain this file` |
| `@folder` | Include an entire directory listing (and contents for small dirs) | `@src/components/ list all components` |
| `@Code Symbols` | Target a specific function, class, or variable by name | `@getUserById what does this function return?` |
| `@Docs` | Search indexed documentation (built-in or custom) | `@Docs React hooks explain useEffect cleanup` |
| `@Past Chats` | Access context from previous conversations | `@Past Chats what did we decide about the auth refactor?` |
| `@my-rule` | Invoke a manually-applied rule by name | `@coding-standards review this code` |

### Automatic Context (no @ needed)

Since Cursor 2.0, these contexts are gathered **automatically** by the agent — you don't need to request them:

- **Web search** — the agent searches the internet when needed
- **Git history** — the agent reads commits, diffs, and blame
- **Definitions** — the agent finds symbol definitions and references
- **Linter errors** — the agent reads your editor's diagnostic output
- **Codebase search** — the agent searches across your project autonomously

---

## 5. Built-in Agent Tools

These are the tools the agent can use autonomously. You don't invoke them directly — the agent decides which tools to use based on your request. There is **no limit** on the number of tool calls per task.

| Tool | Description | When the agent uses it |
|------|-------------|----------------------|
| **Semantic Search** | Searches your codebase by meaning using vector embeddings. The index syncs every 5 minutes and becomes available at 80% completion. | When looking for code related to a concept, not an exact string |
| **Instant Grep** | Custom grep engine faster than ripgrep. Exact matches, regex, patterns. | When searching for an exact string, function name, or pattern |
| **File/Folder Search** | Searches files by name, examines directory structure | When looking for a file by name or listing directory contents |
| **File Reading** | Reads file content. Supports images (.png, .jpg, .gif, .webp, .svg) for vision-capable models. | When it needs to understand a file's content |
| **Code Editing** | Suggests and auto-applies edits to files. Changes appear in the diff view for your review. | When implementing changes to existing code |
| **Terminal Execution** | Executes shell commands in a sandboxed environment (configurable). | When it needs to run builds, tests, installs, or any shell command |
| **Browser Control** | Navigates URLs, clicks elements, fills forms, takes screenshots, monitors console/network, performs accessibility audits. | When debugging web UIs, testing endpoints, or reading web pages |
| **Web Search** | Generates search queries and retrieves results from the internet. | When it needs up-to-date information not in the codebase |
| **Image Generation** | Creates images from text descriptions or references, saved to `assets/` folder. | When you ask for diagrams, mockups, or visual assets |
| **Rules Retrieval** | Retrieves project/user/team rules based on the current context. | Automatically at the start of each session |
| **Clarification** | Asks you clarifying questions during execution. | When the task is ambiguous or requires a decision |
| **MCP Tools** | Any tools exposed by configured MCP servers (databases, APIs, etc.) | When the task requires external integrations |

---

## 6. Tab Completion (Copilot++)

Tab completion is Cursor's inline AI code prediction. It goes beyond traditional autocomplete by understanding your recent edits and intent.

**How it works:**
1. As you type, the AI analyzes your recent edits, surrounding code, and linter errors
2. A suggestion appears as **grayed-out text** at your cursor position
3. Press `Tab` to accept, `Escape` to reject, or keep typing to ignore

**Key features:**

- **Multi-line editing**: suggestions can span multiple lines, including coordinated changes (e.g., adding a parameter to a function signature and updating all call sites)
- **Jump-in-file**: after accepting a suggestion, pressing `Tab` again navigates to the **next likely edit location** — the AI predicts where you'll need to make changes next
- **Cross-file predictions**: when an edit implies changes in other files (e.g., renaming an export), a portal window appears at the bottom of the editor showing the predicted edit in the other file
- **Linter awareness**: suggestions take into account current linter errors and try to fix them

**Configuration:**
- Status indicator in the bottom-right corner: snooze, disable globally, or disable per file extension
- Custom keybinding: search `Accept Cursor Tab Suggestions` in Keyboard Shortcuts
- Full settings: `Cursor Settings > Tab`

---

## 7. Subagents

Subagents are specialized AI assistants that the main agent can delegate work to. Each subagent runs in its own context window, which keeps the main conversation clean and allows parallel work.

### Built-in Subagents

| Subagent | Description | Uses |
|----------|-------------|------|
| **Explore** | Searches and analyzes codebases. Uses a faster model for efficiency. | Understanding large codebases, finding patterns, mapping dependencies |
| **Bash** | Executes shell commands, isolates verbose terminal output from the main context. | Running builds, tests, or any command with long output |
| **Browser** | Controls a browser via MCP tools. Navigates pages, clicks, fills forms, takes screenshots. | Testing web UIs, debugging frontend, scraping documentation |

### Execution Modes

| Mode | Behavior | When to use |
|------|----------|-------------|
| **Foreground** | Main agent waits for the subagent to finish before continuing | When the result is needed before the next step |
| **Background** | Subagent runs independently, main agent continues working | For independent tasks that can run in parallel |

### Custom Subagents

You can create your own subagents as markdown files with YAML frontmatter:

**Locations:**
- `.cursor/agents/` — project-level (version-controlled)
- `~/.cursor/agents/` — global (personal)
- Also supported: `.claude/agents/`, `.codex/agents/`

**Important rules:**
- Subagents **cannot launch other subagents** (single level only)
- They inherit all parent tools including MCP
- They consume tokens independently
- Background subagent output goes to `~/.cursor/subagents/`

---

## 8. Skills

Skills are portable, version-controlled packages that teach the agent domain-specific tasks. Think of them as "recipes" the agent can follow for specific workflows.

**Discovery locations:**
- `.agents/skills/`, `.cursor/skills/` — project-level
- `~/.cursor/skills/` — global
- Legacy: `.claude/skills/`, `.codex/skills/`

**Structure:**
```
skill-name/
  SKILL.md          # Required — YAML frontmatter + instructions
  scripts/          # Executable code the skill can run
  references/       # Supplementary documentation
  assets/           # Templates, images, configs
```

**Invocation:** type `/` in the Agent chat to see available skills, or the agent auto-selects based on context.

---

## 9. Rules System

Rules customize how the agent behaves for your project. They replace the older `.cursorrules` file.

### Rule Types

| Type | Location | Scope | Version-controlled |
|------|----------|-------|--------------------|
| **Project Rules** | `.cursor/rules/*.md` or `*.mdc` | This project only | Yes |
| **User Rules** | Cursor Settings > Rules | All your projects | No |
| **Team Rules** | Cursor Dashboard (Teams/Enterprise plans) | All team members | Admin-managed |
| **AGENTS.md** | Project root or subdirectories | Simple alternative to `.mdc` files | Yes |

### Application Modes

Each rule has a mode that controls when it's applied (set in frontmatter):

| Mode | Behavior |
|------|----------|
| `Always Apply` | Active in every chat session — use for universal conventions |
| `Apply Intelligently` | Agent decides based on the rule's description — use for context-dependent rules |
| `Apply to Specific Files` | Triggered by glob patterns (e.g., `globs: ["**/*.ts"]`) — use for language/framework-specific rules |
| `Apply Manually` | Only active when you invoke it with `@my-rule` — use for optional/situational rules |

### Rule File Format (.mdc)

```markdown
---
description: "Brief purpose of this rule"
alwaysApply: false
globs: ["**/*.ts", "**/*.tsx"]
---

Your instructions here. Use concrete examples.
Keep under 500 lines. Split large rules into multiple files.
Use @filename to reference other files.
```

### Priority Order

Team Rules > Project Rules > User Rules

### Remote Rules

You can import rules from GitHub repositories. They auto-sync with the source.

### Limitations

- User Rules don't apply to Inline Edit (`Cmd+K` / `Ctrl+K`)
- Rules don't affect Tab completion (only Agent and Chat)

---

## 10. MCP (Model Context Protocol)

MCP lets you connect external tool servers to Cursor, extending what the agent can do. For example, you can connect a database MCP server so the agent can query your database, or a cloud provider MCP so it can deploy code.

### Transports Supported

| Transport | Description | Use case |
|-----------|-------------|----------|
| `stdio` | Local execution, single user | Local tools (file-based, scripts) |
| `SSE` | Server-Sent Events endpoints | Remote servers, shared tools |
| `Streamable HTTP` | HTTP endpoints | Remote servers, cloud services |

### Protocol Features

Tools, Prompts, Resources, Roots, Elicitation, Apps extension.

### Configuration

| Scope | Location |
|-------|----------|
| Project | `.cursor/mcp.json` |
| Global | `~/.cursor/mcp.json` |

### Interpolation Variables

Use these in your config to keep paths portable:

| Variable | Resolves to |
|----------|-------------|
| `${env:NAME}` | Environment variable value |
| `${userHome}` | User's home directory |
| `${workspaceFolder}` | Current workspace root |
| `${workspaceFolderBasename}` | Workspace folder name |
| `${pathSeparator}` | OS path separator |

### Static OAuth

Supported with CLIENT_ID, CLIENT_SECRET, scopes. Redirect URL: `cursor://anysphere.cursor-mcp/oauth/callback`

### Debugging

Output panel (`Cmd+Shift+U`) > select "MCP Logs"

### CLI Commands

| Command | Description |
|---------|-------------|
| `agent mcp list` | List all configured MCP servers |
| `agent mcp list-tools <id>` | View tools exposed by a server |
| `agent mcp login <id>` | Authenticate with a server |
| `agent mcp enable <id>` | Enable a server |
| `agent mcp disable <id>` | Disable a server |

---

## 11. Terminal Integration & Sandbox

When the agent runs terminal commands, it does so in a **sandboxed environment** by default. This protects your system from unintended side effects.

### Default Sandbox Permissions

| Permission | Level |
|------------|-------|
| Filesystem read | Allowed |
| Workspace write | Allowed |
| Temp directory | Full access |
| Network | Blocked by default |
| `.cursor` directory | Protected |

### Platform Requirements

| Platform | Requirement |
|----------|-------------|
| macOS | Cursor v2.0+ (works out of box) |
| Windows | WSL2 required |
| Linux | Kernel 6.2+ with Landlock v3 |

### Auto-Run Modes

Configure in `Cursor Settings > Agents > Auto-Run`:

| Mode | Behavior |
|------|----------|
| **Run in Sandbox** (default) | Commands run in sandbox, no approval needed |
| **Ask Every Time** | Every command requires manual approval |
| **Run Everything** | No sandbox, no approval — use with caution |

### Network Access Options

| Option | What's allowed |
|--------|----------------|
| sandbox.json Only | Only explicitly listed domains |
| sandbox.json + Defaults | Listed domains + package managers + cloud providers |
| Allow All | No network restrictions |

### Sandbox Configuration

User-level: `~/.cursor/sandbox.json`
Project-level: `<workspace>/.cursor/sandbox.json`

### Environment Variable

`CURSOR_AGENT` is set when running inside an agent session — useful for disabling heavy shell themes (like Powerlevel10k) that slow down agent commands.

---

## 12. Hooks

Hooks are processes that observe, control, and extend the agent loop. They fire on specific events and can block or modify agent behavior.

### Agent Hook Events

| Event | When it fires |
|-------|---------------|
| `sessionStart` | Agent session begins |
| `sessionEnd` | Agent session ends |
| `preToolUse` | Before a tool is called |
| `postToolUse` | After a tool returns |
| `postToolUseFailure` | After a tool call fails |
| `subagentStart` | Before a subagent is launched |
| `subagentStop` | After a subagent finishes |
| `beforeShellExecution` | Before a terminal command runs |
| `afterShellExecution` | After a terminal command completes |
| `beforeMCPExecution` | Before an MCP tool is called |
| `afterMCPExecution` | After an MCP tool returns |
| `beforeReadFile` | Before a file is read |
| `afterFileEdit` | After a file is edited |
| `beforeSubmitPrompt` | Before the prompt is sent to the model |
| `preCompact` | Before context compaction |
| `stop` | Agent is stopped by user |
| `afterAgentResponse` | After the agent produces a response |
| `afterAgentThought` | After the agent's internal reasoning step |

### Tab Hook Events

| Event | When it fires |
|-------|---------------|
| `beforeTabFileRead` | Before Tab reads a file for predictions |
| `afterTabFileEdit` | After Tab applies an edit |

### Configuration (priority order)

Enterprise (MDM) > Team (cloud) > Project (`.cursor/hooks.json`) > User (`~/.cursor/hooks.json`)

### Execution Types

| Type | How it works |
|------|-------------|
| **Command-based** | Shell script receives JSON on stdin, returns JSON on stdout. Exit 0 = success, exit 2 = block the action. |
| **Prompt-based** | An LLM evaluates conditions and decides whether to allow/block. |

---

## 13. Cloud Agents (Background Agents)

Cloud agents run on **isolated Ubuntu VMs** in the cloud. They have a full desktop environment with mouse/keyboard control. This is useful for tasks that take a long time or need a complete development environment.

### Setup Methods

1. **Agent-driven** (recommended): visit `cursor.com/onboard` and let the agent configure your environment
2. **Manual**: create a Dockerfile via `.cursor/environment.json`

### Capabilities

- Full development workflow: start servers, browse web, run tests
- Screenshot and video artifact generation
- MCP tool integration
- CI failure auto-fixing (GitHub Actions, Teams plan only)
- Docker and Tailscale support

### Triggering from GitHub

Comment `@cursor [your prompt]` on any PR or issue to spawn a cloud agent.

### API Endpoints

For programmatic access to cloud agents:

| Endpoint | Description |
|----------|-------------|
| `GET /v0/agents` | List all agents |
| `POST /v0/agents` | Launch a new agent |
| `GET /v0/agents/{id}` | Get agent status |
| `GET /v0/agents/{id}/conversation` | Get conversation history |
| `GET /v0/agents/{id}/artifacts` | Get generated artifacts |
| `POST /v0/agents/{id}/followup` | Send a follow-up instruction |
| `POST /v0/agents/{id}/stop` | Stop a running agent |
| `DELETE /v0/agents/{id}` | Delete an agent |
| `GET /v0/models` | List available models |
| `GET /v0/repositories` | List connected GitHub repos |

### Secrets Management

Managed via Cursor Settings > Secrets tab. Encrypted at rest with KMS.

---

## 14. Automations

Automations are event-driven cloud agents that trigger automatically based on external events.

### Trigger Types

| Source | Events |
|--------|--------|
| **Scheduled** | Cron expressions (e.g., every day at 9am) |
| **GitHub** | PR created, commits pushed, PR merged, PR comments, CI completion |
| **Slack** | Messages in channels, channel creation |
| **Webhook** | Private HTTP endpoints you define |
| **Linear** | Issue and cycle events |
| **PagerDuty** | Incident triggers |

### Available Tools for Automations

Open PR, Comment on PR, Request reviewers, Send to Slack, Read Slack channels, MCP servers, Memories (persistent notes across runs).

---

## 15. BugBot (Automated Code Review)

BugBot automatically analyzes PR diffs for bugs, security issues, and code quality problems.

**Key features:**
- Auto-reviews on every PR update, or manual trigger via `cursor review` / `bugbot run` comment
- "Fix in Cursor" links for one-click fixes in the IDE
- Custom review rules via `.cursor/BUGBOT.md`
- Autofix: spawns Cloud Agents to automatically fix detected issues

**Platform support:** GitHub.com, GitLab.com, GitHub Enterprise Server (v3.8+), GitLab Self-Hosted

---

## 16. Plugins

Plugins are bundles of rules, skills, agents, commands, MCP servers, and hooks — packaged for sharing.

**Sources:**
- Official plugins: Cursor Marketplace (manually reviewed)
- Community plugins: cursor.directory

**Structure:**
- Manifest: `.cursor-plugin/plugin.json`
- Local testing: `~/.cursor/plugins/local/`
- Team/Enterprise: private team marketplaces

**Limitation:** CLI does not yet support plugins (MCP servers from plugins work in Cloud Agents).

---

## 17. Checkpoints

Cursor automatically takes **snapshots** of your codebase state before significant agent changes. Checkpoints exist separately from Git.

**When to use:** if the agent makes unwanted changes, open the checkpoints panel to preview and restore any previous state — no need to `git stash` or undo manually.

---

## 18. Context Management

### Explicit Context (you control)

| Method | What it does |
|--------|-------------|
| `@file` / `@folder` | Attach specific files or directories |
| `@Code Symbols` | Reference a function, class, or variable |
| `@Docs` | Search indexed documentation |
| `@Past Chats` | Pull context from previous conversations |
| Image drag-and-drop | Paste or drag images into chat (screenshots, mockups, diagrams) |
| Voice input | Microphone icon for natural language dictation |

### Automatic Context (agent gathers)

The agent autonomously searches your codebase, reads git history, finds definitions, checks linter errors, and searches the web — all without explicit @ mentions.

### Semantic Search

Your code is broken into chunks, converted to vector embeddings, and indexed automatically. The index syncs every 5 minutes and becomes available at 80% completion. Code is never stored in plaintext; embeddings are created without storing source code.

### Excluding Files

- `.gitignore` — respected for indexing
- `.cursorignore` — blocks agent access to specified files/directories

---

## 19. Available AI Models

Switch models at any time with `Cmd+/` (Mac) / `Ctrl+/` (Win/Linux).

### Claude (Anthropic)

| Model | Notes |
|-------|-------|
| Claude 4.6 Sonnet | Latest, fast |
| Claude 4.5 Sonnet | Balanced |
| Claude 4.5 Haiku | Fast, lightweight |
| Claude 4 Sonnet | Older generation |
| Claude Opus | Most capable (variants) |

### GPT (OpenAI)

| Model | Notes |
|-------|-------|
| GPT-5 | Latest flagship |
| GPT 5.1–5.4 Codex | Code-specialized variants |
| GPT Mini | Lightweight |
| GPT Nano | Fastest, smallest |

### Gemini (Google)

| Model | Notes |
|-------|-------|
| Gemini 3.1 Pro | Latest |
| Gemini 3.0 Pro | Previous generation |
| Gemini 2.5 Flash | Fast |
| Gemini Flash | Lightweight |

### Cursor Models

| Model | Notes |
|-------|-------|
| Cursor Composer 1, 1.5, 2 | Cursor's own models |

### Others

| Model | Notes |
|-------|-------|
| Grok 4.20 | xAI |
| Kimi K2.5 | Moonshot AI |

---

## 20. CLI Commands

### Installation

| Platform | Command |
|----------|---------|
| Mac / Linux | `curl https://cursor.com/install -fsS \| bash` |
| Windows | `irm 'https://cursor.com/install?win32=true' \| iex` |

### Primary Commands

| Command | Description |
|---------|-------------|
| `agent` | Start interactive session |
| `agent "prompt"` | Start with an initial instruction |
| `agent -p "prompt"` | Non-interactive mode (pipe-friendly, returns result and exits) |
| `agent ls` | List previous conversations |
| `agent resume` | Continue the most recent conversation |
| `agent --continue` | Persist context across interactions |
| `agent --resume="chat-id"` | Resume a specific conversation by ID |
| `agent --model "model"` | Specify which AI model to use |
| `agent --output-format text` | Set output format |
| `agent -c "prompt"` | Start a cloud agent session |
| `& message` | Push a mid-conversation task to the cloud |

### CLI Flags

| Flag | Description |
|------|-------------|
| `--mode=plan\|ask\|agent` | Set the operating mode |
| `--sandbox enabled\|disabled` | Toggle sandbox for terminal commands |
| `--approve-mcps` | Auto-approve MCP tool calls |

### Shell Mode

Executes shell commands inline within the CLI. 30-second timeout per command. Exit with `Escape`, `Backspace`, or `Ctrl+C`.

---

## 21. Privacy and Security

### Agent Security Defaults

| Action | Approval required? |
|--------|-------------------|
| Reading files | No |
| Searching code | No |
| Editing workspace files | No |
| Sensitive data exposure | Yes |
| Config file changes | Yes |
| Terminal commands | Depends on Auto-Run setting |
| MCP tool calls | Yes (by default) |

### File Protection

- `.cursorignore` blocks agent access to specified files (like `.gitignore` but for the AI)
- `.cursor` directory is protected in sandbox mode

### Network Defaults

Network requests limited to GitHub, direct links, and web search providers. No arbitrary network requests unless explicitly allowed.

### Important Warnings

- **Workspace Trust**: disabled by default. When enabled, restricted mode disables all AI features.
- **Auto-reload**: agent file changes might execute before you review them if auto-reload is enabled in your VS Code settings.
- **Allowlist caveat**: "Not a security guarantee. The allowlist is best-effort — bypasses are possible."

### Security Reports

security-reports@cursor.com

---

## 22. Queued Messages

While the agent is working, you can type and press `Enter` to **queue** follow-up instructions. The agent will process them in order after finishing the current task.

- Drag queued messages to **reorder** them
- `Cmd+Enter` sends a message **immediately**, bypassing the queue

---

## 23. Pricing

| Plan | Price | Key Features |
|------|-------|-------------|
| **Hobby** | Free | Limited agent requests & tab completions |
| **Pro** | $20/mo | Extended limits, frontier models, MCPs, skills, hooks, cloud agents |
| **Pro+** | $60/mo | 3× usage on all models |
| **Ultra** | $200/mo | 20× usage, priority feature access |
| **Teams** | $40/user/mo | Shared rules/commands, analytics, SSO, RBAC |
| **Enterprise** | Custom | Pooled usage, SCIM, audit logs, granular admin controls |

---

## 24. Integrations

| Service | Capabilities |
|---------|-------------|
| **GitHub** | Clone repos, push changes, create PRs, `@cursor` comments on PRs/issues |
| **GitLab** | BugBot reviews, self-hosted support |
| **Slack** | Automation triggers, send/read channel messages |
| **Linear** | Issue and cycle event triggers |
| **PagerDuty** | Incident triggers for automations |
| **JetBrains** | IDE integration available |
| **AWS Bedrock** | Model integration |

---

## 25. Miscellaneous Features

| Feature | Description |
|---------|-------------|
| **Max Mode** | Enhanced capability mode for supported models. Toggle with `/max-mode on` in CLI. |
| **Deeplinks** | URL-based links to Cursor features (for sharing/bookmarking) |
| **VS Code Compatibility** | Full compatibility with VS Code extensions, themes, keybindings, and settings |
| **Sudo Handling** | CLI displays secure masked password prompt without exposing credentials to the AI |
| **Cursor Blame** | Attribution feature for AI-generated code |
| **Supported Locales** | en-US, zh-CN, zh-TW, ja, es, fr, pt-BR, ko, ru, tr, id, de |

---

## Version History (key milestones)

| Version | Notable changes |
|---------|----------------|
| 2.4 | Skills system, `/migrate-to-skills`, expanded MCP protocol features |
| 2.0 | Agent mode as default, automatic context gathering (removed @Web, @Git, @Definitions, @Codebase, @Problems), sandbox terminal, hooks system |
| 1.x | Composer (multi-file editing), Tab completion, Chat sidebar, `.cursorrules` file |
| 0.x | Initial release, VS Code fork, basic AI chat integration |

---

*Document generated on March 21, 2026 — Sources: [cursor.com/docs](https://cursor.com/docs), [cursor.com/changelog](https://cursor.com/changelog)*
