# PrivateDoc AI (Student Project)

A minimal self-hosted RAG (Retrieval Augmented Generation) prototype. It ingests PDF files, stores text chunks with embeddings (ChromaDB), and answers questions using OpenAI.

## 1. Requirements
- Docker Desktop
- OpenAI API key (`OPENAI_API_KEY` in `.env`)

## 2. Project Structure
```
private-rag-engine/
├── documents/        # Put PDFs here
├── chroma_db/        # Auto-created vector store
├── src/              # FastAPI + ingestion scripts
├── .env.example
└── docker-compose.yml
```

## 3. First-Time Setup
```bash
cp .env.example .env
# edit .env and add OPENAI_API_KEY=sk-...
docker-compose --profile ingest up rag-ingest   # build + ingest PDFs
docker-compose up -d                            # start API
curl http://localhost:8000/health               # should return healthy
```

## 4. Adding / Re-ingesting Documents
1. Place new PDFs in `documents/`
2. Re-run:
```bash
docker-compose --profile ingest up rag-ingest
```

## 5. Ask Questions
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"Summarize the handbook"}'
```
Response contains `answer` and `sources`.

Python:
```python
import requests
r = requests.post("http://localhost:8000/chat", json={"query": "Key points?"})
print(r.json()["answer"])
```

## 6. Common Commands
```bash
docker-compose up -d        # start
docker-compose down         # stop
docker-compose logs -f      # tail logs
docker-compose restart      # restart
```

## 7. Basic Configuration (.env or environment)
```
OPENAI_MODEL=gpt-4o-mini
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_TOP_K=3
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 8. Backup / Reset
Backup:
```bash
tar -czf chroma_backup.tar.gz chroma_db/
```
Reset (will require re-ingest):
```bash
docker-compose down
rm -rf chroma_db/
docker-compose --profile ingest up rag-ingest
```

## 9. Minimal Troubleshooting
- Empty answers: re-ingest; check PDFs open normally.
- 401 errors: confirm `OPENAI_API_KEY` in `.env`.
- Port conflict: change `8000` mapping in `docker-compose.yml`.
- Schema errors: delete `chroma_db/` and re-ingest.

## 10. Notes
- Educational prototype, not production hardened.
- Do not commit `.env`.
- Costs depend on number of queries and pages.

## 11. API Docs
Browse: http://localhost:8000/docs

Done.