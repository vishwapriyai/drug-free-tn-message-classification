import uvicorn
import os

# Set production configurations or default environment variables if needed
if __name__ == "__main__":
    # Import the FastAPI instance from app/main.py
    from app.main import app
    
    # Hugging Face Spaces routes traffic to port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)
