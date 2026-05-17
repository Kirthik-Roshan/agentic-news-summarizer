# graph.py

from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.fetch_agent import fetch_news
from agents.summarize_agent import summarize_news
from agents.personalize_agent import personalize_summary


class NewsState(TypedDict, total=False):
    topic: str
    title: str
    article: str
    article_url: str
    summary: str
    personalized_summary: str


# Create the workflow
workflow = StateGraph(NewsState)

# Add nodes
workflow.add_node("fetch", fetch_news)
workflow.add_node("summarize", summarize_news)
workflow.add_node("personalize", personalize_summary)

# Define execution order
workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "summarize")
workflow.add_edge("summarize", "personalize")
workflow.add_edge("personalize", END)

# Compile the graph
app_graph = workflow.compile()