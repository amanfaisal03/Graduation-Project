import csv

# اسم ملف النص الأصلي
file_path = r"C:\Users\sauui\XTTS-project\sayyid-work\test-text\نص-التجربة.txt"

# اسم ملف CSV الناتج
output_csv = "timing_sentences_.csv"

# مصفوفة لتخزين النتائج
results = []

# نقرأ كل الأسطر من الملف
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# نمر على كل سطر
for index, line in enumerate(lines):
    line = line.strip()

    if line == "":
        continue

    if "]" not in line:
        print(f"⚠️ سطر غير صالح (ما في ]): {line}")
        continue

    try:
        time_part, text_part = line.split("]")
        time_part = time_part[1:]  # إزالة [
        text = text_part.strip()

        if "-" in time_part:
            start_time, end_time = time_part.split("-")
            start_time = float(start_time.strip())
            end_time = float(end_time.strip())
        else:
            # سطر يحتوي فقط على [start]
            start_time = float(time_part.strip())
            end_time = start_time + 5  # نضيف 5 ثواني كمدة افتراضية
            print(f"ℹ️ تم إنشاء نهاية مؤقتة للسطر: {line}")

        voices = f"sentence-voice_{index:03}.wav"
        results.append([voices, start_time, end_time, text])

    except Exception as e:
        print(f"❌ خطأ عند السطر {index}: {line} - {e}")

# نكتب النتائج في ملف CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["voices", "start", "end", "text"])
    writer.writerows(results)

print("✅ تم استخراج البيانات وحفظها في timing_sentences_.csv")
