from .files import files_bp
from .dev import dev_bp
from .test import test_bp

def register_routes(app):
    app.register_blueprint(files_bp)
    app.register_blueprint(dev_bp)
    app.register_blueprint(test_bp)