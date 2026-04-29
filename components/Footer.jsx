import React from 'react';
import Github from '../assets/svg/Github - Negative.svg';
import Linkedin from '../assets/svg/LinkedIn - Negative.svg';
import Instagram from '../assets/svg/Instagram - Negative.svg';
import Telegram from '../assets/svg/Telegram - Negative.svg';

const Footer = () => {
  const social = [
    {
      name: 'Portfolio',
      link: 'https://mohamedessam18.github.io',
      icon: <Github className="social-icon" />,
    },
    {
      name: 'GitHub',
      link: 'https://github.com/mohamedessam18',
      icon: <Github className="social-icon" />,
    },
    {
      name: 'LinkedIn',
      link: 'https://www.linkedin.com/in/mohammedessam2',
      icon: <Linkedin className="social-icon" />,
    },
    {
      name: 'Telegram',
      link: 'https://t.me/mohvmedesam20',
      icon: <Telegram className="social-icon" />,
    },
    {
      name: 'Instagram',
      link: 'https://www.instagram.com/mohvmedesam20',
      icon: <Instagram className="social-icon" />,
    },
  ];

  return (
    <div className="footer">
      <div className="footer-container">
        <div className="copyright">
          <span className="text">&copy; 2026 mohamedessam</span>
        </div>

        <div className="social">
          {social.map((site) => {
            return (
              <a
                key={site.name}
                href={site.link}
                target="_blank"
                rel="noopener noreferrer"
                className="social-icon-container"
                title={site.name}>
                {site.icon}
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Footer;
