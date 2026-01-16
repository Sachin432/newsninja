import streamlit as st
import requests
from typing import Literal

# -----------------------------
# Configuration
# -----------------------------
SOURCE_TYPES = Literal["news", "reddit", "both"]
BACKEND_URL = "http://localhost:1234"
REQUEST_TIMEOUT = 60  # seconds


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="NewsNinja",
    layout="centered",
    initial_sidebar_state="expanded"
)


# -----------------------------
# Helpers
# -----------------------------
def show_error(title: str, details: str | None = None):
    st.error(title)
    if details:
        with st.expander("Error details"):
            st.code(details)


def call_backend(topics, source_type):
    return requests.post(
        f"{BACKEND_URL}/generate-news-summary",
        json={
            "topics": topics,
            "source_type": source_type
        },
        timeout=REQUEST_TIMEOUT
    )


# -----------------------------
# App
# -----------------------------
def main():
    st.title("NewsNinja- Your AI Journalist")
    st.caption("Recent news and Reddit discussions summarized into text")

    # -------------------------
    # Session State
    # -------------------------
    if "topics" not in st.session_state:
        st.session_state.topics = []

    # -------------------------
    # Sidebar
    # -------------------------
    with st.sidebar:
        st.subheader("Settings")

        source_type = st.selectbox(
            "Select data sources",
            options=["both", "news", "reddit"],
            index=0
        )

        st.markdown("---")
        st.markdown(
            """
            **How it works**
            1. Enter a topic  
            2. Fetch latest news and/or Reddit discussions  
            3. Generate a clean text summary  
            """
        )

    # -------------------------
    # Topic Input
    # -------------------------
    st.subheader("Topic")

    topic_input = st.text_input(
        "Enter a topic to analyze",
        placeholder="Example: AI in India"
    )

    col_add, col_clear = st.columns([1, 1])

    with col_add:
        if st.button("Add topic", use_container_width=True):
            if not topic_input.strip():
                show_error("Topic cannot be empty")
            elif topic_input.strip() in st.session_state.topics:
                show_error("Topic already added")
            else:
                # Single-topic system
                st.session_state.topics = [topic_input.strip()]

    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state.topics.clear()

    # -------------------------
    # Display Selected Topic
    # -------------------------
    if st.session_state.topics:
        st.markdown("**Selected topic**")
        st.write(st.session_state.topics[0])

    st.markdown("---")

    # -------------------------
    # Generate Summary
    # -------------------------
    if st.button(
        "Generate summary",
        disabled=len(st.session_state.topics) == 0,
        use_container_width=True
    ):
        with st.spinner("Collecting data and generating summary..."):
            try:
                response = call_backend(
                    topics=st.session_state.topics,
                    source_type=source_type
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Summary generated")

                    st.subheader("Summary")
                    st.write(data["summary"])

                    st.download_button(
                        label="Download summary",
                        data=data["summary"],
                        file_name="news_summary.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                else:
                    try:
                        error_msg = response.json().get("detail", "Unknown error")
                    except Exception:
                        error_msg = response.text

                    show_error(
                        f"Backend error (status {response.status_code})",
                        error_msg
                    )

            except requests.exceptions.ConnectionError:
                show_error(
                    "Backend not reachable",
                    "Make sure the FastAPI backend is running on port 1234."
                )

            except requests.exceptions.Timeout:
                show_error(
                    "Request timed out",
                    "The backend took too long to respond. Try again."
                )

            except Exception as e:
                show_error(
                    "Unexpected error",
                    str(e)
                )


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
