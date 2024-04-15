import time
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def run_tts(text_to_speak, file_to_save):
    tts.tts_to_file(text=text_to_speak, speaker_wav="oprah1.wav", language="en", file_path=file_to_save)


if __name__ == '__main__':
    # Run TTS
    # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
    # Text to speech list of amplitude values as output

    t1 = time.perf_counter()
    text_to_speak = "Oh no, I can tell you're feeling stressed!  It's completely normal to feel overwhelmed at times, but there are many things you can do to manage stress. Have you tried taking a few deep breaths, going for a walk, or practicing some relaxation techniques like meditation or yoga? These can really help calm your mind and body. 🧘‍♀️ If you ever need to talk about it, I'm here to listen. 🤗"
    wav = tts.tts_to_file(text=text_to_speak, speaker_wav="oprah1.wav", language="en", file_path="../../input5.wav")
    t2 = time.perf_counter()
    print(f"Creating audio took {t2-t1} secs")