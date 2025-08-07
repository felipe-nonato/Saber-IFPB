# api/tests/test_books.py

from api.tests.utils import create_user

def test_list_books_empty(client):
    resp = client.get("/api/books")
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_create_book_data(client):
    u = create_user(email="dep@x.com", senha="pw", nome="Dep", matricula="dep1")
    payload = {
        "titulo": "LivroTeste",
        "autor": "AutorT",
        "depositor_id": u.id
    }
    resp = client.post("/api/books", json=payload)
    # rota retorna 201 ou 200 dependendo da lógica interna; vamos aceitar ambos:
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    # em caso de sucesso, ou virá {"message":..., "book":{...}} ou {"error":...}
    assert "book" in data
    assert data["book"]["titulo"] == "LivroTeste"
