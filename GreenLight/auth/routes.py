from flask import render_template
from . import auth_bp

@auth_bp.route('/index')
def index():
    return render_template('auth_base.html')
