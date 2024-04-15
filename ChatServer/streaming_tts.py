import os
import time
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts


config = XttsConfig()
config.load_json("/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/models/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/models/tts/tts_models--multilingual--multi-dataset--xtts_v2")
model.cuda()

gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["oprah1.wav"])


def run_tts_streaming(text_to_speak, file_to_save=None):
    t0 = time.perf_counter()
    chunks = model.inference_stream(
        text_to_speak,
        "en",
        gpt_cond_latent,
        speaker_embedding
    )

    wav_chuncks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            print(f"Time to first chunck: {time.perf_counter() - t0}")
        print(f"Received chunk {i} of audio length {chunk.shape[-1]}")
        wav_chuncks.append(chunk)
    wav = torch.cat(wav_chuncks, dim=0)
    t1 = time.perf_counter()
    print(f"Creating audio took {t1 - t0} secs")
    if file_to_save:
        torchaudio.save(file_to_save, wav.squeeze().unsqueeze(0).cpu(), 24000)
    else:
        return wav


if __name__ == '__main__':
    while True:
        text_to_speak = ask_me_something = input(">>Generate streaming audio for: ")
        file_to_save = "./tts_testing_streaming.wav"
        run_tts_streaming(text_to_speak, file_to_save)
