# app/routes/auth_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin

# Credenciales de prueba (usuario: {id, password})
_CREDENTIALS = {
    'Juanfer':   {'id': 1, 'password': '1'},
    'Edison':  {'id': 2, 'password': '2'},
    'Johan ': {'id': 3, 'password': '3'},
    'emp': {'id': 4, 'password': '4'}
}

class User(UserMixin):
    def __init__(self, user_id: int, username: str):
        self.id = user_id
        self.username = username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username', '').strip()
        pwd   = request.form.get('password', '').strip()
        cred  = _CREDENTIALS.get(uname)

        if cred and pwd == cred['password']:
            user = User(cred['id'], uname)
            login_user(user)
            return redirect(url_for('sosqueue.index'))
        flash('Usuario o contraseña inválidos', 'danger')

    return render_template('projects/sosqueue/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sosqueue.index'))