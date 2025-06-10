# app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from .routes_main import register_routes
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    
    # Configuración de la aplicación (puedes agregar más configuraciones aquí)
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aquí'  # Reemplaza con una clave secreta segura
    
    from dotenv import load_dotenv
    load_dotenv()
    socketio.init_app(app)

    # Registrar las rutas
    register_routes(app)

    return app