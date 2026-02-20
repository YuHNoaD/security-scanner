from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
import json
import aiofiles
import os

from .db.database import get_db, init_db
from .db.models import Scan, Vulnerability, Report, ScanStatus, SeverityLevel
from .core.scanner import Scanner

app = FastAPI(
    title="Security Scanner API",
    description="Automated vulnerability scanner for web applications",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Health check
@app.get("/")
async def root():
    return {
        "message": "Security Scanner API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Scan endpoints
@app.post("/api/scan/start")
async def start_scan(
    project_name: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start a new security scan"""
    try:
        # Create scan record
        scan = Scan(
            project_name=project_name,
            status=ScanStatus.PENDING,
            started_at=datetime.utcnow()
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        return {
            "scan_id": scan.id,
            "project_name": project_name,
            "status": scan.status.value,
            "message": "Scan created successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scan/{scan_id}/upload")
async def upload_files(
    scan_id: int,
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Upload files for scanning"""
    try:
        # Get scan
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        # Create upload directory
        upload_dir = f"uploads/scan_{scan_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save files
        file_paths = []
        for file in files:
            file_path = os.path.join(upload_dir, file.filename)
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            file_paths.append(file_path)
        
        # Update scan status
        scan.status = ScanStatus.SCANNING
        scan.files_scanned = len(file_paths)
        db.commit()
        
        # Start background scan
        background_tasks.add_task(run_scan, scan_id, file_paths, db)
        
        return {
            "scan_id": scan_id,
            "files_uploaded": len(file_paths),
            "file_paths": file_paths,
            "status": scan.status.value,
            "message": "Files uploaded successfully, scan started"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def run_scan(scan_id: int, file_paths: List[str], db: Session):
    """Run security scan in background"""
    try:
        # Get scan
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return
        
        # Initialize scanner
        scanner = Scanner(scan_id)
        
        # Read and scan files
        files_content = {}
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                files_content[file_path] = content
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        
        # Run scan
        vulnerabilities_data = scanner.scan_multiple_files(files_content)
        
        # Save vulnerabilities
        for vuln_data in vulnerabilities_data:
            vuln = Vulnerability(**vuln_data)
            db.add(vuln)
        
        # Update scan
        scan.vulnerabilities_found = len(vulnerabilities_data)
        scan.status = ScanStatus.COMPLETED
        scan.completed_at = datetime.utcnow()
        
        # Calculate duration
        if scan.started_at:
            duration = (scan.completed_at - scan.started_at).total_seconds()
            scan.scan_duration = int(duration)
        
        db.commit()
        
        # Generate report
        generate_report(scan_id, db)
        
    except Exception as e:
        print(f"Error during scan: {e}")
        scan.status = ScanStatus.FAILED
        db.commit()

def generate_report(scan_id: int, db: Session):
    """Generate scan report"""
    try:
        # Get scan and vulnerabilities
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
        
        # Count by severity
        critical = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.CRITICAL)
        high = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.HIGH)
        medium = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.MEDIUM)
        low = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.LOW)
        info = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.INFO)
        
        # Calculate security score (0-100, higher is better)
        total = critical + high + medium + low + info
        if total == 0:
            score = 100
        else:
            # Weighted score: Critical=10, High=5, Medium=2, Low=1, Info=0
            weighted_score = (critical * 10 + high * 5 + medium * 2 + low * 1)
            score = max(0, 100 - weighted_score)
        
        # Generate summary
        summary = f"""
Security Scan Report for {scan.project_name}

Scan Status: {scan.status.value}
Files Scanned: {scan.files_scanned}
Total Vulnerabilities: {total}
Security Score: {score}/100

Severity Breakdown:
- Critical: {critical}
- High: {high}
- Medium: {medium}
- Low: {low}
- Info: {info}

Scan Duration: {scan.scan_duration} seconds
Started: {scan.started_at}
Completed: {scan.completed_at}
        """.strip()
        
        # Generate recommendations
        recommendations = []
        if critical > 0:
            recommendations.append("⚠️ CRITICAL vulnerabilities found! Fix immediately.")
        if high > 0:
            recommendations.append("🔴 HIGH severity vulnerabilities should be fixed soon.")
        if medium > 0:
            recommendations.append("🟡 MEDIUM severity vulnerabilities should be addressed.")
        if low > 0:
            recommendations.append("🟢 LOW severity vulnerabilities can be fixed when convenient.")
        
        if not recommendations:
            recommendations.append("✅ No vulnerabilities found! Great job!")
        
        # Create report
        report = Report(
            scan_id=scan_id,
            executive_summary=summary,
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
            info_count=info,
            total_score=score,
            recommendations="\n".join(recommendations)
        )
        db.add(report)
        db.commit()
        
    except Exception as e:
        print(f"Error generating report: {e}")

# Get scan results
@app.get("/api/scan/{scan_id}")
async def get_scan(scan_id: int, db: Session = Depends(get_db)):
    """Get scan details"""
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return {
        "id": scan.id,
        "project_name": scan.project_name,
        "status": scan.status.value,
        "files_scanned": scan.files_scanned,
        "vulnerabilities_found": scan.vulnerabilities_found,
        "started_at": scan.started_at.isoformat() if scan.started_at else None,
        "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
        "scan_duration": scan.scan_duration
    }

@app.get("/api/scan/{scan_id}/vulnerabilities")
async def get_vulnerabilities(
    scan_id: int,
    severity: str = None,
    db: Session = Depends(get_db)
):
    """Get vulnerabilities for a scan"""
    # Check if scan exists
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Query vulnerabilities
    query = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id)
    
    # Filter by severity if provided
    if severity:
        query = query.filter(Vulnerability.severity == severity)
    
    vulnerabilities = query.all()
    
    return {
        "scan_id": scan_id,
        "total": len(vulnerabilities),
        "vulnerabilities": [
            {
                "id": v.id,
                "file_path": v.file_path,
                "line_number": v.line_number,
                "vulnerability_type": v.vulnerability_type.value,
                "severity": v.severity.value,
                "title": v.title,
                "description": v.description,
                "code_snippet": v.code_snippet,
                "cwe_id": v.cwe_id,
                "remediation": v.remediation,
                "references": json.loads(v.references) if v.references else []
            }
            for v in vulnerabilities
        ]
    }

@app.get("/api/scan/{scan_id}/report")
async def get_report(scan_id: int, db: Session = Depends(get_db)):
    """Get scan report"""
    # Check if scan exists
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Get report
    report = db.query(Report).filter(Report.scan_id == scan_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {
        "scan_id": scan_id,
        "executive_summary": report.executive_summary,
        "critical_count": report.critical_count,
        "high_count": report.high_count,
        "medium_count": report.medium_count,
        "low_count": report.low_count,
        "info_count": report.info_count,
        "total_score": report.total_score,
        "recommendations": report.recommendations,
        "generated_at": report.generated_at.isoformat()
    }

# List all scans
@app.get("/api/scans")
async def list_scans(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    """List all scans"""
    scans = db.query(Scan).order_by(Scan.started_at.desc()).limit(limit).offset(offset).all()
    
    return {
        "total": len(scans),
        "scans": [
            {
                "id": scan.id,
                "project_name": scan.project_name,
                "status": scan.status.value,
                "files_scanned": scan.files_scanned,
                "vulnerabilities_found": scan.vulnerabilities_found,
                "started_at": scan.started_at.isoformat() if scan.started_at else None,
                "completed_at": scan.completed_at.isoformat() if scan.completed_at else None
            }
            for scan in scans
        ]
    }

# Delete scan
@app.delete("/api/scan/{scan_id}")
async def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    """Delete a scan"""
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Delete scan (cascade will delete vulnerabilities and report)
    db.delete(scan)
    db.commit()
    
    return {"message": "Scan deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)