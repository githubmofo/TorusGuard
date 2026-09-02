# TG-AGENT-002: Unsafe Tool Dispatch & Shell Execution without Sandboxing

## Severity
Critical. Autonomous execution of unsandboxed shell commands or arbitrary file writes based on model outputs allows complete host compromise.

## Applies To
- Agentic Tool Executors, MCP Tools, Auto-GPT, ReAct Loops
- Python `subprocess`, Node.js `child_process`, Docker API

## Why It Matters
AI agents equipped with code execution or terminal tools often evaluate raw model strings. If an agent executes commands directly in the host environment:
1. An attacker can prompt-inject the model into invoking `rm -rf /`, exfiltrating environment variables, or installing backdoors.
2. Shell metacharacters (`;`, `&&`, `|`, `` ` ``) enable command injection through tool arguments.

## What TorusGuard Looks For
1. Invoking `subprocess.run(shell=True)` or `child_process.exec()` with LLM-generated arguments.
2. Direct terminal execution without containerization, seccomp, or read-only volume boundaries.
3. Lack of a strict allowlist of permitted CLI commands and argument schemas.

## Unsafe Example
```python
# UNSAFE: Executing LLM tool call directly in host shell with shell=True
import subprocess

def execute_agent_tool(tool_name: str, command: str):
    if tool_name == "run_command":
        # Remote code execution hazard!
        return subprocess.check_output(command, shell=True, text=True)
```

## Safe Example
```python
# SAFE: Command allowlist, strict parsing, and containerized sandboxing
import shlex
import subprocess

ALLOWED_COMMANDS = {"git status", "pytest", "npm test", "ruff check"}

def execute_agent_tool(command_line: str) -> str:
    # 1. Reject shell syntax
    args = shlex.split(command_line)
    if not args:
        raise ValueError("Empty command")
        
    cmd_base = args[0]
    if cmd_base not in {"git", "pytest", "npm", "ruff"}:
        raise PermissionError(f"Command '{cmd_base}' is not in approved tool allowlist")

    # 2. Execute without shell=True in isolated sandbox directory
    result = subprocess.run(
        args,
        shell=False,
        capture_output=True,
        text=True,
        timeout=30,
        cwd="/sandbox"
    )
    return result.stdout
```

## Remediation
1. **Never use `shell=True`:** Always parse arguments with `shlex.split` and execute as a list of strings.
2. **Strict Command Allowlist:** Define explicit allowlists of permitted binaries and subcommands.
3. **Sandbox Execution:** Run all tool commands inside an ephemeral Docker container or MicroVM with non-root user, dropped capabilities, and read-only host mounts.

## Related Rules
- `TG-AGENT-001`: Prompt Injection in System Context Files
- `TG-AGENT-003`: Overly Broad MCP Tool Scoping
