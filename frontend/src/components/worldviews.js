export const WORLDVIEWS = {
  'Materialist / Naturalist': { glyph: '⚛', color: 'stone', shortName: 'Materialist / Naturalist' },
  Idealist: { glyph: '◉', color: 'indigo', shortName: 'Idealist' },
  Existentialist: { glyph: '↗', color: 'ochre', shortName: 'Existentialist' },
  Stoic: { glyph: '△', color: 'moss', shortName: 'Stoic' },
};

export const worldviewFor = (name) => WORLDVIEWS[name] || {
  glyph: '·',
  color: 'stone',
  shortName: name,
};
