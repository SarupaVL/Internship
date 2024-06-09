import gradio as gr
from diffusers import StableDiffusionPipeline
import torch
from datetime import datetime
from PIL import Image
from gfpgan import GFPGANer
import numpy as np

# Load the pre-trained Stable Diffusion v1.5 model
model_id = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

# Load the GFPGAN model
gfpgan = GFPGANer(
    model_path='C:\\Users\\laksh\\GFPGAN\\experiments\\pretrained_models\\GFPGANv1.4.pth',
    upscale=4,
    arch='clean',
    channel_multiplier=2,
    bg_upsampler=None
)

def generate_and_upscale_image(prompt):
    # Generate an image
    image = pipe(prompt).images[0]

    # Convert PIL image to numpy array
    img_array = np.array(image)

    # Upscale the image using GFPGAN
    _, _, restored_img = gfpgan.enhance(img_array, has_aligned=False, only_center_face=False, paste_back=True)

    # Convert numpy array back to PIL image
    upscaled_image = Image.fromarray(restored_img)

    # Generate output file path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"generated_image_{timestamp}.png"
    upscaled_output_path = f"upscaled_image_{timestamp}.png"

    # Save the generated and upscaled images
    image.save(output_path)
    upscaled_image.save(upscaled_output_path)

    return upscaled_image

# Create Gradio interface
iface = gr.Interface(
    fn=generate_and_upscale_image,
    inputs="text",
    outputs="image",
    title="Text-to-Image Generation and Upscaling",
    description="Enter a text prompt to generate an image using Stable Diffusion and upscale it using GFPGAN.",
)

# Launch the web application
if __name__ == "__main__":
    iface.launch(share=True)
