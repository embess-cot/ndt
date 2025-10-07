import cv2
import subprocess
import os

# === Cấu hình ===
input_video = "video1.mp4"        # video gốc
output_video = "video1_4k.mp4"    # video xuất ra

# === Bước 1: Dùng ffmpeg tách audio và video ===
subprocess.run(["ffmpeg", "-i", input_video, "-q:a", "0", "-map", "a", "audio.aac"])
subprocess.run(["ffmpeg", "-i", input_video, "-q:v", "1", "-an", "video.mp4"])

# === Bước 2: Nâng cấp video bằng Real-ESRGAN ===
# ESRGAN có sẵn model x4 (nâng 4 lần) => từ 1080p -> 4K
subprocess.run([
    "realesrgan-ncnn-vulkan",
    "-i", "video.mp4",
    "-o", "video_upscaled.mp4",
    "-s", "4"   # scale x4
])

# === Bước 3: Ghép lại audio với video đã nâng cấp ===
subprocess.run([
    "ffmpeg", "-i", "video_upscaled.mp4", "-i", "audio.aac",
    "-c:v", "libx264", "-crf", "18", "-preset", "slow",
    "-c:a", "aac", "-b:a", "192k",
    output_video
])

# Xoá file tạm
os.remove("audio.aac")
os.remove("video.mp4")
os.remove("video_upscaled.mp4")

print("✅ Đã xuất video 4K:", output_video)
