import sys
import json
from pathlib import Path
import sqlite3

# Adiciona o diretório scripts ao sys.path (um nível acima do app.py)
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.append(str(scripts_dir))

from flask import Flask, jsonify, request
from flask_cors import CORS
from getRecommendations import main as get_recommendations

app = Flask(__name__)
CORS(app)  # Permite qualquer origem

DB_PATH = str(Path(__file__).parent.parent / "bd" / "saber.db")


def authenticate_user(email, senha):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM usuarios WHERE email = ? AND senha = ?", (email, senha)
    )

    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]  # Retorna o ID do usuário
    return None  # Retorna None se as credenciais forem inválidas


def get_livros_lidos(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT B.isbn13, B.title, B.thumbnail, NL.nota
        FROM NotasLivros NL
        JOIN Biblioteca B ON NL.isbn13 = B.isbn13
        WHERE NL.usuario_id = ?
    """,
        (user_id,),
    )
    livros = [
        {"isbn13": row[0], "titulo": row[1], "thumbnail": row[2], "avaliacao": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return livros


@app.route("/recommendations", methods=["GET"])
def get_recommendations_route():
    try:
        user_id = request.args.get("id", default=1, type=int)
        num_recommendations = request.args.get("num", default=5, type=int)
        result = get_recommendations(user_id, num_recommendations)
        return json.loads(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
    usuarioId = authenticate_user(email, senha)

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    if usuarioId is not None:
        return jsonify({"success": True, "usuario": usuarioId}), 200
    else:
        return jsonify({"success": False, "error": "Credenciais inválidas"}), 401


@app.route("/livros-lidos", methods=["GET"])
def livros_lidos():
    user_id = request.args.get("id", type=int)
    if not user_id:
        return jsonify({"error": "ID do usuário é obrigatório"}), 400
    livros = get_livros_lidos(user_id)
    return jsonify({"livros_lidos": livros}), 200


if __name__ == "__main__":
    app.run(debug=True)
