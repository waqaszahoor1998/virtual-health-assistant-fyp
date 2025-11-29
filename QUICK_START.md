# Quick Start Guide - Virtual Health Assistant

## 🚀 Getting Started in 5 Steps

### Step 1: Backend Setup

#### macOS/Linux:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and JWT secret keys

# Initialize database (if PostgreSQL is running)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run backend server
python run.py
# Backend will run on http://localhost:5000
```

#### Windows (Command Prompt):

```cmd
REM Navigate to backend directory
cd backend

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Set up environment variables (copy .env.example to .env)
copy .env.example .env
REM Edit .env with your database URL and JWT secret keys

REM Initialize database (if PostgreSQL is running)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

REM Run backend server
python run.py
REM Backend will run on http://localhost:5000
```

#### Windows (PowerShell):

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
# If you get an execution policy error, run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
Copy-Item .env.example .env
# Edit .env with your database URL and JWT secret keys

# Initialize database (if PostgreSQL is running)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run backend server
python run.py
# Backend will run on http://localhost:5000
```

---

### Step 2: Frontend Setup

#### macOS/Linux:

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API base URL (optional, defaults to /api)

# Run frontend development server
npm run dev
# Frontend will run on http://localhost:3000
```

#### Windows (Command Prompt):

```cmd
REM Navigate to frontend directory (in a new terminal)
cd frontend

REM Install dependencies
npm install

REM Set up environment variables
copy .env.example .env
REM Edit .env with your API base URL (optional, defaults to /api)

REM Run frontend development server
npm run dev
REM Frontend will run on http://localhost:3000
```

#### Windows (PowerShell):

```powershell
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Set up environment variables
Copy-Item .env.example .env
# Edit .env with your API base URL (optional, defaults to /api)

# Run frontend development server
npm run dev
# Frontend will run on http://localhost:3000
```

---

### Step 3: Database Setup

#### macOS/Linux:

1. Install PostgreSQL (if not installed)
   - macOS: `brew install postgresql` or download from [PostgreSQL website](https://www.postgresql.org/download/)
   - Linux: `sudo apt-get install postgresql` (Ubuntu/Debian)

2. Start PostgreSQL service:
   ```bash
   # macOS (if installed via Homebrew)
   brew services start postgresql
   
   # Linux
   sudo systemctl start postgresql
   ```

3. Create database:
   ```bash
   createdb virtual_health_assistant
   ```

4. Update `backend/.env` with database URL:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/virtual_health_assistant
   ```

#### Windows:

1. Install PostgreSQL:
   - Download from [PostgreSQL website](https://www.postgresql.org/download/windows/)
   - Run the installer and follow the setup wizard
   - Remember the password you set for the `postgres` user
   - Ensure PostgreSQL is added to PATH during installation

2. Start PostgreSQL service:
   - Open Services (Win+R → `services.msc`)
   - Find "postgresql-x64-XX" service
   - Right-click → Start (if not running)

   OR use Command Prompt as Administrator:
   ```cmd
   net start postgresql-x64-14
   ```
   (Version number may vary)

3. Create database:
   ```cmd
   REM Open Command Prompt and run:
   psql -U postgres
   
   REM In PostgreSQL prompt:
   CREATE DATABASE virtual_health_assistant;
   \q
   ```

   OR using SQL:
   ```cmd
   psql -U postgres -c "CREATE DATABASE virtual_health_assistant;"
   ```

4. Update `backend/.env` with database URL:
   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/virtual_health_assistant
   ```

---

### Step 4: Environment Variables Configuration

#### Backend (.env)

Create `backend/.env` file with:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/virtual_health_assistant
CORS_ORIGINS=http://localhost:3000
PORT=5000
```

**Windows Note**: Use forward slashes or double backslashes in paths:
```
# Good:
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Also acceptable:
DATABASE_URL=postgresql://user:pass@localhost:5432\\dbname
```

#### Frontend (.env)

Create `frontend/.env` file with:

```env
# Backend API URL (optional, defaults to /api)
VITE_API_BASE_URL=/api
```

---

### Step 5: Test the Setup

1. **Start Backend Server** (Terminal 1):
   ```bash
   # macOS/Linux
   cd backend
   source venv/bin/activate
   python run.py
   
   # Windows Command Prompt
   cd backend
   venv\Scripts\activate.bat
   python run.py
   
   # Windows PowerShell
   cd backend
   .\venv\Scripts\Activate.ps1
   python run.py
   ```

2. **Start Frontend Server** (Terminal 2):
   ```bash
   # macOS/Linux/Windows
   cd frontend
   npm run dev
   ```

3. **Test the Application**:
   - Open browser to `http://localhost:3000`
   - Click "Sign Up" to create account
   - Login with your credentials
   - You should see the dashboard!

---

## 📁 Project Structure Overview

```
rehan/
├── backend/          # Flask API server
│   ├── app/         # Application code
│   ├── config.py    # Configuration
│   └── run.py       # Entry point
├── frontend/        # React application
│   ├── src/         # Source code
│   └── package.json # Dependencies
├── data/            # Data files
│   ├── raw/         # Original datasets
│   └── processed/   # Cleaned data
├── ml_models/       # ML model files
│   ├── scripts/     # Training scripts
│   └── models/      # Trained models
└── docs/            # Documentation
```

---

## ✅ Verification Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 3000
- [ ] PostgreSQL database created and accessible
- [ ] Environment variables configured
- [ ] Can access http://localhost:3000
- [ ] Can create account and login

---

## 🐛 Common Issues

### Backend won't start

#### macOS/Linux:
```bash
# Check PostgreSQL is running
pg_isready

# Verify DATABASE_URL in .env is correct
# Check all dependencies installed
pip list
```

#### Windows:
```cmd
REM Check PostgreSQL is running
psql --version

REM Test connection
psql -U postgres -c "SELECT version();"

REM Check all dependencies installed
pip list
```

### Frontend won't start

#### macOS/Linux:
```bash
# Check Node.js version
node --version  # Should be 16+

# Clear node_modules and reinstall
rm -rf node_modules
npm install
```

#### Windows:
```cmd
REM Check Node.js version
node --version  # Should be 16+

REM Clear node_modules and reinstall
rmdir /s /q node_modules
npm install
```

### Database connection error

#### macOS/Linux:
```bash
# Verify PostgreSQL is installed and running
pg_isready

# Check database exists
psql -l

# Test connection
psql -U username -d virtual_health_assistant
```

#### Windows:
```cmd
REM Verify PostgreSQL is installed
psql --version

REM Check if service is running
sc query postgresql-x64-14

REM Test connection
psql -U postgres -d virtual_health_assistant
```

**Common Windows Issues:**
- PostgreSQL service not started: Start it from Services (`services.msc`)
- Port 5432 already in use: Change PostgreSQL port or stop conflicting service
- Authentication failed: Check username/password in DATABASE_URL

### Python/Virtual Environment Issues

#### Windows PowerShell Execution Policy Error:
```powershell
# If you see: "execution of scripts is disabled on this system"
# Run as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Python not found:
- Ensure Python is installed and added to PATH
- Check: `python --version` or `python3 --version`
- Reinstall Python with "Add Python to PATH" option checked

### Port Already in Use

#### Windows:
```cmd
REM Check what's using port 5000
netstat -ano | findstr :5000

REM Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### macOS/Linux:
```bash
# Check what's using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

---

## 📚 Next Steps

1. **Data Preparation**: Run data cleaning scripts
   ```bash
   # macOS/Linux
   python ml_models/scripts/analyze_data.py
   
   # Windows
   python ml_models\scripts\analyze_data.py
   ```

2. **ML Model Training**: Train models with cleaned data
   ```bash
   # macOS/Linux
   python ml_models/scripts/train_models.py
   
   # Windows
   python ml_models\scripts\train_models.py
   ```

3. **API Development**: Implement remaining endpoints
   - See `backend/README.md` for API structure

4. **Frontend Development**: Build out dashboard pages
   - See `frontend/README.md` for component structure

---

## 🪟 Windows-Specific Tips

1. **Use PowerShell for better experience** (better than Command Prompt)
2. **Install Git Bash** for Unix-like commands (optional)
3. **Use VS Code** with integrated terminal
4. **Path separators**: Use forward slashes `/` or double backslashes `\\`
5. **Environment variables**: Use `.env` files, not system environment variables
6. **Line endings**: Git should handle this automatically, but use `core.autocrlf true`

---

## 📞 Need Help?

- Check detailed READMEs:
  - `backend/README.md` - Backend documentation
  - `frontend/README.md` - Frontend documentation
- Review project plan: `PROJECT_PLAN.md`
- Check ML recommendations: `ML_MODELS_RECOMMENDATION.md`
- Review dataset info: `DATASET_RECOMMENDATIONS.md`
- JWT Authentication: `JWT_AUTHENTICATION.md`
