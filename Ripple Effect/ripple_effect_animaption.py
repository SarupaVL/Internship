import os
from PIL import Image, ImageDraw
import math
import imageio

def create_concentric_circles(input_path, output_dir, step_size=5, num_points=360, scale_factor=2):
    # Load the image
    image = Image.open(input_path).convert("L")  # Convert to grayscale

    # Get the size of the image and scale it
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    # Create a new image for the output with increased resolution
    output_image = Image.new("L", (width, height), 255)  # White background
    draw = ImageDraw.Draw(output_image)

    # Center coordinates
    center_x = width // 2
    center_y = height // 2

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Draw concentric circles covering the entire image and save each step
    max_radius = int(math.hypot(center_x, center_y))  # Distance from center to the farthest corner
    step_counter = 0

    for radius in range(0, max_radius, step_size):
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            
            if 0 <= x < width and 0 <= y < height:
                intensity = image.getpixel((x // scale_factor, y // scale_factor))
                thickness = max(1, int((225 - intensity) / 225 * step_size))
                next_angle = ((i + 1) / num_points) * 2 * math.pi
                next_x = int(center_x + radius * math.cos(next_angle))
                next_y = int(center_y + radius * math.sin(next_angle))
                
                draw.line([x, y, next_x, next_y], fill=0, width=thickness)

        # Save each step as an image
        output_image_path = os.path.join(output_dir, f"step_{step_counter:04d}.jpg")
        output_image.save(output_image_path)
        print(f"Saved: {output_image_path}")
        step_counter += 1

    return step_counter

def create_gif(image_dir, output_gif_path, duration=0.1):
    images = []
    for file_name in sorted(os.listdir(image_dir)):
        if file_name.endswith(".jpg"):
            file_path = os.path.join(image_dir, file_name)
            images.append(imageio.imread(file_path))
            print(f"Added to GIF: {file_path}")

    if images:
        imageio.mimsave(output_gif_path, images, duration=duration)
        print(f"GIF saved: {output_gif_path}")
    else:
        print("No images found to create GIF.")

# Example usage
input_path = "C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\face.jpg"  # Replace with your input image path
output_dir = "C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\concentric_circle_steps"  # Replace with your desired output directory

# Get user input for step size and scale factor
try:
    step_size = int(input("Enter the step size: "))
    scale_factor = int(input("Enter the scale factor (e.g., 2 for double resolution): "))
    num_steps = create_concentric_circles(input_path, output_dir, step_size=step_size, scale_factor=scale_factor)
    print(f"Images created with step size {step_size} and scale factor {scale_factor}.")
    
    # Create GIF
    output_gif_path = f"C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\face_steppp_{step_size}_scale_{scale_factor}.gif"
    create_gif(output_dir, output_gif_path)
    print(f"GIF created: {output_gif_path}")
except ValueError:
    print("Invalid input. Please enter valid integers for the step size and scale factor.")
