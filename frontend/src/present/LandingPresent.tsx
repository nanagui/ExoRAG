import { useEffect, useState } from 'react';

type Doc = { title: string; path: string; content: string };

function CodeBlock({ doc }: { doc: Doc }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try { await navigator.clipboard.writeText(doc.content); setCopied(true); setTimeout(() => setCopied(false), 1200); } catch {}
  };
  return (
    <div className="code-block">
      <div className="code-block-header">
        <span>{doc.title}</span>
        <button onClick={copy}>{copied ? 'Copiado' : 'Copiar'}</button>
      </div>
      <pre><code>{doc.content}</code></pre>
      <div className="code-block-path">{doc.path}</div>
    </div>
  );
}

export default function LandingPresent() {
  const [docs, setDocs] = useState<Doc[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const list: { title: string; file: string; path: string }[] = [
      { title: 'Prompt Inicial — Meta Projeto', file: '001_prompt_inicial_meta_projeto.md', path: 'prompts/01-iniciacao/001_prompt_inicial_meta_projeto.md' },
      { title: 'Pesquisa do Desafio (AI/ML)', file: '003_pesquisa_desafio_ai_ml.md', path: 'prompts/02-planejamento/003_pesquisa_desafio_ai_ml.md' },
      { title: 'Prompts Multi‑IAs (Research)', file: '004_prompts_multiplas_ias_research.md', path: 'prompts/03-desenvolvimento/004_prompts_multiplas_ias_research.md' },
      { title: 'Síntese Final (Research)', file: '005_prompt_sintese_final_research.md', path: 'prompts/03-desenvolvimento/005_prompt_sintese_final_research.md' },
      { title: 'Slides (gamma.app)', file: 'gamma_meta_projeto_prompt.md', path: 'projeto/apresentacao/slides/gamma_meta_projeto_prompt.md' },
      { title: 'Roteiro de Vídeo (Veo3)', file: 'veo3_video_roteiro.md', path: 'projeto/apresentacao/video/veo3_video_roteiro.md' }
    ];
    Promise.all(
      list.map(async (it) => {
        const res = await fetch(`/prompts/${it.file}`);
        if (!res.ok) throw new Error(`Falha ao carregar ${it.file}`);
        const text = await res.text();
        return { title: it.title, path: it.path, content: text } as Doc;
      })
    )
      .then(setDocs)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div className="landing">
      <header className="landing-header">
        <div className="brand">IA de Ponta a Ponta</div>
        <nav>
          <a href="#/">App</a>
          <a href="#/present">Slider</a>
        </nav>
      </header>

      <section className="hero">
        <div className="hero-text">
          <h1>Do Prompt ao Produto</h1>
          <p>Uma jornada real de desenvolvimento guiada por IAs — do raciocínio aos entregáveis. Prompts versionados, decisões rastreáveis e integração contínua.</p>
          <div className="hero-ctas">
            <a className="btn primary" href="#/present">Ver Slider</a>
            <a className="btn" href="/media/30s.mp4" target="_blank">Ver Vídeo 30s</a>
          </div>
        </div>
        <div className="hero-art">
          <img src="/prints/github.png" alt="Repo" />
        </div>
      </section>

      <section className="features">
        <div className="feature">
          <img src="/prints/claude.png" alt="Claude"/>
          <h3>Orquestração de Código</h3>
          <p>Refino e integração entre camadas com agentes contextuais.</p>
        </div>
        <div className="feature">
          <img src="/prints/perplexity.png" alt="Perplexity"/>
          <h3>Pesquisa com Fontes</h3>
          <p>Coleta estruturada com evidências para corpus e RAG.</p>
        </div>
        <div className="feature">
          <img src="/prints/gemini.png" alt="Gemini"/>
          <h3>Síntese Rápida</h3>
          <p>Resumo e revisão com alternativas gratuitas quando possível.</p>
        </div>
        <div className="feature">
          <img src="/prints/veo3.png" alt="Veo3"/>
          <h3>Mídia em Segundos</h3>
          <p>Vídeos curtos com roteiro e pós‑produção integrada.</p>
        </div>
      </section>

      <section className="prompts">
        <div className="prompts-header">
          <h2>Prompts que movem o projeto</h2>
          <p>Todos versionados, com contexto e rastreabilidade.</p>
        </div>
        {error && <div className="warn">{error}</div>}
        <div className="prompt-grid">
          {docs.slice(0,4).map((doc) => (
            <CodeBlock key={doc.path} doc={doc} />
          ))}
        </div>
        <div className="prompt-grid full">
          {docs.slice(4).map((doc) => (
            <CodeBlock key={doc.path} doc={doc} />
          ))}
        </div>
      </section>

      <section className="stats">
        <div className="stat"><div className="num">98%</div><div className="label">acurácia (proj.)</div></div>
        <div className="stat"><div className="num">60%</div><div className="label">menos dados</div></div>
        <div className="stat"><div className="num">80 ms</div><div className="label">latência de inferência</div></div>
      </section>

      <section className="cta">
        <h2>Prontos para o Hackathon</h2>
        <p>Forme o time, siga as 5 fases e foque na demo. Em 48 horas é possível.</p>
        <div className="hero-ctas">
          <a className="btn primary" href="#/present">Abrir Apresentação</a>
          <a className="btn" href="/prompts/001_prompt_inicial_meta_projeto.md" target="_blank">Ver Prompt Inicial</a>
        </div>
      </section>

      <footer className="landing-footer">
        <div>Workshop IA & Dados — NASA Space Apps SJRP 2025</div>
        <div><a href="#/">Voltar ao app</a></div>
      </footer>
    </div>
  );
}

