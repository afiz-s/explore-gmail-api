import pickle
import os.path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_emails_list():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    return results.get('messages', [])

def get_email_content(message_id):
    service = get_gmail_service()
    data = service.users().messages().get(userId='me', id=message_id).execute()
    return data 

if __name__ == '__main__':
    # messages = get_emails_list()
    # for message in messages:
    #     print(message['id'])
    pprint.pprint(get_email_content('1747063927ef5396'))


