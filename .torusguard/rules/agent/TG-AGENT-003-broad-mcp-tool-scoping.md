# TG-AGENT-003: Overly Broad MCP Tool Scoping & Credential Access

## Severity
High. Granting Model Context Protocol (MCP) servers or autonomous agents unbounded filesystem or database access violates the principle of least privilege.

## Applies To
- Model Context Protocol (MCP) Configurations (`mcp_config.json`, `.agent/mcp.json`)
- AI Coding Agent Plugins & Tool Connectors

## Why It Matters
MCP servers bridge LLMs to local filesystems, git repositories, and external APIs. When MCP configurations grant broad root filesystem access (`/`) or pass unrestricted service-role database keys:
1. A compromised or hallucinating agent can read SSH keys, browser cookies, and bash histories.
2. Destructive SQL operations (`DROP TABLE`, `DELETE FROM`) can be triggered through tool calls without human confirmation.

## What TorusGuard Looks For
1. MCP server configurations mounting root directories (`/`, `C:\`, `~`) instead of project-specific subdirectories.
2. Unrestricted write and delete permissions on production databases passed to agent tools.
3. Lack of Human-in-the-Loop confirmation gates for destructive actions.

## Unsafe Example
```json
// UNSAFE: MCP configuration granting full user home directory access
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"]
    }
  }
}
```

## Safe Example
```json
// SAFE: Least privilege directory scoping restricted to active project workspace
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./src", "./docs"]
    }
  }
}
```

## Remediation
1. **Scope to Project Root:** Restrict filesystem MCP servers to explicit project workspaces. Never mount user home directories or sensitive system paths.
2. **Read-Only by Default:** Configure tools with read-only modes unless write access is explicitly justified.
3. **Human Gate for Destructive Actions:** Require explicit user approval before executing file deletions or destructive database queries.

## Related Rules
- `TG-AGENT-002`: Unsafe Tool Dispatch & Shell Execution without Sandboxing
- `TG-SEC-001`: Hardcoded Secrets
