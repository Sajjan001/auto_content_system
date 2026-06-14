from database.db import save_blog


def publish_blog(blog, topic, image=""):
    result = save_blog(
        title=blog["title"],
        topic=topic,
        content=blog["content"],
        image=image
    )
    return result