"use client";

import { use, useState } from "react";
import axios from "axios";
import Logo from "@/components/logo/logo";

export default function Login() {
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [erro, setErro] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErro("");
        setLoading(true);
        try {
            const response = await axios.post("http://localhost:5000/login", {
                email,
                senha,
            });
            if (response.data.success) {
                // Redirecionar ou salvar token/usuário aqui
                localStorage.setItem("usuario", response.data.usuario);
                if (localStorage.getItem("usuario") !== null)
                    window.location.href = "/books";
            } else {
                setErro(response.data.error || "Falha no login");
            }
        } catch (err: any) {
            setErro("Erro ao conectar com o servidor");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-blue-300 to-blue-500">
            <div className="bg-white rounded-xl shadow-lg p-8 b w-full max-w-md">
                <div className="flex flex-col items-center mb-6">
                    <Logo />
                    <h2 className="text-2xl font-bold text-blue-700 mb-1">
                        Bem-vindo de volta!
                    </h2>
                    <p className="text-gray-500 text-sm">
                        Faça login para acessar sua conta
                    </p>
                </div>
                <form className="space-y-5" onSubmit={handleSubmit}>
                    <div>
                        <label
                            className="block text-gray-700 font-medium mb-1"
                            htmlFor="email"
                        >
                            E-mail
                        </label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="seu@email.com"
                            required
                        />
                    </div>
                    <div>
                        <label
                            className="block text-gray-700 font-medium mb-1"
                            htmlFor="password"
                        >
                            Senha
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={senha}
                            onChange={(e) => setSenha(e.target.value)}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Sua senha"
                            required
                        />
                    </div>
                    {erro && <div className="text-red-600 text-sm">{erro}</div>}
                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition"
                        disabled={loading}
                    >
                        {loading ? "Entrando..." : "Entrar"}
                    </button>
                </form>
                <div className="mt-6 text-center">
                    <a
                        href="#"
                        className="text-blue-600 hover:underline text-sm"
                    >
                        Esqueceu a senha?
                    </a>
                </div>
            </div>
        </div>
    );
}
