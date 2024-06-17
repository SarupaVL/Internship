import os
from PIL import Image, ImageDraw
import math
import imageio

def create_final_concentric_circles(input_path, output_dir, initial_step_size=5, max_step_size=20, step_increment=1, num_points=360, scale_factor=2):
    # Load the image
    image = Image.open(input_path).convert("L")  # Convert to grayscale

    # Get the size of the image and scale it
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    # Center coordinates
    center_x = width // 2
    center_y = height // 2

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    step_counter = 0
    current_step_size = initial_step_size

    while current_step_size <= max_step_size:
        # Create a new image for each step with increased resolution
        output_image = Image.new("L", (width, height), 255)  # White background
        draw = ImageDraw.Draw(output_image)

        max_radius = int(math.hypot(center_x, center_y))  # Distance from center to the farthest corner
        
        for radius in range(0, max_radius, current_step_size):
            for i in range(num_points):
                angle = (i / num_points) * 2 * math.pi
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                
                if 0 <= x < width and 0 <= y < height:
                    intensity = image.getpixel((x // scale_factor, y // scale_factor))
                    thickness = max(1, int((225 - intensity) / 225 * current_step_size))
                    next_angle = ((i + 1) / num_points) * 2 * math.pi
                    next_x = int(center_x + radius * math.cos(next_angle))
                    next_y = int(center_y + radius * math.sin(next_angle))
                    
                    draw.line([x, y, next_x, next_y], fill=0, width=thickness)

        # Save the final image for the current step size
        output_image_path = os.path.join(output_dir, f"step_{step_counter:04d}.jpg")
        output_image.save(output_image_path)
        print(f"Saved: {output_image_path}")
        step_counter += 1
        current_step_size += step_increment

    return step_counter

def create_mp4(image_dir, output_mp4_path, fps=10):
    writer = imageio.get_writer(output_mp4_path, fps=fps, codec='libx264')
    for file_name in sorted(os.listdir(image_dir)):
        if file_name.endswith(".jpg"):
            file_path = os.path.join(image_dir, file_name)
            image = imageio.imread(file_path)
            writer.append_data(image)
            print(f"Added to MP4: {file_path}")
    writer.close()
    print(f"MP4 saved: {output_mp4_path}")

def main():
    input_path = "C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\face.jpg"  # Replace with your input image path
    output_dir = "C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\concentric_circle_steps"  # Replace with your desired output directory

    try:
        initial_step_size = int(input("Enter the initial step size: "))
        max_step_size = int(input("Enter the max step size: "))
        step_increment = int(input("Enter the step increment: "))
        scale_factor = int(input("Enter the scale factor (e.g., 2 for double resolution): "))
        
        num_steps = create_final_concentric_circles(input_path, output_dir, initial_step_size=initial_step_size, max_step_size=max_step_size, step_increment=step_increment, scale_factor=scale_factor)
        print(f"Final images created with initial step size {initial_step_size}, max step size {max_step_size}, step increment {step_increment}, and scale factor {scale_factor}.")
        
        # Create MP4
        output_mp4_path = f"C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\ffface_step_{initial_step_size}_to_{max_step_size}_increment_{step_increment}_scale_{scale_factor}.mp4"
        create_mp4(output_dir, output_mp4_path)
        print(f"MP4 created: {output_mp4_path}")
    except ValueError:
        print("Invalid input. Please enter valid integers for the step size, max step size, step increment, and scale factor.")

if __name__ == "__main__":
    main()
