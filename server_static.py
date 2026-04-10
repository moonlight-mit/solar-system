"""
Static file server for Solar System 3D frontend
Allows serving HTML and assets without separate web server
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

# Create FastAPI app for static files
app = FastAPI()

# Get the templates directory
templates_dir = Path(__file__).parent / "templates"

# Mount static files
app.mount("/templates", StaticFiles(directory=str(templates_dir)), name="templates")
app.mount("/", StaticFiles(directory=str(templates_dir), html=True), name="static")


@app.get("/")
async def root():
    """Serve the main HTML file"""
    return FileResponse(templates_dir / "index.html")


@app.get("/solar_api.js")
async def get_api():
    """Serve the API client"""
    return FileResponse(Path(__file__).parent / "solar_api.js")


if __name__ == "__main__":
    import uvicorn
    print("🌐 Serving Solar System Frontend on http://localhost:9000")
    uvicorn.run(app, host="0.0.0.0", port=9000)
