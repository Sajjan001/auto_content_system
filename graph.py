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


def trend_node(state):

    print(f" TREND NODE ")
    print(f"State: {state}")
    
    if state.get("topic"):
        print(f"Using provided topic: {state['topic']}")
        return {"topic": state["topic"]}
    
    topic = fetch_trends()
    print(f"Using trending topic: {topic}")
    return {"topic": topic}


def generate_node(state):

    print(f"\n GENERATE NODE ")
    print(f"State topic: {state.get('topic', 'NO TOPIC')}")
    
    blog = generate_blog(state["topic"])
    image = search_image(state["topic"])

    print(f"Blog title: {blog.get('title', 'Unknown')}")
    print(f"Image URL: {image}")
    print(f" END GENERATE NODE \n")

    return {
        "topic": state["topic"],
        "blog": blog,
        "image": image
    }


def review_node(state):

    approved = review_blog(state["blog"])

    return {
        "blog": state["blog"],
        "topic": state["topic"],
        "approved": approved
    }


def publish_node(state):

    print(state)

    publish_blog(
        state["blog"],
        state["topic"],
        state.get("image", "")
    )

    return state


def route_review(state):

    if state["approved"]:
        return "publish"

    return END


builder = StateGraph(dict)

builder.add_node("trend", trend_node)

builder.add_node("generate", generate_node)

builder.add_node("review", review_node)

builder.add_node("publish", publish_node)

builder.set_entry_point("trend")

builder.add_edge("trend", "generate")

builder.add_edge("generate", "review")

builder.add_conditional_edges(
    "review",
    route_review,
    {
        "publish": "publish",
        END: END
    }
)

builder.add_edge("publish", END)

graph = builder.compile()
