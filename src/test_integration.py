import os
import json
from src.extraction import extract_event_data
from src.calendar_client import CalendarClient
from dotenv import load_dotenv

load_dotenv()

def test_integration():
    print("--- Starting Integration Test ---")
    
    # 1. Define a sample email
    email_text = """
    Hi there,
    
    I'd like to schedule a project review meeting for next Friday at 10 AM EST. 
    It will last for one hour. We'll meet on Google Meet.
    
    Best,
    Client
    """
    print(f"Input Email:\n{email_text}\n")

    # 2. Extract data using OpenAI
    print("Extracting event data...")
    extraction_result = extract_event_data(email_text)
    print(f"Extracted Data:\n{json.dumps(extraction_result, indent=2)}\n")

    if extraction_result.get("Intent") != "Meeting":
        print("Error: Intent was not identified as Meeting.")
        return

    event_data = extraction_result.get("EventData")
    if not event_data:
        print("Error: No EventData found.")
        return

    # 3. Insert into Google Calendar
    print("Inserting into Google Calendar...")
    try:
        client = CalendarClient()
        result = client.create_event(event_data)
        print(f"SUCCESS: Event created! Link: {result.get('htmlLink')}")
    except Exception as e:
        print(f"FAILURE: Could not create event. Error: {e}")

if __name__ == "__main__":
    test_integration()
