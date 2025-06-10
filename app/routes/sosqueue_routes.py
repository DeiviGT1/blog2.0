# app/routes/sosqueue_routes.py

from flask import Blueprint, render_template, jsonify, abort
from flask_login import login_required, current_user
from app.python.sosqueue.service import QueueService, JobService
from app import socketio

sos_bp = Blueprint('sosqueue', __name__, url_prefix='/sosqueue')
job_queue = JobService()


# Tres colas separadas para cada estado
available_queue = QueueService() # Verde: Disponibles, en orden
working_queue = QueueService()   # Rojo: Ocupados/En trabajo
idle_queue = QueueService()      # Gris: Inactivos/En descanso

def _require_admin():
    if not getattr(current_user, 'is_admin', False):
        abort(403)

def broadcast_state():
    """
    Obtiene el estado actual de todas las colas de sosqueue y lo
    emite a todos los clientes conectados a través de Socket.IO.
    """
    # Esta función contiene la misma lógica para obtener el estado que ya teníamos
    available_users = available_queue.get_queue()
    working_users = working_queue.get_queue()
    idle_users = idle_queue.get_queue()
    job_count = job_queue.get_job_count()
    active_ids = {u['id'] for u in available_users} | {u['id'] for u in working_users}
    first_available_id = available_users[0]['id'] if available_users else None

    state = {
        'available_users': available_users,
        'working_users': working_users,
        'idle_users': idle_users,
        'job_count': job_count,
        'active_ids': list(active_ids),
        'first_available_id': first_available_id,
    }
    # Emite el evento 'update_state'. El cliente estará escuchando este evento.
    socketio.emit('update_state', state)

# ---------------------- VISTA PRINCIPAL ----------------------

@sos_bp.route('/')
@login_required
def index():
    return render_template('projects/sosqueue/main.html')
# ----------- ACCIONES DE EMPLEADOS -------------

@sos_bp.route('/available', methods=['POST'])
@login_required
def become_available():
    """Mueve al usuario de 'idle' a la cola 'available'."""
    if current_user.is_admin:
        return jsonify({'error': 'Los administradores no entran en la cola'}), 403

    idle_queue.remove(current_user.id)
    try:
        available_queue.join(current_user)
        return jsonify({'status': 'ok'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@sos_bp.route('/work', methods=['POST'])
@login_required
def start_work():
    """Mueve al primer usuario de 'available' a 'working' y consume un trabajo."""
    # Validación 1: ¿Es el turno del usuario?
    if not available_queue.get_queue() or available_queue.get_queue()[0]['id'] != current_user.id:
        return jsonify({'error': 'No es tu turno para tomar un trabajo.'}), 403

    # Validación 2: ¿Hay trabajos disponibles?
    if job_queue.get_job_count() == 0:
        return jsonify({'error': 'No hay trabajos disponibles en este momento.'}), 400

    # Si todo está en orden, se consume un trabajo y se mueve al usuario
    job_taken = job_queue.take_job()
    if not job_taken: # Doble chequeo en caso de concurrencia
        return jsonify({'error': 'Justo alguien más tomó el último trabajo.'}), 400

    user_dict = available_queue.pop_first()
    if user_dict:
        with working_queue._lock:
            working_queue._queue.append(user_dict)
    
    broadcast_state()
    return jsonify({'status': 'ok'})

@sos_bp.route('/finish', methods=['POST'])
@login_required
def finish_work():
    """Mueve al usuario de 'working' al final de la cola 'available'."""
    # Se elimina al usuario de la lista de 'working'
    if not working_queue.remove(current_user.id):
        return jsonify({'error': 'No estabas en la lista de trabajo.'}), 404
    
    # Se añade al usuario al final de la cola de 'available'
    try:
        available_queue.join(current_user)
    except ValueError:
        # En caso de que el usuario ya estuviera en la cola de disponibles,
        # lo cual no debería pasar, esta línea evita un error.
        pass
    broadcast_state()
    return jsonify({'status': 'ok'})

@sos_bp.route('/idle', methods=['POST'])
@login_required
def become_idle():
    """Mueve al usuario de 'available' a 'idle' (decide descansar)."""
    if not available_queue.remove(current_user.id):
        return jsonify({'error': 'No estabas en la cola de disponibles.'}), 404

    try:
        idle_queue.join(current_user)
    except ValueError:
        pass
    broadcast_state()
    return jsonify({'status': 'ok'})

@sos_bp.route('/state', methods=['GET'])
@login_required
def get_state():
    """
    NUEVO: Devuelve el estado completo de la aplicación como JSON
    para las actualizaciones dinámicas del cliente.
    """
    available_users = available_queue.get_queue()
    working_users = working_queue.get_queue()
    idle_users = idle_queue.get_queue()
    job_count = job_queue.get_job_count()
    active_ids = {u['id'] for u in available_users} | {u['id'] for u in working_users}
    first_available_id = available_users[0]['id'] if available_users else None

    state = {
        'available_users': available_users,
        'working_users': working_users,
        'idle_users': idle_users,
        'job_count': job_count,
        'active_ids': list(active_ids),
        'first_available_id': first_available_id,
    }
    return jsonify(state)

@socketio.on('connect')
def handle_connect():
    """
    Se ejecuta cuando un nuevo usuario abre la página de sosqueue.
    Le envía inmediatamente el estado actual para que no vea una página vacía.
    """
    broadcast_state()

# ----------- ACCIONES DE ADMINISTRADOR -------------

@sos_bp.route('/admin/move/<int:user_id>/<string:direction>', methods=['POST'])
@login_required
def admin_move(user_id, direction):
    """Mueve a un usuario ARRIBA/ABAJO en la cola de DISPONIBLES."""
    _require_admin()
    if direction == 'up':
        available_queue.move_up(user_id)
    elif direction == 'down':
        available_queue.move_down(user_id)
    broadcast_state()
    return jsonify({'status': 'ok'})

@sos_bp.route('/admin/set_idle/<int:user_id>', methods=['POST'])
@login_required
def admin_set_idle(user_id):
    """Mueve a un usuario desde cualquier cola a la de inactivos."""
    _require_admin()
    # Busca y extrae al usuario de las colas activas
    user_dict = next((u for u in available_queue.get_queue() if u['id'] == user_id), None)
    if user_dict:
        available_queue.remove(user_id)
    else:
        user_dict = next((u for u in working_queue.get_queue() if u['id'] == user_id), None)
        if user_dict:
            working_queue.remove(user_id)

    if not user_dict:
        return jsonify({'error': 'Usuario no encontrado en colas activas'}), 404

    # Añade a idle si no estaba ya
    with idle_queue._lock:
        if not any(u['id'] == user_id for u in idle_queue._queue):
            idle_queue._queue.append(user_dict)
    broadcast_state()
    return jsonify({'status': 'ok'})

@sos_bp.route('/admin/add_job', methods=['POST'])
@login_required
def admin_add_job():
    _require_admin()
    job_queue.add_job()
    broadcast_state()
    return jsonify({'status': 'ok'})