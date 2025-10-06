# Demo Runbook — Meta‑Projeto IA de Ponta a Ponta

Objetivo: passo a passo enxuto para executar as demonstrações ao vivo com plano B offline.

Pré‑requisitos locais:
- Terminal com `rg` (ripgrep) instalado ou substitua por `grep -R`.
- Python 3.11+; Docker opcional.
- Acesso às contas: Claude Code/Cursor (IDE), Codex/este agente, gamma.app, Gemini CLI (opcional), Google Veo 3 (opcional), CapCut/Canva (pós‑produção já feita no repo com mp4).
- Segredos fora do versionamento; revisar `app/.env` e usar `app/.env.example` como referência.

---

## Demo 1 — Contexto vivo no repositório (5 min)

1) Mostrar estrutura essencial
- Comando: `rg --files prompts | head -n 10`
- Comando: `rg --files contexto | head -n 10`
- Comando: `rg --files projeto/apresentacao | head -n 20`
- Pontos: encadeamento de fases; cada prompt/output vira ativo reutilizável.

2) Abrir o meta‑prompt inicial
- Caminho: `prompts/01-iniciacao/001_prompt_inicial_meta_projeto.md`
- Dizer: é a âncora do meta‑projeto.

---

## Demo 2 — IA no Código com contexto (7 min)

1) Mostrar alvos de modificação
- Caminho: `app/Makefile`, `app/design.md`, `app/tasks.md`
- Comando: `sed -n '1,120p' app/Makefile | sed -n '1,40p'` (mostrar help e targets principais)

2) Sugerir micro‑tarefa
- Ex.: adicionar target `check` que roda `lint` + `typecheck`.
- Fluxo com agente (Codex/Claude Code): "Ler Makefile + design + tasks e adicionar target `check` mantendo estilo".

3) Executar
- Editar Makefile (ao vivo, com agente) e rodar: `make help`.
- Falar do porquê: agentes leem contexto e respeitam padrões do repo.

---

## Demo 3 — Alternativa gratuita: Gemini CLI (5 min)

Opção A — CLI oficial (se instalado):
- Exemplo (ajuste conforme sua instalação):
  - `gemini prompt --model gemini-1.5-pro "Resuma os pontos-chave de prompts/02-planejamento/003_pesquisa_desafio_ai_ml.md em 5 bullets"`

Opção B — gcloud AI (se configurado):
- `gcloud ai generativelanguage text --model=gemini-1.5-pro --prompt-file=prompts/02-planejamento/003_pesquisa_desafio_ai_ml.md`

Fallback offline (sem rede/conta):
- Caminho: `contexto/resultado-multi-ais/1/gemini/response.md` (mostrar um exemplo já salvo)
- Ponto: como empilhar IAs mantendo rastreabilidade dos resultados.

---

## Demo 4 — Slides no gamma.app 3.0 (4 min)

1) Copiar e colar o prompt
- Arquivo: `projeto/apresentacao/slides/gamma_meta_projeto_prompt.md`
- Ação: abrir gamma.app, colar, gerar; selecionar tema futurista clean.

2) Ajustes rápidos
- Trocar ícones e visuais conforme disponibilidade.
- Exportar/baixar PDF se quiser mostrar offline.

---

## Demo 5 — Vídeo curto (4 min)

1) Roteiro do Veo 3
- Caminho: `projeto/apresentacao/video/veo3_video_roteiro.md`

2) Mostrar resultado
- Caminho: `projeto/apresentacao/video/30s.mp4`
- Falar: partes salvas em `projeto/apresentacao/video/video_partes/` para fallback.

3) Pós‑produção
- CapCut para cortes/legendas; Canva para thumbnail; arquivos finais versionados quando possível.

---

## Dicas de condução
- Tenha sempre uma aba do terminal e outra do editor.
- Nomeie explicitamente os arquivos exibidos (caminho completo) para reforçar rastreabilidade.
- Se algo falhar on‑line, mostre imediatamente a versão salva no repo e explique o porquê do fallback.

---

## Plano B (sem internet)
- Slides: usar PDF pré‑gerado em `projeto/apresentacao/slides/`.
- Vídeo: tocar `projeto/apresentacao/video/30s.mp4` local.
- Conteúdo Gemini/Claude: mostrar saídas já salvas em `contexto/resultado-multi-ais/`.
- Código: demonstrar apenas leitura e navegação, sem dependências externas.

