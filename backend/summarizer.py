from backend.llm_groq import groq_summarize

def generate_summary(topic, news=None, reddit=None):
    prompt = f"""
Topic: {topic}

Official News:
{news or "No official news"}

Reddit Discussions:
{reddit or "No reddit discussion"}

Create a 60-90 second broadcast-style spoken summary.
"""
    return groq_summarize(prompt)
