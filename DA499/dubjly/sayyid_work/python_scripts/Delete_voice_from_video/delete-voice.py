import moviepy.editor as mp

# مسار الفيديو الأصلي (بصوت)
input_video_path = r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\dubjly\video.mp4"

# مسار حفظ الفيديو الجديد (بدون صوت)
output_video_path = r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\dubjly\sayyid_work\video_and_csv\silent_video.mp4"

# تحميل الفيديو
video = mp.VideoFileClip(input_video_path)

# إزالة الصوت
silent_video = video.without_audio()

# حفظ الفيديو الجديد
silent_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

print("✅ تم حفظ الفيديو بدون صوت.")
