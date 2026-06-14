import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)


def review_blog(blog):

    system_prompt = """
    You are an expert content reviewer.

    Check whether the article looks like it was written by a human.

    Approval Criteria:
    - Human-like writing style
    - Natural flow and readability
    - No repetitive AI-generated patterns
    - Proper grammar and sentence structure
    - Professional tone
    - Clear introduction and conclusion
    - SEO-friendly structure

    Return ONLY:

    APPROVED

    or

    REJECTED
    """

    response = llm.invoke([
        ("system", system_prompt),
        ("human", f"""
        Review this article.

        Title:
        {blog['title']}

        Content:
        {blog['content']}
        """)
    ])

    result = response.content.strip().upper()

    print("Review Result:", result)

    return "APPROVED" in result