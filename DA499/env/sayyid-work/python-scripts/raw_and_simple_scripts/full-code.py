import torch
from TTS.api import TTS
import torchaudio

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

with open("C:\\Users\\sauui\\XTTS-project\\نص_علمي.txt", "r", encoding="utf-8") as f:
    my_text = f.read()

  
output = tts.tts(
    text=my_text,
    #text="نص_علمي.txt"
    speaker_wav="غرباء.wav",
    language="ar",
    temperature=0.75,
    top_k=40,
    top_p=0.9,
    repetition_penalty=8.0,
    gpt_cond_len=6,
    gpt_cond_chunk_len=6
)

torchaudio.save("test5.wav", torch.tensor(output).unsqueeze(0), 24000)
