# generate_image.py

from diffusers import StableDiffusionPipeline
import torch

# Load the pre-trained Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"
device = "cpu"

# Initialize the pipeline
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

# Define your prompt
prompt = "A beautiful sunset over a mountain range"

# Generate an image
image = pipe(prompt).images[0]

# Save the generated image
image.save("generated_image.png")

print("Image generated and saved as 'generated_image.png'")