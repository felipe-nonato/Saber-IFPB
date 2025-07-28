from api.database import db
import datetime


class Penalty(db.Model):
    __tablename__ = "penalties"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(
        db.String(36), db.ForeignKey("books.id"), nullable=False
    )  # String para Book ID
    tipo = db.Column(db.String(50), nullable=False)  # Ex: 'Atraso', 'Dano'
    valor = db.Column(db.Float, nullable=False)
    multiplicador = db.Column(db.Float, default=1.0)
    data_ocorrencia = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship("User", backref="penalties")
    book = db.relationship("Book", backref="penalties")

    def __init__(
        self,
        user_id: int,
        book_id: str,
        tipo: str,
        valor: float,
        multiplicador: float = 1.0,
    ):
        self.user_id = user_id
        self.book_id = book_id
        self.tipo = tipo
        self.valor = valor
        self.multiplicador = multiplicador

    def calcular(self) -> float:
        """Calcula o valor total da penalidade."""
        return self.valor * self.multiplicador

    def aplicar(self, user) -> bool:
        """Aplica a penalidade ao usuário."""
        from api.patterns.singleton import (
            SistemaEconomia,
        )  # Importa aqui para evitar importação circular

        economia = SistemaEconomia.get_instance()

        # Tenta diminuir as moedas do usuário. O método diminuirMoedas já lida com saldo insuficiente.
        if user.diminuirMoedas(self.calcular()):
            # Se as moedas foram diminuídas, repassa para o sistema (ID 0 ou usuário 'system')
            system_user = db.session.query(User).filter_by(nome="system").first()
            system_user_id = (
                system_user.id if system_user else 0
            )  # Use system user's ID or a placeholder

            economia.repassarMoedas(user.id, system_user_id, self.calcular())
            db.session.add(self)  # Adiciona o registro da penalidade
            print(
                f"Penalização de {self.calcular()} aplicada ao usuário {user.nome} para o livro {self.book_id}."
            )
            return True
        else:
            print(
                f"Não foi possível aplicar a penalização completa ao usuário {user.nome}. Saldo insuficiente."
            )
            return False

    def __repr__(self):
        return f"<Penalty ID: {self.id}, User: {self.user_id}, Tipo: {self.tipo}, Valor: {self.valor}>"
