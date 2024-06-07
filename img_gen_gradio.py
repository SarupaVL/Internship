import gradio as gr
from diffusers import StableDiffusionPipeline
import torch
from datetime import datetime
import asyncio

# Load the pre-trained Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"  # Use GPU if available, otherwise CPU

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

async def generate_images(prompt, cycles):
    images = []
    for cycle in range(cycles):
        # Generate an image
        result = await asyncio.to_thread(pipe, prompt)
        image = result.images[0]
        
        # Generate output file path with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"generated_image_{timestamp}_{cycle}.png"
        
        # Save the generated image
        await asyncio.to_thread(image.save, output_path)
        
        images.append(image)
        
    return images

def generate_image_sync(prompt, cycles):
    # Run the asynchronous function in an event loop
    return asyncio.run(generate_images(prompt, cycles))

# Create Gradio interface
iface = gr.Interface(
    fn=generate_image_sync,
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
