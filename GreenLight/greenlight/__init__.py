from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate, Migrate
from flask_mail import Mail



# Initialize Flask extensions
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
def create_app(config):
    """
       Flask application factory.

       Args:
           config (str or object): The Python object path or class containing app config settings.

       Returns:
           Flask app instance configured with blueprints, extensions, and error handlers.
    """
    app = Flask(__name__)

    # Load configuration settings from the provided object
    app.config.from_object(config)

    # Initialize Flask extensions with app instance
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Register Blueprints
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

    from .rating import rating
    app.register_blueprint(rating)

    @app.errorhandler(404)
    def not_found_error(error):
        """Render a custom 404 error page."""
        return render_template('ErrorPage.html', error = 404), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Render a custom 500 error page."""
        return render_template('ErrorPage.html', error = 500), 500

    @app.errorhandler(403)
    def internal_error(error):
        """Render a custom 403 error page."""
        return render_template('ErrorPage.html', error=403), 403

    @app.route('/error-test')
    def error_test():
        """Route to manually test error handler by forcing 403 error."""
        abort(403)

    return app