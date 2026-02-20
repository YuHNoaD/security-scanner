import re
import ast
from typing import List, Dict, Any
from datetime import datetime
from ..db.models import Vulnerability, SeverityLevel, VulnerabilityType

class BaseAnalyzer:
    """Base class for vulnerability analyzers"""
    
    def __init__(self, scan_id: int):
        self.scan_id = scan_id
        self.vulnerabilities: List[Dict[str, Any]] = []
    
    def add_vulnerability(
        self,
        file_path: str,
        line_number: int,
        vuln_type: VulnerabilityType,
        severity: SeverityLevel,
        title: str,
        description: str,
        code_snippet: str = None,
        cwe_id: str = None,
        remediation: str = None,
        references: List[str] = None
    ):
        """Add a vulnerability to the list"""
        self.vulnerabilities.append({
            "scan_id": self.scan_id,
            "file_path": file_path,
            "line_number": line_number,
            "vulnerability_type": vuln_type,
            "severity": severity,
            "title": title,
            "description": description,
            "code_snippet": code_snippet,
            "cwe_id": cwe_id,
            "remediation": remediation,
            "references": references,
            "created_at": datetime.utcnow()
        })
    
    def analyze(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Analyze file content and return vulnerabilities"""
        raise NotImplementedError("Subclasses must implement analyze method")


class SQLInjectionAnalyzer(BaseAnalyzer):
    """Analyzer for SQL Injection vulnerabilities"""
    
    # Patterns that might indicate SQL injection
    PATTERNS = [
        r'execute\s*\(\s*f["\'].*?\{.*?\}.*?["\']',  # f-strings in execute
        r'execute\s*\(\s*["\'].*?\+.*?["\']',         # String concatenation
        r'cursor\.execute\s*\(\s*["\'].*?\{.*?\}',     # cursor.execute with format
        r'select.*from.*where.*\{',                    # SELECT with format
        r'insert\s+into.*values.*\{',                  # INSERT with format
        r'update.*set.*\{',                            # UPDATE with format
        r'delete\s+from.*where.*\{',                   # DELETE with format
    ]
    
    def analyze(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            for pattern in self.PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    self.add_vulnerability(
                        file_path=file_path,
                        line_number=line_num,
                        vuln_type=VulnerabilityType.SQL_INJECTION,
                        severity=SeverityLevel.CRITICAL,
                        title="Potential SQL Injection",
                        description="SQL query constructed with untrusted user input",
                        code_snippet=line.strip(),
                        cwe_id="CWE-89",
                        remediation="Use parameterized queries or prepared statements",
                        references=[
                            "https://owasp.org/www-community/attacks/SQL_Injection",
                            "https://cwe.mitre.org/data/definitions/89.html"
                        ]
                    )
                    break
        
        return self.vulnerabilities


class XSSAnalyzer(BaseAnalyzer):
    """Analyzer for Cross-Site Scripting (XSS) vulnerabilities"""
    
    PATTERNS = [
        r'innerHTML\s*=\s*.*?\{',                      # innerHTML with variable
        r'outerHTML\s*=\s*.*?\{',                      # outerHTML with variable
        r'document\.write\s*\(\s*.*?\{',               # document.write with variable
        r'eval\s*\(\s*.*?\{',                          # eval with variable
        r'<.*?>.*?\{.*?\}.*?</.*?>',                   # HTML tag with variable
        r'return\s+["\'].*?\{.*?\}.*?["\']',           # Return HTML with variable
    ]
    
    def analyze(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            for pattern in self.PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    self.add_vulnerability(
                        file_path=file_path,
                        line_number=line_num,
                        vuln_type=VulnerabilityType.XSS,
                        severity=SeverityLevel.HIGH,
                        title="Potential Cross-Site Scripting (XSS)",
                        description="User input directly embedded in HTML/JavaScript without sanitization",
                        code_snippet=line.strip(),
                        cwe_id="CWE-79",
                        remediation="Sanitize user input before embedding in HTML. Use textContent or proper escaping.",
                        references=[
                            "https://owasp.org/www-community/attacks/xss/",
                            "https://cwe.mitre.org/data/definitions/79.html"
                        ]
                    )
                    break
        
        return self.vulnerabilities


class CommandInjectionAnalyzer(BaseAnalyzer):
    """Analyzer for Command Injection vulnerabilities"""
    
    PATTERNS = [
        r'os\.system\s*\(\s*.*?\{',                    # os.system with variable
        r'subprocess\.(call|run|Popen)\s*\(\s*.*?\{', # subprocess with variable
        r'subprocess\.(call|run|Popen)\s*\(\s*.*?\+',  # subprocess with concatenation
        r'eval\s*\(\s*.*?os\.system',                  # eval with os.system
        r'exec\s*\(\s*.*?os\.system',                  # exec with os.system
        r'popen\s*\(\s*.*?\{',                         # popen with variable
    ]
    
    def analyze(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            for pattern in self.PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    self.add_vulnerability(
                        file_path=file_path,
                        line_number=line_num,
                        vuln_type=VulnerabilityType.COMMAND_INJECTION,
                        severity=SeverityLevel.CRITICAL,
                        title="Potential Command Injection",
                        description="User input directly used in system command execution",
                        code_snippet=line.strip(),
                        cwe_id="CWE-78",
                        remediation="Use subprocess with shell=False and validate/sanitize input",
                        references=[
                            "https://owasp.org/www-community/attacks/Command_Injection",
                            "https://cwe.mitre.org/data/definitions/78.html"
                        ]
                    )
                    break
        
        return self.vulnerabilities


class SecretsAnalyzer(BaseAnalyzer):
    """Analyzer for hardcoded secrets and credentials"""
    
    PATTERNS = [
        (r'(api[_-]?key|apikey|api[_-]?secret|apikey|secret[_-]?key)\s*=\s*["\']([a-zA-Z0-9_\-]{20,})["\']', "API Key"),
        (r'(password|passwd|pwd)\s*=\s*["\']([^"\']{6,})["\']', "Password"),
        (r'(token|access[_-]?token|auth[_-]?token)\s*=\s*["\']([a-zA-Z0-9_\-]{20,})["\']', "Token"),
        (r'(aws[_-]?access[_-]?key[_-]?id)\s*=\s*["\']([A-Z0-9]{20})["\']', "AWS Access Key"),
        (r'(aws[_-]?secret[_-]?access[_-]?key)\s*=\s*["\']([a-zA-Z0-9/+=]{40})["\']', "AWS Secret Key"),
        (r'(private[_-]?key|privkey)\s*=\s*["\']([a-zA-Z0-9/+=]{20,})["\']', "Private Key"),
        (r'(db[_-]?password|database[_-]?password)\s*=\s*["\']([^"\']{6,})["\']', "Database Password"),
    ]
    
    def analyze(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            for pattern, secret_type in self.PATTERNS:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    # Mask the secret in the snippet
                    masked_line = re.sub(match.group(2), '*' * 10, line)
                    self.add_vulnerability(
                        file_path=file_path,
                        line_number=line_num,
                        vuln_type=VulnerabilityType.HARDCODED_SECRET,
                        severity=SeverityLevel.CRITICAL,
                        title=f"Hardcoded {secret_type}",
                        description=f"Hardcoded {secret_type} found in source code",
                        code_snippet=masked_line.strip(),
                        cwe_id="CWE-798",
                        remediation="Move secrets to environment variables or secret management system",
                        references=[
                            "https://cwe.mitre.org/data/definitions/798.html",
                            "https://owasp.org/www-community/credentials/"
                        ]
                    )
                    break
        
        return self.vulnerabilities


class Scanner:
    """Main scanner orchestrator"""
    
    def __init__(self, scan_id: int):
        self.scan_id = scan_id
        self.analyzers = [
            SQLInjectionAnalyzer(scan_id),
            XSSAnalyzer(scan_id),
            CommandInjectionAnalyzer(scan_id),
            SecretsAnalyzer(scan_id),
        ]
    
    def scan_file(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Scan a single file with all analyzers"""
        all_vulnerabilities = []
        
        for analyzer in self.analyzers:
            vulnerabilities = analyzer.analyze(file_path, content)
            all_vulnerabilities.extend(vulnerabilities)
        
        return all_vulnerabilities
    
    def scan_multiple_files(self, files: Dict[str, str]) -> List[Dict[str, Any]]:
        """Scan multiple files"""
        all_vulnerabilities = []
        
        for file_path, content in files.items():
            vulnerabilities = self.scan_file(file_path, content)
            all_vulnerabilities.extend(vulnerabilities)
        
        return all_vulnerabilities