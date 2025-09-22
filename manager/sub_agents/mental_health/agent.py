from google.adk.agents import LlmAgent, SequentialAgent, Agent
from pydantic import BaseModel, Field

# Schema for structured sentiment output
class Sentiment(BaseModel):
    sentiment: str = Field(description="The dominant sentiment (e.g., 'Anxious', 'Stressed', 'Sad', 'Neutral')")

# Mock tool for resources
def get_mental_support_resources(sentiment: str) -> dict:
    """Provides resources based on the user's emotional state."""
    if sentiment.lower() in ["anxious", "stressed"]:
        return {"resources": "Consider trying a 5-minute box breathing exercise. You can also find guided meditations online."}
    else:
        return {"resources": "It can be helpful to talk to someone. Here is a national helpline number: XXX-XXX-XXXX."}

# Step 1: Analyze Sentiment
sentiment_analyzer = LlmAgent(
    name="sentiment_analyzer",
    model="gemini-1.5-flash",
    instruction="Analyze the user's message and determine their primary sentiment. Respond ONLY with the JSON output.",
    output_schema=Sentiment,
)

# Step 2: Provide Support
support_provider = Agent(
    name="support_provider",
    model="gemini-1.5-flash",
    instruction="""
    You are an empathetic mental health support assistant. You have received the user's sentiment.
    - Use the `get_mental_support_resources` tool to find appropriate coping mechanisms or help.
    - Present the resources in a gentle, caring, and non-judgmental tone.
    - Start your response with an empathetic acknowledgment like "I hear that you're feeling..."
    """,
    tools=[get_mental_support_resources]
)

mental_health_agent_pipeline = SequentialAgent(
    name="mental_health_pipeline",
    sub_agents=[sentiment_analyzer, support_provider],
    description="An empathetic agent that first understands the user's emotional state and then provides appropriate mental health support and resources."
)