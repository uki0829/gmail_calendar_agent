import time
import threading
import traceback
from typing import Optional
from src.gmail_client import GmailClient
from src.extraction import extract_event_data
from src.calendar_client import CalendarClient

class Agent:
    def __init__(self, poll_interval: int = 60):
        self.poll_interval = poll_interval
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.gmail_client = None
        self.calendar_client = None
        self.calendar_client = None
        self.status = "Stopped"
        self.stats = {"created_today": 0, "priority_count": 0}
        self.recent_emails = [] # List of dicts: {id, subject, sender, summary, category, importance}

    def initialize_clients(self):
        """Initializes API clients. Done lazily to allow server startup without creds."""
        if not self.gmail_client:
            print("Initializing Gmail Client...")
            self.gmail_client = GmailClient()
        if not self.calendar_client:
            print("Initializing Calendar Client...")
            self.calendar_client = CalendarClient()

    def start(self):
        """Starts the agent loop in a background thread."""
        if self.running:
            print("Agent is already running.")
            return

        try:
            self.initialize_clients()
            self.running = True
            self.status = "Running"
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            print("Agent started.")
        except Exception as e:
            print(f"Failed to start agent: {e}")
            self.status = f"Error: {e}"
            self.running = False

    def stop(self):
        """Stops the agent loop."""
        if not self.running:
            return
        
        print("Stopping agent...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.status = "Stopped"
        print("Agent stopped.")

    def _run_loop(self):
        """Main polling loop."""
        print("Entering main loop...")
        while self.running:
            try:
                self._process_emails()
            except Exception as e:
                print(f"Error in main loop: {e}")
                traceback.print_exc()
            
            # Sleep in small chunks to allow faster stopping
            for _ in range(self.poll_interval):
                if not self.running:
                    break
                time.sleep(1)

    def _process_emails(self):
        """Fetches and processes unread emails."""
        print("Checking for new emails...")
        emails = self.gmail_client.fetch_recent_emails(max_results=5, query='is:unread')
        
        if not emails:
            print("No new emails.")
            return

        for email in emails:
            if not self.running:
                break
                
            print(f"Processing email: {email['subject']}")
            
            # 1. Extract Data
            # Combine subject and body for better context
            full_text = f"Subject: {email['subject']}\n\n{email['body']}"
            extraction_result = extract_event_data(full_text)
            
            intent = extraction_result.get("Intent")
            print(f"Identified Intent: {intent}")
            
            # Store in Recent Emails if Important
            category = extraction_result.get("Category", "Unknown")
            importance = extraction_result.get("Importance", "Low")
            
            if importance in ["High", "Medium"]:
                self.recent_emails.insert(0, {
                    "id": email['id'],
                    "subject": email['subject'],
                    "sender": email.get('sender', 'Unknown'),
                    "summary": event_data.get("description") if event_data else "No summary available",
                    "category": category,
                    "importance": importance
                })
                # Keep only last 10
                self.recent_emails = self.recent_emails[:10]
                self.stats["priority_count"] = len(self.recent_emails)

            if intent in ["Meeting", "Registration", "Event"]:
                event_data = extraction_result.get("EventData")
                if event_data:
                    # 2. Create Calendar Event
                    print(f"Creating event: {event_data.get('title')}")
                    try:
                        self.calendar_client.create_event(event_data)
                        print("Event created successfully.")
                        self.stats["created_today"] += 1
                        
                        # 3. Mark as Read (Only if successfully processed)
                        self.gmail_client.mark_as_read(email['id'])
                        
                    except Exception as e:
                        print(f"Failed to create event: {e}")
            else:
                print("Skipping email (No event detected).")
                # Optional: Mark as read anyway so we don't process it forever?
                # For now, let's leave it unread or maybe mark it read to avoid loops.
                # self.gmail_client.mark_as_read(email['id']) 

if __name__ == "__main__":
    # Manual Test
    agent = Agent(poll_interval=10)
    agent.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop()
