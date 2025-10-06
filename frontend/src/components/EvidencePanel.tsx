interface Props {
  evidence: any;
  loading: boolean;
  error: string | null;
}

const EvidencePanel = ({ evidence, loading, error }: Props) => {
  return (
    <div className="card evidence-panel">
      <h2>Justificativa científica</h2>
      {loading && <div>Consultando base científica...</div>}
      {error && <div className="error">{error}</div>}
      {!loading && !error && evidence && (
        <div className="evidence-content">
          <p>{evidence.answer}</p>
          <ul>
            {evidence.documents?.map((doc: any, index: number) => (
              <li key={index}>
                <strong>{doc.metadata?.source ?? 'Fonte desconhecida'}:</strong> {doc.text?.slice(0, 120)}...
              </li>
            ))}
          </ul>
        </div>
      )}
      {!loading && !error && !evidence && <p>Selecione um candidato para gerar evidências.</p>}
    </div>
  );
};

export default EvidencePanel;
