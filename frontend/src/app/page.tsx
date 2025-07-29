import Logo from "@/components/logo/logo";
import Image from "next/image";

export default function Home() {
    return (
        <div className="flex flex-col min-h-screen items-center justify-center bg-gradient-to-br from-[#f5f7fa] to-[#c3cfe2] p-6">
            <header className="flex flex-col items-center gap-2 mb-8">
                <Logo />
            </header>

            <main className="flex flex-col gap-8 items-center w-full max-w-2xl">
                <section className="bg-white rounded-xl shadow p-6 w-full">
                    <h2 className="text-2xl font-semibold mb-2 text-[#2d3748]">
                        Sobre o Projeto
                    </h2>
                    <p className="text-[#4a5568]">
                        O <b>Saber-IFPB</b> é uma API desenvolvida em Flask para
                        facilitar o empréstimo, reserva e gestão de livros entre
                        estudantes. O sistema utiliza padrões de projeto,
                        autenticação, notificações e integração com moedas
                        virtuais para incentivar a colaboração.
                    </p>
                </section>

                <section className="bg-white rounded-xl shadow p-6 w-full">
                    <h2 className="text-xl font-semibold mb-2 text-[#2d3748]">
                        Funcionalidades
                    </h2>
                    <ul className="list-disc pl-5 text-[#4a5568] space-y-1">
                        <li>Cadastro e autenticação de usuários</li>
                        <li>Depósito, empréstimo e reserva de livros</li>
                        <li>Notificações por e-mail e SMS</li>
                        <li>Gestão de categorias e penalidades</li>
                        <li>Transações com moedas virtuais</li>
                        <li>API RESTful documentada</li>
                    </ul>
                </section>

                <section className="bg-white rounded-xl shadow p-6 w-full">
                    <h2 className="text-xl font-semibold mb-2 text-[#2d3748]">
                        Como usar
                    </h2>
                    <ol className="list-decimal pl-5 text-[#4a5568] space-y-1">
                        <li>Faça login ou cadastre-se na plataforma</li>
                        <li>
                            Deposite livros para compartilhar com outros alunos
                        </li>
                        <li>Pesquise e reserve livros disponíveis</li>
                        <li>Gerencie suas transações e saldo de moedas</li>
                    </ol>
                </section>

                <section className="flex flex-col sm:flex-row gap-4 justify-center w-full">
                    <a
                        href="https://github.com/felipe-nonato/Saber-IFPB"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-[#2b6cb0] text-white px-6 py-2 rounded-lg font-semibold shadow hover:bg-[#2c5282] transition"
                    >
                        Ver código no GitHub
                    </a>
                    <a
                        href="/api/docs"
                        className="bg-[#38a169] text-white px-6 py-2 rounded-lg font-semibold shadow hover:bg-[#2f855a] transition"
                    >
                        Documentação da API
                    </a>
                </section>
            </main>

            <footer className="mt-12 text-[#718096] text-sm text-center">
                © {new Date().getFullYear()} Saber-IFPB. Projeto acadêmico sem
                fins lucrativos.
            </footer>
        </div>
    );
}
