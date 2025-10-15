@echo off
echo ============================================
echo Setting up Zibtek AI Chatbot Locally
echo ============================================

REM Backend Setup
echo.
echo [1/6] Creating Python virtual environment...
cd backend
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment. Check disk space!
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo [4/6] Creating .env file...
if not exist .env (
    copy env.template .env
    echo .env file created! Please edit it and add your OPENAI_API_KEY
)

cd ..

REM Frontend Setup
echo.
echo [5/6] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install npm packages!
    pause
    exit /b 1
)

echo [6/6] Creating frontend .env.local...
if not exist .env.local (
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
)

cd ..

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit backend/.env and add your OPENAI_API_KEY
echo 2. Start Qdrant: docker run -p 6333:6333 qdrant/qdrant
echo 3. Start backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo 4. Start frontend: cd frontend ^&^& npm run dev
echo.
pause

