import React from 'react';
import BtnStyles from '../styles/button.module.scss';

const FunctionHelperButtons = ({ inputName = 'fx', includeRoots = true }) => {
  const insertAtCursor = (text) => {
    const input = document.querySelector(`input[name="${inputName}"]`);
    if (!input) return;

    const start = input.selectionStart ?? input.value.length;
    const end = input.selectionEnd ?? input.value.length;
    const nextValue = `${input.value.slice(0, start)}${text}${input.value.slice(end)}`;

    input.value = nextValue;
    input.focus();
    const cursor = start + text.length - (text.endsWith('()') ? 1 : 0);
    input.setSelectionRange(cursor, cursor);
  };

  const helpers = [
    { label: 'x^5', value: 'x^5' },
    { label: 'x^4', value: 'x^4' },
    { label: 'x^3', value: 'x^3' },
    { label: 'x^2', value: 'x^2' },
  ];

  if (includeRoots) {
    helpers.push({ label: 'Square Root', value: 'sqrt()' }, { label: 'Cube Root', value: 'cbrt()' });
  }

  return (
    <div className={BtnStyles.buttons_container + ' helper-buttons'}>
      {helpers.map((helper) => (
        <button
          key={helper.label}
          type="button"
          className={BtnStyles.button}
          onClick={() => insertAtCursor(helper.value)}>
          {helper.label}
        </button>
      ))}
    </div>
  );
};

export default FunctionHelperButtons;
