"""A practical multilingual B2 route built around argumentation and register."""

B2_CURRICULUM = [
    (55, 1, "advanced_connectors", "grammar", "Причина и следствие", "Ursache und Folge", "Cause and effect", "da / sodass", "Da die Nachfrage gestiegen ist, wurden zusätzliche Kurse angeboten."),
    (56, 1, "concessive_connectors", "grammar", "Уступительные связи", "Konzessive Verknüpfungen", "Concessive links", "obwohl / dennoch", "Obwohl die Lösung teuer ist, lohnt sie sich langfristig."),
    (57, 1, "paired_connectors_b2", "grammar", "Двойные коннекторы", "Zweiteilige Konnektoren", "Paired connectors", "je … desto", "Je genauer wir planen, desto weniger Fehler entstehen."),
    (58, 1, "participle_clauses", "grammar", "Причастные конструкции", "Partizipialkonstruktionen", "Participle clauses", "Partizip I/II als Attribut", "Die gestern veröffentlichte Studie löste eine Debatte aus."),
    (59, 2, "nominal_style", "writing", "Номинальный стиль", "Nominalstil", "Nominal style", "Verb → Nomen", "Die Einführung flexibler Arbeitszeiten führte zu höherer Zufriedenheit."),
    (60, 2, "passive_alternatives", "grammar", "Альтернативы пассиву", "Passiversatzformen", "Passive alternatives", "sich lassen / sein + zu", "Das Problem lässt sich ohne zusätzliche Kosten lösen."),
    (61, 2, "reported_speech", "grammar", "Косвенная речь", "Indirekte Rede", "Reported speech", "Konjunktiv I", "Die Ministerin erklärte, die Maßnahmen seien notwendig."),
    (62, 2, "subjective_modals_b2", "grammar", "Субъективная модальность", "Subjektive Modalität", "Subjective modality", "dürfte / muss / soll", "Die Änderung dürfte vor allem kleine Betriebe betreffen."),
    (63, 3, "formal_register", "writing", "Формальный регистр", "Formelles Register", "Formal register", "präzise und höflich", "Ich möchte Sie daher um eine schriftliche Bestätigung bitten."),
    (64, 3, "argument_structure", "writing", "Структура аргумента", "Argumentationsstruktur", "Argument structure", "These – Grund – Beleg", "Für den Ausbau spricht, dass geschützte Radwege nachweislich die Verkehrssicherheit erhöhen."),
    (65, 3, "counterargument", "writing", "Контраргумент", "Gegenargument entkräften", "Addressing a counterargument", "zwar … jedoch", "Zwar entstehen zunächst Kosten, langfristig überwiegen jedoch die Vorteile."),
    (66, 3, "data_description", "writing", "Описание данных", "Daten beschreiben", "Describing data", "Anstieg / Rückgang / Anteil", "Der Anteil stieg innerhalb von fünf Jahren von 36 auf 48 Prozent, also um zwölf Prozentpunkte."),
    (67, 4, "discussion_language", "speaking", "Дискуссия", "Diskutieren und reagieren", "Discussion skills", "zustimmen / widersprechen", "Ich verstehe deinen Einwand, halte diese Schlussfolgerung aber für zu pauschal."),
    (68, 4, "presentation_structure", "speaking", "Презентация", "Präsentation strukturieren", "Structuring a presentation", "einleiten / überleiten / schließen", "Zunächst erläutere ich die Ausgangslage; anschließend gehe ich auf mögliche Lösungen ein."),
    (69, 4, "text_cohesion", "writing", "Связность текста", "Textkohärenz", "Text cohesion", "Verweise und Übergänge", "Dieser Ansatz ist überzeugend. Darüber hinaus lässt er sich schnell umsetzen."),
    (70, 4, "b2_final", "mixed", "Итоговая задача B2", "B2-Abschlussaufgabe", "B2 final task", "abwägen und begründen", "Einerseits erleichtern digitale Behördendienste den Zugang und sparen Zeit, andererseits können sie Menschen ohne digitale Kenntnisse ausschließen. Insgesamt überwiegen für mich die Vorteile, sofern Datenschutz und analoge Alternativen gewährleistet sind."),
]

B2_TRANSFER = {
    "advanced_connectors": ("Для отчёта объясни рост спроса и его последствие.", "Erkläre in einem Bericht den Nachfrageanstieg und seine Folge.", "Explain the rise in demand and its consequence in a report.", ["Da mehrere Firmen teilnahmen, musste der Kurs erweitert werden.", "Die Nachfrage wuchs, sodass ein zweiter Termin angeboten wurde."], ["da", "sodass"]),
    "concessive_connectors": ("Оцени дорогую, но перспективную меру на совещании.", "Bewerte in einer Sitzung eine teure, aber zukunftsfähige Maßnahme.", "Assess an expensive but promising measure in a meeting.", ["Obwohl der Umbau aufwendig ist, verbessert er die Abläufe.", "Die Umsetzung ist komplex; dennoch sollten wir sie prüfen."], ["obwohl", "dennoch"]),
    "paired_connectors_b2": ("Объясни команде связь между планированием и ошибками.", "Erkläre dem Team den Zusammenhang zwischen Planung und Fehlern.", "Explain the link between planning and errors to the team.", ["Je früher wir beginnen, desto flexibler können wir reagieren.", "Je klarer die Zuständigkeiten sind, desto schneller fällt die Entscheidung."], ["je", "desto"]),
    "participle_clauses": ("Кратко представь недавно опубликованное исследование.", "Stelle eine kürzlich veröffentlichte Studie knapp vor.", "Briefly introduce a recently published study.", ["Die von der Universität erhobenen Daten sind öffentlich zugänglich.", "Der im Bericht beschriebene Trend betrifft vor allem Städte."], ["partizip", "attribut"]),
    "nominal_style": ("Переформулируй вывод для официального отчёта.", "Formuliere ein Ergebnis für einen offiziellen Bericht um.", "Rephrase a finding for an official report.", ["Die Senkung der Kosten ermöglichte weitere Investitionen.", "Nach der Einführung des Modells stieg die Beteiligung."], ["nominalisierung", "genitiv"]),
    "passive_alternatives": ("В служебной записке покажи, что проблема решаема.", "Zeige in einer Notiz, dass das Problem lösbar ist.", "Show in a memo that the problem can be solved.", ["Die Frist lässt sich unter diesen Bedingungen einhalten.", "Die Ergebnisse sind leicht überprüfbar."], ["lässt sich", "überprüfbar"]),
    "reported_speech": ("Нейтрально передай заявление министра в новостной заметке.", "Gib die Aussage der Ministerin in einer Meldung neutral wieder.", "Report the minister's statement neutrally in a news brief.", ["Der Sprecher betonte, die Finanzierung sei gesichert.", "Die Behörde teilte mit, es gebe keine neuen Risiken."], ["sei", "gebe"]),
    "subjective_modals_b2": ("Осторожно оцени вероятные последствия изменения.", "Schätze die wahrscheinlichen Folgen einer Änderung vorsichtig ein.", "Carefully assess the likely effects of a change.", ["Der Engpass dürfte sich im Herbst verschärfen.", "Die Entscheidung muss intern bereits gefallen sein."], ["dürfte", "muss"]),
    "formal_register": ("Попроси организатора письменно подтвердить участие.", "Bitte den Veranstalter schriftlich um eine Teilnahmebestätigung.", "Ask the organiser to confirm participation in writing.", ["Für eine kurze Rückmeldung wäre ich Ihnen sehr dankbar.", "Bitte teilen Sie mir mit, ob meine Anmeldung eingegangen ist."], ["ich möchte sie", "bitten"]),
    "argument_structure": ("Обоснуй на форуме, почему город должен расширить велодорожки.", "Begründe in einem Forum, warum die Stadt Radwege ausbauen sollte.", "Argue in a forum why the city should expand cycle lanes.", ["Ein Ausbau ist sinnvoll, weil dadurch nachweislich Unfälle vermieden werden.", "Dafür spricht, dass sichere Wege mehr Menschen zum Umsteigen bewegen."], ["ausbau", "weil", "sicherheit"]),
    "counterargument": ("Ответь на возражение о высокой стоимости проекта.", "Entkräfte den Einwand, das Projekt sei zu teuer.", "Address the objection that the project is too expensive.", ["Zwar ist die Investition hoch, jedoch sinken dadurch die laufenden Kosten.", "Der Einwand ist nachvollziehbar; langfristig rechnet sich die Maßnahme dennoch."], ["zwar", "jedoch"]),
    "data_description": ("Опиши для презентации изменение доли пользователей за пять лет.", "Beschreibe für eine Präsentation die Nutzerentwicklung über fünf Jahre.", "Describe the change in user share over five years for a presentation.", ["Zwischen 2020 und 2025 nahm der Anteil kontinuierlich zu.", "Nach einem leichten Rückgang stieg der Wert auf 48 Prozent."], ["anteil", "2020", "2025"]),
    "discussion_language": ("В дискуссии вежливо не согласись с обобщением коллеги.", "Widersprich in einer Diskussion höflich einer pauschalen Aussage.", "Politely challenge a colleague's generalisation in a discussion.", ["Dem ersten Punkt stimme ich zu, beim zweiten sehe ich es anders.", "Dein Argument ist nachvollziehbar, berücksichtigt aber nicht alle Gruppen."], ["einwand", "aber"]),
    "presentation_structure": ("Открой короткую презентацию и обозначь её структуру.", "Eröffne eine Kurzpräsentation und kündige ihre Struktur an.", "Open a short presentation and signpost its structure.", ["Zuerst stelle ich die Daten vor; danach bewerte ich zwei Lösungswege.", "Abschließend fasse ich die wichtigsten Ergebnisse zusammen."], ["zunächst", "anschließend", "abschließend"]),
    "text_cohesion": ("Свяжи два абзаца отчёта логическим переходом.", "Verbinde zwei Absätze eines Berichts mit einem logischen Übergang.", "Connect two report paragraphs with a logical transition.", ["Diese Entwicklung senkt die Kosten. Zugleich entstehen neue Anforderungen.", "Das Modell ist wirksam; darüber hinaus ist es leicht übertragbar."], ["darüber hinaus", "dieser"]),
    "b2_final": ("На экзамене взвесь плюсы и минусы цифровых госуслуг и сделай вывод.", "Wäge in einer Prüfung Vor- und Nachteile digitaler Behördendienste ab.", "In an exam, weigh the pros and cons of digital public services.", ["Einerseits erleichtern digitale Dienste den Zugang, andererseits dürfen sie niemanden ausschließen.", "Unter klaren Datenschutzregeln halte ich die Digitalisierung insgesamt für sinnvoll."], ["einerseits", "andererseits", "insgesamt"]),
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
    function_labels = {
        "advanced_connectors": ("Причина и следствие", "Ursache und Folge", "Cause and effect"),
        "concessive_connectors": ("Уступка", "Einräumung", "Concession"),
        "paired_connectors_b2": ("Зависимость двух изменений", "Abhängigkeit zweier Entwicklungen", "Relationship between two changes"),
        "participle_clauses": ("Краткое определение существительного", "Kompaktes Attribut", "Compact noun modification"),
        "nominal_style": ("Формальная номинализация", "Formelle Nominalisierung", "Formal nominalisation"),
        "passive_alternatives": ("Возможность без обычного пассива", "Möglichkeit ohne gewöhnliches Passiv", "Possibility without the standard passive"),
        "reported_speech": ("Нейтральная передача чужой речи", "Neutrale Wiedergabe fremder Aussage", "Neutral reported speech"),
        "subjective_modals_b2": ("Оценка вероятности", "Wahrscheinlichkeitseinschätzung", "Assessment of probability"),
        "formal_register": ("Вежливая формальная просьба", "Höfliche formelle Bitte", "Polite formal request"),
        "argument_structure": ("Аргумент с обоснованием", "Begründetes Argument", "Supported argument"),
        "counterargument": ("Уступка и контраргумент", "Einräumung und Gegenargument", "Concession and counterargument"),
        "data_description": ("Описание изменения данных", "Beschreibung einer Datenentwicklung", "Description of a data trend"),
        "discussion_language": ("Вежливое несогласие", "Höflicher Widerspruch", "Polite disagreement"),
        "presentation_structure": ("Структурирование презентации", "Gliederung einer Präsentation", "Presentation signposting"),
        "text_cohesion": ("Логический переход", "Logischer Übergang", "Logical transition"),
        "b2_final": ("Взвешенный вывод", "Abgewogenes Fazit", "Balanced conclusion"),
    }
    listening_function_ru, listening_function_de, listening_function_en = function_labels[topic]
    wrong_examples = {
        "advanced_connectors": "Da die Nachfrage gestiegen ist wurden zusätzliche Kurse angeboten.",
        "concessive_connectors": "Obwohl die Lösung teuer ist, aber lohnt sie sich langfristig.",
        "paired_connectors_b2": "Je genauer wir planen, desto entstehen weniger Fehler.",
        "participle_clauses": "Die gestern veröffentlichen Studie löste eine Debatte aus.",
        "nominal_style": "Die Einführung von flexible Arbeitszeiten führte zu höherer Zufriedenheit.",
        "passive_alternatives": "Das Problem lässt ohne zusätzliche Kosten lösen.",
        "reported_speech": "Die Ministerin erklärte, die Maßnahmen sind notwendig.",
        "subjective_modals_b2": "Die Änderung dürfte betrifft vor allem kleine Betriebe.",
        "formal_register": "Bestätigen Sie mir das schriftlich.",
        "argument_structure": "Dafür spricht vor allem, dadurch nachweislich Ressourcen gespart werden.",
        "counterargument": "Zwar entstehen zunächst Kosten, aber jedoch überwiegen langfristig die Vorteile.",
        "data_description": "Der Anteil stieg innerhalb von fünf Jahren auf zwölf Prozentpunkte.",
        "discussion_language": "Ich verstehe deinen Einwand, aber deine Schlussfolgerung ist einfach falsch.",
        "presentation_structure": "Zunächst erläutere ich die Ausgangslage, anschließend ich gehe auf mögliche Lösungen ein.",
        "text_cohesion": "Dieser Ansatz ist überzeugend. Aber außerdem lässt er sich schnell umsetzen.",
        "b2_final": "Insgesamt überwiegen die Vorteile, weil Datenschutz und Zugänglichkeit gewährleistet sind.",
    }
    wrong = wrong_examples[topic]
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
            {"id": f"{topic}-guided", "type": guided_type, "stage": "guided", "question": guided_questions["ru"], "answer": model, "accepted_answers": [model, model.rstrip(".")], "hint": rule["ru"], "explanation": rule["ru"], "misconception": "b2_structure", "accessibility_label": guided_questions["ru"]},
            {"question": guided_questions["ru"], "hint": rule["ru"], "explanation": rule["ru"]},
            {"question": guided_questions["de"], "hint": rule["de"], "explanation": rule["de"]},
            {"question": guided_questions["en"], "hint": rule["en"], "explanation": rule["en"]},
        ),
        _localized(
            {"id": f"{topic}-choice", "type": "context_choice", "stage": "independent", "question": scenario_ru, "answer": model, "accepted_answers": [model], "options": [model, wrong, "Das ist halt so und irgendwie auch gut."], "explanation": rule["ru"], "misconception": "register", "accessibility_label": scenario_ru},
            {"question": scenario_ru, "explanation": rule["ru"]},
            {"question": scenario_de, "explanation": rule["de"]},
            {"question": scenario_en, "explanation": rule["en"]},
        ),
        _localized(
            {"id": f"{topic}-listen", "type": "listening_choice", "stage": "independent", "question": "Какую функцию выполняет фраза?", "audio_text": alternatives[0], "answer": listening_function_ru, "accepted_answers": [listening_function_ru], "options": [listening_function_ru, "Пример", "Приветствие"], "explanation": alternatives[0], "misconception": "discourse_function", "accessibility_label": "Прослушать фразу уровня B2 и определить её функцию."},
            {"question": "Какую функцию выполняет фраза?", "answer": listening_function_ru, "accepted_answers": [listening_function_ru], "options": [listening_function_ru, "Пример", "Приветствие"], "explanation": alternatives[0]},
            {"question": "Welche Funktion erfüllt der Satz?", "answer": listening_function_de, "accepted_answers": [listening_function_de], "options": [listening_function_de, "Beispiel", "Begrüßung"], "explanation": alternatives[0]},
            {"question": "What function does the sentence serve?", "answer": listening_function_en, "accepted_answers": [listening_function_en], "options": [listening_function_en, "Example", "Greeting"], "explanation": alternatives[0]},
        ),
        _localized(
            {"id": f"{topic}-dialogue", "type": "dialogue", "stage": "transfer", "mission_role": "final", "question": f"Сформулируй собственный ответ: {scenario_ru}", "answer": model, "model_answer": model, "accepted_answers": [model, model.rstrip(".")], "target_patterns": patterns, "hint": rule["ru"], "explanation": "Ответ может отличаться от модели: оцени выполнение задачи, связность и регистр.", "misconception": "transfer", "accessibility_label": scenario_ru},
            {"question": f"Сформулируй собственный ответ: {scenario_ru}", "hint": rule["ru"], "explanation": "Ответ может отличаться от модели: оцени выполнение задачи, связность и регистр."},
            {"question": f"Formuliere eine eigene Antwort: {scenario_de}", "hint": rule["de"], "explanation": "Die Antwort darf abweichen: Prüfe Aufgabenerfüllung, Kohärenz und Register."},
            {"question": f"Give your own response: {scenario_en}", "hint": rule["en"], "explanation": "The response may differ: check task completion, coherence, and register."},
        ),
        _localized(
            {"id": f"{topic}-repeat", "type": "repeat", "stage": "transfer", "question": "Произнеси новую модель вслух.", "audio_text": alternatives[1], "answer": alternatives[1], "accepted_answers": [alternatives[1], alternatives[1].rstrip(".")], "explanation": "Сохраняй логическое ударение и темп.", "misconception": "fluency", "accessibility_label": "Произнести аргумент уровня B2."},
            {"question": "Произнеси модель вслух.", "explanation": "Сохраняй логическое ударение и темп."},
            {"question": "Sprich das Modell laut nach.", "explanation": "Achte auf Satzakzent und Tempo."},
            {"question": "Say the model aloud.", "explanation": "Keep the sentence stress and pace natural."},
        ),
    ]
    module_titles = {
        1: ("Строй сложные связи", "Komplexe Zusammenhänge", "Build complex connections"),
        2: ("Пиши точно и объективно", "Präzise und objektiv schreiben", "Write precisely and objectively"),
        3: ("Доказывай свою позицию", "Eine Position belegen", "Support a position"),
        4: ("Убеждай в речи и тексте", "Mündlich und schriftlich überzeugen", "Persuade in speech and writing"),
    }
    module_title_ru, module_title_de, module_title_en = module_titles[module]
    module_step = ((day - 55) % 4) + 1
    checkpoint = module_step == 4
    previous_topic = B2_CURRICULUM[day - 56][2] if day > 55 else None
    dialogue = next(item for item in exercises if item["type"] == "dialogue")
    partners = [
        "Wie beurteilen Sie die Ausgangslage?",
        "Welcher Beleg stützt Ihre Position?",
        "Was entgegnen Sie dem wichtigsten Gegenargument?",
    ]
    turn_models = [model, alternatives[0], alternatives[1]]
    turn_goals = {
        "ru": ["Чётко сформулируй позицию.", "Добавь конкретное обоснование.", "Учти возражение и сделай вывод."],
        "de": ["Formuliere eine klare Position.", "Füge eine konkrete Begründung hinzu.", "Berücksichtige einen Einwand und ziehe ein Fazit."],
        "en": ["State a clear position.", "Add specific support.", "Address an objection and conclude."],
    }

    def conversation_turns(language: str) -> list[dict]:
        return [
            {"partner": partner, "goal": turn_goals[language][index], "placeholder": "Antworten Sie in einem vollständigen Satz …", "model": turn_models[index]}
            for index, partner in enumerate(partners)
        ]

    dialogue["conversation_turns"] = conversation_turns("ru")
    for language in ("ru", "de", "en"):
        dialogue["i18n"][language]["conversation_turns"] = conversation_turns(language)
    listening = next(item for item in exercises if item["type"] == "listening_choice")
    repeat = next(item for item in exercises if item["type"] == "repeat")

    practice = [item for item in exercises if item is not dialogue and item is not repeat]
    permutations = ((0, 1, 2), (2, 0, 1), (1, 2, 0), (0, 2, 1))
    exercises = [*(practice[index] for index in permutations[module_step - 1]), dialogue, repeat]
    success = {
        "ru": "Ты формулируешь ясную позицию, развиваешь её доказательством и отвечаешь на возражение в подходящем регистре.",
        "de": "Du formulierst eine klare Position, belegst sie und reagierst im passenden Register auf einen Einwand.",
        "en": "You state a clear position, support it, and address an objection in an appropriate register.",
    }
    delayed_review = {
        "method": "changed_context_retrieval", "after_days": [1, 3, 7, 14, 30],
        "prompt": f"Новый контекст: {scenario_ru} Ответь без модели, добавив доказательство и оговорку.",
        "reason": "Перенос в новый контекст проверяет самостоятельную аргументацию, а не запоминание модели.",
        "i18n": {
            "ru": {"prompt": f"Новый контекст: {scenario_ru} Ответь без модели, добавив доказательство и оговорку.", "reason": "Перенос в новый контекст проверяет самостоятельную аргументацию, а не запоминание модели."},
            "de": {"prompt": f"Neuer Kontext: {scenario_de} Antworte ohne Modell mit einem Beleg und einer Einschränkung.", "reason": "Der Transfer prüft selbstständiges Argumentieren statt das Auswendiglernen eines Modells."},
            "en": {"prompt": f"New context: {scenario_en} Respond without the model, adding evidence and a qualification.", "reason": "Transfer checks independent argumentation rather than memorisation."},
        },
    }
    localized = {
        "ru": {"title": title_ru, "rule": rule["ru"], "objective": objective["ru"], "scenario": scenario_ru, "assessment_rubric": rubric["ru"], "module_title": module_title_ru, "can_do": objective["ru"], "mission": scenario_ru, "success_evidence": success["ru"]},
        "de": {"title": title_de, "rule": rule["de"], "objective": objective["de"], "scenario": scenario_de, "assessment_rubric": rubric["de"], "module_title": module_title_de, "can_do": objective["de"], "mission": scenario_de, "success_evidence": success["de"]},
        "en": {"title": title_en, "rule": rule["en"], "objective": objective["en"], "scenario": scenario_en, "assessment_rubric": rubric["en"], "module_title": module_title_en, "can_do": objective["en"], "mission": scenario_en, "success_evidence": success["en"]},
    }
    # Reuse authored transfer examples for guided recovery only when they
    # are not already answer keys in this lesson.
    used_answers = {
        " ".join(str(value).split()).rstrip(".?!").casefold()
        for item in exercises
        for value in (item.get("accepted_answers") or [item.get("answer", "")])
    }
    retry_examples = [
        {"skill_id": topic, "sentence": sentence}
        for sentence in alternatives
        if isinstance(sentence, str) and sentence.strip()
        and " ".join(sentence.split()).rstrip(".?!").casefold() not in used_answers
    ]
    # Every authored exercise inherits its lesson's stable curriculum skill.
    # Distinct skill-matched retry examples can be added after editorial review.
    for exercise in exercises:
        exercise.setdefault("skill_id", topic)
    return {
        "day": day, "week": module, "track": "B2", "module": module,
        "module_step": module_step, "module_size": 4, "module_title": module_title_ru, "checkpoint": checkpoint,
        "quality_version": 15, "learning_method": "mission_loop_v1",
        "title": title_ru, "objective": objective["ru"], "communication_goal": objective["ru"],
        "can_do": objective["ru"], "mission": scenario_ru, "success_evidence": success["ru"],
        "rule": rule["ru"], "scenario": scenario_ru, "assessment_rubric": rubric["ru"], "examples": [model, *alternatives],
        "audio_text": model, "cefr": "B2", "prerequisites": [previous_topic] if previous_topic else [],
        "common_mistakes": [f"❌ {wrong}", f"✅ {model}"],
        "recall_prompt": "Закрой пример, назови функцию структуры и создай собственный аргумент.",
        "repair_flow": {"mode": "targeted_retry", "contrast_before_retry": True, "misconception": "b2_structure"},
        "delayed_review": delayed_review,
        "content_review": {"status": "approved", "version": "b2-production-path-v15", "languages": {"ru": "reviewed", "de": "reviewed", "en": "reviewed"}},
        "i18n": localized,
        "retry_examples": retry_examples, "exercises": exercises,
    }
