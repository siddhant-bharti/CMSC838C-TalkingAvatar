import concurrent.futures
import multiprocessing
import os
import re
import time
from threading import Thread

import torch
from transformers import (
    pipeline,
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer
)

from streaming_tts import run_tts_streaming

multiprocessing.set_start_method('spawn', force=True)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

llm_tok = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
llm_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.float16, token=True,
                                             device_map="auto")


def get_prompt_for_llm(user_input):
    prompt = f"""<s>[INST] <<SYS>>
        You are the famous celebrity talk show host Oprah Winfrey! You are talking to someone who needs you. Give very short, polite, and empathetic replies. Do not start your sentences
        with works like Oh and Ah. Directly being with the content. Use the following information to guide your responses:
        <</SYS>>

        What is your name? [/INST] My name is Oprah Winfrey </s><s>[INST] {user_input} [/INST]"""
    return prompt


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
    prompt = get_prompt_for_llm(user_input)
    inputs = llm_tok([prompt], return_tensors="pt").to("cuda")
    streamer = TextIteratorStreamer(llm_tok, skip_prompt=True)
    generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=1500)

    thread = Thread(target=llm_model.generate, kwargs=generation_kwargs)
    thread.start()

    generated_text = ""
    curr_sentence = ""
    sentences = []

    for new_text in streamer:
        # Append to the generated text
        generated_text += new_text
        curr_sentence += new_text
        curr_sentence = curr_sentence.strip()

        if curr_sentence and curr_sentence[-1] in ['.','!',';']:
            sentences.append(sanitize_text(curr_sentence))
            curr_sentence = ""

    thread.join()
    print("All sentences are")

    return generated_text


if __name__ == '__main__':
    while True:
        ask_me_something = input(">>Me: ")
        print(sanitize_text(chat_with_oprah_streaming(ask_me_something)))
