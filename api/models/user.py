from api.database import db
import datetime  # Nota: Não usado aqui; remova se não necessário em outros lugares


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(
        db.String(50), unique=True, nullable=True
    )  # Adicionado 'matricula' – permite nulo, mas único
    email = db.Column(
        db.String(120), unique=True, nullable=False
    )  # Renomeado 'email' para 'email' – obrigatório e único
    senha = db.Column(
        db.String(255), nullable=False
    )  # Renomeado 'password' para 'senha' – obrigatório, tamanho aumentado para segurança
    nome = db.Column(
        db.String(120), unique=True, nullable=False
    )  # Renomeado 'username' para 'nome' – obrigatório e único
    saldoMoedas = db.Column(
        db.Integer, default=0, nullable=False
    )  # Renomeado 'coins' para 'saldoMoedas' – default 0, não nulo

    # Relationship para 'historico: List<Aluguel>'
    historico = db.relationship(
        "Rental", back_populates="user_rentee", foreign_keys="Rental.rentee_id"
    )
    deposited_books = db.relationship(
        "Book", back_populates="depositor", foreign_keys="Book.depositor_id"
    )
    reserved_books = db.relationship(
        "Book", back_populates="reserved_by", foreign_keys="Book.reserved_by_id"
    )

    # Campo auxiliar para o UsuarioObserver (não persistente no DB)
    _usuario_observer = None

    def __init__(self, nome, email, senha, matricula=None, saldoMoedas=0):
        """
        Construtor da classe User.

        :param nome: Nome do usuário (obrigatório, único).
        :param email: Email do usuário (obrigatório, único).
        :param senha: Senha do usuário (obrigatório).
        :param matricula: Matrícula do usuário (opcional, única se informada).
        :param saldoMoedas: Saldo inicial de moedas (opcional, default 0).
        """
        self.nome = nome
        self.email = email
        self.senha = senha
        self.matricula = matricula
        self.saldoMoedas = saldoMoedas  # Agora aceita valor personalizado no init

        # Importa aqui para evitar importação circular
        from api.patterns.observer import UsuarioObserver

        self._usuario_observer = UsuarioObserver(self)

    def adicionarMoedas(self, amount: int):
        """
        Adiciona moedas ao saldo do usuário e notifica o observer.

        :param amount: Quantidade de moedas a adicionar (deve ser > 0).
        """
        if amount > 0:
            self.saldoMoedas += amount
            db.session.add(self)
            print(
                f"Usuário {self.nome} adicionou {amount} moedas. Saldo atual: {self.saldoMoedas}"
            )
            # Notifica o observador específico do usuário
            if self._usuario_observer:
                self._usuario_observer.notificar(
                    f"Seu saldo de moedas foi aumentado em {amount}. Saldo total: {self.saldoMoedas}."
                )

    def diminuirMoedas(self, amount: int) -> bool:
        """
        Diminui moedas do saldo do usuário se houver saldo suficiente e notifica o observer.

        :param amount: Quantidade de moedas a diminuir (deve ser > 0).
        :return: True se bem-sucedido, False se saldo insuficiente.
        """
        if amount > 0 and self.saldoMoedas >= amount:
            self.saldoMoedas -= amount
            db.session.add(self)
            print(
                f"Usuário {self.nome} diminuiu {amount} moedas. Saldo atual: {self.saldoMoedas}"
            )
            # Notifica o observador específico do usuário
            if self._usuario_observer:
                self._usuario_observer.notificar(
                    f"Seu saldo de moedas foi diminuído em {amount}. Saldo total: {self.saldoMoedas}."
                )
            return True
        print(
            f"Usuário {self.nome} não pode diminuir {amount} moedas. Saldo insuficiente: {self.saldoMoedas}"
        )
        # Notifica o observador específico do usuário
        if self._usuario_observer:
            self._usuario_observer.notificar(
                f"Falha ao diminuir {amount} moedas. Saldo insuficiente: {self.saldoMoedas}."
            )
        return False

    def __repr__(self):
        return f"<User {self.nome} (ID: {self.id})>"
