import gradio as gr
from diffusers import StableDiffusionPipeline
import torch
from datetime import datetime

# Load the pre-trained Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"
device = "cpu"  # Use CPU

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

def generate_image(prompt):
    # Generate an image
    image = pipe(prompt).images[0]
    
    # Generate output file path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"generated_image_{timestamp}.png"

    # Save the generated image
    image.save(output_path)
    
    return image

# Create Gradio interface
iface = gr.Interface(
    fn=generate_image,
    inputs="text",
    outputs="image",
    title="Text-to-Image Generation",
    description="Enter a text prompt to generate an image using Stable Diffusion.",
)

# Launch the web application
if __name__ == "__main__":
    iface.launch(share=True)
