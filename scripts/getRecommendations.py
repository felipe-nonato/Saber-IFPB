import sqlite3
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

conn = sqlite3.connect("../bd/saber.db")
usuarios = pd.read_sql("SELECT * FROM usuarios", conn)
livros = pd.read_sql("SELECT * FROM Biblioteca", conn)
notas = pd.read_sql("SELECT * FROM NotasLivros", conn)


def get_positive_ratings(notas, livros):
    notas_pos = notas[notas["nota"] >= 4].merge(
        livros[["isbn13", "categories", "authors", "title"]], on="isbn13"
    )
    notas_pos["categories"] = notas_pos["categories"].str.split(";")
    notas_pos["authors"] = notas_pos["authors"].str.split(";")
    return notas_pos


def get_user_cat_aut_matrix(notas_pos):
    notas_cat = notas_pos.explode("categories")
    notas_aut = notas_pos.explode("authors")
    user_cat_matrix = pd.crosstab(notas_cat["usuario_id"], notas_cat["categories"])
    user_cat_matrix = (user_cat_matrix > 0).astype(float)
    user_aut_matrix = pd.crosstab(notas_aut["usuario_id"], notas_aut["authors"])
    user_aut_matrix = (user_aut_matrix > 0).astype(float)
    return notas_cat, notas_aut, user_cat_matrix, user_aut_matrix


def tfidf_recommendation(usuario_id, top_n=5):
    # Livros avaliados positivamente pelo usuário (nota >= 4)
    notas_user = notas[(notas["usuario_id"] == usuario_id) & (notas["nota"] >= 4)]
    livros_user = livros[livros["isbn13"].isin(notas_user["isbn13"])]

    # Livros ainda não avaliados pelo usuário
    livros_nao_lidos = livros[~livros["isbn13"].isin(notas_user["isbn13"])].copy()

    # Junta as descrições dos livros do usuário
    descricoes_user = livros_user["description"].dropna().tolist()
    descricoes_all = livros_nao_lidos["description"].fillna("").tolist()
    if descricoes_user:
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(descricoes_user + descricoes_all)
        user_vec = np.asarray(tfidf_matrix[: len(descricoes_user)].mean(axis=0))
        outros_vecs = tfidf_matrix[len(descricoes_user) :]
        tfidf_scores = cosine_similarity(user_vec, outros_vecs).flatten()
        livros_nao_lidos["tfidf"] = tfidf_scores
    else:
        return pd.DataFrame()

    recomendados = livros_nao_lidos.sort_values("tfidf", ascending=False).head(top_n)
    return recomendados


def jaccard_recommendation(usuario_id, top_n=5):
    # Cria uma matriz binária de usuário x livro (1 se o usuário avaliou o livro, 0 caso contrário)
    user_book = notas.pivot_table(
        index="usuario_id",
        columns="isbn13",
        values="nota",
        aggfunc="count",
        fill_value=0,
    )
    # Calcula a distância de Jaccard entre todos os usuários
    jaccard_dist = pdist(user_book.values, metric="jaccard")
    jaccard_sim = 1 - squareform(jaccard_dist)
    # Encontra o índice do usuário na matriz
    user_idx = user_book.index.get_loc(usuario_id)
    # Similaridade do usuário alvo com todos os outros
    sim_scores = jaccard_sim[user_idx]
    # Seleciona os usuários mais similares (excluindo ele mesmo)
    similar_users = user_book.index[(sim_scores > 0) & (user_book.index != usuario_id)]
    # Livros que o usuário ainda não leu
    livros_lidos = set(notas[notas["usuario_id"] == usuario_id]["isbn13"])
    candidatos = notas[
        notas["usuario_id"].isin(similar_users) & (~notas["isbn13"].isin(livros_lidos))
    ]

    # Recomenda os livros mais populares entre os similares
    recomendados = candidatos["isbn13"].value_counts().head(top_n).index
    recs = livros[livros["isbn13"].isin(recomendados)][
        ["isbn13", "title", "authors", "categories", "thumbnail"]
    ]
    recs["match_type"] = "jaccard"
    return recs


def recomendar_livros(usuario_id, top_n=10):
    # Jaccard recommendations
    jaccard_df = jaccard_recommendation(usuario_id, top_n=top_n)
    # TF-IDF recommendations
    tfidf_df = tfidf_recommendation(usuario_id, top_n=top_n)

    # Se o jaccard_df estiver vazio (usuário sem avaliações suficientes), retorna apenas TF-IDF
    if jaccard_df.empty:
        recomendados = tfidf_df.sort_values("tfidf", ascending=False).head(top_n)
        return recomendados[
            ["isbn13", "title", "authors", "categories", "thumbnail", "tfidf"]
        ]
    elif tfidf_df.empty:
        recomendados = jaccard_df.sort_values("isbn13").head(top_n)
        return recomendados[["isbn13", "title", "authors", "categories", "thumbnail"]]
    elif jaccard_df.empty and tfidf_df.empty:
        return "Não há recomendações disponíveis."

    # Merge on isbn13 to align recommendations
    merged = pd.merge(
        jaccard_df[["isbn13", "title", "authors", "categories", "thumbnail"]],
        tfidf_df[["isbn13", "tfidf"]],
        on="isbn13",
        how="outer",
    )

    # Preencher informações faltantes de título, autor e categoria usando o DataFrame de livros
    merged = pd.merge(
        merged,
        livros[["isbn13", "title", "authors", "categories", "thumbnail"]],
        on="isbn13",
        how="left",
        suffixes=("", "_livro"),
    )
    for col in ["title", "authors", "categories", "thumbnail"]:
        merged[col] = merged[col].combine_first(merged[f"{col}_livro"])

    merged = merged.drop(
        columns=[
            "title_livro",
            "authors_livro",
            "categories_livro",
            "thumbnail_livro",
        ]
    )

    # Add jaccard score: 1 for recommended by jaccard, 0 otherwise
    merged["jaccard"] = merged["isbn13"].isin(jaccard_df["isbn13"]).astype(float)

    # Ajuste os pesos se quiser
    merged["score"] = 0.3 * merged["jaccard"] + 0.7 * merged["tfidf"]

    # Sort and return top_n
    recomendados = merged.sort_values("score", ascending=False).head(top_n)
    return recomendados[
        ["isbn13", "title", "authors", "categories", "thumbnail", "score"]
    ].to_json(orient="records")


def main(id, n):
    # Get hybrid recommendations for user id
    return recomendar_livros(usuario_id=id, top_n=n)
