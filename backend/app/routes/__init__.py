from .users import users_bp
from .files import files_bp
from .dev import dev_bp

def register_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(dev_bp)