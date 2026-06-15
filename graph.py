from langgraph.graph import StateGraph, END
from agents.trend_agent import fetch_trends
from agents.generate_agent import generate_blog
from agents.review_agent import review_blog
from agents.publish_agent import publish_blog
from agents.image_agent import search_image

def trend_node(s):
    s["topic"] = s.get("topic") or fetch_trends()
    return s

def generate_node(s):
    s["blog"] = generate_blog(s["topic"])
    s["image"] = search_image(s["topic"])
    return s

def review_node(s):
    s["approved"] = review_blog(s["blog"])
    return s

def publish_node(s):
    publish_blog(s["blog"], s["topic"], s.get("image", ""))
    return s

builder = StateGraph(dict)
builder.add_node("trend", trend_node)
builder.add_node("generate", generate_node)
builder.add_node("review", review_node)
builder.add_node("publish", publish_node)

builder.set_entry_point("trend")
builder.add_edge("trend", "generate")
builder.add_edge("generate", "review")
builder.add_conditional_edges("review", lambda s: "publish" if s.get("approved") else END)
builder.add_edge("publish", END)

graph = builder.compile()
