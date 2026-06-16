from agents.llm import llm

def generate_blog(topic):
    title = _call(f"Generate ONE catchy blog title about: {topic}")
    content = _call(f"Write a conversational 200-300 word blog article about: {topic}", fallback="AI is shaping our future.")
    print(f"✓ Generated: {title}")
    return {"title": title, "content": content}

def _call(prompt, fallback="Untitled"):
    response = llm.invoke(prompt, fallback=fallback)
    return response.content.strip()
