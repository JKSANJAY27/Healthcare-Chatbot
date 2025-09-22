import re
from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse

def remove_pii_from_text(text: str) -> str:
    """Removes common PII patterns from a given text."""
    # Simple regex for emails and phone numbers
    text = re.sub(r'\S+@\S+', '[REDACTED_EMAIL]', text)
    text = re.sub(r'(\+?\d{1,2}[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', '[REDACTED_PHONE]', text)
    # Add more regex for names, addresses etc. as needed
    return text

def before_model_remove_pii(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    A 'before_model_callback' that redacts PII from the user's latest query
    before sending it to the LLM.
    """
    if not llm_request.contents:
        return None

    # We typically want to check the last user message
    last_content = llm_request.contents[-1]
    if last_content.role == "user" and last_content.parts:
        for part in last_content.parts:
            if hasattr(part, "text") and part.text:
                original_text = part.text
                part.text = remove_pii_from_text(original_text)
                if original_text != part.text:
                    print(f"[CALLBACK] PII redacted from user input.")

    return None