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

interface Recomendado {
    authors: string;
    categories: string;
    isbn13: string;
    score: number;
    thumbnail?: string;
    title: string;
}

export default function BooksPage() {
    const [livrosLidos, setLivrosLidos] = useState<Livro[]>([]);
    const [recomendados, setRecomendados] = useState<Recomendado[]>([]);
    const [loading, setLoading] = useState(true);
    const [erro, setErro] = useState("");

    useEffect(() => {
        const usuarioId = localStorage.getItem("usuario");
        if (!usuarioId) {
            setErro("Usuário não autenticado.");
            setLoading(false);
            return;
        }

        const fetchData = async () => {
            try {
                // Livros já avaliados
                const lidosRes = await axios.get(
                    `http://localhost:5000/livros-lidos?id=${usuarioId}`
                );
                setLivrosLidos(lidosRes.data.livros_lidos || []);

                // Recomendações
                const recRes = await axios.get(
                    `http://localhost:5000/recommendations?id=${usuarioId}&num=5`
                );
                const recs = recRes.data.recommendations || recRes.data || [];
                setRecomendados(recs);
            } catch (e) {
                setErro("Erro ao buscar dados do servidor.");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    function afinidadeTexto(score: number) {
        const percent = Math.round(score * 100);
        return `Este livro combina ${percent}% com seu perfil de leitura`;
    }

    function handleLogout() {
        localStorage.clear();
        window.location.href = "/login";
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#7dabff] via-[#a2c7ff] to-[#eaf4ff] py-12 px-2 flex items-center justify-center">
            <div className="w-full max-w-7xl space-y-12">
                <div className="flex items-center justify-between mb-10">
                    <h1 className="text-5xl font-extrabold text-white text-center drop-shadow-lg tracking-tight">
                        Sua Estante
                    </h1>
                    <button
                        onClick={handleLogout}
                        className="bg-white text-[#7dabff] font-bold px-5 py-2 rounded-xl shadow hover:bg-[#eaf4ff] hover:text-[#0056b3] transition"
                        title="Sair"
                    >
                        Sair
                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                    {/* Livros já avaliados */}
                    <section className="bg-white rounded-3xl shadow-2xl p-8 flex flex-col h-full border-4 border-[#7dabff]/20">
                        <h2 className="text-2xl font-bold text-[#7dabff] mb-6 flex items-center gap-2">
                            <svg
                                className="w-7 h-7 text-[#7dabff]"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M12 20l9 2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v16l9-2z"
                                />
                            </svg>
                            Livros já avaliados
                        </h2>
                        {loading ? (
                            <div className="text-gray-500">Carregando...</div>
                        ) : erro ? (
                            <div className="text-red-600">{erro}</div>
                        ) : livrosLidos.length === 0 ? (
                            <div className="text-gray-500">
                                Nenhum livro avaliado ainda.
                            </div>
                        ) : (
                            <>
                                <ul className="space-y-5">
                                    {livrosLidos.slice(0, 5).map((livro) => (
                                        <li
                                            key={livro.isbn13}
                                            className="flex items-center gap-5 bg-[#f5faff] rounded-xl p-3 shadow hover:scale-[1.02] transition"
                                        >
                                            {livro.thumbnail ? (
                                                <img
                                                    src={livro.thumbnail}
                                                    alt={livro.titulo}
                                                    className="w-16 h-24 object-cover rounded-lg shadow"
                                                />
                                            ) : (
                                                <div className="w-16 h-24 flex items-center justify-center bg-gray-200 text-gray-500 rounded-lg shadow text-xs text-center">
                                                    Sem imagem
                                                </div>
                                            )}
                                            <div className="flex-1">
                                                <span className="font-semibold text-gray-700 text-lg">
                                                    {livro.titulo}
                                                </span>
                                            </div>
                                            <span className="bg-[#7dabff] text-white px-4 py-1 rounded-lg text-base font-bold shadow">
                                                {livro.avaliacao} ★
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                                <div className="mt-8 text-right">
                                    <Link
                                        href="/avaliacoes"
                                        className="text-[#7dabff] hover:underline font-semibold text-base"
                                    >
                                        Ver todas as avaliações →
                                    </Link>
                                </div>
                            </>
                        )}
                    </section>

                    {/* Livros recomendados */}
                    <section className="bg-white rounded-3xl shadow-2xl p-8 flex flex-col h-full border-4 border-[#7dabff]/20">
                        <h2 className="text-2xl font-bold text-[#7dabff] mb-6 flex items-center gap-2">
                            <svg
                                className="w-7 h-7 text-[#7dabff]"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                />
                            </svg>
                            Livros recomendados para você
                        </h2>
                        {loading ? (
                            <div className="text-gray-500">Carregando...</div>
                        ) : recomendados.length === 0 ? (
                            <div className="text-gray-500">
                                Nenhuma recomendação disponível.
                            </div>
                        ) : (
                            <ul className="space-y-5">
                                {recomendados.map((livro) => (
                                    <li
                                        key={livro.isbn13}
                                        className="flex items-center gap-5 bg-[#f5faff] rounded-xl p-3 shadow hover:scale-[1.02] transition"
                                    >
                                        {livro.thumbnail ? (
                                            <img
                                                src={livro.thumbnail}
                                                alt={livro.title}
                                                className="w-16 h-24 object-cover rounded-lg shadow"
                                            />
                                        ) : (
                                            <div className="w-16 h-24 flex items-center justify-center bg-gray-200 text-gray-500 rounded-lg shadow text-xs text-center">
                                                Sem imagem
                                            </div>
                                        )}
                                        <div className="flex-1">
                                            <span className="font-semibold text-gray-700 text-lg">
                                                {livro.title}
                                            </span>
                                            <div className="text-xs text-gray-500">
                                                {livro.authors}
                                            </div>
                                            <div className="text-xs text-gray-400">
                                                {livro.categories}
                                            </div>
                                            <div className="mt-2 text-sm text-[#7dabff] font-semibold">
                                                {afinidadeTexto(livro.score)}
                                            </div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </section>
                </div>
            </div>
        </div>
    );
}
