from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes import complaint, dashboard

app = FastAPI(
    title="Drug Free TN AI System",
    description="AI-powered complaint analysis system",
    version="1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import Response

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)
# Include API routes
app.include_router(complaint.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Get the absolute path to the dashboard directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DASHBOARD_DIR = os.path.join(BASE_DIR, "Ai-tool-29426", "dashboard")

# Serve static files from dashboard directory
app.mount("/static", StaticFiles(directory=DASHBOARD_DIR), name="static")

# Serve the main dashboard HTML file
@app.get("/")
async def serve_dashboard():
    dashboard_file = os.path.join(DASHBOARD_DIR, "dashboard.html")
    if os.path.exists(dashboard_file):
        return FileResponse(dashboard_file, media_type="text/html")
    return {"message": "Drug AI System Running 🚀"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Drug Free TN AI System is running"}