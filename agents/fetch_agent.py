import feedparser


def fetch_news(state: dict) -> dict:
    """
    Fetch the latest article for a topic using Google News RSS.
    """
    topic = state.get("topic", "Artificial Intelligence")
    url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}"

    feed = feedparser.parse(url)

    if not feed.entries:
        state["article"] = "No articles found."
        state["title"] = "No Title"
        return state

    entry = feed.entries[0]

    state["title"] = entry.title
    state["article"] = entry.summary
    state["article_url"] = entry.link

    return state