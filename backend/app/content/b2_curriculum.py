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

B2_TRANSFER = {
    "advanced_connectors": ("Для отчёта объясни рост спроса и его последствие.", "Erkläre in einem Bericht den Nachfrageanstieg und seine Folge.", "Explain the rise in demand and its consequence in a report.", ["Da mehrere Firmen teilnahmen, musste der Kurs erweitert werden.", "Die Nachfrage wuchs, sodass ein zweiter Termin angeboten wurde."], ["da", "sodass"]),
    "concessive_connectors": ("Оцени дорогую, но перспективную меру на совещании.", "Bewerte in einer Sitzung eine teure, aber zukunftsfähige Maßnahme.", "Assess an expensive but promising measure in a meeting.", ["Obwohl der Umbau aufwendig ist, verbessert er die Abläufe.", "Die Umsetzung ist komplex; dennoch sollten wir sie prüfen."], ["obwohl", "dennoch"]),
    "paired_connectors_b2": ("Объясни команде связь между планированием и ошибками.", "Erkläre dem Team den Zusammenhang zwischen Planung und Fehlern.", "Explain the link between planning and errors to the team.", ["Je früher wir beginnen, desto flexibler können wir reagieren.", "Je klarer die Zuständigkeiten sind, desto schneller fällt die Entscheidung."], ["je", "desto"]),
    "participle_clauses": ("Кратко представь недавно опубликованное исследование.", "Stelle eine kürzlich veröffentlichte Studie knapp vor.", "Briefly introduce a recently published study.", ["Die von der Universität erhobenen Daten sind öffentlich zugänglich.", "Der im Bericht beschriebene Trend betrifft vor allem Städte."], ["partizip", "attribut"]),
    "nominal_style": ("Переформулируй вывод для официального отчёта.", "Formuliere ein Ergebnis für einen offiziellen Bericht um.", "Rephrase a finding for an official report.", ["Die Senkung der Kosten ermöglichte weitere Investitionen.", "Nach der Einführung des Modells stieg die Beteiligung."], ["nominalisierung", "genitiv"]),
    "passive_alternatives": ("В служебной записке покажи, что проблема решаема.", "Zeige in einer Notiz, dass das Problem lösbar ist.", "Show in a memo that the problem can be solved.", ["Die Frist lässt sich unter diesen Bedingungen einhalten.", "Die Ergebnisse sind leicht zu überprüfen."], ["lässt sich", "zu"]),
    "reported_speech": ("Нейтрально передай заявление министра в новостной заметке.", "Gib die Aussage der Ministerin in einer Meldung neutral wieder.", "Report the minister's statement neutrally in a news brief.", ["Der Sprecher betonte, die Finanzierung sei gesichert.", "Die Behörde teilte mit, es gebe keine neuen Risiken."], ["sei", "gebe"]),
    "subjective_modals_b2": ("Осторожно оцени вероятные последствия изменения.", "Schätze die wahrscheinlichen Folgen einer Änderung vorsichtig ein.", "Carefully assess the likely effects of a change.", ["Der Engpass dürfte sich im Herbst verschärfen.", "Die Entscheidung muss intern bereits gefallen sein."], ["dürfte", "muss"]),
    "formal_register": ("Попроси организатора письменно подтвердить участие.", "Bitte den Veranstalter schriftlich um eine Teilnahmebestätigung.", "Ask the organiser to confirm participation in writing.", ["Für eine kurze Rückmeldung wäre ich Ihnen sehr dankbar.", "Bitte teilen Sie mir mit, ob meine Anmeldung eingegangen ist."], ["ich möchte sie", "bitten"]),
    "argument_structure": ("Обоснуй на форуме, почему город должен расширить велодорожки.", "Begründe in einem Forum, warum die Stadt Radwege ausbauen sollte.", "Argue in a forum why the city should expand cycle lanes.", ["Ein Ausbau ist sinnvoll, weil dadurch nachweislich Unfälle vermieden werden.", "Dafür spricht, dass sichere Wege mehr Menschen zum Umsteigen bewegen."], ["these", "grund", "beleg"]),
    "counterargument": ("Ответь на возражение о высокой стоимости проекта.", "Entkräfte den Einwand, das Projekt sei zu teuer.", "Address the objection that the project is too expensive.", ["Zwar ist die Investition hoch, jedoch sinken dadurch die laufenden Kosten.", "Der Einwand ist nachvollziehbar; langfristig rechnet sich die Maßnahme dennoch."], ["zwar", "jedoch"]),
    "data_description": ("Опиши для презентации изменение доли пользователей за пять лет.", "Beschreibe für eine Präsentation die Nutzerentwicklung über fünf Jahre.", "Describe the change in user share over five years for a presentation.", ["Zwischen 2020 und 2025 nahm der Anteil kontinuierlich zu.", "Nach einem leichten Rückgang stieg der Wert auf 48 Prozent."], ["anstieg", "zeitraum"]),
    "discussion_language": ("В дискуссии вежливо не согласись с обобщением коллеги.", "Widersprich in einer Diskussion höflich einer pauschalen Aussage.", "Politely challenge a colleague's generalisation in a discussion.", ["Dem ersten Punkt stimme ich zu, beim zweiten sehe ich es anders.", "Dein Argument ist nachvollziehbar, berücksichtigt aber nicht alle Gruppen."], ["einwand", "aber"]),
    "presentation_structure": ("Открой короткую презентацию и обозначь её структуру.", "Eröffne eine Kurzpräsentation und kündige ihre Struktur an.", "Open a short presentation and signpost its structure.", ["Zuerst stelle ich die Daten vor; danach bewerte ich zwei Lösungswege.", "Abschließend fasse ich die wichtigsten Ergebnisse zusammen."], ["zunächst", "anschließend", "abschließend"]),
    "text_cohesion": ("Свяжи два абзаца отчёта логическим переходом.", "Verbinde zwei Absätze eines Berichts mit einem logischen Übergang.", "Connect two report paragraphs with a logical transition.", ["Diese Entwicklung senkt die Kosten. Zugleich entstehen neue Anforderungen.", "Das Modell ist wirksam; darüber hinaus ist es leicht übertragbar."], ["darüber hinaus", "dieser"]),
    "b2_final": ("На экзамене взвесь плюсы и минусы цифровых госуслуг и сделай вывод.", "Wäge in einer Prüfung Vor- und Nachteile digitaler Behördendienste ab.", "In an exam, weigh the pros and cons of digital public services.", ["Einerseits erleichtern digitale Dienste den Zugang, andererseits dürfen sie niemanden ausschließen.", "Unter klaren Datenschutzregeln halte ich die Digitalisierung insgesamt für sinnvoll."], ["abwägung", "begründung", "schluss"]),
}


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
    scenario_ru, scenario_de, scenario_en, alternatives, patterns = B2_TRANSFER[topic]
    wrong = model.replace(",", "", 1) if "," in model else model[:1].lower() + model[1:]
    rubric = {
        "ru": ["Задача полностью выполнена и позиция ясна.", "Аргументы логично связаны и развиты.", "Регистр и грамматика соответствуют уровню B2."],
        "de": ["Die Aufgabe ist vollständig erfüllt und die Position klar.", "Die Argumente sind logisch verknüpft und entwickelt.", "Register und Grammatik entsprechen dem B2-Niveau."],
        "en": ["The task is fully addressed and the position is clear.", "Arguments are logically connected and developed.", "Register and grammar are appropriate for B2."],
    }
    guided_type = "error_repair" if day % 2 else "transform"
    guided_questions = {
        "ru": f"Исправь: {wrong}" if guided_type == "error_repair" else f"Переформулируй для официального контекста: {wrong}",
        "de": f"Korrigiere: {wrong}" if guided_type == "error_repair" else f"Formuliere für einen formellen Kontext um: {wrong}",
        "en": f"Correct: {wrong}" if guided_type == "error_repair" else f"Rephrase for a formal context: {wrong}",
    }
    exercises = [
        _localized(
            {"type": guided_type, "stage": "guided", "question": guided_questions["ru"], "answer": model, "accepted_answers": [model, model.rstrip(".")], "hint": rule["ru"], "explanation": rule["ru"], "misconception": "b2_structure"},
            {"question": guided_questions["ru"], "hint": rule["ru"], "explanation": rule["ru"]},
            {"question": guided_questions["de"], "hint": rule["de"], "explanation": rule["de"]},
            {"question": guided_questions["en"], "hint": rule["en"], "explanation": rule["en"]},
        ),
        _localized(
            {"type": "context_choice", "stage": "independent", "question": scenario_ru, "answer": model, "accepted_answers": [model], "options": [model, wrong, "Das ist halt so und irgendwie auch gut."], "explanation": rule["ru"], "misconception": "register"},
            {"question": scenario_ru, "explanation": rule["ru"]},
            {"question": scenario_de, "explanation": rule["de"]},
            {"question": scenario_en, "explanation": rule["en"]},
        ),
        _localized(
            {"type": "listening_choice", "stage": "independent", "question": "Какую функцию выполняет фраза?", "answer": focus, "accepted_answers": [focus], "options": [focus, "Beispiel", "Begrüßung"], "explanation": model, "misconception": "discourse_function"},
            {"question": "Какую функцию выполняет фраза?", "explanation": model},
            {"question": "Welche Funktion erfüllt der Satz?", "explanation": model},
            {"question": "What function does the sentence serve?", "explanation": model},
        ),
        _localized(
            {"type": "dialogue", "stage": "transfer", "question": f"Сформулируй собственный ответ: {scenario_ru}", "answer": model, "model_answer": model, "accepted_answers": [model, model.rstrip(".")], "target_patterns": patterns, "hint": rule["ru"], "explanation": "Ответ может отличаться от модели: оцени выполнение задачи, связность и регистр.", "misconception": "transfer"},
            {"question": f"Сформулируй собственный ответ: {scenario_ru}", "hint": rule["ru"], "explanation": "Ответ может отличаться от модели: оцени выполнение задачи, связность и регистр."},
            {"question": f"Formuliere eine eigene Antwort: {scenario_de}", "hint": rule["de"], "explanation": "Die Antwort darf abweichen: Prüfe Aufgabenerfüllung, Kohärenz und Register."},
            {"question": f"Give your own response: {scenario_en}", "hint": rule["en"], "explanation": "The response may differ: check task completion, coherence, and register."},
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
        "quality_version": 5, "learning_method": "notice_build_use_reflect",
        "title": title_ru, "objective": objective["ru"], "communication_goal": objective["ru"],
        "rule": rule["ru"], "scenario": scenario_ru, "assessment_rubric": rubric["ru"], "examples": [model, *alternatives],
        "audio_text": model, "cefr": "B2", "prerequisites": [],
        "common_mistakes": [f"❌ {wrong}", f"✅ {model}"],
        "recall_prompt": "Закрой пример, назови функцию структуры и создай собственный аргумент.",
        "i18n": {
            "ru": {"title": title_ru, "rule": rule["ru"], "objective": objective["ru"], "scenario": scenario_ru, "assessment_rubric": rubric["ru"]},
            "de": {"title": title_de, "rule": rule["de"], "objective": objective["de"], "scenario": scenario_de, "assessment_rubric": rubric["de"]},
            "en": {"title": title_en, "rule": rule["en"], "objective": objective["en"], "scenario": scenario_en, "assessment_rubric": rubric["en"]},
        },
        "exercises": exercises,
    }
