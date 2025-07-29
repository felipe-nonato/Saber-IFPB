from api.database import db
from api.patterns.state import (
    EstadoLivro,
    Disponivel,
    Alugado,
    Reservado,
)  # Import state classes
from api.models.category import Category  # Import Category model
import uuid  # Para gerar UUIDs


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )  # Alterado para String e UUID
    titulo = db.Column(
        db.String(120), nullable=False
    )  # Renomeado 'title' para 'titulo'
    autor = db.Column(
        db.String(120), nullable=False
    )  # Adicionado 'autor' conforme builder
    ISBN = db.Column(
        db.String(20), unique=True, nullable=True
    )  # Adicionado 'ISBN' – opcional, único
    resumo = db.Column(
        db.Text, nullable=True
    )  # Adicionado 'resumo' – opcional, texto longo
    capa = db.Column(
        db.String(255), nullable=True
    )  # Adicionado 'capa' – opcional, URL da imagem
    ano_publicacao = db.Column(
        db.Integer, nullable=True
    )  # Adicionado 'ano_publicacao' – opcional, ano do livro
    paginas = db.Column(
        db.Integer, nullable=True
    )  # Adicionado 'paginas' – opcional, número de páginas
    depositor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Campo para armazenar o nome do estado (para persistência no DB)
    _estado_nome = db.Column("estado", db.String(50), default="disponivel")
    categoria_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=True
    )  # Link para Category

    # Relacionamentos
    depositor = db.relationship(
        "User", back_populates="deposited_books", foreign_keys=[depositor_id]
    )
    categoria = db.relationship("Category", back_populates="books")

    # Detalhes de aluguel atuais (para o estado do livro, Aluguel é histórico)
    rentee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reserved_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    rentee = db.relationship("User", foreign_keys=[rentee_id])
    reserved_by = db.relationship(
        "User", back_populates="reserved_books", foreign_keys=[reserved_by_id]
    )

    def __init__(
        self, titulo: str, autor: str, depositor_id: int, categoria: Category = None
    ):
        self.titulo = titulo
        self.autor = autor
        self.depositor_id = depositor_id
        self._estado_nome = "disponivel"  # Estado inicial
        if categoria:
            self.categoria = categoria  # Atribui o objeto Category diretamente

    @property
    def estado(self) -> EstadoLivro:
        """Retorna o objeto de estado atual com base no _estado_nome."""
        # A instância do livro é passada para o objeto de estado para que ele possa operar sobre o livro.
        if self._estado_nome == "disponivel":
            return Disponivel(self)
        elif self._estado_nome == "alugado":
            return Alugado(self)
        elif self._estado_nome == "reservado":
            return Reservado(self)
        else:
            raise ValueError(f"Estado desconhecido: {self._estado_nome}")

    def set_estado(self, new_state_object: EstadoLivro):
        """Define o novo objeto de estado do livro e atualiza o nome do estado persistente."""
        self._estado_nome = new_state_object.__class__.__name__.lower()
        db.session.add(self)

    # Métodos do livro que delegam ao objeto de estado
    def alugar(self, user, mediator):
        """Delega a operação de alugar para o objeto de estado atual."""
        self.estado.alugar(user, mediator)

    def devolver(self, user, mediator):
        """Delega a operação de devolver para o objeto de estado atual."""
        self.estado.devolver(user, mediator)

    def reservar(self, user, mediator):
        """Delega a operação de reservar para o objeto de estado atual."""
        self.estado.reservar(user, mediator)

    def cancelar_reserva(self):
        """Cancela a reserva e retorna ao estado disponível, se aplicável."""
        if self._estado_nome == "reservado":
            self.reserved_by_id = None
            self._estado_nome = "disponivel"
            db.session.add(self)
            print(f"Reserva do livro '{self.titulo}' cancelada.")

    def gerarQRCode(self) -> str:
        """Placeholder para a lógica de geração de QR Code."""
        print(f"QR Code para o livro '{self.titulo}' (ID: {self.id}) gerado.")
        return f"api://book/{self.id}"

    def alterarEstado(self, new_state_name: str):
        """
        Método público para alterar o estado interno do livro.
        Em um padrão State estrito, as transições ocorrem através dos métodos de estado.
        Este método é mais para manipulação direta ou para os objetos de estado definirem o próximo estado.
        """
        valid_states = ["disponivel", "alugado", "reservado"]
        if new_state_name.lower() in valid_states:
            self._estado_nome = new_state_name.lower()
            db.session.add(self)
            print(f"Estado do livro '{self.titulo}' alterado para: {self._estado_nome}")
        else:
            print(f"Estado inválido: {new_state_name}")

    def __repr__(self):
        return f"<Book {self.titulo} (ID: {self.id}, Estado: {self._estado_nome})>"
