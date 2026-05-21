import os
from dotenv import load_dotenv

load_dotenv()

SOURCE_FOLDER_ID = os.getenv("SOURCE_FOLDER_ID")
TARGET_FOLDER_ID = os.getenv("TARGET_FOLDER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LOCAL_AUDIO = "data/audio"
LOCAL_TRANSCRIPTS = "data/transcripts"
TEMPLATE_XLSX = "data/report.xlsx"
OUTPUT_XLSX = "data/report_processed.xlsx"