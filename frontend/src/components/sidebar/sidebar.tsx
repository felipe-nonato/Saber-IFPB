"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import SmallLogo from "../logo/smallLogo";
import { useCallback, useEffect, useState } from "react";

const links = [
    { href: "/alugar", label: "Alugar Livro" },
    { href: "/doar", label: "Doar Livro" },
    { href: "/devolver", label: "Devolver Livro" },
    { href: "/historico", label: "Histórico" },
];

export default function Sidebar() {
    const pathname = usePathname();
    const router = useRouter();

    const [usuario, setUsuario] = useState<{
        nome: string;
        saldoMoedas: number;
    } | null>(null);

    useEffect(() => {
        // Busca usuário do localStorage e, se possível, do backend
        const usuarioId = localStorage.getItem("usuario");
        const token = localStorage.getItem("token");
        if (usuarioId && token) {
            fetch(`http://localhost:5000/api/users/${usuarioId}`, {
                headers: { Authorization: `Bearer ${token}` },
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data && data.nome) {
                        setUsuario({
                            nome: data.nome,
                            saldoMoedas: data.saldoMoedas,
                        });
                    }
                })
                .catch(() => {
                    setUsuario(null);
                });
        }
    }, []);

    const handleLogout = useCallback(() => {
        if (typeof window !== "undefined") {
            localStorage.removeItem("token");
            localStorage.removeItem("usuario_id");
        }
        router.push("/login");
    }, [router]);

    return (
        <aside className="w-64 h-screen bg-blue-700 text-white flex flex-col py-8 px-4 shadow-lg">
            {/* Logo */}
            <div className="flex flex-col items-center mb-8">
                <SmallLogo />
            </div>
            {/* Links */}
            <nav className="flex-1 flex flex-col gap-4">
                {links.map((link) => (
                    <Link
                        key={link.href}
                        href={link.href}
                        className={`py-2 px-4 rounded transition-colors w-full text-center ${
                            pathname === link.href
                                ? "bg-blue-900 font-semibold"
                                : "hover:bg-blue-800"
                        }`}
                    >
                        {link.label}
                    </Link>
                ))}
            </nav>
            {/* Usuário e botão sair */}
            <div className="mt-8 flex flex-col items-center gap-2">
                {usuario && (
                    <>
                        <span className="font-semibold text-lg">
                            {usuario.nome}
                        </span>
                        <span className="text-sm text-blue-100">
                            Moedas:{" "}
                            <span className="font-bold">
                                {usuario.saldoMoedas}
                            </span>
                        </span>
                    </>
                )}
                <button
                    onClick={handleLogout}
                    className="mt-4 py-2 px-4 rounded bg-red-600 hover:bg-red-700 transition-colors w-full font-semibold"
                >
                    Sair
                </button>
            </div>
        </aside>
    );
}
