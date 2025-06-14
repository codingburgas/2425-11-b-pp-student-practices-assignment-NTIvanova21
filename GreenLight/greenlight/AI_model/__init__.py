from flask import Blueprint


AI_bp = Blueprint('AI', __name__,template_folder='templates', static_folder='static', static_url_path='/AI/static')


from . import routes