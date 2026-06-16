import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class _MockResponse:
    def __init__(self, content):
        self.content = content

class SafeLLM:
    def __init__(self):
        key = os.getenv("GROQ_API_KEY", "")
        self.client = None
        if key and "your_groq" not in key and "gsk_qR3e" not in key:
            try:
                self.client = ChatGroq(groq_api_key=key, model_name="llama-3.1-8b-instant")
                print(f"✓ Groq API connected")
            except Exception as e:
                print(f"⚠ Groq init failed: {e}")

    def invoke(self, prompt, fallback="APPROVED"):
        if self.client:
            response = self.client.invoke(prompt)
            print(f"✓ LLM response received")
            return response
        print(f"⚠ Using fallback: {fallback}")
        return _MockResponse(fallback)

llm = SafeLLM()
