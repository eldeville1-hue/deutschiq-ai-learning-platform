import React from 'react';
import { FaArrowRight, FaBrain, FaCheck, FaGithub, FaTelegramPlane } from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';
import { LanguagePicker } from '../components/LanguagePicker';
import { tr } from '../i18n/language';

const telegramUrl = 'https://t.me/DeutschIQ_bot';
const githubUrl = 'https://github.com/eldeville1-hue/deutschiq-ai-learning-platform';

export const Portfolio: React.FC = () => {
  const { lang } = useLanguage();
  return (
  <main className="portfolio-page">
    <nav className="portfolio-nav">
      <a className="portfolio-logo" href="/"><b>D</b><span>DeutschIQ</span></a>
      <div><LanguagePicker compact /><a href={githubUrl} target="_blank" rel="noreferrer"><FaGithub /> {tr(lang, 'Код', 'Code', 'Code')}</a><a className="nav-launch" href={telegramUrl} target="_blank" rel="noreferrer">Telegram <FaArrowRight /></a></div>
    </nav>

    <section className="portfolio-hero">
      <div className="hero-copy">
        <p className="portfolio-kicker"><i /> LIVE · TELEGRAM MINI APP</p>
        <h1>{tr(lang, 'Немецкий, который помнит твои ошибки.', 'Deutsch, das sich deine Fehler merkt.', 'German that remembers your mistakes.')}</h1>
        <p className="portfolio-lead">{tr(lang, 'Диагностика, персональный маршрут и ИИ‑репетитор — в одном Telegram-приложении.', 'Einstufung, persönlicher Lernweg und KI‑Tutor in einer Telegram-App.', 'Placement, a personal learning path and an AI tutor in one Telegram app.')}</p>
        <div className="portfolio-actions"><a className="launch-primary" href={telegramUrl} target="_blank" rel="noreferrer"><FaTelegramPlane /> {tr(lang, 'Открыть DeutschIQ', 'DeutschIQ öffnen', 'Open DeutschIQ')} <FaArrowRight /></a><a href={githubUrl} target="_blank" rel="noreferrer"><FaGithub /> {tr(lang, 'Посмотреть код', 'Code ansehen', 'View code')}</a></div>
        <div className="portfolio-proof"><span><b>30</b> {tr(lang, 'уроков', 'Lektionen', 'lessons')}</span><span><b>120</b> {tr(lang, 'заданий', 'Aufgaben', 'exercises')}</span><span><b>A1—B2</b> {tr(lang, 'маршрут', 'Lernweg', 'path')}</span></div>
      </div>
      <div className="hero-device" aria-label="DeutschIQ mobile application preview">
        <div className="device-glow"/><div className="phone-frame"><span className="phone-island"/><img src="/portfolio/01-home.png" alt="DeutschIQ personalized home screen" /></div>
        <span className="floating-note note-top"><FaBrain /><b>Adaptive</b><small>learning engine</small></span>
        <span className="floating-note note-bottom"><FaCheck /><b>Server-side</b><small>answer validation</small></span>
      </div>
    </section>

    <section className="portfolio-system">
      <header><p className="portfolio-kicker">PRODUCT SYSTEM</p><h2>{tr(lang, 'Не набор экранов. Один учебный цикл.', 'Keine Sammlung von Screens. Ein Lernkreislauf.', 'Not a set of screens. One learning loop.')}</h2></header>
      <div className="system-steps"><article><b>01</b><h3>{tr(lang, 'Диагностика', 'Einstufung', 'Placement')}</h3><p>{tr(lang, 'Определяет уровень и реальные пробелы.', 'Ermittelt Niveau und echte Wissenslücken.', 'Finds your level and real knowledge gaps.')}</p></article><article><b>02</b><h3>{tr(lang, 'Практика', 'Übung', 'Practice')}</h3><p>{tr(lang, 'Подбирает следующий урок по твоим ответам.', 'Wählt die nächste Lektion aus deinen Antworten.', 'Selects the next lesson from your answers.')}</p></article><article><b>03</b><h3>{tr(lang, 'Повторение', 'Wiederholung', 'Review')}</h3><p>{tr(lang, 'Возвращает тему в нужный момент.', 'Bringt ein Thema zum richtigen Zeitpunkt zurück.', 'Brings each topic back at the right time.')}</p></article></div>
    </section>

    <section className="portfolio-screens">
      <header><p className="portfolio-kicker">INSIDE THE APP</p><h2>{tr(lang, 'У каждой страницы своя задача.', 'Jede Seite hat eine klare Aufgabe.', 'Every page has one clear job.')}</h2></header>
      <div className="screen-gallery"><figure><img src="/portfolio/05-analytics.png" alt="DeutschIQ learning analytics"/><figcaption><b>{tr(lang, 'Анализ', 'Analyse', 'Analysis')}</b><span>{tr(lang, 'Картина знаний', 'Wissensprofil', 'Knowledge profile')}</span></figcaption></figure><figure><img src="/portfolio/06-ai-tutor.png" alt="DeutschIQ AI tutor"/><figcaption><b>{tr(lang, 'ИИ‑репетитор', 'KI‑Tutor', 'AI tutor')}</b><span>{tr(lang, 'Диалог и практика', 'Dialog und Übung', 'Conversation and practice')}</span></figcaption></figure><figure><img src="/portfolio/07-profile.png" alt="DeutschIQ learner profile"/><figcaption><b>{tr(lang, 'Профиль', 'Profil', 'Profile')}</b><span>{tr(lang, 'История и настройки', 'Verlauf und Einstellungen', 'History and settings')}</span></figcaption></figure></div>
    </section>

    <section className="portfolio-tech"><p className="portfolio-kicker">ENGINEERING</p><h2>{tr(lang, 'Создано как реальный full-stack продукт.', 'Als echtes Full-Stack-Produkt entwickelt.', 'Built as a real full-stack product.')}</h2><div><span>React + TypeScript</span><span>FastAPI</span><span>PostgreSQL</span><span>Telegram WebApp</span><span>OpenAI API</span><span>Docker + Render</span></div></section>
    <section className="portfolio-final"><span className="portfolio-logo"><b>D</b></span><h2>{tr(lang, 'Начни с точной точки.', 'Starte am richtigen Punkt.', 'Start at the right point.')}</h2><p>{tr(lang, 'Открой бота, пройди диагностику и получи свой маршрут.', 'Öffne den Bot, mache die Einstufung und erhalte deinen Lernweg.', 'Open the bot, take the placement test and get your path.')}</p><a className="launch-primary" href={telegramUrl} target="_blank" rel="noreferrer"><FaTelegramPlane /> {tr(lang, 'Открыть', 'Öffnen', 'Open')} @DeutschIQ_bot <FaArrowRight /></a></section>
    <footer className="portfolio-footer"><span>DeutschIQ · Portfolio project</span><nav><a href="/privacy">Datenschutz</a><a href="/imprint">Impressum</a><a href="/terms">Nutzung</a></nav></footer>
  </main>
  );
};
