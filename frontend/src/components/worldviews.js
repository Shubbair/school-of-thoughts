export const worldviewFor = (name, details = {}) => ({
  glyph: '·',
  color: 'stone',
  shortName: name,
  ...details,
});
