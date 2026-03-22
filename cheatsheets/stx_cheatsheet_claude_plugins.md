# Claude Code Plugins — Complete Reference Guide (March 21, 2026)

> Official sources: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) + [code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)
> Requires: Claude Code version **1.0.33 or later**

---

## What Are Claude Code Plugins?

A plugin is a **self-contained directory** that extends Claude Code with custom functionality. It can bundle any combination of: skills, agents, hooks, MCP servers, LSP servers, and commands — all packaged together for easy sharing and installation.

**Why plugins instead of standalone configuration?**

Without plugins, you customize Claude Code by placing files in your `.claude/` directory (skills, agents, hooks, etc.). This works well for personal workflows or project-specific tweaks. But as soon as you want to **share** those customizations — with your team, your organization, or the community — you need a distribution mechanism. That's what plugins provide.

| Approach | Skill invocation | Best for |
|----------|-----------------|----------|
| **Standalone** (`.claude/` directory) | `/hello` | Personal workflows, project-specific customizations, quick experiments |
| **Plugin** (directory with `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Sharing with teammates, distributing to community, versioned releases, reusable across projects |

**Key differences:**
- Plugins are **namespaced**: all components are prefixed with the plugin name (e.g., `/my-plugin:deploy`) to prevent conflicts when multiple plugins are installed
- Plugins are **versioned**: they follow semantic versioning, enabling controlled updates
- Plugins are **distributable**: they can be published to marketplaces (public or private) and installed with a single command
- Plugins are **scoped**: they can be installed at user, project, or local level

---

## 1. Plugin Architecture

### 1.1 Directory Structure

A plugin is a directory containing a `.claude-plugin/` metadata folder and any combination of component directories:

```
my-plugin/
├── .claude-plugin/           # Metadata directory (ONLY plugin.json goes here)
│   └── plugin.json           # Plugin manifest (optional but recommended)
├── commands/                 # Slash commands as markdown files
│   ├── status.md
│   └── logs.md
├── agents/                   # Custom subagent definitions
│   ├── security-reviewer.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills (each in its own subdirectory)
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       ├── reference.md
│       └── scripts/
│           └── helper.py
├── hooks/                    # Hook configurations
│   └── hooks.json
├── settings.json             # Default settings (only "agent" key supported)
├── .mcp.json                 # MCP server definitions
├── .lsp.json                 # LSP server configurations
├── scripts/                  # Utility scripts (used by hooks, skills, etc.)
│   ├── security-scan.sh
│   └── format-code.py
├── README.md                 # Documentation for users
├── LICENSE
└── CHANGELOG.md
```

**Critical rule**: only `plugin.json` goes inside `.claude-plugin/`. All component directories (`commands/`, `agents/`, `skills/`, `hooks/`, `scripts/`) must be at the **plugin root level**, not inside `.claude-plugin/`.

### 1.2 Plugin Manifest (`.claude-plugin/plugin.json`)

The manifest describes the plugin's metadata and tells Claude Code where to find its components. It is **optional** — if omitted, Claude Code auto-discovers components in default locations and derives the plugin name from the directory name.

```json
{
  "name": "my-plugin",
  "version": "1.2.0",
  "description": "Brief description of what this plugin does",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/my-plugin",
  "repository": "https://github.com/author/my-plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/"
}
```

#### Metadata Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique identifier. Must be kebab-case, no spaces (e.g., `code-formatter`) |
| `version` | string | No | Semantic version: `MAJOR.MINOR.PATCH` (e.g., `1.2.0`) |
| `description` | string | No | Brief explanation shown in marketplace and plugin manager |
| `author` | object | No | `{name, email, url}` — creator information |
| `homepage` | string | No | URL to documentation |
| `repository` | string | No | URL to source code |
| `license` | string | No | SPDX identifier (e.g., `"MIT"`, `"Apache-2.0"`) |
| `keywords` | array | No | Discovery tags for marketplace search |

#### Component Path Fields

All paths must be **relative to the plugin root** and start with `./`. Custom paths **supplement** default directories — they don't replace them.

| Field | Type | Description |
|-------|------|-------------|
| `commands` | string or array | Additional command files or directories |
| `agents` | string or array | Additional agent definition files |
| `skills` | string or array | Additional skill directories |
| `hooks` | string, array, or object | Hook config file paths or inline config |
| `mcpServers` | string, array, or object | MCP config file paths or inline config |
| `lspServers` | string, array, or object | LSP server config file paths or inline config |
| `outputStyles` | string or array | Output style files or directories |

### 1.3 Environment Variables

Two special variables are available in all plugin contexts (hooks, MCP configs, scripts):

| Variable | Description | Example value |
|----------|-------------|---------------|
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to the plugin's installation directory. **Changes on update** — never hardcode this path. | `/Users/me/.claude/plugins/cache/abc123/my-plugin` |
| `${CLAUDE_PLUGIN_DATA}` | Persistent directory for plugin state that **survives updates** (caches, databases, node_modules). | `~/.claude/plugins/data/{plugin-id}/` |

**Rule of thumb**: use `${CLAUDE_PLUGIN_ROOT}` to reference files shipped with the plugin (scripts, configs). Use `${CLAUDE_PLUGIN_DATA}` for anything the plugin creates at runtime (caches, generated files, downloaded dependencies).

---

## 2. Plugin Components

A plugin can include any combination of the following components. Each component type has its own format and conventions.

### 2.1 Skills (`SKILL.md`)

A skill is a set of instructions that teaches Claude how to perform a specific task. Each skill lives in its own subdirectory under `skills/`, with a `SKILL.md` file as the entry point.

**Example**: `skills/code-reviewer/SKILL.md`

```yaml
---
name: code-reviewer
description: Reviews code for quality, security, and best practices. Use after implementing changes.
user-invocable: true
argument-hint: [file-or-directory]
allowed-tools: Read, Grep, Glob
model: sonnet
effort: high
context: fork
agent: Explore
disable-model-invocation: false
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

You are a code reviewer. Analyze the code at $ARGUMENTS and provide:
1. Security issues (critical first)
2. Performance concerns
3. Code style violations
4. Suggestions for improvement

Use $ARGUMENTS[0] for the target path. Current session: ${CLAUDE_SESSION_ID}.
Skill directory: ${CLAUDE_SKILL_DIR}.
```

#### Frontmatter Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | directory name | Display name (lowercase, hyphens, max 64 chars) |
| `description` | string | — | What the skill does. Claude uses this to decide when to auto-invoke it. **Write it carefully** — a vague description means Claude won't know when to use it. |
| `user-invocable` | boolean | `true` | If `true`, appears in the `/` menu for manual invocation. If `false`, only Claude can invoke it (hidden from user). |
| `disable-model-invocation` | boolean | `false` | If `true`, only the user can invoke this skill (Claude cannot auto-select it). Use for dangerous or expensive operations. |
| `argument-hint` | string | — | Autocomplete hint shown after the skill name (e.g., `[issue-number]`). |
| `allowed-tools` | string | all tools | Comma-separated list of tools Claude can use without permission when this skill is active (e.g., `Read, Grep, Bash`). |
| `model` | string | session default | Model to use: `sonnet`, `opus`, `haiku`. |
| `effort` | string | session default | Reasoning effort: `low`, `medium`, `high`, `max`. |
| `context` | string | — | Set to `fork` to run the skill in an isolated subagent (separate context window). |
| `agent` | string | `general-purpose` | When `context: fork`, which subagent type to use: `Explore`, `Plan`, `general-purpose`, or a custom agent name. |
| `hooks` | object | — | Hooks scoped to this skill's lifecycle (same format as `hooks.json`). |

#### Dynamic Context

Use shell commands in backticks prefixed with `!` to inject dynamic content into the skill prompt at invocation time:

```markdown
Current git branch: !`git branch --show-current`
Recent changes: !`git diff --stat HEAD~5`
```

#### Variables Available in Skill Body

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Full argument string passed by user |
| `$ARGUMENTS[0]`, `$ARGUMENTS[1]`, `$0`, `$1` | Positional arguments |
| `${CLAUDE_SESSION_ID}` | Current session identifier |
| `${CLAUDE_SKILL_DIR}` | Absolute path to the skill's directory |

### 2.2 Agents (Subagents)

A subagent is a specialized AI assistant that the main agent can delegate work to. Each subagent runs in its own context window, which keeps the main conversation clean. Subagents are defined as markdown files in `agents/`.

**Example**: `agents/security-reviewer.md`

```yaml
---
name: security-reviewer
description: Reviews code for security vulnerabilities. Use proactively after code changes.
tools: Read, Glob, Grep, Bash
disallowedTools: Write, Edit
model: sonnet
maxTurns: 20
effort: high
background: false
isolation: worktree
memory: user
skills:
  - api-conventions
---

You are a security reviewer. Analyze code for OWASP Top 10 vulnerabilities,
injection risks, authentication issues, and data exposure.

Report findings with severity (Critical/High/Medium/Low), affected file and line,
description, and recommended fix.
```

#### Frontmatter Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | filename | Subagent identifier |
| `description` | string | — | When to use this subagent. Claude reads this to decide when to delegate. Include "Use proactively" if it should be auto-triggered. |
| `tools` | string | all tools | Comma-separated list of allowed tools |
| `disallowedTools` | string | — | Tools explicitly denied to this subagent |
| `model` | string | session default | Model: `sonnet`, `opus`, `haiku` |
| `maxTurns` | number | — | Maximum conversation turns before the subagent must return |
| `effort` | string | session default | Reasoning effort: `low`, `medium`, `high`, `max` |
| `background` | boolean | `false` | If `true`, runs in background without blocking the main agent |
| `isolation` | string | — | Set to `worktree` to give the subagent its own git worktree |
| `memory` | string | — | Memory access: `user` gives access to user memories |
| `skills` | array | — | Skills available to this subagent |

#### Restrictions for Plugin Subagents

For security reasons, plugin subagents **cannot** use:
- `hooks` — ignored
- `mcpServers` — ignored
- `permissionMode` — ignored

These fields work in standalone agents (`.claude/agents/`) but are silently ignored in plugins.

### 2.3 Hooks (`hooks.json`)

Hooks are processes that observe, control, and extend the agent loop. They fire on specific lifecycle events and can block or modify agent behavior. Hooks are defined in a `hooks.json` file.

**Example**: `hooks/hooks.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh",
            "timeout": 600,
            "statusMessage": "Formatting code..."
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/security-scan.sh",
            "timeout": 300,
            "statusMessage": "Security scan..."
          }
        ]
      }
    ]
  }
}
```

#### 25 Lifecycle Events

| Event | When it fires |
|-------|---------------|
| `SessionStart` | Agent session begins |
| `SessionEnd` | Agent session ends |
| `InstructionsLoaded` | All rules and instructions have been loaded |
| `UserPromptSubmit` | User sends a message |
| `PreToolUse` | Before a tool is called |
| `PermissionRequest` | When a tool requests user permission |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `SubagentStart` | Before a subagent is launched |
| `SubagentStop` | After a subagent finishes |
| `TeammateIdle` | A teammate in an Agent Team becomes idle |
| `TaskCompleted` | A background task completes |
| `Stop` | Agent is stopped by user |
| `StopFailure` | Agent stop failed |
| `ConfigChange` | Configuration files changed |
| `PreCompact` | Before context compaction (conversation too long) |
| `PostCompact` | After context compaction |
| `WorktreeCreate` | Git worktree created for isolation |
| `WorktreeRemove` | Git worktree removed |
| `Notification` | Agent sends a notification |
| `Elicitation` | Agent asks user a structured question |
| `ElicitationResult` | User responds to an elicitation |

#### 4 Handler Types

| Type | How it works |
|------|-------------|
| `command` | Runs a shell script. Receives JSON on stdin, returns JSON on stdout. Most common type. |
| `http` | Sends a POST request to an HTTP endpoint with JSON body. |
| `prompt` | An LLM evaluates a condition and decides whether to allow/block. |
| `agent` | Launches a subagent with tools to handle the event. |

#### Exit Codes (for `command` type)

| Exit code | Meaning |
|-----------|---------|
| `0` | Success — process JSON output if any |
| `2` | Blocking error — action is cancelled, stderr is fed to Claude for correction |
| Other | Non-blocking error — logged but execution continues |

#### Matcher Syntax

The `matcher` field filters which tool or event triggers the hook:
- Exact match: `"Bash"`
- Multiple tools: `"Write|Edit"`
- Regex: `".*"` (all tools)

### 2.4 MCP Servers (`.mcp.json`)

MCP (Model Context Protocol) servers extend the agent's capabilities with external tools. A plugin can bundle MCP server configurations that are automatically activated when the plugin is installed.

**Example**: `.mcp.json`

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_DATA}/database.sqlite"
      }
    },
    "remote-api": {
      "type": "sse",
      "url": "https://api.example.com/mcp"
    }
  }
}
```

#### Supported Transports

| Transport | Description | Use case |
|-----------|-------------|----------|
| `stdio` | Local process, communicates via stdin/stdout | Local tools, scripts, binaries |
| `sse` | Server-Sent Events over HTTP | Remote servers, shared team tools |
| `streamable-http` | HTTP streaming | Cloud services, APIs |

**Important**: always use `${CLAUDE_PLUGIN_ROOT}` for paths to bundled binaries/configs, and `${CLAUDE_PLUGIN_DATA}` for runtime data.

### 2.5 LSP Servers (`.lsp.json`)

LSP (Language Server Protocol) servers provide language intelligence (autocomplete, diagnostics, go-to-definition) to the agent. This is particularly useful for languages that Claude doesn't natively understand well.

**Example**: `.lsp.json`

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  },
  "python": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python",
      ".pyi": "python"
    }
  }
}
```

#### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Path to the language server binary |
| `extensionToLanguage` | Yes | Maps file extensions to language IDs |
| `args` | No | Command-line arguments |
| `transport` | No | `stdio` (default) or `socket` |
| `env` | No | Environment variables |
| `initializationOptions` | No | LSP initialization options |
| `settings` | No | LSP workspace settings |
| `workspaceFolder` | No | Override workspace root |
| `startupTimeout` | No | Max time to wait for server start (ms) |
| `shutdownTimeout` | No | Max time to wait for graceful shutdown (ms) |
| `restartOnCrash` | No | Auto-restart if server crashes (boolean) |
| `maxRestarts` | No | Maximum restart attempts |

### 2.6 Commands (Legacy)

Commands are slash commands defined as markdown files in `commands/`. They are the simplest form of customization — a markdown file whose content is injected into the conversation when the user types the command.

**Example**: `commands/status.md`

```markdown
Check the status of the current project:
1. Run `git status` to see uncommitted changes
2. Run the test suite
3. Check for linting errors
4. Summarize findings
```

The command is invoked as `/my-plugin:status`. The filename (without `.md`) becomes the command name.

**Note**: Skills (`SKILL.md`) are the modern replacement for commands. Skills offer frontmatter configuration, argument handling, tool restrictions, and model selection. Use commands only for very simple instructions.

### 2.7 Settings (`settings.json`)

A plugin can set a default subagent that activates when the plugin is loaded. Currently, only the `agent` key is supported.

**Example**: `settings.json`

```json
{
  "agent": "security-reviewer"
}
```

This makes the `security-reviewer` subagent (defined in `agents/security-reviewer.md`) the default agent for sessions using this plugin.

---

## 3. Using Plugins

### 3.1 Adding a Marketplace

Before installing plugins, you need to add a **marketplace** — a repository or URL that hosts plugin definitions.

```bash
# From GitHub (owner/repo shorthand)
/plugin marketplace add anthropics/claude-code

# From GitLab, Bitbucket, or any git host
/plugin marketplace add https://gitlab.com/company/plugins.git

# Specific branch or tag
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0

# Local directory (for development)
/plugin marketplace add ./my-marketplace

# Remote URL (non-git)
/plugin marketplace add https://example.com/marketplace.json
```

### 3.2 Installing Plugins

```bash
# Install to user scope (default — available in all your projects)
/plugin install code-formatter@company-tools

# Install to project scope (shared with team via version control)
claude plugin install code-formatter@company-tools --scope project

# Install to local scope (project-specific, gitignored)
claude plugin install code-formatter@company-tools --scope local
```

### 3.3 Managing Plugins

```bash
# Disable (keeps installed, stops loading)
/plugin disable code-formatter@company-tools

# Re-enable
/plugin enable code-formatter@company-tools

# Uninstall
/plugin uninstall code-formatter@company-tools

# Uninstall but keep persistent data
/plugin uninstall code-formatter@company-tools --keep-data

# Update to latest version
/plugin update code-formatter@company-tools

# Reload all plugins without restarting Claude Code
/reload-plugins
```

### 3.4 Installation Scopes

| Scope | Settings file | Shared | Use case |
|-------|--------------|--------|----------|
| `user` | `~/.claude/settings.json` | No | Personal plugins, available in all your projects |
| `project` | `.claude/settings.json` | Yes (via git) | Team plugins — all team members get them |
| `local` | `.claude/settings.local.json` | No (gitignored) | Project-specific, personal plugins |
| `managed` | Managed settings (read-only) | Yes (org-wide) | Organization-wide, admin-controlled |

### 3.5 Team Configuration

To pre-configure plugins for your team, add this to `.claude/settings.json` (committed to version control):

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

When a team member clones the repo and opens Claude Code, they will be prompted to install these plugins.

### 3.6 The Plugin Manager UI

Type `/plugin` in Claude Code to open the interactive plugin manager with four tabs:

| Tab | What it shows |
|-----|---------------|
| **Discover** | Available plugins from all added marketplaces |
| **Installed** | Currently installed plugins with enable/disable toggles |
| **Marketplaces** | Configured marketplace sources |
| **Errors** | Plugin loading errors and diagnostics |

---

## 4. Creating a Plugin — Step by Step

### Step 1: Start with standalone components

Develop your skills, agents, and hooks in your `.claude/` directory first. Test them thoroughly in your daily workflow before packaging.

### Step 2: Create the plugin directory

```bash
mkdir my-plugin
cd my-plugin
mkdir -p .claude-plugin skills/my-skill agents hooks scripts
```

### Step 3: Write the manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does in one sentence",
  "author": { "name": "Your Name" },
  "license": "MIT",
  "keywords": ["relevant", "tags"]
}
```

### Step 4: Add your components

Move your tested skills, agents, hooks, and MCP configs into the plugin directory. Update all file paths to use `${CLAUDE_PLUGIN_ROOT}`.

### Step 5: Test locally

```bash
# Load the plugin directly without installing
claude --plugin-dir ./my-plugin

# Load multiple plugins simultaneously
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

When a `--plugin-dir` plugin has the same name as an installed marketplace plugin, the **local copy takes precedence** — this is useful for testing updates.

Inside Claude Code, after making changes to your plugin files:

```
/reload-plugins
```

### Step 6: Validate

```bash
# From the terminal
claude plugin validate .

# Or from within Claude Code
/plugin validate .
```

### Step 7: Debug if needed

```bash
# Debug mode shows detailed plugin loading information
claude --debug
```

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Plugin not loading | Invalid `plugin.json` | Run `claude plugin validate .` |
| Commands not appearing | Wrong directory structure | `commands/` must be at plugin root, not inside `.claude-plugin/` |
| Hooks not firing | Script not executable | `chmod +x scripts/my-hook.sh` |
| MCP server fails | Hardcoded paths | Use `${CLAUDE_PLUGIN_ROOT}` for all plugin file paths |
| Path errors | Absolute paths in manifest | All paths must be relative, starting with `./` |
| LSP binary not found | Not installed on user's machine | Document prerequisites in README |
| Skills not appearing | Cache issue | `rm -rf ~/.claude/plugins/cache`, restart, reinstall |
| Version not updating | Version not bumped | Always increment `version` in `plugin.json` before distributing |

---

## 5. Publishing Plugins

### 5.1 Creating a Marketplace

A marketplace is a repository containing a `marketplace.json` file that lists available plugins.

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "metadata": {
    "description": "Internal development tools for our team",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": { "name": "DevTools Team" },
      "homepage": "https://docs.example.com/formatter",
      "repository": "https://github.com/company/formatter",
      "license": "MIT",
      "keywords": ["formatting", "linting"],
      "category": "productivity",
      "tags": ["code-quality"],
      "strict": true
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin",
        "ref": "v2.0.0",
        "sha": "a1b2c3d4e5f6..."
      }
    }
  ]
}
```

### 5.2 Plugin Source Types

Plugins in a marketplace can be sourced from various locations:

| Source | Format | Required fields |
|--------|--------|-----------------|
| **Relative path** | `"./my-plugin"` | — |
| **GitHub** | object | `source: "github"`, `repo` |
| **Git URL** | object | `source: "url"`, `url` |
| **Git subdirectory** | object | `source: "git-subdir"`, `url`, `path` |
| **npm** | object | `source: "npm"`, `package` |

Optional fields for all git sources: `ref` (branch/tag), `sha` (commit hash for pinning).

**Example — GitHub source:**
```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "owner/repo-name",
    "ref": "v1.0.0",
    "sha": "abc123..."
  }
}
```

**Example — npm source:**
```json
{
  "name": "my-plugin",
  "source": {
    "source": "npm",
    "package": "@company/claude-plugin-formatter",
    "version": "^2.0.0",
    "registry": "https://npm.company.com"
  }
}
```

### 5.3 Strict Mode

| `strict` value | Behavior |
|----------------|----------|
| `true` (default) | `plugin.json` inside the plugin is the authority. Marketplace entry can only supplement metadata. |
| `false` | Marketplace entry **is** the entire plugin definition. Useful for lightweight plugins or when wrapping third-party tools. |

### 5.4 Hosting Your Marketplace

| Method | How users add it |
|--------|-----------------|
| **GitHub** (recommended) | `/plugin marketplace add owner/repo` |
| **Any git host** | `/plugin marketplace add https://gitlab.com/company/plugins.git` |
| **Private repos** | Uses existing git credentials. Set `GITHUB_TOKEN`, `GITLAB_TOKEN`, or `BITBUCKET_TOKEN` for automated access. |
| **HTTP URL** | `/plugin marketplace add https://example.com/marketplace.json` |

### 5.5 Submitting to the Official Anthropic Marketplace

For broad distribution, submit your plugin to Anthropic's official marketplace:

- **From Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- **From Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

Plugins with an **"Anthropic Verified"** badge have undergone additional quality and safety review.

### 5.6 Versioning

Follow **semantic versioning** (`MAJOR.MINOR.PATCH`):

| Change type | Version bump | Example |
|-------------|-------------|---------|
| Breaking changes (renamed commands, removed skills) | MAJOR | `1.0.0` → `2.0.0` |
| New features (new skills, new agents) | MINOR | `1.0.0` → `1.1.0` |
| Bug fixes (fixed hook, updated prompt) | PATCH | `1.0.0` → `1.0.1` |
| Pre-release testing | Suffix | `2.0.0-beta.1` |

**Important**: if you change code but don't bump the version, users won't see the changes due to caching. Always increment before distributing.

Version can be set in both `plugin.json` and `marketplace.json` — if both are set, `plugin.json` wins silently.

### 5.7 Auto-Updates

Official Anthropic marketplaces have auto-update enabled by default. For other marketplaces, auto-update can be toggled per marketplace via the `/plugin` > Marketplaces tab.

| Environment variable | Effect |
|---------------------|--------|
| `DISABLE_AUTOUPDATER=true` | Disables all auto-updates (including plugins) |
| `FORCE_AUTOUPDATE_PLUGINS=true` | Keeps plugin auto-updates even when the main updater is disabled |

### 5.8 Release Channels

For stable vs. beta releases, create separate marketplace files pinned to different refs:

```json
{
  "name": "stable-tools",
  "plugins": [{
    "name": "formatter",
    "source": { "source": "github", "repo": "company/formatter", "ref": "stable" }
  }]
}
```

```json
{
  "name": "beta-tools",
  "plugins": [{
    "name": "formatter",
    "source": { "source": "github", "repo": "company/formatter", "ref": "beta" }
  }]
}
```

### 5.9 Pre-Populating for CI/Containers

Set the `CLAUDE_CODE_PLUGIN_SEED_DIR` environment variable to a directory containing pre-built plugins. Claude Code will load them on startup. Supports layered paths with `:` separator on Unix.

---

## 6. Cross-Compatibility (Agent Skills Open Standard)

Claude Code skills follow the **[Agent Skills](https://agentskills.io)** open standard — an interoperable format recognized by **30+ AI tools**. This means a skill you write for Claude Code can also work in other tools, and vice versa.

### Compatible Tools

| Tool | Skills docs |
|------|------------|
| **Cursor IDE** | [cursor.com/docs/context/skills](https://cursor.com/docs/context/skills) |
| **VS Code / GitHub Copilot** | [code.visualstudio.com/docs/copilot/customization/agent-skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) |
| **Gemini CLI** | [geminicli.com/docs/cli/skills](https://geminicli.com/docs/cli/skills/) |
| **OpenAI Codex** | [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills/) |
| **JetBrains Junie** | [junie.jetbrains.com/docs/agent-skills.html](https://junie.jetbrains.com/docs/agent-skills.html) |
| **Roo Code, Goose, OpenHands, Amp, Letta, TRAE, Kiro, Databricks, Spring AI** | See [agentskills.io](https://agentskills.io) |

### The Universal Format

The **core format** is the same everywhere: a `SKILL.md` file with YAML frontmatter containing at minimum `name` and `description`, followed by markdown instructions.

```yaml
---
name: my-skill
description: What this skill does
---
Instructions for the AI agent...
```

This minimal format works across all compatible tools.

### Claude Code Extensions

Claude Code **extends** the standard with additional frontmatter fields: `disable-model-invocation`, `context`, `agent`, `allowed-tools`, `hooks`, `effort`, `model`, `user-invocable`, and `argument-hint`. These extensions are **silently ignored** by tools that don't support them — the skill still works, it just loses those extra features.

### Making a Plugin Work on Both Claude Code and Cursor IDE

**For skills**: place them in `.agents/skills/` or `.cursor/skills/` (Cursor) and `.claude/skills/` (Claude Code). Both tools discover `SKILL.md` files in these directories. Use only the standard frontmatter fields (`name`, `description`) for maximum compatibility.

**For agents/subagents**: both Cursor and Claude Code support agents as markdown files with YAML frontmatter in their respective directories (`.cursor/agents/`, `.claude/agents/`). The format is largely compatible.

**For MCP servers**: both tools use the same MCP configuration format. Cursor uses `.cursor/mcp.json`, Claude Code uses `.mcp.json` or `.claude/mcp.json`.

**For rules**: Cursor uses `.cursor/rules/*.mdc` and `AGENTS.md`. Claude Code uses `CLAUDE.md` and `.claude/rules/*.md`. These are **not compatible** — you need separate rule files for each tool.

**For hooks**: Cursor uses `.cursor/hooks.json`, Claude Code uses `.claude/settings.json` or `hooks/hooks.json`. The event names and formats differ — hooks are **not cross-compatible**.

### Compatibility Summary

| Component | Cross-compatible? | Shared format |
|-----------|-------------------|---------------|
| Skills (SKILL.md) | Yes | Agent Skills open standard |
| Agents/Subagents | Largely yes | Markdown + YAML frontmatter |
| MCP servers | Yes | Same JSON format, different file locations |
| Rules | No | Different file formats and locations |
| Hooks | No | Different event names and formats |
| LSP servers | No | Claude Code specific |
| Commands | No | Claude Code specific |

### Strategy for Dual-Platform Plugins

If you need a plugin that works on both Claude Code and Cursor IDE:

1. **Skills**: write once using the standard format, place in both `.claude/skills/` and `.cursor/skills/` (or use symlinks)
2. **MCP servers**: write the config once, copy to both `.mcp.json` and `.cursor/mcp.json`
3. **Agents**: write once, copy to both `.claude/agents/` and `.cursor/agents/`
4. **Rules**: write separately for each tool (different formats)
5. **Hooks**: write separately for each tool (different event systems)

---

## 7. Security and Permissions

### Trust Model

Plugins execute arbitrary code with **your user privileges**. This means a malicious plugin could:
- Read/modify any file your user can access
- Execute any command you could run
- Access network resources
- Exfiltrate data

**Only install plugins from trusted sources.**

Anthropic does not verify third-party plugins. Only plugins with the "Anthropic Verified" badge have been reviewed.

### Plugin Subagent Restrictions

For security, plugin subagents have restricted capabilities compared to standalone agents:

| Feature | Standalone agent | Plugin subagent |
|---------|-----------------|-----------------|
| `hooks` | Supported | **Ignored** |
| `mcpServers` | Supported | **Ignored** |
| `permissionMode` | Supported | **Ignored** |

### Organization Lockdown

Administrators can restrict which marketplaces are allowed via `strictKnownMarketplaces` in managed settings:

```json
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/approved-plugins" },
    { "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
  ]
}
```

| Value | Effect |
|-------|--------|
| Not set | No restrictions — users can add any marketplace |
| `[]` (empty array) | Complete lockdown — no marketplaces allowed |
| List of sources | Only listed sources are allowed |

### Cache and Isolation

- Plugins are cached to `~/.claude/plugins/cache/` for security and verification
- Plugins **cannot reference files outside their directory** — use symlinks as a workaround if needed
- Persistent data is isolated per plugin in `~/.claude/plugins/data/{plugin-id}/`

---

## 8. CLI Commands Reference

### Plugin Management

| Command | Description |
|---------|-------------|
| `claude plugin install <name>@<marketplace> [--scope user\|project\|local]` | Install a plugin |
| `claude plugin uninstall <name> [--scope ...] [--keep-data]` | Remove a plugin |
| `claude plugin enable <name> [--scope ...]` | Enable a disabled plugin |
| `claude plugin disable <name> [--scope ...]` | Disable without removing |
| `claude plugin update <name> [--scope ...]` | Update to latest version |
| `claude plugin validate .` | Validate plugin structure |

### Marketplace Management

| Command | Description |
|---------|-------------|
| `/plugin marketplace add <source>` | Add a marketplace |
| `/plugin marketplace list` | List configured marketplaces |
| `/plugin marketplace update <name>` | Refresh marketplace index |
| `/plugin marketplace remove <name>` | Remove a marketplace |

### In-Session Commands

| Command | Description |
|---------|-------------|
| `/plugin` | Open the interactive plugin manager (Discover, Installed, Marketplaces, Errors) |
| `/reload-plugins` | Reload all active plugins without restarting |
| `/agents` | List and manage subagent configurations |
| `/skills` | List available skills |
| `/hooks` | View active hook configurations |
| `/mcp` | Manage MCP server connections |

### Development

| Command | Description |
|---------|-------------|
| `claude --plugin-dir ./my-plugin` | Load a local plugin for testing |
| `claude --plugin-dir ./a --plugin-dir ./b` | Load multiple local plugins |
| `claude --debug` | Start with debug output (shows plugin loading details) |

---

## 9. Best Practices

### Development Workflow

1. **Start standalone**: develop and test components in `.claude/` before packaging
2. **Test locally**: use `--plugin-dir` during development, `/reload-plugins` after changes
3. **Validate**: run `claude plugin validate .` before every release
4. **Version**: always bump `version` in `plugin.json` before distributing

### Design Guidelines

- **One plugin, one purpose**: a plugin should do one thing well. Don't bundle unrelated tools.
- **Write precise descriptions**: Claude uses skill and agent descriptions to decide when to invoke them. Vague descriptions = unused components.
- **Keep SKILL.md under 500 lines**: move detailed reference material to separate files in the skill directory
- **Limit tool access**: in skills and agents, grant only the tools needed (`allowed-tools`, `tools`). Don't give `Bash` access if the skill only needs `Read`.
- **Use environment variables**: always use `${CLAUDE_PLUGIN_ROOT}` for bundled files and `${CLAUDE_PLUGIN_DATA}` for runtime state
- **Document prerequisites**: if your plugin requires binaries (gopls, pyright, etc.), document this in README
- **Include a CHANGELOG**: users need to know what changed between versions
- **Test on a clean machine**: your development environment may have dependencies that users don't

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Putting components inside `.claude-plugin/` | Only `plugin.json` goes there. Everything else at plugin root. |
| Using absolute paths | All manifest paths must be relative (`./...`) |
| Forgetting to bump version | Users won't get updates due to caching |
| Overly broad tool permissions | Restrict with `allowed-tools` / `disallowedTools` |
| Missing `chmod +x` on scripts | Hook scripts must be executable |
| No description on skills/agents | Claude won't know when to use them |
| Giant monolithic SKILL.md | Split into SKILL.md + reference files |

---

*Document generated on March 21, 2026 — Sources: [code.claude.com/docs](https://code.claude.com/docs/en/plugins), [agentskills.io](https://agentskills.io)*
