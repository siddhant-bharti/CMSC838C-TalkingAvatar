import time

from TTS.api import TTS

from utils import get_device

# Get device
device = get_device()

# Init TTS
# Model with best audio quality I could find is tts_models/multilingual/multi-dataset/xtts_v2
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def run_tts(text_to_speak, file_to_save):
    t1 = time.perf_counter()
    tts.tts_to_file(text=text_to_speak, speaker_wav="./oprah1.wav", language="en", file_path=file_to_save)
    t2 = time.perf_counter()
    print(f"Creating audio took {t2 - t1} secs")


if __name__ == '__main__':
    while True:
        text_to_speak = ask_me_something = input(">>Generate audio for: ")
        file_to_save = "./tts_testing_vanilla.wav"
        run_tts(text_to_speak, file_to_save)
