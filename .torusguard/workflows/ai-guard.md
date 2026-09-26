# /torusguard-ai-guard — AI Application & RAG Pipeline Guard

$ARGUMENTS

---

## Objective
Detect and remediate prompt injection, unsandboxed autonomous tool executions, and cross-tenant vector contamination across AI agent and RAG architectures.

---

## Tri-Mode Parity
- **Mode A (Terminal CLI):** `torusguard ai-guard [target]`
- **Mode B (AI Chat Slash Command):** `/torusguard ai-guard [target]`
- **Mode C (Native MCP Tool):** `torusguard_ai_guard`

---

## Execution Steps

1. **Discover LLM & Agent Call Sites:** Locate AI framework usage (OpenAI, Anthropic, LangChain, LlamaIndex, Vercel AI SDK).
2. **Audit Prompt Templates:**
   - Detect raw user string concatenation into system instructions (`TG-AGENT-001`).
   - Flag raw document chunk ingestion in RAG without inert delimiters (`TG-RAG-002`).
3. **Audit Tool Registry & Dispatchers:**
   - Check for unsandboxed shell, file, or database tool calls lacking Human Gates (`TG-AGENT-002`).
   - Enforce Zod/Pydantic schema validation on all tool argument payloads (`TG-AGENT-003`).
4. **Audit Vector Store Queries:**
   - Assert all similarity searches (`pgvector`, `pinecone`, `qdrant`, `chroma`) include tenant/user metadata filters (`TG-RAG-001`).
   - Flag ingestion of unvalidated external document payloads (`TG-RAG-003`).
5. **Formulate Patches & Synchronize:** Propose surgical fixes and record findings in `security_report.md`.
