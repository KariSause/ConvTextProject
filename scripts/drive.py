import io
import os
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import unicodedata

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds
creds = get_credentials()
service = build('drive', 'v3', credentials=creds)


def list_audio(folder_id):
    q = f"'{folder_id}' contains in'audio/'"
    res = service.files().list(q=q, fields="files(id,name)").execute()
    return res.get("files", [])


def download(file_id, name, path):
    request = service.files().get_media(fileId=file_id)

    folder = Path(path) 
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / name
    
    filepath_str = os.path.normpath(str(filepath))
    print(f"[Drive] Downloading to: {filepath_str}")

    with io.FileIO(filepath_str, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    return filepath_str  

def upload(path, folder_id):
    path_str = os.path.normpath(str(path))
    filename = os.path.basename(path_str)
    
    metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    if path_str.endswith('.txt'):
        mimetype = 'text/plain'
    elif path_str.endswith('.mp3'):
        mimetype = 'audio/mpeg'
    else:
        mimetype = 'application/octet-stream'

    media = MediaFileUpload(path_str, mimetype=mimetype, resumable=True)

    try:
        return service.files().create(body=metadata, media_body=media, fields="id").execute()
    except Exception as ex:
        try:
            ascii_name = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
            if not ascii_name:
                ascii_name = 'file'
            metadata2 = {"name": ascii_name, "parents": [folder_id]}
            return service.files().create(body=metadata2, media_body=media, fields="id").execute()
        except Exception:
            raise