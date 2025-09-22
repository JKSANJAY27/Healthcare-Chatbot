from google.adk.agents import Agent, SequentialAgent
from .tools import detect_emergency, find_nearest_hospital, identify_potential_diagnosis

# Agent Step 1: Triage and Emergency Detection
emergency_detection_agent = Agent(
    name="emergency_detector",
    model="gemini-1.5-flash",
    instruction="""
    Your sole task is to analyze the user's symptoms for life-threatening conditions.
    - Use the `detect_emergency` tool.
    - If it IS an emergency, immediately use `find_nearest_hospital` and output ONLY the hospital info.
    - If it is NOT an emergency, state that and pass the symptoms to the next agent.
    - Your output must clearly state "EMERGENCY" or "NON-EMERGENCY".
    """,
    tools=[detect_emergency, find_nearest_hospital]
)

# Agent Step 2: Diagnosis Identification
diagnosis_identification_agent = Agent(
    name="diagnosis_identifier",
    model="gemini-1.5-flash",
    instruction="""
    You will receive a user's symptoms that have been determined to be non-emergency.
    - Use the `identify_potential_diagnosis` tool to get potential conditions.
    - Format the tool's output into a clear, empathetic message.
    - ALWAYS include the disclaimer provided by the tool.
    """,
    tools=[identify_potential_diagnosis]
)

# The Sequential Pipeline for the full diagnosis flow
diagnosis_agent_pipeline = SequentialAgent(
    name="diagnosis_pipeline",
    sub_agents=[emergency_detection_agent, diagnosis_identification_agent],
    description="A multi-step agent for symptom analysis. It first performs emergency triage and then provides a preliminary diagnosis for non-critical cases."
)