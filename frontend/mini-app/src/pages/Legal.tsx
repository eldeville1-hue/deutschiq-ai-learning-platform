import React from 'react';

type LegalKind = 'privacy' | 'imprint' | 'terms';
const pages: Record<LegalKind, { title: string; intro: string; sections: Array<[string, string]> }> = {
  privacy: { title: 'Datenschutzerklärung', intro: 'Diese Seite erklärt transparent, welche Daten die DeutschIQ Lernanwendung verarbeitet.', sections: [
    ['Verarbeitete Daten', 'Telegram-Nutzer-ID und Profilbasisdaten, Lernfortschritt, Diagnoseantworten, Fehler, Tutor-Nachrichten und technische Protokolle.'],
    ['Zweck', 'Die Daten werden verwendet, um den Lernstand zu speichern, personalisierte Übungen bereitzustellen und den Dienst sicher zu betreiben.'],
    ['Dienste', 'Die Anwendung nutzt Telegram, Render, Neon PostgreSQL und optional die OpenAI API. Bei Tutor-Anfragen wird der eingegebene Text an den KI-Dienst übermittelt.'],
    ['Speicherung und Löschung', 'Daten bleiben gespeichert, solange DeutschIQ genutzt wird. Export und dauerhafte Löschung sind direkt im Profil verfügbar.'],
    ['Sicherheit', 'Zugangsdaten werden als Server-Secrets gespeichert und nicht an den Browser ausgeliefert. Bitte keine sensiblen persönlichen Daten in den Tutor eingeben.'],
  ]},
  imprint: { title: 'Impressum', intro: 'DeutschIQ ist derzeit ein nicht-kommerzielles Portfolio- und Lernprojekt.', sections: [
    ['Projekt', 'DeutschIQ — AI-powered Telegram Mini App for adaptive German learning.'],
    ['Kontakt', 'Kontakt und Projektanfragen erfolgen derzeit über das öffentliche GitHub-Profil eldeville1-hue.'],
    ['Hinweis', 'Vor einem kommerziellen Betrieb müssen vollständige Anbieterangaben, eine ladungsfähige Anschrift und weitere rechtlich erforderliche Informationen ergänzt werden.'],
  ]},
  terms: { title: 'Nutzungsbedingungen', intro: 'Mit der Nutzung von DeutschIQ gelten die folgenden Bedingungen.', sections: [
    ['Lernhilfe', 'DeutschIQ ist eine Lernhilfe und garantiert kein bestimmtes Sprachniveau, Prüfungsergebnis oder fehlerfreie KI-Antworten.'],
    ['Zulässige Nutzung', 'Die Anwendung darf nicht missbräuchlich, automatisiert überlastend oder zur Verarbeitung rechtswidriger Inhalte genutzt werden.'],
    ['Pro-Zugang', 'Ein über Telegram Stars gekaufter Pro-Zugang gilt 30 Tage ab erfolgreicher Zahlung. Der aktuelle Status und das Enddatum werden im Profil angezeigt.'],
    ['Verfügbarkeit', 'Der Dienst kann für Wartung oder notwendige Produktänderungen vorübergehend eingeschränkt sein.'],
  ]},
};

export const Legal: React.FC<{ kind: LegalKind }> = ({ kind }) => {
  const page = pages[kind];
  return <main className="legal-page">
    <a className="legal-brand" href="/">D <span>DeutschIQ</span></a><p className="eyebrow">LEGAL</p>
    <h1>{page.title}</h1><p className="legal-intro">{page.intro}</p>
    {page.sections.map(([heading, body]) => <section key={heading}><h2>{heading}</h2><p>{body}</p></section>)}
    <footer><a href="/privacy">Datenschutz</a><a href="/imprint">Impressum</a><a href="/terms">Nutzung</a><a href="https://github.com/eldeville1-hue" target="_blank" rel="noreferrer">GitHub-Kontakt</a></footer>
  </main>;
};
