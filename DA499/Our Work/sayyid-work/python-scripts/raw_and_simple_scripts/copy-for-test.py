import torch
from TTS.api import TTS
import torchaudio
import os
import time
import numpy as np
import pandas as pd

# تحميل البيانات من CSV
csv_path = r"C:\Users\sauui\XTTS-project\timing2_sentences_.csv"
df = pd.read_csv(csv_path)

# إعداد XTTS
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

speaker_wav = r"C:\Users\sauui\XTTS-project\sayyid-work\input-test-voice\غرباء.wav"
output_dir = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\original-video-voice"
os.makedirs(output_dir, exist_ok=True)

# توليد الصوت من كل صف في CSV
for idx, row in df.iterrows():
    text = row['text']
    start = row['start']
    end = row['end']
    print(f"\n🔊 Segment {idx+1}: {start} --> {end}")

    attempts = 0
    success = False

    while attempts < 3 and not success:
        try:
            output = tts.tts(
                text=text,
                speaker_wav=speaker_wav,
                language="ar",
                temperature=0.75,
                top_k=40,
                top_p=0.9,
                repetition_penalty=8.0,
                gpt_cond_len=6,
                gpt_cond_chunk_len=6
            )

            if isinstance(output, list):
                output = output[0]
            if isinstance(output, np.ndarray):
                output = torch.tensor(output)
            if not isinstance(output, torch.Tensor):
                raise ValueError(f"Output is not a tensor: {type(output)}")

            if output.ndim != 1:
                raise ValueError(f"Expected 1D tensor, got shape {output.shape}")

            output = output.unsqueeze(0)

            filename = f"{idx+1:03d}_from_{start:.2f}_to_{end:.2f}.wav"
            save_path = os.path.join(output_dir, filename)
            torchaudio.save(save_path, output, 24000)
            print(f"✅ Saved: {filename}")
            success = True

        except Exception as e:
            print(f"⚠️ Attempt {attempts+1} failed: {e}")
            torch.cuda.empty_cache()
            time.sleep(1)
            attempts += 1

    if not success:
        print(f"❌ Failed to generate segment {idx+1} after 3 tries.")
