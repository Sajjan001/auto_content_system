from agents.llm import llm

def review_blog(blog):
    prompt = f"""You are a content reviewer. Reply APPROVED or REJECTED only.

Review this article:
Title: {blog.get('title', 'Untitled')}
Content: {blog.get('content', '')}

Reply with just APPROVED or REJECTED."""
    response = llm.invoke(prompt, fallback="APPROVED")
    result = response.content.strip().upper()
    print(f"✓ Review Result: {result}")
    return "APPROVED" in result