from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load your video
video_path = "bear_identity_decomposed.mp4"  # Replace with your video file path
output_video_path = "bear_identity_decomposed_text.mp4"  # Replace with your output video file path
video_path = "4_bears_full.mp4"  # Replace with your video file path
output_video_path = "4_bears_full_text.mp4"  # Replace with your output video file path
video_path = "4_bears_fg.mp4"  # Replace with your video file path
output_video_path = "4_bears_fg_text.mp4"  # Replace with your output video file path
video_path = "optimization_track.mp4"  # Replace with your video file path
output_video_path = "optimization_track_text.mp4"  # Replace with your output video file path
video = VideoFileClip(video_path)

# Create text clips
# texts = ["Unseen views", "Background", "Foreground", "Geometry (Normal map)"]
# texts = ["Unseen [Identity] views", "Make it a grizzly bear", "Make it a panda", "Make it a polar bear"]
texts = ["GT view", "Learned view","Editted scene","Background","Foreground", "Depth map","Normal map"]

text_clips = []

# Set font size and colors
fontsize = 30
text_color = 'white'
bg_color = 'black'
padding_height = 100  # Height of the text box

# Create a text clip for each text
for text in texts:
    text_clip = TextClip(text, fontsize=fontsize, color=text_color, bg_color=bg_color, size=(video.w / len(texts), padding_height))
    text_clips.append(text_clip.set_duration(video.duration))

# Positioning the text clips
# Starting from the center and adjusting horizontal offsets
offsets = [0, 994, 1988, 2982]  # Adjust these values to disturb horizontally
offsets = [0, 320, 640, 960, 1280, 1600, 1920]  # Adjust these values to disturb horizontally

text_positions = [(offset, video.h - padding_height) for offset in offsets]

# Set positions for each text clip
for i, text_clip in enumerate(text_clips):
    text_clips[i] = text_clip.set_pos(text_positions[i])  # Set the position

# Create a composite video with the text clips
final_video = CompositeVideoClip([video] + text_clips)

# Write the final video to a file
final_video.write_videofile(output_video_path, codec="libx264")
