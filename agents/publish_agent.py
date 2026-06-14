from database.db import save_blog


def publish_blog(blog, topic, image=""):
    try:
        print(f"Publishing blog: title={blog.get('title', '?')}, topic={topic}")
        result = save_blog(
            title=blog["title"],
            topic=topic,
            content=blog["content"],
            image=image
        )
        if result:
            print(f"Blog published successfully: {blog['title']}")
        else:
            print(f"Blog publish failed (likely duplicate): {blog['title']}")
        return result
    except Exception as e:
        print(f"ERROR in publish_blog: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise