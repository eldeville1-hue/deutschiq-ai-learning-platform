import React, { useEffect, useMemo, useState } from 'react';
import { FaArrowRight, FaCheck, FaChevronDown, FaChevronRight, FaCommentDots, FaDownload, FaMedal, FaMoon, FaPaperPlane, FaRedo, FaShareAlt, FaSun, FaTrash } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';
import { getTelegramUser, getUserId, withUser } from '../utils/user';
import { LanguagePicker } from '../components/LanguagePicker';
import { tr } from '../i18n/language';

const CountUp: React.FC<{ value: number }> = ({ value }) => {
  const [shown, setShown] = useState(0);
  useEffect(() => { let frame = 0; const start = performance.now(); const tick = (now: number) => { const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; const p = reduced ? 1 : Math.min(1, (now - start) / 700); setShown(Math.round(value * (1 - Math.pow(1 - p, 3)))); if (p < 1) frame = requestAnimationFrame(tick); }; frame = requestAnimationFrame(tick); return () => cancelAnimationFrame(frame); }, [value]);
  return <>{shown}</>;
};

export const Profile: React.FC = () => {
  const { lang } = useLanguage();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [lessons, setLessons] = useState<any[]>([]);
  const [actionStatus, setActionStatus] = useState('');
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [feedbackText, setFeedbackText] = useState('');
  const user = getTelegramUser();
  const rawName = user?.first_name || '';
  const name = /[\p{L}\p{N}]/u.test(rawName) ? rawName : tr(lang, 'Ученик', 'Lernende', 'Learner');
  const initials = Array.from(name).filter(char => /[\p{L}\p{N}]/u.test(char)).slice(0, 2).join('').toUpperCase() || 'D';
  useEffect(() => { Promise.allSettled([api.getDashboard(getUserId()), api.getPlan(getUserId(), lang)]).then(([d, p]) => { setData(d.status === 'fulfilled' ? d.value : {}); setLessons(p.status === 'fulfilled' && Array.isArray(p.value) ? p.value : []); }); }, [lang]);
  const completed = useMemo(() => lessons.filter(item => item.completed).length, [lessons]);
  if (!data) return <main className="app-shell"><div className="skeleton profile-skeleton" /></main>;
  const retake = () => { const ok = window.confirm(tr(lang, 'Пройти диагностику заново? Новый результат заменит текущую оценку уровня.', 'Diagnose wiederholen? Das neue Ergebnis ersetzt deine aktuelle Einstufung.', 'Retake the placement test? The new result will replace your current level.')); if (ok) navigate(withUser('/diagnostic?retake=true')); };
  const share = () => window.open(`https://t.me/share/url?url=https://t.me/DeutschIQ_bot?start=ref_${getUserId()}&text=DeutschIQ`, '_blank');
  const exportData = async () => {
    try {
      setActionStatus(tr(lang, 'Подготавливаем файл…', 'Datei wird vorbereitet…', 'Preparing your file…'));
      const payload = await api.exportUserData(getUserId());
      const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
      const link = document.createElement('a');
      link.href = url; link.download = 'deutschiq-data.json'; link.click(); URL.revokeObjectURL(url);
      setActionStatus(tr(lang, 'Файл готов.', 'Datei ist bereit.', 'Your file is ready.'));
    } catch { setActionStatus(tr(lang, 'Не удалось скачать данные.', 'Daten konnten nicht geladen werden.', 'Could not download your data.')); }
  };
  const deleteData = async () => {
    const phrase = tr(lang, 'УДАЛИТЬ', 'LÖSCHEN', 'DELETE');
    const entered = window.prompt(tr(lang, `Это навсегда удалит прогресс. Введи ${phrase}`, `Dadurch wird dein Fortschritt endgültig gelöscht. Gib ${phrase} ein.`, `This permanently deletes your progress. Type ${phrase}.`));
    if (entered !== phrase) return;
    try {
      setActionStatus(tr(lang, 'Удаляем данные…', 'Daten werden gelöscht…', 'Deleting your data…'));
      await api.deleteUserData(getUserId());
      localStorage.clear();
      window.location.assign('/');
    } catch { setActionStatus(tr(lang, 'Не удалось удалить данные. Попробуй позже.', 'Daten konnten nicht gelöscht werden. Versuche es später erneut.', 'Could not delete your data. Try again later.')); }
  };
  const resetTestJourney = async () => {
    const ok = window.confirm(tr(lang, 'Начать тестирование как новый пользователь? Текущий учебный прогресс будет удалён.', 'Test als neue Person starten? Dein aktueller Lernfortschritt wird gelöscht.', 'Restart testing as a new user? Your current learning progress will be deleted.'));
    if (!ok) return;
    try {
      setActionStatus(tr(lang, 'Сбрасываем тестовый путь…', 'Testverlauf wird zurückgesetzt…', 'Resetting the test journey…'));
      await api.resetTestJourney(getUserId());
      const savedLanguage = localStorage.getItem('deutschiq_lang');
      const savedTheme = localStorage.getItem('deutschiq_theme');
      localStorage.clear();
      if (savedLanguage) localStorage.setItem('deutschiq_lang', savedLanguage);
      if (savedTheme) localStorage.setItem('deutschiq_theme', savedTheme);
      sessionStorage.clear();
      window.location.assign('/');
    } catch { setActionStatus(tr(lang, 'Не удалось сбросить путь.', 'Testverlauf konnte nicht zurückgesetzt werden.', 'Could not reset the test journey.')); }
  };
  const sendFeedback = async () => {
    const message = feedbackText.trim();
    if (!message) return;
    setActionStatus(tr(lang, 'Отправляем отзыв…', 'Feedback wird gesendet…', 'Sending feedback…'));
    try {
      await api.submitBetaFeedback({ user_id: getUserId(), message, language: lang, page: 'profile' });
      setFeedbackText('');
      setFeedbackOpen(false);
      setActionStatus(tr(lang, 'Спасибо. Отзыв сохранён.', 'Danke. Dein Feedback wurde gespeichert.', 'Thank you. Your feedback was saved.'));
    } catch {
      setActionStatus(tr(lang, 'Не удалось отправить. Попробуй ещё раз.', 'Senden fehlgeschlagen. Versuche es erneut.', 'Could not send it. Please try again.'));
    }
  };
  const weekdays = lang === 'ru' ? ['ПН','ВТ','СР','ЧТ','ПТ','СБ','ВС'] : lang === 'de' ? ['MO','DI','MI','DO','FR','SA','SO'] : ['MO','TU','WE','TH','FR','SA','SU'];
  return (
    <main className="app-shell profile-page precision-profile v30-page v30-profile page-enter">
      <header className="profile-masthead page-stagger-1"><span>{tr(lang, 'ПРОФИЛЬ', 'PROFIL', 'PROFILE')}</span><b>DeutschIQ</b></header>
      <section className="profile-passport page-stagger-1"><div className="avatar">{initials}</div><div><small>{tr(lang, 'УЧЕНИК', 'LERNENDE', 'LEARNER')}</small><h1>{name}</h1><p>{tr(lang, 'Немецкий каждый день', 'Deutsch jeden Tag', 'German every day')}</p></div><strong>{data.level || 'A1'}</strong></section>
      <section className="profile-learning-pass page-stagger-2">
        <header><small>{tr(lang, 'УЧЕБНЫЙ ПРОФИЛЬ', 'LERNPROFIL', 'LEARNING PROFILE')}</small></header>
        <div className="profile-quick-stats">
          <span><b>{completed}</b><small>{tr(lang, 'уроков', 'Lektionen', 'lessons')}</small></span>
          <span><b><CountUp value={data.xp || 0} /></b><small>XP</small></span>
          <span><b>{data.streak || 0}</b><small>{tr(lang, 'дней подряд', 'Tage Serie', 'day streak')}</small></span>
        </div>
        <button type="button" onClick={() => navigate(withUser('/plan'))}>{tr(lang, 'Продолжить обучение', 'Weiterlernen', 'Continue learning')} <FaArrowRight /></button>
      </section>
      <section className="profile-settings page-stagger-3"><div className="profile-language"><strong>{tr(lang, 'Язык интерфейса', 'App-Sprache', 'App language')}</strong><LanguagePicker compact /></div><button onClick={toggleTheme}><span>{theme === 'dark' ? <FaMoon /> : <FaSun />}{tr(lang, 'Оформление', 'Darstellung', 'Appearance')}</span><small>{theme === 'dark' ? tr(lang, 'Тёмное', 'Dunkel', 'Dark') : tr(lang, 'Светлое', 'Hell', 'Light')}</small></button><button onClick={share}><span><FaShareAlt />{tr(lang, 'Пригласить друга', 'Freund einladen', 'Invite a friend')}</span><FaChevronRight /></button></section>
      <details className="profile-progress-details page-stagger-4">
        <summary><span>{tr(lang, 'Активность и достижения', 'Aktivität und Erfolge', 'Activity and achievements')}</span><FaChevronDown /></summary>
        <section className="streak-section"><small>{tr(lang, 'ТВОЯ СЕРИЯ', 'DEINE SERIE', 'YOUR STREAK')}</small><h2>{data.streak || 0} {tr(lang, 'дней', 'Tage', 'days')}</h2><div className="week-row">{weekdays.map((day, index) => <div key={day} style={{ animationDelay: `${index * 55}ms` }}><span>{day}</span><i className={index < (data.streak || 0) ? 'active' : ''} /></div>)}</div></section>
        <section className="achievement-section"><header><small>{tr(lang, 'ДОСТИЖЕНИЯ', 'ERFOLGE', 'ACHIEVEMENTS')}</small><span>1 / 8</span></header><button type="button" className="achievement-card" onClick={() => navigate(withUser('/analytics'))}><FaMedal /><span><b>{tr(lang, 'Первый шаг', 'Erster Schritt', 'First step')}</b><small>{tr(lang, 'Диагностика завершена', 'Diagnose abgeschlossen', 'Placement test completed')} <FaCheck /></small></span><FaChevronRight /></button></section>
      </details>
      <details className="profile-beta-feedback"><summary><FaCommentDots /> {tr(lang, 'Помочь улучшить DeutschIQ', 'DeutschIQ verbessern helfen', 'Help improve DeutschIQ')}</summary><p>{tr(lang, 'Во время беты все функции доступны. Напиши, что было непонятно.', 'Während der Beta sind alle Funktionen verfügbar. Sag uns, was unklar war.', 'All features are available during beta. Tell us what felt unclear.')}</p><button type="button" className="beta-feedback-trigger" onClick={() => setFeedbackOpen(value => !value)}>{tr(lang, 'Написать отзыв', 'Feedback schreiben', 'Write feedback')}</button>{feedbackOpen && <div className="beta-feedback-form"><textarea autoFocus maxLength={800} value={feedbackText} onChange={event => setFeedbackText(event.target.value)} placeholder={tr(lang, 'Что было непонятно или не работало?', 'Was war unklar oder hat nicht funktioniert?', 'What was unclear or did not work?')} /><button type="button" disabled={!feedbackText.trim()} onClick={sendFeedback}><FaPaperPlane /> {tr(lang, 'Отправить', 'Senden', 'Send')}</button></div>}</details>
      <button className="retake-link" onClick={retake}><FaRedo /> {tr(lang, 'Пройти диагностику заново', 'Diagnose wiederholen', 'Retake placement test')}</button>
      <button className="retake-link" onClick={resetTestJourney}><FaRedo /> {tr(lang, 'Начать тестовый путь заново', 'Testverlauf neu starten', 'Restart test journey')}</button>
      <nav className="legal-links"><a href="/privacy">{tr(lang, 'Конфиденциальность', 'Datenschutz', 'Privacy')}</a><a href="/imprint">{tr(lang, 'Информация', 'Impressum', 'Legal')}</a><a href="/terms">{tr(lang, 'Условия', 'Nutzung', 'Terms')}</a></nav>
      <section className="data-controls"><button onClick={exportData}><FaDownload />{tr(lang, 'Скачать мои данные', 'Meine Daten herunterladen', 'Download my data')}</button><button className="danger" onClick={deleteData}><FaTrash />{tr(lang, 'Удалить аккаунт и данные', 'Konto und Daten löschen', 'Delete account and data')}</button></section>
      {actionStatus && <p className="profile-action-status" role="status">{actionStatus}</p>}
      <small className="build-version">DeutschIQ · {tr(lang, 'Персональное обучение немецкому', 'Personalisiertes Deutschlernen', 'Personalised German learning')}</small>
    </main>
  );
};
