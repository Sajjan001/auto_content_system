from agents.llm import llm

def generate_blog(topic):
    return {
        "title": _call(f"Generate ONE catchy blog title about: {topic}"),
        "content": _call(f"Write a conversational blog article about: {topic}", fallback="AI is shaping our future.")
    }

def _call(prompt, fallback="Untitled"):
    response = llm.invoke(prompt, fallback=fallback)
    return response.content.strip()
