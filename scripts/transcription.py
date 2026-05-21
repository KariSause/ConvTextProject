import os
from pathlib import Path
from openai import OpenAI


client = OpenAI()

def transcribe(path: str, local_transcripts: str) -> tuple:
    path_str = os.path.normpath(str(path))
    if not os.path.exists(path_str):
        raise FileNotFoundError(f"No file: {path_str}")
    print(f"[OpenAI Whisper] Starting transcription..: {os.path.basename(path_str)}")
    with open(path_str, "rb") as audio_file:
        transcript_response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            language="uk"  
        )
    text = transcript_response.text
    folder = Path(local_transcripts)
    folder.mkdir(parents=True, exist_ok=True)
    audio_name = Path(path_str).stem
    tpath = folder / f"{audio_name}.txt"
    with open(tpath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[OpenAI Whisper] Transcription saved: {tpath.name}")
    
    return text, str(tpath)