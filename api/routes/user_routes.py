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
    email = data.get("email")
    senha = data.get("senha")

    # Validação básica
    if not nome:
        return jsonify({"error": "Nome do usuário é obrigatório"}), 400
    if not email:
        return jsonify({"error": "Email do usuário é obrigatório"}), 400
    if not senha:
        return jsonify({"error": "Senha do usuário é obrigatória"}), 400

    facade = get_facade()
    user, message = facade.cadastrarUsuario(
        nome=nome, matricula=matricula, email=email, senha=senha
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
                        "senha": user.senha,
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
                "senha": user.senha,
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
    if not user or user.senha != senha:
        return jsonify({"error": "Credenciais inválidas"}), 401

    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
    }
    # Esta linha está correta para PyJWT
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"success": True, "token": token, "usuario": user.id})


@user_bp.route("/users/<int:user_id>/alugados", methods=["GET"])
def get_livros_alugados(user_id):
    # Importa os modelos necessários
    from api.models.book import Book
    from api.models.rental import Rental

    # Busca os livros alugados pelo usuário e ainda NÃO devolvidos (dataDevolucaoEfetiva == None)
    alugueis = (
        Rental.query.filter_by(rentee_id=user_id)
        .filter(Rental.dataDevolucaoEfetiva == None)
        .all()
    )

    livros = []
    for aluguel in alugueis:
        livro = Book.query.get(aluguel.book_id)
        if livro:
            livros.append(
                {
                    "id": livro.id,
                    "titulo": livro.titulo,
                    "autor": livro.autor,
                    "estado": (
                        livro._estado_nome
                        if hasattr(livro, "_estado_nome")
                        else "alugado"
                    ),
                    "data_devolucao_estimada": (
                        aluguel.dataDevolucao.strftime("%Y-%m-%d")
                        if aluguel.dataDevolucao
                        else None
                    ),
                    "capa": getattr(livro, "capa", None),
                    "resumo": getattr(livro, "resumo", None),
                    "categoria": (
                        livro.categoria.nome
                        if getattr(livro, "categoria", None)
                        else None
                    ),
                    "ISBN": getattr(livro, "ISBN", None),
                    "ano_publicacao": getattr(livro, "ano_publicacao", None),
                    "paginas": getattr(livro, "paginas", None),
                }
            )

    return jsonify(livros)


@user_bp.route("/users/<int:user_id>/devolvidos", methods=["GET"])
def get_livros_devolvidos(user_id):
    from api.models.book import Book
    from api.models.rental import Rental

    # Busca os livros alugados pelo usuário e JÁ devolvidos (dataDevolucaoEfetiva != None)
    alugueis = (
        Rental.query.filter_by(rentee_id=user_id)
        .filter(Rental.dataDevolucaoEfetiva != None)
        .all()
    )

    livros = []
    for aluguel in alugueis:
        livro = Book.query.get(aluguel.book_id)
        if livro:
            livros.append(
                {
                    "id": livro.id,
                    "titulo": livro.titulo,
                    "autor": livro.autor,
                    "estado": (
                        livro._estado_nome
                        if hasattr(livro, "_estado_nome")
                        else "devolvido"
                    ),
                    "data_devolucao_efetiva": (
                        aluguel.dataDevolucaoEfetiva.strftime("%Y-%m-%d")
                        if aluguel.dataDevolucaoEfetiva
                        else None
                    ),
                    "capa": getattr(livro, "capa", None),
                    "resumo": getattr(livro, "resumo", None),
                    "categoria": (
                        livro.categoria.nome
                        if getattr(livro, "categoria", None)
                        else None
                    ),
                    "ISBN": getattr(livro, "ISBN", None),
                    "ano_publicacao": getattr(livro, "ano_publicacao", None),
                    "paginas": getattr(livro, "paginas", None),
                }
            )
    return jsonify(livros)
