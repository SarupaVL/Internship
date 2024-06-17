from PIL import Image, ImageDraw
import math

def create_concentric_circles(input_path, output_path, step_size=5, num_points=360, scale_factor=2):
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

    # Draw concentric circles covering the entire image
    max_radius = int(math.hypot(center_x, center_y))  # Distance from center to the farthest corner
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

    # Save the result
    output_image.save(output_path)

    # Display the result
    output_image.show()

# Example usage with interactive input for step size and scale factor
input_path = "C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\face.jpg"  # Replace with your input image path

while True:
    step_size = input("Enter the step size (or type 'stop' to end): ")
    if step_size.lower() == 'stop':
        break
    try:
        step_size = int(step_size)
        scale_factor = int(input("Enter the scale factor (e.g., 2 for double resolution): "))
        output_path = f"C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\face_step_{step_size}_scale_{scale_factor}.jpg"  # Replace with your desired output image path
        create_concentric_circles(input_path, output_path, step_size=step_size, scale_factor=scale_factor)
        print(f"Image created with step size {step_size} and scale factor {scale_factor}: {output_path}")
    except ValueError:
        print("Invalid input. Please enter valid integers for the step size and scale factor.")
