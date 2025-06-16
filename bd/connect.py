import sqlite3
import csv

# Define o nome do arquivo do banco de dados
db_file = 'bd/saber.db'
csv_file = 'assets/biblioteca_dinamica.csv'
csv_horarios = 'assets/horarios.csv'

# Tenta conectar ao banco de dados. Se não existir, ele será criado.
try:
    conn = sqlite3.connect(db_file)
    print(f"Conectado ao banco de dados: {db_file}")

    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Cria uma tabela (exemplo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            matricula INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT UNIQUE,
            curso TEXT NOT NULL,
            periodo INTEGER NOT NULL CHECK (periodo > 0 AND periodo <= 10)  
        )
    ''')
    print("Tabela 'usuarios' criada (se não existia).")

    # Insere dados (exemplo)
    cursor.execute("INSERT INTO usuarios (nome, email, curso, periodo) VALUES (?, ?, ?, ?)", ('Luis Felipe Nonato', 'felipe.nonato@academico.ifpb.edu.br', 'Engenharia de Computação', 7))
    cursor.execute("INSERT INTO usuarios (nome, email, curso, periodo) VALUES (?, ?, ?, ?)", ('Maria Souza', 'maria.souza@example.com', 'Matemática', 1))
    conn.commit()
    print("Dados inseridos com sucesso em usuarios.")


    # Consulta dados (exemplo)
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


    # Cria a tabela 'biblioteca' (ajuste os tipos conforme necessário)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS biblioteca (
            ISBN TEXT PRIMARY KEY,
            Titulo TEXT,
            Autor TEXT,
            Editora TEXT,
            Ano TEXT,
            Paginas INTEGER,
            Disciplina TEXT,
            Capa TEXT,
            Qtd_Exemplares INTEGER,
            Avaliacao REAL,
            Emprestimos INTEGER
        )
    ''')
    print("Tabela 'biblioteca' criada (se não existia).")

    # Lê o CSV e insere os dados
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        livros = [
            (
                row['ISBN'],
                row['Título'],
                row['Autor'],
                row['Editora'],
                row['Ano'],
                int(row['Páginas']) if row['Páginas'].isdigit() else 0,
                row['Disciplina'],
                row['Capa'],
                int(row['Qtd_Exemplares']) if row['Qtd_Exemplares'].isdigit() else 0,
                float(row['Avaliação'].replace(',', '.')) if row['Avaliação'] else None,
                int(row['Empréstimos']) if row['Empréstimos'].isdigit() else 0
            )
            for row in reader
        ]

    cursor.executemany('''
        INSERT OR IGNORE INTO biblioteca
        (ISBN, Titulo, Autor, Editora, Ano, Paginas, Disciplina, Capa, Qtd_Exemplares, Avaliacao, Emprestimos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', livros)
    conn.commit()
    print("Dados do CSV inseridos na tabela 'biblioteca'.")


    # Cria a tabela 'horarios'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso TEXT,
            semestre TEXT,
            bloco TEXT,
            faixa_horario TEXT,
            segunda TEXT,
            terca TEXT,
            quarta TEXT,
            quinta TEXT,
            sexta TEXT
        )
    ''')
    print("Tabela 'horarios' criada (se não existia).")

    # Lê o CSV e insere os dados na tabela 'horarios'
    with open(csv_horarios, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        horarios = [
            (
                row['Course'],
                row['Semester'],
                row['Time Block'],
                row['Time Range'],
                row['Monday'],
                row['Tuesday'],
                row['Wednesday'],
                row['Thursday'],
                row['Friday']
            )
            for row in reader
        ]

    cursor.executemany('''
        INSERT INTO horarios
        (curso, semestre, bloco, faixa_horario, segunda, terca, quarta, quinta, sexta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', horarios)
    conn.commit()
    print("Dados do CSV inseridos na tabela 'horarios'.")

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Fecha a conexão
    if conn:
        conn.close()
        print("Conexão fechada.")