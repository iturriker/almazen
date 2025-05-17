import os
import logging
import psycopg
from flask import Flask, g, abort
from flask_cors import CORS

# Función para crear y configurar la aplicación Flask
def create_flask_app():
    app = Flask(__name__)

    # Configuración del logger
    configure_logging(app)

    # Configuración de CORS para controlar los orígenes permitidos
    origins = os.getenv("CORS_ORIGINS", "").split(",")
    CORS(app, origins=origins)
    app.logger.info("origins: %s", origins)

    # Conexión a la base de datos antes de cada solicitud
    @app.before_request
    def before_request():
        try:
            g.db_connection = psycopg.connect(
                host=os.getenv("POSTGRES_HOST"),
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                autocommit=True
            )
            # app.logger.info("✅ Conexión a PostgreSQL establecida.")
        except Exception as e:
            app.logger.error(f"❌ Error al conectar: {e}")
            abort(500, description="No se pudo conectar a la base de datos")

    # Cerrar la conexión después de cada solicitud
    @app.after_request
    def after_request(response):
        try:
            if hasattr(g, 'db_connection'):
                g.db_connection.close()
                # app.logger.info("✅ Conexión a PostgreSQL cerrada.")
        except Exception as e:
            app.logger.warning(f"⚠️ Problema al cerrar la conexión: {e}")
        return response

    return app

# Función para configurar los logs
def configure_logging(app):
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    app.logger = logger  # Asignar el logger a la aplicación