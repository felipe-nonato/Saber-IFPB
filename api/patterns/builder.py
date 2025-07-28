from api.models.book import Book
from api.models.category import Category


class LivroBuilder:
    def __init__(self):
        self._titulo = None
        self._autor = None
        self._depositor_id = None
        self._categoria = None  # Armazena o objeto Category

    def setTitulo(self, titulo: str):
        self._titulo = titulo
        return self

    def setAutor(self, autor: str):
        self._autor = autor
        return self

    def setCategoria(self, categoria: Category):  # Espera um objeto Category
        self._categoria = categoria
        return self

    def setDepositorId(self, depositor_id: int):
        self._depositor_id = depositor_id
        return self

    def build(self) -> Book:
        if not all([self._titulo, self._autor, self._depositor_id]):
            raise ValueError(
                "Título, autor e ID do depositante são obrigatórios para construir um livro."
            )

        new_book = Book(
            titulo=self._titulo,
            autor=self._autor,
            depositor_id=self._depositor_id,
            categoria=self._categoria,
        )
        return new_book
