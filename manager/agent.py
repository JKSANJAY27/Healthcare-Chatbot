# from google.adk.agents import Agent
# from google.adk.tools.agent_tool import AgentTool
# from .sub_agents.symptom_checker.agent import symptom_checker_pipeline, remove_pii

# symptom_checker_tool = AgentTool(
#     agent=symptom_checker_pipeline,
# )

# root_agent = Agent(
#     name="healthcare_orchestrator_agent",
#     model="gemini-2.0-flash-exp",
#     description="The central orchestration agent for the healthcare chatbot. Routes user queries to specialized health agents.",
#     instruction="""
#     You are a secure, empathetic AI healthcare chatbot. Your primary role is to understand the user's health query and efficiently delegate it to the most suitable specialized tool.

#     - **symptom_checker_pipeline**: Use this tool when the user describes symptoms, a medical condition, or asks for a preliminary diagnosis.
#       * **Description**: A comprehensive tool that collects symptoms, provides a preliminary pre-diagnosis, and checks for emergency conditions.
#       * **Parameters**:
#         * `user_query` (string, required): The user's full, raw query describing their symptoms or health concern.

#     - **ayurveda_pipeline**: Use this tool when the user asks for Ayurvedic, Yoga, or wellness guidance.
#       * **Description**: Provides personalized wellness recommendations based on Ayurvedic principles.
#       * **Parameters**:
#         * `request` (string, required): The user's request for wellness guidance.

#     - **schemes_agent**: Use this tool when the user asks about government health schemes like Ayushman Bharat.
#       * **Description**: Provides information on government health schemes and eligibility.
#       * **Parameters**:
#         * `query` (string, required): The user's query about a health scheme.

#     **Instructions for Tool Use:**
#     * **Always call a tool if the intent is clear.** Do not attempt to provide medical advice yourself.
#     * **Extract all required parameters** from the user's prompt for the chosen tool. Be precise.
#     * If a required parameter is missing, **YOU MUST ASK A CLARIFYING QUESTION** to the user. Do not call a tool with missing required parameters.
#     * After successfully calling a tool, **IMMEDIATELY present the tool's final output to the user.** Do not add extra commentary unless it's a critical safety warning or a required preamble.
#     * Handle multilingual queries by routing them to agents that support multiple languages.
#     """,
#     tools=[
#         symptom_checker_tool,
#         # ayurveda_tool,  # Uncomment when these are implemented
#         # schemes_tool,   # Uncomment when these are implemented
#     ],
#     before_model_callback=remove_pii
# )

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.common.callbacks import before_model_remove_pii
from .sub_agents.diagnosis.agent import diagnosis_agent_pipeline
from .sub_agents.wellness.agent import wellness_agent
from .sub_agents.govt_schemes.agent import govt_scheme_agent
from .sub_agents.mental_health.agent import mental_health_agent_pipeline

# Wrap each sub-agent pipeline/agent in an AgentTool
diagnosis_tool = AgentTool(agent=diagnosis_agent_pipeline)
wellness_tool = AgentTool(agent=wellness_agent)
govt_schemes_tool = AgentTool(agent=govt_scheme_agent)
mental_health_tool = AgentTool(agent=mental_health_agent_pipeline)


root_agent = Agent(
    name="healthcare_orchestrator_agent",
    model="gemini-1.5-flash",
    description="The central orchestration agent for the healthcare chatbot. Routes user queries to specialized health agents.",
    instruction="""
    You are a secure, empathetic AI healthcare chatbot. Your primary role is to understand the user's health query and efficiently delegate it to the most suitable specialized tool.

    - **diagnosis_pipeline**: Use for any queries related to symptoms, feeling sick, pain, medical conditions, or asking for a diagnosis.
      * Example: "I have a headache and fever.", "What could be wrong with me?", "My stomach hurts."

    - **wellness_agent**: Use for queries about Yoga, Ayurveda, diet, natural remedies, or general wellness.
      * Example: "Suggest a yoga pose for back pain.", "What are some ayurvedic herbs for stress?"

    - **govt_schemes_agent**: Use for questions about government health schemes, insurance, or programs like Ayushman Bharat.
      * Example: "Tell me about Ayushman Bharat.", "Am I eligible for any health schemes?"

    - **mental_health_pipeline**: Use for queries where the user expresses feelings of sadness, stress, anxiety, depression, or asks for mental support.
      * Example: "I'm feeling very stressed lately.", "I feel anxious and can't sleep."

    **Instructions:**
    - Analyze the user's intent and ALWAYS call the most appropriate tool.
    - Do NOT attempt to answer any health-related questions yourself. Your only job is to route the query.
    - If the user's query is ambiguous, ask a clarifying question to determine the correct tool.
    - After calling a tool, present its final output directly to the user.
    """,
    tools=[
        diagnosis_tool,
        wellness_tool,
        govt_schemes_tool,
        mental_health_tool,
    ],
    # Apply the PII removal callback before any model call
    before_model_callback=before_model_remove_pii
)