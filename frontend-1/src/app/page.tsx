// filepath: /home/lipe/Codes/Saber-IFPB/frontend/src/app/landing.tsx
import Image from "next/image";
import { useEffect, useState } from "react";

export default function LandingPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Substitua pela URL da sua API
    fetch('/api/your-endpoint')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold">Bem-vindo ao Projeto Saber IFPB</h1>
        <p className="mt-4 text-lg">Uma plataforma para [descrever brevemente o que o projeto faz].</p>
      </header>

      <main className="flex flex-col items-center">
        {data ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {data.map(item => (
              <div key={item.id} className="border p-4 rounded shadow">
                <h2 className="text-xl font-semibold">{item.title}</h2>
                <p>{item.description}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>Carregando dados...</p>
        )}
      </main>

      <footer className="mt-8">
        <Image
          src="/logo.svg"
          alt="Logo do projeto"
          width={100}
          height={100}
        />
        <p className="mt-2">© 2023 Saber IFPB. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}