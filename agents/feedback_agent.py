import json
import os

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



def save_profile(profile):
    os.makedirs("data", exist_ok=True)
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)



def update_feedback(liked: bool):
    profile = load_profile()

    if liked:
        profile["liked_summaries"] += 1
    else:
        profile["disliked_summaries"] += 1

    save_profile(profile)