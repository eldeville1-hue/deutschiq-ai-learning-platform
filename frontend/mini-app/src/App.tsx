import { lazy, Suspense, useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import { ThemeProvider } from './context/ThemeContext';
import { AppBackButton } from './components/AppBackButton';
import { hasTelegramIdentity } from './utils/user';
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

function AppRoutes() {
  const location = useLocation();
  const [telegramReady, setTelegramReady] = useState(() => hasTelegramIdentity());
  const [bootstrapFinished, setBootstrapFinished] = useState(false);
  useEffect(() => {
    if (telegramReady) { setBootstrapFinished(true); return; }
    let attempts = 0;
    const timer = window.setInterval(() => {
      attempts += 1;
      if (hasTelegramIdentity()) {
        setTelegramReady(true);
        setBootstrapFinished(true);
        window.clearInterval(timer);
      } else if (attempts >= 20) {
        setBootstrapFinished(true);
        window.clearInterval(timer);
      }
    }, 100);
    return () => window.clearInterval(timer);
  }, [telegramReady]);
  const authenticated = telegramReady || (import.meta.env.DEV && Boolean(import.meta.env.VITE_DEV_USER_ID));
  if (!bootstrapFinished) return <main className="entry-loading"><div className="brand-mark">D</div><div className="analysis-loader" /></main>;
  if (!authenticated) return <main className="auth-error"><div className="brand-mark">D</div><h1>Не удалось получить данные Telegram</h1><p>Закрой Mini App и открой его снова кнопкой «Открыть DeutschIQ» в боте.</p><button className="primary-action" onClick={() => window.location.reload()}>Повторить</button></main>;
  const hasBackButton = !['/', '/dashboard', '/analytics', '/plan', '/tutor', '/profile'].includes(location.pathname);
  return (
    <div className={hasBackButton ? 'has-back-button' : undefined}>
      <AppBackButton />
      <Suspense fallback={<div className="route-skeleton"><div className="skeleton" /><div className="skeleton" /><div className="skeleton" /></div>}>
        <Routes>
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
        </Routes>
      </Suspense>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </LanguageProvider>
    </ThemeProvider>
  );
}
export default App;
