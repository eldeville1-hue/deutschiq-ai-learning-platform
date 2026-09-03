import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { FaArrowLeft } from 'react-icons/fa';

const ROOT_ROUTES = new Set(['/', '/dashboard', '/analytics', '/plan', '/tutor', '/profile']);

export function AppBackButton() {
  const location = useLocation();
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const visible = !ROOT_ROUTES.has(location.pathname);

  const goBack = () => {
    if (window.history.length > 1) navigate(-1);
    else navigate('/dashboard');
  };

  useEffect(() => {
    const backButton = (window as any).Telegram?.WebApp?.BackButton;
    if (!visible || !backButton) return;
    backButton.show();
    backButton.onClick(goBack);
    return () => {
      backButton.offClick?.(goBack);
      backButton.hide();
    };
  }, [location.pathname, location.search, visible]);

  if (!visible) return null;
  return <button className="app-back-button" type="button" onClick={goBack} aria-label={lang === 'ru' ? 'Назад' : 'Zurück'}><FaArrowLeft aria-hidden="true" /></button>;
}
