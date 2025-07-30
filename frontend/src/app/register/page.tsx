"use client";
import { useState } from "react";
import axios from "axios";
import Logo from "@/components/logo/logo"; // Ajuste o caminho se necessário
import { redirect, RedirectType } from "next/navigation";

export default function Register() {
    const [nome, setNome] = useState("");
    const [matricula, setMatricula] = useState("");
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [saldoMoedas, setSaldoMoedas] = useState(0);
    const [erro, setErro] = useState("");
    const [sucesso, setSucesso] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErro("");
        setSucesso("");
        setLoading(true);
        try {
            const response = await axios.post(
                "http://localhost:5000/api/users",
                {
                    nome,
                    matricula,
                    email,
                    senha,
                }
            );
            if (response.data.user) {
                setSucesso("Usuário cadastrado com sucesso! Faça login.");
                setNome("");
                setMatricula("");
                setEmail("");
                setSenha("");
                redirect("/login", RedirectType.push); // Redireciona para a página de login após o registro
            } else {
                setErro(response.data.error || "Erro ao cadastrar usuário");
            }
        } catch (err: any) {
            setErro(
                err.response?.data?.error || "Erro ao conectar com o servidor"
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-blue-300 to-blue-500">
            <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-md">
                <div className="flex flex-col items-center mb-6">
                    <Logo />
                    <h2 className="text-2xl font-bold text-blue-700 mb-1">
                        Crie sua conta
                    </h2>
                    <p className="text-gray-500 text-sm">
                        Preencha os dados para se registrar
                    </p>
                </div>
                <form className="space-y-5" onSubmit={handleSubmit}>
                    <div>
                        <label
                            className="block text-gray-700 font-medium mb-1"
                            htmlFor="nome"
                        >
                            Nome
                        </label>
                        <input
                            type="text"
                            id="nome"
                            value={nome}
                            onChange={(e) => setNome(e.target.value)}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Seu nome"
                            required
                        />
                    </div>
                    <div>
                        <label
                            className="block text-gray-700 font-medium mb-1"
                            htmlFor="matricula"
                        >
                            Matrícula (opcional)
                        </label>
                        <input
                            type="text"
                            id="matricula"
                            value={matricula}
                            onChange={(e) => setMatricula(e.target.value)}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Sua matrícula"
                        />
                    </div>
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
                            htmlFor="senha"
                        >
                            Senha
                        </label>
                        <input
                            type="password"
                            id="senha"
                            value={senha}
                            onChange={(e) => setSenha(e.target.value)}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Sua senha"
                            required
                        />
                    </div>
                    {erro && <div className="text-red-600 text-sm">{erro}</div>}
                    {sucesso && (
                        <div className="text-green-600 text-sm">{sucesso}</div>
                    )}
                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition"
                        disabled={loading}
                    >
                        {loading ? "Registrando..." : "Registrar"}
                    </button>
                </form>
                <div className="mt-6 text-center">
                    <a
                        href="/login"
                        className="text-blue-600 hover:underline text-sm"
                    >
                        Já tem conta? Faça login
                    </a>
                </div>
            </div>
        </div>
    );
}
