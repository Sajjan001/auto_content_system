from database.db import save_blog

def publish_blog(blog, topic, image=""):
    return save_blog(blog.get("title", "Untitled"), topic, blog.get("content", ""), image)