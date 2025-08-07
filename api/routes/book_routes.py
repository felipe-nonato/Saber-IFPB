from flask import Blueprint, request, jsonify, current_app
from api.models.rental import Rental

book_bp = Blueprint("book_bp", __name__)


def get_facade():
    return current_app.facade


@book_bp.route("/books", methods=["POST"])
def deposit_book_route():
    data = request.json
    titulo = data.get("titulo")
    autor = data.get("autor")
    depositor_id = data.get("depositor_id")
    categoria_nome = data.get("categoria")
    ISBN = data.get("ISBN")
    resumo = data.get("resumo")
    capa = data.get("capa")
    ano_publicacao = data.get("ano_publicacao")
    paginas = data.get("paginas")

    if not all([titulo, autor, depositor_id]):
        return (
            jsonify({"error": "Título, autor e ID do depositante são obrigatórios"}),
            400,
        )

    try:
        depositor_id = int(depositor_id)
    except ValueError:
        return jsonify({"error": "ID do depositante deve ser um número inteiro"}), 400

    facade = get_facade()
    book, message = facade.depositarLivro(titulo, autor, depositor_id, categoria_nome)
    if book:
        return (
            jsonify(
                {
                    "message": message,
                    "book": {
                        "id": book.id,
                        "titulo": book.titulo,
                        "autor": book.autor,
                        "estado": book._estado_nome,
                        "depositor_id": book.depositor_id,
                        "categoria": book.categoria.nome if book.categoria else None,
                        "ISBN": book.ISBN,
                        "resumo": book.resumo,
                        "capa": book.capa,
                        "ano_publicacao": book.ano_publicacao,
                        "paginas": book.paginas,
                    },
                }
            ),
            201,
        )
    else:
        return jsonify({"error": message}), 400


@book_bp.route("/books", methods=["GET"])
def list_books_route():
    estado = request.args.get("estado")
    facade = get_facade()
    books = facade.listarLivros(estado=estado)
    book_list = [
        {
            "id": book.id,
            "titulo": book.titulo,
            "autor": book.autor,
            "estado": book._estado_nome,
            "depositor_id": book.depositor_id,
            "categoria": book.categoria.nome if book.categoria else None,
            "ISBN": book.ISBN,
            "resumo": book.resumo,
            "capa": book.capa,
            "ano_publicacao": book.ano_publicacao,
            "paginas": book.paginas,
        }
        for book in books
    ]
    return jsonify(book_list)


@book_bp.route("/books/<book_id>/rent", methods=["POST"])
def rent_book_route(book_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "ID do usuário é obrigatório"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "ID do usuário deve ser um número inteiro"}), 400

    facade = get_facade()
    book, message = facade.alugarLivro(book_id, user_id)
    if book:
        latest_rental = (
            Rental.query.filter_by(book_id=book.id, rentee_id=user_id)
            .order_by(Rental.dataAluguel.desc())
            .first()
        )
        return_date_str = (
            latest_rental.dataDevolucao.strftime("%Y-%m-%d %H:%M:%S")
            if latest_rental and latest_rental.dataDevolucao
            else None
        )

        return (
            jsonify(
                {
                    "message": message,
                    "book": {
                        "id": book.id,
                        "titulo": book.titulo,
                        "estado": book._estado_nome,
                        "rentee_id": book.rentee_id,
                        "data_devolucao_estimada": return_date_str,
                        "ISBN": book.ISBN,
                        "resumo": book.resumo,
                        "capa": book.capa,
                        "ano_publicacao": book.ano_publicacao,
                        "paginas": book.paginas,
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({"error": message}), 400


@book_bp.route("/books/<book_id>/return", methods=["POST"])
def return_book_route(book_id):
    from datetime import datetime

    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "ID do usuário é obrigatório"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "ID do usuário deve ser um número inteiro"}), 400

    facade = get_facade()
    book, message = facade.processarDevolucao(book_id, user_id)
    if book:
        # Atualiza a data de devolução efetiva para agora
        rental = (
            Rental.query.filter_by(book_id=book.id, rentee_id=user_id)
            .filter(Rental.dataDevolucaoEfetiva == None)
            .order_by(Rental.dataAluguel.desc())
            .first()
        )
        if rental:
            rental.dataDevolucaoEfetiva = datetime.now()
            current_app.db.session.commit()

        return (
            jsonify(
                {
                    "message": message,
                    "book": {
                        "id": book.id,
                        "titulo": book.titulo,
                        "estado": book._estado_nome,
                        "ISBN": book.ISBN,
                        "resumo": book.resumo,
                        "capa": book.capa,
                        "ano_publicacao": book.ano_publicacao,
                        "paginas": book.paginas,
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({"error": message}), 400


@book_bp.route("/books/<book_id>/reserve", methods=["POST"])
def reserve_book_route(book_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "ID do usuário é obrigatório"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "ID do usuário deve ser um número inteiro"}), 400

    facade = get_facade()
    book, message = facade.reservarLivro(book_id, user_id)
    if book:
        return (
            jsonify(
                {
                    "message": message,
                    "book": {
                        "id": book.id,
                        "titulo": book.titulo,
                        "estado": book._estado_nome,
                        "reserved_by_id": book.reserved_by_id,
                        "ISBN": book.ISBN,
                        "resumo": book.resumo,
                        "capa": book.capa,
                        "ano_publicacao": book.ano_publicacao,
                        "paginas": book.paginas,
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({"error": message}), 400
