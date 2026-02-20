# Security Scanner Backend

FastAPI backend for automated vulnerability scanning.

## Features

- **SQL Injection Detection** - Detects SQL injection vulnerabilities
- **XSS Detection** - Finds cross-site scripting vulnerabilities
- **Command Injection Detection** - Identifies command injection risks
- **Secrets Detection** - Finds hardcoded credentials and API keys
- **Report Generation** - Creates detailed security reports
- **REST API** - Full REST API for integration

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Running

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Scans

- `POST /api/scan/start` - Start a new scan
- `POST /api/scan/{scan_id}/upload` - Upload files for scanning
- `GET /api/scan/{scan_id}` - Get scan details
- `GET /api/scan/{scan_id}/vulnerabilities` - Get vulnerabilities
- `GET /api/scan/{scan_id}/report` - Get scan report
- `GET /api/scans` - List all scans
- `DELETE /api/scan/{scan_id}` - Delete a scan

### Health

- `GET /` - API info
- `GET /health` - Health check

## Vulnerability Types

1. **SQL Injection** (Critical)
   - Detects f-string queries
   - String concatenation in queries
   - Unparameterized queries

2. **XSS** (High)
   - innerHTML with variables
   - document.write with variables
   - eval with variables

3. **Command Injection** (Critical)
   - os.system with variables
   - subprocess with variables
   - popen with variables

4. **Hardcoded Secrets** (Critical)
   - API keys
   - Passwords
   - Tokens
   - AWS keys
   - Private keys

## Severity Levels

- **Critical** (9-10) - Immediate fix required
- **High** (7-8) - Fix soon
- **Medium** (4-6) - Fix when possible
- **Low** (1-3) - Nice to fix
- **Info** (0) - Informational

## Security Score

Score calculated based on vulnerabilities found:
- Critical: -10 points
- High: -5 points
- Medium: -2 points
- Low: -1 point
- Info: 0 points

Maximum score: 100

## Database

Uses SQLite by default. Database file: `security_scanner.db`

To use PostgreSQL, set `DATABASE_URL` environment variable.

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Deployment

### Vercel

```bash
vercel deploy
```

### Railway

```bash
railway up
```

### Docker

```bash
docker build -t security-scanner .
docker run -p 8000:8000 security-scanner
```

## License

MIT