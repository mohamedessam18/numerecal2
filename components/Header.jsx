/* eslint-disable react-hooks/rules-of-hooks */
import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useTheme } from 'next-themes';
import Image from 'next/image';

// Assets
import mnaLogoDark from '../public/mna-logo-dark.png';
import mnaLogoLight from '../public/mna-logo-light.png';
import LightIcon from '../assets/svg/lightIcon';
import DarkIcon from '../assets/svg/darkIcon';
import SettingsIcon from '../assets/svg/settingsIcon';
import FunctionIcon from '../assets/svg/functionIcon';
import HistoryIcon from '../assets/svg/historyIcon';
import BookmarksIcon from '../assets/svg/bookmarksIcon';

const Header = () => {
  const router = useRouter();
  const { theme, setTheme } = useTheme();
  const [mode, setMode] = React.useState('light');
  // const [themeLabel, setThemeLabel] = React.useState('Dark');

  // React.useEffect(() => {
  //   if (theme === 'dark') setTheme('dark');
  //   else setTheme('light');
  // }, []);

  const menuItems = [
    {
      name: 'Methods',
      path: '/methods',
      icon: <FunctionIcon />,
    },
    {
      name: 'History',
      path: '/history',
      icon: <HistoryIcon />,
    },
    {
      name: 'Saved',
      path: '/saved',
      icon: <BookmarksIcon />,
    },

    {
      name: 'Settings',
      path: '/settings',
      icon: <SettingsIcon />,
    },
  ];

  React.useEffect(() => {
    if (theme !== 'system') setMode(theme);
    else setMode(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }, [theme]);

  const headerLogo = mode === 'dark' ? mnaLogoDark : mnaLogoLight;

  return (
    <div className="header">
      <div className="header-container">
        <Link href="/">
          <div className="logo">
            <Image src={headerLogo} alt="MNA logo" width={70} height={38} className="header-logo-image" priority />
          </div>
        </Link>
        <div className="header-buttons">
          {menuItems.map((item) => (
            // eslint-disable-next-line react-hooks/rules-of-hooks
            <Link
              key={item.path}
              className={`header-button ${router.pathname === item.path && 'active-page'}`}
              title={item.name}
              href={item.path}>
              {item.icon && <div className="header-button-icon">{item.icon}</div>}
              {/* <div className="header-button-text">{item.name}</div> */}
            </Link>
          ))}
          <div
            className="header-button header-button-static"
            title={mode === 'dark' ? 'Light mode' : 'Dark mode'}
            onClick={() => (mode === 'dark' ? setTheme('light') : setTheme('dark'))}>
            <div className="header-button-icon">{mode === 'dark' ? <LightIcon /> : <DarkIcon />}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
