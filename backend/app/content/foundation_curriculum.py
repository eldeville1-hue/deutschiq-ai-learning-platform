"""Dedicated multilingual A1 and A2 routes for Adaptive Foundation v2."""

# day, module, skill id, pillar, RU/DE/EN title, target focus, model, typical error
A1_CURRICULUM = [
    (1,1,"greetings","speaking","Приветствие","Begrüßung","Greetings","Begrüßung","Guten Morgen! Ich heiße Mia.","Guten Morgen! Ich heißen Mia."),
    (2,1,"personal_details","speaking","О себе","Sich vorstellen","Introducing yourself","ich heiße / ich komme aus","Ich heiße Amir und komme aus Hamburg.","Ich heiße Amir und ich aus Hamburg."),
    (3,1,"main_clause","grammar","Простое предложение","Aussagesatz","Main clauses","Verb auf Position 2","Heute lerne ich Deutsch.","Heute ich lerne Deutsch."),
    (4,1,"yes_no_questions","grammar","Общие вопросы","Ja-/Nein-Fragen","Yes/no questions","Verb auf Position 1","Wohnst du in Berlin?","Du wohnst in Berlin?"),
    (5,1,"w_questions","grammar","Вопросы с W-словом","W-Fragen","W-questions","Wort + Verb + Subjekt","Wo arbeitest du?","Wo du arbeitest?"),
    (6,2,"present_regular","grammar","Глаголы в Präsens","Regelmäßige Verben","Regular present tense","Präsens-Endungen","Wir lernen jeden Abend Deutsch.","Wir lernt jeden Abend Deutsch."),
    (7,2,"sein_haben","grammar","sein и haben","Sein und haben","Sein and haben","bin / bist / ist; habe / hast","Ich bin müde, aber ich habe Zeit.","Ich sein müde, aber ich haben Zeit."),
    (8,2,"noun_gender","vocabulary","Артикли существительных","Nomen und Artikel","Nouns and articles","der / die / das","Das ist ein Buch und eine Lampe.","Das ist eine Buch und ein Lampe."),
    (9,2,"plural","vocabulary","Множественное число","Pluralformen","Plural forms","Plural mit die","Die Bücher liegen auf dem Tisch.","Der Bücher liegen auf dem Tisch."),
    (10,2,"negation","grammar","Отрицание","Negation","Negation","kein bei Nomen, nicht sonst","Ich habe kein Auto, aber ich fahre gern Rad.","Ich habe nicht Auto, aber ich fahre gern Rad."),
    (11,3,"accusative_a1","grammar","Akkusativ","Akkusativ","Accusative","direktes Objekt","Ich kaufe einen Kaffee und ein Brötchen.","Ich kaufe ein Kaffee und einen Brötchen."),
    (12,3,"modal_verbs_a1","grammar","Модальные глаголы","Modalverben","Modal verbs","Modalverb + Infinitiv","Ich kann heute länger arbeiten.","Ich kann arbeite heute länger."),
    (13,3,"separable_verbs_a1","grammar","Отделяемые глаголы","Trennbare Verben","Separable verbs","Vorsilbe am Ende","Der Kurs fängt um neun Uhr an.","Der Kurs anfängt um neun Uhr."),
    (14,3,"time_daily_routine","vocabulary","Распорядок дня","Tagesablauf","Daily routine","Zeit + Handlung","Um sieben Uhr stehe ich auf.","Um sieben Uhr ich aufstehe."),
    (15,3,"directions","speaking","Как пройти","Nach dem Weg fragen","Asking directions","höfliche Ortsfrage","Entschuldigung, wo ist der Bahnhof?","Entschuldigung, wo der Bahnhof ist?"),
    (16,4,"shopping","speaking","В магазине","Einkaufen","Shopping","Preis und Wunsch","Ich hätte gern ein Kilo Äpfel.","Ich hätte gern einen Kilo Äpfel."),
    (17,4,"appointments","speaking","Встречи и время","Termine und Uhrzeit","Appointments and time","am / um","Der Termin ist am Montag um zehn Uhr.","Der Termin ist um Montag am zehn Uhr."),
    (18,4,"family","vocabulary","Семья","Familie","Family","Possessivartikel","Meine Schwester wohnt mit ihrem Mann in Köln.","Mein Schwester wohnt mit sein Mann in Köln."),
    (19,4,"simple_past_experience","speaking","Вчера","Über gestern sprechen","Talking about yesterday","Perfekt-Modell","Gestern habe ich lange gearbeitet.","Gestern ich habe lange gearbeitet."),
    (20,4,"a1_final","mixed","Итоговая задача A1","A1-Abschlussaufgabe","A1 final task","Vorstellung + Alltag","Ich heiße Lina, wohne in Bremen und lerne jeden Tag Deutsch.","Ich Lina, in Bremen und jeden Tag Deutsch lernen."),
]

A2_CURRICULUM = [
    (1,1,"dative_a2","grammar","Dativ","Dativ","Dative","Empfänger im Dativ","Ich gebe meiner Freundin das Buch.","Ich gebe meine Freundin das Buch."),
    (2,1,"dative_accusative","grammar","Dativ и Akkusativ","Dativ und Akkusativ","Dative and accusative","Person vor Sache","Der Lehrer erklärt den Schülern die Aufgabe.","Der Lehrer erklärt die Schüler die Aufgabe."),
    (3,1,"two_way_prepositions","grammar","Wechselpräpositionen","Wechselpräpositionen","Two-way prepositions","wo = Dativ, wohin = Akkusativ","Ich stelle die Vase auf den Tisch.","Ich stelle die Vase auf dem Tisch."),
    (4,1,"dative_prepositions","grammar","Предлоги с Dativ","Dativpräpositionen","Dative prepositions","mit / nach / bei / seit","Seit einem Jahr wohne ich bei meiner Tante.","Seit einen Jahr wohne ich bei meine Tante."),
    (5,1,"accusative_prepositions","grammar","Предлоги с Akkusativ","Akkusativpräpositionen","Accusative prepositions","für / ohne / durch / gegen","Das Geschenk ist für meinen Bruder.","Das Geschenk ist für meinem Bruder."),
    (6,2,"perfect_haben","grammar","Perfekt с haben","Perfekt mit haben","Perfect with haben","haben + Partizip II","Ich habe gestern einen Film gesehen.","Ich bin gestern einen Film gesehen."),
    (7,2,"perfect_sein","grammar","Perfekt с sein","Perfekt mit sein","Perfect with sein","sein bei Bewegung","Wir sind am Wochenende nach Lübeck gefahren.","Wir haben am Wochenende nach Lübeck gefahren."),
    (8,2,"perfect_participles","grammar","Partizip II","Partizip II","Past participles","ge- / starke Formen","Sie hat die E-Mail geschrieben und abgeschickt.","Sie hat die E-Mail geschreibt und abschicken."),
    (9,2,"modal_past_a2","grammar","Modalverben в прошлом","Modalverben im Präteritum","Past modal verbs","konnte / musste / durfte","Früher musste ich jeden Samstag arbeiten.","Früher muss ich jeden Samstag arbeiten."),
    (10,2,"past_sequence","speaking","Рассказ о прошлом","Vergangenes erzählen","Narrating past events","zuerst / dann / danach","Zuerst bin ich aufgestanden, danach habe ich gefrühstückt.","Zuerst ich bin aufgestanden, danach ich habe gefrühstückt."),
    (11,3,"weil_clause","grammar","Придаточные с weil","Nebensätze mit weil","Clauses with weil","Verb am Ende","Ich lerne Deutsch, weil ich in Deutschland arbeite.","Ich lerne Deutsch, weil ich arbeite in Deutschland."),
    (12,3,"dass_clause","grammar","Придаточные с dass","Nebensätze mit dass","Clauses with dass","Verb am Ende","Ich glaube, dass der Kurs sehr hilfreich ist.","Ich glaube, dass ist der Kurs sehr hilfreich."),
    (13,3,"wenn_clause","grammar","Придаточные с wenn","Nebensätze mit wenn","Clauses with wenn","Bedingung + Verbende","Wenn ich Zeit habe, besuche ich meine Freunde.","Wenn ich habe Zeit, ich besuche meine Freunde."),
    (14,3,"comparatives","grammar","Сравнение","Komparativ und Superlativ","Comparatives","-er / am -sten","Der Zug ist schneller als der Bus.","Der Zug ist mehr schnell als der Bus."),
    (15,3,"reflexive_verbs","grammar","Возвратные глаголы","Reflexive Verben","Reflexive verbs","mich / dich / sich","Ich interessiere mich für moderne Kunst.","Ich interessiere für moderne Kunst."),
    (16,4,"requests_a2","speaking","Вежливая просьба","Höflich bitten","Polite requests","könnte / würde","Könnten Sie mir bitte einen Termin geben?","Können Sie geben mir bitte einen Termin?"),
    (17,4,"formal_message_a2","writing","Официальное сообщение","Formelle Nachricht","Formal message","Anrede + Anliegen + Schluss","Sehr geehrte Frau Klein, ich möchte meinen Termin verschieben.","Hallo Frau Klein, ich will anderen Termin."),
    (18,4,"opinions_a2","speaking","Мнение и причина","Meinung und Grund","Opinion and reason","ich finde …, weil","Ich finde den Kurs gut, weil wir viel sprechen.","Ich finde den Kurs gut, weil wir sprechen viel."),
    (19,4,"problem_solution_a2","speaking","Проблема и решение","Problem und Lösung","Problem and solution","Problem erklären + Bitte","Mein Zug fällt aus. Deshalb brauche ich eine andere Verbindung.","Mein Zug ausfällt. Ich brauche deshalb andere Verbindung."),
    (20,4,"a2_final","mixed","Итоговая задача A2","A2-Abschlussaufgabe","A2 final task","Vergangenheit + Grund + Plan","Letztes Jahr bin ich umgezogen, weil ich eine neue Stelle gefunden habe.","Letztes Jahr ich bin umgezogen, weil ich habe neue Stelle gefunden."),
]


def _localized(base: dict, ru: dict, de: dict, en: dict) -> dict:
    return {**base, "i18n": {"ru": ru, "de": de, "en": en}}


def build_foundation_content(row: tuple, level: str) -> dict:
    day, module, topic, pillar, title_ru, title_de, title_en, focus, model, wrong = row
    rules = {
        "ru": f"Отработай структуру «{focus}» и используй её в понятной немецкой фразе.",
        "de": f"Übe die Struktur „{focus}“ und nutze sie in einem klaren deutschen Satz.",
        "en": f"Practise the “{focus}” pattern and use it in a clear German sentence.",
    }
    goals = {
        "ru": f"Самостоятельно использовать {focus} в повседневной ситуации.",
        "de": f"{focus} selbstständig in einer Alltagssituation verwenden.",
        "en": f"Use {focus} independently in an everyday situation.",
    }
    patterns = [word.casefold().strip(".,;:?!") for word in model.split() if len(word) > 3][:4]
    exercises = [
        _localized(
            {"type":"error_repair","stage":"guided","question":f"Исправь: {wrong}","answer":model,"accepted_answers":[model,model.rstrip(".")],"hint":rules["ru"],"explanation":rules["ru"],"misconception":"foundation_form"},
            {"question":f"Исправь: {wrong}","hint":rules["ru"],"explanation":rules["ru"]},
            {"question":f"Korrigiere: {wrong}","hint":rules["de"],"explanation":rules["de"]},
            {"question":f"Correct: {wrong}","hint":rules["en"],"explanation":rules["en"]},
        ),
        _localized(
            {"type":"context_choice","stage":"independent","question":"Выбери фразу, подходящую ситуации.","answer":model,"accepted_answers":[model],"options":[model,wrong,f"{model.rstrip('.')} nicht."],"explanation":rules["ru"],"misconception":"foundation_context"},
            {"question":"Выбери фразу, подходящую ситуации.","explanation":rules["ru"]},
            {"question":"Wähle den Satz, der zur Situation passt.","explanation":rules["de"]},
            {"question":"Choose the sentence that fits the situation.","explanation":rules["en"]},
        ),
        _localized(
            {"type":"listening_choice","stage":"independent","question":"Прослушай модель. Какую структуру ты слышишь?","answer":focus,"accepted_answers":[focus],"options":[focus,"Begrüßung","Zeitangabe"],"explanation":model,"misconception":"foundation_listening"},
            {"question":"Прослушай модель. Какую структуру ты слышишь?","explanation":model},
            {"question":"Höre das Modell. Welche Struktur hörst du?","explanation":model},
            {"question":"Listen to the model. Which pattern do you hear?","explanation":model},
        ),
        _localized(
            {"type":"dialogue","stage":"transfer","question":goals["ru"],"answer":model,"model_answer":model,"accepted_answers":[model,model.rstrip(".")],"target_patterns":patterns,"hint":rules["ru"],"explanation":"Сравни свой ответ с моделью.","misconception":"foundation_transfer"},
            {"question":goals["ru"],"hint":rules["ru"],"explanation":"Сравни свой ответ с моделью."},
            {"question":goals["de"],"hint":rules["de"],"explanation":"Vergleiche deine Antwort mit dem Modell."},
            {"question":goals["en"],"hint":rules["en"],"explanation":"Compare your response with the model."},
        ),
        _localized(
            {"type":"repeat","stage":"transfer","question":"Произнеси модель вслух.","answer":model,"accepted_answers":[model,model.rstrip(".")],"explanation":"Повтори спокойно и чётко.","misconception":"foundation_fluency"},
            {"question":"Произнеси модель вслух.","explanation":"Повтори спокойно и чётко."},
            {"question":"Sprich das Modell laut nach.","explanation":"Sprich ruhig und deutlich."},
            {"question":"Say the model aloud.","explanation":"Speak calmly and clearly."},
        ),
    ]
    return {
        "day":day,"week":module,"track":level,"module":module,"quality_version":4,
        "learning_method":"notice_build_use_reflect","title":title_ru,"objective":goals["ru"],
        "communication_goal":goals["ru"],"rule":rules["ru"],"examples":[model,model.rstrip("."),f"{level}-Muster: {model}"],
        "audio_text":model,"cefr":level,"prerequisites":[],"common_mistakes":[f"❌ {wrong}",f"✅ {model}"],
        "recall_prompt":"Закрой пример, назови правило и создай собственную фразу.",
        "i18n":{"ru":{"title":title_ru,"rule":rules["ru"],"objective":goals["ru"]},"de":{"title":title_de,"rule":rules["de"],"objective":goals["de"]},"en":{"title":title_en,"rule":rules["en"],"objective":goals["en"]}},
        "exercises":exercises,
    }
