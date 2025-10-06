import { useEffect, useMemo, useState } from 'react';

type Props = {
  src: string; // e.g. /prompts/xxx.md
  title?: string;
  open: boolean;
  onClose: () => void;
};

export default function MarkdownViewer({ src, title, open, onClose }: Props) {
  const [raw, setRaw] = useState<string>('');
  const [err, setErr] = useState<string | null>(null);
  const [scale, setScale] = useState<number>(1);

  useEffect(() => {
    if (!open) return;
    fetch(src)
      .then((r) => (r.ok ? r.text() : Promise.reject(new Error(`Falha ao carregar ${src}`))))
      .then((t) => {
        // Detect SPA fallback (index.html) and show guidance instead of raw HTML
        const lower = t.trim().toLowerCase();
        if (lower.startsWith('<!doctype') || lower.includes('<html')) {
          setErr('Arquivo não encontrado no public. Rode: npm run prepare-media');
          setRaw('');
          return;
        }
        setRaw(t); setErr(null);
      })
      .catch((e) => setErr(e.message));
  }, [src, open]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!open) return;
      if (e.key === 'Escape') onClose();
      if (e.key === '+') setScale((s) => Math.min(2, s + 0.1));
      if (e.key === '-') setScale((s) => Math.max(0.6, s - 0.1));
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  const html = useMemo(() => {
    // render markdown with a trivial converter to avoid extra deps
    // headings, code blocks and lists handled in a minimal way
    const escape = (s: string) => s.replace(/[&<>]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c] as string));
    const lines = raw.split(/\r?\n/);
    const out: string[] = [];
    let inCode = false;
    lines.forEach((ln) => {
      if (ln.trim().startsWith('```')) { inCode = !inCode; out.push(inCode ? '<pre><code>' : '</code></pre>'); return; }
      if (inCode) { out.push(escape(ln)); return; }
      if (/^#\s+/.test(ln)) out.push(`<h1>${escape(ln.replace(/^#\s+/, ''))}</h1>`);
      else if (/^##\s+/.test(ln)) out.push(`<h2>${escape(ln.replace(/^##\s+/, ''))}</h2>`);
      else if (/^\-\s+/.test(ln)) out.push(`<li>${escape(ln.replace(/^\-\s+/, ''))}</li>`);
      else if (ln.trim() === '') out.push('<br/>');
      else out.push(`<p>${escape(ln)}</p>`);
    });
    // wrap list items into a ul
    return out.join('\n').replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>');
  }, [raw]);

  if (!open) return null;

  return (
    <div className="overlay" onClick={onClose}>
      <div className="overlay-card" onClick={(e) => e.stopPropagation()}>
        <div className="overlay-header">
          <div className="title">{title || src}</div>
          <div className="actions">
            <button onClick={() => setScale((s) => Math.max(0.6, s - 0.1))}>-</button>
            <button onClick={() => setScale((s) => Math.min(2, s + 0.1))}>+</button>
            <button onClick={onClose}>Fechar</button>
          </div>
        </div>
        {err ? (
          <div className="prompt-error" style={{ margin: '0.75rem' }}>{err}</div>
        ) : (
          <div className="overlay-body" style={{ transform: `scale(${scale})`, transformOrigin: '0 0' }}>
            <div className="markdown" dangerouslySetInnerHTML={{ __html: html }} />
          </div>
        )}
      </div>
    </div>
  );
}
