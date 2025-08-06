# api/routes/user_routes.py

from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from api.models.user import User  # para consulta mais clara

user_bp = Blueprint("user_bp", __name__)


def get_facade():
    return current_app.facade


@user_bp.route("/users", methods=["POST"])
def create_user_route():
    data = request.json or {}

    nome = data.get("nome")
    matricula = data.get("matricula")
    email = data.get("email")
    senha = data.get("senha")

    # validações mínimas
    if not all([nome, matricula, email, senha]):
        return (
            jsonify({"error": "nome, matrícula, e-mail e senha são obrigatórios"}),
            400,
        )

    facade = get_facade()
    # agora passando email e senha ao facade
    user, message = facade.cadastrarUsuario(
        nome=nome, email=email, senha=senha, matricula=matricula
    )

    if user:
        return (
            jsonify(
                {
                    "message": message,
                    "user": {
                        "id": user.id,
                        "matricula": user.matricula,
                        "nome": user.nome,
                        "email": user.email,
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
                "email": user.email,
                "saldoMoedas": user.saldoMoedas,
            }
        )

    return jsonify({"error": "Usuário não encontrado"}), 404


@user_bp.route("/login", methods=["POST"])
def login_route():
    data = request.json or {}

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    # Consulta usando o modelo User
    user = User.query.filter_by(email=email).first()

    if not user or user.senha != senha:
        return jsonify({"error": "Credenciais inválidas"}), 401

    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"success": True, "token": token, "usuario": user.nome})
