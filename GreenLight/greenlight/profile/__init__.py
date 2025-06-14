from flask import Blueprint


profile_bp = Blueprint('profile', __name__,template_folder='templates', static_folder='static', static_url_path='/profile/static')


from . import routes