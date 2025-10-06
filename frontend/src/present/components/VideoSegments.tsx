import { useEffect, useState } from 'react';
import MarkdownViewer from './MarkdownViewer';

type Segment = { file: string; label: string };

const DEFAULT_SEGMENTS: Segment[] = [
  { file: '/media/part1.mp4', label: 'Parte 1' },
  { file: '/media/part2.mp4', label: 'Parte 2' },
  { file: '/media/part3.mp4', label: 'Parte 3' },
  { file: '/media/part4.mp4', label: 'Parte 4' }
];

export default function VideoSegments() {
  const [segments, setSegments] = useState<Segment[]>(DEFAULT_SEGMENTS);
  const [openPrompt, setOpenPrompt] = useState(false);
  const [exists, setExists] = useState<boolean[]>([false, false, false, false]);

  useEffect(() => {
    Promise.all(segments.map((s) => fetch(s.file, { method: 'HEAD' }).then((r) => r.ok).catch(() => false)))
      .then(setExists);
  }, [segments]);

  return (
    <div className="segments">
      <div className="segments-grid">
        {segments.map((s, i) => (
          <div key={s.file} className="segment-card">
            <div className="seg-header">
              <div className="seg-title">{s.label}</div>
              <button className="seg-prompt" onClick={() => setOpenPrompt(true)}>Ver roteiro</button>
            </div>
            {exists[i] ? (
              <video controls preload="metadata" style={{ width: '100%', borderRadius: 10 }}>
                <source src={s.file} type="video/mp4" />
              </video>
            ) : (
              <div className="image-fallback">Arquivo não encontrado ({s.file}). Rode npm run prepare-media.</div>
            )}
          </div>
        ))}
      </div>
      <MarkdownViewer src="/prompts/veo3_video_roteiro.md" title="Roteiro Veo3" open={openPrompt} onClose={() => setOpenPrompt(false)} />
    </div>
  );
}

