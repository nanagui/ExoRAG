import { useEffect, useMemo, useState } from 'react';
import { slides, type Slide } from './slidesData';
import useFullscreen from './hooks/useFullscreen';
import MarkdownViewer from './components/MarkdownViewer';
import Carousel from './components/Carousel';
import VideoSegments from './components/VideoSegments';
import PDFViewer from './components/PDFViewer';
import ExternalModal from './components/ExternalModal';
import ImageLightbox from './components/ImageLightbox';

function useKeyNav(onPrev: () => void, onNext: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') onPrev();
      if (e.key === 'ArrowRight' || e.key === ' ') onNext();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onPrev, onNext]);
}

function RepoRefs({ refs, openMarkdown, openImage, openPdf }:
  { refs: string[] | undefined,
    openMarkdown?: (src: string, title?: string) => void,
    openImage?: (src: string, alt?: string) => void,
    openPdf?: (src: string, title?: string) => void }) {
  if (!refs || !refs.length) return null;
  const handleClick = (r: string) => {
    if (r.includes('*')) return; // ignore wildcard refs
    const file = r.split('/').pop() || r;
    const ext = file.toLowerCase().slice(file.lastIndexOf('.'));
    if (ext === '.md' || ext === '.txt') {
      openMarkdown && openMarkdown(`/prompts/${file}`, file);
    } else if (['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'].includes(ext)) {
      openImage && openImage(`/prints/${file}`, file);
    } else if (ext === '.pdf') {
      openPdf && openPdf(`/docs/${file}`, file);
    } else if (ext === '.mp4') {
      try { window.open(`/media/${file}`, '_blank'); } catch {}
    }
  };
  return (
    <div className="slide-refs">
      <strong>Referências (repo):</strong>
      <ul>
        {refs.map((r, i) => (
          <li key={i}>
            <button className="ref-chip" onClick={() => handleClick(r)} title="Abrir">
              <code>{r}</code>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function PromptEmbed({ file, title, pathHint }: { file: string; title?: string; pathHint?: string }) {
  const [text, setText] = useState<string>('');
  const [err, setErr] = useState<string | null>(null);
  useEffect(() => {
    let mounted = true;
    fetch(`/prompts/${file}`)
      .then((r) => (r.ok ? r.text() : Promise.reject(new Error('404'))))
      .then((t) => mounted && setText(t))
      .catch(() => mounted && setErr('Não foi possível carregar o prompt. Rode npm run prepare-media.'));
    return () => { mounted = false; };
  }, [file]);
  return (
    <div className="prompt-embed">
      <div className="prompt-embed-header">
        <span>{title || file}</span>
        <span className="path">{pathHint || `/prompts/${file}`}</span>
      </div>
      {err ? (
        <div className="prompt-error">{err}</div>
      ) : (
        <pre><code>{text}</code></pre>
      )}
    </div>
  );
}

function SlideView({ slide, openMarkdown, openImage, openPdf, openExternal }:
  { slide: Slide,
    openMarkdown?: (src: string, title?: string) => void,
    openImage?: (src: string, alt?: string) => void,
    openPdf?: (src: string, title?: string) => void,
    openExternal?: (url: string, title?: string) => void }) {
  const [imgError, setImgError] = useState(false);
  const layout = slide.layout || 'content';
  if (layout === 'cover') {
    return (
      <div className={"slide slide-cover"}>
        <div className="cover-text">
          <h1 className="slide-title">{slide.title}</h1>
          {slide.subtitle && <h3 className="slide-subtitle">{slide.subtitle}</h3>}
          {slide.bullets && (
            <ul className="slide-bullets">
              {slide.bullets.map((b, i) => (
                <li key={i} dangerouslySetInnerHTML={{ __html: b }} />
              ))}
            </ul>
          )}
          {/* about-me extra actions removidas (abriremos imagem clicável) */}
        </div>
        {slide.image && (
          <div className="cover-image">
            {!imgError ? (
              <img src={slide.image.src} alt={slide.image.alt} onError={() => setImgError(true)} />
            ) : (
              <div className="image-fallback">Imagem sugerida: {slide.image.recommendFromRepo}</div>
            )}
          </div>
        )}
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  if (layout === 'imageRight') {
    return (
      <div className="slide slide-split">
        <div className="split-left">
          <h2 className="slide-title">{slide.title}</h2>
          {slide.subtitle && <h3 className="slide-subtitle">{slide.subtitle}</h3>}
          {slide.body && <p className="slide-body">{slide.body}</p>}
          {slide.bullets && (
            <ul className="slide-bullets">
              {slide.bullets.map((b, i) => (
                <li key={i} dangerouslySetInnerHTML={{ __html: b }} />
              ))}
            </ul>
          )}
          <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
        </div>
        <div className="split-right">
          {slide.image && !imgError ? (
            <img src={slide.image.src} alt={slide.image.alt} onError={() => setImgError(true)} onClick={() => openImage && openImage(slide.image!.src, slide.image!.alt)} style={{ cursor: 'zoom-in' }} />
          ) : (
            slide.image ? <div className="image-fallback">Imagem sugerida: {slide.image.recommendFromRepo}</div> : null
          )}
        </div>
      </div>
    );
  }

  if (layout === 'imageFull' && slide.image) {
    return (
      <div className="slide slide-image-full">
        {!imgError ? (
          <img src={slide.image.src} alt={slide.image.alt} onError={() => setImgError(true)} onClick={() => openImage && openImage(slide.image!.src, slide.image!.alt)} style={{ cursor: 'zoom-in' }} />
        ) : (
          <div className="image-fallback">Imagem sugerida: {slide.image.recommendFromRepo}</div>
        )}
        <div className="image-caption">
          <h2>{slide.title}</h2>
          {slide.subtitle && <p>{slide.subtitle}</p>}
        </div>
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  // Prompt slides by convention (ids mapped to files copied by prepare-media)
  if (slide.id === 'prompt-inicial') {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        <div className="card"><p>Slide removido da sequência.</p></div>
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }
  if (slide.id === 'prompt-gamma') {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        <div className="card"><p>Use o slide “Apresentação — deck (PDF)” para abrir o deck.</p></div>
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }
  if (slide.id === 'prompt-veo3') {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        <div className="card"><p>Use o slide “30 segundos — roteiro (4 partes)” para abrir o roteiro.</p></div>
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  if (slide.id === 'multi-ia-carousel') {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        <Carousel onOpenImage={(src, alt) => openImage && openImage(src, alt)} items={[
          { src:'/prints/claude.png', alt:'Claude' },
          { src:'/prints/chatgpt.png', alt:'ChatGPT' },
          { src:'/prints/gemini.png', alt:'Gemini' },
          { src:'/prints/perplexity.png', alt:'Perplexity' },
        ]} />
        <div style={{ marginTop: '0.5rem' }}>
          <button className="btn" onClick={() => openMarkdown && openMarkdown('/prompts/004_prompts_multiplas_ias_research.md', 'Prompts Multi‑IAs (Research)')}>Ver Prompt Consolidado</button>
        </div>
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  if (slide.id === 'slides-pdf') {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        {slide.bullets && (
          <ul className="slide-bullets">
            {slide.bullets.map((b, i) => (
              <li key={i} dangerouslySetInnerHTML={{ __html: b }} />
            ))}
          </ul>
        )}
        <div className="card" style={{ margin: '0.5rem auto 0', width: 'fit-content' }}>
          <button className="btn" onClick={() => openPdf && openPdf('/docs/NASA-Space-Apps-2025-AI-Solution-for-Exoplanet-Discovery.pdf', 'Deck (PDF)')}>Abrir Deck (PDF)</button>
        </div>
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  if (slide.id === 'video-segments') {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        <VideoSegments />
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  if (slide.cards && slide.cards.length) {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        <div className="card-grid">
          {slide.cards.map((c, i) => (
            <div key={i} className="card-pro">
              {c.icon && <div className="card-icn" aria-hidden>{c.icon}</div>}
              <div className="card-ttl">{c.title}</div>
              <div className="card-txt">{c.text}</div>
            </div>
          ))}
        </div>
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  if (slide.video) {
    return (
      <div className="slide">
        <h2 className="slide-title">{slide.title}</h2>
        {slide.subtitle && <h3 className="slide-subtitle">{slide.subtitle}</h3>}
        <div className="slide-video">
          <video controls preload="metadata" poster={slide.image?.src} style={{ width: '100%', borderRadius: 10 }}>
            <source src={slide.video.src} type="video/mp4" />
          </video>
        </div>
        {slide.bullets && (
          <ul className="slide-bullets">
            {slide.bullets.map((b, i) => (
              <li key={i} dangerouslySetInnerHTML={{ __html: b }} />
            ))}
          </ul>
        )}
        <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
      </div>
    );
  }

  return (
    <div className="slide">
      <h2 className="slide-title">{slide.title}</h2>
      {slide.subtitle && <h3 className="slide-subtitle">{slide.subtitle}</h3>}
      {slide.body && <p className="slide-body">{slide.body}</p>}
      {slide.bullets && (
        <ul className="slide-bullets">
          {slide.bullets.map((b, i) => (
            <li key={i} dangerouslySetInnerHTML={{ __html: b }} />
          ))}
        </ul>
      )}
      {/* Botão explícito para abrir a imagem do LinkedIn em tela cheia */}
      {slide.id === 'about-me' && slide.image && (
        <div className="card" style={{ margin: '0.5rem auto 0', width: 'fit-content' }}>
          <button className="btn" onClick={() => openImage && openImage(slide.image!.src, slide.image!.alt)}>Ver perfil (imagem)</button>
        </div>
      )}
      {slide.promptButton && (
        <div className="card" style={{ margin: '0.5rem auto 0', width: 'fit-content' }}>
          <button
            className="btn"
            onClick={() => openMarkdown && openMarkdown(
              slide.promptButton!.src.startsWith('/prompts') ? slide.promptButton!.src : `/prompts/${slide.promptButton!.src}`,
              slide.promptButton!.title || 'Abrir Prompt'
            )}
          >
            {slide.promptButton.title || 'Abrir Prompt'}
          </button>
        </div>
      )}
      {slide.image && (
        <div className="slide-image">
          {!imgError ? (
            <img
              src={slide.image.src}
              alt={slide.image.alt}
              onError={() => setImgError(true)}
              onClick={() => openImage && openImage(slide.image!.src, slide.image!.alt)}
              style={{ cursor: 'zoom-in' }}
            />
          ) : (
            <div className="image-fallback">
              <div>Imagem sugerida: {slide.image.recommendFromRepo}</div>
            </div>
          )}
        </div>
      )}
      <RepoRefs refs={slide.references} openMarkdown={openMarkdown} openImage={openImage} openPdf={openPdf} />
    </div>
  );
}

export default function SliderPresent() {
  const data = useMemo(() => slides, []);
  const [idx, setIdx] = useState(0);
  const total = data.length;
  const current = data[idx];
  const bgClass = current.background === 'stars' ? 'bg-stars' : current.background === 'grid' ? 'bg-grid' : 'bg-gradient';
  const [assetWarning, setAssetWarning] = useState<string | null>(null);
  const [overview, setOverview] = useState(false);
  const [mdOpen, setMdOpen] = useState<{open: boolean, src: string, title?: string}>({open:false, src:''});
  const { toggle: toggleFs } = useFullscreen();
  const [isFs, setIsFs] = useState(false);
  const [imgOpen, setImgOpen] = useState<{open:boolean, src:string, alt?:string}>({open:false, src:''});
  const [pdfOpen, setPdfOpen] = useState<{open:boolean, src:string, title?:string}>({open:false, src:''});
  const [extOpen, setExtOpen] = useState<{open:boolean, url:string, title?:string}>({open:false, url:''});

  useEffect(() => {
    // quick asset existence check; displays a hint if prints are missing
    const probe = async () => {
      try {
        const res = await fetch('/prints/github.png', { method: 'HEAD' });
        if (!res.ok) throw new Error('missing');
      } catch (_) {
        setAssetWarning('Imagens não encontradas. Rode: npm run dev (copia mídias) ou npm run prepare-media');
      }
    };
    probe();
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'f') toggleFs();
      if (e.key.toLowerCase() === 'o') setOverview((v) => !v);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [toggleFs]);

  useEffect(() => {
    const onFs = () => {
      const d: any = document;
      const active = !!(d.fullscreenElement || d.webkitFullscreenElement);
      setIsFs(active);
    };
    document.addEventListener('fullscreenchange', onFs);
    // @ts-ignore
    document.addEventListener('webkitfullscreenchange', onFs);
    return () => {
      document.removeEventListener('fullscreenchange', onFs);
      // @ts-ignore
      document.removeEventListener('webkitfullscreenchange', onFs);
    };
  }, []);

  const prev = () => setIdx((i) => Math.max(0, i - 1));
  const next = () => setIdx((i) => Math.min(total - 1, i + 1));

  useKeyNav(prev, next);

  return (
    <div className={`present-container ${bgClass} ${isFs ? 'is-full' : ''}`}>
      <header className="present-header">
        <div className="brand">Workshop IA & Dados — Apresentação</div>
        <nav className="present-nav" style={{ display:'flex', gap: '10px' }}>
          <button className="btn" onClick={() => setOverview((v)=>!v)}>Overview</button>
          <button className="btn" onClick={() => toggleFs()}>Tela cheia</button>
          <a href="#/">Voltar ao app</a>
        </nav>
      </header>
      <main className="present-main">
        <SlideView
          key={current.id}
          slide={current}
          openMarkdown={(src, title) => setMdOpen({ open:true, src, title })}
          openImage={(src, alt) => setImgOpen({ open: true, src, alt })}
          openPdf={(src, title) => setPdfOpen({ open:true, src, title })}
          openExternal={(url, title) => setExtOpen({ open:true, url, title })}
        />
      </main>
      <footer className="present-footer">
        <div className="progress">{idx + 1} / {total}</div>
        <div className="controls">
          <button onClick={prev} disabled={idx === 0}>&larr; Anterior</button>
          <button onClick={next} disabled={idx === total - 1}>Próximo &rarr;</button>
        </div>
        <div className="tip">Dica: use ← → ou espaço para navegar</div>
      </footer>
      {assetWarning && (
        <div className="present-toast" role="status">{assetWarning}</div>
      )}
      {overview && (
        <div className="overlay" onClick={() => setOverview(false)}>
          <div className="overlay-card" onClick={(e) => e.stopPropagation()}>
            <div className="overlay-header"><div className="title">Overview</div><button onClick={() => setOverview(false)}>Fechar</button></div>
            <div className="overview-grid">
              {data.map((s, i) => (
                <button key={s.id} className={i===idx? 'thumb active':'thumb'} onClick={() => { setIdx(i); setOverview(false); }}>
                  <div className="thumb-title">{s.title}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
      <MarkdownViewer src={mdOpen.src} title={mdOpen.title} open={mdOpen.open} onClose={() => setMdOpen({open:false, src:''})} />
      <PDFViewer src={pdfOpen.src} title={pdfOpen.title} open={pdfOpen.open} onClose={() => setPdfOpen({ open:false, src:'' })} />
      <ExternalModal url={extOpen.url} title={extOpen.title} open={extOpen.open} onClose={() => setExtOpen({ open:false, url:'' })} />
      <ImageLightbox src={imgOpen.src} alt={imgOpen.alt} open={imgOpen.open} onClose={() => setImgOpen({ open:false, src:'' })} />
    </div>
  );
}
