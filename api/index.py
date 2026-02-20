from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="Security Scanner API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Security Scanner API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Mangum adapter for AWS Lambda/Vercel
lambda_handler = Mangum(app)

# Vercel expects a handler function
handler = lambda_handler

__all__ = ["handler"]