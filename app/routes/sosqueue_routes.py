# app/routes/sosqueue_routes.py

from flask import Blueprint, render_template, jsonify, abort
from flask_login import login_required, current_user
from app.python.sosqueue.service import QueueService, JobService
from app import socketio

sos_bp = Blueprint('sosqueue', __name__, url_prefix='/sosqueue')

# --- Instancias de las Colas de Servicio ---
job_queue = JobService()
available_queue = QueueService()
working_queue = QueueService()
idle_queue = QueueService()

def _require_admin():
    """Función de utilidad para proteger rutas de administrador."""
    if not getattr(current_user, 'is_admin', False):
        abort(403, "Se requiere permiso de administrador.")

def broadcast_reload():
    """Emite una señal simple para que todos los clientes recarguen su página."""
    socketio.emit('reload_page')

# --- Rutas HTTP ---

@sos_bp.route('/')
@login_required
def index():
    """
    Renderiza la página principal.
    Obtiene todos los datos necesarios del estado actual y los pasa a la plantilla
    para el renderizado inicial del lado del servidor.
    """
    available_users = available_queue.get_queue()
    working_users = working_queue.get_queue()
    idle_users = idle_queue.get_queue()
    job_count = job_queue.get_job_count()
    active_ids = {u['id'] for u in available_users} | {u['id'] for u in working_users}

    return render_template(
        'projects/sosqueue/main.html',
        available_users=available_users,
        working_users=working_users,
        idle_users=idle_users,
        job_count=job_count,
        active_ids=active_ids
    )

# --- Rutas de Acciones de Empleados ---

@sos_bp.route('/available', methods=['POST'])
@login_required
def become_available():
    """Mueve al usuario de la inactividad a la cola de disponibles."""
    if current_user.is_admin:
        return jsonify({'error': 'Los administradores no entran en la cola'}), 403

    idle_queue.remove(current_user.id)
    available_queue.join(current_user)
    broadcast_reload()
    return jsonify({'status': 'ok'})

@sos_bp.route('/work', methods=['POST'])
@login_required
def start_work():
    """Mueve al primer usuario disponible a la cola de trabajo y consume un trabajo."""
    if not available_queue.get_queue() or available_queue.get_queue()[0]['id'] != current_user.id:
        return jsonify({'error': 'No es tu turno para tomar un trabajo.'}), 403
    if job_queue.get_job_count() == 0:
        return jsonify({'error': 'No hay trabajos disponibles en este momento.'}), 400

    job_queue.take_job()
    user_dict = available_queue.pop_first()
    if user_dict:
        # Se añade el diccionario del usuario directamente a la cola de trabajo.
        with working_queue._lock:
            if not any(u['id'] == user_dict['id'] for u in working_queue._queue):
                working_queue._queue.append(user_dict)
    
    broadcast_reload()
    return jsonify({'status': 'ok'})

@sos_bp.route('/finish', methods=['POST'])
@login_required
def finish_work():
    """Mueve a un usuario de la cola de trabajo de vuelta al final de la cola de disponibles."""
    if not working_queue.remove(current_user.id):
        return jsonify({'error': 'No estabas en la lista de trabajo.'}), 404
    
    available_queue.join(current_user)
    broadcast_reload()
    return jsonify({'status': 'ok'})

@sos_bp.route('/idle', methods=['POST'])
@login_required
def become_idle():
    """Mueve a un usuario de la cola de disponibles a la cola de inactivos."""
    if not available_queue.remove(current_user.id):
        return jsonify({'error': 'No estabas en la cola de disponibles.'}), 404

    idle_queue.join(current_user)
    broadcast_reload()
    return jsonify({'status': 'ok'})

# --- Rutas de Acciones de Administrador ---

@sos_bp.route('/admin/add_job', methods=['POST'])
@login_required
def admin_add_job():
    _require_admin()
    job_queue.add_job()
    broadcast_reload()
    return jsonify({'status': 'ok'})

@sos_bp.route('/admin/move/<int:user_id>/<string:direction>', methods=['POST'])
@login_required
def admin_move(user_id, direction):
    _require_admin()
    if direction == 'up':
        available_queue.move_up(user_id)
    elif direction == 'down':
        available_queue.move_down(user_id)
    
    broadcast_reload()
    return jsonify({'status': 'ok'})

@sos_bp.route('/admin/set_idle/<int:user_id>', methods=['POST'])
@login_required
def admin_set_idle(user_id):
    _require_admin()
    user_to_move = None
    
    # Busca al usuario en la cola de disponibles
    for u in available_queue.get_queue():
        if u['id'] == user_id:
            user_to_move = u
            available_queue.remove(user_id)
            break
    
    # Si no lo encontró, lo busca en la cola de trabajo
    if not user_to_move:
        for u in working_queue.get_queue():
            if u['id'] == user_id:
                user_to_move = u
                working_queue.remove(user_id)
                break

    if not user_to_move:
        return jsonify({'error': 'Usuario no encontrado en colas activas'}), 404

    # Añade al usuario a la cola de inactivos
    with idle_queue._lock:
        if not any(u['id'] == user_id for u in idle_queue._queue):
            idle_queue._queue.append(user_to_move)

    broadcast_reload()
    return jsonify({'status': 'ok'})