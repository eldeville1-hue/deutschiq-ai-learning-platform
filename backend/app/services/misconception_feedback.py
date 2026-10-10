"""Short, actionable feedback for the mistakes DeutschIQ is designed to diagnose."""

FEEDBACK = {
    "verb_not_final": ("Поставь спрягаемый глагол в конец придаточного.", "Setze das konjugierte Verb ans Ende des Nebensatzes.", "Move the conjugated verb to the end of the subordinate clause."),
    "wrong_connector": ("Сначала определи смысл: время, причина, условие или контраст.", "Bestimme zuerst die Bedeutung: Zeit, Grund, Bedingung oder Gegensatz.", "Identify the meaning first: time, reason, condition, or contrast."),
    "relative_case": ("Определи падеж местоимения по его роли внутри Relativsatz.", "Bestimme den Kasus des Pronomens aus seiner Rolle im Relativsatz.", "Choose the pronoun case from its role inside the relative clause."),
    "passive_auxiliary": ("Выбери форму werden и поставь Partizip II в конец.", "Wähle die passende Form von werden und setze das Partizip II ans Ende.", "Choose the correct form of werden and place the past participle at the end."),
    "modal_form": ("Проверь форму модального глагола и инфинитив в конце.", "Prüfe die Modalverbform und den Infinitiv am Ende.", "Check the modal form and the infinitive at the end."),
    "case_ending": ("Сначала определи артикль и падеж, затем окончание.", "Bestimme zuerst Artikel und Kasus, dann die Endung.", "Identify the article and case before choosing the ending."),
    "fixed_connection": ("Учи существительное и глагол как одно устойчивое выражение.", "Lerne Nomen und Verb als eine feste Verbindung.", "Learn the noun and verb as one fixed expression."),
    "register": ("Используй вежливую полную формулировку, подходящую ситуации.", "Nutze eine vollständige höfliche Formulierung für die Situation.", "Use a complete polite expression that fits the situation."),
    "cohesion": ("Свяжи позицию, причину и пример явными маркерами.", "Verbinde Position, Grund und Beispiel mit klaren Markern.", "Connect your position, reason, and example with clear markers."),
    "missing_words": ("Сравни ответ с образцом: проверь, не пропущены ли слова.", "Vergleiche mit dem Mustersatz: Fehlen Wörter?", "Compare with the model sentence: are any words missing?"),
    "answer_mismatch": ("Сравни свой ответ с образцом по одному слову.", "Vergleiche deine Antwort Wort für Wort mit dem Muster.", "Compare your answer with the model one word at a time."),
    "word_order": ("Проверь позицию глагола и порядок частей предложения.", "Prüfe die Verbposition und die Reihenfolge der Satzteile.", "Check the verb position and the order of sentence parts."),
    "conjugation": ("Проверь форму глагола для подлежащего.", "Prüfe die Verbform passend zum Subjekt.", "Check the verb ending for the subject."),
    "auxiliary": ("Проверь выбор вспомогательного глагола haben или sein.", "Prüfe, ob das Hilfsverb haben oder sein passt.", "Check whether the auxiliary should be haben or sein."),
    "case": ("Определи роль слова в предложении и нужный падеж.", "Bestimme die Satzfunktion und den passenden Kasus.", "Identify the word's role and the required case."),
    "article": ("Проверь род, число и падеж существительного.", "Prüfe Genus, Numerus und Kasus des Nomens.", "Check the noun's gender, number and case."),
    "adjective": ("Проверь артикль, падеж и окончание прилагательного.", "Prüfe Artikel, Kasus und Adjektivendung.", "Check the article, case and adjective ending."),
    "preposition": ("Проверь предлог и падеж после него.", "Prüfe die Präposition und den Kasus danach.", "Check the preposition and the case it requires."),
    "negation": ("Проверь, что именно отрицают nicht или kein.", "Prüfe, was nicht oder kein verneint.", "Check what nicht or kein negates."),
    "infinitive": ("Проверь, требуется ли zu перед инфинитивом.", "Prüfe, ob vor dem Infinitiv zu nötig ist.", "Check whether the infinitive needs zu."),
    "missing_target_structure": ("Используй целевую структуру урока в полном предложении.", "Nutze die Zielstruktur der Lektion in einem vollständigen Satz.", "Use the lesson’s target structure in a complete sentence."),
}


def misconception_feedback(tag: str | None, language: str) -> str:
    ru, de, en = FEEDBACK.get(tag or "", FEEDBACK["missing_target_structure"])
    return {"ru": ru, "de": de, "en": en}.get(language, en)
