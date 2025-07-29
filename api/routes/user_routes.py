from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime

# current_app é usado para acessar a instância da aplicação Flask e suas propriedades
# que foram anexadas na função create_app.
# Ex: current_app.facade

user_bp = Blueprint("user_bp", __name__)


def get_facade():
    return current_app.facade


@user_bp.route("/users", methods=["POST"])
def create_user_route():
    data = request.json
    nome = data.get("nome")
    matricula = data.get("matricula")
    if not nome:
        return jsonify({"error": "Nome do usuário é obrigatório"}), 400

    facade = get_facade()
    user, message = facade.cadastrarUsuario(nome=nome, matricula=matricula)
    if user:
        return (
            jsonify(
                {
                    "message": message,
                    "user": {
                        "id": user.id,
                        "matricula": user.matricula,
                        "nome": user.nome,
                        "saldoMoedas": user.saldoMoedas,
                    },
                }
            ),
            201,
        )
    else:
        return jsonify({"error": message}), 400


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    facade = get_facade()
    user = facade.obterUsuario(user_id)
    if user:
        return jsonify(
            {
                "id": user.id,
                "matricula": user.matricula,
                "nome": user.nome,
                "saldoMoedas": user.saldoMoedas,
            }
        )
    return jsonify({"error": "Usuário não encontrado"}), 404


@user_bp.route("/login", methods=["POST"])
def login_route():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")
    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    user = (
        current_app.db.session.query(current_app.db.Model.metadata.tables["users"])
        .filter_by(email=email)
        .first()
    )
    # Ou, se você tem o modelo User importado:
    # user = User.query.filter_by(email=email).first()
    if not user or user.senha != senha:
        return jsonify({"error": "Credenciais inválidas"}), 401

    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"success": True, "token": token, "usuario": user.nome})
