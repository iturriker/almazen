from app import create_flask_app
from app.routes import register_routes

app = create_flask_app()
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)