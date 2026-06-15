from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.trend_agent import fetch_trends
from agents.generate_agent import generate_blog
from agents.review_agent import review_blog
from agents.publish_agent import publish_blog
from agents.image_agent import search_image

class BlogState(TypedDict):
    topic: str
    blog: dict
    image: str
    approved: bool


def trend_node(state):
    print("\nTREND NODE")
    if not state.get("topic"):
        state["topic"] = fetch_trends()
    print(f"Using topic: {state['topic']}")
    return state

def generate_node(state):
    print("\nGENERATE NODE")
    state["blog"] = generate_blog(state["topic"])
    state["image"] = search_image(state["topic"])
    print(f"Generated Title: {state['blog'].get('title', 'Unknown')}")
    return state

def review_node(state):
    print("\nREVIEW NODE")
    state["approved"] = review_blog(state["blog"])
    return state

def publish_node(state):
    print("\nPUBLISH NODE")
    publish_blog(state["blog"], state["topic"], state.get("image", ""))
    return state

def route_review(state):
    return "publish" if state.get("approved") else END


builder = StateGraph(dict)

builder.add_node("trend", trend_node)
builder.add_node("generate", generate_node)
builder.add_node("review", review_node)
builder.add_node("publish", publish_node)

builder.set_entry_point("trend")
builder.add_edge("trend", "generate")
builder.add_edge("generate", "review")
builder.add_conditional_edges("review", route_review, {"publish": "publish", END: END})
builder.add_edge("publish", END)

graph = builder.compile()
