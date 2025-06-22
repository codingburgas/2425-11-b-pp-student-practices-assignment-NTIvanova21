from flask import Blueprint

rating = Blueprint('rating', __name__,template_folder='templates', static_folder='static', static_url_path='/rating/static')


from . import routes 