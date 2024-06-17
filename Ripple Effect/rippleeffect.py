from PIL import Image, ImageDraw
import math

def create_concentric_circles(input_path, output_path, step_size=5, num_points=360):
    # Load the image
    image = Image.open(input_path).convert("L")  # Convert to grayscale

    # Get the size of the image
    width, height = image.size

    # Create a new image for the output
    output_image = Image.new("L", (width, height), 255)  # White background
    draw = ImageDraw.Draw(output_image)

    # Center coordinates
    center_x = width // 2
    center_y = height // 2

    # Draw concentric circles
    for radius in range(0, min(center_x, center_y), step_size):
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            
            if 0 <= x < width and 0 <= y < height:
                intensity = image.getpixel((x, y))
                thickness = max(1, int((255 - intensity) / 255 * step_size))
                next_angle = ((i + 1) / num_points) * 2 * math.pi
                next_x = int(center_x + radius * math.cos(next_angle))
                next_y = int(center_y + radius * math.sin(next_angle))
                
                draw.line([x, y, next_x, next_y], fill=0, width=thickness)

    # Save the result
    output_image.save(output_path)

    # Display the result
    output_image.show()

# Example usage
input_path = "C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\rip2.jpg"  # Replace with your input image path
output_path = "C:\\Users\\laksh\\Dropbox\\My PC (LAPTOP-6UJV2OF2)\\Downloads\\internship projects\\concentric_circles_effect2.jpg"  # Replace with your desired output image path
create_concentric_circles(input_path, output_path, step_size=5, num_points=360)
