# run.py
from app import create_app
from app.python.sosqueue.scheduler import start_scheduler

app = create_app()
scheduler = start_scheduler()

if __name__ == '__main__':
    # Ejecuta la aplicación en modo debug para desarrollo
    app.run(debug=True)