"""A practical multilingual B2 route built around argumentation and register."""

B2_CURRICULUM = [
    (55, 1, "advanced_connectors", "grammar", "Причина и следствие", "Ursache und Folge", "Cause and effect", "da / sodass", "Da die Nachfrage gestiegen ist, wurden zusätzliche Kurse angeboten."),
    (56, 1, "concessive_connectors", "grammar", "Уступительные связи", "Konzessive Verknüpfungen", "Concessive links", "obwohl / dennoch", "Obwohl die Lösung teuer ist, lohnt sie sich langfristig."),
    (57, 1, "paired_connectors_b2", "grammar", "Двойные коннекторы", "Zweiteilige Konnektoren", "Paired connectors", "je … desto", "Je genauer wir planen, desto weniger Fehler entstehen."),
    (58, 1, "participle_clauses", "grammar", "Причастные конструкции", "Partizipialkonstruktionen", "Participle clauses", "Partizip als Attribut", "Die gestern veröffentlichte Studie löste eine Debatte aus."),
    (59, 2, "nominal_style", "writing", "Номинальный стиль", "Nominalstil", "Nominal style", "Verb → Nomen", "Die Einführung flexibler Arbeitszeiten führte zu höherer Zufriedenheit."),
    (60, 2, "passive_alternatives", "grammar", "Альтернативы пассиву", "Passiversatzformen", "Passive alternatives", "sich lassen / sein + zu", "Das Problem lässt sich ohne zusätzliche Kosten lösen."),
    (61, 2, "reported_speech", "grammar", "Косвенная речь", "Indirekte Rede", "Reported speech", "Konjunktiv I", "Die Ministerin erklärte, die Maßnahmen seien notwendig."),
    (62, 2, "subjective_modals_b2", "grammar", "Субъективная модальность", "Subjektive Modalität", "Subjective modality", "dürfte / muss / soll", "Die Änderung dürfte vor allem kleine Betriebe betreffen."),
    (63, 3, "formal_register", "writing", "Формальный регистр", "Formelles Register", "Formal register", "präzise und höflich", "Ich möchte Sie daher um eine schriftliche Bestätigung bitten."),
    (64, 3, "argument_structure", "writing", "Структура аргумента", "Argumentationsstruktur", "Argument structure", "These – Grund – Beleg", "Dafür spricht vor allem, dass dadurch nachweislich Ressourcen gespart werden."),
    (65, 3, "counterargument", "writing", "Контраргумент", "Gegenargument entkräften", "Addressing a counterargument", "zwar … jedoch", "Zwar entstehen zunächst Kosten, langfristig überwiegen jedoch die Vorteile."),
    (66, 3, "data_description", "writing", "Описание данных", "Daten beschreiben", "Describing data", "Anstieg / Rückgang / Anteil", "Der Anteil stieg innerhalb von fünf Jahren um zwölf Prozentpunkte."),
    (67, 4, "discussion_language", "speaking", "Дискуссия", "Diskutieren und reagieren", "Discussion skills", "zustimmen / widersprechen", "Ich verstehe deinen Einwand, halte diese Schlussfolgerung aber für zu pauschal."),
    (68, 4, "presentation_structure", "speaking", "Презентация", "Präsentation strukturieren", "Structuring a presentation", "einleiten / überleiten / schließen", "Zunächst erläutere ich die Ausgangslage; anschließend gehe ich auf mögliche Lösungen ein."),
    (69, 4, "text_cohesion", "writing", "Связность текста", "Textkohärenz", "Text cohesion", "Verweise und Übergänge", "Dieser Ansatz ist überzeugend. Darüber hinaus lässt er sich schnell umsetzen."),
    (70, 4, "b2_final", "mixed", "Итоговая задача B2", "B2-Abschlussaufgabe", "B2 final task", "abwägen und begründen", "Insgesamt überwiegen die Vorteile, sofern Datenschutz und Zugänglichkeit gewährleistet sind."),
]


def _localized(base: dict, ru: dict, de: dict, en: dict) -> dict:
    return {**base, "i18n": {"ru": ru, "de": de, "en": en}}


def build_b2_content(row: tuple) -> dict:
    day, module, topic, pillar, title_ru, title_de, title_en, focus, model = row
    rule = {
        "ru": f"Используй {focus}, чтобы точно связать идеи в формальном контексте.",
        "de": f"Nutze {focus}, um Gedanken in formellen Kontexten präzise zu verknüpfen.",
        "en": f"Use {focus} to connect ideas precisely in formal contexts.",
    }
    objective = {
        "ru": f"Самостоятельно применить {focus} в аргументированном ответе.",
        "de": f"{focus} selbstständig in einer begründeten Antwort anwenden.",
        "en": f"Use {focus} independently in a reasoned response.",
    }
    wrong = model.replace(",", "", 1)
    patterns = [word.casefold().strip(".,;:?!") for word in model.split() if len(word) > 4][:4]
    exercises = [
        _localized(
            {"type": "error_repair", "stage": "guided", "question": f"Исправь: {wrong}", "answer": model, "accepted_answers": [model, model.rstrip(".")], "hint": rule["ru"], "explanation": rule["ru"], "misconception": "b2_structure"},
            {"question": f"Исправь: {wrong}", "hint": rule["ru"], "explanation": rule["ru"]},
            {"question": f"Korrigiere: {wrong}", "hint": rule["de"], "explanation": rule["de"]},
            {"question": f"Correct: {wrong}", "hint": rule["en"], "explanation": rule["en"]},
        ),
        _localized(
            {"type": "context_choice", "stage": "independent", "question": "Выбери подходящую формулировку для формального текста.", "answer": model, "accepted_answers": [model], "options": [model, wrong, f"Also, {model}"], "explanation": rule["ru"], "misconception": "register"},
            {"question": "Выбери подходящую формулировку для формального текста.", "explanation": rule["ru"]},
            {"question": "Wähle die passende Formulierung für einen formellen Text.", "explanation": rule["de"]},
            {"question": "Choose the suitable wording for a formal text.", "explanation": rule["en"]},
        ),
        _localized(
            {"type": "listening_choice", "stage": "independent", "question": "Какую функцию выполняет фраза?", "answer": focus, "accepted_answers": [focus], "options": [focus, "Beispiel", "Begrüßung"], "explanation": model, "misconception": "discourse_function"},
            {"question": "Какую функцию выполняет фраза?", "explanation": model},
            {"question": "Welche Funktion erfüllt der Satz?", "explanation": model},
            {"question": "What function does the sentence serve?", "explanation": model},
        ),
        _localized(
            {"type": "dialogue", "stage": "transfer", "question": objective["ru"], "answer": model, "model_answer": model, "accepted_answers": [model, model.rstrip(".")], "target_patterns": patterns, "hint": rule["ru"], "explanation": "Сравни структуру и регистр с моделью.", "misconception": "transfer"},
            {"question": objective["ru"], "hint": rule["ru"], "explanation": "Сравни структуру и регистр с моделью."},
            {"question": objective["de"], "hint": rule["de"], "explanation": "Vergleiche Struktur und Register mit dem Modell."},
            {"question": objective["en"], "hint": rule["en"], "explanation": "Compare your structure and register with the model."},
        ),
        _localized(
            {"type": "repeat", "stage": "transfer", "question": "Произнеси модель вслух.", "answer": model, "accepted_answers": [model, model.rstrip(".")], "explanation": "Сохраняй логическое ударение и темп.", "misconception": "fluency"},
            {"question": "Произнеси модель вслух.", "explanation": "Сохраняй логическое ударение и темп."},
            {"question": "Sprich das Modell laut nach.", "explanation": "Achte auf Satzakzent und Tempo."},
            {"question": "Say the model aloud.", "explanation": "Keep the sentence stress and pace natural."},
        ),
    ]
    return {
        "day": day, "week": module, "track": "B2", "module": module,
        "quality_version": 4, "learning_method": "notice_build_use_reflect",
        "title": title_ru, "objective": objective["ru"], "communication_goal": objective["ru"],
        "rule": rule["ru"], "examples": [model, model.rstrip("."), f"B2-Muster: {model}"],
        "audio_text": model, "cefr": "B2", "prerequisites": [],
        "common_mistakes": [f"❌ {wrong}", f"✅ {model}"],
        "recall_prompt": "Закрой пример, назови функцию структуры и создай собственный аргумент.",
        "i18n": {
            "ru": {"title": title_ru, "rule": rule["ru"], "objective": objective["ru"]},
            "de": {"title": title_de, "rule": rule["de"], "objective": objective["de"]},
            "en": {"title": title_en, "rule": rule["en"], "objective": objective["en"]},
        },
        "exercises": exercises,
    }
