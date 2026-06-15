from database.db import save_blog

def publish_blog(blog, topic, image=""):
    try:
        title = blog.get("title", "Untitled")
        content = blog.get("content", "")
        
        success = save_blog(title=title, topic=topic, content=content, image=image)
        if success:
            print(f"Blog '{title}' published successfully.")
        else:
            print(f"Blog '{title}' publish failed (duplicate or DB error).")
        return success
    except Exception as e:
        print(f"Error publishing blog: {e}")
        return False