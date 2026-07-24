# RAG Pipeline Patterns — Production Architectures

## Pattern 1: Naive RAG (Baseline)

```
Query → Embed → Vector Search (top-k) → LLM Generation → Answer
```

**When to use:** Prototypes, < 100 docs, simple factual questions.
**Limitations:** No re-ranking. Retrieves by similarity, not relevance. Citations may be wrong.

```python
# Minimum viable RAG
from openai import OpenAI
client = OpenAI()

def naive_rag(query, documents, top_k=5):
    # Embed query
    q_embed = client.embeddings.create(model="text-embedding-3-small", input=query)
    # Retrieve (assumes pre-embedded docs)
    results = vector_store.search(q_embed.data[0].embedding, top_k=top_k)
    # Generate
    context = "\n\n".join([r.content for r in results])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system", 
            "content": f"Answer using only this context:\n{context}"
        }, {
            "role": "user",
            "content": query
        }]
    )
    return response.choices[0].message.content
```

## Pattern 2: RAG with Re-Ranking

```
Query → Embed → Vector Search (top-20) → Cross-Encoder Re-Rank → Top-5 → LLM → Answer
```

**When to use:** Production RAG (>100 docs, accuracy matters).
**Key insight:** Vector search returns neighbors, not answers. Re-ranking filters the top-20 to find the 5 truly relevant chunks.

```python
from cohere import Client
co = Client()

def rag_with_rerank(query, documents, top_k=20, rerank_k=5):
    q_embed = embed(query)
    candidates = vector_store.search(q_embed, top_k=top_k)
    
    # Re-rank with cross-encoder
    reranked = co.rerank(
        query=query,
        documents=[c.content for c in candidates],
        top_n=rerank_k,
        model="rerank-english-v3.0"
    )
    
    context = "\n\n".join([candidates[r.index].content for r in reranked.results])
    return generate(query, context)
```

## Pattern 3: RAG with Query Transformation

```
User Query → Query Rewriting/Decomposition → Multiple Retrievals → Fusion → LLM → Answer
```

**When to use:** Complex multi-part questions, long documents, multi-hop reasoning.

Query transformations:
- **HyDE:** Generate hypothetical answer → embed THAT → retrieve similar docs
- **Multi-query:** Generate 3 variant queries → retrieve for each → fuse results
- **Step-back:** Abstract the question → retrieve broad context → narrow with specific query
- **Decomposition:** Break into sub-questions → answer each → synthesize

## Pattern 4: Agentic RAG

```
Query → Agent decides: retrieve/search/web/calculate → Tool execution → 
Observe → Decide next action → ... → Final answer with citations
```

**When to use:** Multi-source retrieval (docs + API + database), conditional retrieval paths, self-correcting retrieval.

## Retrieval Quality Benchmarks

| Pattern | recall@5 | Recall@10 | Latency (ms) | Cost/query |
|---------|---------|-----------|-------------|------------|
| Naive RAG | 0.72 | 0.81 | 200 | $0.002 |
| + Re-rank | 0.91 | 0.95 | 400 | $0.004 |
| + Query transform | 0.94 | 0.97 | 600 | $0.006 |
| Agentic RAG | 0.96 | 0.98 | 1200 | $0.015 |

**Choose:** Naive for prototypes. Re-rank for production. Query transform for complex queries. Agentic only when multi-source retrieval is required.
