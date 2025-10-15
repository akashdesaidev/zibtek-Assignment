# LangSmith Tracing Setup Guide

## ✅ LangSmith Tracing Enabled!

I've successfully configured LangSmith tracing for your Zibtek AI Chatbot. Here's what was added:

---

## **📋 What Was Configured:**

### 1. **Backend Configuration** (`backend/app/core/config.py`)

- Added LangSmith environment variables support
- Made them optional (won't break if not set)
- Added `extra = "ignore"` to handle additional env vars

### 2. **Main Application** (`backend/app/main.py`)

- Added automatic LangSmith initialization
- Sets up tracing when `LANGSMITH_TRACING=true`
- Configures all required environment variables

### 3. **Dependencies** (`requirements.txt` & `pyproject.toml`)

- Added `langsmith>=0.0.83,<0.1` (compatible with LangChain 0.1.4)
- Installed successfully with UV

---

## **🔧 Your .env Configuration:**

Your `backend/.env` file should now include:

```env
# Existing settings...
OPENAI_API_KEY=sk-your-key-here
QDRANT_HOST=localhost
QDRANT_PORT=6333

# LangSmith Tracing (NEW)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_pt_a7e6f19324aa4c17...ad0d39d7329a_a81e91248e
LANGSMITH_PROJECT=zibtek
```

---

## **🚀 How to Enable Tracing:**

### **Option 1: Enable Tracing**

Set in your `.env`:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT=zibtek
```

### **Option 2: Disable Tracing**

Set in your `.env`:

```env
LANGSMITH_TRACING=false
# Or remove the line entirely
```

---

## **📊 What Gets Traced:**

When enabled, LangSmith will trace:

1. **OpenAI API Calls**

   - Embedding generation
   - LLM responses
   - Token usage and costs

2. **RAG Pipeline**

   - Query embedding generation
   - Vector search in Qdrant
   - Context retrieval
   - Response generation

3. **LangChain Operations**
   - Chain executions
   - Tool calls
   - Error handling

---

## **🔍 Viewing Traces:**

1. **Go to LangSmith Dashboard**: https://smith.langchain.com
2. **Sign in** with your account
3. **Navigate to your project** (named "zibtek")
4. **View traces** in real-time as users interact with the chatbot

---

## **📈 Benefits of Tracing:**

### **Development:**

- Debug RAG pipeline issues
- Monitor token usage and costs
- Track response quality
- Identify bottlenecks

### **Production:**

- Monitor system performance
- Track user interactions
- Debug production issues
- Optimize costs

### **Analytics:**

- Most common questions
- Response times
- Error rates
- User satisfaction

---

## **🧪 Testing Tracing:**

### **1. Restart Backend** (to apply changes):

```bash
# Stop current backend (Ctrl+C)
# Then restart:
cd D:/Zibtek/backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Check Logs:**

You should see:

```
INFO - LangSmith tracing enabled
```

### **3. Test the Chatbot:**

1. Open: http://localhost:3000
2. Ask: "What services does Zibtek offer?"
3. Check LangSmith dashboard for traces

---

## **🔧 Troubleshooting:**

### **Issue: "LangSmith not installed"**

**Solution:**

```bash
cd backend
uv add "langsmith>=0.0.83,<0.1"
```

### **Issue: "Invalid API key"**

**Solution:**

- Check your LangSmith API key in `.env`
- Verify the key is active in LangSmith dashboard
- Ensure no extra spaces in the key

### **Issue: "No traces appearing"**

**Solution:**

- Verify `LANGSMITH_TRACING=true` in `.env`
- Check backend logs for "LangSmith tracing enabled"
- Ensure LangSmith project exists
- Try a simple query first

### **Issue: "Permission denied"**

**Solution:**

- Check LangSmith API key permissions
- Ensure project name matches exactly
- Verify endpoint URL is correct

---

## **📝 Environment Variables Reference:**

| Variable             | Required | Description               | Example                           |
| -------------------- | -------- | ------------------------- | --------------------------------- |
| `LANGSMITH_TRACING`  | Yes      | Enable/disable tracing    | `true`                            |
| `LANGSMITH_ENDPOINT` | Yes      | LangSmith API endpoint    | `https://api.smith.langchain.com` |
| `LANGSMITH_API_KEY`  | Yes      | Your LangSmith API key    | `lsv2_pt_...`                     |
| `LANGSMITH_PROJECT`  | Yes      | Project name in LangSmith | `zibtek`                          |

---

## **🎯 Next Steps:**

1. **Restart your backend** to apply the changes
2. **Test the chatbot** with a few questions
3. **Check LangSmith dashboard** for traces
4. **Monitor performance** and costs
5. **Use traces** to debug and optimize

---

## **💡 Pro Tips:**

### **Cost Monitoring:**

- Set up alerts in LangSmith for high token usage
- Monitor daily/weekly costs
- Optimize prompts to reduce tokens

### **Performance Optimization:**

- Use traces to identify slow operations
- Optimize similarity thresholds
- Cache frequently asked questions

### **Debugging:**

- Use traces to debug RAG pipeline issues
- Monitor embedding quality
- Track context retrieval effectiveness

---

**🎉 Your Zibtek AI Chatbot now has full LangSmith tracing enabled!**

Check the LangSmith dashboard to see your traces in action.
