"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";

interface Livro {
    isbn13: string;
    titulo: string;
    thumbnail?: string;
    avaliacao?: number;
}

const PAGE_SIZE = 8;

export default function AvaliacoesPage() {
    const [livros, setLivros] = useState<Livro[]>([]);
    const [loading, setLoading] = useState(true);
    const [erro, setErro] = useState("");
    const [pagina, setPagina] = useState(1);

    useEffect(() => {
        const usuarioId = localStorage.getItem("usuario");
        if (!usuarioId) {
            setErro("Usuário não autenticado.");
            setLoading(false);
            return;
        }

        const fetchData = async () => {
            try {
                const res = await axios.get(
                    `http://localhost:5000/livros-lidos?id=${usuarioId}`
                );
                setLivros(res.data.livros_lidos || []);
            } catch (e) {
                setErro("Erro ao buscar dados do servidor.");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const totalPaginas = Math.ceil(livros.length / PAGE_SIZE);
    const livrosPagina = livros.slice(
        (pagina - 1) * PAGE_SIZE,
        pagina * PAGE_SIZE
    );

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#7dabff] via-[#a2c7ff] to-[#eaf4ff] py-12 px-2 flex items-center justify-center">
            <div className="w-full max-w-5xl space-y-10">
                <div className="flex items-center justify-between mb-6">
                    <h1 className="text-4xl font-extrabold text-white drop-shadow-lg tracking-tight">
                        Todos os livros avaliados
                    </h1>
                    <Link
                        href="/books"
                        className="text-white font-semibold hover:underline text-lg"
                    >
                        ← Voltar para estante
                    </Link>
                </div>

                <div className="bg-white rounded-3xl shadow-2xl p-8 border-4 border-[#7dabff]/20">
                    {loading ? (
                        <div className="text-gray-500">Carregando...</div>
                    ) : erro ? (
                        <div className="text-red-600">{erro}</div>
                    ) : livros.length === 0 ? (
                        <div className="text-gray-500">
                            Nenhum livro avaliado ainda.
                        </div>
                    ) : (
                        <>
                            <ul className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-7">
                                {livrosPagina.map((livro) => (
                                    <li
                                        key={livro.isbn13}
                                        className="flex flex-col items-center bg-[#f5faff] rounded-xl p-4 shadow hover:scale-[1.02] transition"
                                    >
                                        {livro.thumbnail ? (
                                            <img
                                                src={livro.thumbnail}
                                                alt={livro.titulo}
                                                className="w-24 h-36 object-cover rounded-lg shadow mb-3"
                                            />
                                        ) : (
                                            <div className="w-24 h-36 flex items-center justify-center bg-gray-200 text-gray-500 rounded-lg shadow text-xs text-center mb-3">
                                                Sem imagem
                                            </div>
                                        )}
                                        <span className="font-semibold text-gray-700 text-center mb-2">
                                            {livro.titulo}
                                        </span>
                                        <span className="bg-[#7dabff] text-white px-3 py-1 rounded-lg text-sm font-bold shadow">
                                            {livro.avaliacao} ★
                                        </span>
                                    </li>
                                ))}
                            </ul>
                            {/* Paginação */}
                            <div className="flex justify-center items-center gap-3 mt-8">
                                <button
                                    className="px-3 py-1 rounded bg-[#7dabff] text-white font-semibold disabled:opacity-50"
                                    onClick={() =>
                                        setPagina((p) => Math.max(1, p - 1))
                                    }
                                    disabled={pagina === 1}
                                >
                                    Anterior
                                </button>
                                <span className="font-semibold text-[#7dabff]">
                                    Página {pagina} de {totalPaginas}
                                </span>
                                <button
                                    className="px-3 py-1 rounded bg-[#7dabff] text-white font-semibold disabled:opacity-50"
                                    onClick={() =>
                                        setPagina((p) =>
                                            Math.min(totalPaginas, p + 1)
                                        )
                                    }
                                    disabled={pagina === totalPaginas}
                                >
                                    Próxima
                                </button>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
