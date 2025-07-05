from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', hours=24)
def run_daily():
    subprocess.run(["python3", "get_companies.py"])
    subprocess.run(["python3", "preprocess_enrich.py"])
    print("✅ Updated leads")

scheduler.start()
