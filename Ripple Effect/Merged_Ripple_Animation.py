import os
import math
from PIL import Image, ImageDraw
import imageio.v2 as imageio
import gradio as gr
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def draw_thick_line(draw, start, end, thickness, fill):
    start_x, start_y = start
    end_x, end_y = end
    dx = end_x - start_x
    dy = end_y - start_y
    angle = math.atan2(dy, dx)

    for i in range(thickness):
        offset_angle = angle + math.pi / 2
        offset_x = math.cos(offset_angle) * (i - thickness // 2)
        offset_y = math.sin(offset_angle) * (i - thickness // 2)
        draw.line([(start_x + offset_x, start_y + offset_y), (end_x + offset_x, end_y + offset_y)], fill=fill)

def create_frames(image, output_dir, ripple_type, initial_step_size=5, max_step_size=20, step_increment=1, scale_factor=2, grayscale=False, line_thickness=1):
    if ripple_type == "Circular":
        return create_concentric_circles_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness)
    elif ripple_type == "Square":
        return create_concentric_squares_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness)
    elif ripple_type == "Triangular":
        return create_concentric_triangles_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness)
    elif ripple_type == "Parallel Lines":
        return create_parallel_lines_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness)

def create_concentric_circles_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness):
    image = image.convert("RGB")
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    center_x = width // 2
    center_y = height // 2

    frames = []
    max_radius = int(math.hypot(center_x, center_y))
    current_step_size = initial_step_size

    while current_step_size <= max_step_size:
        output_image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(output_image)

        for radius in range(0, max_radius, current_step_size):
            for i in range(360):
                angle = (i / 360) * 2 * math.pi
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))

                if 0 <= x < width and 0 <= y < height:
                    r, g, b = image.getpixel((x // scale_factor, y // scale_factor))
                    if grayscale:
                        intensity = (r + g + b) // 3
                        r, g, b = intensity, intensity, intensity
                    thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                    next_angle = ((i + 1) / 360) * 2 * math.pi
                    next_x = int(center_x + radius * math.cos(next_angle))
                    next_y = int(center_y + radius * math.sin(next_angle))

                    draw.line([x, y, next_x, next_y], fill=(r, g, b), width=thickness)

        frame_path = os.path.join(output_dir, f"frame_{current_step_size}.jpg")
        output_image.save(frame_path)
        frames.append(imageio.imread(frame_path))
        current_step_size += step_increment

    return frames

def create_concentric_squares_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness):
    image = image.convert("RGB")
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    center_x = width // 2
    center_y = height // 2

    frames = []
    max_radius = int(math.hypot(center_x, center_y))
    current_step_size = initial_step_size

    while current_step_size <= max_step_size:
        output_image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(output_image)

        for radius in range(0, max_radius, current_step_size):
            top_left = (center_x - radius, center_y - radius)
            bottom_right = (center_x + radius, center_y + radius)
            
            for x in range(top_left[0], bottom_right[0] + 1):
                if 0 <= x < width:
                    y_top = top_left[1]
                    y_bottom = bottom_right[1]
                    if 0 <= y_top < height:
                        r, g, b = image.getpixel((x // scale_factor, y_top // scale_factor))
                        if grayscale:
                            intensity = (r + g + b) // 3
                            r, g, b = intensity, intensity, intensity
                        thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                        draw.line([x, y_top, x+1, y_top], fill=(r, g, b), width=thickness)
                    if 0 <= y_bottom < height:
                        r, g, b = image.getpixel((x // scale_factor, y_bottom // scale_factor))
                        if grayscale:
                            intensity = (r + g + b) // 3
                            r, g, b = intensity, intensity, intensity
                        thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                        draw.line([x, y_bottom, x+1, y_bottom], fill=(r, g, b), width=thickness)

            for y in range(top_left[1], bottom_right[1] + 1):
                if 0 <= y < height:
                    x_left = top_left[0]
                    x_right = bottom_right[0]
                    if 0 <= x_left < width:
                        r, g, b = image.getpixel((x_left // scale_factor, y // scale_factor))
                        if grayscale:
                            intensity = (r + g + b) // 3
                            r, g, b = intensity, intensity, intensity
                        thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                        draw.line([x_left, y, x_left, y+1], fill=(r, g, b), width=thickness)
                    if 0 <= x_right < width:
                        r, g, b = image.getpixel((x_right // scale_factor, y // scale_factor))
                        if grayscale:
                            intensity = (r + g + b) // 3
                            r, g, b = intensity, intensity, intensity
                        thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                        draw.line([x_right, y, x_right, y+1], fill=(r, g, b), width=thickness)

        frame_path = os.path.join(output_dir, f"frame_{current_step_size}.jpg")
        output_image.save(frame_path)
        frames.append(imageio.imread(frame_path))
        current_step_size += step_increment

    return frames

def create_concentric_triangles_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness):
    image = image.convert("RGB")
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    frames = []
    current_step_size = initial_step_size

    max_radius = int(math.hypot(width, height))

    while current_step_size <= max_step_size:
        output_image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(output_image)

        for radius in range(0, max_radius, current_step_size):
            top_vertex = (width // 2, height // 2 - radius)
            left_vertex = (int(width // 2 - radius * math.sqrt(3) / 2), int(height // 2 + radius / 2))
            right_vertex = (int(width // 2 + radius * math.sqrt(3) / 2), int(height // 2 + radius / 2))

            triangle_vertices = [top_vertex, left_vertex, right_vertex, top_vertex]

            for i in range(len(triangle_vertices) - 1):
                start_x, start_y = triangle_vertices[i]
                end_x, end_y = triangle_vertices[i + 1]
                num_steps = max(abs(end_x - start_x), abs(end_y - start_y))

                if num_steps == 0:
                    num_steps = 1

                for step in range(num_steps + 1):
                    x = start_x + step * (end_x - start_x) / num_steps
                    y = start_y + step * (end_y - start_y) / num_steps

                    if 0 <= x < width and 0 <= y < height:
                        r, g, b = image.getpixel((int(x) // scale_factor, int(y) // scale_factor))
                        if grayscale:
                            intensity = (r + g + b) // 3
                            r, g, b = intensity, intensity, intensity
                        thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                        draw_thick_line(draw, (x, y), (x + 1, y + 1), thickness, (r, g, b))

        frame_path = os.path.join(output_dir, f"frame_{current_step_size}.jpg")
        output_image.save(frame_path)
        frames.append(imageio.imread(frame_path))
        current_step_size += step_increment

    return frames

def create_parallel_lines_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness):
    image = image.convert("RGB")
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    frames = []
    current_step_size = initial_step_size

    while current_step_size <= max_step_size:
        output_image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(output_image)

        for y in range(0, height, current_step_size):
            for x in range(width):
                if 0 <= x < width and 0 <= y < height:
                    r, g, b = image.getpixel((x // scale_factor, y // scale_factor))
                    if grayscale:
                        intensity = (r + g + b) // 3
                        r, g, b = intensity, intensity, intensity
                    thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                    draw.line([x, y, x+1, y], fill=(r, g, b), width=thickness)

        frame_path = os.path.join(output_dir, f"frame_{current_step_size}.jpg")
        output_image.save(frame_path)
        frames.append(imageio.imread(frame_path))
        current_step_size += step_increment

    return frames

def create_gif(image_files, audio_file, output_dir, ripple_type, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness):
    frames = []
    for image_file in image_files:
        image = Image.open(image_file)
        frames += create_frames(image, output_dir, ripple_type, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness)

    gif_path = os.path.join(output_dir, "output.gif")
    imageio.mimsave(gif_path, frames, duration=0.1)

    if audio_file:
        gif_clip = VideoFileClip(gif_path)
        audio_clip = AudioFileClip(audio_file)
        audio_clip = audio_clip.subclip(0, gif_clip.duration)
        final_clip = gif_clip.set_audio(audio_clip)
        video_path = os.path.join(output_dir, "output_with_audio.mp4")
        final_clip.write_videofile(video_path, codec="libx264")
        return video_path

    return gif_path

def process_images(image_files, audio_file, ripple_type, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness):
    output_dir = "/mnt/data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return create_gif(image_files, audio_file, output_dir, ripple_type, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness)

# Create the Gradio interface
interface = gr.Interface(
    fn=process_images,
    inputs=[
        gr.File(label="Image Files", type="filepath", file_count="multiple"),
        gr.File(label="Audio File (optional)", type="filepath"),
        gr.Dropdown(choices=["Circular", "Square", "Triangular", "Parallel Lines"], label="Ripple Type"),
        gr.Number(label="Initial Step Size", value=5),
        gr.Number(label="Max Step Size", value=20),
        gr.Number(label="Step Increment", value=1),
        gr.Number(label="Scale Factor", value=2),
        gr.Checkbox(label="Grayscale", value=False),
        gr.Number(label="Line Thickness", value=1)
    ],
    outputs=gr.Video(label="Output GIF/Video")
)

interface.launch()
