from flask import Blueprint


stats_bp = Blueprint('stats', __name__,template_folder='templates', static_folder='static', static_url_path='/stats/static')


from . import routes