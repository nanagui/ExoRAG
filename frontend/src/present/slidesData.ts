export type Slide = {
  id: string;
  title: string;
  subtitle?: string;
  bullets?: string[];
  body?: string;
  references?: string[]; // repo paths
  image?: {
    src: string; // expected under /prints/* (frontend public). Falls back to showing path if missing.
    alt: string;
    recommendFromRepo?: string; // original path in repo (e.g., print_screens/claude.png)
  };
  video?: {
    src: string; // /media/*.mp4
    poster?: string;
  };
  cards?: { title: string; text: string; icon?: string }[];
  promptButton?: { src: string; title?: string };
  layout?: 'cover' | 'content' | 'imageRight' | 'imageFull';
  background?: 'stars' | 'grid' | 'gradient';
};

export const slides: Slide[] = [
  // 1) Capa
  {
    id: 'cover',
    title: 'IA de Ponta a Ponta',
    subtitle: 'Do prompt ao produto — NASA Space Apps',
    bullets: [
      'Mostraremos, na prática, o uso de múltiplas IAs',
      'Do zero até um entregável forte e explicável',
      'Com referências reais do repositório'
    ],
    references: [
      'projeto/apresentacao/slides/gamma_meta_projeto_prompt.md',
      'projeto/apresentacao/video/30s.mp4'
    ],
    image: { src: '/prints/github.png', alt: 'Estrutura do repositório', recommendFromRepo: 'print_screens/github.png' },
    layout: 'cover',
    background: 'stars'
  },
  // 2) Quem sou eu?
  {
    id: 'about-me',
    title: 'Quem sou eu?',
    bullets: [
      'Guilherme Janku Achcar — IA, produto e comunidade',
      'Local Lead Space Apps; cofundador IA Rio Preto',
      'Missão: tornar IA e dados acessíveis'
    ],
    references: [
      'contexto/workshop-ia/analise_release_workshop.md',
      'contexto/Resume_Achcar_Guilherme_07_2025.pdf'
    ],
    image: { src: '/prints/linkedin.png', alt: 'Perfil LinkedIn — Guilherme Achcar', recommendFromRepo: 'print_screens/linkedin.png' },
    background: 'grid'
  },
  // 3) Objetivo da apresentação
  {
    id: 'objective',
    title: 'Objetivo da apresentação',
    bullets: [
      'IA ponta a ponta no desafio Space Apps',
      'Ideação → Organização → Gestão → Desenvolvimento → Apresentação',
      'Exemplos, prompts e mídia reais do repositório'
    ],
    references: [
      'projeto/apresentacao/mapa_narrativo_repo.md',
      'contexto/metodologia/guia_execucao_prompts.md'
    ],
    background: 'gradient'
  },
  // 4) Escolha do desafio e estratégia
  {
    id: 'challenge-selection',
    title: 'Escolha do desafio e estratégia',
    bullets: [
      'Match com perfil: IA/ML + produto + entregáveis rápidos',
      'Estratégia: valor rápido, explicável e com evidências',
      'Exemplos alinhados ao histórico e ao tempo do evento'
    ],
    references: [
      'contexto/workshop-ia/analise_release_workshop.md',
      'contexto/resultado-multi-ais/sintese_estrategica_final.md'
    ],
    promptButton: { src: '002_analise_perfil_desafios_nasa.md', title: 'Prompt — análise de desafios' },
    background: 'grid'
  },
  // 5) Desafio escolhido (resultado do prompt)
  {
    id: 'challenge-picked',
    title: 'Desafio escolhido',
    bullets: [
      'IA & Machine Learning — foco em explicabilidade',
      'Match com perfil + entregáveis práticos em 48h',
      'Baseado na análise dos desafios (prompt)'
    ],
    references: [
      'contexto/workshop-ia/recomendacoes_desafios_2025.md',
      'print_screens/desafio.png'
    ],
    image: { src: '/prints/desafio.png', alt: 'Desafio selecionado — captura', recommendFromRepo: 'print_screens/desafio.png' },
    layout: 'imageRight',
    background: 'grid'
  },
  // 5) Contexto do desafio
  {
    id: 'challenge-context',
    title: 'Contexto do desafio escolhido',
    bullets: [
      'Problema, oportunidade e critérios de avaliação',
      'Explicação acessível; analogias quando útil',
      'Como diferentes IAs se complementam'
    ],
    references: [
      'contexto/workshop-ia/contexto_completo_desafio_ai_ml.md'
    ],
    background: 'gradient'
  },
  // 6) Carrossel Multi‑IAs
  {
    id: 'multi-ia-carousel',
    title: 'Carrossel — resultados de múltiplas IAs',
    bullets: [
      'Navegue: Claude, ChatGPT, Gemini, Perplexity',
      'Sínteses, riscos e convergências',
      'Abra o prompt consolidado de pesquisa'
    ],
    references: [
      'contexto/resultado-multi-ais/1/*',
      'contexto/resultado-multi-ais/sintese_estrategica_final.md',
      'prompts/03-desenvolvimento/004_prompts_multiplas_ias_research.md'
    ],
    background: 'gradient'
  },
  
  // 7) Decisão da solução
  {
    id: 'decision',
    title: 'Decisão da solução',
    bullets: [
      'Brainstorm guiado por IA → ideias em minutos',
      'Critérios: tempo, explicabilidade, evidências',
      'Solução híbrida com RAG e justificativas citáveis'
    ],
    references: [
      'contexto/resultado-multi-ais/sintese_estrategica_final.md',
      'app/docs/architecture_overview.md'
    ],
    background: 'grid'
  },
  {
    id: 'decision',
    title: 'Decisão da solução',
    bullets: [
      'Brainstorm guiado por IA → ideias em minutos',
      'Critérios: tempo, explicabilidade, evidências',
      'Solução híbrida com RAG e justificativas citáveis'
    ],
    references: [
      'contexto/resultado-multi-ais/sintese_estrategica_final.md',
      'app/docs/architecture_overview.md'
    ],
    background: 'grid'
  },
  {
    id: 'project-plan',
    title: 'Plano de gestão do projeto',
    bullets: [
      'WBS, dependências e riscos com ajuda de IA',
      'Entregáveis Space Apps: repo, descrição, vídeo, slides, demo',
      'Runbook para demos e contingência'
    ],
    references: [
      'app/tasks.md',
      'projeto/apresentacao/demo_runbook_meta_projeto.md',
      'projeto/apresentacao/slides/NASA-Space-Apps-2025-AI-Solution-for-Exoplanet-Discovery.pdf'
    ],
    background: 'gradient'
  },
  {
    id: 'hands-on',
    title: 'Mão na massa — descrição do projeto',
    bullets: [
      'Paper: estrutura (sem resultados finais)',
      'Protótipo: foco no essencial',
      'Vídeo: planejado desde o início'
    ],
    references: [
      'projeto/solucao/nasa_space_apps_exoplanet_ai_paper.md',
      'app/docs/architecture_overview.md'
    ],
    background: 'grid'
  },
  {
    id: 'dev-coding',
    title: 'Desenvolvimento — programando com IA',
    bullets: [
      'Micro‑tarefas com contexto (Claude Code, Codex, Cursor)',
      'Antes → Depois de um trecho real',
      'Prompt curto com caminho de arquivo'
    ],
    references: [
      'app/src/app/api/predictions.py',
      'app/src/app/rag/pipeline.py',
      'app/src/app/models/architecture.py'
    ],
    background: 'grid',
    promptButton: { src: 'prompts_prontos_para_executar.md', title: 'Prompt — micro‑tarefa' }
  },
  {
    id: 'dev-rag',
    title: 'Desenvolvimento — RAG e evidências',
    bullets: [
      'Pergunta → retrieval → resposta com citações',
      'Menos “alucinações”, mais confiança',
      'Arquitetura simples de manter'
    ],
    references: [
      'app/src/app/rag/pipeline.py',
      'app/src/app/rag/retriever.py',
      'app/src/app/rag/indexer.py'
    ],
    background: 'gradient'
  },
  {
    id: 'slides-build',
    title: 'Apresentação de slides',
    bullets: [
      'Gamma.app para estrutura',
      'Beautiful.ai para polimento visual',
      'Manus.im para automação (quando fizer sentido)'
    ],
    references: ['projeto/apresentacao/slides/gamma_meta_projeto_prompt.md'],
    background: 'grid',
    promptButton: { src: 'gamma_meta_projeto_prompt.md', title: 'Prompt — deck (gamma.app)' }
  },
  {
    id: 'slides-pdf',
    title: 'Apresentação — deck (PDF)',
    bullets: [
      'Abra o PDF do deck gerado',
      'Ideal para leitura rápida ou envio ao time'
    ],
    references: ['projeto/apresentacao/slides/NASA-Space-Apps-2025-AI-Solution-for-Exoplanet-Discovery.pdf'],
    background: 'grid'
  },
  {
    id: 'multi-ia-carousel',
    title: 'Multi‑IAs — telas e prompts',
    bullets: [
      'Navegue pelas telas das ferramentas',
      'Abra o prompt consolidado de pesquisa (multi‑IAs)'
    ],
    references: [
      'print_screens/claude.png',
      'print_screens/chatgpt.png',
      'print_screens/gemini.png',
      'print_screens/perplexity.png',
      'prompts/03-desenvolvimento/004_prompts_multiplas_ias_research.md'
    ],
    background: 'gradient'
  },
  
  // 13) Roteiro em 4 partes (vídeos)
  {
    id: 'video-segments',
    title: '30 segundos de glória — roteiro (4 partes)',
    bullets: [
      '4 segmentos para demonstrar a narrativa',
      'Cada parte com seu trecho do roteiro Veo3',
      'Botão para abrir o roteiro completo'
    ],
    references: [
      'projeto/apresentacao/video/video_partes/part1.mp4',
      'projeto/apresentacao/video/video_partes/part2.mp4',
      'projeto/apresentacao/video/video_partes/part3.mp4',
      'projeto/apresentacao/video/video_partes/part4.mp4',
      'projeto/apresentacao/video/veo3_video_roteiro.md'
    ],
    background: 'grid'
  },
  // 14) Vídeo final 30s
  {
    id: 'slides-video',
    title: '30 segundos — vídeo final',
    bullets: [
      'Compilado no CapCut/Canva',
      'Resultado da narrativa em 4 partes',
      'Feito para palco e redes'
    ],
    references: [
      'projeto/apresentacao/video/30s.mp4',
      'print_screens/capcut.png',
      'print_screens/canva.png'
    ],
    video: { src: '/media/30s.mp4' },
    image: { src: '/prints/veo3.png', alt: 'Veo3', recommendFromRepo: 'print_screens/veo3.png' },
    layout: 'content',
    background: 'grid'
  },
  {
    id: 'prompt-recipes',
    title: 'Receitas de Prompt (exemplos úteis)',
    bullets: [
      '“Leia estes arquivos e proponha…” (citar caminhos completos)',
      '“Aplique mudança X mantendo estilo e convenções do projeto”',
      '“Gere slides (gamma) com estas seções e visuais”',
      '“Escreva roteiro de vídeo 30s com 4 cenas (Veo3)”',
      '“Faça revisão crítica e liste riscos/mitigações”'
    ],
    references: [
      'prompts/03-desenvolvimento/prompts_prontos_para_executar.md',
      'projeto/apresentacao/video/veo3_video_roteiro.md',
      'projeto/apresentacao/slides/gamma_meta_projeto_prompt.md'
    ],
    background: 'gradient'
  },
  {
    id: 'risks',
    title: 'Riscos e Mitigações (IA aplicada)',
    bullets: [
      'Hallucinations: RAG + checagem manual + fontes citadas',
      'Deriva de contexto: âncoras por caminho de arquivo',
      'Lock‑in: alternativas (Gemini CLI, OSS) e outputs versionados',
      'Segurança: tokens fora do repo; rotação de credenciais'
    ],
    references: [
      'contexto/metodologia/guia_execucao_prompts.md',
      'app/.env.example'
    ],
    background: 'grid'
  },
  {
    id: 'demos',
    title: 'Demos (para “mão na massa”)',
    bullets: [
      'Contexto vivo: prompts/ + contexto/ → decisão no design',
      'Micro‑tarefa Makefile: target `check` (lint+typecheck)',
      'Síntese “free”: Gemini CLI + fallback salvo',
      'Slides/vídeo: gamma 3.0 + MP4 30s'
    ],
    references: [
      'projeto/apresentacao/demo_runbook_meta_projeto.md'
    ],
    background: 'gradient'
  },
  {
    id: 'cta',
    title: 'Próximos Passos (Hackathon)',
    bullets: [
      'Formem times e definam a Teoria da Mudança (Módulo 1)',
      'Apliquem as 5 fases com multi‑IA (este módulo)',
      'Usem dados NASA (Módulo 3) e busquem evidências',
      'Foquem em demo funcional em 48h'
    ],
    references: [
      'contexto/workshop-ia/roteiro_apresentacao.md'
    ],
    background: 'stars'
  },
  {
    id: 'assets',
    title: 'Imagens e Mídia — onde usar cada uma',
    bullets: [
      'Claude (orquestração de código): /prints/claude.png',
      'ChatGPT (análises comparativas): /prints/chatgpt.png',
      'Gemini (sínteses rápidas): /prints/gemini.png',
      'Perplexity (pesquisa com fontes): /prints/perplexity.png',
      'GitHub (visão do repo): /prints/github.png',
      'Veo 3 (geração de vídeo): /prints/veo3.png',
      'CapCut (edição): /prints/capcut.png; Canva (thumb): /prints/canva.png'
    ],
    references: [
      'print_screens/claude.png',
      'print_screens/chatgpt.png',
      'print_screens/gemini.png',
      'print_screens/perplexity.png',
      'print_screens/github.png',
      'print_screens/veo3.png',
      'print_screens/capcut.png',
      'print_screens/canva.png'
    ]
  },
  // 15) Conclusão
  {
    id: 'conclusion',
    title: 'Conclusão e próximos passos',
    bullets: [
      'IA como parceira: método > improviso',
      'Decisões ancoradas, evidências citáveis',
      'Abrir, coletar feedback, iterar'
    ],
    references: [
      'projeto/apresentacao/apresentacao_script_fala_workshop_ia.md',
      'projeto/apresentacao/mapa_narrativo_repo.md'
    ],
    background: 'stars'
  }
];
