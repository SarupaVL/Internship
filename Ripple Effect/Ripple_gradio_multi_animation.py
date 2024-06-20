import os
import math
from PIL import Image, ImageDraw
import imageio.v2 as imageio
import gradio as gr
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def create_concentric_circles_frames(image, output_dir, initial_step_size=5, max_step_size=20, step_increment=1, num_points=360, scale_factor=2, grayscale=False, line_thickness=1):
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
            for i in range(num_points):
                angle = (i / num_points) * 2 * math.pi
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))

                if 0 <= x < width and 0 <= y < height:
                    r, g, b = image.getpixel((x // scale_factor, y // scale_factor))
                    if grayscale:
                        intensity = (r + g + b) // 3
                        r, g, b = intensity, intensity, intensity
                    thickness = max(line_thickness, int((225 - ((r + g + b) // 3)) / 225 * current_step_size))
                    next_angle = ((i + 1) / num_points) * 2 * math.pi
                    next_x = int(center_x + radius * math.cos(next_angle))
                    next_y = int(center_y + radius * math.sin(next_angle))

                    draw.line([x, y, next_x, next_y], fill=(r, g, b), width=thickness)

        frame_path = os.path.join(output_dir, f"frame_{current_step_size}.jpg")
        output_image.save(frame_path)
        frames.append(imageio.imread(frame_path))
        current_step_size += step_increment

    return frames

def create_animation(images, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness, fps=10):
    video_files = []
    for i, image_path in enumerate(images):
        image = Image.open(image_path)
        frames = create_concentric_circles_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor=scale_factor, grayscale=grayscale, line_thickness=line_thickness)
        output_video_path = os.path.join(output_dir, f"concentric_circles_{i:04d}.mp4")
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
    output_dir = "concentric_circle_frames"
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
    title="Concentric Circles Animation with Audio",
    description="Upload multiple images and an audio file, then adjust the parameters to create a concentric circles animation."
)

if __name__ == "__main__":
    iface.launch()
