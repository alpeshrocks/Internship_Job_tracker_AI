from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from services.worker.db import SessionLocal
from services.worker.connectors import jobright, indeed, usc_portal
from services.api.crud import upsert_jobs

def pull():
    print("[worker] pulling at", datetime.utcnow().isoformat())
    sources=[jobright, indeed, usc_portal]
    all_items=[]
    for s in sources:
        try:
            all_items.extend(s.fetch())
        except Exception as e:
            print("[worker] failed source:", s.__name__, e)
    from sqlalchemy.orm import Session
    with SessionLocal() as db:
        inserted = upsert_jobs(db, all_items)
        print(f"[worker] upserted {inserted}/{len(all_items)}")

def main():
    sched = BackgroundScheduler(timezone="UTC")
    sched.add_job(pull, "cron", minute=5)
    sched.start()
    print("[worker] scheduler started, doing initial pull...")
    pull()
    import time
    try:
        while True: time.sleep(5)
    except KeyboardInterrupt:
        sched.shutdown()

if __name__ == "__main__":
    main()
