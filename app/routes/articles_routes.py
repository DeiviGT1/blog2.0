from flask import Blueprint, render_template

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles')
def index():
    return render_template('articles/index.html')

@articles_bp.route('/articles/ia-mercado-laboral')
def ia_mercado_laboral():
    return render_template('articles/ia-mercado-laboral.html')
