export const normalizeExpression = (expression = '') =>
  expression
    .replace(/\^/g, '**')
    .replace(/(\d)(x)/gi, '$1*$2')
    .replace(/(x|\))(\d)/gi, '$1*$2')
    .replace(/(x|\))(?=\()/gi, '$1*')
    .replace(/\)(x)/gi, ')*$1')
    .replace(/(sin|cos|tan|exp|log|sqrt|cbrt|abs)\s*\(/g, 'Math.$1(')
    .replace(/(\d|x|\))(Math\.)/gi, '$1*$2')
    .replace(/\bpi\b/gi, 'Math.PI')
    .replace(/\be\b/g, 'Math.E');

export const createFunction = (expression) => {
  const normalized = normalizeExpression(expression);
  return new Function('x', `"use strict"; return (${normalized});`);
};

export const linspace = (min, max, count) => {
  if (count <= 1) return [min];
  const step = (max - min) / (count - 1);
  return Array.from({ length: count }, (_, index) => min + step * index);
};
