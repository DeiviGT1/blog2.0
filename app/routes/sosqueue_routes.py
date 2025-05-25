## app/routes/sosqueue_routes.py

from flask import Blueprint, render_template, jsonify, abort
from flask_login import login_required, current_user
from app.python.sosqueue.service import QueueService

sos_bp = Blueprint('sosqueue', __name__, url_prefix='/sosqueue')

# 2 colas separadas
queue = QueueService()
queue_idle = QueueService()

def _remove(service: QueueService, user):
    """Elimina al usuario de la cola (sin rotarlo)."""
    service._queue = [u for u in service._queue if u['id'] != user.id]

def _require_admin():
    if not getattr(current_user, 'is_admin', False):
        abort(403)

# ---------------------- vistas ----------------------

@sos_bp.route('/', methods=['GET'])
@login_required
def index():
    activos   = queue.get_queue()
    queue_ids = [u['id'] for u in activos]               # ids sólo de activos
    combined  = activos + queue_idle.get_queue()         # activos + idle
    return render_template(
        'projects/sosqueue/main.html',
        queue=combined,
        queue_ids=queue_ids
    )

# ----------- acciones de empleados -------------

@sos_bp.route('/join', methods=['POST'])
@login_required
def join():
    if current_user.is_admin:
        return jsonify({'error': 'Los administradores no entran en la cola'}), 403

    _remove(queue_idle, current_user)

    try:
        queue.join(current_user)
        return jsonify({'active': queue.get_queue(),
                        'idle':   queue_idle.get_queue()})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@sos_bp.route('/work', methods=['POST'])
@login_required
def work():
    if current_user.is_admin:
        return jsonify({'error': 'Los administradores no trabajan cola'}), 403

    try:
        queue.work(current_user)
        return jsonify({'active': queue.get_queue(),
                        'idle':   queue_idle.get_queue()})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@sos_bp.route('/leave', methods=['POST'])
@login_required
def leave():
    if current_user.is_admin:
        return jsonify({'error': 'Los administradores no pueden salir'}), 403

    _remove(queue, current_user)
    try:
        queue_idle.join(current_user)
    except ValueError:
        pass

    return jsonify({'active': queue.get_queue(),
                    'idle':   queue_idle.get_queue()})

# ----------- acciones de administrador -------------

@sos_bp.route('/admin/move/<int:user_id>/<string:direction>', methods=['POST'])
@login_required
def admin_move(user_id, direction):
    _require_admin()
    if direction == 'up':
        queue.move_up(user_id)
    elif direction == 'down':
        queue.move_down(user_id)
    else:
        return jsonify({'error': 'Dirección inválida'}), 400
    return jsonify({'active': queue.get_queue(),
                    'idle':   queue_idle.get_queue()})

@sos_bp.route('/admin/idle/<int:user_id>', methods=['POST'])
@login_required
def admin_send_to_idle(user_id):
    _require_admin()

    # 1) quitar de activos
    with queue._lock:
        for idx, u in enumerate(queue._queue):
            if u['id'] == user_id:
                user_dict = queue._queue.pop(idx)
                break
        else:
            return jsonify({'error': 'Usuario no encontrado en activos'}), 404

    # 2) añadir a idle (si no estaba)
    with queue_idle._lock:
        if not any(u['id'] == user_id for u in queue_idle._queue):
            queue_idle._queue.append(user_dict)

    return jsonify({'active': queue.get_queue(),
                    'idle':   queue_idle.get_queue()})