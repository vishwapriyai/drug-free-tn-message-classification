import uvicorn
import gradio as gr
from app.main import app

# Create a clean Gradio interface for status display
with gr.Blocks(title="Drug Free TN AI Status") as demo:
    gr.Markdown("# 🚀 Drug Free TN AI Backend is Live!")
    gr.Markdown("The FastAPI server is running. You can access the Swagger API documentation at [/docs](/docs).")

# Mount your FastAPI application onto the Gradio container at '/status'
app = gr.mount_gradio_app(app, demo, path="/status")

if __name__ == "__main__":
    # Start the FastAPI server on port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)
