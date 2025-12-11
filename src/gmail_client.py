import os
import base64
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

class GmailClient:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticates using credentials.json and creates token.json."""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                     raise FileNotFoundError("credentials.json not found. Please download it from Google Cloud Console.")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)

    def fetch_recent_emails(self, max_results: int = 5, query: str = 'is:unread') -> List[Dict[str, Any]]:
        """
        Fetches recent emails matching the query.
        
        Args:
            max_results: Maximum number of emails to fetch.
            query: Gmail search query (default: 'is:unread').
            
        Returns:
            List of dictionaries containing 'id', 'subject', 'body', 'snippet'.
        """
        if not self.service:
            raise RuntimeError("Gmail service not initialized.")

        results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            
            # Extract Subject and Sender
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            
            # Extract Body
            body = ""
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data')
                        if data:
                            body += base64.urlsafe_b64decode(data).decode()
            else:
                # Fallback for simple emails
                data = msg['payload']['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode()

            email_data.append({
                'id': message['id'],
                'subject': subject,
                'sender': sender,
                'body': body,
                'snippet': msg.get('snippet', '')
            })
            
        return email_data

    def mark_as_read(self, message_id: str):
        """Marks an email as read by removing the UNREAD label."""
        if not self.service:
             raise RuntimeError("Gmail service not initialized.")
             
        self.service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"Marked message {message_id} as read.")

if __name__ == "__main__":
    # Manual test
    try:
        client = GmailClient()
        emails = client.fetch_recent_emails(max_results=3)
        for email in emails:
            print(f"Subject: {email['subject']}")
            print(f"Snippet: {email['snippet']}")
            print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")
