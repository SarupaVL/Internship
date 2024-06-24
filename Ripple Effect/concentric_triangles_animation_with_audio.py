import os
import math
from PIL import Image, ImageDraw
import imageio.v2 as imageio
import gradio as gr
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def draw_thick_line(draw, start, end, thickness, fill):
    #Draws a thick line by drawing multiple lines perpendicular to the main line.
    start_x, start_y = start
    end_x, end_y = end
    dx = end_x - start_x
    dy = end_y - start_y
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)

    for i in range(thickness):
        offset_angle = angle + math.pi / 2
        offset_x = math.cos(offset_angle) * (i - thickness // 2)
        offset_y = math.sin(offset_angle) * (i - thickness // 2)
        draw.line([(start_x + offset_x, start_y + offset_y), (end_x + offset_x, end_y + offset_y)], fill=fill)

def create_concentric_triangles_frames(image, output_dir, initial_step_size=5, max_step_size=20, step_increment=1, scale_factor=2, grayscale=False, line_thickness=1):
    image = image.convert("RGB")
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    frames = []
    current_step_size = initial_step_size

    # Calculate the maximum radius to cover the entire image
    max_radius = int(math.hypot(width, height))

    while current_step_size <= max_step_size:
        output_image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(output_image)

        for radius in range(0, max_radius, current_step_size):
            # Calculate the triangle vertices to span the entire image
            top_vertex = (width // 2, height // 2 - radius)
            left_vertex = (int(width // 2 - radius * math.sqrt(3) / 2), int(height // 2 + radius / 2))
            right_vertex = (int(width // 2 + radius * math.sqrt(3) / 2), int(height // 2 + radius / 2))

            triangle_vertices = [top_vertex, left_vertex, right_vertex, top_vertex]

            for i in range(len(triangle_vertices) - 1):
                start_x, start_y = triangle_vertices[i]
                end_x, end_y = triangle_vertices[i + 1]
                num_steps = max(abs(end_x - start_x), abs(end_y - start_y))

                # Ensure num_steps is at least 1 to avoid division by zero
                if num_steps == 0:
                    num_steps = 1

                for step in range(num_steps + 1):
                    x = start_x + step * (end_x - start_x) // num_steps
                    y = start_y + step * (end_y - start_y) // num_steps

                    if 0 <= x < width and 0 <= y < height:
                        r, g, b = image.getpixel((x // scale_factor, y // scale_factor))
                        if grayscale:
                            intensity = (r + g + b) // 3
                            r, g, b = intensity, intensity, intensity
                        thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                        draw_thick_line(draw, (x, y), (x + 1, y), thickness, fill=(r, g, b))

        frame_path = os.path.join(output_dir, f"frame_{current_step_size}.jpg")
        output_image.save(frame_path)
        frames.append(imageio.imread(frame_path))
        current_step_size += step_increment

    return frames

def create_animation(images, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness, fps=10):
    video_files = []
    for i, image_path in enumerate(images):
        image = Image.open(image_path)
        frames = create_concentric_triangles_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor=scale_factor, grayscale=grayscale, line_thickness=line_thickness)
        output_video_path = os.path.join(output_dir, f"concentric_triangles_{i:04d}.mp4")
        imageio.mimsave(output_video_path, frames, fps=fps)
        video_files.append(output_video_path)
        print(f"Saved: {output_video_path}")

    return video_files

def concatenate_videos(video_files, output_path):
    clips = [VideoFileClip(file) for file in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec='libx264')
    print(f"Concatenated video saved: {output_path}")

def add_audio_to_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path).set_duration(video_clip.duration)
    video_with_audio = video_clip.set_audio(audio_clip)
    video_with_audio.write_videofile(output_path, codec='libx264')
    print(f"Video with audio saved: {output_path}")

def process_images(images, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness, audio_file):
    output_dir = "concentric_triangle_frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_files = create_animation(images, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness)
    concatenated_video_path = "concatenated_animation.mp4"
    concatenate_videos(video_files, concatenated_video_path)

    final_output_path = "final_animation_with_audio.mp4"
    add_audio_to_video(concatenated_video_path, audio_file, final_output_path)

    return final_output_path

iface = gr.Interface(
    fn=process_images,
    inputs=[
        gr.File(label="Upload Images", type="filepath", file_count="multiple"),
        gr.Number(label="Initial Step Size"),
        gr.Number(label="Max Step Size"),
        gr.Number(label="Step Increment"),
        gr.Number(label="Scale Factor"),
        gr.Checkbox(label="Grayscale"),
        gr.Number(label="Line Thickness"),
        gr.File(label="Upload Audio", type="filepath")
    ],
    outputs=gr.Video(label="Final Animation with Audio"),
    title="Concentric Triangles Animation with Audio",
    description="Upload multiple images and an audio file, then adjust the parameters to create a concentric triangles animation."
)

if __name__ == "__main__":
    iface.launch()
