# Zibtek AI Chatbot

An AI-powered chatbot that answers queries exclusively based on Zibtek's website content using RAG (Retrieval-Augmented Generation), LangChain, Qdrant vector database, and OpenAI models.

## Features

- ✅ **Custom Data Integration**: Responds only using Zibtek website data
- ✅ **Multi-turn Conversations**: Maintains conversation history with context
- ✅ **Conversation Management**: Create new chats, load old conversations from sidebar
- ✅ **Prompt Injection Protection**: Prevents manipulation of chatbot behavior
- ✅ **Out-of-Scope Handling**: Politely rejects questions unrelated to Zibtek
- ✅ **Comprehensive Logging**: All queries and responses logged in SQLite
- ✅ **Modern UI**: Clean, responsive Next.js frontend with Tailwind CSS
- ✅ **Docker Deployment**: Fully containerized setup with Docker Compose

## Tech Stack

### Backend

- **FastAPI**: High-performance Python web framework
- **LangChain**: RAG pipeline and conversation management
- **Qdrant**: Vector database for semantic search
- **OpenAI**: Embeddings (text-embedding-3-small) and LLM (GPT-3.5-turbo)
- **SQLite**: Conversation and query logging
- **BeautifulSoup**: Web scraping

### Frontend

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Modern styling
- **Zustand**: State management
- **Lucide Icons**: Beautiful icons

## Architecture

```
User Query → FastAPI → Prompt Injection Check → LangChain RAG Pipeline
→ Qdrant Vector Search → Context Retrieval→ Reranker → OpenAI LLM → Response
→ SQLite Logging
```

## Prerequisites

- Docker and Docker Compose
- OpenAI API Key
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Zibtek
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp backend/env.template .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Start the Application

```bash
docker-compose up --build
```

This will:

1. Start Qdrant vector database
2. Build and start the FastAPI backend
3. Scrape Zibtek website and create embeddings (first run only)
4. Build and start the Next.js frontend

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## Usage

### Chat Interface

1. Open http://localhost:3000
2. The app automatically creates a new conversation
3. Type your question about Zibtek in the input box
4. Press "Send" or hit Enter
5. The AI will respond based on Zibtek's website content

### Managing Conversations

- **New Chat**: Click "New Chat" button in the sidebar
- **Load Old Chat**: Click on any conversation in the sidebar
- **Delete Chat**: Hover over a conversation and click the trash icon

### Example Queries

**Valid Queries (about Zibtek):**

- "What services does Zibtek offer?"
- "Tell me about Zibtek's team"
- "What technologies does Zibtek use?"
- "How can I contact Zibtek?"

**Invalid Queries (will be politely rejected):**

- "Who is the president of the US?"
- "What is the price of iPhone?"
- "Tell me about Google"

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/routes/          # API endpoints
│   │   ├── core/                # Config, database, security
│   │   ├── services/            # Scraper, embeddings, Qdrant, RAG
│   │   ├── models/              # Pydantic schemas
│   │   ├── utils/               # Logging utilities
│   │   ├── main.py              # FastAPI app
│   │   └── ingest_data.py       # Data ingestion script
│   ├── data/                    # SQLite database
│   ├── requirements.txt
│   ├── Dockerfile
│   └── start.sh
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   ├── components/          # React components
│   │   ├── lib/                 # API client, store
│   │   └── types/               # TypeScript types
│   ├── package.json
│   ├── Dockerfile
│   └── tailwind.config.js
└── docker-compose.yml
```

## API Endpoints

### Chat

- `POST /api/chat/message` - Send a message and get response
- `POST /api/chat/new` - Create new conversation

### Conversations

- `GET /api/chat/conversations` - List all conversations
- `GET /api/chat/conversations/{id}` - Get conversation with messages
- `DELETE /api/chat/conversations/{id}` - Delete conversation

## Security Features

### Prompt Injection Protection

The system detects and blocks common prompt injection patterns:

- "Ignore previous instructions"
- "You are now..."
- "System:"
- "Forget everything"
- And more...

### Out-of-Scope Detection

Questions unrelated to Zibtek are detected using:

1. Similarity scoring with retrieved context
2. Strong system prompts
3. Polite rejection messages

## Data Ingestion

The backend automatically scrapes Zibtek's website on first startup:

1. Crawls up to 50 pages from https://www.zibtek.com
2. Extracts and cleans text content
3. Chunks text into 1000-token segments with 200-token overlap
4. Generates embeddings using OpenAI
5. Stores in Qdrant vector database

To re-ingest data:

```bash
docker-compose exec backend python -m app.ingest_data
```

## Development

### Run Backend Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.template .env
# Edit .env with your OpenAI API key
uvicorn app.main:app --reload
```

### Run Frontend Locally

```bash
cd frontend
npm install
# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## Configuration

Edit `backend/app/core/config.py` to customize:

- `CHUNK_SIZE`: Size of text chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K_RESULTS`: Number of similar documents to retrieve (default: 5)
- `SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.7)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)

## Logging

All user queries and bot responses are logged in SQLite:

- Database: `backend/data/chatbot.db`
- Table: `query_logs`
- Fields: user_query, bot_response, sources, timestamp

To view logs:

```bash
sqlite3 backend/data/chatbot.db
SELECT * FROM query_logs;
```

## Troubleshooting

### Backend won't start

- Check if OpenAI API key is set correctly
- Ensure Qdrant is running: `docker-compose ps`
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend

- Verify CORS settings in backend `.env`
- Check `NEXT_PUBLIC_API_URL` in frontend environment

### No responses from chatbot

- Verify data ingestion completed successfully
- Check Qdrant has documents: http://localhost:6333/dashboard
- Review backend logs for errors

## License

MIT

## Support

For issues or questions, please contact Zibtek support.

# zibtek-Assignment
