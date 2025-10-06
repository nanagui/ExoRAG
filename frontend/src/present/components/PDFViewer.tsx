type Props = { src: string; title?: string; open: boolean; onClose: () => void };

export default function PDFViewer({ src, title, open, onClose }: Props) {
  if (!open) return null;
  return (
    <div className="overlay" onClick={onClose}>
      <div className="overlay-card" onClick={(e) => e.stopPropagation()}>
        <div className="overlay-header">
          <div className="title">{title || 'Documento'}</div>
          <div className="actions">
            <a className="btn" href={src} target="_blank" rel="noreferrer">Abrir em nova aba</a>
            <button className="btn" onClick={onClose}>Fechar</button>
          </div>
        </div>
        <div className="overlay-body" style={{ padding: 0 }}>
          <object data={src} type="application/pdf" width="100%" height="100%">
            <div style={{ padding: '1rem' }}>
              Não foi possível embutir o PDF. <a href={src} target="_blank" rel="noreferrer">Clique aqui</a> para abrir em nova aba.
            </div>
          </object>
        </div>
      </div>
    </div>
  );
}

