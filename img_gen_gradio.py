import gradio as gr
from diffusers import StableDiffusionPipeline
import torch
from datetime import datetime

# Load the pre-trained Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"
device = "cpu"  # Use CPU

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

def generate_image(prompt, cycles):
    images = []
    for cycle in range(cycles):
        # Generate an image
        image = pipe(prompt).images[0]
        
        # Generate output file path with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"generated_image_{timestamp}_{cycle}.png"
        
        # Save the generated image
        image.save(output_path)
        
        images.append(image)
        yield images  # Update the interface in real-time

# Create Gradio interface
iface = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter a text prompt here...", label="Prompt"), 
        gr.Slider(minimum=1, maximum=10, step=1, value=1, label="Number of Cycles")
    ],
    outputs=gr.Gallery(label="Generated Images"),
    title="Text-to-Image Generation",
    description="Enter a text prompt to generate images using Stable Diffusion. Specify the number of cycles to generate multiple images.",
)

# Launch the web application
if __name__ == "__main__":
    iface.launch(share=True)
