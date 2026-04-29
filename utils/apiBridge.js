export const solveMethod = async (method, values) => {
  const response = await fetch('/api/solve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ method, values }),
  });

  const payload = await response.json();
  if (!response.ok) return { error: payload.error || payload.result?.error || 'Solve failed.' };
  return payload.result;
};
