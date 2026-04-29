import React from 'react';
import MiniLabel from './MiniLabel';

const FinalRoot = ({ value }) => {
  if (value === undefined || value === null) return null;

  return (
    <div className="final-root">
      <span>Final Root</span>
      <strong>{value}</strong>
      <MiniLabel label="Root" />
    </div>
  );
};

export default FinalRoot;
