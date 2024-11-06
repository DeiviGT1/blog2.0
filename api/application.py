##application

from flask import Flask

# Crea una instancia de la aplicación Flask
app = Flask(__name__, template_folder='templates', static_url_path="/static")
app.secret_key = 'david'

# Importa los módulos de la aplicación
from .controllers import mod

# Registra los módulos de la aplicación en la instancia de Flask
app.register_blueprint(mod)

if __name__ == '__main__':
    app.run(debug=True)