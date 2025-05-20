# app/routes.py

from flask_login import LoginManager
from flask_bootstrap import Bootstrap

def register_routes(app):
    # ——— Inicializar extensiones ———
    # Bootstrap (si quieres usarlo aquí)
    Bootstrap(app)

    # LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # user_loader para reconstruir al usuario desde su ID
    from .routes.auth_routes import User, _CREDENTIALS
    @login_manager.user_loader
    def load_user(user_id):
        for username, cred in _CREDENTIALS.items():
            if cred['id'] == int(user_id):
                return User(cred['id'], username)
        return None

    # ——— Registrar blueprints ———
    from .routes.main import main_bp
    from .routes.openai_routes import openai_bp
    from .routes.playlists_routes import playlists_bp
    from .routes.dashboard_routes import dashboard_bp
    from .routes.blogpost_routes import blogpost_bp
    from .routes.sosqueue_routes import sos_bp
    from .routes.auth_routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(openai_bp)
    app.register_blueprint(playlists_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(blogpost_bp)
    app.register_blueprint(sos_bp)
    app.register_blueprint(auth_bp)