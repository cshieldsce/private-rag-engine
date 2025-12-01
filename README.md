# PrivateDoc AI - Self-Hosted Edition

> **Your AI-powered document assistant that runs entirely on your infrastructure.**

PrivateDoc AI is a self-hosted Retrieval Augmented Generation (RAG) system that allows you to chat with your PDF documents using advanced AI, while maintaining complete control over your data.

---

## ✨ Why Use PrivateDoc AI?

### 🔒 **Complete Privacy**
- Your documents never leave your server
- No third-party storage or cloud uploads
- All processing happens locally on your infrastructure
- Only embeddings and queries are sent to OpenAI (not your full documents)

### 💰 **No Monthly Subscriptions**
- Pay only for OpenAI API usage (typically $0.01-0.10 per query)
- No platform fees or per-user charges
- No hidden costs or premium tiers
- Cancel anytime - you own the software

### 🏠 **You Own Your Data**
- Full control over your document database
- Easy backup and restore (just copy the `chroma_db/` folder)
- No vendor lock-in - export your data anytime
- Run on-premises or in your own private cloud

### 🚀 **Enterprise-Ready Features**
- Built with FastAPI for production workloads
- Docker containerization for easy deployment
- Persistent vector database (ChromaDB)
- Scalable architecture

---

## 📁 Project Structure

```
PrivateDoc-AI/
├── documents/              # Place your PDF files here
│   └── README.txt         # Instructions
├── src/                   # Application source code
│   ├── main.py           # FastAPI application
│   ├── ingest.py         # Document ingestion script
│   └── config.py         # Configuration management
├── chroma_db/            # Vector database (auto-created)
├── .env                  # Your API key (create from .env.example)
├── .env.example          # Template for environment variables
├── Dockerfile            # Container definition
├── docker-compose.yml    # Orchestration configuration
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── LICENSE              # MIT License
```

---

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop)
   - Windows 10/11, macOS 10.15+, or Linux
   - 4GB RAM minimum (8GB recommended)
   
2. **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
   - Cost: ~$0.01-0.10 per document query
   - Pay-as-you-go, no subscription required

---

## 🛠️ Setup Guide

### Step 1: Download Docker Desktop

1. Visit [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Download for your operating system
3. Install and start Docker Desktop
4. Verify installation:
   ```bash
   docker --version
   ```

### Step 2: Configure Your API Key

1. **Create the configuration file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and paste your OpenAI API key:**
   ```bash
   # Open .env in any text editor (Notepad, VS Code, etc.)
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
   ```

   **Where to find your API key:**
   - Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Copy and paste into `.env`

### Step 3: Launch PrivateDoc AI

**First-time setup (ingest your documents):**
```bash
# Place your PDF files in the documents/ folder first!
docker-compose --profile ingest up rag-ingest
```

Wait for: `✓ Successfully ingested X chunks into ChromaDB`

**Start the API server:**
```bash
docker-compose up -d
```

**Verify it's running:**
```bash
curl http://localhost:8000/health
```

You should see: `{"status":"healthy"}`

---

## 📖 How to Use PrivateDoc AI

### Adding Documents

1. **Place PDF files in the `documents/` folder:**
   ```
   PrivateDoc-AI/
   └── documents/
       ├── company-handbook.pdf
       ├── product-specs.pdf
       └── research-paper.pdf
   ```

2. **Run the ingestion process:**
   ```bash
   docker-compose --profile ingest up rag-ingest
   ```

3. **Documents are now searchable!** The system will:
   - Extract text from all PDFs
   - Split into 1000-character chunks
   - Create embeddings and store in ChromaDB
   - Make them available for AI queries

### Asking Questions

**Option 1: Using PowerShell (Windows)**
```powershell
$body = @{ query = "What are the key findings?" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/chat -Method POST -ContentType "application/json" -Body $body
```

**Option 2: Using curl (Linux/Mac/Git Bash)**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key findings in the research paper?"}'
```

**Option 3: Using Python**
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"query": "Summarize the product specifications"}
)

print(response.json()["answer"])
```

**Option 4: Using any HTTP client**
- Postman, Insomnia, Thunder Client, etc.
- POST to `http://localhost:8000/chat`
- Body: `{"query": "your question here"}`

**Response format:**
```json
{
  "answer": "Based on the documents, the key findings are...",
  "sources": [
    "/app/documents/research-paper.pdf",
    "/app/documents/product-specs.pdf"
  ]
}
```

---

## 🔄 Day-to-Day Operations

### Starting/Stopping the Service

**Start:**
```bash
docker-compose up -d
```

**Stop:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

### Adding New Documents

1. Copy new PDFs to `documents/` folder
2. Re-run ingestion:
   ```bash
   docker-compose --profile ingest up rag-ingest
   ```
3. New documents are now searchable (existing documents remain)

### Backing Up Your Data

**Backup the vector database:**
```bash
# Linux/Mac
tar -czf backup-$(date +%Y%m%d).tar.gz chroma_db/

# Windows (PowerShell)
Compress-Archive -Path chroma_db -DestinationPath backup-$(Get-Date -Format 'yyyyMMdd').zip
```

**Restore from backup:**
```bash
# Stop the service first
docker-compose down

# Extract backup
tar -xzf backup-20240115.tar.gz  # Linux/Mac
# OR
Expand-Archive backup-20240115.zip  # Windows

# Restart
docker-compose up -d
```

---

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'langchain.chains'"

**Problem:** LangChain dependencies not properly installed or outdated

**Solutions:**
1. Rebuild the Docker image:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

2. If still failing, check the build logs:
   ```bash
   docker-compose build --no-cache 2>&1 | tee build.log
   ```

### "401 Unauthorized" Error

**Problem:** API key not found or invalid

**Solutions:**
1. Check that `.env` file exists in the project root
2. Verify the file contains: `OPENAI_API_KEY=sk-...`
3. Ensure there are no extra spaces or quotes around the key
4. Test your API key at [platform.openai.com/playground](https://platform.openai.com/playground)
5. Restart the container:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### "No documents found" or Empty Results

**Problem:** Documents not ingested or ingestion failed

**Solutions:**
1. Verify PDFs are in `documents/` folder
2. Check PDF files aren't corrupted (try opening them manually)
3. Re-run ingestion with verbose logging:
   ```bash
   docker-compose --profile ingest up rag-ingest
   ```
4. Check logs for errors:
   ```bash
   docker-compose logs rag-ingest
   ```

### "no such column: collections.topic" Error

**Problem:** ChromaDB schema mismatch (database created with different version)

**Solution - Full Reset:**
```bash
# Stop all services
docker-compose down

# Delete the vector database (BACKUP FIRST if needed!)
# Windows PowerShell:
Remove-Item -Recurse -Force chroma_db

# Linux/Mac:
rm -rf chroma_db/

# Re-ingest documents with fresh database
docker-compose --profile ingest up rag-ingest

# Restart API
docker-compose up -d
```

**Alternative - Backup First:**
```powershell
# Windows - backup before deleting
Rename-Item chroma_db chroma_db.backup
docker-compose --profile ingest up rag-ingest
docker-compose up -d
```

### Port 8000 Already in Use

**Problem:** Another service is using port 8000

**Solution:** Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8000 to any available port
```

Then access at `http://localhost:8001`

### Docker Daemon Not Running

**Problem:** "Cannot connect to the Docker daemon"

**Solutions:**
1. Start Docker Desktop application
2. Wait 30 seconds for Docker to fully start
3. Verify with: `docker ps`

### Out of Memory Errors

**Problem:** Container crashes or slow performance

**Solutions:**
1. Close other applications
2. Increase Docker memory limit:
   - Docker Desktop → Settings → Resources
   - Set Memory to at least 4GB (8GB recommended)
3. Process fewer documents at once

### "Rate limit exceeded" from OpenAI

**Problem:** Too many API requests

**Solutions:**
1. Wait 60 seconds and retry
2. Check your OpenAI usage at [platform.openai.com/usage](https://platform.openai.com/usage)
3. Add payment method if on free tier
4. Reduce chunk size in `config.py` to lower costs

---

## 📊 Interactive API Documentation

Once running, visit: **http://localhost:8000/docs**

Features:
- Try all API endpoints interactively
- See request/response schemas
- Test queries without writing code

---

## 🔧 Advanced Configuration

Edit `src/config.py` or set environment variables in `.env`:

```bash
# Model selection (default: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# Chunk size for document splitting (default: 1000)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Number of chunks to retrieve per query (default: 3)
RETRIEVAL_TOP_K=3

# Database location
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

---

## 📈 Cost Estimation

**Typical costs with GPT-4o-mini:**
- Document ingestion: $0.001 per page
- Each query: $0.01 - $0.05
- 1000 queries/month: ~$10-50

**Cost-saving tips:**
- Use GPT-4o-mini (default) instead of GPT-4
- Reduce `RETRIEVAL_TOP_K` to 2 instead of 3
- Cache frequent queries in your application

---

## 🔐 Security Best Practices

1. **Never commit `.env` to version control**
   ```bash
   # Already in .gitignore
   ```

2. **Restrict network access:**
   - Run behind a firewall
   - Use reverse proxy (nginx) for HTTPS
   - Implement authentication layer if exposing externally

3. **Regular updates:**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

4. **Monitor API usage:**
   - Check OpenAI dashboard weekly
   - Set spending limits in OpenAI account

---

## 🆘 Support & Resources

- **Documentation:** [LangChain Docs](https://python.langchain.com/)
- **OpenAI API:** [platform.openai.com/docs](https://platform.openai.com/docs)
- **Docker Help:** [docs.docker.com](https://docs.docker.com/)

---

## 📄 License

MIT License - See LICENSE file for details.

This software is provided as-is for self-hosting. You are responsible for:
- OpenAI API usage and costs
- Compliance with OpenAI's usage policies
- Data privacy and security in your environment

---

## 🎯 Quick Reference Card

```bash
# First-time setup
cp .env.example .env                          # Configure API key
docker-compose --profile ingest up rag-ingest # Ingest documents
docker-compose up -d                          # Start API

# Daily operations
docker-compose logs -f                        # View logs
docker-compose restart                        # Restart service
docker-compose down                           # Stop service

# Adding documents
# 1. Copy PDFs to documents/
# 2. Run: docker-compose --profile ingest up rag-ingest

# Query the API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "your question"}'
```

---

**PrivateDoc AI** - Because your documents deserve privacy. 🔒