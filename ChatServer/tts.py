import time
import torch
from TTS.api import TTS
import re

from utils import get_device

# Get device
device = get_device()

# Init TTS
# Model with best audio quality I could find is tts_models/multilingual/multi-dataset/xtts_v2
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def sanitize_text(generated_text):
    """Remove all the special tokens and the emojis that LLaMA2 generates.
    """
    cleaned_text = re.sub(r'\*.*?\*', '', generated_text)
    cleaned_text = re.sub(r'\<.*?\>', '', cleaned_text)

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # Replace matched characters with an empty string
    cleaned_text = emoji_pattern.sub('', cleaned_text)
    return cleaned_text


def run_tts(text_to_speak, file_to_save):
    text_to_speak = text_to_speak.replace("\n", "")
    futures = []
    sentences = []
    tmp_sentences = text_to_speak.split('.')
    for sentence in tmp_sentences:
        if len(sentence) < 5:
            continue
        sentences.append(sanitize_text(sentence))
    t1 = time.perf_counter()
    tts.tts_to_file(text=" ".join(sentences), speaker_wav="./oprah1.wav", language="en", file_path=file_to_save)
    t2 = time.perf_counter()
    print(f"Text: {text_to_speak}")
    print(f"Audio generation time: {t2 - t1} secs")


if __name__ == '__main__':
    while True:
        text_to_speak = ask_me_something = input(">>Generate audio for: ")
        file_to_save = "./tts_testing_vanilla.wav"
        run_tts(text_to_speak, file_to_save)
