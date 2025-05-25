# app/python/sosqueue/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from app.routes.sosqueue_routes import queue, queue_idle

def move_actives_to_idle():
    """
    Llamado por el scheduler: mueve todos los activos
    a la cola idle.
    """
    queue.move_all_to(queue_idle)

def start_scheduler():
    """
    Inicializa APScheduler y programa el job a las 2:00 AM (UTC-5).
    """
    sched = BackgroundScheduler(timezone=timezone("America/New_York"))
    # Cron: todos los días a las 2:00
    sched.add_job(move_actives_to_idle, 'cron', hour=2, minute=0)
    sched.start()
    return sched