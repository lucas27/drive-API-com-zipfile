import os.path
import logging
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
from zip_file import main_zip, caminho_para_zip

logging.basicConfig(level=logging.INFO, filename='program.log', format='%(asctime)s - %(filename)s - %(message)s')

load_dotenv('.env')

SCOPES = [os.getenv('SCOPE_')]

def upload(service, file_metadata, file_path, mime_type):
    tempo_inicial = time.time()

    media = MediaFileUpload(file_path, mimetype=mime_type, chunksize=256*1024, resumable=True)
    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logging.info(f"Uploaded {int(status.progress() * 100)}%.")
    logging.info(f'File ID: {response.get("id")}')
    logging.info(f'demorou: {round(time.time() - tempo_inicial)} segundos')

def iniciar_sessão():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    services = build("drive", "v3", credentials=creds, cache_discovery=False)
    return services

def main():
    
    FILE_NAME_WITH_ZIP, PATH = caminho_para_zip()

    try:
        service = iniciar_sessão()

        folder_id = os.getenv('FOLDER_ID_')
        file_name = FILE_NAME_WITH_ZIP.split('.')[0]
        file_path = FILE_NAME_WITH_ZIP
        mime_type = os.getenv('MIME_TYPE_')

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        
        main_zip(FILE_NAME_WITH_ZIP, PATH)

        upload(service, file_metadata, file_path, mime_type)
        
        if os.path.exists(FILE_NAME_WITH_ZIP):
            os.unlink(FILE_NAME_WITH_ZIP)

    except HttpError as error:
        logging.error(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
    
    ...