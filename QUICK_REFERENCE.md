# Quick Reference Guide

## Essential Commands

### Start Everything

```bash
docker-compose up --build
```

### Stop Everything

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Clean Start (Remove All Data)

```bash
docker-compose down -v
docker-compose up --build
```

## Important URLs

| Service      | URL                             | Description         |
| ------------ | ------------------------------- | ------------------- |
| Frontend     | http://localhost:3000           | Chat interface      |
| Backend API  | http://localhost:8000           | REST API            |
| API Docs     | http://localhost:8000/docs      | Swagger UI          |
| Qdrant       | http://localhost:6333/dashboard | Vector DB dashboard |
| Health Check | http://localhost:8000/health    | Backend status      |

## Environment Variables

Create `.env` file in root directory:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## Common Tasks

### Re-ingest Website Data

```bash
docker-compose exec backend python -m app.ingest_data
```

### Access Database

```bash
docker-compose exec backend sqlite3 /app/data/chatbot.db
```

### View All Conversations

```sql
sqlite3 backend/data/chatbot.db "SELECT * FROM conversations;"
```

### View Query Logs

```sql
sqlite3 backend/data/chatbot.db "SELECT * FROM query_logs ORDER BY timestamp DESC LIMIT 10;"
```

### Check Container Status

```bash
docker-compose ps
```

### Remove Specific Container

```bash
docker-compose rm -f backend
docker-compose up -d backend
```

## File Locations

### Backend

- Main app: `backend/app/main.py`
- Configuration: `backend/app/core/config.py`
- RAG service: `backend/app/services/langchain_rag.py`
- Security: `backend/app/core/security.py`
- Database: `backend/data/chatbot.db`

### Frontend

- Main page: `frontend/src/app/page.tsx`
- Components: `frontend/src/components/`
- API client: `frontend/src/lib/api.ts`
- Store: `frontend/src/lib/store.ts`

## Configuration Options

Edit `backend/app/core/config.py`:

| Setting              | Default       | Description                        |
| -------------------- | ------------- | ---------------------------------- |
| CHUNK_SIZE           | 1000          | Text chunk size for embeddings     |
| CHUNK_OVERLAP        | 200           | Overlap between chunks             |
| TOP_K_RESULTS        | 5             | Number of similar docs to retrieve |
| SIMILARITY_THRESHOLD | 0.7           | Minimum similarity score           |
| OPENAI_MODEL         | gpt-3.5-turbo | LLM model to use                   |

## Troubleshooting Quick Fixes

### Backend won't start

```bash
docker-compose logs backend | tail -50
# Check for OPENAI_API_KEY error
```

### Frontend can't connect

```bash
# Check backend is running
curl http://localhost:8000/health
```

### No responses from chatbot

```bash
# Check Qdrant has data
curl http://localhost:6333/collections/zibtek_docs
```

### Port already in use

```bash
# Find process using port 3000
lsof -ti:3000 | xargs kill -9

# Or change ports in docker-compose.yml
```

### Clear all data and restart fresh

```bash
docker-compose down -v
rm -rf backend/data/*.db
docker-compose up --build
```

## API Endpoints Reference

### Chat

```bash
# Send message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "123", "message": "What is Zibtek?"}'

# Create conversation
curl -X POST http://localhost:8000/api/chat/new \
  -H "Content-Type: application/json" \
  -d '{"title": "New Chat"}'
```

### Conversations

```bash
# List all
curl http://localhost:8000/api/chat/conversations

# Get specific conversation
curl http://localhost:8000/api/chat/conversations/123

# Delete conversation
curl -X DELETE http://localhost:8000/api/chat/conversations/123
```

## Development Mode

### Backend Local Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.template .env
# Edit .env
uvicorn app.main:app --reload
```

### Frontend Local Development

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## Performance Monitoring

### Check Docker Resource Usage

```bash
docker stats
```

### Check Backend Memory

```bash
docker-compose exec backend ps aux
```

### Monitor Logs in Real-time

```bash
docker-compose logs -f --tail=100
```

## Security Checklist

- [ ] OpenAI API key is in `.env`, not committed to git
- [ ] `.env` file is in `.gitignore`
- [ ] CORS origins are properly configured
- [ ] Production deployment uses HTTPS
- [ ] Database has proper backup strategy

## Version Information

- FastAPI: 0.109.0
- LangChain: 0.1.4
- Next.js: 14.1.0
- Qdrant: Latest (Docker image)
- Python: 3.11
- Node: 18

## Support Contacts

For technical issues, refer to:

- README.md - Detailed documentation
- SETUP.md - Setup instructions
- TESTING.md - Testing guide

