import requests
import json
import time

# URL base da sua API Flask
BASE_URL = "http://127.0.0.1:5000/api"


def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, params=data, headers=headers)
        else:
            raise ValueError(f"Método HTTP {method} não suportado para este helper.")

        response.raise_for_status()  # Levanta um erro para respostas 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição {method} {url}: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            try:
                print(f"Response Body: {e.response.json()}")
            except json.JSONDecodeError:
                print(f"Response Body (raw): {e.response.text}")
        return None


def test_api():
    print("Iniciando testes da API SaberIFPB...\n")
    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    def test_assert(cond, msg):
        nonlocal total_tests, passed_tests, failed_tests
        total_tests += 1
        if cond:
            print(f"✔️  {msg}")
            passed_tests += 1
        else:
            print(f"❌ {msg}")
            failed_tests += 1

    # --- 1. Teste de Criação de Usuário ---
    print("--- Teste de Criação de Usuários ---")
    user_alice_data = {"nome": "Alice", "matricula": "A001"}
    user_bob_data = {"nome": "Bob", "matricula": "B002"}

    alice_response = make_request("POST", "users", user_alice_data)
    test_assert(alice_response is not None, "Usuário Alice criado")
    if not alice_response:
        print("Falha ao criar Alice. Encerrando testes.")
        print(
            f"\nTestes concluídos: {passed_tests}/{total_tests} passaram, {failed_tests} falharam."
        )
        return
    alice_id = alice_response["user"]["id"]

    bob_response = make_request("POST", "users", user_bob_data)
    test_assert(bob_response is not None, "Usuário Bob criado")
    if not bob_response:
        print("Falha ao criar Bob. Encerrando testes.")
        print(
            f"\nTestes concluídos: {passed_tests}/{total_tests} passaram, {failed_tests} falharam."
        )
        return
    bob_id = bob_response["user"]["id"]

    # --- 2. Teste de Obtenção de Usuário ---
    print("\n--- Teste de Obtenção de Usuário ---")
    get_alice = make_request("GET", f"users/{alice_id}")
    test_assert(get_alice is not None, "Dados de Alice obtidos")
    test_assert(
        get_alice and get_alice["nome"] == "Alice" and get_alice["saldoMoedas"] == 0,
        "Dados de Alice corretos",
    )

    # --- 3. Teste de Depósito de Livro ---
    print("\n--- Teste de Depósito de Livro ---")
    book1_data = {
        "titulo": "Aventura do Código",
        "autor": "Programador Mestre",
        "depositor_id": alice_id,
        "categoria": "Tecnologia",
    }
    book1_response = make_request("POST", "books", book1_data)
    test_assert(book1_response is not None, "Livro 1 depositado")
    if not book1_response:
        print("Falha ao depositar Livro 1.")
        print(
            f"\nTestes concluídos: {passed_tests}/{total_tests} passaram, {failed_tests} falharam."
        )
        return
    book1_id = book1_response["book"]["id"]
    alice_after_deposit = make_request("GET", f"users/{alice_id}")
    test_assert(
        alice_after_deposit["saldoMoedas"] > 0, "Alice recebeu moedas pelo depósito"
    )

    book2_data = {
        "titulo": "Mistérios da Biblioteca",
        "autor": "Autor Anônimo",
        "depositor_id": alice_id,
        "categoria": "Ficção",
    }
    book2_response = make_request("POST", "books", book2_data)
    test_assert(book2_response is not None, "Livro 2 depositado")
    if not book2_response:
        print("Falha ao depositar Livro 2.")
        print(
            f"\nTestes concluídos: {passed_tests}/{total_tests} passaram, {failed_tests} falharam."
        )
        return
    book2_id = book2_response["book"]["id"]

    # --- 4. Teste de Listagem de Livros ---
    print("\n--- Teste de Listagem de Livros ---")
    list_all_books = make_request("GET", "books")
    test_assert(list_all_books is not None, "Livros listados")
    test_assert(
        list_all_books and len(list_all_books) >= 2, "Pelo menos 2 livros depositados"
    )

    list_available_books = make_request("GET", "books", {"estado": "disponivel"})
    test_assert(list_available_books is not None, "Livros disponíveis listados")
    test_assert(
        list_available_books and len(list_available_books) >= 2,
        "Pelo menos 2 livros disponíveis",
    )

    # --- 5. Teste de Aluguel de Livro ---
    print("\n--- Teste de Aluguel de Livro ---")
    # Bob deposita dois livros para garantir saldo suficiente para alugar dois livros
    deposit_for_bob_data1 = {
        "titulo": "Livro do Bob 1",
        "autor": "Bob Autor",
        "depositor_id": bob_id,
        "categoria": "Autoajuda",
    }
    deposit_for_bob_response1 = make_request("POST", "books", deposit_for_bob_data1)
    test_assert(
        deposit_for_bob_response1 is not None,
        "Bob depositou Livro 1 para ganhar moedas",
    )

    deposit_for_bob_data2 = {
        "titulo": "Livro do Bob 2",
        "autor": "Bob Autor",
        "depositor_id": bob_id,
        "categoria": "Autoajuda",
    }
    deposit_for_bob_response2 = make_request("POST", "books", deposit_for_bob_data2)
    test_assert(
        deposit_for_bob_response2 is not None,
        "Bob depositou Livro 2 para ganhar moedas",
    )

    bob_initial_coins = make_request("GET", f"users/{bob_id}")["saldoMoedas"]
    test_assert(bob_initial_coins > 0, "Bob tem moedas suficientes para alugar")

    # Bob aluga o Livro 1
    rent_book1_data = {"user_id": bob_id}
    rent_book1_response = make_request(
        "POST", f"books/{book1_id}/rent", rent_book1_data
    )
    test_assert(rent_book1_response is not None, "Bob alugou Livro 1")
    if rent_book1_response:
        test_assert(
            rent_book1_response["book"]["estado"] == "alugado", "Livro 1 está alugado"
        )
        bob_after_rent = make_request("GET", f"users/{bob_id}")
        test_assert(
            bob_after_rent["saldoMoedas"] < bob_initial_coins, "Saldo de Bob diminuiu"
        )
        alice_after_rent = make_request("GET", f"users/{alice_id}")
        test_assert(
            alice_after_rent["saldoMoedas"] > alice_after_deposit["saldoMoedas"],
            "Alice recebeu moedas do aluguel",
        )

    # --- 6. Teste de Reserva de Livro ---
    print("\n--- Teste de Reserva de Livro ---")
    reserve_book2_data = {"user_id": alice_id}  # Alice reserva o livro
    reserve_book2_response = make_request(
        "POST", f"books/{book2_id}/reserve", reserve_book2_data
    )
    test_assert(reserve_book2_response is not None, "Alice reservou Livro 2")
    if reserve_book2_response:
        test_assert(
            reserve_book2_response["book"]["estado"] == "reservado",
            "Livro 2 está reservado",
        )

    print("\n--- Teste: Tentar alugar livro reservado por outro usuário ---")
    try_rent_reserved_by_other_data = {"user_id": bob_id}
    try_rent_reserved_by_other_response = make_request(
        "POST", f"books/{book2_id}/rent", try_rent_reserved_by_other_data
    )
    test_assert(
        try_rent_reserved_by_other_response is None,
        "Bob não conseguiu alugar livro reservado por Alice",
    )

    # --- 8. Teste de Aluguel de Livro Reservado pelo Usuário Correto (Alice) ---
    print(
        "\n--- Teste de Aluguel de Livro Reservado (pelo usuário correto - Alice) ---"
    )
    alice_initial_coins_for_reserved = make_request("GET", f"users/{alice_id}")[
        "saldoMoedas"
    ]
    rent_reserved_book2_data = {"user_id": alice_id}
    rent_reserved_book2_response = make_request(
        "POST", f"books/{book2_id}/rent", rent_reserved_book2_data
    )
    test_assert(
        rent_reserved_book2_response is not None, "Alice alugou Livro 2 (reservado)"
    )
    if rent_reserved_book2_response:
        test_assert(
            rent_reserved_book2_response["book"]["estado"] == "alugado",
            "Livro 2 está alugado",
        )
        test_assert(
            rent_reserved_book2_response["book"]["rentee_id"] == alice_id,
            "Alice é a locatária do Livro 2",
        )
        alice_after_rent_reserved = make_request("GET", f"users/{alice_id}")
        test_assert(
            alice_after_rent_reserved["saldoMoedas"] < alice_initial_coins_for_reserved,
            "Saldo de Alice diminuiu após aluguel de livro reservado",
        )

    # --- 9. Teste de Devolução do Livro Reservado Alugado (Alice) ---
    print("\n--- Teste de Devolução do Livro Reservado Alugado (Alice) ---")
    if (
        rent_reserved_book2_response
        and rent_reserved_book2_response["book"]["estado"] == "alugado"
    ):
        return_book2_data = {"user_id": alice_id}
        return_book2_response = make_request(
            "POST", f"books/{book2_id}/return", return_book2_data
        )
        test_assert(return_book2_response is not None, "Alice devolveu Livro 2")
        if return_book2_response:
            test_assert(
                return_book2_response["book"]["estado"] == "disponivel",
                "Livro 2 está disponível após devolução",
            )
    else:
        print("Alice não alugou Livro 2, não é possível testar devolução.")

    print(
        f"\nTestes concluídos: {passed_tests}/{total_tests} passaram, {failed_tests} falharam."
    )


if __name__ == "__main__":
    # Pequena pausa para garantir que o servidor Flask esteja totalmente inicializado
    print("Aguardando 5 segundos para o servidor Flask iniciar...")
    time.sleep(5)
    test_api()
