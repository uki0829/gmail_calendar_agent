import os
from typing import Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'

class CalendarClient:
    def __init__(self):
        self.creds = None
        self.service = None
        self.calendar_id = os.getenv("CALENDAR_ID")
        if not self.calendar_id:
            raise ValueError("CALENDAR_ID not found in environment variables.")
        
        self.authenticate()

    def authenticate(self):
        """Authenticates using the service account file."""
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            self.creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            self.service = build('calendar', 'v3', credentials=self.creds)
        else:
            raise FileNotFoundError(f"Service account file '{SERVICE_ACCOUNT_FILE}' not found.")

    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inserts an event into the Google Calendar.
        
        Args:
            event_data: Dictionary containing event details (title, startDateTime, endDateTime, etc.)
            
        Returns:
            The created event object from the API.
        """
        if not self.service:
            raise RuntimeError("Calendar service not initialized. Call authenticate() first.")

        event = {
            'summary': event_data.get('title', 'New Event'),
            'location': event_data.get('location', ''),
            'description': event_data.get('description', ''),
            'start': {
                'dateTime': event_data['startDateTime'],
                'timeZone': 'UTC', # Assuming UTC from extraction, or infer from string
            },
            'end': {
                'dateTime': event_data['endDateTime'],
                'timeZone': 'UTC',
            },
            'attendees': [{'email': email} for email in (event_data.get('attendees') or [])],
        }

        try:
            event_result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            print(f"Event created: {event_result.get('htmlLink')}")
            return event_result
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

if __name__ == "__main__":
    # Manual test (requires service_account.json and CALENDAR_ID)
    try:
        client = CalendarClient()
        test_event = {
            "title": "Test Event from Agent",
            "startDateTime": "2025-11-21T10:00:00Z",
            "endDateTime": "2025-11-21T11:00:00Z",
            "description": "This is a test event.",
            "location": "Virtual"
        }
        client.create_event(test_event)
    except Exception as e:
        print(f"Test failed: {e}")
