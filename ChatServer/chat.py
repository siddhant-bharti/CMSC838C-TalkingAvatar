import re

import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

import multiprocessing

multiprocessing.set_start_method('spawn', force=True)

import time

from tts import run_tts
from ChatServer.streaming_tts import run_tts_streaming

import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.float16, token=True,
                                             device_map="auto")


# Function to simulate chat with Oprah Winfrey
def chat_with_oprah(user_input):
    generator = pipeline('text-generation', model='meta-llama/Llama-2-7b-chat-hf', torch_dtype=torch.float16,
                         token=True, device="cuda")
    # Crafting a prompt that includes Oprah's persona
    prompt = f"User: {user_input}\nOprah Winfrey: "

    # Generating Oprah Winfrey's response
    responses = generator(prompt, max_new_tokens=3, num_return_sequences=1)

    # Extracting and printing the generated text
    oprah_response = responses[0]['generated_text'].split("Oprah Winfrey: ")[-1]
    print(oprah_response)


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


def chat_with_oprah_streaming(user_input):
    prompt = f"""<s>[INST] <<SYS>>
        You are the famous celebrity talk show host Oprah Winfrey! You are talking to someone who needs you. Give very short, polite, and empathetic replies. Do not start your sentences
        with works like Oh and Ah. Directly being with the content. Use the following information to guide your responses:
        <</SYS>>

        What is your name? [/INST] My name is Oprah Winfrey </s><s>[INST] {user_input} [/INST]"""
    inputs = tok([prompt], return_tensors="pt").to("cuda")
    streamer = TextIteratorStreamer(tok, skip_prompt=True)
    generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=1500)

    processes = []

    start_time = time.time()

    # model_process = multiprocessing.Process(target=model.generate, kwargs=generation_kwargs)
    # model_process.start()
    # processes.append(model_process)

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    generated_text = ""
    sentences = []

    index = 0
    for new_text in streamer:
        # print(new_text, end='', flush=True)
        new_text = sanitize_text(new_text)

        # Append to the generated text
        generated_text += new_text

        if new_text == "":
            continue

        run_tts_streaming(generated_text, f"audio_chunk_{index}.wav")

        generated_text = ""
        index += 1

        # Append to the generated audio
        # call run_tts with new_text and file path like "{index}.wav"

        # audio_process = multiprocessing.Process(target=run_tts, args=(new_text, f"audio_chunk_{index}.wav"))
        # audio_process.start()
        # processes.append(audio_process)

    for process in processes:
        process.join()

    thread.join()

    end_time = time.time()

    print(f"Total time taken: {end_time - start_time}")

    # print("\n")
    return generated_text


if __name__ == '__main__':
    while True:
        ask_me_something = input(">>Me: ")
        user_input = f"""<s>[INST] <<SYS>>
        You are the famous celebrity talk show host Oprah Winfrey! You are talking to someone who needs you. Give very short, polite, and empathetic replies. Do not start your sentences
        with works like Oh and Ah. Directly being with the content. Use the following information to guide your responses:
        <</SYS>>

        What is your name? [/INST] My name is Oprah Winfrey </s><s>[INST] {ask_me_something} [/INST]"""
        print(sanitize_text(chat_with_oprah_streaming(user_input)))
