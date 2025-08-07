from api.database import db
import datetime


class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(36), db.ForeignKey("books.id"), nullable=False)
    rentee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    dataAluguel = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dataDevolucao = db.Column(db.DateTime, nullable=True)  # Data prevista
    dataDevolucaoEfetiva = db.Column(
        db.DateTime, nullable=True
    )  # Data real da devolução
    preco = db.Column(db.Float, nullable=False)

    # Relacionamentos
    book = db.relationship("Book", foreign_keys=[book_id])
    user_rentee = db.relationship(
        "User", back_populates="historico", foreign_keys=[rentee_id]
    )

    def __init__(
        self,
        book_id: str,
        rentee_id: int,
        preco: float,
        data_aluguel: datetime.datetime = None,
        data_devolucao: datetime.datetime = None,
        data_devolucao_efetiva: datetime.datetime = None,
    ):
        self.book_id = book_id
        self.rentee_id = rentee_id
        self.preco = preco
        self.dataAluguel = data_aluguel if data_aluguel else datetime.datetime.utcnow()
        self.dataDevolucao = data_devolucao
        self.dataDevolucaoEfetiva = data_devolucao_efetiva

    def __repr__(self):
        return (
            f"<Rental ID: {self.id}, Book: {self.book_id}, Rented by: {self.rentee_id}>"
        )
