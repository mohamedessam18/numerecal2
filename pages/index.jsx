import React from 'react';
import Button from '../components/Button';
import Styles from '../styles/containers.module.scss';
import Image from 'next/image';
import { useTheme } from 'next-themes';
import naLogoDark from '../public/na-logo-dark.png';
import naLogoLight from '../public/na-logo-light.png';
import FadeChildren from '../components/FadeChildren';
import Head from 'next/head';

const Home = () => {
  const { theme } = useTheme();
  const [mode, setMode] = React.useState('light');

  React.useEffect(() => {
    if (theme !== 'system') setMode(theme);
    else setMode(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }, [theme]);

  const homeLogo = mode === 'dark' ? naLogoDark : naLogoLight;

  return (
    <>
      <Head>
        <title>Numerical Analysis Project</title>
      </Head>
      <div className="center-content-page">
        <div className={Styles.flexColumnFullWidth}>
          <FadeChildren>
            <Image src={homeLogo} alt="NA logo" width={150} height={150} className="logo-icon" priority />
            <div
              className="center-title landpage-title"
              style={{
                marginBottom: '5px',
              }}>
              Numerical Analysis <br /> Mini Project
            </div>
            <Button label="Jump to methods →" path="/methods" isPrimary={true} />
          </FadeChildren>
        </div>
      </div>
    </>
  );
};

export default Home;
