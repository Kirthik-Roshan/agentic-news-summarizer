import os
from openai import OpenAI


def summarize_news(state: dict) -> dict:
    article = state.get("article", "")

    if not article:
        state["summary"] = "No article content available."
        return state

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        state["summary"] = "OPENAI_API_KEY not found in .env"
        return state

    client = OpenAI(api_key=api_key)

    prompt = f"""
Summarize the following news article into 5 concise bullet points.

Article:
{article}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    state["summary"] = response.output_text
    return state