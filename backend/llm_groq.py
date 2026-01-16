import time
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from backend.config import settings


# -----------------------------
# Configuration
# -----------------------------
MODEL_ID = "llama-3.1-8b-instant"
TEMPERATURE = 0.3
MAX_TOKENS = 600
RETRIES = 2
RETRY_DELAY_SEC = 0.5


# -----------------------------
# Validate configuration
# -----------------------------
if not settings.GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing. Check Streamlit secrets.")

# LangSmith tracing is enabled automatically via env vars:
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY
# LANGCHAIN_PROJECT=NewsNinja


# -----------------------------
# LLM Initialization (LangChain)
# -----------------------------
llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name=MODEL_ID,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS,
)


# -----------------------------
# Public API
# -----------------------------
def groq_summarize(
    prompt: str,
    system_message: Optional[str] = None
) -> str:
    """
    Generate a concise text summary using Groq via LangChain.

    - Fully traceable in LangSmith
    - Safe for Streamlit Cloud
    - Retries on transient failures
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    sys_msg = system_message or (
        "You are a professional news analyst. "
        "Use only the information provided. "
        "Write concise, factual summaries in plain text."
    )

    messages = [
        SystemMessage(content=sys_msg),
        HumanMessage(content=prompt),
    ]

    last_error = None

    for attempt in range(1, RETRIES + 1):
        try:
            response = llm.invoke(messages)

            content = response.content
            if not content or not content.strip():
                raise RuntimeError("Empty response from Groq model.")

            return content.strip()

        except Exception as e:
            last_error = e
            if attempt < RETRIES:
                time.sleep(RETRY_DELAY_SEC)

    raise RuntimeError(
        f"Groq summarization failed after {RETRIES} attempts: {last_error}"
    )
