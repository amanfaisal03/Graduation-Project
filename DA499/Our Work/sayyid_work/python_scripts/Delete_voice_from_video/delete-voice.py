import moviepy.editor as mp

# تحميل الفيديو
video = mp.VideoFileClip(
    "C:\\Users\\sauui\\Downloads\\Deep Learning _ What is Deep Learning_ _ Deep Learning Tutorial For Beginners _ 2023 _ Simplilearn.mp4"
)

# إزالة الصوت
silent_video = video.without_audio()

# حفظ الفيديو الجديد
silent_video.write_videofile("silent_video.mp4", codec="libx264", audio_codec="aac")

print("✅ تم حفظ الفيديو بدون صوت.")
