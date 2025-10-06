type Props = { url: string; title?: string; open: boolean; onClose: () => void };

export default function ExternalModal({ url, title, open, onClose }: Props) {
  if (!open) return null;
  return (
    <div className="overlay" onClick={onClose}>
      <div className="overlay-card" onClick={(e) => e.stopPropagation()}>
        <div className="overlay-header">
          <div className="title">{title || url}</div>
          <div className="actions">
            <a className="btn" href={url} target="_blank" rel="noreferrer">Abrir em nova aba</a>
            <button className="btn" onClick={onClose}>Fechar</button>
          </div>
        </div>
        <div className="overlay-body" style={{ padding: 0 }}>
          <iframe src={url} title={title || url} style={{ width: '100%', height: '100%', border: 0 }} />
          <div style={{ padding: '0.5rem', fontSize: '0.9rem', color: '#475569' }}>
            Se o LinkedIn bloquear a incorporação, use “Abrir em nova aba”.
          </div>
        </div>
      </div>
    </div>
  );
}

