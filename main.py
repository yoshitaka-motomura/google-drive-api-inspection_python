import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

EMAIL = (os.environ['WORK_MAIL_ADDRESS'])
JSON_FILE = (os.environ['CREDENTIAL_JSON_FILE'])


def main():
    credentials_file = Path.cwd().joinpath('credentials', JSON_FILE)
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file,
        scopes=['https://www.googleapis.com/auth/drive'],
    )

    delegated_credentials = credentials.with_subject(EMAIL)

    drive_service = build('drive', 'v3', credentials=delegated_credentials)

    # 時間指定
    # UTCによる時間を算出する
    # https://developers.google.com/drive/api/guides/search-files?hl=ja#examples
    date_by = datetime.utcnow() - timedelta(hours=24)
    format_date = date_by.strftime('%Y-%m-%dT%H:%M:%S')

    # Queryの生成
    # Example 24時間以内のjpegまたpngのファイルを取得する
    query = f"sharedWithMe=true and modifiedTime > '{format_date}' and (mimeType='image/jpeg' or mimeType='image/png' or mimeType='image/gif')"

    results = drive_service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
    items = results.get('files', [])

    if not items:
        print('No shared files found.')
    else:
        print('Shared files:')
        for item in items:
            print(f"ID: {item['id']}, Name: {item['name']}, Link: {item['webViewLink']}")


if __name__ == '__main__':
    main()
