from backend.app.main import app as api_app

# Vercel expects a handler that takes ASGI scope, receive, send
from mangum import Mangum

# Wrap FastAPI app for serverless deployment
handler = Mangum(api_app)

__all__ = ["handler"]