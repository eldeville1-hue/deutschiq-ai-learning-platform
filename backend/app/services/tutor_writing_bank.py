"""Open-ended B1/B2 writing tasks; no automatic grades."""
WRITING_PROMPTS = (
    ("b1-w01", "B1", "Schreibe eine E-Mail an deine Sprachschule. Du kannst morgen nicht zum Kurs kommen.", "Erkläre den Grund, entschuldige dich und frage nach den Hausaufgaben.", "80-100"),
    ("b1-w02", "B1", "Sollte man jeden Tag Sport treiben? Schreibe deine Meinung.", "Nenne einen Vorteil, einen Nachteil und deine Erfahrung.", "80-120"),
    ("b1-w03", "B1", "Du möchtest eine Wohnung besichtigen. Schreibe an den Vermieter.", "Stelle dich vor, frage nach einem Termin und einer Information.", "80-100"),
    ("b2-w01", "B2", "Sollte KI im Unterricht eingesetzt werden? Eroertere die Frage.", "Beschreibe Chancen und Risiken, begruende deine Position und ziehe ein Fazit.", "150-200"),
    ("b2-w02", "B2", "Immer mehr Menschen arbeiten im Homeoffice. Verfasse einen argumentativen Text.", "Diskutiere Vor- und Nachteile und begruende deine Meinung.", "150-200"),
    ("b2-w03", "B2", "Schreibe eine formelle Beschwerde ueber einen verspaeteten Online-Einkauf.", "Beschreibe das Problem, die Folgen und deine gewuenschte Loesung.", "120-180"),
)
WRITING_CRITERIA = {
    "ru": "Самопроверка: содержание; грамматика; словарный запас; связность и структура. Открытый ответ не получает автоматическую оценку.",
    "de": "Selbstcheck: Inhalt; Grammatik; Wortschatz; Kohaerenz und Aufbau. Keine automatische Bewertung offener Texte.",
    "en": "Self-check: content; grammar; vocabulary; coherence and structure. Open writing is not automatically graded.",
}
