import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Ensure the GROQ API key is available at runtime. On Render set this in
# Environment → Environment Variables, or provide a local .env (do NOT commit).
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Add it to Render environment variables or a local .env file"
    )

llm = ChatGroq(
    groq_api_key=groq_key,
    model_name="llama-3.1-8b-instant"
)


def generate_blog(topic):
    
    title = generate_title(topic)
    content = generate_content(topic)

    return {
        "title": title,
        "content": content
    }


def generate_title(topic):
    print(f"TITLE GENERATION - Topic received: {topic}")
    
    prompt = f"""Your task: Generate ONE catchy blog title ONLY about this specific topic: {topic}

DO NOT deviate from this topic.
DO NOT write about other topics.
ONLY write the title, nothing else.

Topic: {topic}
Title:"""
    
    response = llm.invoke(prompt)
    title = response.content.strip()
    
    print(f"Generated Title: {title}")
    return title if title else "Untitled"


def generate_content(topic):
    print(f"CONTENT GENERATION - Topic received: {topic}")
    
    prompt = f"""Write a blog article ONLY about: {topic}

Stay focused on this topic: {topic}
Do not write about anything else.

Make it conversational and human-like with short paragraphs, real examples, and personality.

Start writing the article about {topic}:"""
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    print(f"Generated Content: {len(content)} characters")
    return content