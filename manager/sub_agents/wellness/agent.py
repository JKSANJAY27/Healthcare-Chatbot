from google.adk.agents import Agent
# Assume tools are defined in agents/sub_agents/wellness/tools.py
# e.g., get_ayurveda_recommendation, get_yoga_plan, analyze_yoga_pose_image

# Mock tools for demonstration
def get_ayurvedic_recommendation(health_conditions: str) -> dict:
    """Provides Ayurvedic recommendations based on health conditions."""
    return {"recommendation": f"For {health_conditions}, consider incorporating Brahmi and Ashwagandha. Drink warm water throughout the day."}

def get_yoga_plan(age: int, health_conditions: str) -> dict:
    """Generates a custom yoga plan."""
    return {"plan": f"A gentle yoga plan for age {age} with {health_conditions}: Sun Salutation (Surya Namaskar) x3, Triangle Pose (Trikonasana), Corpse Pose (Shavasana)."}


wellness_agent = Agent(
    name="wellness_agent",
    model="gemini-1.5-flash",
    instruction="""
    You are a wellness expert specializing in Ayurveda and Yoga.
    - If the user asks for Yoga advice, use the `get_yoga_plan` tool.
    - If the user asks for Ayurveda advice, use `get_ayurvedic_recommendation` tool.
    - You MUST get all required parameters (like age, health_conditions) from the user before calling a tool. Ask clarifying questions if needed.
    - Present the information in a supportive and easy-to-understand manner.
    """,
    tools=[get_ayurvedic_recommendation, get_yoga_plan],
    description="Provides personalized wellness guidance based on Ayurvedic and Yogic principles. Can create custom yoga plans and suggest dietary recommendations."
)