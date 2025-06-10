# run.py
from app import create_app
from app.python.sosqueue.scheduler import start_scheduler
from app import socketio

app = create_app()
scheduler = start_scheduler()

if __name__ == '__main__':
    # Ejecuta la aplicación en modo debug para desarrollo
    socketio.run(app, debug=True)
