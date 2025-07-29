// filepath: /home/lipe/Codes/Saber-IFPB/frontend/src/app/landing.tsx
import Image from "next/image";
import { useEffect, useState } from "react";

export default function LandingPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Chame a API existente para obter os dados necessários
    const fetchData = async () => {
      const response = await fetch('/api/your-endpoint'); // Substitua pelo seu endpoint
      const result = await response.json();
      setData(result);
    };

    fetchData();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold">Bem-vindo ao Nosso Projeto!</h1>
        <p className="mt-4 text-lg">Uma breve descrição do que o projeto faz.</p>
      </header>
      
      {data ? (
        <section className="grid grid-cols-1 sm:grid-cols-2 gap-8">
          {data.map((item) => (
            <div key={item.id} className="border p-4 rounded shadow">
              <Image src={item.image} alt={item.title} width={300} height={200} />
              <h2 className="text-xl font-semibold mt-2">{item.title}</h2>
              <p>{item.description}</p>
            </div>
          ))}
        </section>
      ) : (
        <p>Carregando...</p>
      )}

      <footer className="mt-8">
        <p>© 2023 Seu Nome ou Empresa. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}