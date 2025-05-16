from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
bootstrap = Bootstrap()
#login_manager = LoginManager()
def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    #db.init_app(app)
    bootstrap.init_app(app)
    #login_manager.init_app(app)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .main import main_bp
    app.register_blueprint(main_bp)

    from .profile import profile_bp
    app.register_blueprint(profile_bp)

    from .statistics import stats_bp
    app.register_blueprint(stats_bp)

    from .AI_model import AI_bp
    app.register_blueprint(AI_bp)

    return app