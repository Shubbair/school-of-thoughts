import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { worldviewFor } from './worldviews';
import './Stage2.css';

export default function Stage2({ comparisons }) {
  if (!comparisons || comparisons.length === 0) {
    return null;
  }

  return (
    <div className="stage stage2">
      <h3 className="stage-title">Positions in tension</h3>

      <h4>Rebuttals across the table</h4>
      <p className="stage-description">
        Each representative stays inside its own school and explains what it reveals, where it conflicts with another school, and what it struggles to explain.
      </p>

      <div className="rebuttal-list">
        {comparisons.map((comparison, index) => {
          const worldview = worldviewFor(comparison.model);
          return (
            <article className={`rebuttal-card rebuttal-${worldview.color}`} key={index}>
              <div className="rebuttal-source">
                <span className="seat-glyph" aria-hidden="true">{worldview.glyph}</span>
                <div>
                  <p className="eyebrow">Rebuttal</p>
                  <h4>{worldview.shortName}</h4>
                </div>
              </div>
              <div className="rebuttal-line" aria-hidden="true"></div>
              <div className="rebuttal-content markdown-content">
                <ReactMarkdown>
                  {comparison.comparison || comparison.ranking}
                </ReactMarkdown>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
