from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class SeverityLevel(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class VulnerabilityType(str, enum.Enum):
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    HARDCODED_SECRET = "hardcoded_secret"
    INSECURE_DEPENDENCY = "insecure_dependency"
    MISSING_VALIDATION = "missing_validation"
    UNSAFE_FILE_OP = "unsafe_file_op"
    WEAK_CRYPTO = "weak_crypto"
    OTHER = "other"

class ScanStatus(str, enum.Enum):
    PENDING = "pending"
    SCANNING = "scanning"
    COMPLETED = "completed"
    FAILED = "failed"

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(255), nullable=False)
    scan_type = Column(String(50), default="code")
    status = Column(SQLEnum(ScanStatus), default=ScanStatus.PENDING)
    files_scanned = Column(Integer, default=0)
    vulnerabilities_found = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    scan_duration = Column(Integer, nullable=True)  # in seconds

    # Relationships
    vulnerabilities = relationship("Vulnerability", back_populates="scan", cascade="all, delete-orphan")
    report = relationship("Report", back_populates="scan", uselist=False, cascade="all, delete-orphan")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    line_number = Column(Integer, nullable=True)
    vulnerability_type = Column(SQLEnum(VulnerabilityType), nullable=False)
    severity = Column(SQLEnum(SeverityLevel), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    cwe_id = Column(String(20), nullable=True)  # CWE identifier
    remediation = Column(Text, nullable=True)
    references = Column(Text, nullable=True)  # JSON string of URLs
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    scan = relationship("Scan", back_populates="vulnerabilities")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), unique=True, nullable=False)
    executive_summary = Column(Text, nullable=False)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    info_count = Column(Integer, default=0)
    total_score = Column(Integer, default=0)  # Security score (0-100)
    recommendations = Column(Text, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    scan = relationship("Scan", back_populates="report")