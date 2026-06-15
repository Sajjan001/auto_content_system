import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class MockResponse:
    def __init__(self, content):
        self.content = content

class SafeLLM:
    def __init__(self):
        key = os.getenv("GROQ_API_KEY")
        self.is_valid = key and not any(p in key for p in ["gsk_qR3e", "your_groq"])
        self.client = None
        if self.is_valid:
            try:
                self.client = ChatGroq(groq_api_key=key, model_name="llama-3.1-8b-instant")
            except Exception:
                self.client = None

    def invoke(self, prompt):
        if self.client:
            try:
                return self.client.invoke(prompt)
            except Exception as e:
                print(f"Groq API Error, using local fallback: {e}")
        
        prompt_str = str(prompt)
        if "title" in prompt_str.lower():
            topic = "AI"
            if "topic:" in prompt_str.lower():
                parts = prompt_str.lower().split("topic:")
                if len(parts) > 1:
                    topic = parts[1].strip().title()
            return MockResponse(f"Understanding the Impact of {topic} in Modern Tech")
        return MockResponse("Artificial Intelligence is shaping our future. This mock article covers key insights, trends, and efficiencies.")

llm = SafeLLM()

def generate_blog(topic):
    return {
        "title": generate_title(topic),
        "content": generate_content(topic)
    }

def generate_title(topic):
    prompt = f"Generate ONE catchy blog title about this specific topic: {topic}"
    response = llm.invoke(prompt)
    title = response.content.strip()
    print(f"Generated Title: {title}")
    return title

def generate_content(topic):
    prompt = f"Write a conversation-style blog article about: {topic}"
    response = llm.invoke(prompt)
    content = response.content.strip()
    print(f"Generated Content: {len(content)} characters")
    return content
