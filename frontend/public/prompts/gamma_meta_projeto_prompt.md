# Prompt para geração de slides no gamma.app — Workshop IA & Dados (Guilherme Achcar)

Objetivo: criar um deck para o Módulo 2 do Workshop de IA & Dados (NASA Space Apps SJRP 2025), intitulado "IA de Ponta a Ponta: da ideação a solução", com foco em prática, multi‑IA e redução do tempo até a demo.

Contexto do evento (para referência visual/textual em slides 1/rodapé):
- Data: 20/09/2025 — IFSP Rio Preto, Auditório B111
- Público: Participantes e mentores do NASA Space Apps 2025 (SJRP)
- Módulos do workshop: 1) Teoria da Mudança; 2) IA de Ponta a Ponta (esta apresentação); 3) Dados da NASA na prática

Instruções para o gamma.app:
1) Idioma: Português brasileiro, tom prático, encorajador, sem jargão excessivo; destacar ganhos de produtividade.
2) Estilo visual: futurista‑clean; base #0B3D91 (azul escuro), #1B9CFC (azul vivo), branco; ícones minimalistas (IA, código, dados, apresentação). Tipografia legível em telão.
3) Estrutura desejada (14 slides): (incluir em cada slide de conteúdo 1 callout com caminho de arquivo do repo — ver `projeto/apresentacao/mapa_narrativo_repo.md`)
   - Slide 1: Título — "IA de Ponta a Ponta: da ideação a solução"; subtítulo "Workshop IA & Dados — NASA Space Apps SJRP 2025"; linha fina com data/local.
   - Slide 2: Agenda — Ideação; Organização de contexto; Gestão e divisão de tarefas; Desenvolvimento; Apresentação; Demos rápidas; Recursos.
   - Slide 3: Filosofia — reduzir ansiedade pré‑hackathon; foco em prática; "demo acima de slides"; frase central do Guilherme.
   - Slide 4: Framework das 5 fases — diagrama simples (Ideação → Organização → Gestão → Desenvolvimento → Apresentação) com 1 bullet por fase.
   - Slide 5: Multi‑IA por competência — Claude Code, Codex (CLI/Agente), Gemini CLI (free), Perplexity (research), Copilot; quando usar cada uma.
   - Slide 6: Ideação orientada por prompts — exemplos de prompts (2–3 bullets), referência a "guia_execucao_prompts.md"; dica de timeboxing. Callout: `prompts/01-iniciacao/001_prompt_inicial_meta_projeto.md`.
   - Slide 7: Organização de contexto e requisitos — salvando prompts/outputs; estrutura `prompts/` e `contexto/`; template de requisitos. Callout: `contexto/workshop-ia/analise_release_workshop.md`.
   - Slide 8: Gestão e divisão de tarefas — WBS com IA; alocação por perfil; riscos e dependências; checklists. Callout: `app/tasks.md`.
   - Slide 9: Desenvolvimento com IA — geração e refino de código; integração com dados NASA; testes rápidos; boas práticas de validação. Callouts: `app/src/app/api/predictions.py`, `app/src/app/rag/pipeline.py`.
   - Slide 10: Apresentação (pitch) — slides com gamma.app 3.0; script; Q&A; vídeos curtos (Veo 3); pós‑produção (CapCut/Canva).
   - Slide 11: Demos rápidas — 1) navegar no repositório e mostrar contexto vivo; 2) micro‑tarefa no Makefile com agente; 3) síntese com Gemini CLI (free) + fallback. Callouts: `app/Makefile`, `contexto/resultado-multi-ais/gemini/response.md`.
   - Slide 12: Boas práticas e riscos — segredos (.env.example); alucinações; lock‑in; plano B offline (PDF/MP4).
   - Slide 13: Recursos e links — QR para o repositório; materiais em `contexto/workshop-ia/`; contatos/mentoria.
   - Slide 14: Call to action — próximos passos até o hackathon; formar times; validar escopo; construir demo em 48h.
4) Rodapé discreto em todas as páginas: "Workshop IA & Dados — NASA Space Apps SJRP 2025 | Repositório com prompts, contexto e entregáveis".
5) Garantir contraste e legibilidade; priorizar bullets de 1 linha; incluir sugestões de ícones/visuais por slide (usar prints em `print_screens/*.png` quando útil).

Saída esperada: esqueleto completo do deck com títulos, bullets e sugestões visuais para cada slide.
