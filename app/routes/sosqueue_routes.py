# app/routes/sosqueue_routes.py

from flask import Blueprint, render_template, jsonify, abort
from flask_login import login_required, current_user
from app.python.sosqueue.service import QueueService, JobService
# Se importa la instancia de socketio desde el __init__.py de la app
from app import socketio

sos_bp = Blueprint('sosqueue', __name__, url_prefix='/sosqueue')
job_queue = JobService()

available_queue = QueueService()
working_queue = QueueService()
idle_queue = QueueService()

def _require_admin():
    if not getattr(current_user, 'is_admin', False):
        abort(403, "Se requiere permiso de administrador.")

def broadcast_state():
    """Obtiene el estado completo y lo emite a todos los clientes."""
    state = {
        'available_users': available_queue.get_queue(),
        'working_users': working_queue.get_queue(),
        'idle_users': idle_queue.get_queue(),
        'job_count': job_queue.get_job_count(),
        'active_ids': list({u['id'] for u in available_queue.get_queue()} | {u['id'] for u in working_queue.get_queue()}),
        'first_available_id': available_queue.get_queue()[0]['id'] if available_queue.get_queue() else None,
    }
    socketio.emit('update_state', state)

@socketio.on('connect')
def handle_connect():
    """Cuando un cliente se conecta, se le envía el estado actual."""
    broadcast_state()

@sos_bp.route('/')
@login_required
def index():
    """La ruta principal solo sirve el HTML. El contenido se llenará vía Socket.IO."""
    return render_template('projects/sosqueue/main.html')

# --- Acciones de Empleados ---

@sos_bp.route('/available', methods=['POST'])
@login_required
def become_available():
    if current_user.is_admin: return jsonify({'error': 'Los administradores no entran en la cola'}), 403
    idle_queue.remove(current_user.id)
    try:
        available_queue.join(current_user)
    except ValueError: pass
    broadcast_state() # <-- Notificar a todos
    return jsonify({'status': 'ok'})

@sos_bp.route('/work', methods=['POST'])
@login_required
def start_work():
    if not available_queue.get_queue() or available_queue.get_queue()[0]['id'] != current_user.id: return jsonify({'error': 'No es tu turno.'}), 403
    if job_queue.get_job_count() == 0: return jsonify({'error': 'No hay trabajos disponibles.'}), 400
    job_taken = job_queue.take_job()
    if not job_taken: return jsonify({'error': 'Alguien más tomó el último trabajo.'}), 400
    user_dict = available_queue.pop_first()
    if user_dict: working_queue.join(user_dict) # Usar join en lugar de manipulación directa
    broadcast_state() # <-- Notificar a todos
    return jsonify({'status': 'ok'})

@sos_bp.route('/finish', methods=['POST'])
@login_required
def finish_work():
    if not working_queue.remove(current_user.id): return jsonify({'error': 'No estabas en la lista de trabajo.'}), 404
    try:
        available_queue.join(current_user)
    except ValueError: pass
    broadcast_state() # <-- Notificar a todos
    return jsonify({'status': 'ok'})

@sos_bp.route('/idle', methods=['POST'])
@login_required
def become_idle():
    if not available_queue.remove(current_user.id): return jsonify({'error': 'No estabas en la cola.'}), 404
    try:
        idle_queue.join(current_user)
    except ValueError: pass
    broadcast_state() # <-- Notificar a todos
    return jsonify({'status': 'ok'})

# --- Acciones de Administrador ---

@sos_bp.route('/admin/add_job', methods=['POST'])
@login_required
def admin_add_job():
    _require_admin()
    job_queue.add_job()
    broadcast_state() # <-- Notificar a todos
    return jsonify({'status': 'ok'})

@sos_bp.route('/admin/move/<int:user_id>/<string:direction>', methods=['POST'])
@login_required
def admin_move(user_id, direction):
    _require_admin()
    if direction == 'up': available_queue.move_up(user_id)
    elif direction == 'down': available_queue.move_down(user_id)
    broadcast_state() # <-- Notificar a todos
    return jsonify({'status': 'ok'})

@sos_bp.route('/admin/set_idle/<int:user_id>', methods=['POST'])
@login_required
def admin_set_idle(user_id):
    _require_admin()
    user_to_move = None
    if available_queue.remove(user_id):
        user_to_move = next((u for u in available_queue.get_queue() if u['id'] == user_id), None)
    elif working_queue.remove(user_id):
        user_to_move = next((u for u in working_queue.get_queue() if u['id'] == user_id), None)
    if not user_to_move: return jsonify({'error': 'Usuario no encontrado en colas activas'}), 404
    try:
        idle_queue.join(user_to_move)
    except ValueError: pass
    broadcast_state() # <-- Notificar a todos
    return jsonify({'status': 'ok'})