import React from 'react';
import { createFunction, linspace } from '../utils/functionMath.js';

const width = 800;
const height = 500;
const padding = 52;

const MethodGraph = ({ expression, boundsLow, boundsHigh, root, title, plotExpression }) => {
  const graph = React.useMemo(() => {
    if (!expression || root === undefined || root === null) return null;

    try {
      const f = createFunction(plotExpression || expression);
      const low = Number(boundsLow);
      const high = Number(boundsHigh);
      const rootValue = Number(root);
      const margin = Math.max(Math.abs(high - low) * 0.5, 2.0);
      const xMin = Math.min(low, rootValue) - margin;
      const xMax = Math.max(high, rootValue) + margin;
      const points = linspace(xMin, xMax, 250)
        .map((x) => ({ x, y: f(x) }))
        .filter((point) => Number.isFinite(point.y));

      if (!points.length) return null;

      const yValues = points.map((point) => point.y);
      const yMinRaw = Math.min(...yValues);
      const yMaxRaw = Math.max(...yValues);
      const marginY = Math.max((yMaxRaw - yMinRaw) * 0.1, 1.0);
      const yMin = yMinRaw - marginY;
      const yMax = yMaxRaw + marginY;
      const scaleX = (x) => padding + ((x - xMin) / (xMax - xMin)) * (width - padding * 2);
      const scaleY = (y) => height - padding - ((y - yMin) / (yMax - yMin || 1)) * (height - padding * 2);
      const path = points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${scaleX(point.x)} ${scaleY(point.y)}`).join(' ');
      const rootY = f(rootValue);

      return {
        path,
        axisY: scaleY(0),
        rootX: scaleX(rootValue),
        rootY: Number.isFinite(rootY) ? scaleY(rootY) : scaleY(0),
        xMin,
        xMax,
      };
    } catch (error) {
      return null;
    }
  }, [boundsHigh, boundsLow, expression, plotExpression, root]);

  if (!graph) return null;

  return (
    <div className="method-graph">
      <div className="inputs-title">{title || 'Graph'}</div>
      <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`${title || 'Method'} graph`}>
        <rect x="0" y="0" width={width} height={height} rx="12" />
        <line x1={padding} x2={width - padding} y1={graph.axisY} y2={graph.axisY} className="graph-axis" />
        <path d={graph.path} className="graph-line" />
        <circle cx={graph.rootX} cy={graph.rootY} r="8" className="graph-root" />
        <text x={padding} y={height - 18} className="graph-label">
          x: {graph.xMin.toFixed(2)} to {graph.xMax.toFixed(2)}
        </text>
        <text x={width - padding} y={height - 18} textAnchor="end" className="graph-label">
          Root ~= {Number(root).toFixed(4)}
        </text>
      </svg>
    </div>
  );
};

export default MethodGraph;
