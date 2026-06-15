from flask import Flask, request, redirect, url_for, render_template
import markdown
import threading
import os
from database.db import init_db, get_all_blogs, get_blog
from graph import graph
from scheduler import start_scheduler, scheduler

app = Flask(__name__)
automation_active = False

init_db()
start_scheduler()

SCHEDULES = {
    "1sec":     {"trigger": "interval", "seconds": 1},
    "1min":     {"trigger": "interval", "minutes": 1},
    "daily2pm": {"trigger": "cron",     "hour": 14, "minute": 0},
}

def run_job():
    try:
        graph.invoke({})
    except Exception as e:
        print(f"Job error: {e}")


@app.route("/")
def home():
    return render_template("index.html", blogs=get_all_blogs(), automation_active=automation_active)


@app.route("/schedule", methods=["POST"])
def schedule_blog():
    global automation_active
    kwargs = SCHEDULES.get(request.form.get("schedule", "daily2pm"), SCHEDULES["daily2pm"])
    scheduler.add_job(run_job, id="blog_job", replace_existing=True, **kwargs)
    threading.Thread(target=run_job, daemon=True).start()
    automation_active = True
    return redirect(url_for("home"))


@app.route("/revoke", methods=["POST"])
def revoke_automation():
    global automation_active
    if scheduler.get_job("blog_job"):
        scheduler.remove_job("blog_job")
    automation_active = False
    return redirect(url_for("home"))


@app.route("/generate")
def generate():
    result = graph.invoke({})
    return render_template("success.html", blog=result.get("blog", {}),
                           topic=result.get("topic", "N/A"), image=result.get("image", ""))


@app.route("/article/<int:blog_id>")
def article(blog_id):
    blog = get_blog(blog_id)
    return render_template("published.html", blog=blog,
                           html_content=markdown.markdown(blog[3]) if blog else "")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)