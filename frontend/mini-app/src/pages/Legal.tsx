import React from 'react';
import { LanguagePicker } from '../components/LanguagePicker';
import { useLanguage } from '../context/LanguageContext';
import type { AppLanguage } from '../i18n/language';

type LegalKind = 'privacy' | 'imprint' | 'terms';
type Page = { title: string; intro: string; sections: Array<[string, string]> };

const pages: Record<AppLanguage, Record<LegalKind, Page>> = {
  de: {
    privacy: { title: 'Datenschutz', intro: 'Welche Daten DeutschIQ verarbeitet und warum.', sections: [
      ['Verarbeitete Daten', 'Telegram-Nutzer-ID und Profilbasisdaten, Lernfortschritt, Diagnoseantworten, Fehler, Tutor-Nachrichten und technische Protokolle.'],
      ['Zweck', 'Wir speichern deinen Lernstand und erstellen passende Übungen.'],
      ['Dienste', 'DeutschIQ nutzt Telegram, Render, Neon PostgreSQL und optional die OpenAI API. Tutor-Texte können zur Verarbeitung an den KI-Dienst übermittelt werden.'],
      ['Löschen', 'Du kannst deine Daten im Profil exportieren oder dauerhaft löschen.'],
      ['Sicherheit', 'Zugangsdaten bleiben auf dem Server. Teile im Tutor keine sensiblen persönlichen Daten.'],
    ]},
    imprint: { title: 'Impressum', intro: 'Angaben zum Projekt DeutschIQ.', sections: [
      ['Projekt', 'DeutschIQ — eine adaptive Lernanwendung für Deutsch in Telegram.'],
      ['Kontakt', 'Projektanfragen: GitHub-Profil eldeville1-hue.'],
      ['Testphase', 'DeutschIQ befindet sich in einer kostenlosen öffentlichen Testphase. Vor einem kommerziellen Start werden die vollständigen Anbieterangaben ergänzt.'],
    ]},
    terms: { title: 'Nutzungsbedingungen', intro: 'Die wichtigsten Regeln für die Nutzung.', sections: [
      ['Lernhilfe', 'DeutschIQ unterstützt beim Lernen, garantiert aber kein Sprachniveau, Prüfungsergebnis oder fehlerfreie KI-Antworten.'],
      ['Faire Nutzung', 'Der Dienst darf nicht missbräuchlich, rechtswidrig oder automatisiert überlastend genutzt werden.'],
      ['Kostenlose Testphase', 'Alle Lernfunktionen sind derzeit kostenlos. Es werden keine Zahlungen angeboten.'],
      ['Verfügbarkeit', 'Wartung und Produktänderungen können den Dienst vorübergehend einschränken.'],
    ]},
  },
  en: {
    privacy: { title: 'Privacy', intro: 'What DeutschIQ processes and why.', sections: [
      ['Data we process', 'Telegram user ID and basic profile data, learning progress, diagnostic answers, mistakes, tutor messages and technical logs.'],
      ['Purpose', 'We save your progress and provide exercises suited to your learning needs.'],
      ['Services', 'DeutschIQ uses Telegram, Render, Neon PostgreSQL and optionally the OpenAI API. Tutor text may be sent to the AI service for processing.'],
      ['Deletion', 'You can export or permanently delete your data from your profile.'],
      ['Security', 'Credentials remain on the server. Do not enter sensitive personal data in the tutor.'],
    ]},
    imprint: { title: 'Legal notice', intro: 'Information about the DeutschIQ project.', sections: [
      ['Project', 'DeutschIQ — an adaptive German-learning application for Telegram.'],
      ['Contact', 'Project enquiries: GitHub profile eldeville1-hue.'],
      ['Testing phase', 'DeutschIQ is currently in a free public testing phase. Full provider details will be added before commercial launch.'],
    ]},
    terms: { title: 'Terms of use', intro: 'The key rules for using DeutschIQ.', sections: [
      ['Learning aid', 'DeutschIQ supports learning but does not guarantee a language level, exam result or error-free AI answers.'],
      ['Fair use', 'Do not misuse, overload or use the service for unlawful content.'],
      ['Free testing phase', 'All learning features are currently free. No payments are offered.'],
      ['Availability', 'Maintenance and product changes may temporarily limit the service.'],
    ]},
  },
  ru: {
    privacy: { title: 'Конфиденциальность', intro: 'Какие данные обрабатывает DeutschIQ и зачем.', sections: [
      ['Данные', 'Telegram ID и основные данные профиля, прогресс, ответы диагностики, ошибки, сообщения репетитору и технические журналы.'],
      ['Цель', 'Мы сохраняем прогресс и подбираем упражнения под ваши учебные потребности.'],
      ['Сервисы', 'DeutschIQ использует Telegram, Render, Neon PostgreSQL и, при необходимости, OpenAI API. Текст для репетитора может передаваться ИИ-сервису.'],
      ['Удаление', 'Данные можно экспортировать или навсегда удалить в профиле.'],
      ['Безопасность', 'Ключи доступа остаются на сервере. Не отправляйте репетитору конфиденциальные личные данные.'],
    ]},
    imprint: { title: 'Правовая информация', intro: 'Информация о проекте DeutschIQ.', sections: [
      ['Проект', 'DeutschIQ — адаптивное приложение для изучения немецкого в Telegram.'],
      ['Контакт', 'Вопросы по проекту: профиль GitHub eldeville1-hue.'],
      ['Тестирование', 'Сейчас DeutschIQ проходит бесплатное публичное тестирование. Полные данные поставщика будут добавлены до коммерческого запуска.'],
    ]},
    terms: { title: 'Условия использования', intro: 'Главные правила использования DeutschIQ.', sections: [
      ['Учебный сервис', 'DeutschIQ помогает учиться, но не гарантирует уровень языка, результат экзамена или безошибочные ответы ИИ.'],
      ['Добросовестное использование', 'Нельзя использовать сервис незаконно, злоупотреблять им или создавать автоматическую перегрузку.'],
      ['Бесплатное тестирование', 'Сейчас все учебные функции бесплатны. Платежей нет.'],
      ['Доступность', 'Технические работы и изменения продукта могут временно ограничивать сервис.'],
    ]},
  },
};

export const Legal: React.FC<{ kind: LegalKind }> = ({ kind }) => {
  const { lang } = useLanguage();
  const page = pages[lang][kind];
  const links = lang === 'ru' ? ['Конфиденциальность', 'Информация', 'Условия', 'Контакт'] : lang === 'de' ? ['Datenschutz', 'Impressum', 'Nutzung', 'Kontakt'] : ['Privacy', 'Legal notice', 'Terms', 'Contact'];
  return <main className="legal-page">
    <div className="legal-top"><a className="legal-brand" href="/">D <span>DeutschIQ</span></a><LanguagePicker compact /></div>
    <p className="eyebrow">LEGAL</p><h1>{page.title}</h1><p className="legal-intro">{page.intro}</p>
    {page.sections.map(([heading, body]) => <section key={heading}><h2>{heading}</h2><p>{body}</p></section>)}
    <footer><a href="/privacy">{links[0]}</a><a href="/imprint">{links[1]}</a><a href="/terms">{links[2]}</a><a href="https://github.com/eldeville1-hue" target="_blank" rel="noreferrer">{links[3]}</a></footer>
  </main>;
};
