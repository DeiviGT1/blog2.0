# app/python/sosqueue/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
# Se importan las TRES nuevas colas desde el archivo de rutas
from app.routes.sosqueue_routes import available_queue, working_queue, idle_queue


def reset_all_queues():
    """
    Llamado por el scheduler: mueve a todos los usuarios de las colas
    'working' (Ocupados) y 'available' (Disponibles) a la cola 'idle' (Inactivos).
    Esto resetea el estado para el día siguiente.
    """
    print("SCHEDULER: Ejecutando reseteo diario de colas...")
    # 1. Mueve a todos los usuarios que estaban trabajando a la cola de inactivos.
    working_queue.move_all_to(idle_queue)
    # 2. Mueve a todos los usuarios que estaban disponibles a la cola de inactivos.
    available_queue.move_all_to(idle_queue)
    print("SCHEDULER: Reseteo completado.")


def start_scheduler():
    """
    Inicializa APScheduler y programa la tarea de reseteo a las 2:00 AM.
    La zona horaria está configurada como 'America/New_York'.
    """
    sched = BackgroundScheduler(timezone=timezone("America/New_York"))
    # La tarea se ejecuta con una regla 'cron' todos los días a las 2:00 AM.
    sched.add_job(reset_all_queues, 'cron', hour=2, minute=0)
    sched.start()
    return sched