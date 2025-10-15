# Running Zibtek AI Chatbot Locally

## Prerequisites

1. **Python 3.10+** installed
2. **Node.js 18+** installed
3. **Docker Desktop** (for Qdrant only)
4. **OpenAI API Key**

## Quick Setup (Automated)

### Option 1: Use Setup Script (Windows)

Double-click `setup-local.bat` or run:

```bash
setup-local.bat
```

This will:

- Create Python virtual environment
- Install all Python dependencies
- Install all Node.js dependencies
- Create .env files

### Option 2: Manual Setup

Follow these steps if the automated script fails or you need more control.

---

## Manual Setup Instructions

### Step 1: Free Up Disk Space (If Needed)

If you get "No space left on device" error:

1. **Delete UV cache:**

   ```bash
   rmdir /s /q C:\Users\Vandana\AppData\Local\uv\cache
   ```

2. **Clean temp files:**

   - Press `Windows + R`
   - Type `%temp%` and press Enter
   - Delete all files (Ctrl+A, Delete)
   - Empty Recycle Bin

3. **Run Disk Cleanup:**
   - Search for "Disk Cleanup"
   - Select C: drive
   - Check all boxes and clean

---

### Step 2: Backend Setup

1. **Navigate to backend:**

   ```bash
   cd backend
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**

   ```bash
   # Windows Command Prompt
   venv\Scripts\activate.bat

   # Windows PowerShell
   venv\Scripts\Activate.ps1

   # Git Bash
   source venv/Scripts/activate
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file:**

   ```bash
   copy env.template .env
   ```

6. **Edit .env file and add your OpenAI API key:**
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   QDRANT_COLLECTION_NAME=zibtek_docs
   DATABASE_URL=sqlite:///./data/chatbot.db
   CORS_ORIGINS=["http://localhost:3000"]
   TARGET_WEBSITE=https://www.zibtek.com
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   TOP_K_RESULTS=5
   SIMILARITY_THRESHOLD=0.7
   ```

---

### Step 3: Frontend Setup

1. **Open a NEW terminal and navigate to frontend:**

   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Create .env.local file:**

   ```bash
   echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
   ```

   Or manually create `frontend/.env.local` with:

   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

---

### Step 4: Start Qdrant (Vector Database)

In a NEW terminal:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

**Or use Docker Desktop:**

- Open Docker Desktop
- Search for "qdrant/qdrant"
- Run with ports 6333:6333

Wait for Qdrant to start (you'll see "Qdrant is ready" message)

---

### Step 5: Ingest Data (First Time Only)

In the backend terminal (with venv activated):

```bash
python -m app.ingest_data
```

This will:

- Scrape zibtek.com
- Create embeddings
- Populate Qdrant database

**This takes 5-10 minutes on first run.**

---

### Step 6: Start the Backend

In the backend terminal (with venv activated):

```bash
uvicorn app.main:app --reload
```

**Or use the batch file:**

```bash
# From project root
start-backend.bat
```

Backend will start at: http://localhost:8000

Check it's working: http://localhost:8000/docs

---

### Step 7: Start the Frontend

In the frontend terminal:

```bash
npm run dev
```

**Or use the batch file:**

```bash
# From project root
start-frontend.bat
```

Frontend will start at: http://localhost:3000

---

## Verify Everything is Running

You should have **4 terminals** open:

1. **Qdrant** - `docker run qdrant...` → Port 6333
2. **Backend** - `uvicorn app.main:app --reload` → Port 8000
3. **Frontend** - `npm run dev` → Port 3000
4. **(Optional)** Fourth terminal for running commands

**Check:**

- ✅ Qdrant: http://localhost:6333/dashboard
- ✅ Backend API: http://localhost:8000/docs
- ✅ Frontend: http://localhost:3000

---

## Testing the Chatbot

1. Open http://localhost:3000
2. You should see the chat interface
3. Try asking: "What services does Zibtek offer?"
4. Try an out-of-scope question: "Who is the president?"

---

## Troubleshooting

### Backend won't start

**Error: "No module named 'app'"**

- Make sure you're in the `backend` directory
- Make sure virtual environment is activated (you should see `(venv)` in your prompt)

**Error: "OPENAI_API_KEY not found"**

- Check that `backend/.env` exists
- Check that OPENAI_API_KEY is set in the .env file

### Frontend won't start

**Error: "Cannot find module"**

- Run `npm install` again
- Delete `node_modules` and `package-lock.json`, then run `npm install`

**Error: "Port 3000 already in use"**

- Kill the process using port 3000
- Or change the port: `npm run dev -- -p 3001`

### Qdrant connection errors

**Error: "Failed to connect to Qdrant"**

- Make sure Docker is running
- Make sure Qdrant container is running: `docker ps`
- Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant`

### Disk Space Issues

**Error: "No space left on device"**

1. Clean UV cache: `rmdir /s /q C:\Users\Vandana\AppData\Local\uv\cache`
2. Clean temp files: `%temp%` → Delete all
3. Empty Recycle Bin
4. Run Disk Cleanup on C: drive
5. Consider moving virtual environment to D: drive

---

## Stopping the Services

Press `Ctrl+C` in each terminal to stop:

1. Frontend (npm run dev)
2. Backend (uvicorn)
3. Qdrant (docker)

---

## Development Workflow

### Making Code Changes

**Backend changes:**

- Edit files in `backend/app/`
- Server auto-reloads (--reload flag)
- Check http://localhost:8000/docs for API changes

**Frontend changes:**

- Edit files in `frontend/src/`
- Browser auto-refreshes
- Check console for errors

### Re-ingesting Data

If you need to update the Zibtek website data:

```bash
# In backend directory with venv activated
python -m app.ingest_data
```

### Viewing Logs

**Backend logs:**

- Visible in the terminal where uvicorn is running

**Query logs (SQLite):**

```bash
# Install SQLite browser or use command line
sqlite3 backend/data/chatbot.db
SELECT * FROM query_logs ORDER BY timestamp DESC LIMIT 10;
```

---

## Quick Start Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Docker Desktop running
- [ ] OpenAI API key obtained
- [ ] Disk space: At least 2GB free
- [ ] Qdrant running (Docker)
- [ ] Backend .env file configured
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Data ingested (first time)
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Chatbot tested and working

---

## Next Steps

Once everything is running:

1. Read `TESTING.md` for comprehensive testing
2. Read `README.md` for full documentation
3. Explore the code in your IDE
4. Try customizing the system prompts
5. Adjust RAG parameters for better results

---

## Need Help?

- Check terminal output for specific errors
- Review `QUICK_REFERENCE.md` for common commands
- Check `SETUP.md` for Docker setup (alternative)
- Review backend logs for API errors
- Check browser console for frontend errors
