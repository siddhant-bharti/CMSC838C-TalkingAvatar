import os
import time

from chat import chat_with_oprah_streaming, sanitize_text, chat_with_oprah_streaming_audio
from tts import run_tts
from streaming_tts import run_tts_streaming

# Directory to save uploaded files
UPLOAD_DIRECTORY = "/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/ChatServer/tmp/uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

if __name__ == "__main__":
    # while True:
    #     ask_me_something = input(">>Me: ")
    #     t1 = time.perf_counter()
    #     oprah_reply = chat_with_oprah_streaming(ask_me_something)
    #     print("Oprah's reply:", oprah_reply)
    #     t2 = time.perf_counter()
    #     run_tts(oprah_reply, "./tts_testing_vanilla.wav")
    #     t3 = time.perf_counter()
    #     run_tts_streaming(oprah_reply, "./tts_testing_streaming.wav")
    #     t4 = time.perf_counter()
    #     print(f"Reply took {t2 - t1} secs")
    #     print(f"Audio took {t3 - t2} secs")
    #     print(f"Streaming audio took {t4 - t3} secs")
    while True:
        ask_me_something = input(">>Me: ")
        t1 = time.perf_counter()
        oprah_reply = chat_with_oprah_streaming_audio(ask_me_something, "./tts_testing_vanilla.wav", is_streaming=False)
        print("Oprah's reply:", oprah_reply)
        t2 = time.perf_counter()
        oprah_reply = chat_with_oprah_streaming_audio(ask_me_something, "./tts_testing_streaming.wav", is_streaming=True)
        print("Oprah's reply:", oprah_reply)
        t3 = time.perf_counter()
        print(f"Without streaming took {t2-t1} secs")
        print(f"With streaming took {t3-t2} secs")
