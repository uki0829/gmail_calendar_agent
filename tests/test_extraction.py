import json
import unittest
from unittest.mock import MagicMock, patch
from src.extraction import extract_event_data

# Mock response for a meeting
MOCK_MEETING_RESPONSE = {
    "choices": [
        {
            "message": {
                "tool_calls": [
                    {
                        "function": {
                            "arguments": json.dumps({
                                "Intent": "Meeting",
                                "EventData": {
                                    "title": "Coffee with Alice",
                                    "startDateTime": "2023-10-27T14:00:00Z",
                                    "endDateTime": "2023-10-27T15:00:00Z",
                                    "location": "Starbucks",
                                    "description": "Discuss project",
                                    "attendees": ["alice@example.com"]
                                }
                            })
                        }
                    }
                ]
            }
        }
    ]
}

# Mock response for no event
MOCK_NO_EVENT_RESPONSE = {
    "choices": [
        {
            "message": {
                "tool_calls": [
                    {
                        "function": {
                            "arguments": json.dumps({
                                "Intent": "None",
                                "EventData": {}
                            })
                        }
                    }
                ]
            }
        }
    ]
}

class TestExtraction(unittest.TestCase):
    @patch("src.extraction.client")
    def test_extract_meeting(self, mock_client):
        # Setup mock
        mock_client.chat.completions.create.return_value = MagicMock(**MOCK_MEETING_RESPONSE)
        # Mock the nested structure access
        mock_client.chat.completions.create.return_value.choices[0].message.tool_calls[0].function.arguments = json.dumps({
            "Intent": "Meeting",
            "EventData": {
                "title": "Coffee with Alice",
                "startDateTime": "2023-10-27T14:00:00Z",
                "endDateTime": "2023-10-27T15:00:00Z",
                "location": "Starbucks",
                "description": "Discuss project",
                "attendees": ["alice@example.com"]
            }
        })
        
        email_text = "Let's meet for coffee tomorrow at 2 PM at Starbucks."
        result = extract_event_data(email_text)
        
        self.assertEqual(result["Intent"], "Meeting")
        self.assertEqual(result["EventData"]["title"], "Coffee with Alice")
        self.assertEqual(result["EventData"]["location"], "Starbucks")
        self.assertIn("alice@example.com", result["EventData"]["attendees"])

    @patch("src.extraction.client")
    def test_extract_no_event(self, mock_client):
        # Setup mock
        mock_client.chat.completions.create.return_value = MagicMock(**MOCK_NO_EVENT_RESPONSE)
        # Mock the nested structure access
        mock_client.chat.completions.create.return_value.choices[0].message.tool_calls[0].function.arguments = json.dumps({
            "Intent": "None",
            "EventData": {}
        })
        
        email_text = "Just checking in on the project status."
        result = extract_event_data(email_text)
        
        self.assertEqual(result["Intent"], "None")
        self.assertEqual(result["EventData"], {})

if __name__ == "__main__":
    unittest.main()
