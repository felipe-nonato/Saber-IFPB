"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import Modal from "react-modal";
import Sidebar from "@/components/sidebar/sidebar";

interface Livro {
    id: string;
    titulo: string;
    autor: string;
    estado: string;
    depositor_id: number;
    categoria?: string;
    ISBN?: string;
    resumo?: string;
    capa?: string;
    ano_publicacao?: number;
    paginas?: number;
}

export default function BooksPage() {
    const [livros, setLivros] = useState<Livro[]>([]);
    const [loading, setLoading] = useState(true);
    const [erro, setErro] = useState("");
    const [modalAberta, setModalAberta] = useState(false);
    const [livroSelecionado, setLivroSelecionado] = useState<Livro | null>(
        null
    );
    const [alugando, setAlugando] = useState(false);
    const [mensagem, setMensagem] = useState("");

    useEffect(() => {
        const fetchLivros = async () => {
            setLoading(true);
            setErro("");
            try {
                const res = await axios.get("http://localhost:5000/api/books");
                setLivros(res.data);
            } catch (e) {
                setErro("Erro ao buscar livros do servidor.");
            } finally {
                setLoading(false);
            }
        };
        fetchLivros();
    }, []);

    useEffect(() => {
        if (typeof window !== "undefined") {
            Modal.setAppElement("body");
        }
    }, []);

    const handleAbrirModal = (livro: Livro) => {
        setLivroSelecionado(livro);
        setMensagem("");
        setModalAberta(true);
    };

    const handleFecharModal = () => {
        setModalAberta(false);
        setLivroSelecionado(null);
        setMensagem("");
    };

    const handleAlugar = async (livro: Livro) => {
        setAlugando(true);
        setMensagem("");
        try {
            const usuario_id = localStorage.getItem("usuario");
            if (!usuario_id) {
                setMensagem("Usuário não autenticado.");
                setAlugando(false);
                return;
            }
            const res = await axios.post(
                `http://localhost:5000/api/books/${livro.id}/rent`,
                { user_id: usuario_id }
            );
            setMensagem(res.data.message || "Livro alugado com sucesso!");
            // Atualiza o estado do livro na lista
            setLivros((prev) =>
                prev.map((l) =>
                    l.id === livro.id ? { ...l, estado: "alugado" } : l
                )
            );
        } catch (e: any) {
            setMensagem(
                e.response?.data?.error ||
                    "Erro ao tentar alugar o livro. Verifique seu saldo ou tente novamente."
            );
        } finally {
            setAlugando(false);
        }
    };

    return (
        <div className="flex min-h-screen bg-gradient-to-br from-[#7dabff] via-[#a2c7ff] to-[#eaf4ff]">
            <Sidebar />
            <div className="flex-1 py-12 px-2 flex items-center justify-center">
                <div className="w-full max-w-6xl space-y-12">
                    <h1 className="text-4xl font-extrabold text-[#3730A3] text-center mb-10 drop-shadow-lg tracking-tight">
                        Livros Disponíveis
                    </h1>
                    {loading ? (
                        <div className="text-gray-500 text-center">
                            Carregando...
                        </div>
                    ) : erro ? (
                        <div className="text-red-600 text-center">{erro}</div>
                    ) : livros.length === 0 ? (
                        <div className="text-gray-500 text-center">
                            Nenhum livro cadastrado ainda.
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                            {livros.map((livro) => (
                                <div
                                    key={livro.id}
                                    className="bg-white rounded-2xl shadow-lg p-5 flex flex-col items-center hover:scale-105 transition cursor-pointer border-2 border-[#7dabff]/20"
                                    onClick={() => handleAbrirModal(livro)}
                                >
                                    <div className="w-24 h-36 mb-4 flex items-center justify-center bg-gray-100 rounded-lg shadow">
                                        {livro.capa ? (
                                            <img
                                                src={livro.capa}
                                                alt={livro.titulo}
                                                className="w-full h-full object-cover rounded"
                                            />
                                        ) : (
                                            <span className="text-gray-400 text-xs text-center">
                                                Sem capa
                                            </span>
                                        )}
                                    </div>
                                    <div className="flex-1 flex flex-col items-center">
                                        <span className="font-bold text-lg text-[#3730A3] text-center">
                                            {livro.titulo}
                                        </span>
                                        <span className="text-gray-600 text-sm text-center">
                                            {livro.autor}
                                        </span>
                                        <span
                                            className={`mt-2 px-3 py-1 rounded-full text-xs font-semibold ${
                                                livro.estado === "disponivel"
                                                    ? "bg-green-100 text-green-700"
                                                    : livro.estado === "alugado"
                                                    ? "bg-yellow-100 text-yellow-700"
                                                    : "bg-blue-100 text-blue-700"
                                            }`}
                                        >
                                            {livro.estado
                                                .charAt(0)
                                                .toUpperCase() +
                                                livro.estado.slice(1)}
                                        </span>
                                    </div>
                                    <button
                                        className={`mt-4 w-full py-2 rounded-lg font-bold transition ${
                                            livro.estado === "disponivel"
                                                ? "bg-blue-600 text-white hover:bg-blue-700"
                                                : "bg-gray-300 text-gray-500 cursor-not-allowed"
                                        }`}
                                        disabled={livro.estado !== "disponivel"}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleAlugar(livro);
                                        }}
                                    >
                                        Alugar
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Modal do livro */}
                    <Modal
                        isOpen={modalAberta}
                        onRequestClose={handleFecharModal}
                        contentLabel="Detalhes do Livro"
                        className="bg-white rounded-2xl shadow-xl p-8 max-w-lg mx-auto mt-24 outline-none relative"
                        overlayClassName="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
                    >
                        {livroSelecionado && (
                            <div>
                                <button
                                    onClick={handleFecharModal}
                                    className="absolute top-4 right-4 text-gray-400 hover:text-gray-700 text-2xl font-bold"
                                    aria-label="Fechar"
                                >
                                    ×
                                </button>
                                <div className="flex flex-col items-center">
                                    <div className="w-32 h-48 mb-4 flex items-center justify-center bg-gray-100 rounded-lg shadow">
                                        {livroSelecionado.capa ? (
                                            <img
                                                src={livroSelecionado.capa}
                                                alt={livroSelecionado.titulo}
                                                className="w-full h-full object-cover rounded"
                                            />
                                        ) : (
                                            <span className="text-gray-400 text-xs text-center">
                                                Sem capa
                                            </span>
                                        )}
                                    </div>
                                    <h2 className="text-2xl font-bold text-[#3730A3] mb-2 text-center">
                                        {livroSelecionado.titulo}
                                    </h2>
                                    <div className="text-gray-600 text-base mb-2 text-center">
                                        <span className="font-semibold">
                                            Autor:
                                        </span>{" "}
                                        {livroSelecionado.autor}
                                    </div>
                                    {livroSelecionado.categoria && (
                                        <div className="text-gray-500 text-sm mb-2">
                                            <span className="font-semibold">
                                                Categoria:
                                            </span>{" "}
                                            {livroSelecionado.categoria}
                                        </div>
                                    )}
                                    {livroSelecionado.ISBN && (
                                        <div className="text-gray-500 text-sm mb-2">
                                            <span className="font-semibold">
                                                ISBN:
                                            </span>{" "}
                                            {livroSelecionado.ISBN}
                                        </div>
                                    )}
                                    {livroSelecionado.ano_publicacao && (
                                        <div className="text-gray-500 text-sm mb-2">
                                            <span className="font-semibold">
                                                Ano:
                                            </span>{" "}
                                            {livroSelecionado.ano_publicacao}
                                        </div>
                                    )}
                                    {livroSelecionado.paginas && (
                                        <div className="text-gray-500 text-sm mb-2">
                                            <span className="font-semibold">
                                                Páginas:
                                            </span>{" "}
                                            {livroSelecionado.paginas}
                                        </div>
                                    )}
                                    {livroSelecionado.resumo && (
                                        <div className="text-gray-700 text-sm mt-4 mb-2 text-justify">
                                            <span className="font-semibold">
                                                Resumo:
                                            </span>{" "}
                                            {livroSelecionado.resumo}
                                        </div>
                                    )}
                                    <div className="mt-4">
                                        <span
                                            className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                                livroSelecionado.estado ===
                                                "disponivel"
                                                    ? "bg-green-100 text-green-700"
                                                    : livroSelecionado.estado ===
                                                      "alugado"
                                                    ? "bg-yellow-100 text-yellow-700"
                                                    : "bg-blue-100 text-blue-700"
                                            }`}
                                        >
                                            {livroSelecionado.estado
                                                .charAt(0)
                                                .toUpperCase() +
                                                livroSelecionado.estado.slice(
                                                    1
                                                )}
                                        </span>
                                    </div>
                                    <button
                                        className={`mt-6 w-full py-2 rounded-lg font-bold transition ${
                                            livroSelecionado.estado ===
                                            "disponivel"
                                                ? "bg-blue-600 text-white hover:bg-blue-700"
                                                : "bg-gray-300 text-gray-500 cursor-not-allowed"
                                        }`}
                                        disabled={
                                            livroSelecionado.estado !==
                                                "disponivel" || alugando
                                        }
                                        onClick={() =>
                                            handleAlugar(livroSelecionado)
                                        }
                                    >
                                        {alugando
                                            ? "Alugando..."
                                            : livroSelecionado.estado ===
                                              "disponivel"
                                            ? "Alugar"
                                            : "Indisponível"}
                                    </button>
                                    {mensagem && (
                                        <div className="mt-4 text-center text-sm font-semibold text-blue-700">
                                            {mensagem}
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </Modal>
                </div>
            </div>
        </div>
    );
}
