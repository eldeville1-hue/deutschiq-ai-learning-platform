import React, { useCallback, useEffect, useState } from 'react';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { getUserId } from '../utils/user';
import { DiagnosticWelcome } from './DiagnosticWelcome';
import { ReturningIntro } from './ReturningIntro';
import { Navigate } from 'react-router-dom';
import { BrandMark } from '../components/BrandMark';
import type { AppLanguage } from '../i18n/language';
import { normalizeLanguage, tr } from '../i18n/language';
import { BetaAccess, BetaOnboarding } from './BetaAccess';

type UserState = { exists?: boolean; diagnostic_completed: boolean; language: AppLanguage; level: string; beta_access?: boolean; beta_onboarding_completed?: boolean };

export const Entry: React.FC = () => {
  const { lang, setLanguage } = useLanguage();
  const [state, setState] = useState<UserState | null>(null);
  const [failed, setFailed] = useState(false);
  const userId = getUserId();

  const loadState = useCallback(() => {
    setFailed(false);
    setState(null);
    api.getUserState(userId).then((value) => {
      const selectedLanguage = value.exists === false ? lang : normalizeLanguage(value.language);
      setLanguage(selectedLanguage, value.exists === false);
      setState({ ...value, language: selectedLanguage });
    }).catch(() => setFailed(true));
  }, [lang, setLanguage, userId]);
  useEffect(() => { loadState(); }, [loadState]);

  if (failed) return <main className="auth-error"><BrandMark label="DeutschIQ" /><h1>{tr(lang, 'Не удалось загрузить профиль', 'Profil konnte nicht geladen werden', 'Could not load your profile')}</h1><p>{tr(lang, 'Проверь соединение и попробуй ещё раз.', 'Prüfe deine Verbindung und versuche es erneut.', 'Check your connection and try again.')}</p><button className="primary-action" onClick={loadState}>{tr(lang, 'Повторить', 'Erneut versuchen', 'Try again')}</button></main>;
  if (!state) return <main className="entry-loading"><BrandMark label="DeutschIQ" /><div className="analysis-loader" /></main>;
  if (state.beta_access === false) return <BetaAccess onDone={loadState} />;
  if (state.beta_onboarding_completed === false) return <BetaOnboarding onDone={loadState} />;
  if (!state.diagnostic_completed) return <DiagnosticWelcome />;
  const introKey = `deutschiq-intro-${userId}-${new Date().toISOString().slice(0, 10)}`;
  if (sessionStorage.getItem(introKey)) return <Navigate to="/dashboard" replace />;
  return <ReturningIntro level={state.level || 'A1'} introKey={introKey} />;
};
