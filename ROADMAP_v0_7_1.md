# TorusGuard v0.7.1+ Development Roadmap & Improvement Backlog

This backlog outlines prioritized enhancements, rule family expansions, and architecture upgrades derived directly from the v0.0.0–v0.7.0 full-system validation audit.

---

## 📋 Prioritized Backlog Items

### 1. PatchGovernor Content-Aware Keyword Escalation
- **Description:** Extend `PatchGovernor.evaluate_diff()` to scan added and modified unified diff lines for sensitive domain keywords, rather than inspecting file paths alone.
- **Motivation:** Resolves known validation check gap in `validate_v0_6_1_scale.py` where edits in files with generic names (e.g., `views.py`) touching authentication functions (`old_auth()`, `new_auth()`) bypass high-risk review escalation.
- **Priority:** 🔴 **High**

### 2. `TG-AGENT-*` Rule Family for Agentic AI Systems
- **Description:** Introduce specialized security rules targeting agentic AI architectures (Hermes, AutoPentest-AI, LangChain, MCP servers).
  - `TG-AGENT-001`: Direct/Indirect Prompt Injection in System Context Files.
  - `TG-AGENT-002`: Unsafe Tool Dispatch & Shell Command Execution without Sandboxing.
  - `TG-AGENT-003`: Overly Broad Model Context Protocol (MCP) Tool Scoping & Credential Access.
  - `TG-AGENT-004`: Persistent Memory & Cross-Session Information Leakage.
- **Motivation:** Enables TorusGuard to audit agentic reasoning frameworks, tool execution backends, and MCP server implementations with first-class rules.
- **Priority:** 🔴 **High**

### 3. Runtime Probing for GraphQL and WebSockets
- **Description:** Extend `ExploitChecker` and `WebValidator` to support bounded query complexity introspection, depth limit checks, and WebSocket handshake/channel authorization assertions.
- **Motivation:** Closes the gap between static detection (`TG-GQL-*`, `TG-WS-*`) and runtime exploitability confirmation for modern real-time and GraphQL web services.
- **Priority:** 🟠 **Medium**

### 4. Deeper Container & Supply Chain Build-Chain Analysis
- **Description:** Model multi-stage Docker build layers to detect build-time secret persistence, layer caching leaks, and container execution privileges across `compose.yaml` configurations.
- **Motivation:** Strengthens container security detection beyond simple single-stage Dockerfile inspection.
- **Priority:** 🟠 **Medium**

### 5. CI/CD Permission Modeling & OIDC Security
- **Description:** Analyze GitHub Actions workflow permissions (`permissions: write-all` vs least privilege), OIDC trust policies, and runner isolation boundaries.
- **Motivation:** Prevents lateral compromise from supply chain dependencies into production cloud credentials.
- **Priority:** 🟠 **Medium**

### 6. Duplex WebSocket & Webhook Replay Handshakes
- **Description:** Implement bidirectional message state-machine recording and replay in `ReplayManager` for interactive event-driven architectures.
- **Motivation:** Ensures deterministic replay trace verification for streaming and asynchronous web application components.
- **Priority:** 🟡 **Low**

### 7. Headless Chromium Sandbox Integration
- **Description:** Containerize headless browser verification drivers inside a bounded Docker execution sandbox for visual regression and DOM inspection.
- **Motivation:** Isolates client-side route guard verification from local agent host environments.
- **Priority:** 🟡 **Low**

---

## 🎯 Target Release Milestones

| Milestone | Target Window | Primary Focus |
|:---:|:---:|---|
| **v0.7.1** | Q4 2026 | PatchGovernor diff content escalation, `TG-AGENT-001` through `TG-AGENT-004` rule definitions. |
| **v0.7.2** | Q1 2027 | GraphQL & WebSocket runtime validation, multi-stage Dockerfile layer inspection. |
| **v0.8.0** | Q2 2027 | Full agentic MCP security evaluation suite, sandboxed browser replay engine. |
