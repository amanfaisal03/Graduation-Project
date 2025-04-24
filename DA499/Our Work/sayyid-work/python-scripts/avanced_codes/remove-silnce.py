# Import required libraries
import numpy as np
from pydub.silence import split_on_silence
from pydub import AudioSegment, effects 
from scipy.io.wavfile import read, write
# Pass audio path
path =r'C:\Users\sauui\XTTS-project\merged_audio.wav'
rate, audio = read(path)
# make the audio in pydub audio segment format
aud = AudioSegment(audio.tobytes(),frame_rate = rate,
                     sample_width = audio.dtype.itemsize,channels = 1)
# use split on sience method to split the audio based on the silence, 
# here we can pass the min_silence_len as silent length threshold in ms and intensity thershold
audio_chunks = split_on_silence(
    aud,
    min_silence_len = 1500,
    silence_thresh = -45,
    keep_silence = 500,)
#audio chunks are combined here
audio_processed = sum(audio_chunks)
audio_processed = np.array(audio_processed.get_array_of_samples())
#Note the processed audio rate is not the same - it would be 1K 
print(audio_processed)
output_path = r"C:\Users\sauui\XTTS-project\sayyid-work\cleaned3.wav"
write(output_path, rate, audio_processed)