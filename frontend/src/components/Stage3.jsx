import ReactMarkdown from 'react-markdown';
import './Stage3.css';

const SECTIONS = [
  { key: 'AGREEMENT', label: 'Agreement', className: 'agreement' },
  { key: 'DISAGREEMENT', label: 'Disagreement', className: 'disagreement' },
  { key: 'MINORITY VIEW', label: 'Minority View', className: 'minority' },
  { key: 'BOTTOM LINE', label: "Chairman's Synthesis", className: 'bottom-line' },
];

function sectionContent(text, key, aliases = []) {
  const keys = [key, ...aliases];
  const headingPattern = SECTIONS.flatMap((section) => [section.key, ...(section.aliases || [])]).join('|');
  const expression = new RegExp(
    `(?:^|\\n)\\s*(?:[#*]+\\s*)?(?:${keys.join('|')}):?\\s*([\\s\\S]*?)(?=\\n\\s*(?:[#*]+\\s*)?(?:${headingPattern}):|$)`,
    'i'
  );
  return text.match(expression)?.[1]?.trim() || '';
}

export default function Stage3({ finalResponse }) {
  if (!finalResponse) {
    return null;
  }

  const report = finalResponse.response || '';

  return (
    <section className="stage synthesis-stage">
      <div className="synthesis-heading">
        <div>
          <p className="eyebrow">Council report</p>
          <h3 className="stage-title">Chairman's synthesis</h3>
        </div>
        <span className="synthesis-source">One model, four premises</span>
      </div>
      <div className="synthesis-grid">
        {SECTIONS.map((section) => {
          const content = sectionContent(report, section.key, section.aliases);
          return (
            <article className={`synthesis-block ${section.className}`} key={section.key}>
              <p className="block-label">{section.label}</p>
              <div className="synthesis-text markdown-content">
                <ReactMarkdown>{content || report}</ReactMarkdown>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
