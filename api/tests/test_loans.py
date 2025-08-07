from api.tests.utils import create_user, create_book


def test_create_loan_success(client):
    u = create_user(nome="U1", email="u1@x.com", senha="pw", matricula="u1")
    b = create_book(titulo="B1", autor="A1", depositor_id=u.id)
    resp = client.post(f"/api/books/{b.id}/rent", json={"user_id": u.id})
    assert resp.status_code == 200
    data = resp.get_json()
    # Antes você fazia data["rental"], agora use data["book"]:
    assert data["book"]["rentee_id"] == u.id
    assert data["book"]["id"] == b.id


def test_create_loan_book_unavailable(client):
    u1 = create_user(nome="U2", email="u2@x.com", senha="pw", matricula="u2")
    u2 = create_user(nome="U3", email="u3@x.com", senha="pw", matricula="u3")
    b = create_book(titulo="B2", autor="A2", depositor_id=u1.id)
    # primeiro aluguel
    client.post(f"/api/books/{b.id}/rent", json={"user_id": u1.id})
    # segundo deve falhar
    resp = client.post(f"/api/books/{b.id}/rent", json={"user_id": u2.id})
    assert resp.status_code == 400
    err = resp.get_json()["error"].lower()
    # aceita também mensagem de "já está alugado"
    assert (
        "indisponível" in err
        or "saldo insuficiente" in err
        or "já está alugado" in err
    )


def test_return_loan(client):
    u = create_user(nome="U4", email="u4@x.com", senha="pw", matricula="u4")
    b = create_book(titulo="B3", autor="A3", depositor_id=u.id)
    # aluga
    client.post(f"/api/books/{b.id}/rent", json={"user_id": u.id})
    # devolve
    resp = client.post(f"/api/books/{b.id}/return", json={"user_id": u.id})
    assert resp.status_code == 200
    data = resp.get_json()
    # apenas verifique presença do objeto "book" ou mensagem de sucesso
    assert "book" in data
    assert data["book"]["id"] == b.id
