from api.database import db
from api.models.transaction import Transaction
from api.models.user import User


class SistemaEconomia:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SistemaEconomia, cls).__new__(cls)
            # Inicializa qualquer estado ou recursos aqui, se necessário.
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls.__new__(cls)

    def gerarMoedas(self, recipient_id: int, amount: int) -> bool:
        """Simula a geração de novas moedas para o sistema ou para um destinatário."""
        # Para simplicidade, assumimos que moedas são geradas "do nada" para um usuário.
        # Um sender_id=None pode representar a origem "sistema".
        transaction = Transaction(
            sender_id=None, receiver_id=recipient_id, amount=amount
        )
        db.session.add(transaction)

        recipient = User.query.get(recipient_id)
        if recipient:
            recipient.adicionarMoedas(amount)
            print(
                f"Sistema Economia: {amount} moedas geradas para o usuário ID {recipient_id}."
            )
            return True
        print(
            f"Sistema Economia: Não foi possível gerar moedas. Usuário ID {recipient_id} não encontrado."
        )
        return False

    def repassarMoedas(self, sender_id: int, receiver_id: int, amount: int) -> bool:
        """Transfere moedas entre usuários ou de/para o sistema."""
        sender_user = (
            User.query.get(sender_id)
            if sender_id != 0
            else User.query.filter_by(nome="system").first()
        )
        receiver_user = (
            User.query.get(receiver_id)
            if receiver_id != 0
            else User.query.filter_by(nome="system").first()
        )

        if not sender_user:
            print(f"Sistema Economia: Remetente ID {sender_id} não encontrado.")
            return False
        if not receiver_user:
            print(f"Sistema Economia: Destinatário ID {receiver_id} não encontrado.")
            return False

        # Garante que o remetente tenha moedas suficientes, a menos que seja o sistema
        if (
            sender_user.nome != "system"
        ):  # O usuário 'system' tem saldo ilimitado para repassar
            if not sender_user.diminuirMoedas(
                amount
            ):  # Isso também atualiza o saldo do usuário na sessão
                print(
                    f"Sistema Economia: Saldo insuficiente para o remetente {sender_user.nome} (ID: {sender_id})."
                )
                return False
        else:
            print(
                f"Sistema Economia: Sistema transferindo {amount} moedas de {sender_user.nome} para {receiver_user.nome}"
            )

        receiver_user.adicionarMoedas(
            amount
        )  # Isso também atualiza o saldo do usuário na sessão

        transaction = Transaction(
            sender_id=sender_user.id, receiver_id=receiver_user.id, amount=amount
        )
        db.session.add(transaction)
        print(
            f"Sistema Economia: {amount} moedas repassadas de {sender_user.nome} para {receiver_user.nome}."
        )
        return True
