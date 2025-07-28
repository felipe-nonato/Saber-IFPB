from api.database import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(200), nullable=True)

    # Relacionamento para livros
    books = db.relationship("Book", back_populates="categoria")

    def __init__(self, nome: str, descricao: str = None):
        self.nome = nome
        self.descricao = descricao

    def getNome(self) -> str:
        return self.nome

    def __repr__(self):
        return f"<Category {self.nome}>"
