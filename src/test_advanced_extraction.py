import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from src.extraction import extract_event_data
from src.calendar_client import CalendarClient
from dotenv import load_dotenv

load_dotenv()

def test_advanced_extraction():
    print("--- Starting Advanced Extraction Test ---")
    
    # Sample email with Location and URL
    email_text = """
    Subject: Zoom Meeting: Project Kickoff
    
    Hi Team,
    
    Please join us for the project kickoff meeting.
    
    When: Tomorrow at 2 PM EST
    Where: https://zoom.us/j/123456789
    Physical Location: Conference Room B, 123 Tech Park, NY
    
    Agenda:
    1. Introductions
    2. Roadmap
    """
    print(f"Input Email:\n{email_text}\n")

    # 1. Extract data
    print("Extracting event data...")
    extraction_result = extract_event_data(email_text)
    print(f"Extracted Data:\n{json.dumps(extraction_result, indent=2)}\n")

    event_data = extraction_result.get("EventData")
    if not event_data:
        print("Error: No EventData found.")
        return

    # Verify Location extraction
    location = event_data.get("location")
    print(f"Extracted Location: {location}")
    
    # Note: The model might pick the Zoom link OR the physical location, or combine them.
    # Ideally, we want the Zoom link if it's a virtual meeting.
    
    # 2. Insert into Calendar
    print("Inserting into Google Calendar...")
    try:
        client = CalendarClient()
        result = client.create_event(event_data)
        print(f"SUCCESS: Event created! Link: {result.get('htmlLink')}")
        print("Check the event details in your calendar to verify the location/URL.")
    except Exception as e:
        print(f"FAILURE: Could not create event. Error: {e}")

if __name__ == "__main__":
    test_advanced_extraction()
