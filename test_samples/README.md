# Test Samples

This directory contains vulnerable code samples for testing the security scanner.

## vulnerable_app.py

Contains 10 different vulnerability types:

1. **SQL Injection** (Critical) - f-string queries
2. **SQL Injection** (Critical) - string concatenation
3. **XSS** (High) - HTML embedding
4. **XSS** (High) - innerHTML
5. **Command Injection** (Critical) - os.system
6. **Command Injection** (Critical) - subprocess
7. **Hardcoded API Key** (Critical)
8. **Hardcoded Password** (Critical)
9. **Hardcoded AWS Credentials** (Critical)
10. **Hardcoded Token** (Critical)

Also includes one safe function that should not trigger any alerts.

## Usage

Upload this file to the scanner to test vulnerability detection:

```bash
# Start the backend
cd backend
python -m uvicorn app.main:app --reload

# Upload file via API
curl -X POST "http://localhost:8000/api/scan/1/upload" \
  -F "files=@test_samples/vulnerable_app.py"
```

## Expected Results

The scanner should detect:
- 3 SQL Injection vulnerabilities
- 2 XSS vulnerabilities
- 2 Command Injection vulnerabilities
- 4 Hardcoded Secret vulnerabilities

Total: 11 vulnerabilities

Severity breakdown:
- Critical: 9
- High: 2
- Medium: 0
- Low: 0
- Info: 0