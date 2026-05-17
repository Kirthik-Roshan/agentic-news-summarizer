# Agentic News Summarizer

A personalized news summarization application built using LangGraph, OpenAI, and Streamlit.

## Features

- Fetch latest news from Google News RSS
- Summarize articles using OpenAI
- Personalize summaries based on user preferences
- Feedback loop with persistent profile storage
- Multi-agent orchestration using LangGraph

## Architecture

1. Fetch Agent
2. Summarization Agent
3. Personalization Agent
4. Feedback Agent

## Setup

```bash
git clone https://github.com/yourusername/agentic-news-summarizer.git
cd agentic-news-summarizer

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
