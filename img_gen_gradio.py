import gradio as gr
from diffusers import StableDiffusionPipeline
from datetime import datetime
from PIL import Image
import torch
from realesrgan import RealESRGAN

# Load the pre-trained Stable Diffusion model once at startup
model_id = "runwayml/stable-diffusion-v1-5"  # Use the correct model ID for Stable Diffusion 1.5
device = "cpu"  # Use CPU

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

# Load the Real-ESRGAN model for upscaling
upscale_model = RealESRGAN(device, scale=4)  # Using scale 4x for upscaling
upscale_model.load_weights("RealESRGAN_x4plus.pth")  # Ensure you have the model weights

def generate_image(prompt):
    # Generate an image
    image = pipe(prompt, num_inference_steps=20, guidance_scale=7.5).images[0]
    
    # Upscale the generated image
    upscaled_image = upscale_model.predict(image)
    
    # Generate output file path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"generated_image_{timestamp}.png"

    # Save the upscaled image
    upscaled_image.save(output_path)
    
    return upscaled_image

# Create Gradio interface
iface = gr.Interface(
    fn=generate_image,
    inputs="text",
    outputs="image",
    title="Text-to-Image Generation",
    description="Enter a text prompt to generate an upscaled image using Stable Diffusion 1.5.",
)

# Launch the web application
if __name__ == "__main__":
    iface.launch()
