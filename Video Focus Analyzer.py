import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip

# ✅ Set your actual folder path here
folder_path = r"C:\Path\To\Your\Videos"

if not os.path.exists(folder_path):
    print("❌ Error: Folder path does not exist.")
    exit()

results = []

def estimate_video_quality(video_path):
    cap = cv2.VideoCapture(video_path)
    sharpness_list = []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(total_frames // 10, 1)  # ✅ Avoid division by zero

    for i in range(0, total_frames, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_list.append(laplacian_var)

    cap.release()
    avg_sharpness = np.mean(sharpness_list) if sharpness_list else 0
    return avg_sharpness

def estimate_audio_quality(video_path):
    try:
        clip = VideoFileClip(video_path)
        audio = clip.audio
        if audio is None:
            return 0
        samples = audio.to_soundarray(fps=22050)
        volume = np.abs(samples).mean() * 100
        clip.close()
        return volume
    except Exception as e:
        print(f"⚠️ Audio error in {video_path}: {e}")
        return 0

# ✅ Loop through video files in the folder
for file_name in os.listdir(folder_path):
    if file_name.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        file_path = os.path.join(folder_path, file_name)
        video_score = estimate_video_quality(file_path)
        audio_score = estimate_audio_quality(file_path)
        results.append((file_name, video_score, audio_score))

# ✅ Sort videos by best sharpness
results.sort(key=lambda x: x[1], reverse=True)

# ✅ Save the report
output_path = os.path.join(folder_path, "video_quality_report.txt")
with open(output_path, "w") as f:
    if results:
        f.write(f"Best Focused Video: {results[0][0]}\n\n")
    f.write("Video Name".ljust(25) + "| Video Quality | Sound Quality\n")
    f.write("-" * 55 + "\n")
    for file_name, video_score, audio_score in results:
        f.write(f"{file_name.ljust(25)}| {video_score:>14.1f} | {audio_score:>14.1f}\n")

print("✅ Report saved:", output_path)
