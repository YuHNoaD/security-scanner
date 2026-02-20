from fastapi import FastAPI

app = FastAPI(title="Security Scanner API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Security Scanner API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/test")
async def test_endpoint():
    return {"message": "Test endpoint working!"}

from mangum import Mangum
handler = Mangum(app)

__all__ = ["handler"]