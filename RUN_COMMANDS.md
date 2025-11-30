# 🚀 Run Commands - Backend & Frontend

## Quick Start Commands

---

## 🔷 Backend Server

### macOS/Linux:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python run.py              # Start server
```

**Backend runs on**: `http://localhost:5000`

### Windows (Command Prompt):

```cmd
cd backend
venv\Scripts\activate.bat
python run.py
```

**Backend runs on**: `http://localhost:5000`

### Windows (PowerShell):

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python run.py
```

**Backend runs on**: `http://localhost:5000`

---

## 🔷 Frontend Server

### macOS/Linux/Windows:

```bash
cd frontend
npm run dev
```

**Frontend runs on**: `http://localhost:5173` (Vite default port)

---

## 🔷 Running Both Servers

### Option 1: Two Separate Terminals

**Terminal 1 - Backend:**
```bash
cd /Users/m.w.zahoor/Desktop/rehan/backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd /Users/m.w.zahoor/Desktop/rehan/frontend
npm run dev
```

---

### Option 2: Background Process

**Start Backend in Background:**
```bash
cd backend
source venv/bin/activate
python run.py &
```

**Then start Frontend:**
```bash
cd frontend
npm run dev
```

---

## ✅ Verify Setup

### Check Backend:
- Open: `http://localhost:5000`
- Should see API response or error (means it's running)

### Check Frontend:
- Open: `http://localhost:5173`
- Should see login page

---

## 📋 Prerequisites Before Running

### Backend Prerequisites:
1. ✅ Virtual environment created and activated
2. ✅ Dependencies installed: `pip install -r requirements.txt`
3. ✅ `.env` file configured with:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
4. ✅ PostgreSQL database created
5. ✅ Database migrations run: `flask db upgrade`

### Frontend Prerequisites:
1. ✅ Node.js installed (16+)
2. ✅ Dependencies installed: `npm install`
3. ✅ `.env` file (optional, defaults to `/api`)

---

## 🛑 Stop Servers

### Stop Backend:
- Press `Ctrl+C` in terminal running backend
- Or kill process: `lsof -ti:5000 | xargs kill` (macOS/Linux)
- Or: `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F` (Windows)

### Stop Frontend:
- Press `Ctrl+C` in terminal running frontend
- Or kill process: `lsof -ti:5173 | xargs kill` (macOS/Linux)

---

## 🔍 Quick Status Check

```bash
# Check if backend is running
curl http://localhost:5000/api/health 2>/dev/null || echo "Backend not running"

# Check if frontend is running
curl http://localhost:5173 2>/dev/null || echo "Frontend not running"
```

---

## 📝 Full Setup (First Time)

### Backend First-Time Setup:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python run.py
```

### Frontend First-Time Setup:
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env if needed (optional)
npm run dev
```

---

## 🌐 Default URLs

- **Backend API**: `http://localhost:5000`
- **Frontend App**: `http://localhost:5173`
- **API Base Path**: `/api`
- **Swagger Docs**: `http://localhost:5000/swagger` (if enabled)

---

**Quick Run**: Backend: `python run.py` | Frontend: `npm run dev`

