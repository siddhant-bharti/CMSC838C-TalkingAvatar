from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread


# Function to simulate chat with Oprah Winfrey
def chat_with_oprah(user_input):
    generator = pipeline('text-generation', model='meta-llama/Llama-2-7b-chat-hf')
    # Crafting a prompt that includes Oprah's persona
    prompt = f"User: {user_input}\nOprah Winfrey: "

    # Generating Oprah Winfrey's response
    responses = generator(prompt, max_new_tokens=3, num_return_sequences=1)

    # Extracting and printing the generated text
    oprah_response = responses[0]['generated_text'].split("Oprah Winfrey: ")[-1]
    print(oprah_response)


def chat_with_oprah_streaming(user_input):
    tok = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    inputs = tok([user_input], return_tensors="pt")
    streamer = TextIteratorStreamer(tok)
    generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=5)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    generated_text = ""
    for new_text in streamer:
        print(new_text)
        generated_text += new_text
    print(generated_text)


if __name__ == '__main__':
    user_input = "What's your secret to success?"
    # chat_with_oprah(user_input)
    chat_with_oprah_streaming(user_input)
