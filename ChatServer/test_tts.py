import time
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
t1 = time.perf_counter()
text_to_speak = "Remember to breathe. The key to managing stress is not just tackling what's on your plate, but also ensuring you replenish your spirit. Prioritize your tasks, focus on one thing at a time, and don't forget to take moments for yourself. You have the power within you to overcome this. Trust that you can handle it, and you will"
wav = tts.tts_to_file(text=text_to_speak, speaker_wav="oprah1.wav", language="en", file_path="../output.wav")
t2 = time.perf_counter()
print(f"Creating audio took {t2-t1} secs")
