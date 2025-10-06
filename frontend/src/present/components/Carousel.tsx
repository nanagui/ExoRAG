import { useEffect, useState } from 'react';

type Item = { src: string; alt: string; caption?: string };

type Props = {
  items: Item[];
  onOpenImage?: (src: string, alt?: string) => void;
};

export default function Carousel({ items, onOpenImage }: Props) {
  const [idx, setIdx] = useState(0);
  const [warn, setWarn] = useState<string | null>(null);
  const current = items[idx];

  useEffect(() => {
    // probe first asset
    fetch(current.src, { method: 'HEAD' }).then((r) => {
      if (!r.ok) setWarn('Imagens não encontradas. Rode npm run prepare-media.');
    }).catch(() => setWarn('Imagens não encontradas. Rode npm run prepare-media.'));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="carousel">
      <div className="carousel-stage">
        <button className="nav" onClick={() => setIdx((i) => (i === 0 ? items.length - 1 : i - 1))}>‹</button>
        <div className="frame" onClick={() => onOpenImage && onOpenImage(current.src, current.alt)} style={{ cursor: onOpenImage ? 'zoom-in' : 'default' }}>
          <img src={current.src} alt={current.alt} />
          {current.caption && <div className="caption">{current.caption}</div>}
        </div>
        <button className="nav" onClick={() => setIdx((i) => (i + 1) % items.length)}>›</button>
      </div>
      <div className="dots">
        {items.map((_, i) => (
          <button key={i} className={i === idx ? 'dot active' : 'dot'} onClick={() => setIdx(i)} />
        ))}
      </div>
      {warn && <div className="present-toast">{warn}</div>}
    </div>
  );
}
