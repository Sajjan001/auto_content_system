from flask import Flask, request, redirect, url_for
from flask import render_template
import markdown
from database.db import (
    init_db,
    get_all_blogs,
    get_blog
)

from graph import graph
from scheduler import start_scheduler, scheduler
import threading

app = Flask(__name__)
automation_active = False

init_db()
start_scheduler()
@app.route("/schedule", methods=["POST"])
def schedule_blog():
    schedule_type = request.form["schedule"]
    topic = request.form.get("topic", "")

    print(f"/schedule called with schedule={schedule_type}, topic={topic}")

    def run_job():
        print(f"Scheduled job running for topic: {topic}")
        graph.invoke({"topic": topic})

    if schedule_type == "10sec":
        scheduler.add_job(
            run_job,
            "interval",
            seconds=10,
            id="blog_job",
            replace_existing=True
        )

        # Run once immediately in background to verify scheduling works
        threading.Thread(target=run_job, daemon=True).start()

    elif schedule_type == "1min":
        scheduler.add_job(
            run_job,
            "interval",
            minutes=1,
            id="blog_job",
            replace_existing=True
        )

        # Run once immediately in background to verify scheduling works
        threading.Thread(target=run_job, daemon=True).start()

    elif schedule_type == "daily2pm":
        scheduler.add_job(
            run_job,
            "cron",
            hour=14,
            minute=0,
            id="blog_job",
            replace_existing=True
        )

        # Run once immediately in background to verify scheduling works
        threading.Thread(target=run_job, daemon=True).start()

    global automation_active
    automation_active = True
    print("Automation scheduled and activated")
    return redirect(url_for("home"))


@app.route("/")
def home():
    blogs = get_all_blogs()
    return render_template(
        "index.html",
        blogs=blogs,
        automation_active=automation_active
    )


@app.route("/revoke", methods=["POST"])
def revoke_automation():
    global automation_active
    if scheduler.get_job("blog_job"):
        print("Removing scheduled job blog_job")
        scheduler.remove_job("blog_job")
    automation_active = False
    return redirect(url_for("home"))


@app.route("/generate")
def generate():

    result = graph.invoke({})

    return render_template(
        "success.html",
        blog=result["blog"],
        topic=result["topic"],
        image=result.get("image", "")
    )


@app.route("/article/<int:blog_id>")
def article(blog_id):

    blog = get_blog(blog_id)

    html_content = markdown.markdown(blog[3])

    return render_template(
        "published.html",
        blog=blog,
        html_content=html_content
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)