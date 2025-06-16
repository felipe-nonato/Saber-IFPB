import random
import sqlite3
import csv
import faker
import unidecode

fake = faker.Faker('pt_BR')

# Define o nome do arquivo do banco de dados
db_file = 'bd/saber.db'
csv_file = 'assets/books.csv'
csv_horarios = 'assets/horarios.csv'

# Tenta conectar ao banco de dados. Se não existir, ele será criado.
try:
    conn = sqlite3.connect(db_file)
    print(f"Conectado ao banco de dados: {db_file}")

    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Cria uma tabela (exemplo) com campo de senha
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    print("Tabela 'usuarios' criada (se não existia).")


    dominios = ['@exemplo.com', '@ifpb.edu.br', '@gmail.com']
    for i in range(100):
        nome = fake.name()
        # Gera o e-mail a partir do nome
        nome_email = unidecode.unidecode(nome.lower().replace(' ', '.'))
        email = f"{nome_email.split('.')[0]}.{nome_email.split('.')[-1]}{fake.random_int(1,999)}{fake.random_element(dominios)}"
        senha = fake.password(length=10)
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
    conn.commit()

    print("Dados inseridos com sucesso em usuarios.")


    # Consulta dados (exemplo)
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


    # Cria a tabela Biblioteca com os campos do books.csv
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Biblioteca (
            isbn13 TEXT PRIMARY KEY,
            isbn10 TEXT,
            title TEXT,
            subtitle TEXT,
            authors TEXT,
            categories TEXT,
            thumbnail TEXT,
            description TEXT,
            published_year INTEGER,
            average_rating REAL,
            num_pages INTEGER,
            ratings_count INTEGER
        )
    ''')
    print("Tabela 'Biblioteca' criada (se não existia).")

    # Importa os dados do books.csv para a tabela Biblioteca
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT OR IGNORE INTO Biblioteca (
                    isbn13, isbn10, title, subtitle, authors, categories, thumbnail, description,
                    published_year, average_rating, num_pages, ratings_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['isbn13'],
                row['isbn10'],
                row['title'],
                row['subtitle'],
                row['authors'],
                row['categories'],
                row['thumbnail'],
                row['description'],
                int(row['published_year']) if row['published_year'] else None,
                float(row['average_rating']) if row['average_rating'] else None,
                int(row['num_pages']) if row['num_pages'] else None,
                int(row['ratings_count']) if row['ratings_count'] else None
            ))
    conn.commit()
    print("Dados importados do books.csv para a tabela 'Biblioteca'.")


    # Cria a tabela NotasLivros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NotasLivros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            isbn13 TEXT,
            nota INTEGER,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(isbn13) REFERENCES Biblioteca(isbn13)
        )
    ''')
    print("Tabela 'NotasLivros' criada (se não existia).")

    # Busca todos os ids de usuários e isbn13 de livros
    cursor.execute("SELECT id FROM usuarios")
    usuarios_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT isbn13 FROM Biblioteca")
    livros_isbn13 = [row[0] for row in cursor.fetchall()]


    # Garante que a maioria dos usuários tenha pelo menos 5 avaliações de livros aleatórios
    avaliacoes_por_usuario = {}
    total_usuarios = len(usuarios_ids)
    usuarios_com_5_ou_mais = int(total_usuarios * 0.9)  # 90% dos usuários terão pelo menos 5 avaliações

    # Seleciona aleatoriamente os usuários que terão pelo menos 5 avaliações
    usuarios_escolhidos = random.sample(usuarios_ids, usuarios_com_5_ou_mais)

    # Aumenta o número mínimo de avaliações para 8
    for usuario_id in usuarios_escolhidos:
        livros_avaliados = set()
        for _ in range(8):  # Aumentado de 5 para 8 avaliações mínimas
            isbn13 = random.choice(livros_isbn13)
            while isbn13 in livros_avaliados:
                isbn13 = random.choice(livros_isbn13)
            livros_avaliados.add(isbn13)
            nota = fake.random_int(min=1, max=5)
            cursor.execute('''
                INSERT INTO NotasLivros (usuario_id, isbn13, nota)
                VALUES (?, ?, ?)
            ''', (usuario_id, isbn13, nota))
        avaliacoes_por_usuario[usuario_id] = 8

    # Para o restante dos usuários, insere entre 2 e 5 avaliações
    for usuario_id in usuarios_ids:
        if usuario_id not in avaliacoes_por_usuario:
            num_avaliacoes = random.randint(2, 5)  # Aumentado o mínimo de 1 para 2
            livros_avaliados = set()
            for _ in range(num_avaliacoes):
                isbn13 = random.choice(livros_isbn13)
                while isbn13 in livros_avaliados:
                    isbn13 = random.choice(livros_isbn13)
                livros_avaliados.add(isbn13)
                nota = fake.random_int(min=1, max=5)
                cursor.execute('''
                    INSERT INTO NotasLivros (usuario_id, isbn13, nota)
                    VALUES (?, ?, ?)
                ''', (usuario_id, isbn13, nota))

    # Aumenta significativamente o número de avaliações extras
    avaliacoes_extras = total_usuarios * 20  # Aumentado de 10 para 20 avaliações extras por usuário em média
    for _ in range(avaliacoes_extras):
        usuario_id = random.choice(usuarios_ids)
        isbn13 = random.choice(livros_isbn13)
        nota = fake.random_int(min=1, max=5)
        cursor.execute('''
            INSERT INTO NotasLivros (usuario_id, isbn13, nota)
            VALUES (?, ?, ?)
        ''', (usuario_id, isbn13, nota))

    conn.commit()
    print("Notas aleatórias inseridas na tabela 'NotasLivros'.")


except Exception as e:
    print(f"Erro: {e}")

finally:
    # Fecha a conexão
    if conn:
        conn.close()
        print("Conexão fechada.")