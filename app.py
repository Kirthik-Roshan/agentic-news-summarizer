# app.py

import os
import traceback

import streamlit as st
from dotenv import load_dotenv

# Load environment variables BEFORE importing modules that may use them
load_dotenv()

st.set_page_config(
    page_title="Agentic News Summarizer",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Personalized News Summarization App")
st.caption("Built with LangGraph, OpenAI, and Streamlit")

# Optional debug info
with st.sidebar:
    st.header("System Status")
    st.write("OpenAI API Key Loaded:", bool(os.getenv("OPENAI_API_KEY")))

# Import project modules after load_dotenv()
try:
    from graph import app_graph
    from agents.feedback_agent import load_profile, update_feedback
except Exception as e:
    st.error("❌ Failed to import project modules.")
    st.code(traceback.format_exc())
    st.stop()

# Load user profile
try:
    profile = load_profile()
except Exception as e:
    st.error("❌ Failed to load profile.json")
    st.code(traceback.format_exc())
    st.stop()

# Sidebar profile display
with st.sidebar:
    st.header("👤 User Profile")
    st.write(
        "Preferred Topics:",
        ", ".join(profile.get("preferred_topics", []))
    )
    st.write(
        "Summary Style:",
        profile.get("summary_style", "bullet points")
    )
    st.write(
        "👍 Likes:",
        profile.get("liked_summaries", 0)
    )
    st.write(
        "👎 Dislikes:",
        profile.get("disliked_summaries", 0)
    )

# Main input
topic = st.text_input(
    "Enter a news topic",
    value="Artificial Intelligence"
)

# Generate summary
if st.button("Generate Personalized Summary"):
    try:
        with st.spinner("Fetching and summarizing latest news..."):
            result = app_graph.invoke({"topic": topic})

        # Store result in session state so feedback buttons work
        st.session_state["last_result"] = result

    except Exception:
        st.error("❌ Error while running the agent workflow.")
        st.code(traceback.format_exc())
        st.stop()

# Display results if available
if "last_result" in st.session_state:
    result = st.session_state["last_result"]

    st.subheader("📰 Article Title")
    st.write(result.get("title", "No title available"))

    article_url = result.get("article_url")
    if article_url:
        st.markdown(f"[Read Original Article]({article_url})")

    st.subheader("📄 Raw Summary")
    st.write(result.get("summary", "No summary generated"))

    st.subheader("✨ Personalized Summary")
    st.write(
        result.get(
            "personalized_summary",
            "No personalized summary generated"
        )
    )

    st.divider()

    st.subheader("📝 Was this summary helpful?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Helpful"):
            try:
                update_feedback(True)
                st.success("Thanks! Your positive feedback was saved.")
                st.rerun()
            except Exception:
                st.error("Failed to save feedback.")
                st.code(traceback.format_exc())

    with col2:
        if st.button("👎 Not Helpful"):
            try:
                update_feedback(False)
                st.warning("Thanks! Your feedback was saved.")
                st.rerun()
            except Exception:
                st.error("Failed to save feedback.")
                st.code(traceback.format_exc())