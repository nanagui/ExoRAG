/* Copy print assets from repo root `print_screens/` into frontend `public/prints/` */
const fs = require('fs');
const path = require('path');

function ensureDir(p) {
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
}

function copyIfNewer(src, dst) {
  try {
    const s = fs.statSync(src);
    try {
      const d = fs.statSync(dst);
      if (s.mtimeMs <= d.mtimeMs) return; // up to date
    } catch (_) {}
    fs.copyFileSync(src, dst);
    // eslint-disable-next-line no-console
    console.log(`[prepare-media] Copied ${path.basename(src)}`);
  } catch (e) {
    // ignore if source missing
  }
}

const repoRoot = path.resolve(__dirname, '../../..');
const srcDir = path.join(repoRoot, 'print_screens');
const dstDir = path.join(__dirname, '..', 'public', 'prints');

ensureDir(dstDir);

const candidates = [
  'claude.png',
  'chatgpt.png',
  'gemini.png',
  'perplexity.png',
  'github.png',
  'veo3.png',
  'veo3-2.png',
  'capcut.png',
  'canva.png',
  'linkedin.png',
  'desafio.png'
];

candidates.forEach((name) => {
  const s = path.join(srcDir, name);
  const d = path.join(dstDir, name);
  copyIfNewer(s, d);
});

// Copy demo video (optional)
const videoSrc = path.join(repoRoot, 'projeto', 'apresentacao', 'video', '30s.mp4');
const videoDstDir = path.join(__dirname, '..', 'public', 'media');
ensureDir(videoDstDir);
copyIfNewer(videoSrc, path.join(videoDstDir, '30s.mp4'));

// Copy segmented videos if available
const partsDir = path.join(repoRoot, 'projeto', 'apresentacao', 'video', 'video_partes');
['part1.mp4', 'part2.mp4', 'part3.mp4', 'part4.mp4'].forEach((name) => {
  const s = path.join(partsDir, name);
  const d = path.join(videoDstDir, name);
  copyIfNewer(s, d);
});

// Copy selected prompts for LandingPresent
const promptsMap = [
  { src: path.join(repoRoot, 'prompts', '01-iniciacao', '001_prompt_inicial_meta_projeto.md'), dst: '001_prompt_inicial_meta_projeto.md' },
  { src: path.join(repoRoot, 'prompts', '02-planejamento', '002_analise_perfil_desafios_nasa.md'), dst: '002_analise_perfil_desafios_nasa.md' },
  { src: path.join(repoRoot, 'prompts', '02-planejamento', '003_pesquisa_desafio_ai_ml.md'), dst: '003_pesquisa_desafio_ai_ml.md' },
  { src: path.join(repoRoot, 'prompts', '03-desenvolvimento', '004_prompts_multiplas_ias_research.md'), dst: '004_prompts_multiplas_ias_research.md' },
  { src: path.join(repoRoot, 'prompts', '03-desenvolvimento', '005_prompt_sintese_final_research.md'), dst: '005_prompt_sintese_final_research.md' },
  { src: path.join(repoRoot, 'prompts', '03-desenvolvimento', 'prompts_prontos_para_executar.md'), dst: 'prompts_prontos_para_executar.md' },
  { src: path.join(repoRoot, 'projeto', 'apresentacao', 'slides', 'gamma_meta_projeto_prompt.md'), dst: 'gamma_meta_projeto_prompt.md' },
  { src: path.join(repoRoot, 'projeto', 'apresentacao', 'video', 'veo3_video_roteiro.md'), dst: 'veo3_video_roteiro.md' },
  // Contextos citados diretamente
  { src: path.join(repoRoot, 'contexto', 'workshop-ia', 'recomendacoes_desafios_2025.md'), dst: 'recomendacoes_desafios_2025.md' },
  { src: path.join(repoRoot, 'contexto', 'workshop-ia', 'contexto_completo_desafio_ai_ml.md'), dst: 'contexto_completo_desafio_ai_ml.md' },
  { src: path.join(repoRoot, 'contexto', 'workshop-ia', 'analise_release_workshop.md'), dst: 'analise_release_workshop.md' },
  { src: path.join(repoRoot, 'contexto', 'resultado-multi-ais', 'sintese_estrategica_final.md'), dst: 'sintese_estrategica_final.md' },
  { src: path.join(repoRoot, 'contexto', 'metodologia', 'guia_execucao_prompts.md'), dst: 'guia_execucao_prompts.md' },
  // Documentos do projeto citados
  { src: path.join(repoRoot, 'projeto', 'apresentacao', 'mapa_narrativo_repo.md'), dst: 'mapa_narrativo_repo.md' },
  { src: path.join(repoRoot, 'projeto', 'apresentacao', 'apresentacao_script_fala_workshop_ia.md'), dst: 'apresentacao_script_fala_workshop_ia.md' },
  { src: path.join(repoRoot, 'projeto', 'apresentacao', 'demo_runbook_meta_projeto.md'), dst: 'demo_runbook_meta_projeto.md' },
  { src: path.join(repoRoot, 'projeto', 'solucao', 'nasa_space_apps_exoplanet_ai_paper.md'), dst: 'nasa_space_apps_exoplanet_ai_paper.md' },
  { src: path.join(repoRoot, 'app', 'docs', 'architecture_overview.md'), dst: 'architecture_overview.md' },
  { src: path.join(repoRoot, 'app', 'tasks.md'), dst: 'tasks.md' }
];

const promptsDst = path.join(__dirname, '..', 'public', 'prompts');
ensureDir(promptsDst);
promptsMap.forEach(({ src, dst }) => copyIfNewer(src, path.join(promptsDst, dst)));

// Presenter notes
const notesSrc = path.join(repoRoot, 'projeto', 'apresentacao', 'apresentacao_script_fala_workshop_ia.md');
const notesDstDir = path.join(__dirname, '..', 'public', 'notes');
ensureDir(notesDstDir);
copyIfNewer(notesSrc, path.join(notesDstDir, 'presenter_notes.md'));

// Copy slides PDF
const pdfSrc = path.join(repoRoot, 'projeto', 'apresentacao', 'slides', 'NASA-Space-Apps-2025-AI-Solution-for-Exoplanet-Discovery.pdf');
const pdfDstDir = path.join(__dirname, '..', 'public', 'docs');
ensureDir(pdfDstDir);
copyIfNewer(pdfSrc, path.join(pdfDstDir, 'NASA-Space-Apps-2025-AI-Solution-for-Exoplanet-Discovery.pdf'));
// Copy Resume PDF (about-me)
copyIfNewer(path.join(repoRoot, 'contexto', 'Resume_Achcar_Guilherme_07_2025.pdf'), path.join(pdfDstDir, 'Resume_Achcar_Guilherme_07_2025.pdf'));
