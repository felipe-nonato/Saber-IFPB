"use client";

export default function ApiDocs() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-100 via-blue-300 to-blue-500 flex flex-col items-center py-10 px-4">
            <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-3xl">
                <h1 className="text-3xl font-bold text-blue-700 mb-4">
                    Documentação da API Saber-IFPB
                </h1>
                <p className="mb-6 text-gray-700">
                    Esta API permite gerenciar usuários, livros, empréstimos,
                    reservas e transações de moedas virtuais no sistema
                    Saber-IFPB.
                </p>

                <h2 className="text-xl font-semibold text-blue-600 mt-6 mb-2">
                    Autenticação
                </h2>
                <p className="mb-4 text-gray-700">
                    <b>Nota:</b> Algumas rotas podem exigir autenticação.
                    Implemente um sistema de autenticação conforme necessário.
                </p>

                <h2 className="text-xl font-semibold text-blue-600 mt-6 mb-2">
                    Usuários
                </h2>
                <div className="mb-4">
                    <b>POST /api/users</b>
                    <pre className="bg-gray-100 rounded p-2 text-sm mt-1">
                        {`{
  "nome": "João Silva",
  "matricula": "20231234"
}`}
                    </pre>
                    <span className="text-gray-700">Cria um novo usuário.</span>
                </div>
                <div className="mb-4">
                    <b>GET /api/users/&lt;user_id&gt;</b>
                    <span className="block text-gray-700">
                        Retorna os dados de um usuário.
                    </span>
                </div>

                <h2 className="text-xl font-semibold text-blue-600 mt-6 mb-2">
                    Livros
                </h2>
                <div className="mb-4">
                    <b>POST /api/books</b>
                    <pre className="bg-gray-100 rounded p-2 text-sm mt-1">
                        {`{
  "titulo": "O Pequeno Príncipe",
  "autor": "Antoine de Saint-Exupéry",
  "depositor_id": 1,
  "categoria": "Literatura"
}`}
                    </pre>
                    <span className="text-gray-700">
                        Deposita um novo livro no sistema.
                    </span>
                </div>
                <div className="mb-4">
                    <b>GET /api/books</b>
                    <span className="block text-gray-700">
                        Lista todos os livros cadastrados.
                    </span>
                </div>
                <div className="mb-4">
                    <b>POST /api/books/&lt;book_id&gt;/rent</b>
                    <pre className="bg-gray-100 rounded p-2 text-sm mt-1">
                        {`{
  "user_id": 1
}`}
                    </pre>
                    <span className="text-gray-700">
                        Realiza o aluguel de um livro.
                    </span>
                </div>
                <div className="mb-4">
                    <b>POST /api/books/&lt;book_id&gt;/return</b>
                    <pre className="bg-gray-100 rounded p-2 text-sm mt-1">
                        {`{
  "user_id": 1
}`}
                    </pre>
                    <span className="text-gray-700">
                        Realiza a devolução de um livro.
                    </span>
                </div>
                <div className="mb-4">
                    <b>POST /api/books/&lt;book_id&gt;/reserve</b>
                    <pre className="bg-gray-100 rounded p-2 text-sm mt-1">
                        {`{
  "user_id": 1
}`}
                    </pre>
                    <span className="text-gray-700">
                        Reserva um livro para o usuário.
                    </span>
                </div>

                <h2 className="text-xl font-semibold text-blue-600 mt-6 mb-2">
                    Exemplo de Resposta
                </h2>
                <pre className="bg-gray-100 rounded p-2 text-sm mb-4">
                    {`{
  "message": "Livro alugado com sucesso.",
  "book": {
    "id": "uuid-do-livro",
    "titulo": "O Pequeno Príncipe",
    "estado": "alugado",
    "rentee_id": 1,
    "data_devolucao_estimada": "2025-07-29 12:00:00"
  }
}`}
                </pre>

                <h2 className="text-xl font-semibold text-blue-600 mt-6 mb-2">
                    Observações
                </h2>
                <ul className="list-disc pl-6 text-gray-700">
                    <li>Todos os endpoints retornam respostas em JSON.</li>
                    <li>
                        Em caso de erro, a resposta terá o campo{" "}
                        <code>error</code> com a mensagem.
                    </li>
                    <li>
                        Para mais detalhes, consulte o código-fonte ou entre em
                        contato com a equipe do projeto.
                    </li>
                </ul>
            </div>
        </div>
    );
}
