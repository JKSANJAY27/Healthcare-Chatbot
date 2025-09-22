from google.adk.agents import Agent
from google.adk.tools import google_search

# Mock tool for Google Calendar
def create_calendar_event(event_title: str, date: str) -> dict:
    """Creates a Google Calendar event to remind the user."""
    return {"status": "success", "message": f"Reminder set for '{event_title}' on {date}."}


govt_scheme_agent = Agent(
    name="govt_schemes_agent",
    model="gemini-1.5-flash",
    instruction="""
    You are an expert on Indian government health schemes.
    - Use the `google_search` tool to find information about schemes like Ayushman Bharat.
    - Summarize the key benefits, eligibility criteria, and application process.
    - If a user wants a reminder for a deadline, use the `create_calendar_event` tool.
    """,
    tools=[google_search, create_calendar_event],
    description="Provides detailed information on government health schemes like Ayushman Bharat, including eligibility and benefits."
)