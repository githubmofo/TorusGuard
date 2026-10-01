# 📦 Option 1: npm & npx Installation & Usage Guide

> **TorusGuard** is an autonomous security guardrail and governed remediation engine.  
> It is distributed via npm as an executable **Command-Line Interface (CLI)** and **Model Context Protocol (MCP)** server, not a runtime JavaScript library.

---

## ⚡ Quick Decision: Which npm method should you use?

| Method | Command | When to Use | Execution |
| :--- | :--- | :--- | :--- |
| **1. Direct NPX** *(Recommended)* | `npx torusguard init` | Fastest setup, zero installation footprint | `npx torusguard <cmd>` |
| **2. Global Install** | `npm install -g torusguard` | Available anywhere in terminal as `torusguard` | `torusguard <cmd>` |
| **3. Local Project Install** | `npm install -D torusguard` | Pinned team dependency in `package.json` | `npx torusguard <cmd>` or `npm run` |

---

## Method 1: Direct NPX Execution (Zero Install — Recommended)

You do **not** need to install anything before running TorusGuard. Node.js comes with `npx`, which downloads and runs the latest published package directly from the npm registry:

### 1. Initialize your project
Open a terminal in your project's root directory and run:

```bash
npx torusguard init
```

To ensure you always pull the newest release and bypass any local npm cache:

```bash
npx torusguard@latest init
```

### 2. What happens during `init`
- Discovers your project stack (Go, TypeScript, Python, Java, PHP, Rust, etc.).
- Scaffolds a clean `.torusguard/` governance workspace in your project root.
- Unpacks 88 security rules across 22 architectural families.
- Automatically connects to existing IDE configurations (Cursor, Claude Code, Windsurf, Copilot, AGENTS.md).
- **Zero unwanted folders:** Creates **only** `.torusguard/`.

### 3. Run security commands via npx
All TorusGuard commands run seamlessly through `npx`:

```bash
# Check security posture & active rules
npx torusguard status

# Run full AST security audit
npx torusguard audit

# Formulate surgical Ponytail-bounded patches
npx torusguard harden

# Apply patches with automatic pre-apply rollback snapshots
npx torusguard apply

# Generate visual dark-mode HTML dashboard
npx torusguard report --html

# Export OASIS SARIF v2.1.0 for GitHub Security
npx torusguard report --sarif

# Interactive help guide
npx torusguard help
```

---

## Method 2: Global Installation (`npm install -g torusguard`)

If you want the `torusguard` command available in any terminal or directory without typing `npx`:

### 1. Install globally
```bash
npm install -g torusguard
```

*(On Linux or macOS, you may need `sudo npm install -g torusguard` depending on your npm setup).*

### 2. Verify installation
```bash
torusguard --version
# Output: torusguard v2.1.3
```

### 3. Use directly anywhere
Navigate to any project directory:

```bash
cd /path/to/my-project

# Initialize workspace
torusguard init

# Run security audit
torusguard audit

# View diagnostic status
torusguard status
```

### 4. Updating the global installation
TorusGuard includes a built-in auto-updater:

```bash
# Check for newer versions on the npm registry
torusguard update

# Automatically upgrade to the latest version
torusguard update --install
```

Or manually:
```bash
npm install -g torusguard@latest
```

---

## Method 3: Local Project Installation (`npm install torusguard`)

When you run `npm install torusguard` or `npm install -D torusguard` in your project:

```bash
npm install -D torusguard
```

### Understanding where the files go
1. **The files live in `node_modules/torusguard/`**: npm installs the package code into your project's `node_modules/` folder.
2. **The CLI binary is symlinked to `node_modules/.bin/torusguard`**: npm automatically links the binary in `node_modules/.bin/`.
3. **You do NOT import it in JavaScript code**: TorusGuard is a security enforcement engine, not a library like `lodash` or `express`.

### How to execute TorusGuard when locally installed:

#### Way A: Using `npx` (Simplest)
When inside a directory with `node_modules`, `npx` automatically finds and runs the local binary from `node_modules/.bin/`:

```bash
npx torusguard init
npx torusguard audit
npx torusguard status
```

#### Way B: Adding npm scripts in `package.json` (Recommended for Teams)
Add TorusGuard lifecycle scripts to your project's `package.json`:

```json
{
  "scripts": {
    "security:init": "torusguard init",
    "security:audit": "torusguard audit",
    "security:status": "torusguard status",
    "security:harden": "torusguard harden",
    "security:report": "torusguard report --html",
    "security:ci": "torusguard audit && torusguard report --sarif"
  },
  "devDependencies": {
    "torusguard": "^2.1.3"
  }
}
```

Now any developer or CI runner on your team can run:

```bash
npm run security:audit
npm run security:status
npm run security:report
```

#### Way C: Direct binary execution
You can directly call the executable from your shell:

- **Linux / macOS:**
  ```bash
  ./node_modules/.bin/torusguard audit
  ```
- **Windows (PowerShell):**
  ```powershell
  .\node_modules\.bin\torusguard audit
  ```
- **Windows (Command Prompt):**
  ```cmd
  node_modules\.bin\torusguard audit
  ```

---

## 🤖 Using with AI IDEs (Cursor, Claude Code, Antigravity, Windsurf)

Once you initialize your workspace with `npx torusguard init` or `torusguard init`:

1. **AI Chat Slash Commands:**
   In your AI IDE chat, invoke:
   - `/torusguard` — Master security orchestrator
   - `/torusguard audit` — Execute static AST scan
   - `/torusguard harden` — Formulate surgical Ponytail-bounded patches
   - `/torusguard status` — View diagnostic posture

2. **Native MCP Server:**
   Connect TorusGuard directly to agents supporting the Model Context Protocol:
   ```json
   {
     "mcpServers": {
       "torusguard": {
         "command": "npx",
         "args": ["-y", "torusguard", "mcp"]
       }
     }
   }
   ```
   Or if installed globally:
   ```json
   {
     "mcpServers": {
       "torusguard": {
         "command": "torusguard",
         "args": ["mcp"]
       }
     }
   }
   ```

---

## 🛠️ Troubleshooting & FAQs

### Q1: `npm i torusguard` gave me an older version or `npx` ran an old version
**Cause:** npm or npx often caches downloaded packages locally on disk (`~/.npm/_npx` or `%LocalAppData%\npm-cache\_npx`).  
**Fix:** Explicitly specify `@latest` to bypass the cache:
```bash
npx torusguard@latest init
```
Or clear your local npx cache:
```bash
# Force npx to ignore local cache
npx --ignore-existing torusguard@latest status

# Or clean npm cache
npm cache clean --force
```

### Q2: How do I verify which version is currently running?
```bash
npx torusguard --version
# Expected: torusguard v2.1.3
```

### Q3: Why does `init` create only `.torusguard/`?
Starting in **v2.1.3**, TorusGuard enforces strict zero-clutter initialization. All governance assets, rules, and scripts are stored entirely within `.torusguard/`. No extra `.agent/` or `.agents/` folders are generated.

---

## 📚 Related Documentation
- [Option 2: Build from Source Guide](option-2-source.md)
- [Option 3: Go Install Guide](option-3-go-install.md)
- [System Architecture](../../README.md#-autonomous-architecture--workflow)
