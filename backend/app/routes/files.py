from flask import Blueprint, request, jsonify, g
from flask import current_app as app
from app.services.fish import add_fish
from app.services.providers import add_provider
import traceback

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
        file = request.files.get("file")

        if not name or not provider or not date:
            return jsonify({
                "state": "error",
                "message": "Los campos 'name', 'provider' y 'date' son obligatorios",
                "data": None
            }), 400
        
        if file is None:
            return jsonify({
                "state": "error",
                "message": "El archivo es obligatorio",
                "data": None
            }), 400
        
        with connection.cursor() as cursor:
            provider_result = add_provider(cursor, provider)

            provider_id = provider_result[0]

            exists = check_file(cursor, name)
            if exists:
                return jsonify({
                    "state": "error",
                    "message": f"Ya existe un archivo con el nombre '{name}'",
                    "data": None
                }), 409

            cursor.execute(
                '''INSERT INTO public.files (name, date, provider_id)
                   VALUES (%s, %s, %s) RETURNING id, name, date, provider_id;''',
                (name, date, provider_id)
            )
            file_record = cursor.fetchone()

            add_fish(cursor, file, file_record[0]) # Añadir el archivo a la tabla fish


        return jsonify({
            "state": "success",
            "message": "Archivo creado",
            "data": {
                "id": file_record[0],
                "name": file_record[1],
                "date": file_record[2],
                "provider_id": file_record[3]
            }
        }), 201

    except Exception as e:
        app.logger.error("❌ Error en la creación del archivo:\n%s", traceback.format_exc())
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
                '''SELECT id, name, date, provider_id FROM public.files ORDER BY id;'''
            )
            files = cursor.fetchall()

        files_data = [
            {
                "id": f[0],
                "name": f[1],
                "date": f[2].isoformat(),  # Para que se convierta a formato ISO legible en JS
                "provider_id": f[3]
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