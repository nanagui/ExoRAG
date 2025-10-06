import { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import LightCurveViewer from './components/LightCurveViewer';
import EvidencePanel from './components/EvidencePanel';
import CandidatesTable from './components/CandidatesTable';
import { logger } from './utils/logger';
import SliderPresent from './present/SliderPresent';
import LandingPresent from './present/LandingPresent';

export type Candidate = {
  target: string;
  mission: string | null;
  path: string;
  downloaded_at: string;
};

function App() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [selected, setSelected] = useState<Candidate | null>(null);
  const [evidence, setEvidence] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [route, setRoute] = useState<string>(typeof window !== 'undefined' ? window.location.hash : '');
  useEffect(() => {
    const onHash = () => setRoute(window.location.hash);
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);
  const isPresentMode = useMemo(() => {
    const h = route;
    const p = typeof window !== 'undefined' ? window.location.pathname : '';
    return h === '#/present' || p.endsWith('/present') || h === '#present';
  }, [route]);
  const isLandingMode = useMemo(() => {
    const h = route;
    const p = typeof window !== 'undefined' ? window.location.pathname : '';
    return h === '#/landing' || p.endsWith('/landing') || h === '#landing';
  }, [route]);

  useEffect(() => {
    if (isPresentMode || isLandingMode) return; // skip in presentation/landing
    const token = localStorage.getItem('EXOAI_TOKEN');
    if (!token) return; // skip when unauthenticated to avoid 401/500 noise
    axios
      .get<Candidate[]>('/api/predictions/candidates', {
        headers: { Authorization: token }
      })
      .then((res) => setCandidates(res.data))
      .catch((err) => {
        logger.error('Failed to load candidates', { err });
        setError('Unable to load candidates. Check authentication.');
      });
  }, [isPresentMode, isLandingMode]);

  const handleSelect = (candidate: Candidate) => {
    setSelected(candidate);
    setEvidence(null);
    setLoading(true);
    setError(null);
    axios
      .get('/api/predictions/explain', {
        params: { path: candidate.path },
        headers: { Authorization: localStorage.getItem('EXOAI_TOKEN') ?? '' }
      })
      .then((res) => setEvidence(res.data))
      .catch((err) => {
        logger.error('Failed to load explanation', { err, path: candidate.path });
        setError('Failed to load explanation.');
      })
      .finally(() => setLoading(false));
  };

  if (isPresentMode) {
    return <SliderPresent />;
  }
  if (isLandingMode) {
    return <LandingPresent />;
  }

  return (
    <div className="app-container">
      <header>
        <h1>Exoplanet AI Control Center</h1>
        <p>Monitor predictions, inspect attention overlays, and review scientific evidence.</p>
        <div style={{ marginTop: '8px' }}>
          <a href="#/present" style={{ marginRight: 12 }}>Abrir modo apresentação</a>
          <a href="#/landing">Abrir landing</a>
        </div>
      </header>
      <main>
        <section className="sidebar">
          <CandidatesTable
            candidates={candidates}
            selected={selected}
            onSelect={handleSelect}
          />
        </section>
        <section className="content">
          {selected ? (
            <div className="visualization">
              <LightCurveViewer candidate={selected} authHeader={localStorage.getItem('EXOAI_TOKEN') ?? ''} />
              <EvidencePanel evidence={evidence} loading={loading} error={error} />
            </div>
          ) : (
            <div className="placeholder">Selecione um candidato para visualizar detalhes.</div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
