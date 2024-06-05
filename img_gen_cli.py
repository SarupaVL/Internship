#This is the code for a stable diffuser cli and it saves the image using timestamp

import argparse
from diffusers import StableDiffusionPipeline
import torch
from datetime import datetime

def generate_image(prompt):
    # Load the pre-trained Stable Diffusion model
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cpu"  # Use CPU

    # Initialize the pipeline
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to(device)

    # Generate an image
    image = pipe(prompt).images[0]

    # Generate output file path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"generated_image_{timestamp}.png"

    # Save the generated image
    image.save(output_path)
    print(f"Image generated and saved as '{output_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an image from a text prompt using Stable Diffusion.")
    parser.add_argument("prompt", type=str, help="The text prompt to generate the image from.")
    
    args = parser.parse_args()
    generate_image(args.prompt)
