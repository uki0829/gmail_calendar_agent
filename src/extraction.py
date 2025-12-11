import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_current_time_str() -> str:
    """Returns the current time in ISO 8601 format."""
    return datetime.now().astimezone().isoformat()

EVENT_EXTRACTION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Extracts event data from an email body for Google Calendar insertion.",
            "parameters": {
                "type": "object",
                "required": ["Intent", "EventData"],
                "properties": {
                    "Intent": {
                        "type": "string",
                        "description": "The primary purpose of the email.",
                        "enum": ["Meeting", "Registration", "Event", "None"]
                    },
                    "EventData": {
                        "type": "object",
                        "required": ["title", "startDateTime", "endDateTime"],
                        "properties": {
                            "title": { "type": "string", "description": "Concise event title." },
                            "startDateTime": { "type": "string", "description": "ISO 8601 start date/time (YYYY-MM-DDTHH:MM:SSZ)." },
                            "endDateTime": { "type": "string", "description": "ISO 8601 end date/time (YYYY-MM-DDTHH:MM:SSZ)." },
                            "location": { "type": "string", "description": "Physical or virtual location URL (Zoom/Meet link preferred).", "nullable": True },
                            "description": { "type": "string", "description": "Detailed event summary, including agenda or key details.", "nullable": True },
                            "attendees": {
                                "type": "array",
                                "items": { "type": "string", "format": "email" },
                                "description": "Array of discovered email addresses of other participants (excluding the user).",
                                "nullable": True
                            }
                        }
                    }
                }
            }
        }
    }
]

def extract_event_data(email_text: str) -> Dict[str, Any]:
    """
    Analyzes email text using OpenAI API to extract structured event data.
    
    Args:
        email_text: The raw text content of the email.
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_text}
            ],
            tools=EVENT_EXTRACTION_TOOLS,
            tool_choice={"type": "function", "function": {"name": "create_calendar_event"}}
        )

        tool_call = response.choices[0].message.tool_calls[0]
        function_args = json.loads(tool_call.function.arguments)
        return function_args

    except Exception as e:
        print(f"Error extracting event data: {e}")
        return {"Intent": "None", "EventData": {}}

if __name__ == "__main__":
    # Simple manual test
    sample_email = "Hey, let's meet for coffee tomorrow at 2 PM at Starbucks."
    print(json.dumps(extract_event_data(sample_email), indent=2))
