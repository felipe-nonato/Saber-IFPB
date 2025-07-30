"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import Sidebar from "@/components/sidebar/sidebar";
import Modal from "react-modal";

interface Livro {
    id: string;
    titulo: string;
    autor: string;
    estado: string;
    data_devolucao_efetiva?: string;
    capa?: string;
    resumo?: string;
    categoria?: string;
    ISBN?: string;
    ano_publicacao?: number;
    paginas?: number;
}

export default function HistoricoPage() {
    const [livros, setLivros] = useState<Livro[]>([]);
    const [loading, setLoading] = useState(true);
    const [erro, setErro] = useState("");
    const [modalAberta, setModalAberta] = useState(false);
    const [livroSelecionado, setLivroSelecionado] = useState<Livro | null>(
        null
    );

    // Busca livros já devolvidos pelo usuário logado
    const fetchLivrosDevolvidos = async () => {
        setLoading(true);
        setErro("");
        try {
            const usuario_id = localStorage.getItem("usuario");
            if (!usuario_id) {
                setErro("Usuário não autenticado.");
                setLoading(false);
                return;
            }
            const res = await axios.get(
                `http://localhost:5000/api/users/${usuario_id}/devolvidos`
            );
            setLivros(res.data);
        } catch (e) {
            setErro("Erro ao buscar histórico de devoluções.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLivrosDevolvidos();
    }, []);

    useEffect(() => {
        if (typeof window !== "undefined") {
            Modal.setAppElement("body");
        }
    }, []);

    const handleAbrirModal = (livro: Livro) => {
        setLivroSelecionado(livro);
        setModalAberta(true);
    };

    const handleFecharModal = () => {
        setModalAberta(false);
        setLivroSelecionado(null);
    };

    return (
        <div className="flex min-h-screen bg-gradient-to-br from-[#7dabff] via-[#a2c7ff] to-[#eaf4ff]">
            <Sidebar />
            <div className="flex-1 py-12 px-2 flex items-center justify-center">
                <div className="w-full max-w-5xl space-y-12">
                    <h1 className="text-4xl font-extrabold text-[#3730A3] text-center mb-10 drop-shadow-lg tracking-tight">
                        Histórico de Livros Devolvidos
                    </h1>
                    {loading ? (
                        <div className="text-gray-500 text-center">
                            Carregando...
                        </div>
                    ) : erro ? (
                        <div className="text-red-600 text-center">{erro}</div>
                    ) : livros.length === 0 ? (
                        <div className="text-gray-500 text-center">
                            Você ainda não devolveu nenhum livro.
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
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
                                        {livro.data_devolucao_efetiva && (
                                            <span className="mt-2 px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700">
                                                Devolvido em:{" "}
                                                {new Date(
                                                    livro.data_devolucao_efetiva
                                                ).toLocaleDateString("pt-BR")}
                                            </span>
                                        )}
                                    </div>
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
                                    {livroSelecionado.data_devolucao_efetiva && (
                                        <div className="mt-4 px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700">
                                            Devolvido em:{" "}
                                            {new Date(
                                                livroSelecionado.data_devolucao_efetiva
                                            ).toLocaleDateString("pt-BR")}
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
