import os


class Configuration:
    # Singleton pattern para garantir uma única instância
    _instance = None

    @classmethod
    def get_instance(cls):
        """Retorna a instância única da configuração."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            # Inicializa as configurações aqui
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Carrega as configurações de ambiente ou valores padrão."""
        # Configurações do Banco de Dados (exemplo, ajuste conforme necessário)
        PATH = os.path.dirname(os.path.abspath(__file__))

        self.SQLALCHEMY_DATABASE_URI = os.environ.get(
            "DATABASE_URL", "sqlite:///{}/../bd/saber.db".format(PATH)
        )
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SECRET_KEY = os.environ.get("SECRET_KEY", "uma_chave_secreta_padrao")

        # Configurações de Negócio para o Sistema de Moedas (NOVO: Adicionadas aqui!)
        self.DEPOSIT_COINS = int(
            os.environ.get("DEPOSIT_COINS", 10)
        )  # 10 moedas por depósito, padrão
        self.RENT_COINS_PER_DAY = int(
            os.environ.get("RENT_COINS_PER_DAY", 1)
        )  # Valor por dia de aluguel
        self.FINE_PER_DAY_COINS = int(
            os.environ.get("FINE_PER_DAY_COINS", 2)
        )  # Multa por dia de atraso
        self.MAX_COINS_BALANCE = int(
            os.environ.get("MAX_COINS_BALANCE", 1000)
        )  # Limite máximo de saldo
        self.RENTAL_PERIOD_DAYS = int(
            os.environ.get("RENTAL_PERIOD_DAYS", 7)
        )  # Período de aluguel em dias (padrão 7 dias)

        # Outras configurações (expanda conforme necessário)
        self.APP_NAME = "SaberIFPB"
        self.DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"

        print("Configurações carregadas com sucesso!")  # Log para depuração

    def reload(self):
        """Recarrega as configurações, útil para ambientes dinâmicos."""
        self._load_config()


# Exemplo de uso (para testes)
if __name__ == "__main__":
    config = Configuration()
    print(f"DEPOSIT_COINS: {config.DEPOSIT_COINS}")
