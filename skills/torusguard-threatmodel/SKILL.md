---
name: torusguard-threatmodel
description: Synthesizes an architectural STRIDE threat model, interactive Mermaid Data Flow Diagram (DFD), and trust boundary register into SECURITY_THREAT_MODEL.md.
tools: Read, Grep, Glob, Bash, Edit, Write
version: 2.1.2
last-updated: 2026-09-30
skills:
  - torusguard
  - torusguard-audit
---

# TorusGuard Threat Model — STRIDE & DFD Synthesizer

TorusGuard Threat Model automatically maps routes, trust boundaries, datastores, and egress sinks to construct an architectural Data Flow Diagram and formal STRIDE threat model.

## Invocation

- **Mode A (Terminal CLI):** `torusguard threatmodel`
- **Mode B (AI Chat Slash Command):** `/torusguard threatmodel` or `/torusguard-threatmodel`
- **Mode C (Native MCP Tool):** `torusguard_threatmodel(target=".")`

## Core Capabilities

1. **Automated DFD Generation:** Renders interactive Mermaid diagram showing Zones 1–4 (Clients, Gateways, Core Services, Datastores).
2. **STRIDE Risk Ledger:** Evaluates threats across Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.
3. **Multi-Modal Vision Integration:** Discovers architectural diagrams and verifies that visual trust boundaries match code execution paths.
4. **Living Compliance Artifact:** Emits `SECURITY_THREAT_MODEL.md` at workspace root.
