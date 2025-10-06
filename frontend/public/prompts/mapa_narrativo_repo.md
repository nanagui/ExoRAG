# Mapa Narrativo do Repositório — Workshop IA & Dados (Guilherme Achcar)

Objetivo: contar a história do desenvolvimento do projeto como exemplo, mostrando onde cada artefato vive no repo e como as IAs entraram em cada fase.

## Visão de Raiz (pastas → propósito)
- `prompts/` — histórico dos prompts por fase do projeto (fonte de verdade do raciocínio).
- `contexto/` — análises, sínteses, estudos e resultados de múltiplas IAs (apoio e referências).
- `projeto/` — entregáveis finais de apresentação (slides, roteiros de vídeo, PDF, MP4).
- `print_screens/` — telas de ferramentas usadas (Claude, ChatGPT, Gemini, Perplexity, Veo3, CapCut, Canva).
- `app/` — código da solução (API FastAPI, ML, RAG, frontend, docs, testes).

---

## Fase 0 — Kickoff e Método
- Prompt âncora do processo: `prompts/01-iniciacao/001_prompt_inicial_meta_projeto.md`
  - Define: salvar tudo (prompts/outputs), estruturar contexto, construir apresentação a partir do trabalho real.
- Guia de execução de prompts: `contexto/metodologia/guia_execucao_prompts.md`

Como mostrar:
- Exibir rapidamente `001_prompt_inicial_meta_projeto.md` e explicar o porquê de versionar prompts.

---

## Fase 1 — Contexto do Workshop e Objetivos
- Release analisado: `contexto/250916 Release_WorkshopIA.pdf`
- Análise do release: `contexto/workshop-ia/analise_release_workshop.md`
- Roteiro do workshop (macro): `contexto/workshop-ia/roteiro_apresentacao.md`

Como mostrar:
- Abrir `analise_release_workshop.md` (dados do evento, público, módulos) e ligar à sua fala.

---

## Fase 2 — Pesquisa & Direcionamento (Multi‑IA)
- Planejamento inicial: `prompts/02-planejamento/002_analise_perfil_desafios_nasa.md`, `.../003_pesquisa_desafio_ai_ml.md`
- Saídas multi‑IA: `contexto/resultado-multi-ais/1/claude/response.md`, `.../chagpt/response.md`, `.../gemini/response.md`, `.../perplexity/**`
- Síntese final: `contexto/resultado-multi-ais/sintese_estrategica_final.md`
- Prints das ferramentas: `print_screens/claude.png`, `.../chatgpt.png`, `.../gemini.png`, `.../perplexity.png`

Como mostrar:
- Destacar 1–2 achados que se repetem entre IAs (consistência) e 1 divergência (onde você decidiu).

---

## Fase 3 — Arquitetura e Planejamento da Solução
- Design e tarefas: `app/design.md`, `app/tasks.md`
- Visão de arquitetura: `app/docs/architecture_overview.md`
- Onboarding dev: `app/docs/onboarding.md`
- Requisitos/stack: `app/requirements.md`, `app/requirements.txt`

Como mostrar:
- Abrir `architecture_overview.md` (diagrama) e conectar com os módulos do código.

---

## Fase 4 — Desenvolvimento (Código + IA)
- API/entrypoint: `app/src/app/main.py`
- Predição: `app/src/app/api/predictions.py`
- RAG/evidências: `app/src/app/rag/pipeline.py`, `.../retriever.py`, `.../indexer.py`
- Dados NASA: `app/src/app/data/earthaccess_client.py`, `.../ingestion.py`
- Preprocessamento: `app/src/app/preprocessing/pipeline.py`, `.../validation.py`
- Modelagem: `app/src/app/models/architecture.py`, `.../module.py`, `.../losses.py`
- Baseline: `app/src/app/baselines/random_forest.py`
- Frontend (plotly/React): `app/frontend/src/components/LightCurveViewer.tsx`, `.../EvidencePanel.tsx`
- Qualidade: `app/Makefile`, `app/tests/**`
- Execução: `app/docker-compose.yml`, `app/Dockerfile`, `app/.env.example`

Como mostrar:
- Navegar pelo `predictions.py` (fluxo de preproc→modelo→RAG) e conectar com o diagrama.
- Mostrar `Makefile` (`make help`) e um teste alvo.

Onde as IAs entram aqui:
- Claude/Codex: refino de módulos e colagem entre camadas.
- Perplexity: papers/datasets para corpus RAG.
- Gemini (free): síntese de docs e prompts auxiliares.

---

## Fase 5 — Entregáveis de Apresentação
- Slides (prompt): `projeto/apresentacao/slides/gamma_meta_projeto_prompt.md`
- Slides (PDF): `projeto/apresentacao/slides/NASA-Space-Apps-2025-AI-Solution-for-Exoplanet-Discovery.pdf`
- Vídeo (Veo3): `projeto/apresentacao/video/veo3_video_roteiro.md`, `projeto/apresentacao/video/30s.mp4`
- Paper: `projeto/solucao/nasa_space_apps_exoplanet_ai_paper.md`
- Prints de pós‑produção: `print_screens/capcut.png`, `print_screens/canva.png`, `print_screens/veo3.png`

Como mostrar:
- Abrir o prompt do gamma e o PDF final para provar reuso do conteúdo técnico.
- Tocar o MP4 de 30s como demo curta.

---

## Demos (comprovando o caminho)
1) Contexto vivo → decisão
- Mostrar `prompts/` e `contexto/` lado a lado; conectar um prompt a uma síntese e a uma decisão no design.

2) Código com agente
- Micro‑tarefa no `app/Makefile` (ex.: target `check` encadeando `lint`+`typecheck`) e rodar `make help`.

3) Pipeline de explicação
- Abrir `app/src/app/api/predictions.py` e `app/src/app/rag/pipeline.py`; explicar como a resposta retorna `prediction + evidence`.

4) Slides/vídeo
- Colar `projeto/apresentacao/slides/gamma_meta_projeto_prompt.md` no gamma; abrir `30s.mp4`.

---

## Links rápidos (referências na fala)
- prompts/01-iniciacao/001_prompt_inicial_meta_projeto.md
- contexto/workshop-ia/analise_release_workshop.md
- contexto/resultado-multi-ais/sintese_estrategica_final.md
- app/docs/architecture_overview.md
- app/src/app/api/predictions.py
- app/src/app/rag/pipeline.py
- app/Makefile
- projeto/apresentacao/slides/gamma_meta_projeto_prompt.md
- projeto/apresentacao/video/30s.mp4

