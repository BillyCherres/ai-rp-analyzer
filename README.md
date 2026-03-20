# AI Research Paper Analyzer — Backend

A backend API for ingesting, indexing, and semantically querying academic research papers. Built as the foundation for an AI-powered research assistant capable of understanding and answering questions about scientific literature.

---

## What This Does

At its core, this system solves a fundamental problem with academic papers: they are long, dense, and difficult to query programmatically. Standard keyword search fails because the vocabulary in a question rarely matches the exact vocabulary in a paper. This backend addresses that by converting paper content into mathematical vector representations — embeddings — that encode semantic meaning rather than surface-level words.

The result is a system where a query like *"how do animals develop cultural behaviours"* will surface relevant passages about imitation, social learning, and group-specific behaviour in non-human primates, even if those exact words never appear in the query.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    FastAPI Backend                   │
│                                                     │
│  POST /papers/upload                                │
│       │                                             │
│       ▼                                             │
│  PDF Text Extraction (pypdf)                        │
│       │                                             │
│       ▼                                             │
│  Text Chunking (500-char sliding window)            │
│       │                                             │
│       ├──────────────────────┐                      │
│       ▼                      ▼                      │
│  SQLite (paper metadata   Embedding Model           │
│  + raw chunks)            (sentence-transformers)   │
│                              │                      │
│                              ▼                      │
│                           ChromaDB                  │
│                           (vector store)            │
│                                                     │
│  GET /papers/search?q=...                           │
│       │                                             │
│       ▼                                             │
│  Embed query → ChromaDB similarity search           │
│       │                                             │
│       ▼                                             │
│  Return top-k semantically matched chunks           │
└─────────────────────────────────────────────────────┘
```

---

## Stack

| Layer | Technology | Purpose |
|---|---|---|
| API Framework | FastAPI | REST API, request validation, async-ready |
| ORM | SQLAlchemy | Database models and session management |
| Migrations | Alembic | Schema versioning |
| Relational DB | SQLite | Stores paper metadata, raw content, chunks |
| PDF Parsing | pypdf | Text extraction from uploaded PDFs |
| Embedding Model | sentence-transformers (`all-MiniLM-L6-v2`) | Converts text to 384-dimensional vectors |
| Vector Store | ChromaDB | Stores and searches embeddings by cosine similarity |
| Frontend (planned) | TBD | Will consume this API |

The embedding model is intentionally isolated behind a single service module (`embedding_service.py`) to allow a clean swap to a hosted provider such as Google Gemini's embedding API when moving out of local development.

---

## Data Flow

### Ingestion (Upload)

1. PDF is uploaded via `POST /papers/upload`
2. Text is extracted page-by-page using `pypdf`
3. Extracted text is cleaned (collapsed whitespace, normalised line breaks)
4. Text is split into 500-character chunks — small enough to be semantically focused, large enough to carry context
5. The paper record (title, authors, abstract, content, chunks) is persisted to SQLite
6. Each chunk is passed through the embedding model, producing a 384-dimensional float vector
7. All chunk vectors are stored in ChromaDB with their `paper_id` as metadata, enabling per-paper filtering

### Querying (Semantic Search)

1. Query string is received at `GET /papers/search?q=`
2. Query is embedded using the same model — producing a vector in the same 384-dimensional space
3. ChromaDB performs a nearest-neighbour search using cosine similarity
4. The top 5 most semantically similar chunks are returned with their source `paper_id`

---

## Project Structure

```
app/
├── main.py                    # FastAPI app entry point
├── database.py                # SQLAlchemy engine and session
├── vector_store.py            # ChromaDB client and collection
├── models/
│   └── paper.py               # SQLAlchemy Paper model
├── schemas/
│   └── paper.py               # Pydantic request/response schemas
├── services/
│   ├── paper_service.py       # Paper CRUD + embedding orchestration
│   ├── pdf_service.py         # PDF text extraction and cleaning
│   ├── text_chuncker.py       # Text chunking logic
│   └── embedding_service.py   # Embedding model interface
└── api/
    └── routes/
        └── papers.py          # API route definitions
alembic/                       # Database migration files
requirements.txt
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/papers` | Create a paper record manually |
| `POST` | `/papers/upload` | Upload a PDF and auto-ingest |
| `GET` | `/papers` | List all papers |
| `GET` | `/papers/search?q=` | Semantic search across all chunks |
| `GET` | `/papers/{id}` | Get a single paper by ID |

---

## Setup

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

---

## Roadmap

- [x] PDF ingestion and text extraction
- [x] Text chunking
- [x] Semantic embeddings (local, sentence-transformers)
- [x] Vector storage and similarity search (ChromaDB)
- [ ] RAG — retrieval-augmented generation (answer questions using retrieved chunks + LLM)
- [ ] Swap local embeddings for hosted provider (Google Gemini)
- [ ] Multi-paper search and cross-paper reasoning
- [ ] Structured metadata extraction (authors, abstract, citations)
