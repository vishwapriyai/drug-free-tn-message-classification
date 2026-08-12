import gradio as gr
from app.main import app

# Create a clean Gradio interface for status display
with gr.Blocks(title="Drug Free TN AI Status") as demo:
    gr.Markdown("# 🚀 Drug Free TN AI Backend is Live!")
    gr.Markdown("The FastAPI server is running. You can access the Swagger API documentation at [/docs](/docs).")

# Mount your FastAPI application onto the Gradio container at '/status'
# This makes FastAPI the primary application on the root domain
app = gr.mount_gradio_app(app, demo, path="/status")
