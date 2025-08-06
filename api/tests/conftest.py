import pytest
from api.app import create_app
from api.config_test import TestingConfig
from api.database import db as _db
from api.models.user import User

@pytest.fixture(scope="session")
def app():
    return create_app(TestingConfig)

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function", autouse=True)
def db(app):
    with app.app_context():
        _db.create_all()
        # Cria o usuário do sistema para a economia interna
        system = User(
            nome="system",
            email="system@saber.ifpb",
            senha="system",
            matricula="SYS001",
            saldoMoedas=10**9
        )
        _db.session.add(system)
        _db.session.commit()
        yield _db
        _db.session.remove()
        _db.drop_all()
