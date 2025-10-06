import { Candidate } from '../App';

interface Props {
  candidates: Candidate[];
  selected: Candidate | null;
  onSelect(candidate: Candidate): void;
}

const formatDate = (value: string) => new Date(value).toLocaleString();

const CandidatesTable = ({ candidates, selected, onSelect }: Props) => {
  return (
    <div className="card">
      <h2>Últimos candidatos</h2>
      <table>
        <thead>
          <tr>
            <th>Target</th>
            <th>Missão</th>
            <th>Data</th>
          </tr>
        </thead>
        <tbody>
          {candidates.map((candidate) => (
            <tr
              key={candidate.path}
              className={selected?.path === candidate.path ? 'selected' : ''}
              onClick={() => onSelect(candidate)}
            >
              <td>{candidate.target}</td>
              <td>{candidate.mission ?? '—'}</td>
              <td>{formatDate(candidate.downloaded_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CandidatesTable;
