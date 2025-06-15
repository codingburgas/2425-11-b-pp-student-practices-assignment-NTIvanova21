from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate, Migrate
from flask_mail import Mail


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

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

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404ErrorPage.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500ErrorPage.html'), 500

    @app.route('/error-test')
    def error_test():
        abort(404)

    return app