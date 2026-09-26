# TG-RAG-003: Unpartitioned Vector Database Tenant Lookup

## Severity
High. Executing similarity searches across vector databases without multi-tenant metadata filters leaks private organization or user documents across tenant boundaries.

## Applies To
- Vector Databases: Pinecone, Qdrant, Chroma, Weaviate, Milvus, pgvector
- RAG applications with multi-tenant users or workspaces

## Why It Matters
Vector embeddings from different tenants exist in the same high-dimensional embedding space. If an embedding lookup only searches by cosine similarity without an explicit `filter={"tenant_id": user.tenant_id}` or namespace partition, queries from User A will return private embeddings, contracts, or records belonging to User B.

## What TorusGuard Looks For
1. Vector similarity searches lacking metadata filter arguments (e.g. `index.query(vector=..., top_k=5)` with no `filter`).
2. Missing tenant partitioning in vector retrieval endpoints.

## Unsafe Example
```python
# UNSAFE: Vector similarity search across all tenants
def search_knowledge_base(user: User, query_vector: list[float]):
    results = pinecone_index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True
        # MISSING tenant filter!
    )
    return results
```

## Safe Example
```python
# SAFE: Mandatory tenant scoping in metadata filter
def search_knowledge_base(user: User, query_vector: list[float]):
    results = pinecone_index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True,
        filter={
            "tenant_id": {"$eq": user.tenant_id}
        }
    )
    return results
```

## Remediation
1. Always scope vector similarity queries by tenant ID in the metadata filter.
2. In pgvector, enforce row-level security (RLS) or explicit `WHERE tenant_id = :tenant_id` clauses on embedding queries.

## Related Rules
- `TG-DB-001`: Missing Tenant Query Isolation
- `TG-RAG-001`: Untrusted RAG Context Injection
