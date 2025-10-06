import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { Candidate } from '../App';

interface Props {
  candidate: Candidate;
  authHeader: string;
}

const LightCurveViewer = ({ candidate, authHeader }: Props) => {
  const [data, setData] = useState<{ time: number[]; flux: number[] } | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios
      .get('/api/predictions/explain', {
        params: { path: candidate.path, return_series: true },
        headers: { Authorization: authHeader }
      })
      .then((res) => {
        setData(res.data.series);
      })
      .finally(() => setLoading(false));
  }, [candidate, authHeader]);

  if (loading) return <div className="card">Carregando curva de luz...</div>;
  if (!data) return <div className="card">Sem dados para exibir.</div>;

  return (
    <div className="card">
      <h2>{candidate.target}</h2>
      <Plot
        data={[
          {
            x: data.time,
            y: data.flux,
            type: 'scatter',
            mode: 'lines',
            line: { color: '#1B9CFC' }
          }
        ]}
        layout={{
          autosize: true,
          title: 'Curva de luz normalizada',
          xaxis: { title: 'Tempo (dias)' },
          yaxis: { title: 'Fluxo normalizado' },
          margin: { l: 50, r: 20, t: 50, b: 40 }
        }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler
      />
    </div>
  );
};

export default LightCurveViewer;
