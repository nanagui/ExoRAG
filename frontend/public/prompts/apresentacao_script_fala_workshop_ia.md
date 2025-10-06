# Script de Fala — Workshop IA & Dados (Módulo 2)

Duração alvo: 45–60 min. Estilo: prático, ancorado no repositório. Use o arquivo `projeto/apresentacao/mapa_narrativo_repo.md` como guia na tela secundária.

## 0) Abertura (2 min)
- Mensagem: “Hoje vou mostrar como desenvolvi um projeto real e, no caminho, como integrei múltiplas IAs para acelerar cada fase. Tudo está versionado no repositório.”
- Mostrar raiz do repo (pastas): `prompts/`, `contexto/`, `projeto/`, `print_screens/`, `app/`.

## 1) Kickoff & Método (3 min)
- Abrir: `prompts/01-iniciacao/001_prompt_inicial_meta_projeto.md`
- Falar: “Esse é o compromisso com rastreabilidade: toda decisão nasce de um prompt salvo.”
- Abrir: `contexto/metodologia/guia_execucao_prompts.md` (resumo em 30s).

## 2) Contexto do Workshop (3 min)
- Abrir: `contexto/workshop-ia/analise_release_workshop.md` — linha do evento, público, objetivo de reduzir ansiedade antes do hackathon.
- Mensagem: “Esse contexto guia às prioridades de conteúdo e demonstração.”

## 3) Pesquisa Multi‑IA (7 min)
- Abrir: `prompts/02-planejamento/003_pesquisa_desafio_ai_ml.md` (origem das perguntas).
- Mostrar saídas: `contexto/resultado-multi-ais/1/claude/response.md`, `.../chagpt/response.md`, `.../gemini/response.md`, `.../perplexity/1/result.md`.
- Exibir prints: `print_screens/claude.png`, `print_screens/perplexity.png`.
- Mensagem: “Onde convergiram? Onde divergiram? Como decidi?” Apontar para `contexto/resultado-multi-ais/sintese_estrategica_final.md`.

## 4) Arquitetura & Planejamento (8 min)
- Abrir: `app/docs/architecture_overview.md` (diagrama). Conectar caixas aos módulos.
- Abrir: `app/design.md` e `app/tasks.md` (pontos principais, 30s cada).
- Mensagem: “O repositório suporta reprodutibilidade: docs, tasks, onboarding.”

## 5) Desenvolvimento (Código + IA) (12 min)
- Predição end‑to‑end:
  - Abrir: `app/src/app/api/predictions.py` — fluxo preproc → modelo → RAG → resposta (prediction + evidence).
  - Abrir: `app/src/app/rag/pipeline.py` — geração de evidências via retrieval + LLM.
  - Abrir: `app/src/app/data/earthaccess_client.py` — integração com Earthdata (apenas overview).
- Frontend:
  - Abrir: `app/frontend/src/components/LightCurveViewer.tsx` e `.../EvidencePanel.tsx` (o que aparece na UI).
- Qualidade/execução:
  - Abrir: `app/Makefile` (mostrar `make help`).
  - Comentar: `app/tests/**`, `app/.env.example`, `app/docker-compose.yml`.
- Mensagem: “Aqui entra IA de código: Claude/Codex para ajustes entre camadas; Perplexity para corpus; Gemini para sínteses rápidas.”

## 6) Entregáveis (Slides + Vídeo + Paper) (6 min)
- Slides (gamma): `projeto/apresentacao/slides/gamma_meta_projeto_prompt.md` e PDF final `.../NASA-Space-Apps-2025-AI-Solution-for-Exoplanet-Discovery.pdf`.
- Vídeo (Veo3): `projeto/apresentacao/video/veo3_video_roteiro.md` e `projeto/apresentacao/video/30s.mp4` (tocar 15–30s).
- Paper: `projeto/solucao/nasa_space_apps_exoplanet_ai_paper.md` (mostrar título + abstract).
- Prints CapCut/Canva: `print_screens/capcut.png`, `print_screens/canva.png`.

## 7) Demos rápidas (7 min)
- Demo 1 — Contexto vivo: listar `prompts/` e `contexto/` (relacionar 1 prompt→1 decisão no design).
- Demo 2 — Micro‑tarefa Makefile: adicionar `check` (roda lint+typecheck) e `make help`.
- Demo 3 — Síntese com ferramenta gratuita: usar Gemini CLI em um arquivo de `prompts/` (ou fallback `contexto/resultado-multi-ais/1/gemini/response.md`).

## 8) Boas práticas + Riscos (3 min)
- Segredos: usar `app/.env.example`; tokens fora do repo.
- Alucinações: validação humana + cross‑check de fontes; testes pequenos.
- Lock‑in: manter alternativas (Gemini CLI, open‑source local) e outputs versionados.

## 9) Encerramento (2 min)
- CTA: “Forme seu time, use as 5 fases, foque em demo. Em 48 horas é possível.”
- Disponibilize QR: link do repositório e materiais em `contexto/workshop-ia/`.

---

Notas para improviso
- “Sem contexto versionado, cada IA vira silo; com contexto, viram uma orquestra.”
- “Não é sobre a ferramenta perfeita; é sobre acoplar a ferramenta certa à fase certa.”
- “Tudo que mostrei está neste repositório com caminhos claros.”

