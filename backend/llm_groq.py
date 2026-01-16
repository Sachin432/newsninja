import os
import time
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain.callbacks.manager import CallbackManager

from backend.config import settings

# -----------------------------
# Model configuration
# -----------------------------
MODEL_ID = "llama-3.1-8b-instant"
TEMPERATURE = 0.3
MAX_TOKENS = 600
RETRIES = 2
RETRY_DELAY_SEC = 0.5


# -----------------------------
# LangSmith tracer (EXPLICIT)
# -----------------------------
tracer = LangChainTracer(
    project_name=os.getenv("LANGCHAIN_PROJECT", "NewsNinja")
)
callback_manager = CallbackManager([tracer])


# -----------------------------
# LLM factory
# -----------------------------
def _get_llm():
    """
    Lazy initialization AFTER env vars are set by Streamlit.
    Required for LangSmith tracing.
    """
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY missing")

    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=MODEL_ID,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        callbacks=callback_manager,   # 🔑 THIS ENABLES TRACING
    )


# -----------------------------
# Public API
# -----------------------------
def groq_summarize(
    prompt: str,
    system_message: Optional[str] = None
) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    sys_msg = system_message or (
        "You are a professional news analyst. "
        "Use only the provided information. "
        "Be factual, neutral, and concise."
    )

    messages = [
        SystemMessage(content=sys_msg),
        HumanMessage(content=prompt),
    ]

    last_error = None

    for attempt in range(1, RETRIES + 1):
        try:
            llm = _get_llm()   # created AFTER env vars exist
            response = llm.invoke(messages)

            if not response.content:
                raise RuntimeError("Empty LLM response")

            return response.content.strip()

        except Exception as e:
            last_error = e
            if attempt < RETRIES:
                time.sleep(RETRY_DELAY_SEC)

    raise RuntimeError(
        f"Groq summarization failed after {RETRIES} attempts: {last_error}"
    )
