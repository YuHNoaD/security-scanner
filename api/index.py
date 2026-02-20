# Vercel serverless function handler
from backend.app.main import app as api_app

# Vercel expects a handler function
handler = api_app

# Export for Vercel
__all__ = ["handler"]