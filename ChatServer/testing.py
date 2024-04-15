from chat import chat_with_oprah_streaming, sanitize_text
from tts import run_tts
import shutil
import os
import time


# Directory to save uploaded files
UPLOAD_DIRECTORY = "/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/ChatServer/tmp/uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


if __name__ == "__main__":
    while True:
        ask_me_something = input(">>Me: ")
        t1 = time.perf_counter()
        temp_reply_file_path = os.path.join(UPLOAD_DIRECTORY, "reply.mp3")
        oprah_reply = sanitize_text(chat_with_oprah_streaming(ask_me_something))
        t2 = time.perf_counter()
        print("Oprah's reply:", oprah_reply)
        run_tts(oprah_reply, temp_reply_file_path)
        t3 = time.perf_counter()
        print(f"Reply took {t2-t1} ms")
        print(f"Audio took {t3-t2} ms")
