import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { worldviewFor } from './worldviews';
import './Stage1.css';

export default function Stage1({ responses, question }) {
  const [activeName, setActiveName] = useState(null);
  if (!responses || responses.length === 0) {
    return null;
  }

  const seats = responses.map((response) => ({
    name: response.model,
    details: worldviewFor(response.model, response.details),
    response,
  }));
  const activeSeat = seats.find((seat) => seat.name === activeName);

  return (
    <section className="stage table-stage">
      <div className="stage-heading">
        <div>
          <p className="eyebrow">Opening views</p>
          <h3 className="stage-title">The round table</h3>
        </div>
        <span className="stage-note">{responses.length} of {seats.length} seats answered</span>
      </div>

      <div className="round-table" aria-label="Council round table">
        <div className="table-question">
          <span className="question-label">The question</span>
          <p>{question || 'The council is considering this question.'}</p>
        </div>
        {seats.map((seat) => (
          <button
            type="button"
            key={seat.name}
            className={`worldview-seat seat-${seat.details.color} ${
              activeName === seat.name ? 'is-selected' : ''
            } ${!seat.response ? 'is-empty' : ''}`}
            onClick={() => seat.response && setActiveName(
              activeName === seat.name ? null : seat.name
            )}
            disabled={!seat.response}
          >
            <span className="seat-glyph" aria-hidden="true">{seat.details.glyph}</span>
            <span className="seat-name">{seat.details.shortName}</span>
            <span className="seat-status">
              {seat.response ? 'Has the floor' : 'Did not respond'}
            </span>
            {seat.response && activeName !== seat.name && (
              <span className="seat-excerpt">{seat.response.response}</span>
            )}
          </button>
        ))}
      </div>

      {activeSeat?.response && (
        <div className={`focused-position focus-${activeSeat.details.color}`}>
          <div className="focused-heading">
            <span className="seat-glyph" aria-hidden="true">{activeSeat.details.glyph}</span>
            <div>
              <p className="eyebrow">Focused position</p>
              <h4>{activeSeat.name}</h4>
            </div>
          </div>
          <div className="position-text markdown-content">
            <ReactMarkdown>{activeSeat.response.response}</ReactMarkdown>
          </div>
        </div>
      )}
    </section>
  );
}
