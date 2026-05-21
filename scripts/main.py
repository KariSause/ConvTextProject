import os
from config import *
from drive import list_audio, download, upload
from transcription import transcribe
from gpt_analysis import analyze
from excel_processor import append_to_excel, download_template
from pathlib import Path


os.makedirs(LOCAL_AUDIO, exist_ok=True)
os.makedirs(LOCAL_TRANSCRIPTS, exist_ok=True)


def run():
    audio_files = list_audio(SOURCE_FOLDER_ID)
    print(f"[Main] Files: {len(audio_files)}")
    print(audio_files)
    
    if not os.path.exists(TEMPLATE_XLSX):
        try:
            download_template(Path(TEMPLATE_XLSX), "1ocXd45G7v0ECgMSo0O9JOuLpt9e42o-1")
        except Exception as ex:
            print(f"[Error] No Excel: {ex}")
            return

    for f in audio_files:
        try:
            print(f"\n--- Старт обробки: {f['name']} ---")
            path = download(f["id"], f["name"], LOCAL_AUDIO)
            #upload(str(path), TARGET_FOLDER_ID)
            
            text, tpath = transcribe(str(path), LOCAL_TRANSCRIPTS)
            
            upload(str(tpath), TARGET_FOLDER_ID)

            result = analyze(text)
            append_to_excel(TEMPLATE_XLSX, OUTPUT_XLSX, result)
            
            print(f"[Main] Успішно завершено повний цикл для: {f['name']}")
            
        except Exception as e:
            print(f"[Error] Script skipped file due to error {f['name']}: {e}")
            continue

    print("\n[Main] Обробку всіх файлів завершено!")


if __name__ == "__main__":
    run()