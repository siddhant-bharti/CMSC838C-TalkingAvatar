import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from stt import run_stt
from chat import chat_with_oprah_streaming, sanitize_text, chat_with_oprah_streaming_audio
from tts import run_tts
import shutil
import os
import time

app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIRECTORY = "/home/lyhan12/Workspace/siddhantbharti/CMSC838C/CMSC838C-TalkingAvatar/ChatServer/tmp/uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def conversation_pipeline():
    pass


@app.post("/process-audio/")
async def process_audio(audio: UploadFile = File(...)):
    # Save uploaded file to disk for processing
    temp_file_path = os.path.join(UPLOAD_DIRECTORY, audio.filename)
    temp_reply_file_path = os.path.join(UPLOAD_DIRECTORY, "reply_vanilla.mp3")

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    t0 = time.perf_counter()
    user_text = run_stt(temp_file_path)
    print("user_text: ", user_text)
    t1 = time.perf_counter()

    oprah_reply = chat_with_oprah_streaming(user_text)
    t2 = time.perf_counter()
    run_tts(oprah_reply, temp_reply_file_path)
    t3 = time.perf_counter()
    print(f"Speech to text took {t1-t0} secs")
    print(f"LLM took {t2-t1} secs")
    print(f"Text to speech took {t3-t2} secs")

    # Return the processed audio file
    return FileResponse(temp_reply_file_path, media_type="audio/mpeg", filename="reply_vanilla.mp3")


@app.post("/process-audio-streaming/")
async def process_audio(audio: UploadFile = File(...)):
    # Save uploaded file to disk for processing
    temp_file_path = os.path.join(UPLOAD_DIRECTORY, audio.filename)
    temp_reply_file_path = os.path.join(UPLOAD_DIRECTORY, "reply_streaming.mp3")

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    t0 = time.perf_counter()
    user_text = run_stt(temp_file_path)
    print("user_text: ", user_text)
    t1 = time.perf_counter()

    oprah_reply = chat_with_oprah_streaming_audio(user_text, temp_reply_file_path, is_streaming=True)
    t2 = time.perf_counter()
    print(f"Speech to text took {t1 - t0} secs")
    print(f"LLM and speech took {t2 - t1} secs")

    # Return the processed audio file
    return FileResponse(temp_reply_file_path, media_type="audio/mpeg", filename="reply_streaming.mp3")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
