import { createFunction } from './functionMath.js';

const maxIterations = (condition) => (condition?.type === 'it' ? Number(condition.value) : 50);
const stopError = (condition) => (condition?.type === 'es' ? Number(condition.value) : 0);
const finite = (value) => Number.isFinite(value);

const makeError = (message) => ({ error: message });

const derivative = (f, x) => {
  const h = Math.max(Math.abs(x) * 1e-6, 1e-6);
  return (f(x + h) - f(x - h)) / (2 * h);
};

export const bisection = ({ fx, xl, xu, condition }) => {
  const f = createFunction(fx);
  let lower = Number(xl);
  let upper = Number(xu);
  let xr = null;
  let xrOld = null;
  const rows = [];

  if (f(lower) * f(upper) >= 0) return makeError('f(xl) and f(xu) must have opposite signs.');

  for (let i = 1; i <= maxIterations(condition); i++) {
    xrOld = xr;
    xr = (lower + upper) / 2;
    const fxl = f(lower);
    const fxr = f(xr);
    const fxu = f(upper);
    const ea = xrOld !== null && xr !== 0 ? Math.abs((xr - xrOld) / xr) * 100 : 0;

    rows.push({ i, xl: lower, fxl, xr, fxr, xu: upper, fxu, ea });
    if (ea !== 0 && ea < stopError(condition)) break;
    if (Math.abs(fxr) < 1e-10) break;
    if (fxl * fxr < 0) upper = xr;
    else lower = xr;
  }

  rows.graph = { expression: fx, boundsLow: Math.min(Number(xl), Number(xu)), boundsHigh: Math.max(Number(xl), Number(xu)), root: xr, title: 'Bisection Method' };
  return rows;
};

export const falsePosition = ({ fx, xl, xu, condition }) => {
  const f = createFunction(fx);
  let lower = Number(xl);
  let upper = Number(xu);
  const lowerInitial = lower;
  const upperInitial = upper;
  let xr = 0;
  let xrOld = 0;
  const rows = [];

  if (f(lower) * f(upper) >= 0) return makeError('f(xl) and f(xu) must have opposite signs.');

  for (let i = 1; i <= maxIterations(condition); i++) {
    xrOld = xr;
    const fl = f(lower);
    const fu = f(upper);
    xr = upper - (fu * (lower - upper)) / (fl - fu);
    const fxr = f(xr);
    const ea = i > 1 && xr !== 0 ? Math.abs((xr - xrOld) / xr) * 100 : 0;

    rows.push({ i, xl: lower, fxl: fl, xr, fxr, xu: upper, fxu: fu, ea });
    if (i > 1 && ea < stopError(condition)) break;
    if (fl * fxr < 0) upper = xr;
    else lower = xr;
  }

  rows.graph = { expression: fx, boundsLow: lowerInitial, boundsHigh: upperInitial, root: xr, title: 'False Position Method' };
  return rows;
};

export const simpleFixedPoint = ({ fx, x0, condition }) => {
  const g = createFunction(fx);
  let xr = Number(x0);
  const rows = [];

  for (let i = 1; i <= maxIterations(condition); i++) {
    const xrOld = xr;
    xr = g(xrOld);
    if (!finite(xr)) return makeError('Method diverged or produced an invalid value.');
    const ea = i > 1 ? Math.abs((xr - xrOld) / (xr || xr + 1e-10)) * 100 : 100;

    rows.push({ i, xi: xr, fxi: xr, ea });
    if (i > 1 && ea < stopError(condition)) break;
    if (i > 10 && ea > 1000) return makeError('Method may be diverging. Try another initial guess or rearrangement.');
  }

  rows.graph = {
    expression: fx,
    plotExpression: `x - (${fx})`,
    boundsLow: Number(x0) - 2,
    boundsHigh: Number(x0) + 2,
    root: xr,
    title: 'Fixed Point Iteration (f(x) = x - g(x))',
  };
  return rows;
};

export const newton = ({ fx, x0, condition }) => {
  const f = createFunction(fx);
  const initial = Number(x0);
  let xr = initial;
  const rows = [];

  for (let i = 1; i <= maxIterations(condition); i++) {
    const xrOld = xr;
    const fxi = f(xrOld);
    const dfxi = derivative(f, xrOld);
    if (!finite(dfxi) || dfxi === 0) return makeError('Derivative is zero or invalid. Newton-Raphson fails.');
    xr = xrOld - fxi / dfxi;
    const ea = xr !== 0 ? Math.abs((xr - xrOld) / xr) * 100 : 0;

    rows.push({ i, xi: xrOld, fxi, dfxi, ea });
    if (ea < stopError(condition)) break;
  }

  rows.graph = { expression: fx, boundsLow: initial - 2, boundsHigh: initial + 2, root: xr, title: 'Newton-Raphson' };
  return rows;
};

export const secant = ({ fx, x_1, x0, condition }) => {
  const f = createFunction(fx);
  const initialA = Number(x_1);
  let xiMinus1 = initialA;
  let xi = Number(x0);
  let xiPlus1 = xi;
  const rows = [];

  for (let i = 1; i <= maxIterations(condition); i++) {
    const fxa = f(xiMinus1);
    const fxb = f(xi);
    if (fxb - fxa === 0) return makeError('Division by zero in the secant formula.');
    xiPlus1 = xi - (fxb * (xi - xiMinus1)) / (fxb - fxa);
    const ea = xiPlus1 !== 0 ? Math.abs((xiPlus1 - xi) / xiPlus1) * 100 : 0;

    rows.push({ i, x_1: xiMinus1, fxa, x0: xi, fxb, ea });
    if (ea < stopError(condition)) break;
    xiMinus1 = xi;
    xi = xiPlus1;
  }

  rows.graph = { expression: fx, boundsLow: initialA, boundsHigh: xiPlus1, root: xiPlus1, title: 'Secant Method' };
  return rows;
};

const toMatrix = (matrix) => matrix.map((row) => row.map(Number));

const solveLinear = (matrix) => {
  const a = toMatrix(matrix);
  const n = a.length;
  const mainMatrix = a.map((row) => [...row]);

  for (let i = 0; i < n; i++) {
    let pivotRow = i;
    for (let row = i + 1; row < n; row++) {
      if (Math.abs(a[row][i]) > Math.abs(a[pivotRow][i])) pivotRow = row;
    }
    if (Math.abs(a[pivotRow][i]) < 1e-12) return makeError('The system has no unique solution.');
    if (pivotRow !== i) [a[i], a[pivotRow]] = [a[pivotRow], a[i]];
    for (let row = i + 1; row < n; row++) {
      const factor = a[row][i] / a[i][i];
      for (let col = i; col <= n; col++) a[row][col] -= factor * a[i][col];
    }
  }

  const xsValues = Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) {
    let rhs = a[i][n];
    for (let col = i + 1; col < n; col++) rhs -= a[i][col] * xsValues[col];
    xsValues[i] = rhs / a[i][i];
  }

  const values = xsValues.map((value, index) => ({ name: 'x', sub: index + 1, value }));
  return { mainMatrix, step1: [], step2: [], step3: [], xsValues: values };
};

export const gaussElimination = ({ matrix }) => solveLinear(matrix);
export const gaussJordan = ({ matrix }) => solveLinear(matrix);
export const luDecomposition = ({ matrix }) => {
  const solved = solveLinear(matrix);
  if (solved.error) return solved;
  return {
    A: toMatrix(matrix).map((row) => row.slice(0, 3)),
    b: toMatrix(matrix).map((row) => [row[3]]),
    step1: [],
    step2: [],
    U: { comment: 'Upper matrix', matrix: toMatrix(matrix).map((row) => row.slice(0, 3)) },
    L: { comment: 'Lower matrix', matrix: [[1, 0, 0], [0, 1, 0], [0, 0, 1]] },
    AxEqB: { comment: 'Solution', xsValues: solved.xsValues },
    LcEqB: {},
    UxEqC: {},
  };
};

const det3 = (m) =>
  m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
  m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
  m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);

export const cramer = ({ matrix }) => {
  const data = toMatrix(matrix);
  const a = data.map((row) => row.slice(0, 3));
  const b = data.map((row) => row[3]);
  const determinant = det3(a);
  if (Math.abs(determinant) < 1e-12) return makeError("Cramer's Rule requires a non-zero determinant.");

  const replaceColumn = (column) => a.map((row, index) => row.map((value, col) => (col === column ? b[index] : value)));
  const determinants = [0, 1, 2].map((column) => det3(replaceColumn(column)));
  const xValues = determinants.map((value) => value / determinant);

  return {
    A: { matrix: a, matrixLabel: 'A = ', det: `D = ${determinant}` },
    A1: { matrix: replaceColumn(0), matrixLabel: 'A1 = ', det: `D1 = ${determinants[0]}` },
    A2: { matrix: replaceColumn(1), matrixLabel: 'A2 = ', det: `D2 = ${determinants[1]}` },
    A3: { matrix: replaceColumn(2), matrixLabel: 'A3 = ', det: `D3 = ${determinants[2]}` },
    xEq: xValues.map((value, index) => ({
      rule: `x${index + 1} = D${index + 1} / D`,
      sub_in_rule: `${determinants[index]} / ${determinant} = ${value}`,
    })),
    xValues: xValues.map((value, index) => ({ name: 'x', sub: index + 1, value })),
  };
};
