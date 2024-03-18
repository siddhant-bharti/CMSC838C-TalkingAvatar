from transformers import pipeline

# Initialize the pipeline for text-generation using the Llama 2 model
generator = pipeline('text-generation', model='meta-llama/Llama-2-7b-chat-hf')


# Function to simulate chat with Oprah Winfrey
def chat_with_oprah(user_input):
    # Crafting a prompt that includes Oprah's persona
    prompt = f"User: {user_input}\nOprah Winfrey: "

    # Generating Oprah Winfrey's response
    responses = generator(prompt, max_length=150, num_return_sequences=1)

    # Extracting and printing the generated text
    oprah_response = responses[0]['generated_text'].split("Oprah Winfrey: ")[-1]
    return oprah_response


# Example user input
user_input = "What's your secret to success?"

# Get Oprah's response
oprah_response = chat_with_oprah(user_input)
print(f"Oprah Winfrey: {oprah_response}")
