import os
import sys
from pathlib import Path
import streamlit as st
from typing import Literal

# ==================================================
# EXPOSE STREAMLIT SECRETS AS ENV VARS (CRITICAL)
# ==================================================
# LangChain + LangSmith only read from os.environ
for key, value in st.secrets.items():
    os.environ[key] = str(value)

# ==================================================
# FIX IMPORT PATH FOR STREAMLIT CLOUD
# ==================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# =============================
# IMPORT BACKEND LOGIC DIRECTLY
# =============================
from backend.news_scraper import fetch_google_news
from backend.reddit_scraper import fetch_reddit
from backend.summarizer import generate_summary

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="NewsNinja – Your AI Journalist",
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


@st.cache_data(show_spinner=False)
def get_news(topic: str):
    return fetch_google_news(topic)


@st.cache_data(show_spinner=False)
def get_reddit(topic: str):
    return fetch_reddit(topic)


# -----------------------------
# App
# -----------------------------
def main():
    # -------- Branding --------
    st.markdown(
        "<h1 style='text-align:center; font-size:3rem;'>NewsNinja</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; font-size:1.2rem; color:gray;'>Your Personal AI Journalist</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # -------------------------
    # Session State
    # -------------------------
    if "topic" not in st.session_state:
        st.session_state.topic = None

    # -------------------------
    # Sidebar
    # -------------------------
    with st.sidebar:
        st.subheader("Settings")

        source_type: Literal["news", "reddit", "both"] = st.selectbox(
            "Select data sources",
            options=["both", "news", "reddit"],
            index=0
        )

        st.markdown("---")
        st.markdown(
            """
            **How it works**
            1. Enter a topic  
            2. Fetch recent news and/or Reddit discussions  
            3. Generate a clean AI-written summary  
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

    col_add, col_clear = st.columns(2)

    with col_add:
        if st.button("Add topic", use_container_width=True):
            if not topic_input.strip():
                show_error("Topic cannot be empty")
            else:
                st.session_state.topic = topic_input.strip()

    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state.topic = None

    # -------------------------
    # Display Selected Topic
    # -------------------------
    if st.session_state.topic:
        st.markdown("**Selected topic**")
        st.info(st.session_state.topic)

    st.markdown("---")

    # -------------------------
    # Generate Summary
    # -------------------------
    if st.button(
        "Generate summary",
        disabled=st.session_state.topic is None,
        use_container_width=True
    ):
        with st.spinner("Collecting data and generating summary..."):
            try:
                topic = st.session_state.topic

                news_data = None
                reddit_data = None

                if source_type in ["news", "both"]:
                    news_data = get_news(topic)

                if source_type in ["reddit", "both"]:
                    reddit_data = get_reddit(topic)

                summary = generate_summary(
                    topic=topic,
                    news=news_data,
                    reddit=reddit_data
                )

                if not summary or not summary.strip():
                    show_error("Summary could not be generated", "Empty response.")
                    return

                st.success("Summary generated")

                st.subheader("Summary")
                st.write(summary)

                st.download_button(
                    label="Download summary",
                    data=summary,
                    file_name="news_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:
                show_error("Failed to generate summary", str(e))


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
