# Claude Code — Complete Reference Guide (March 21, 2026)

> Official sources: [code.claude.com/docs](https://code.claude.com/docs/en/cli-reference) + [CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
> Current version: ~2.1.81 — Models Claude 4.5/4.6

---

## What is Claude Code?

Claude Code is an **AI command-line assistant** (CLI) that works directly in your terminal. Unlike ChatGPT or Claude.ai in a browser, Claude Code has access to your file system: it can read your code, modify it, execute shell commands, and interact with git. It's like having a senior developer looking at your screen who can type on your behalf, but who asks your permission before any potentially risky action.

**Fundamental concepts to understand:**

- **Session**: a conversation with Claude Code. Each session has a history, an ID, and can be resumed later. It's the equivalent of a discussion thread.
- **Context (context window)**: the amount of text Claude can "keep in mind" simultaneously. When the conversation becomes too long, Claude Code **compacts** it (summarizes older exchanges to free up space).
- **Interactive mode vs print mode**: in interactive mode (`claude`), you discuss with Claude turn by turn. In print mode (`claude -p`), Claude responds once and returns control — useful for integration in scripts.
- **Permission**: before each potentially destructive action (writing a file, executing a command), Claude asks for your approval. Several permission modes allow adjusting this level of control.

---

## 1. CLI Commands (launching)

These are the commands you type in your terminal to start or resume a session.

| Command | Description | Example |
|---|---|---|
| `claude` | Start an interactive session — Claude waits for your instructions | `claude` |
| `claude "query"` | Start with a first question already asked | `claude "explain this project"` |
| `claude -p "query"` | **Print mode**: Claude responds and exits immediately. Useful in CI/CD scripts or pipelines | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Send a file's content to Claude via a Unix pipe | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | **Resume the last conversation** in the current directory. Handy when you accidentally close the terminal | `claude -c` |
| `claude -c -p "query"` | Continue the last conversation in print mode (for scripts) | `claude -c -p "Check for type errors"` |
| `claude -r "<session>" "query"` | Resume a specific session by its ID or name. Each session is saved and can be retrieved | `claude -r "auth-refactor" "Finish this PR"` |
| `claude update` | Update Claude Code to the latest version | `claude update` |
| `claude auth login` | Sign in to your Anthropic account. `--console` for API billing, `--sso` for enterprise SSO | `claude auth login --console` |
| `claude auth logout` | Sign out | `claude auth logout` |
| `claude auth status` | Check if you're logged in and with what type of account. `--text` for a human-readable format | `claude auth status` |
| `claude agents` | List all available subagents (built-in + custom), grouped by source | `claude agents` |
| `claude mcp` | Configure MCP servers (see MCP section below) | `claude mcp` |
| `claude remote-control` | Start in **Remote Control** mode: your terminal becomes a server you can control from claude.ai or the mobile app. Useful when you want to launch work from your phone on your development machine | `claude remote-control --name "My Project"` |

---

## 2. CLI Flags

Flags are added after `claude` to modify session behavior. Most common first, most specialized last.

### Essential flags (daily use)

| Flag | When to use | Example |
|---|---|---|
| `--model` | Choose a different model. `opus` is the most capable but slower/more expensive, `sonnet` is the best quality/speed ratio, `haiku` is the fastest | `claude --model opus` |
| `--continue`, `-c` | Resume the last conversation | `claude -c` |
| `--resume`, `-r` | Resume a conversation by name or ID | `claude -r "my-feature"` |
| `--print`, `-p` | Single response without interaction. For scripts and automation | `claude -p "list all TODO comments"` |
| `--name`, `-n` | Give the session a name to find it easily later | `claude -n "auth-refactor"` |
| `--add-dir` | Give access to other directories in addition to the current directory. Useful in a monorepo | `claude --add-dir ../shared-lib` |
| `--effort` | Control Claude's depth of reasoning. `low` = fast and superficial, `high` = thoughtful and thorough, `max` = Opus 4.6 only, maximum reasoning | `claude --effort high` |
| `--verbose` | Display details of each tool used. Useful for understanding what Claude is doing | `claude --verbose` |

### Behavior customization flags

| Flag | When to use | Example |
|---|---|---|
| `--agent` | Start the entire session in "custom agent" mode. The system prompt is replaced by the agent's (see Subagents section) | `claude --agent code-reviewer` |
| `--agents` | Create agents on the fly via JSON, without creating a file. For quick prototyping | `claude --agents '{"reviewer":{"description":"...","prompt":"..."}}'` |
| `--append-system-prompt` | Add extra instructions to Claude without replacing its default behavior. For example, forcing a language or code style | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | Same but from a file. Handy for long guidelines | `claude --append-system-prompt-file ./style-rules.txt` |
| `--system-prompt` | **Completely replace** the system prompt. Warning: you lose Claude Code's default behaviors (tool usage, etc.). For advanced use cases | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | Same from a file | `claude --system-prompt-file ./custom-prompt.txt` |

### Tool and permission control flags

| Flag | When to use | Example |
|---|---|---|
| `--tools` | Restrict which tools Claude can use. `""` = none, `"Bash,Read"` = only Bash and Read | `claude --tools "Bash,Edit,Read"` |
| `--allowedTools` | Tools Claude can use **without asking** for permission. Avoids popups for routine commands | `claude --allowedTools "Bash(git log *)" "Read"` |
| `--disallowedTools` | Completely forbidden tools. Claude doesn't even see them | `claude --disallowedTools "Write"` |
| `--permission-mode` | Choose a global permission mode (see Permission Modes section) | `claude --permission-mode plan` |
| `--dangerously-skip-permissions` | **Skip all permission prompts.** Claude can do everything without asking. Only use in disposable environments (CI, containers) | `claude --dangerously-skip-permissions` |

### Print mode / automation flags

These flags only work with `-p` (print mode). They serve to integrate Claude Code into scripts, CI/CD pipelines, or the Agent SDK.

| Flag | When to use | Example |
|---|---|---|
| `--output-format` | Output format. `json` for programmatic parsing, `stream-json` for event-by-event streaming | `claude -p --output-format json "query"` |
| `--input-format` | Input format. `stream-json` allows sending structured messages | `claude -p --input-format stream-json` |
| `--json-schema` | Force output to match a precise JSON schema. Claude does its work then formats the result according to your schema | `claude -p --json-schema '{"type":"object",...}'` |
| `--max-turns` | Limit the number of "turns" (successive actions) before stopping. Prevents Claude from looping indefinitely | `claude -p --max-turns 3 "query"` |
| `--max-budget-usd` | Cap API spending for this execution | `claude -p --max-budget-usd 5.00 "query"` |
| `--fallback-model` | If the primary model is overloaded, use this fallback model | `claude -p --fallback-model sonnet "query"` |
| `--no-session-persistence` | Don't save the session to disk. For ephemeral executions | `claude -p --no-session-persistence "query"` |

### Advanced / specialized flags

| Flag | When to use | Example |
|---|---|---|
| `--worktree`, `-w` | Start in an **isolated git worktree**: an independent copy of your repo in a subdirectory. Claude can make changes there without touching your main branch. Like a git sandbox | `claude -w feature-auth` |
| `--remote` | Create a **web session on claude.ai** with a task description. Claude works on a remote environment in the cloud | `claude --remote "Fix the login bug"` |
| `--remote-control`, `--rc` | Start a local interactive session that is **also controllable remotely** from claude.ai or the mobile app. You can work in the terminal AND from your phone simultaneously | `claude --rc "My Project"` |
| `--teleport` | Bring back a web session (started with `--remote`) into your local terminal to continue work locally | `claude --teleport` |
| `--chrome` / `--no-chrome` | Enable/disable Chrome browser control. When enabled, Claude can navigate the web, click, fill forms — useful for end-to-end testing | `claude --chrome` |
| `--teammate-mode` | Configure the display of **Agent Teams** (multiple Claudes working in parallel). `tmux` = each in its own terminal pane, `in-process` = in the same terminal | `claude --teammate-mode tmux` |
| `--ide` | Connect Claude Code to your IDE (VS Code, JetBrains) automatically on startup | `claude --ide` |
| `--from-pr` | Resume sessions linked to a specific GitHub Pull Request. Claude retrieves the work context for this PR | `claude --from-pr 123` |
| `--fork-session` | When resuming a session, create a **copy** instead of continuing in the original. Like a conversation "branch" | `claude --resume abc --fork-session` |
| `--mcp-config` | Load MCP servers from a JSON file (see MCP section) | `claude --mcp-config ./mcp.json` |
| `--strict-mcp-config` | Ignore all MCP servers except those from `--mcp-config`. For total control | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--plugin-dir` | Load plugins from a local directory (for plugin development) | `claude --plugin-dir ./my-plugins` |
| `--debug` | Debug mode. Filter by category: `"api,hooks"` to see only API and hooks logs | `claude --debug "api,mcp"` |
| `--bare` | Minimal scripted mode: no hooks, no LSP, no plugin sync. For the lightest integrations | `claude --bare` |
| `--init` / `--init-only` | Run initialization hooks. `--init-only` exits after init | `claude --init` |
| `--maintenance` | Run maintenance hooks and exit | `claude --maintenance` |
| `--setting-sources` | Choose which settings sources to load among `user`, `project`, `local` | `claude --setting-sources user,project` |
| `--settings` | Load an additional settings file | `claude --settings ./settings.json` |
| `--session-id` | Use a specific UUID (for programmatic integrations) | `claude --session-id "550e..."` |
| `--betas` | Enable beta features on the API side (API key users only) | `claude --betas interleaved-thinking` |
| `--channels` | Listen to MCP channel server notifications (preview feature) | `claude --channels plugin:notifier@marketplace` |
| `--include-partial-messages` | Include partial streaming events (for real-time UIs) | `claude -p --output-format stream-json --include-partial-messages` |
| `--allow-dangerously-skip-permissions` | Enable permission bypass as an option combinable with `--permission-mode` | `claude --permission-mode plan --allow-dangerously-skip-permissions` |

---

## 3. Built-in Commands (slash commands)

Commands are used **during an interactive session** by typing `/` followed by the name. Type `/` alone to see the full list, or `/` followed by letters to filter.

### Session management

| Command | When to use |
|---|---|
| `/clear` | Start fresh: clears conversation history. Your previous session is saved and can be resumed. Aliases: `/reset`, `/new` |
| `/compact [instructions]` | When context is almost full. Claude summarizes the conversation to free up space. You can give instructions: `/compact focus on the database changes` to guide the summary |
| `/resume [session]` | Resume a previous conversation. Without argument, displays an interactive picker. Alias: `/continue` |
| `/rename [name]` | Give a name to the current session. Without argument, Claude auto-generates one from the conversation content |
| `/branch [name]` | Create a **conversation branch**: a snapshot from which you can explore an alternative direction without losing the original. Alias: `/fork` |
| `/rewind` | **Rewind** the conversation AND the code to a previous point. Claude made a mistake? `/rewind` restores the previous state. Alias: `/checkpoint` |
| `/export [filename]` | Save the conversation as plain text (to share, document, etc.) |
| `/exit` | Quit. Alias: `/quit` |

### Information and diagnostics

| Command | When to use |
|---|---|
| `/help` | Display help and available commands |
| `/context` | Visualize how much context is used as a colored grid. Indicates if tools or files consume too much space and suggests optimizations |
| `/cost` | See how many tokens have been used and the estimated cost |
| `/usage` | See your plan limits and whether you're approaching a rate limit |
| `/stats` | Personal dashboard: daily usage, session history, usage streaks |
| `/status` | System info: version, active model, connected account, connectivity |
| `/diff` | **Interactive diff viewer**: see uncommitted changes and modifications made by Claude turn by turn. Left/right arrows to navigate between views |
| `/doctor` | Diagnose and verify your Claude Code installation (version, connection, configuration) |
| `/release-notes` | View the changelog of recent versions |
| `/insights` | Analysis report of your sessions: which modules you work on most, your interaction patterns, your friction points |

### Configuration

| Command | When to use |
|---|---|
| `/config` | Open the settings interface: theme, model, output style, etc. Alias: `/settings` |
| `/model [model]` | Change the AI model mid-session. Left/right arrows to adjust the effort level |
| `/effort [level]` | Adjust reasoning depth: `low` (fast, superficial), `medium` (default), `high` (thorough), `max` (Opus only, maximum reasoning), `auto` (reset to default) |
| `/fast [on\|off]` | **Fast mode**: same Opus 4.6 model but with accelerated output. Does NOT change the model |
| `/theme` | Change the visual theme (light, dark, colorblind, ANSI) |
| `/color [color]` | Change the prompt bar color (red, blue, green, yellow, purple, orange, pink, cyan) |
| `/permissions` | View and modify permission rules (which tools require approval). Alias: `/allowed-tools` |
| `/plan` | Enter **plan mode**: Claude explores and analyzes your code without modifying it. It proposes an action plan that you validate before any modification |
| `/sandbox` | Enable/disable **sandbox mode**: command isolation to prevent destructive actions |
| `/vim` | Switch to Vim editing mode (Vim-style navigation and editing in the input area) |
| `/keybindings` | Customize keyboard shortcuts |
| `/terminal-setup` | Configure terminal-specific shortcuts (Shift+Enter, etc.). Required for certain terminals like VS Code or Alacritty |
| `/statusline` | Configure the **status line** displayed in your shell prompt. Shows info like the active model, cost, rate limits directly in your terminal |

### Work tools

| Command | When to use |
|---|---|
| `/copy [N]` | Copy Claude's last response to clipboard. `/copy 2` copies the second-to-last. When code blocks are present, an interactive picker lets you choose which block to copy |
| `/pr-comments [PR]` | Retrieve and display comments from a GitHub Pull Request. Automatically detects the PR for the current branch |
| `/security-review` | Analyze current changes to detect security vulnerabilities (injection, auth, data exposure) |
| `/btw <question>` | **Quick "by the way" question**: ask a question without polluting conversation history. The answer appears in a temporary overlay. Claude sees all context but cannot use tools. Works even while Claude is working |
| `/add-dir <path>` | Give access to an additional directory mid-session |

### Memory and project

| Command | When to use |
|---|---|
| `/init` | Initialize the project by creating a `CLAUDE.md` file. This file contains persistent instructions that Claude will read at the beginning of each session (code conventions, architecture, build commands, etc.) |
| `/memory` | Manage `CLAUDE.md` memory files and **auto-memory** (Claude automatically saves useful context between sessions) |

### External integrations

| Command | When to use |
|---|---|
| `/mcp` | Manage connections to **MCP** servers (see dedicated section) |
| `/chrome` | Configure Chrome integration for web automation |
| `/ide` | Manage IDE integrations (VS Code, JetBrains) |
| `/desktop` | Continue the session in the Claude Code desktop application. macOS and Windows only. Alias: `/app` |
| `/remote-control` | Make the session controllable remotely from claude.ai or the mobile app. Alias: `/rc` |
| `/remote-env` | Configure the default remote environment for `--remote` sessions |
| `/install-github-app` | Install the GitHub Actions integration to use Claude Code in your CI/CD |
| `/install-slack-app` | Install the Claude app in Slack |
| `/mobile` | QR code to download the mobile app. Aliases: `/ios`, `/android` |

### Plugins and skills

| Command | When to use |
|---|---|
| `/plugin` | Install, uninstall, and manage Claude Code plugins |
| `/reload-plugins` | Reload all active plugins to apply changes without restarting |
| `/skills` | List all available skills (built-in + custom) |
| `/agents` | Manage subagents: create, edit, delete, see which are active |

### Task management

| Command | When to use |
|---|---|
| `/tasks` | View and manage background tasks. Claude automatically creates a task list for complex work |

### Account and subscription

| Command | When to use |
|---|---|
| `/login` / `/logout` | Sign in/out of your Anthropic account |
| `/upgrade` | Switch to a higher plan (Pro, Max) |
| `/extra-usage` | Configure extra usage to keep working when rate limits are hit |
| `/privacy-settings` | Privacy settings (Pro and Max only) |
| `/passes` | Share a free week of Claude Code with a friend (if eligible) |
| `/feedback` | Report a bug or send feedback. Alias: `/bug` |
| `/stickers` | Order Claude Code stickers |
| `/voice` | Enable push-to-talk voice dictation (hold Space to speak) |

---

## 4. Bundled Skills (built-in skills)

**Bundled skills** are predefined workflows shipped with Claude Code. Unlike built-in commands (which execute fixed logic), skills are **playbooks** that Claude interprets and adapts to your codebase. They can spawn agents in parallel, read files, and adapt to context.

| Skill | When to use | Example |
|---|---|---|
| `/batch <instruction>` | You need to apply the **same type of change across the entire codebase** (migrate a framework, rename an API, etc.). Claude analyzes the repo, breaks the work into 5-30 independent units, and launches one agent per unit in an isolated git worktree. Each agent implements, tests, and creates a PR. Requires a git repository | `/batch migrate src/ from Solid to React` |
| `/claude-api` | You're developing an application that uses the **Claude API** or the Anthropic SDK. Loads the reference documentation for your language (Python, TypeScript, Java, Go, etc.). Also activates automatically if your code imports `anthropic` or `@anthropic-ai/sdk` | `/claude-api` |
| `/debug [description]` | Something is wrong with your **Claude Code session itself** (unexpected behavior, failing tool, etc.). Claude reads the session debug log and diagnoses the problem | `/debug the edit tool keeps failing` |
| `/loop [interval] <prompt>` | You want an action to **repeat automatically** at regular intervals as long as the session is open. Useful for monitoring a deployment, checking a CI pipeline status, or periodically rerunning another skill | `/loop 5m check if the deploy finished` |
| `/simplify [focus]` | After writing code, request a **quality review**. Launches 3 agents in parallel that look for duplicated code, quality issues, and inefficiencies, then apply corrections. Optionally, focus the analysis: `/simplify focus on memory efficiency` | `/simplify` |

---

## 5. Internal Tools

Tools are Claude Code's **capabilities** — what it can concretely do. When Claude decides to read a file, it uses the `Read` tool. When it modifies code, it uses `Edit`. You don't invoke tools directly; Claude chooses them based on what you ask. But understanding the available tools helps you configure permissions and restrictions.

**Permission = Yes** means Claude will ask for your approval before using that tool (unless configured otherwise).

### File tools

| Tool | What it does | Permission |
|---|---|---|
| `Read` | Read a file's content (code, images, PDF, Jupyter notebooks) | No |
| `Edit` | Modify a specific part of an existing file (targeted text replacement) | Yes |
| `Write` | Create a new file or completely overwrite an existing file | Yes |
| `Glob` | Find files by pattern (e.g.: `**/*.ts` = all TypeScript files) | No |
| `Grep` | Search for text or regex in project file contents | No |
| `NotebookEdit` | Modify Jupyter notebook cells (.ipynb) | Yes |

### Execution tools

| Tool | What it does | Permission |
|---|---|---|
| `Bash` | Execute a shell command in your terminal. Each command runs in a separate process. The working directory persists between commands, but environment variables do not | Yes |
| `LSP` | **Language Server Protocol**: real-time code intelligence. Detects type errors after each modification, allows navigating to definitions, finding references. Requires a code-intelligence plugin | No |

### Agent and task tools

| Tool | What it does | Permission |
|---|---|---|
| `Agent` | Create a **subagent**: a separate Claude with its own context, that works on a subtask and returns the result (see Subagents section) | No |
| `Skill` | Trigger a skill (a predefined workflow) | Yes |
| `AskUserQuestion` | Ask a multiple-choice question to clarify requirements | No |
| `EnterPlanMode` | Switch to plan mode (read-only exploration) | No |
| `ExitPlanMode` | Present the elaborated plan for validation and exit plan mode | Yes |
| `EnterWorktree` | Create an isolated git worktree to work without risk | No |
| `ExitWorktree` | Return to the main directory from a worktree | No |

### Task management tools

These tools allow Claude to create and track a task list for complex work. The task list displays in your terminal (toggle with `Ctrl+T`).

| Tool | What it does | Permission |
|---|---|---|
| `TaskCreate` | Create a new task | No |
| `TaskGet` | Get task details | No |
| `TaskList` | List all tasks and their status | No |
| `TaskUpdate` | Update a task's status/details | No |
| `TaskOutput` | Retrieve output from a background task | No |
| `TaskStop` | Stop a background task | No |
| `TodoWrite` | Simplified version for non-interactive mode / Agent SDK | No |

### Scheduling tools

| Tool | What it does | Permission |
|---|---|---|
| `CronCreate` | Schedule a recurring prompt within the session (e.g.: check a build every 5 min). Disappears when Claude exits | No |
| `CronDelete` | Cancel a scheduled task | No |
| `CronList` | List scheduled tasks | No |

### Web and MCP tools

| Tool | What it does | Permission |
|---|---|---|
| `WebFetch` | Retrieve and analyze content from a URL (web pages, APIs) | Yes |
| `WebSearch` | Perform a web search | Yes |
| `ListMcpResourcesTool` | List resources exposed by connected MCP servers | No |
| `ReadMcpResourceTool` | Read a specific MCP resource by URI | No |
| `ToolSearch` | Search for and load MCP tools on demand when there are too many to keep in memory | No |

---

## 6. Subagents — Task Delegation

### The concept

A **subagent** is a separate Claude, launched by the main Claude to handle a specific subtask. Each subagent has its own context (it doesn't see your conversation), its own tools, and potentially a different model.

**Why use subagents?**
- **Preserve context**: searching through 50 files fills up the context. By delegating to a subagent, only the summary comes back to your conversation.
- **Parallelism**: Claude can launch multiple subagents simultaneously on independent tasks.
- **Specialization**: a "reviewer" subagent can only read (not modify), a "debugger" subagent has access to specific tools.
- **Cost**: a subagent on Haiku (fast and cheap) for simple research, Opus for complex analysis.

### Built-in subagents

| Agent | Model | Capabilities | Claude uses it when... |
|---|---|---|---|
| **Explore** | Haiku (fast) | Read-only (Read, Grep, Glob) | It needs to search or understand code without modifying it. Three levels: `quick` (targeted lookup), `medium` (moderate exploration), `very thorough` (exhaustive analysis) |
| **Plan** | Inherited from parent | Read-only | You're in plan mode and Claude needs to explore the codebase before proposing a plan |
| **General-purpose** | Inherited from parent | All tools | The task is complex, requires both exploration and modifications, or involves multiple dependent steps |
| **Bash** | Inherited from parent | Terminal only | It needs to execute commands in a separate context |
| **statusline-setup** | Sonnet | Configuration | You run `/statusline` to configure your status line |
| **Claude Code Guide** | Haiku | Documentation | You ask a question about Claude Code features |

### Creating a custom subagent

A subagent is a Markdown file with **YAML frontmatter** (metadata between `---`) followed by the **system prompt** (the instructions the subagent will follow).

**Where to place the file:**

| Location | Scope | Should it be committed? |
|---|---|---|
| `.claude/agents/my-agent.md` | This project only | Yes, shared with the team |
| `~/.claude/agents/my-agent.md` | All your projects | No, personal |
| Plugin `agents/` | Where the plugin is enabled | Via the plugin |
| `--agents` (JSON in CLI) | This session only | No, ephemeral |

**Complete example — a code review agent:**

```markdown
---
name: code-reviewer
description: Expert code review. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. When invoked:
1. Run git diff to see recent changes
2. Review for quality, security, and best practices
3. Provide feedback organized by priority: Critical / Warning / Suggestion
```

**Frontmatter fields:**

| Field | Description |
|---|---|
| `name` | Unique identifier (lowercase letters and hyphens) |
| `description` | **Critical**: Claude uses this description to decide when to delegate to this agent. Add "use proactively" so Claude uses it without being asked |
| `tools` | Tool allowlist. If omitted, inherits all tools. E.g.: `Read, Grep, Glob` = read-only |
| `disallowedTools` | Tool denylist: these tools are removed. E.g.: `Write, Edit` = no modifications |
| `model` | `haiku` (fast/cheap), `sonnet` (balanced), `opus` (most capable), `inherit` (same as parent) |
| `permissionMode` | `default` (normal), `acceptEdits` (auto-accepts edits), `plan` (read-only), `dontAsk` (auto-denies), `bypassPermissions` (everything allowed — caution!) |
| `maxTurns` | Maximum number of actions before stopping (prevents infinite loops) |
| `skills` | Skills whose full content is injected at startup. The subagent has them in memory, no need to search for them |
| `mcpServers` | MCP servers dedicated to this subagent. Can be references to existing servers or inline definitions |
| `hooks` | Lifecycle hooks specific to this subagent (see Hooks section) |
| `memory` | Persistent memory between sessions: `user` (global, `~/.claude/agent-memory/`), `project` (`.claude/agent-memory/`, versionable), `local` (`.claude/agent-memory-local/`, not versioned) |
| `background` | `true` = always in background. Claude continues responding while the agent works |
| `effort` | `low`, `medium`, `high`, `max` — reasoning depth |
| `isolation` | `worktree` = the agent works in an isolated git copy of the repo |

### How to invoke a subagent

| Method | How | When |
|---|---|---|
| **Automatic** | Claude decides on its own based on the `description` | When the description matches the task |
| **Natural language** | `"Use the code-reviewer to look at my changes"` | Claude usually chooses well |
| **@-mention** | `@"code-reviewer (agent)" review the auth module` | You **guarantee** that this specific agent is used |
| **Entire session** | `claude --agent code-reviewer` | The entire session uses this system prompt, model, and restrictions |

### Foreground vs Background

- **Foreground** (default): the subagent blocks the conversation. You see its permission requests and questions.
- **Background**: the subagent works in parallel. Permissions are requested before launch. You can put an agent in background with `Ctrl+B`.

---

## 7. Hooks — Event Automation

### The concept

**Hooks** are scripts or actions that trigger automatically when a specific event occurs in Claude Code. It's the equivalent of **git hooks** (pre-commit, post-merge...) but for Claude Code.

**Typical use cases:**
- Automatically run a linter after each file modification
- Block dangerous Bash commands (e.g.: `rm -rf /`)
- Send a Slack notification when Claude finishes work
- Log all actions for compliance auditing
- Validate that a SQL command is read-only

### The 24 available events

#### Session lifecycle

| Hook | Triggers when... | Use case |
|---|---|---|
| `SessionStart` | At the start or resumption of a session | Load dev context, set environment variables |
| `SessionEnd` | When the session ends | Cleanup, logging, state saving |

#### User input

| Hook | Triggers when... | Use case |
|---|---|---|
| `UserPromptSubmit` | Before Claude processes your message | Add automatic context, validate or block a prompt |
| `InstructionsLoaded` | When a CLAUDE.md or rules file is loaded | Compliance auditing, observability |

#### Tool execution

| Hook | Triggers when... | Use case |
|---|---|---|
| `PreToolUse` | **Before** Claude uses a tool. This is the most powerful hook: you can block, allow, or modify the action | Validate Bash commands, auto-approve safe operations, modify parameters |
| `PermissionRequest` | When the permission popup appears | Auto-approve or auto-deny certain permissions |
| `PostToolUse` | After a tool has succeeded | Log results, validate output, run a linter |
| `PostToolUseFailure` | After a tool has failed | Log errors, send alerts, suggest corrections |

#### Agent control

| Hook | Triggers when... | Use case |
|---|---|---|
| `SubagentStart` | When a subagent is launched | Inject context, apply guidelines |
| `SubagentStop` | When a subagent finishes | Validate its output, apply quality gates |
| `Stop` | When the main agent finishes its response | Force continuation, check completion criteria |
| `StopFailure` | When a turn fails (API error, rate limit...) | Log, alert, recovery actions |

#### Team and tasks

| Hook | Triggers when... | Use case |
|---|---|---|
| `TeammateIdle` | Before a teammate (in an Agent Team) goes idle | Enforce that tests pass before stopping |
| `TaskCompleted` | When a task is marked complete | Check completion criteria |

#### System

| Hook | Triggers when... | Use case |
|---|---|---|
| `Notification` | When a notification is sent | Relay to alerting systems |
| `ConfigChange` | When a configuration file changes | Security audit, block unauthorized modifications |
| `PreCompact` / `PostCompact` | Before/after context compaction | Logging, reacting to the new compacted state |

#### Worktree

| Hook | Triggers when... | Use case |
|---|---|---|
| `WorktreeCreate` / `WorktreeRemove` | When a git worktree is created/removed | Replace git with SVN/Perforce/Mercurial, cleanup |

#### MCP

| Hook | Triggers when... | Use case |
|---|---|---|
| `Elicitation` | An MCP server requests user input | Respond programmatically, bypass the dialog |
| `ElicitationResult` | After the user has responded to an elicitation | Modify the response before sending to the server |

### Handler types

Each hook can use one of these 4 handler types:

| Type | What it does | When to use |
|---|---|---|
| `command` | Executes a shell command. Receives data as JSON on stdin, returns JSON on stdout | Validations, local scripts |
| `http` | Sends a JSON POST to a URL | External integrations (Slack, logging, webhook) |
| `prompt` | Evaluates a single-turn LLM prompt to decide what to do | Contextual AI-based decisions |
| `agent` | Launches a subagent for verification | Complex validations requiring AI analysis |

### Exit codes (for `command` handlers)

| Code | Effect |
|---|---|
| **0** | Success — JSON output is processed |
| **2** | **Blocking** — the action is cancelled, the stderr message is displayed |
| **Other** | Non-blocking — execution continues despite the error |

### Where to configure hooks

| Location | Scope |
|---|---|
| `~/.claude/settings.json` | All your projects |
| `.claude/settings.json` | This project (shareable with the team) |
| `.claude/settings.local.json` | This project (personal) |
| Plugin `hooks/hooks.json` | When the plugin is enabled |
| Skill/agent frontmatter | During the component's lifetime |
| Managed policy settings | Entire organization (admin) |

### Matchers — Filtering when a hook triggers

Matchers allow precisely targeting when a hook should trigger:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "./scripts/validate-bash.sh" }
        ]
      }
    ]
  }
}
```

Here, the script will only execute when Claude uses the `Bash` tool, not for `Read` or `Edit`.

Matcher patterns: `Bash`, `Edit|Write` (or), `mcp__.*` (regex for all MCP tools).

---

## 8. Custom Skills — Extending Claude

### The concept

A **skill** is an instruction file (`SKILL.md`) that Claude can load when relevant — or that you can invoke directly with `/skill-name`. It's like giving Claude a procedure manual for a specific type of task.

**Difference from a subagent:** a skill executes within your conversation context (unless `context: fork`), while a subagent always has its own separate context.

### Two types of content

| Type | Example | Typical invocation |
|---|---|---|
| **Reference** (knowledge) | API conventions, code patterns, style guide | Claude loads it automatically when relevant |
| **Task** (workflow) | Deployment, commit with conventions, code generation | You invoke it with `/skill-name` |

### Location

| Scope | Path | Reach |
|---|---|---|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project (versionable) |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where the plugin is enabled |
| Enterprise | Managed settings | The entire organization |

Priority in case of name conflict: Enterprise > Personal > Project.

### Skill structure

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
allowed-tools: Bash
---

Deploy $ARGUMENTS to production:
1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

### Frontmatter — Configuration fields

| Field | Default | Description |
|---|---|---|
| `name` | Folder name | Display name and `/` command name |
| `description` | 1st paragraph | **Essential**: Claude uses this description to decide when to automatically load the skill |
| `argument-hint` | — | Hint displayed in autocomplete (e.g.: `[issue-number]`) |
| `disable-model-invocation` | `false` | `true` = **only you** can invoke this skill. Claude will never use it automatically. For workflows with side effects (deploy, sending messages, etc.) |
| `user-invocable` | `true` | `false` = invisible in the `/` menu. Only Claude can use it. For background knowledge |
| `allowed-tools` | — | Tools Claude can use without permission when this skill is active |
| `model` | inherited | Force a specific model |
| `effort` | inherited | Force an effort level |
| `context` | — | `fork` = execute in an isolated subagent (separate context) |
| `agent` | `general-purpose` | Subagent type when `context: fork`. E.g.: `Explore` for read-only |
| `hooks` | — | Hooks active during this skill |

### Variable substitutions

| Variable | Replaced by |
|---|---|
| `$ARGUMENTS` | Everything the user types after `/skill-name` |
| `$ARGUMENTS[N]` or `$N` | The N-th argument (0-based). E.g.: `$0` = first argument |
| `${CLAUDE_SESSION_ID}` | The current session ID |
| `${CLAUDE_SKILL_DIR}` | The path to the folder containing SKILL.md |

### Dynamic context injection

The `` !`command` `` syntax executes a shell command **before** Claude receives the skill content. The command output replaces the placeholder.

```yaml
---
name: pr-summary
description: Summarize the current PR
context: fork
---

## PR context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`

Summarize this pull request.
```

When you run `/pr-summary`, the `gh` commands execute first, and Claude receives the result (the actual diff, the actual comments) — not the commands themselves.

### Supporting files

A skill can have additional files in its folder:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/          # Expected output examples
└── scripts/
    └── helper.py      # Script that Claude can execute
```

Reference them from SKILL.md so Claude knows when to load them.

---

## 9. Keyboard Shortcuts

### Main controls

| Shortcut | What it does |
|---|---|
| `Ctrl+C` | Cancel: interrupts the current generation or clears your input |
| `Ctrl+D` | Quit Claude Code (EOF signal) |
| `Ctrl+B` | **Background**: a running Bash command or agent moves to background, and Claude continues responding. Tmux users must press twice |
| `Ctrl+F` | **Kill all background agents** (press 2x within 3 seconds to confirm) |
| `Ctrl+G` | Open your default text editor to compose a long prompt |
| `Ctrl+L` | Clear the screen (conversation remains intact) |
| `Ctrl+O` | Toggle verbose: show/hide details of each tool used |
| `Ctrl+R` | **Reverse search** in your prompt history (like in bash) |
| `Ctrl+T` | Toggle the **task list** in the terminal status area |
| `Ctrl+V` / `Cmd+V` | Paste an image from clipboard (Claude can analyze screenshots) |
| `Esc+Esc` | **Rewind**: restore code and/or conversation to a previous point |
| `Shift+Tab` / `Alt+M` | Switch between **permission modes** (Normal, Auto-Accept, Plan) |
| `Alt+P` / `Option+P` | Change **model** without clearing your current prompt |
| `Alt+T` / `Option+T` | Toggle **extended thinking** (deep reasoning mode). Run `/terminal-setup` first |

### Multiline input

| Method | Shortcut | Note |
|---|---|---|
| Backslash | `\` + `Enter` | Works everywhere |
| macOS | `Option+Enter` | Default on macOS |
| Shift+Enter | `Shift+Enter` | iTerm2, WezTerm, Ghostty, Kitty natively. For others, run `/terminal-setup` |
| Line feed | `Ctrl+J` | Universal alternative |
| Paste | Paste directly | For code blocks or logs |

### Quick prefixes

| Prefix | What it does |
|---|---|
| `/` | Invoke a command or skill |
| `!` | **Direct Bash mode**: execute a shell command without going through Claude. Output is added to conversation context. E.g.: `! npm test` |
| `@` | **File mention**: triggers file path autocomplete. The mentioned file is added to context |
| Hold `Space` | **Voice dictation** push-to-talk (requires `/voice` enabled) |

### Text editing

| Shortcut | Action |
|---|---|
| `Ctrl+K` | Delete from cursor to end of line (stored for pasting) |
| `Ctrl+U` | Delete entire line (stored for pasting) |
| `Ctrl+Y` | Paste text deleted with Ctrl+K or Ctrl+U |
| `Alt+B` / `Alt+F` | Move back/forward one word |

### Vim mode

Enabled with `/vim`. Full navigation: `h/j/k/l`, `w/e/b`, `gg/G`, operators `d/c/y` with text objects (`iw`, `i"`, `i{`...), INSERT mode with `i/a/o`, and all classic Vim commands.

---

## 10. Plugins — Packaged Extensions

### The concept

A **plugin** is a package that bundles skills, agents, MCP servers, and hooks into a single installable unit. It's the equivalent of a VS Code extension, but for Claude Code.

### Commands

```bash
# Install a plugin from the marketplace
claude plugin install <plugin-name>@<marketplace>

# Install with a precise commit SHA (version pinning)
claude plugin install <plugin-name>@<marketplace>#<sha>
```

| In-session command | Description |
|---|---|
| `/plugin` | Interactive plugin management interface |
| `/reload-plugins` | Reload all active plugins without restarting (for development) |

### Plugin components

A plugin can contain all or some of:
- `skills/` — additional skills
- `agents/` — specialized subagents
- `hooks/hooks.json` — automated hooks
- MCP servers — external tools

**Security restrictions:** agents defined in plugins CANNOT use `hooks`, `mcpServers`, or `permissionMode`. For these features, copy the agent file to `.claude/agents/`.

---

## 11. Configuration Files

Claude Code uses a hierarchy of files for its configuration. Higher-level files override lower-level ones.

### Settings (Claude Code behavior)

| File | Scope | Should it be committed? |
|---|---|---|
| `~/.claude/settings.json` | All your projects | No (personal) |
| `.claude/settings.json` | This project | Yes (shared with the team) |
| `.claude/settings.local.json` | This project | No (personal, in .gitignore) |

### Persistent instructions (what Claude "knows")

| File | Scope | Typical content |
|---|---|---|
| `CLAUDE.md` (project root) | This project | Project architecture, code conventions, build/test commands, special instructions |
| `~/.claude/CLAUDE.md` | All your projects | Global personal preferences (code style, preferred language, etc.) |

`CLAUDE.md` is automatically loaded at the beginning of each session. It's the ideal place to document what Claude needs to know about your project.

### Skills and agents

| File | Scope |
|---|---|
| `.claude/skills/<name>/SKILL.md` | Project skills |
| `~/.claude/skills/<name>/SKILL.md` | Personal skills |
| `.claude/agents/<name>.md` | Project subagents |
| `~/.claude/agents/<name>.md` | Personal subagents |

### Agent memory

| Directory | When |
|---|---|
| `~/.claude/agent-memory/<agent>/` | Global memory for an agent (`memory: user`) |
| `.claude/agent-memory/<agent>/` | Project memory for an agent (`memory: project`) |
| `.claude/agent-memory-local/<agent>/` | Local memory for an agent (`memory: local`) |

---

## 12. Available Models

| Alias | Full ID | Characteristics |
|---|---|---|
| `opus` | `claude-opus-4-6` | Most capable. Best reasoning, best code quality. Slower and more expensive. Supports `effort: max` |
| `sonnet` | `claude-sonnet-4-6` | **Recommended for most use cases**. Good balance of quality/speed/cost |
| `haiku` | `claude-haiku-4-5-20251001` | Fastest and cheapest. Ideal for quick research subagents |

Changing models: `--model <alias>` at launch, `/model` in session, or `Alt+P`.

**Fast mode** (`/fast`) accelerates Opus 4.6 output without changing models.

---

## 13. Key Environment Variables

Variables to set in your shell **before** launching `claude`.

| Variable | Value | What it does |
|---|---|---|
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | `1` | Disables all background tasks (background subagents, background Bash) |
| `CLAUDE_CODE_DISABLE_CRON` | `1` | Immediately stops all scheduled cron jobs |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | `false` | Disables prompt suggestions (the grayed-out text that appears after each response) |
| `CLAUDE_CODE_NEW_INIT` | `true` | `/init` offers a guided interactive flow that also configures skills, hooks, and memory |
| `CLAUDE_CODE_TASK_LIST_ID` | `my-project` | Uses a named directory in `~/.claude/tasks/` to share the task list between sessions |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | `50` | Triggers auto-compaction at 50% of context instead of 95% (default). Useful for subagents |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | `1` | Resets the working directory to the project directory after each Bash command |
| `CLAUDE_ENV_FILE` | `./setup.sh` | Shell script executed to persist environment variables between Bash commands |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | `1` | Also loads CLAUDE.md files found in directories added via `--add-dir` |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | `32000` | Override of the character budget for skill descriptions in context |
| `ENABLE_CLAUDEAI_MCP_SERVERS` | `false` | Disables MCP servers provided by claude.ai |

---

## 14. Key Settings (settings.json)

These settings go in `~/.claude/settings.json` (global) or `.claude/settings.json` (project).

| Setting | Type | What it does |
|---|---|---|
| `agent` | string | Default agent for each session. Equivalent to permanent `--agent` |
| `autoMemoryDirectory` | string | Custom directory for auto-memory storage |
| `cleanupPeriodDays` | number | Session transcript retention duration (default: 30 days) |
| `modelOverrides` | object | Map model selector entries to custom provider IDs |
| `plansDirectory` | string | Where to store plan files |
| `showTurnDuration` | boolean | Show/hide the duration of each conversation turn |
| `temperatureOverride` | number | Override model temperature (0 = deterministic, 1 = creative) |
| `sandbox.enableWeakerNetworkIsolation` | boolean | Less strict network isolation (macOS) |
| `sandbox.excludedCommands` | array | Commands excluded from sandbox |

### Permissions in settings.json

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(git log *)",
      "Bash(npm test *)"
    ],
    "deny": [
      "Agent(Explore)",
      "Skill(deploy *)"
    ]
  }
}
```

- `allow`: these tools execute **without asking** for permission
- `deny`: these tools are **completely blocked**

**Pattern syntax:**
```
Read                    # The exact tool "Read"
Bash(git log *)         # Bash, but only commands starting with "git log"
Agent(Explore)          # The "Explore" subagent
Skill(commit)           # The "commit" skill exactly
Skill(deploy *)         # Any skill starting with "deploy"
mcp__memory__*          # All MCP tools from the "memory" server
```

---

## 15. Agent Teams — Parallel Work

### The concept

**Agent Teams** allow **multiple Claude Code instances** to work in parallel on independent tasks and **communicate with each other**. This is different from subagents (which work within a single session): each teammate has its own independent session with its own context.

**When to use Agent Teams rather than subagents:**
- Tasks are truly independent and voluminous
- A single subagent's context isn't enough
- You want to see each agent working in its own terminal

| Mode | What it does |
|---|---|
| `auto` | Claude chooses the best display mode |
| `in-process` | All teammates display in the same terminal |
| `tmux` | Each teammate has its own tmux pane (requires tmux installed) |

Configuration: `claude --teammate-mode tmux`

---

## 16. MCP — Model Context Protocol

### The concept

**MCP** is a standard protocol that allows Claude Code to connect to **external tools and services**. An MCP server exposes functionality (read a database, send a Slack message, query an API...) that Claude can use like any other tool.

It's like plugging "tool plugins" into Claude: an MCP server for GitHub, one for Slack, one for your internal database, etc.

### Commands

```bash
# Add an MCP server
claude mcp add <name> -- <command> [args...]

# Example: add a Playwright server for web automation
claude mcp add playwright -- npx -y @playwright/mcp@latest

# List configured servers
claude mcp list

# Remove a server
claude mcp remove <name>
```

In session: `/mcp` to manage interactively.

### Transport types

| Type | What it does | When to use |
|---|---|---|
| `stdio` | Launches a local process, communicates via stdin/stdout | Local tools (Playwright, local database) |
| `http` | Communicates via HTTP | Web services, remote APIs |
| `sse` | Server-Sent Events (unidirectional streaming) | Services that send continuous updates |
| `ws` | WebSocket (bidirectional real-time) | Real-time communication |

### MCP Tool Search

When you have many MCP servers, their tool descriptions can consume too much context. Claude Code then automatically enables **tool search**: instead of loading all descriptions into memory, Claude searches for relevant tools on demand via the `ToolSearch` tool.

Default threshold: ~10% of context. Configurable via the `auto:N` setting (0-100%).

### MCP prompts as commands

MCP servers can expose predefined prompts. They appear as commands `/mcp__<server>__<prompt>`.

---

## 17. Permission Modes

Permission modes control Claude's level of autonomy. Switch between modes with `Shift+Tab` in session or `--permission-mode` at launch.

| Mode | Control level | When to use |
|---|---|---|
| **Normal** (default) | Claude asks permission for each sensitive action (writing, execution) | Daily use — you keep control |
| **Auto-Accept** | Claude can modify files without asking, but still asks for shell commands | You trust Claude for edits and want to go faster |
| **Plan** | Claude can only **read** code. No modifications possible | Exploration, understanding an unfamiliar codebase, developing an action plan before starting |
| **Don't Ask** | Auto-denies all permission requests. Only tools explicitly in `allow` work | Restricted environments, controlled execution |
| **Bypass Permissions** | Claude does everything without asking (except writing to `.git`, `.claude`, `.vscode`) | Only in disposable environments (CI/CD, containers). **Never in production** |

---

## 18. Recent Major Version History

| Version | Date (approx.) | Notable additions |
|---|---|---|
| **2.1.81** | March 2026 | `--bare` flag, channel servers for mobile approval |
| **2.1.80** | March 2026 | `rate_limits` statusline, plugin from settings.json |
| **2.1.76** | Feb 2026 | MCP elicitation (MCP servers requesting user input) |
| **2.1.75** | Feb 2026 | `/color`, timestamps on memory files |
| **2.1.71** | Feb 2026 | `/loop` skill (recurring prompts), cron tools |
| **2.1.70** | Feb 2026 | `/debug` skill, voice dictation in 20 languages |
| **2.1.69** | Jan 2026 | `/claude-api` skill, `InstructionsLoaded` hook |
| **2.1.66** | Jan 2026 | `/simplify` and `/batch` skills, HTTP hooks |
| **2.1.59** | Jan 2026 | Auto-memory (Claude saves context automatically) |
| **2.1.51** | Dec 2025 | `claude remote-control` |
| **2.1.50** | Dec 2025 | Worktree hooks, `isolation: worktree`, LSP |
| **2.1.49** | Dec 2025 | `--worktree`, background agents |
| **2.1.45** | Nov 2025 | Claude Sonnet 4.6 |
| **2.1.33** | Nov 2025 | `TeammateIdle`/`TaskCompleted` hooks, persistent agent memory |
| **2.1.32** | Nov 2025 | Claude Opus 4.6, skill auto-discovery |
| **2.1.16** | Oct 2025 | Task system with dependencies |

---

*Sources: [CLI Reference](https://code.claude.com/docs/en/cli-reference) · [Commands](https://code.claude.com/docs/en/commands) · [Tools Reference](https://code.claude.com/docs/en/tools-reference) · [Hooks](https://code.claude.com/docs/en/hooks) · [Skills](https://code.claude.com/docs/en/slash-commands) · [Subagents](https://code.claude.com/docs/en/sub-agents) · [Interactive Mode](https://code.claude.com/docs/en/interactive-mode) · [GitHub](https://github.com/anthropics/claude-code) · [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)*
