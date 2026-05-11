from flask import Blueprint, render_template

meper_bp = Blueprint('meper', __name__)


@meper_bp.route('/meper')
def meper():
    return render_template('meper/index.html')
