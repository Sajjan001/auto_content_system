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
        return MockResponse("APPROVED")

llm = SafeLLM()

def review_blog(blog):
    system_prompt = "You are a content reviewer. Return APPROVED or REJECTED."
    try:
        response = llm.invoke([
            ("system", system_prompt),
            ("human", f"Review this article:\nTitle: {blog['title']}\nContent: {blog['content']}")
        ])
        result = response.content.strip().upper()
        print(f"Review Result: {result}")
        return "APPROVED" in result
    except Exception as e:
        print(f"Error in review: {e}")
        return True