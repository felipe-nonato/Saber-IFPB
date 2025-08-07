from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Configurações
from .config import Configuration

# Para testes, basta importar aqui sua TestingConfig:
# from .config_test import TestingConfig

# Banco de dados
from .database import db

# Models (necessários para db.create_all)
from .models.user import User
from .models.book import Book
from .models.rental import Rental
from .models.category import Category
from .models.penalty import Penalty
from .models.transaction import Transaction

# Padrões (patterns)
from .patterns.builder import LivroBuilder
from .patterns.factory import (
    NotificationFactory,
    EmailFactory,
    SMSFactory,
    EmailNotification,
    SMSNotification,
)
from .patterns.mediator import BibliotecaMediator
from .patterns.observer import (
    Subject,
    UsuarioObserver,
    CoinReceivedObserver,
    RentalDueObserver,
)
from .patterns.pricing_strategy import PrecificacaoStrategy, PorRecorrencia, PorTempo
from .patterns.singleton import SistemaEconomia
from .patterns.state import EstadoLivro, Disponivel, Alugado, Reservado

# Facade
from .services.saber_facade import SaberFacade

# Blueprints / rotas
from .routes.user_routes import user_bp
from .routes.book_routes import book_bp


def create_app(config_class=None):
    """
    Factory de aplicação.
    Se receber config_class, usa-a (ex: TestingConfig para pytest);
    caso contrário, carrega o singleton Configuration.
    """
    app = Flask(__name__)

    # --- Configurações ---
    if config_class:
        app.config.from_object(config_class)
    else:
        cfg = Configuration.get_instance()
        app.config.from_object(cfg)

    # --- Extensões ---
    db.init_app(app)

    # --- CORS ---
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    # --- Setup de padrões, singleton e observers ---
    # Escolhe a instância de config para usar na estratégia de precificação
    if config_class:
        cfg_instance = config_class()
    else:
        cfg_instance = Configuration.get_instance()

    sistema_economia = SistemaEconomia.get_instance()

    notification_subject = Subject()
    email_factory = EmailFactory()
    sms_factory = SMSFactory()
    notification_subject.attach(CoinReceivedObserver(email_factory))
    notification_subject.attach(RentalDueObserver(email_factory))

    default_pricing_strategy: PrecificacaoStrategy = PorTempo(cfg_instance)

    mediator = BibliotecaMediator(
        db, default_pricing_strategy, sistema_economia, notification_subject
    )
    facade = SaberFacade(db, mediator, LivroBuilder())

    # Anexa recursos úteis na app
    app.facade = facade
    app.db = db
    app.sistema_economia = sistema_economia

    # --- Registro de blueprints ---
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(book_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return "Bem-vindo à Saber API!"

    return app


# Quando executado diretamente, cria tabelas e inicia o servidor em dev
if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()  # Create tables based on models
        # Optional: Add initial data or system user for economy
        if not User.query.filter_by(nome="system").first():
            system_user = User(
                matricula="SYS001",
                nome="system",
                email="system@saber.ifpb",
                senha="system",  # Ou gere uma senha forte se preferir
                saldoMoedas=999999999,
            )
            db.session.add(system_user)
            db.session.commit()
            print("Usuário do sistema criado para transações de economia.")

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

    print("Aplicação Flask está rodando. Acesse em http://127.0.0.1:5000/")

    # Optional: For Colab/external access via ngrok
    # try:
    #     from pyngrok import ngrok
    #     ngrok.kill() # Terminate any previous ngrok tunnels
    #     public_url = ngrok.connect(5000)
    #     print(f"Ngrok Tunnel URL: {public_url}")
    # except ImportError:
    #     print("Ngrok não está instalado. Instale com `!pip install pyngrok` para acesso externo.")
    # except Exception as e:
    #     print(f"Erro ao configurar ngrok: {e}")
