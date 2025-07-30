"use client";
import { useEffect, useState } from "react";
import Sidebar from "@/components/sidebar/sidebar";
import axios from "axios";

export default function DoarLivroPage() {
    const [titulo, setTitulo] = useState("");
    const [autor, setAutor] = useState("");
    const [categoria, setCategoria] = useState("");
    const [depositor_id, setDepositorId] = useState("");
    const [mensagem, setMensagem] = useState("");
    const [erro, setErro] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setDepositorId(localStorage.getItem("usuario") || "");
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMensagem("");
        setErro("");
        setLoading(true);
        try {
            const response = await axios.post(
                "http://localhost:5000/api/books",
                {
                    titulo,
                    autor,
                    categoria,
                    depositor_id,
                }
            );
            setMensagem(response.data.message || "Livro doado com sucesso!");
            setTitulo("");
            setAutor("");
            setCategoria("");
            setDepositorId("");
        } catch (err: any) {
            setErro(
                err.response?.data?.error ||
                    "Erro ao doar livro. Verifique os dados e tente novamente."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                <main className="flex-1 flex items-center justify-center bg-gray-100">
                    <div className="bg-white rounded-lg shadow-md p-8 w-full max-w-md">
                        <h2 className="text-2xl font-bold mb-6 text-blue-700 text-center">
                            Doar Livro
                        </h2>
                        <form className="space-y-5" onSubmit={handleSubmit}>
                            <div>
                                <label
                                    className="block text-gray-700 font-medium mb-1"
                                    htmlFor="titulo"
                                >
                                    Título
                                </label>
                                <input
                                    type="text"
                                    id="titulo"
                                    value={titulo}
                                    onChange={(e) => setTitulo(e.target.value)}
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    placeholder="Título do livro"
                                    required
                                />
                            </div>
                            <div>
                                <label
                                    className="block text-gray-700 font-medium mb-1"
                                    htmlFor="autor"
                                >
                                    Autor
                                </label>
                                <input
                                    type="text"
                                    id="autor"
                                    value={autor}
                                    onChange={(e) => setAutor(e.target.value)}
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    placeholder="Autor do livro"
                                    required
                                />
                            </div>
                            <div>
                                <label
                                    className="block text-gray-700 font-medium mb-1"
                                    htmlFor="categoria"
                                >
                                    Categoria
                                </label>
                                <input
                                    type="text"
                                    id="categoria"
                                    value={categoria}
                                    onChange={(e) =>
                                        setCategoria(e.target.value)
                                    }
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    placeholder="Categoria do livro"
                                />
                            </div>
                            {erro && (
                                <div className="text-red-600 text-sm">
                                    {erro}
                                </div>
                            )}
                            {mensagem && (
                                <div className="text-green-600 text-sm">
                                    {mensagem}
                                </div>
                            )}
                            <button
                                type="submit"
                                className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition"
                                disabled={loading}
                            >
                                {loading ? "Enviando..." : "Doar Livro"}
                            </button>
                        </form>
                    </div>
                </main>
            </div>
        </div>
    );
}
