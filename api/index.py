from fastapi import FastAPI

app = FastAPI(title="Security Scanner API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Security Scanner API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Direct handler for Vercel
handler = app

__all__ = ["handler"]