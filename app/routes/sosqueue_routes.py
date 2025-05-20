from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.python.sosqueue.service import QueueService

sos_bp = Blueprint('sosqueue', __name__, url_prefix='/sosqueue')
queue = QueueService()

@sos_bp.route('/', methods=['GET'])
@login_required
def index():
    q = queue.get_queue()
    # pre-compute IDs si los necesitas en el template
    queue_ids = [u['id'] for u in q]
    return render_template('projects/sosqueue/main.html',
                           queue=q,
                           queue_ids=queue_ids)


@sos_bp.route('/join', methods=['POST'])
@login_required
def join():
    try:
        q = queue.join(current_user)
        return jsonify(q)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@sos_bp.route('/work', methods=['POST'])
@login_required
def work():
    try:
        q = queue.work(current_user)
        return jsonify(q)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@sos_bp.route('/leave', methods=['POST'])
@login_required
def leave():
    try:
        q = queue.leave(current_user)
        return jsonify(q)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
