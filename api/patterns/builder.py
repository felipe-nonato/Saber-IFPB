from api.models.book import Book
from api.models.category import Category


class LivroBuilder:
    def __init__(self):
        self._titulo = None
        self._autor = None
        self._depositor_id = None
        self._categoria = None
        self._ISBN = None
        self._resumo = None
        self._capa = None
        self._ano_publicacao = None
        self._paginas = None

    def setTitulo(self, titulo: str):
        self._titulo = titulo
        return self

    def setAutor(self, autor: str):
        self._autor = autor
        return self

    def setCategoria(self, categoria: Category):
        self._categoria = categoria
        return self

    def setDepositorId(self, depositor_id: int):
        self._depositor_id = depositor_id
        return self

    def setISBN(self, isbn: str):
        self._ISBN = isbn
        return self

    def setResumo(self, resumo: str):
        self._resumo = resumo
        return self

    def setCapa(self, capa: str):
        self._capa = capa
        return self

    def setAnoPublicacao(self, ano: int):
        self._ano_publicacao = ano
        return self

    def setPaginas(self, paginas: int):
        self._paginas = paginas
        return self

    def build(self) -> Book:
        if not all([self._titulo, self._autor, self._depositor_id]):
            raise ValueError(
                "Título, autor e ID do depositante são obrigatórios para construir um livro."
            )

        # Passa todos os campos opcionais diretamente ao construtor do modelo Book
        new_book = Book(
            titulo=self._titulo,
            autor=self._autor,
            depositor_id=self._depositor_id,
            categoria=self._categoria,
        )
        if self._ISBN is not None:
            new_book.ISBN = self._ISBN
        if self._resumo is not None:
            new_book.resumo = self._resumo
        if self._capa is not None:
            new_book.capa = self._capa
        if self._ano_publicacao is not None:
            new_book.ano_publicacao = self._ano_publicacao
        if self._paginas is not None:
            new_book.paginas = self._paginas

        return new_book
