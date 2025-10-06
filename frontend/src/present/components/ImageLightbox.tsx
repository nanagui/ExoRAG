import { useEffect } from 'react';

type Props = { src: string; alt?: string; open: boolean; onClose: () => void };

export default function ImageLightbox({ src, alt, open, onClose }: Props) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    if (open) window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="overlay-fullimg" onClick={onClose}>
      <div className="fullimg-bar" onClick={(e) => e.stopPropagation()}>
        <div className="title">{alt || 'Imagem'}</div>
        <button className="btn" onClick={onClose}>Fechar</button>
      </div>
      <img className="fullimg-image" src={src} alt={alt || ''} onClick={(e) => e.stopPropagation()} />
    </div>
  );
}
