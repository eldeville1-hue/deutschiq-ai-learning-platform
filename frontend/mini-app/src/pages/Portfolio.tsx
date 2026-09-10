import React from 'react';
import { FaArrowRight, FaBrain, FaCheck, FaGithub, FaTelegramPlane } from 'react-icons/fa';

const telegramUrl = 'https://t.me/DeutschIQ_bot';
const githubUrl = 'https://github.com/eldeville1-hue/deutschiq-ai-learning-platform';

export const Portfolio: React.FC = () => (
  <main className="portfolio-page">
    <nav className="portfolio-nav">
      <a className="portfolio-logo" href="/"><b>D</b><span>DeutschIQ</span></a>
      <div><a href={githubUrl} target="_blank" rel="noreferrer"><FaGithub /> Code</a><a className="nav-launch" href={telegramUrl} target="_blank" rel="noreferrer">Telegram <FaArrowRight /></a></div>
    </nav>

    <section className="portfolio-hero">
      <div className="hero-copy">
        <p className="portfolio-kicker"><i /> LIVE · TELEGRAM MINI APP</p>
        <h1>Немецкий, который<br/><em>помнит твои ошибки.</em></h1>
        <p className="portfolio-lead">Адаптивная диагностика, персональный 30-дневный маршрут и ИИ‑репетитор — в одном Telegram-приложении.</p>
        <div className="portfolio-actions"><a className="launch-primary" href={telegramUrl} target="_blank" rel="noreferrer"><FaTelegramPlane /> Открыть DeutschIQ <FaArrowRight /></a><a href={githubUrl} target="_blank" rel="noreferrer"><FaGithub /> Посмотреть код</a></div>
        <div className="portfolio-proof"><span><b>30</b> уроков</span><span><b>120</b> заданий</span><span><b>A1—B2</b> траектория</span></div>
      </div>
      <div className="hero-device" aria-label="DeutschIQ mobile application preview">
        <div className="device-glow"/><div className="phone-frame"><span className="phone-island"/><img src="/portfolio/01-home.png" alt="DeutschIQ personalized home screen" /></div>
        <span className="floating-note note-top"><FaBrain /><b>Adaptive</b><small>learning engine</small></span>
        <span className="floating-note note-bottom"><FaCheck /><b>Server-side</b><small>answer validation</small></span>
      </div>
    </section>

    <section className="portfolio-system">
      <header><p className="portfolio-kicker">PRODUCT SYSTEM</p><h2>Не набор экранов.<br/>Один учебный цикл.</h2></header>
      <div className="system-steps"><article><b>01</b><h3>Диагностика</h3><p>Определяет уровень и реальные пробелы без раскрытия ответов.</p></article><article><b>02</b><h3>Практика</h3><p>Даёт следующий урок, опираясь на ошибки и удержание знаний.</p></article><article><b>03</b><h3>Повторение</h3><p>Возвращает тему в нужный момент и обновляет mastery.</p></article></div>
    </section>

    <section className="portfolio-screens">
      <header><p className="portfolio-kicker">INSIDE THE APP</p><h2>Каждая страница —<br/>своё действие.</h2></header>
      <div className="screen-gallery"><figure><img src="/portfolio/05-analytics.png" alt="DeutschIQ learning analytics"/><figcaption><b>Анализ</b><span>Картина знаний</span></figcaption></figure><figure><img src="/portfolio/06-ai-tutor.png" alt="DeutschIQ AI tutor"/><figcaption><b>ИИ‑репетитор</b><span>Диалог и практика</span></figcaption></figure><figure><img src="/portfolio/07-profile.png" alt="DeutschIQ learner profile"/><figcaption><b>Профиль</b><span>История и настройки</span></figcaption></figure></div>
    </section>

    <section className="portfolio-tech"><p className="portfolio-kicker">ENGINEERING</p><h2>Создано как реальный full-stack продукт.</h2><div><span>React + TypeScript</span><span>FastAPI</span><span>PostgreSQL</span><span>Telegram WebApp</span><span>OpenAI API</span><span>Docker + Render</span></div></section>
    <section className="portfolio-final"><span className="portfolio-logo"><b>D</b></span><h2>Начни с точной точки.</h2><p>Открой бота, пройди диагностику и получи свой первый маршрут.</p><a className="launch-primary" href={telegramUrl} target="_blank" rel="noreferrer"><FaTelegramPlane /> Открыть @DeutschIQ_bot <FaArrowRight /></a></section>
    <footer className="portfolio-footer"><span>DeutschIQ · Portfolio project</span><nav><a href="/privacy">Datenschutz</a><a href="/imprint">Impressum</a><a href="/terms">Nutzung</a></nav></footer>
  </main>
);
