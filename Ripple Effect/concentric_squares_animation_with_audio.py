import os
import math
from PIL import Image, ImageDraw
import imageio.v2 as imageio
import gradio as gr
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def create_concentric_squares_frames(image, output_dir, initial_step_size=5, max_step_size=20, step_increment=1, scale_factor=2, grayscale=False, line_thickness=1):
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

def create_animation(images, output_dir, initial_step_size, max_step_size, step_increment, scale_factor, grayscale, line_thickness, fps=10):
    video_files = []
    for i, image_path in enumerate(images):
        image = Image.open(image_path)
        frames = create_concentric_squares_frames(image, output_dir, initial_step_size, max_step_size, step_increment, scale_factor=scale_factor, grayscale=grayscale, line_thickness=line_thickness)
        output_video_path = os.path.join(output_dir, f"concentric_squares_{i:04d}.mp4")
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
    output_dir = "concentric_square_frames"
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
    title="Concentric Squares Animation with Audio",
    description="Upload multiple images and an audio file, then adjust the parameters to create a concentric squares animation."
)

if __name__ == "__main__":
    iface.launch()
