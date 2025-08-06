from api.config import Configuration

class TestingConfig(Configuration):
    """
    Configuração de testes: ativa TESTING e usa SQLite em memória,
    define preços de depósito/aluguel e chave secreta fixa.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    # Para JWT
    SECRET_KEY = "test-secret"

    # Para o pricing strategy
    DEPOSIT_COINS = 10              # quantas moedas concede ao depositar um livro
    PENALTY_COINS_PER_DAY = 1       # penalidade por dia de atraso
    RENTAL_PERIOD_DAYS = 7          # duração padrão do aluguel
