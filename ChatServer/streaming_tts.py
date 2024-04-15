import os
import time
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

print("Loading model...")
config = XttsConfig()
config.load_json("/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/models/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/models/tts/tts_models--multilingual--multi-dataset--xtts_v2")
model.cuda()

print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["oprah1.wav"])

print("Inference...")
t0 = time.perf_counter()
chunks = model.inference_stream(
    "Oh no, I can tell you're feeling stressed!  It's completely normal to feel overwhelmed at times, but there are many things you can do to manage stress. Have you tried taking a few deep breaths, going for a walk, or practicing some relaxation techniques like meditation or yoga? These can really help calm your mind and body. 🧘‍♀️ If you ever need to talk about it, I'm here to listen. 🤗",
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
    # torchaudio.save(f"stream_{i}.wav", chunk.squeeze().unsqueeze(0).cpu(), 24000)
wav = torch.cat(wav_chuncks, dim=0)
torchaudio.save("xtts_streaming.wav", wav.squeeze().unsqueeze(0).cpu(), 24000)
t1 = time.perf_counter()
print(f"Creating audio took {t1-t0} secs")