from flask import Blueprint, request, jsonify, g
from flask import current_app as app

users_bp = Blueprint("users", __name__)

## Endpoint para añadir un nuevo usuario
@users_bp.route("/users/add-user", methods=["POST"])
def add_user():
    # Usar la conexión de la solicitud actual
    connection = g.db_connection

    try:
        json = request.get_json()
        name = json.get("name")
        surname = json.get("surname")
        email = json.get("email")

        if not name or not surname or not email:
            return jsonify({
                "state": "error",
                "message": "Los campos 'name', 'surname' y 'email' son obligatorios",
                "data": None
            }), 400

        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO public.users (name, surname, email) 
                VALUES (%s, %s, %s) 
                RETURNING id, name, surname, email;''',
                (name, surname, email)
            )
            user = cursor.fetchone()

        return jsonify({
            "state": "success",
            "message": "Usuario creado con éxito",
            "data": {
                "id": user[0],
                "name": user[1],
                "surname": user[2],
                "email": user[3]
            }
        }), 201

    except Exception as e:
        app.logger.error(f"❌ Error en la creación del usuario: {e}")
        return jsonify({
            "state": "error",
            "message": str(e),
            "data": None
        }), 500