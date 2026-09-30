# TorusGuard Threat Model Workflow (`/torusguard threatmodel`)

## Purpose
Synthesizes architectural STRIDE threat models, interactive Mermaid Data Flow Diagrams (DFDs), and trust boundary registers directly into `SECURITY_THREAT_MODEL.md`.

## Steps
1. Execute `torusguard threatmodel` or native MCP tool `torusguard_threatmodel`.
2. Inspect `SECURITY_THREAT_MODEL.md` to verify identified entrypoints, data stores, and trust boundaries.
3. Align STRIDE risk controls against corresponding TorusGuard security invariants (`TG-AUTH`, `TG-DB`, `TG-RATE`, `TG-SSRF`).
