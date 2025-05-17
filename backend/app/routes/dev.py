from flask import Blueprint, jsonify, g
from flask import current_app as app

dev_bp = Blueprint("dev", __name__)

# Endpoint para resetear la base de datos (vaciar tablas y reiniciar ID autoincrementales)
@dev_bp.route("/dev/db/reset", methods=["POST"])
def reset_database():
    connection = g.db_connection

    try:
        with connection.cursor() as cursor:
            tables = ['providers', 'files', 'fish']

            # Construir y ejecutar el comando TRUNCATE
            sql = f"TRUNCATE TABLE {', '.join(f'public.{t}' for t in tables)} RESTART IDENTITY CASCADE;"
            cursor.execute(sql)
            connection.commit()

        return jsonify({
            "state": "success",
            "message": "✅ Base de datos reseteada correctamente",
            "data": None
        }), 200

    except Exception as e:
        app.logger.error(f"❌ Error al resetear la base de datos: {e}")
        return jsonify({
            "state": "error",
            "message": str(e),
            "data": None
        }), 500
