### Passo 1: Criar o arquivo `landing.tsx`

Crie um novo arquivo chamado `landing.tsx` no diretório `src/app`.

### Passo 2: Estruturar a página

Aqui está um exemplo de como você pode estruturar a nova página de apresentação:

```tsx
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
        <h1 className="text-4xl font-bold">Bem-vindo ao Nosso Projeto</h1>
        <p className="mt-4 text-lg">Uma breve descrição do que fazemos.</p>
      </header>

      <main className="flex flex-col items-center">
        {data ? (
          <div className="text-center">
            <h2 className="text-2xl font-semibold">Informações do Projeto</h2>
            <p className="mt-2">{data.description}</p>
            <Image
              className="mt-4"
              src={data.imageUrl}
              alt="Imagem do projeto"
              width={600}
              height={400}
            />
          </div>
        ) : (
          <p>Carregando...</p>
        )}
      </main>

      <footer className="mt-8">
        <a
          className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          href="/"
        >
          Voltar para a Home
        </a>
      </footer>
    </div>
  );
}
```

### Passo 3: Configurar a API

Certifique-se de que a API que você está chamando no `fetch` está configurada corretamente e que o endpoint `/api/your-endpoint` retorna os dados que você espera. O exemplo acima assume que a resposta da API contém um objeto com uma propriedade `description` e `imageUrl`.

### Passo 4: Estilização

Você pode ajustar as classes CSS conforme necessário para se adequar ao estilo do seu projeto. O exemplo acima usa classes do Tailwind CSS, que parecem estar em uso no seu projeto.

### Passo 5: Navegação

Adicione um link para a nova página de apresentação em sua página inicial ou em qualquer outro lugar que faça sentido na navegação do seu aplicativo.

### Passo 6: Testar

Após implementar a nova página, inicie seu servidor de desenvolvimento e teste a nova landing page para garantir que tudo esteja funcionando conforme o esperado.

Com esses passos, você deve ser capaz de criar uma nova página de apresentação do projeto como uma landing page utilizando a API existente. Se precisar de mais ajuda ou ajustes, sinta-se à vontade para perguntar!