from api.database import db
from api.models.user import User
from api.models.book import Book
from api.models.category import Category
from api.patterns.mediator import BibliotecaMediator
from api.patterns.builder import LivroBuilder


class SaberFacade:
    def __init__(
        self, db_instance, mediator: BibliotecaMediator, livro_builder: LivroBuilder
    ):
        self.db = db_instance
        self.mediator = mediator
        self.livro_builder = livro_builder  # Instância do builder

    def cadastrarUsuario(self, nome: str, matricula: str = None):
        existing_user = User.query.filter_by(nome=nome).first()
        if existing_user:
            return None, "Usuário com este nome já existe."
        if matricula and User.query.filter_by(matricula=matricula).first():
            return None, "Usuário com esta matrícula já existe."

        new_user = User(nome=nome, matricula=matricula)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user, "Usuário cadastrado com sucesso."

    def depositarLivro(
        self, titulo: str, autor: str, depositor_id: int, categoria_nome: str = None
    ):
        depositor = User.query.get(depositor_id)
        if not depositor:
            return None, "Depositante não encontrado."

        categoria = None
        if categoria_nome:
            categoria = Category.query.filter_by(nome=categoria_nome).first()
            if not categoria:
                # Cria a categoria se ela não existir
                categoria = Category(
                    nome=categoria_nome,
                    descricao=f"Categoria para livros de {categoria_nome}",
                )
                self.db.session.add(categoria)
                self.db.session.flush()  # Garante que a categoria obtenha um ID antes de ser usada

        # Usa o builder
        book = (
            self.livro_builder.setTitulo(titulo)
            .setAutor(autor)
            .setDepositorId(depositor_id)
            .setCategoria(categoria)
            .build()
        )

        # Agora passa o livro e o depositante para o mediador para processar o depósito (concessão de moedas)
        return self.mediator.processarDeposito(book, depositor)

    def alugarLivro(self, book_id: str, user_id: int):
        return self.mediator.processarAluguel(book_id, user_id)

    def processarDevolucao(self, book_id: str, user_id: int):
        return self.mediator.processarDevolucao(book_id, user_id)

    def gerenciarBiblioteca(self):
        """Placeholder para funções mais amplas de gerenciamento de biblioteca, como listar todos os livros, usuários, relatórios."""
        all_books = Book.query.all()
        all_users = User.query.all()
        return {
            "total_books": len(all_books),
            "total_users": len(all_users),
            "available_books": Book.query.filter_by(_estado_nome="disponivel").count(),
            "rented_books": Book.query.filter_by(_estado_nome="alugado").count(),
            "reserved_books": Book.query.filter_by(_estado_nome="reservado").count(),
        }

    def listarLivros(self, estado: str = None):
        query = Book.query
        if estado:
            query = query.filter_by(_estado_nome=estado.lower())
        books = query.all()
        return books

    def obterUsuario(self, user_id: int):
        user = User.query.get(user_id)
        return user

    def reservarLivro(self, book_id: str, user_id: int):
        return self.mediator.processarReserva(book_id, user_id)
