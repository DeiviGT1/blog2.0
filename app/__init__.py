# app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    
    # Configuración de la aplicación (puedes agregar más configuraciones aquí)
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aquí'  # Reemplaza con una clave secreta segura
    
    # Inicializar extensiones
    Bootstrap(app)
    
    # Registrar rutas desde routes.py
    from . import routes
    app.register_blueprint(routes.main_bp)
    
    return app