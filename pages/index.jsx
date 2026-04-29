import React from 'react';
import Button from '../components/Button';
import Styles from '../styles/containers.module.scss';
import Image from 'next/image';
import logo from '../public/logo.png';
import FadeChildren from '../components/FadeChildren';
import Head from 'next/head';

const Home = () => {
  return (
    <>
      <Head>
        <title>Numerical Analysis Project</title>
      </Head>
      <div className="center-content-page">
        <div className={Styles.flexColumnFullWidth}>
          <FadeChildren>
            <Image src={logo} alt="logo" width={150} height={150} className="logo-icon" />
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
