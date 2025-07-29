from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import threading
import os

# Import configurations
from .config import Configuration

# Import database setup
from .database import db

# Import models (required for db.create_all() to find them)
from .models.user import User
from .models.book import Book
from .models.rental import Rental
from .models.category import Category
from .models.penalty import Penalty
from .models.transaction import Transaction

# Import patterns
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

# Import services
from .services.saber_facade import SaberFacade


def create_app():
    app = Flask(__name__)
    # Instancie o Singleton corretamente
    config = Configuration.get_instance()  # Ou: config = Configuration()

    # Carregue as configurações do objeto instanciado
    app.config.from_object(config)

    # Depuração: Verifique se as configs foram carregadas
    print("Configurações carregadas:")
    print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")

    db.init_app(app)

    # Initialize global instances of singletons and factories
    config = (
        Configuration()
    )  # Configuration is already a singleton via its class definition
    sistema_economia = SistemaEconomia.get_instance()  # Singleton for economy

    # Notification Setup
    notification_subject = Subject()
    email_factory = EmailFactory()
    sms_factory = SMSFactory()

    # Instantiate and attach observers
    notification_subject.attach(
        CoinReceivedObserver(email_factory)
    )  # Pass email_factory
    notification_subject.attach(RentalDueObserver(email_factory))  # Pass email_factory

    # Pricing Strategies
    # For this example, we'll use PorTempo as the default pricing strategy for the system.
    # In a real application, the choice of strategy might be dynamic.
    default_pricing_strategy: PrecificacaoStrategy = PorTempo(config)

    # Mediator and Facade
    mediator = BibliotecaMediator(
        db, default_pricing_strategy, sistema_economia, notification_subject
    )
    facade = SaberFacade(db, mediator, LivroBuilder())  # Pass LivroBuilder to Facade

    # Attach instances to app for access in blueprints (e.g., current_app.facade)
    app.facade = facade
    app.db = db
    app.sistema_economia = sistema_economia

    # Register blueprints (API routes)
    from .routes.user_routes import user_bp
    from .routes.book_routes import book_bp

    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(book_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return "Bem-vindo à Saber API!"

    return app


# --- Run Flask App ---
# This block ensures the app runs when `python -m saber.app` is executed
if __name__ == "__main__":
    app = create_app()

    def run_flask():
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

    # Run the Flask app in a separate thread to not block the Colab notebook
    thread = threading.Thread(target=run_flask)
    thread.start()

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
