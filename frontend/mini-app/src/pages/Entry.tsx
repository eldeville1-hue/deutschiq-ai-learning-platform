import React, { useCallback, useEffect, useState } from 'react';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { getUserId } from '../utils/user';
import { DiagnosticWelcome } from './DiagnosticWelcome';
import { ReturningIntro } from './ReturningIntro';
import { Navigate } from 'react-router-dom';
import { BrandMark } from '../components/BrandMark';

type UserState = { diagnostic_completed: boolean; language: 'ru' | 'de'; level: string };

export const Entry: React.FC = () => {
  const { lang, setLanguage } = useLanguage();
  const [state, setState] = useState<UserState | null>(null);
  const [failed, setFailed] = useState(false);
  const userId = getUserId();

  const loadState = useCallback(() => {
    setFailed(false);
    setState(null);
    api.getUserState(userId).then((value) => {
      const remoteLanguage = value.language === 'de' ? 'de' : 'ru';
      setLanguage(remoteLanguage, false);
      setState(value);
    }).catch(() => setFailed(true));
  }, [setLanguage, userId]);
  useEffect(() => { loadState(); }, [loadState]);

  if (failed) return <main className="auth-error"><BrandMark label="DeutschIQ" /><h1>{lang === 'ru' ? 'Не удалось загрузить профиль' : 'Profil konnte nicht geladen werden'}</h1><p>{lang === 'ru' ? 'Проверь соединение и попробуй ещё раз.' : 'Prüfe deine Verbindung und versuche es erneut.'}</p><button className="primary-action" onClick={loadState}>{lang === 'ru' ? 'Повторить' : 'Erneut versuchen'}</button></main>;
  if (!state) return <main className="entry-loading"><BrandMark label="DeutschIQ" /><div className="analysis-loader" /></main>;
  if (!state.diagnostic_completed) return <DiagnosticWelcome />;
  const introKey = `deutschiq-intro-${userId}-${new Date().toISOString().slice(0, 10)}`;
  if (sessionStorage.getItem(introKey)) return <Navigate to="/dashboard" replace />;
  return <ReturningIntro level={state.level || 'A1'} introKey={introKey} />;
};
