# api/tests/test_auth.py

from api.tests.utils import create_user

def test_register_success(client):
    resp = client.post("/api/users", json={
        "nome": "NovoUser",
        "email": "novo@teste.com",
        "senha": "Senha123",
        "matricula": "novo1"
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["message"] == "Usuário cadastrado com sucesso."
    assert data["user"]["nome"] == "NovoUser"
    assert data["user"]["matricula"] == "novo1"

def test_register_duplicate(client):
    create_user(nome="Dup", email="dup@x.com", senha="pw", matricula="dup1")
    resp = client.post("/api/users", json={
        "nome": "Dup",
        "email": "dup@x.com",
        "senha": "pw",
        "matricula": "dup1"
    })
    assert resp.status_code == 400
    assert "já existe" in resp.get_json()["error"]

def test_login_success(client):
    # primeiro registra via helper
    create_user(nome="A", email="a@b.com", senha="abc", matricula="a1")
    resp = client.post("/api/login", json={
        "email": "a@b.com",
        "senha": "abc"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert "token" in data and isinstance(data["token"], str)

def test_login_fail(client):
    resp = client.post("/api/login", json={
        "email": "nao@existe.com",
        "senha": "errada"
    })
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Credenciais inválidas"
