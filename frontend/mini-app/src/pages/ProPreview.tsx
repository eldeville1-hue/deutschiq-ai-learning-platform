import { useEffect, useState } from 'react';
import { FaCheck, FaClock, FaCrown, FaRedo } from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import { tr } from '../i18n/language';
import { getUserId } from '../utils/user';

const features = [
  ['A1–B2', 'A1–B2', 'A1–B2'],
  ['Безлимитные повторения', 'Unbegrenzte Wiederholungen', 'Unlimited reviews'],
  ['AI-репетитор и разбор ошибок', 'KI-Tutor und Fehleranalyse', 'AI tutor and mistake analysis'],
  ['Полная аналитика прогресса', 'Vollständige Lernanalyse', 'Complete progress analytics'],
] as const;

export const ProPreview = () => {
  const { lang } = useLanguage();
  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState('');
  useEffect(() => {
    void api.getDashboard(getUserId()).then(setData).catch(() => setData({ beta_free: true, payments_enabled: false, pro_price_stars: 700 }));
    void api.trackEvent({ user_id: getUserId(), event_name: 'pro_preview_viewed', properties: { language: lang } });
  }, [lang]);
  const beta = data?.beta_free !== false || !data?.payments_enabled;
  const interested = () => {
    if (!beta) {
      const url = 'https://t.me/DeutschIQ_bot?start=subscribe';
      const telegram = (window as any).Telegram?.WebApp;
      if (telegram?.openTelegramLink) telegram.openTelegramLink(url);
      else window.open(url, '_blank', 'noopener,noreferrer');
      return;
    }
    void api.trackEvent({ user_id: getUserId(), event_name: 'pro_interest_clicked', properties: { language: lang, price_stars: data?.pro_price_stars || 700 } });
    setStatus(tr(lang, 'Записано. Во время беты платить не нужно.', 'Gespeichert. Während der Beta musst du nichts bezahlen.', 'Saved. You do not need to pay during beta.'));
  };
  const restore = () => {
    void api.trackEvent({ user_id: getUserId(), event_name: 'subscription_restore_requested', properties: { language: lang } });
    setStatus(tr(lang, 'Платных покупок пока нет. Бета-доступ уже активен.', 'Es gibt noch keine bezahlten Käufe. Dein Beta-Zugang ist aktiv.', 'There are no paid purchases yet. Your beta access is already active.'));
  };
  return <main className="app-shell pro-preview page-enter">
    <header className="pro-preview-hero"><FaCrown/><small>DEUTSCHIQ PRO · PREVIEW</small><h1>{tr(lang,'Учись без ограничений','Lerne ohne Grenzen','Learn without limits')}</h1><p>{tr(lang,'Предварительный экран будущей подписки. Сейчас вся бета бесплатна.','Vorschau auf das künftige Abo. Die gesamte Beta ist derzeit kostenlos.','Preview of the future subscription. The entire beta is free right now.')}</p></header>
    <section className="pro-plan-card"><div className="pro-price"><span>{data?.pro_price_stars || 700} <b>Stars</b></span><small>{tr(lang,'за 30 дней','für 30 Tage','for 30 days')}</small></div><ul>{features.map(row=><li key={row[2]}><FaCheck/><span>{row[lang === 'ru' ? 0 : lang === 'de' ? 1 : 2]}</span></li>)}</ul></section>
    <section className="pro-beta-notice"><FaClock/><div><strong>{tr(lang,'Платный запуск ещё закрыт','Der Bezahlstart ist noch geschlossen','Paid launch is still closed')}</strong><p>{tr(lang,'Мы не спишем Stars. Цена и преимущества показаны только для проверки спроса во время закрытой беты.','Es werden keine Stars abgebucht. Preis und Vorteile dienen nur der Nachfrageprüfung in der geschlossenen Beta.','No Stars will be charged. Price and benefits are shown only to test demand during the closed beta.')}</p></div></section>
    <button className="pro-interest" type="button" onClick={interested}>{beta ? tr(lang,'Мне интересен Pro','Ich interessiere mich für Pro','I am interested in Pro') : tr(lang,'Открыть подписку в Telegram','Abo in Telegram öffnen','Open subscription in Telegram')}</button>
    <button className="pro-restore" type="button" onClick={restore}><FaRedo/>{tr(lang,'Восстановить доступ','Zugang wiederherstellen','Restore access')}</button>
    {status && <p className="pro-status" role="status">{status}</p>}
    <nav className="pro-legal"><a href="/terms">{tr(lang,'Условия','Bedingungen','Terms')}</a><a href="/privacy">{tr(lang,'Конфиденциальность','Datenschutz','Privacy')}</a><a href="/imprint">{tr(lang,'Информация','Impressum','Legal')}</a></nav>
  </main>;
};
