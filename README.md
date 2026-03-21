# AI Research Paper Analyzer — Backend

A learning project to explore RAG (Retrieval-Augmented Generation), vector databases, and the building blocks of single-agent AI systems — using research papers as the data source.

---

## Architecture

```
Client
  │
  └─ sends PDF
        │
        ▼
  FastAPI endpoint
        │
        ▼
  chunked into text segments
        │
        ▼
  vector embedded (sentence-transformers)
        │
        ▼
  stored in ChromaDB

  Query
  │
  └─ vector embedded
        │
        ▼
  ChromaDB similarity search
        │
        ▼
  top chunks → RAG prompt → Gemini
        │
        ▼
  answer returned to client
```

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| ORM / Migrations | SQLAlchemy + Alembic |
| Database | SQLite |
| PDF Parsing | pypdf |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Store | ChromaDB |
| LLM | Google Gemini 2.5 Flash |

---

## Data Flow

### Upload

1. PDF uploaded → text extracted page-by-page
2. Text split into 500-character chunks
3. Paper metadata and chunks saved to SQLite
4. Each chunk embedded → vectors stored in ChromaDB

### Search

1. Query embedded into the same vector space
2. ChromaDB returns top 5 most similar chunks

### Ask (RAG)

1. Question embedded → top 5 chunks retrieved
2. Chunks injected into a grounded prompt
3. Gemini answers using only the provided context

---

## Roadmap

- [x] PDF ingestion and text extraction
- [x] Text chunking
- [x] Semantic embeddings (local, sentence-transformers)
- [x] Vector storage and similarity search (ChromaDB)
- [x] RAG pipeline — retrieval-augmented generation via Google Gemini 2.5 Flash
- [ ] Multi-agent router — classify question type and route to the appropriate agent
- [ ] Summarization agent — full paper summarization
- [ ] Swap local embeddings for hosted provider (Google Gemini embedding API)
- [ ] Multi-paper search and cross-paper reasoning
- [ ] Structured metadata extraction (authors, abstract, citations)
