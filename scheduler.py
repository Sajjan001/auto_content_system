from apscheduler.schedulers.background import BackgroundScheduler
from graph import graph

def run_job():
    print("Checking trends...")
    graph.invoke({})
    print("Blog Published")

scheduler = BackgroundScheduler()

scheduler.add_job(
    run_job,
    "interval",
    seconds=10000
)

def start_scheduler():
    scheduler.start()