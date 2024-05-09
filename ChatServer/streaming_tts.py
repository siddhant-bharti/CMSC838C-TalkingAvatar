import os
import time
import torch
import torchaudio
import concurrent.futures
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import logging
import random
import re
import threading


locks = [threading.Lock() for i in range(8)]

model_ = []
gpt_cond_latent_ = []
speaker_embedding_ = []

def init_model():
    global model_, gpt_cond_latent_, speaker_embedding_
    config = XttsConfig()
    config.load_json("/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/models/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json")
    model = Xtts.init_from_config(config)
    model.load_checkpoint(config, checkpoint_dir="/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/models/tts/tts_models--multilingual--multi-dataset--xtts_v2")
    model.cuda()
    gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["oprah1.wav"])
    model_.append(model)
    gpt_cond_latent_.append(gpt_cond_latent)
    speaker_embedding_.append(speaker_embedding)


init_model()
init_model()
init_model()
init_model()
init_model()
init_model()
# init_model()
# init_model()


def get_chunks(idx, text_to_speak):
    global model_, gpt_cond_latent_, speaker_embedding_
    with locks[idx]:
        return model_[idx].inference_stream(
            text_to_speak,
            "en",
            gpt_cond_latent_[idx],
            speaker_embedding_[idx]
        )



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


def run_tts_streaming(text_to_speak, file_to_save=None):
    time.sleep(random.random())
    t0 = time.perf_counter()
    # with lock:
    #     chunks = model.inference_stream(
    #         text_to_speak,
    #         "en",
    #         gpt_cond_latent,
    #         speaker_embedding
    #     )
    chunks = get_chunks(random.randint(0,5), text_to_speak)

    wav_chuncks = []
    try:
        for i, chunk in enumerate(chunks):
            if i == 0:
                print(f"Time to first chunck: {time.perf_counter() - t0}")
            # print(f"Received chunk {i} of audio length {chunk.shape[-1]}")
            wav_chuncks.append(chunk)
        # wav = torch.cat(wav_chuncks, dim=0)
        t1 = time.perf_counter()
        print(f"Creating streaming audio took {t1 - t0} secs")
        if file_to_save:
            torchaudio.save(file_to_save, wav.squeeze().unsqueeze(0).cpu(), 24000)
        else:
            return wav_chuncks
    except Exception as e:
        # logging.exception("run_tts_streaming failed")
        print(f"run_tts_streaming failed for {text_to_speak}. {str(e)}")
        return wav_chuncks


def run_tts_streaming_1(text_to_speak, file_to_save=None):
    """This parallelizes across sentences"""
    t1 = time.perf_counter()
    text_to_speak = text_to_speak.replace("\n", "")
    futures = []
    sentences = []
    tmp_sentences = text_to_speak.split('.')
    for sentence in tmp_sentences:
        if len(sentence) < 5:
            continue
        sentences.append(sanitize_text(sentence))
    wav_chuncks = []
    print(f"sentences: {sentences}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for sentence in sentences[:6]:
            futures.append(executor.submit(run_tts_streaming, sentence))
        for future in futures:
            wav_chuncks.append(future.result())
        # wav = torch.cat(wav_chuncks, dim=0)
        # torchaudio.save(file_to_save, wav.squeeze().unsqueeze(0).cpu(), 24000)
    # for sentence in sentences:
    #     wav_chuncks.append(run_tts_streaming(sentence))
    t2 = time.perf_counter()
    print(f"Text: {text_to_speak}")
    print(f"Parallel audio generation time: {t2-t1} secs")


if __name__ == '__main__':
    while True:
        text_to_speak = ask_me_something = input(">>Generate streaming audio for: ")
        file_to_save = "./tts_testing_streaming.wav"
        run_tts_streaming(text_to_speak, file_to_save)
