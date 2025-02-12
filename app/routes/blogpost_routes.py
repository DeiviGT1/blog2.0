from flask import Blueprint, render_template

blogpost_bp = Blueprint('blogpost', __name__)

@blogpost_bp.route('/blogpost')
def index():
    return render_template('blogpost/index_blogpost.html')

# Data Science Projects
@blogpost_bp.route('/blogpost/distribucion-sobrantes')
def distribucion_sobrantes():
    return render_template('blogpost/projects/data-science/distribucion-sobrantes.html')

@blogpost_bp.route('/blogpost/kmeans')
def kmeans():
    return render_template('blogpost/projects/data-science/kmeans.html')

@blogpost_bp.route('/blogpost/macros-excel')
def macros_excel():
    return render_template('blogpost/projects/data-science/macros-excel.html')

@blogpost_bp.route('/blogpost/predict-calification')
def predict_calification():
    return render_template('blogpost/projects/data-science/predict-calification.html')

@blogpost_bp.route('/blogpost/webscrapping')
def webscrapping():
    return render_template('blogpost/projects/data-science/webscrapping.html')

# Mobile Development Projects
@blogpost_bp.route('/blogpost/motivai')
def motivai():
    return render_template('blogpost/projects/mobile-development/motivai.html')

@blogpost_bp.route('/blogpost/raisen')
def raisen():
    return render_template('blogpost/projects/mobile-development/raisen.html')

# Web Development Projects
@blogpost_bp.route('/blogpost/gato-tuerto')
def gato_tuerto():
    return render_template('blogpost/projects/web-development/gato-tuerto.html')

@blogpost_bp.route('/blogpost/portfolio')
def portfolio():
    return render_template('blogpost/projects/web-development/portfolio.html')