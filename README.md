# 🛡️ Security Audit & Vulnerability Scanner System

Automated vulnerability scanner for web applications and codebases.

## 🎯 Features

### Vulnerability Detection
- **SQL Injection** - Detects SQL injection vulnerabilities
- **XSS** - Finds cross-site scripting vulnerabilities
- **Command Injection** - Identifies command injection risks
- **Hardcoded Secrets** - Detects hardcoded credentials and API keys
- **More coming soon** - Dependency scanning, config checking, etc.

### Core Features
- 🔍 Multi-file scanning
- 📊 Detailed vulnerability reports
- 📈 Security scoring (0-100)
- 🎨 REST API
- 📝 Remediation recommendations
- 📋 Scan history
- 🚀 Fast scanning

## 📦 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database (PostgreSQL ready)
- **Python 3.12** - Core language

### Frontend (Coming Soon)
- **Next.js 14** - React framework
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Beautiful components
- **Recharts** - Data visualization

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Test the Scanner

```bash
# 1. Start a scan
curl -X POST "http://localhost:8000/api/scan/start?project_name=Test"

# 2. Upload vulnerable code
curl -X POST "http://localhost:8000/api/scan/1/upload" \
  -F "files=@test_samples/vulnerable_app.py"

# 3. Get scan results
curl "http://localhost:8000/api/scan/1"

# 4. Get vulnerabilities
curl "http://localhost:8000/api/scan/1/vulnerabilities"

# 5. Get report
curl "http://localhost:8000/api/scan/1/report"
```

## 📊 API Documentation

Once the backend is running:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔍 Vulnerability Types

### 1. SQL Injection (Critical)
Detects:
- f-string queries with user input
- String concatenation in queries
- Unparameterized queries

**Example:**
```python
# VULNERABLE
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# SAFE
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### 2. XSS (High)
Detects:
- innerHTML with variables
- document.write with variables
- HTML embedding with user input

**Example:**
```python
# VULNERABLE
html = f"<div>Welcome, {user_input}!</div>"

# SAFE
html = f"<div>Welcome, {escape(user_input)}!</div>"
```

### 3. Command Injection (Critical)
Detects:
- os.system with variables
- subprocess with variables
- popen with variables

**Example:**
```python
# VULNERABLE
os.system(f"cat {filename}")

# SAFE
subprocess.run(['cat', filename], shell=False)
```

### 4. Hardcoded Secrets (Critical)
Detects:
- API keys
- Passwords
- Tokens
- AWS credentials
- Private keys

**Example:**
```python
# VULNERABLE
api_key = "sk-1234567890"

# SAFE
api_key = os.getenv("API_KEY")
```

## 📈 Security Score

Score calculated based on vulnerabilities:
- **Critical:** -10 points
- **High:** -5 points
- **Medium:** -2 points
- **Low:** -1 point
- **Info:** 0 points

**Maximum score: 100**

## 🎨 Project Structure

```
security-scanner/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core scanner logic
│   │   │   └── analyzers/  # Vulnerability analyzers
│   │   ├── db/             # Database models
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── README.md
├── frontend/               # Next.js frontend (coming soon)
├── test_samples/           # Vulnerable code samples
│   ├── vulnerable_app.py
│   └── README.md
└── README.md
```

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest
```

### Test with Sample Code

```bash
# Upload vulnerable code to test detection
curl -X POST "http://localhost:8000/api/scan/1/upload" \
  -F "files=@test_samples/vulnerable_app.py"
```

**Expected Results:**
- 3 SQL Injection vulnerabilities
- 2 XSS vulnerabilities
- 2 Command Injection vulnerabilities
- 4 Hardcoded Secret vulnerabilities
- **Total: 11 vulnerabilities**

## 📚 Documentation

- [Backend README](backend/README.md) - Backend documentation
- [API Docs](http://localhost:8000/docs) - Interactive API documentation
- [Test Samples](test_samples/README.md) - Vulnerable code examples

## 🚀 Deployment

### Vercel

```bash
# Backend
cd backend
vercel deploy

# Frontend (coming soon)
cd frontend
vercel deploy
```

### Railway

```bash
railway up
```

### Docker

```bash
# Build
docker build -t security-scanner -f backend/Dockerfile .

# Run
docker run -p 8000:8000 security-scanner
```

## 🎓 Learning Outcomes

### Technical Skills
- FastAPI backend development
- Security analysis techniques
- Static code analysis
- Database design
- API development
- Authentication & authorization

### Security Knowledge
- Common web vulnerabilities (OWASP Top 10)
- Vulnerability detection techniques
- Security best practices
- Remediation strategies
- Security metrics & reporting

## 📊 Status

- ✅ Backend Core (Phase 1) - **COMPLETE**
- ⏳ Frontend (Phase 2) - **PENDING**
- ⏳ Testing & Deployment (Phase 3) - **PENDING**

## 🎯 Next Steps

1. Build frontend dashboard
2. Add more vulnerability types
3. Implement dependency scanning
4. Add configuration checking
5. Create PDF report export
6. Deploy to production

## 📝 License

MIT

## 👨‍💻 Author

Built by Eye (AI Assistant)

---

**Made with 🤖 by Eye - Security Scanner System**