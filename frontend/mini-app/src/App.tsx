import { lazy, Suspense, useEffect, useLayoutEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import { ThemeProvider } from './context/ThemeContext';
import { AppBackButton } from './components/AppBackButton';
import { BrandMark } from './components/BrandMark';
import { BottomNav } from './components/BottomNav';
import { BetaIssueReporter } from './components/BetaIssueReporter';
import { getTelegramUser, hasTelegramIdentity } from './utils/user';
import { normalizeLanguage, tr } from './i18n/language';
import './styles/global.css';

const Entry = lazy(() => import('./pages/Entry').then(module => ({ default: module.Entry })));
const Dashboard = lazy(() => import('./pages/Dashboard').then(module => ({ default: module.Dashboard })));
const Diagnostic = lazy(() => import('./pages/Diagnostic').then(module => ({ default: module.Diagnostic })));
const Lesson = lazy(() => import('./pages/Lesson').then(module => ({ default: module.Lesson })));
const Plan = lazy(() => import('./pages/Plan').then(module => ({ default: module.Plan })));
const Tutor = lazy(() => import('./pages/Tutor').then(module => ({ default: module.Tutor })));
const Result = lazy(() => import('./pages/Result').then(module => ({ default: module.Result })));
const Profile = lazy(() => import('./pages/Profile').then(module => ({ default: module.Profile })));
const Analytics = lazy(() => import('./pages/Analytics').then(module => ({ default: module.Analytics })));
const Mistakes = lazy(() => import('./pages/Mistakes').then(module => ({ default: module.Mistakes })));
const Review = lazy(() => import('./pages/Review').then(module => ({ default: module.Review })));
const Legal = lazy(() => import('./pages/Legal').then(module => ({ default: module.Legal })));
const Portfolio = lazy(() => import('./pages/Portfolio').then(module => ({ default: module.Portfolio })));
const Checkpoint = lazy(() => import('./pages/Checkpoint').then(module => ({ default: module.Checkpoint })));
const ControlCenter = lazy(() => import('./pages/ControlCenter').then(module => ({ default: module.ControlCenter })));

function ConnectionStatus() {
  const { lang } = useLanguage();
  const [online, setOnline] = useState(() => navigator.onLine);
  useEffect(() => {
    const connected = () => setOnline(true);
    const disconnected = () => setOnline(false);
    window.addEventListener('online', connected);
    window.addEventListener('offline', disconnected);
    return () => {
      window.removeEventListener('online', connected);
      window.removeEventListener('offline', disconnected);
    };
  }, []);
  if (online) return null;
  return <div className="connection-status" role="status">{tr(lang, 'Нет сети · сохранённые данные доступны', 'Offline · gespeicherte Daten sind verfügbar', 'Offline · saved data remains available')}</div>;
}

function AppRoutes() {
  const location = useLocation();
  useLayoutEffect(() => {
    if ('scrollRestoration' in window.history) window.history.scrollRestoration = 'manual';

    const resetScroll = () => {
      window.scrollTo(0, 0);
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
      document.querySelectorAll<HTMLElement>('.app-shell').forEach(page => {
        page.scrollTo({ top: 0, left: 0, behavior: 'auto' });
      });
    };

    resetScroll();
    const frame = window.requestAnimationFrame(resetScroll);
    const timer = window.setTimeout(resetScroll, 160);
    return () => {
      window.cancelAnimationFrame(frame);
      window.clearTimeout(timer);
    };
  }, [location.key]);
  const legalKind = ({ '/privacy': 'privacy', '/imprint': 'imprint', '/terms': 'terms' } as const)[location.pathname as '/privacy' | '/imprint' | '/terms'];
  const portfolioRoute = location.pathname === '/about';
  if (location.pathname === '/control-center') return <Suspense fallback={<main className="entry-loading"><div className="analysis-loader" /></main>}><ControlCenter /></Suspense>;
  const outsideTelegram = !import.meta.env.DEV && (window as any).Telegram?.WebApp?.platform === 'unknown';
  if (legalKind) return <Suspense fallback={<main className="entry-loading"><div className="analysis-loader" /></main>}><Legal kind={legalKind} /></Suspense>;
  if (portfolioRoute || (outsideTelegram && location.pathname === '/')) return <Suspense fallback={<main className="entry-loading"><div className="analysis-loader" /></main>}><Portfolio /></Suspense>;
  const primaryRoutes = ['/dashboard', '/analytics', '/plan', '/tutor', '/profile'];
  const hasBackButton = !['/', ...primaryRoutes].includes(location.pathname);
  const showPrimaryNav = primaryRoutes.includes(location.pathname);
  return (
    <div className={`app-frame${hasBackButton ? ' has-back-button' : ''}`}>
      <ConnectionStatus />
      <AppBackButton />
      <Suspense fallback={<div className="route-skeleton"><div className="skeleton" /><div className="skeleton" /><div className="skeleton" /></div>}>
        <Routes location={location}>
          <Route path="/" element={<Entry />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/diagnostic" element={<Diagnostic />} />
          <Route path="/lesson/:id" element={<Lesson />} />
          <Route path="/plan" element={<Plan />} />
          <Route path="/tutor" element={<Tutor />} />
          <Route path="/result" element={<Result />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/mistakes" element={<Mistakes />} />
          <Route path="/review" element={<Review />} />
          <Route path="/checkpoint/:level" element={<Checkpoint />} />
        </Routes>
      </Suspense>
      {showPrimaryNav && <BottomNav />}
      {showPrimaryNav && <BetaIssueReporter />}
    </div>
  );
}

type BootstrapState = 'waiting' | 'ready' | 'missing';

function TelegramBootstrap() {
  const developmentIdentity = import.meta.env.DEV && Boolean(import.meta.env.VITE_DEV_USER_ID);
  const publicPage = ['/about', '/privacy', '/imprint', '/terms', '/control-center'].includes(window.location.pathname)
    || (window as any).Telegram?.WebApp?.platform === 'unknown';
  const [state, setState] = useState<BootstrapState>(() => (
    hasTelegramIdentity() || developmentIdentity || publicPage ? 'ready' : 'waiting'
  ));
  const preferredLanguage = normalizeLanguage(
    localStorage.getItem('deutschiq_lang') || getTelegramUser()?.language_code,
  );

  useEffect(() => {
    if (state === 'ready') return;
    const webApp = (window as any).Telegram?.WebApp;
    webApp?.ready?.();
    webApp?.expand?.();

    const startedAt = Date.now();
    const timer = window.setInterval(() => {
      if (hasTelegramIdentity()) {
        setState('ready');
        window.clearInterval(timer);
      } else if (Date.now() - startedAt >= 10_000) {
        setState('missing');
        window.clearInterval(timer);
      }
    }, 150);
    return () => window.clearInterval(timer);
  }, [state]);

  if (state === 'waiting') return <main className="entry-loading"><BrandMark label="DeutschIQ" /><div className="analysis-loader" /></main>;
  if (state === 'missing') return (
    <main className="auth-error">
      <BrandMark label="DeutschIQ" />
      <h1>{tr(preferredLanguage, 'Открой DeutschIQ в Telegram', 'Öffne DeutschIQ in Telegram', 'Open DeutschIQ in Telegram')}</h1>
      <p>{tr(preferredLanguage, 'Запусти приложение через @DeutschIQ_bot.', 'Starte die App über @DeutschIQ_bot.', 'Launch the app through @DeutschIQ_bot.')}</p>
      <a className="primary-action" href="https://t.me/DeutschIQ_bot">{tr(preferredLanguage, 'Открыть Telegram', 'Telegram öffnen', 'Open Telegram')}</a>
      <button className="secondary-action" type="button" onClick={() => window.location.reload()}>{tr(preferredLanguage, 'Повторить', 'Erneut versuchen', 'Try again')}</button>
    </main>
  );

  // Providers that read Telegram identity mount only after the signed payload is
  // available. This prevents an initial user 0 request and duplicate bootstrap.
  return (
    <LanguageProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </LanguageProvider>
  );
}

function App() {
  return (
    <ThemeProvider>
      <TelegramBootstrap />
    </ThemeProvider>
  );
}
export default App;
