import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from src.extraction import extract_event_data
from src.calendar_client import CalendarClient
from dotenv import load_dotenv

load_dotenv()

def test_location_maps():
    print("--- Starting Google Maps Location Test ---")
    
    # Sample email mimicking a reservation confirmation (like the user's screenshot)
    email_text = """
    Subject: Reservation Confirmed: JoJo
    
    Your reservation at JoJo is confirmed.
    
    Date: Saturday, November 29
    Time: 7:15 PM - 8:15 PM
    Guests: 1
    
    Location:
    JoJo
    160 East 64th Street, New York, NY, 10065, United States
    +1 212-223-5656
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
    
    if "160 East 64th Street" in location:
        print("PASS: Full address detected.")
    else:
        print("WARNING: Full address might be missing. Check output.")

    # 2. Insert into Calendar
    print("Inserting into Google Calendar...")
    try:
        client = CalendarClient()
        result = client.create_event(event_data)
        print(f"SUCCESS: Event created! Link: {result.get('htmlLink')}")
        print("Please check the event in Google Calendar. Clicking the location should open Google Maps.")
    except Exception as e:
        print(f"FAILURE: Could not create event. Error: {e}")

if __name__ == "__main__":
    test_location_maps()
