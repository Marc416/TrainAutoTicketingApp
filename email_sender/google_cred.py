import os
from google.auth import exceptions
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# 토큰이 사용되기 위한 범위 설정 (https://developers.google.com/identity/protocols/oauth2/scopes?hl=ko#drive)
SCOPES = ['https://mail.google.com/']  # (파일을 생성, 수정, 삭제)
token_path = '/Users/joonheelee/Desktop/Github_Marc416/TrainAutoTicketingApp/email_sender/secret/uploader_app_token.json'  # google driver 앱클라이언트를 사용할 유저의 토큰
# token_path = '/secret/uploader_app_token.json'  # google driver 앱클라이언트를 사용할 유저의 토큰
credentials_path = '/Users/joonheelee/Desktop/Github_Marc416/TrainAutoTicketingApp/email_sender/secret/credentials.json'  # google driver 의 앱클라이언트 토큰
# credentials_path = '/secret/credentials.json'  # google driver 의 앱클라이언트 토큰

def get_creds(
        token_path: str = token_path,
        credentials_path: str = credentials_path,
        scopes: list = SCOPES,
        main_method_for_retry=None,
):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except exceptions.RefreshError as error:
                print(f"업로드에 필요한 토큰이 만료됐습니다 '{token_path}'을 지우고 다시 생성합니다  ;message: {error}")
                os.remove(token_path)
                return main_method_for_retry
        else:
            # uploader_app_token이 없는 경우
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w+') as token:
            token.write(creds.to_json())
    return creds

get_creds()