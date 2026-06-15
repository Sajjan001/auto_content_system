from agents.llm import llm

def review_blog(blog):
    response = llm.invoke([
        ("system", "You are a content reviewer. Reply APPROVED or REJECTED only."),
        ("human", f"Review this article:\nTitle: {blog['title']}\nContent: {blog['content']}")
    ], fallback="APPROVED")
    result = response.content.strip().upper()
    print(f"Review: {result}")
    return "APPROVED" in result