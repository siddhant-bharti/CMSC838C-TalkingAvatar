import torch
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline
)

from utils import (
    get_device,
    get_torch_dtype
)


device = get_device()
torch_dtype = get_torch_dtype()

stt_model_id = "openai/whisper-small"

stt_model = AutoModelForSpeechSeq2Seq.from_pretrained(
    stt_model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
stt_model.to(device)

stt_processor = AutoProcessor.from_pretrained(stt_model_id)

stt_pipe = pipeline(
    "automatic-speech-recognition",
    model=stt_model,
    tokenizer=stt_processor.tokenizer,
    feature_extractor=stt_processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)


def run_stt(input_audio_path):
    """We are not doing streaming or parallelization here because we want to send the entire transcript as context to
    the LLM.
    """
    return stt_pipe(input_audio_path, generate_kwargs = {"language":"<|en|>","task":"transcribe"})["text"]


if __name__ == '__main__':
    print(run_stt("oprah1.wav"))
