import React from 'react';
import Button from './Button';
import { useRouter } from 'next/router';

import { useX } from '../context/xContext';
import Styles from '../styles/button.module.scss';
import CalculateIcon from '../assets/svg/calculateIcon';
import ClearIcon from '../assets/svg/clearIcon';
import DeleteIcon from '../assets/svg/deleteIcon';
import BookmarkIcon from '../assets/svg/bookmarkIcon';
import ShareIcon from '../assets/svg/shareIcon';

const MethodButtons = (props) => {
  const { showMsg } = useX();
  const router = useRouter();

  const copyLink = async () => {
    const URL = window.location.href;
    if ('clipboard' in navigator) {
      await navigator.clipboard.writeText(URL);
      showMsg('success', 'Solution Link Copied');
    } else {
      document.execCommand('copy', true, URL);
      showMsg('success', 'Solution Link Copied');
    }
  };

  return (
    <div
      className={Styles.buttons_container}
      data-aos="fade-up"
      data-aos-duration="400"
      data-aos-delay={props['data-aos-delay'] ? props['data-aos-delay'] : '0'}
      data-aos-once="true">
      <Button label="Solve" icon={<CalculateIcon />} type="submit" value="calculate" isPrimary={true} />
      <Button
        label="Save"
        icon={<BookmarkIcon />}
        type="button"
        onClick={() => props.calculate({ operation: 'save' })}
      />
      <Button label="Clear Input" icon={<ClearIcon />} type="reset" />
      <Button label="Clear Output" icon={<DeleteIcon />} type="button" onClick={props.clearOutput} />
      {router.query.operation === 'calculateQuery' && (
        <Button label="Share Solution" icon={<ShareIcon />} type="button" onClick={copyLink} isNew={true} />
      )}
    </div>
  );
};

export default MethodButtons;
