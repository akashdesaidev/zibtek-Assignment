# 🚀 Get Started in 5 Minutes

Follow these simple steps to run the Zibtek AI Chatbot on your machine.

## Step 1: Prerequisites ✓

Make sure you have:

- **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop))
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

## Step 2: Create Environment File ⚙️

Create a file named `.env` in the project root directory with:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Replace `sk-your-actual-api-key-here` with your real OpenAI API key.

## Step 3: Start the Application 🐳

Open terminal in the project directory and run:

```bash
docker-compose up --build
```

**First time?** This will take 5-10 minutes to:

- Download Docker images
- Build the application
- Scrape the Zibtek website
- Create embeddings
- Start all services

## Step 4: Open the Chat 💬

Once you see "Uvicorn running on http://0.0.0.0:8000" in the logs:

**Open your browser to:** http://localhost:3000

## Step 5: Start Chatting! 🤖

Try these questions:

✅ **Valid** (will get answers):

- "What services does Zibtek offer?"
- "Tell me about Zibtek's team"
- "What technologies does Zibtek use?"

❌ **Invalid** (will be rejected):

- "Who is the president of the US?"
- "What's the weather today?"

---

## Troubleshooting 🔧

### Issue: "OpenAI API key not found"

**Fix:** Make sure you created the `.env` file with your API key.

### Issue: "Port already in use"

**Fix:** Stop any services using ports 3000, 8000, or 6333.

### Issue: "Connection refused"

**Fix:** Wait a few more minutes for all services to start.

---

## What's Next? 📚

- **Full Documentation**: Read [README.md](README.md)
- **Setup Guide**: See [SETUP.md](SETUP.md)
- **Testing**: Check [TESTING.md](TESTING.md)
- **Quick Commands**: View [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## Stop the Application 🛑

```bash
# Press Ctrl+C in the terminal, then:
docker-compose down
```

---

**That's it! You're ready to go! 🎉**

