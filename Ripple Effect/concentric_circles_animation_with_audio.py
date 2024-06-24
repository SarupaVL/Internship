import os
import math
from PIL import Image, ImageDraw
import imageio.v2 as imageio
import gradio as gr
from moviepy.editor import VideoFileClip, AudioFileClip

def create_final_concentric_circles(image, output_dir, initial_step_size=5, max_step_size=20, step_increment=1, num_points=360, scale_factor=2):
    image = image.convert("RGB")
    width, height = image.size
    width *= scale_factor
    height *= scale_factor

    center_x = width // 2
    center_y = height // 2

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    step_counter = 0
    current_step_size = initial_step_size

    while current_step_size <= max_step_size:
        output_image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(output_image)

        max_radius = int(math.hypot(center_x, center_y))

        for radius in range(0, max_radius, current_step_size):
            for i in range(num_points):
                angle = (i / num_points) * 2 * math.pi
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))

                if 0 <= x < width and 0 <= y < height:
                    r, g, b = image.getpixel((x // scale_factor, y // scale_factor))
                    intensity = (r + g + b) // 3
                    thickness = max(1, int((225 - intensity) / 225 * current_step_size))
                    next_angle = ((i + 1) / num_points) * 2 * math.pi
                    next_x = int(center_x + radius * math.cos(next_angle))
                    next_y = int(center_y + radius * math.sin(next_angle))

                    draw.line([x, y, next_x, next_y], fill=(r, g, b), width=thickness)

        output_image_path = os.path.join(output_dir, f"step_{step_counter:04d}.jpg")
        output_image.save(output_image_path)
        print(f"Saved: {output_image_path}")
        step_counter += 1
        current_step_size += step_increment

    return step_counter

def create_mp4(image_dir, output_mp4_path, fps=10):
    images = []
    for file_name in sorted(os.listdir(image_dir)):
        if isinstance(file_name, str) and file_name.endswith(".jpg"):
            file_path = os.path.join(image_dir, file_name)
            image = imageio.imread(file_path)
            images.append(image)
            print(f"Added to MP4: {file_path}")

    imageio.mimwrite(output_mp4_path, images, fps=fps, codec='libx264')
    print(f"MP4 saved: {output_mp4_path}")

def add_audio_to_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path).set_duration(video_clip.duration)
    video_with_audio = video_clip.set_audio(audio_clip)
    video_with_audio.write_videofile(output_path, codec='libx264')
    print(f"Video with audio saved: {output_path}")

def process_image(input_image, initial_step_size, max_step_size, step_increment, scale_factor, audio_file=None):
    output_dir = "concentric_circle_steps"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    num_steps = create_final_concentric_circles(input_image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor=scale_factor)
    print(f"Final images created with initial step size {initial_step_size}, max step size {max_step_size}, step increment {step_increment}, and scale factor {scale_factor}.")

    output_mp4_path = "concentric_circles_animation.mp4"
    create_mp4(output_dir, output_mp4_path)

    if audio_file is not None:
        audio_file_path = audio_file.name
        final_output_path = "concentric_circles_animation_with_audio.mp4"
        add_audio_to_video(output_mp4_path, audio_file_path, final_output_path)
        return final_output_path
    else:
        return output_mp4_path

iface = gr.Interface(
    fn=process_image,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Number(label="Initial Step Size"),
        gr.Number(label="Max Step Size"),
        gr.Number(label="Step Increment"),
        gr.Number(label="Scale Factor"),
        gr.File(label="Upload Audio (Optional)", type="filepath")
    ],
    outputs=gr.Video(label="Concentric Circles Animation with Audio"),
    title="Concentric Circles Animation",
    description="Upload an image and optional audio, then adjust the parameters to create a concentric circles animation.",
)

if __name__ == "__main__":
    iface.launch()
