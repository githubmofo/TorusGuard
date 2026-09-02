# TG-AGENT-004: Persistent Memory & Cross-Session Information Leakage

## Severity
High. Storing unredacted sensitive session data, tokens, or personal information in long-term vector memory stores causes cross-session data leakage.

## Applies To
- Agent Long-Term Memory, RAG Vector Stores, ChromaDB, Pinecone, LangChain Memory
- Multi-Tenant AI Assistants & Support Bots

## Why It Matters
Autonomous agents increasingly use vector embeddings and episodic memory databases to remember user preferences across sessions. If multi-tenant agents store memories without tenant isolation:
1. User A's API tokens, medical history, or confidential notes can be indexed into vector search.
2. When User B queries the agent, vector similarity search can retrieve User A's private context and inject it into the prompt.

## What TorusGuard Looks For
1. Ingesting raw user messages containing credentials, tokens, or PII into persistent vector databases without automated secret scrubbing.
2. Vector database queries lacking mandatory `tenant_id` metadata filtering.
3. Cross-user shared memory caches in multi-user AI services.

## Unsafe Example
```python
# UNSAFE: Storing raw user messages in shared vector memory without tenant isolation
def save_agent_memory(vector_store, user_id: str, message: str):
    # Missing credential scrub & missing tenant namespace
    vector_store.add_texts(
        texts=[message],
        metadatas=[{"source": "chat"}] # Danger: Searchable across all users!
    )
```

## Safe Example
```python
# SAFE: Secret redaction and mandatory tenant metadata isolation
from core.runtime_evidence import mask_sensitive_data

def save_agent_memory(vector_store, tenant_id: str, user_id: str, message: str):
    # 1. Scrub credentials and tokens prior to indexing
    clean_message = mask_sensitive_data(message)
    
    # 2. Store with strict tenant metadata
    vector_store.add_texts(
        texts=[clean_message],
        metadatas=[{
            "tenant_id": tenant_id,
            "user_id": user_id,
            "source": "chat"
        }]
    )

def query_agent_memory(vector_store, tenant_id: str, query: str):
    # Mandatory tenant filter prevents cross-tenant memory leakage
    return vector_store.similarity_search(
        query,
        k=4,
        filter={"tenant_id": tenant_id}
    )
```

## Remediation
1. **Always Sanitize Before Storing:** Run credential masking over all text before saving to memory databases.
2. **Strict Tenant Filtering:** Enforce hard metadata filters (`filter={"tenant_id": ...}`) on every vector search query.
3. **Session Cleansing:** Provide users with clear commands to clear and audit persistent memory.

## Related Rules
- `TG-AGENT-001`: Prompt Injection in System Context Files
- `TG-DB-004`: Missing Tenant Query Isolation
- `TG-SEC-004`: Sensitive Logging
