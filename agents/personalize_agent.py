import os
import json
from openai import OpenAI

PROFILE_PATH = "data/profile.json"


def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return {
            "preferred_topics": ["Artificial Intelligence", "Startups"],
            "summary_style": "bullet points",
            "liked_summaries": 0,
            "disliked_summaries": 0,
        }

    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def personalize_summary(state: dict) -> dict:
    summary = state.get("summary", "")
    profile = load_profile()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        state["personalized_summary"] = "OPENAI_API_KEY not found in .env"
        return state

    client = OpenAI(api_key=api_key)

    prompt = f"""
Rewrite the summary according to user preferences.

Preferred Topics: {profile['preferred_topics']}
Summary Style: {profile['summary_style']}

Summary:
{summary}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    state["personalized_summary"] = response.output_text
    return state