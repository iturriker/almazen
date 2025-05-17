from flask import Blueprint, request, jsonify, g
from flask import current_app as app

files_bp = Blueprint("files", __name__)

## Endpoint para añadir un nuevo archivo
@files_bp.route("/files/add-file", methods=["POST"])
def add_file():
    # Usar la conexión de la solicitud actual
    connection = g.db_connection

    try:
        data = request.form
        name = data.get("name")
        provider = data.get("provider")
        date = data.get("date")

        if not name or not provider or not date:
            return jsonify({
                "state": "error",
                "message": "Los campos 'name', 'provider' y 'date' son obligatorios",
                "data": None
            }), 400

        with connection.cursor() as cursor:
            exists = check_file(cursor, name)
            if exists:
                return jsonify({
                    "state": "error",
                    "message": f"Ya existe un archivo con el nombre '{name}'",
                    "data": None
                }), 409

            cursor.execute(
                '''INSERT INTO public.files (name, provider, date)
                   VALUES (%s, %s, %s) RETURNING id, name, provider, date;''',
                (name, provider, date)
            )
            file = cursor.fetchone()

        return jsonify({
            "state": "success",
            "message": "Archivo creado",
            "data": {
                "id": file[0],
                "name": file[1],
                "provider": file[2],
                "date": file[3]
            }
        }), 201

    except Exception as e:
        app.logger.error(f"❌ Error en la creación del archivo: {e}")
        return jsonify({
            "state": "error",
            "message": str(e),
            "data": None
        }), 500

## Endpoint para ver todos los archivos
@files_bp.route("/files/get-files", methods=["GET"])
def get_files():
    connection = g.db_connection

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT id, name, provider, date FROM public.files ORDER BY provider;'''
            )
            files = cursor.fetchall()

        files_data = [
            {
                "id": f[0],
                "name": f[1],
                "provider": f[2],
                "date": f[3].isoformat()  # Para que se convierta a formato ISO legible en JS
            }
            for f in files
        ]

        return jsonify({
            "state": "success",
            "message": f"Se recuperaron {len(files_data)} archivos",
            "data": files_data
        }), 200

    except Exception as e:
        app.logger.error(f"❌ Error al obtener archivos: {e}")
        return jsonify({
            "state": "error",
            "message": str(e),
            "data": None
        }), 500


## Funciones auxiliares
def check_file(cursor, name):
    cursor.execute("SELECT id FROM public.files WHERE name = %s;", (name,))
    return cursor.fetchone()