from api.database import db
from api.models.user import User
from api.models.book import Book

def create_user(nome="TestUser",
                email="u@u.com",
                senha="pwr",
                matricula=None,
                saldoMoedas=100):
    """
    Cria um usuário diretamente no banco de teste.
    Usa matricula baseada no email se não informado.
    """
    if matricula is None:
        matricula = email.split("@")[0]
    u = User(
        nome=nome,
        email=email,
        senha=senha,
        matricula=matricula,
        saldoMoedas=saldoMoedas
    )
    db.session.add(u)
    db.session.commit()
    return u

def create_book(titulo="Livro X",
                autor="Autor Y",
                depositor_id=None,
                categoria=None):
    """
    Cria um livro diretamente no banco de teste.
    """
    if depositor_id is None:
        raise ValueError("É preciso informar depositor_id para criar um Book")
    b = Book(
        titulo=titulo,
        autor=autor,
        depositor_id=depositor_id,
        categoria=categoria
    )
    db.session.add(b)
    db.session.commit()
    return b
