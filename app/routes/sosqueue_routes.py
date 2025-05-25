## app/routes/sosqueue_routes.py

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.python.sosqueue.service import QueueService

sos_bp = Blueprint('sosqueue', __name__, url_prefix='/sosqueue')

# 2 colas separadas
queue = QueueService()
queue_idle = QueueService()

def _remove(service: QueueService, user):
    """
    Elimina al usuario de la cola (sin rotarlo).
    Accede a service._queue directamente para remover.
    """
    # _queue es lista de dicts {'id', 'name'}
    service._queue = [u for u in service._queue if u['id'] != user.id]

@sos_bp.route('/', methods=['GET'])
@login_required
def index():
    activos = queue.get_queue()
    # **no** conviertas a strings, déjalos como ints
    queue_ids = [u['id'] for u in activos]

    combined = activos + queue_idle.get_queue()
    return render_template(
        'projects/sosqueue/main.html',
        queue=combined,
        queue_ids=queue_ids
    )

@sos_bp.route('/join', methods=['POST'])
@login_required
def join():
    # Si estaba en idle, lo quitamos de ahí
    _remove(queue_idle, current_user)

    try:
        queue.join(current_user)
        return jsonify({
            'active': queue.get_queue(),
            'idle': queue_idle.get_queue()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@sos_bp.route('/work', methods=['POST'])
@login_required
def work():
    try:
        queue.work(current_user)
        return jsonify({
            'active': queue.get_queue(),
            'idle': queue_idle.get_queue()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@sos_bp.route('/leave', methods=['POST'])
@login_required
def leave():
    # Si estás en activos, te quitas de ahí
    _remove(queue, current_user)
    # Y te añades a idle
    try:
        queue_idle.join(current_user)
    except ValueError:
        # si ya estabas en idle, lo ignoramos
        pass

    return jsonify({
        'active': queue.get_queue(),
        'idle': queue_idle.get_queue()
    })