import {
  bisection,
  falsePosition,
  simpleFixedPoint,
  newton,
  secant,
  gaussElimination,
  luDecomposition,
  cramer,
  gaussJordan,
} from '../../utils/Methods.js';

const methodMap = {
  Bisection: { solve: bisection, backendFile: 'Bisection.py' },
  'False Position': { solve: falsePosition, backendFile: 'false_position.py' },
  'Simple Fixed': { solve: simpleFixedPoint, backendFile: 'fixed_point.py' },
  Newton: { solve: newton, backendFile: 'newton.py' },
  Secant: { solve: secant, backendFile: 'secant.py' },
  'Gauss Elimination': { solve: gaussElimination, backendFile: 'gauss elimination method.py' },
  'LU Decomposition': { solve: luDecomposition, backendFile: 'lu_pivotting.py' },
  'Gauss Jordan': { solve: gaussJordan, backendFile: 'gauss jordan method.py' },
  Cramer: { solve: cramer, backendFile: 'cramer_rule.py' },
};

export default function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Use POST for method solving.' });
    return;
  }

  const { method, values } = req.body || {};
  const solver = methodMap[method];

  if (!solver) {
    res.status(400).json({ error: 'Unknown numerical method.' });
    return;
  }

  try {
    const result = solver.solve(values);
    res.status(result?.error ? 422 : 200).json({
      backendFile: solver.backendFile,
      result,
    });
  } catch (error) {
    res.status(422).json({ backendFile: solver.backendFile, error: error.message || 'Solve failed.' });
  }
}
