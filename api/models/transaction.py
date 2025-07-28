from api.database import db
import datetime


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )  # Null para sistema (origem/destino)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )  # Null para sistema (origem/destino)
    amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relacionamentos, podem ser nulos para transações do sistema
    sender = db.relationship(
        "User", foreign_keys=[sender_id], backref="sent_transactions"
    )
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], backref="received_transactions"
    )

    def __init__(self, sender_id: int, receiver_id: int, amount: int):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return f"<Transaction ID: {self.id}, From: {self.sender_id}, To: {self.receiver_id}, Amount: {self.amount}>"
