# app/routes.py
from flask import Blueprint
from .routes.main import main_bp
from .routes.openai_routes import openai_bp
from .routes.playlists_routes import playlists_bp
from .routes.dashboard_routes import dashboard_bp

# Crear un Blueprint principal si es necesario, o usar la aplicación Flask directamente
# Aquí asumiremos que este archivo se encarga de registrar los blueprints

def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(openai_bp)
    app.register_blueprint(playlists_bp)
    app.register_blueprint(dashboard_bp)