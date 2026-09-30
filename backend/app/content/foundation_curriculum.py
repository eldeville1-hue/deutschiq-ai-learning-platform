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

# A concrete situation, a second natural model, and minimal language markers
# for each foundation skill. These keep free production open-ended without
# accepting unrelated text or forcing learners to copy names and places.
PRACTICE_VARIANTS = {
    "greetings": ("Ты встречаешь соседа утром.", "Du triffst morgens deinen Nachbarn.", "You meet your neighbour in the morning.", "Hallo! Ich bin Sara.", ["hallo", "heiße"]),
    "personal_details": ("Ты знакомишься с участником курса.", "Du lernst jemanden im Kurs kennen.", "You meet someone in your course.", "Ich bin Leo und wohne in Bremen.", ["ich", "komme"]),
    "main_clause": ("Ты рассказываешь, что делаешь сегодня.", "Du erzählst, was du heute machst.", "You say what you are doing today.", "Am Abend koche ich zu Hause.", ["ich"]),
    "yes_no_questions": ("Ты уточняешь план друга.", "Du fragst nach dem Plan eines Freundes.", "You check a friend's plan.", "Hast du morgen Zeit?", ["du"]),
    "w_questions": ("Ты хочешь узнать место встречи.", "Du möchtest den Treffpunkt wissen.", "You want to know the meeting place.", "Wann beginnt der Kurs?", ["wo", "wann"]),
    "present_regular": ("Ты описываешь вечернюю привычку.", "Du beschreibst eine Abendroutine.", "You describe an evening habit.", "Ich lerne nach der Arbeit Deutsch.", ["lerne", "arbeiten"]),
    "sein_haben": ("Ты объясняешь своё состояние и время.", "Du erklärst deinen Zustand und deine Zeit.", "You explain how you feel and whether you have time.", "Wir sind bereit und haben noch Zeit.", ["bin", "habe"]),
    "noun_gender": ("Ты показываешь вещи в комнате.", "Du zeigst Dinge im Zimmer.", "You point out objects in a room.", "Hier sind ein Tisch und eine Tasche.", ["ein", "eine"]),
    "plural": ("Ты описываешь несколько предметов.", "Du beschreibst mehrere Gegenstände.", "You describe several objects.", "Die Stühle stehen am Fenster.", ["die"]),
    "negation": ("Ты говоришь, чего у тебя нет.", "Du sagst, was du nicht hast.", "You say what you do not have.", "Ich habe keine Fahrkarte.", ["kein", "keine"]),
    "accusative_a1": ("Ты заказываешь еду в кафе.", "Du bestellst etwas im Café.", "You order something in a café.", "Ich nehme einen Tee und eine Suppe.", ["einen", "eine"]),
    "modal_verbs_a1": ("Ты говоришь, что можешь сделать сегодня.", "Du sagst, was du heute tun kannst.", "You say what you can do today.", "Wir müssen jetzt nach Hause gehen.", ["kann", "muss"]),
    "separable_verbs_a1": ("Ты сообщаешь время начала.", "Du nennst eine Anfangszeit.", "You say when something starts.", "Der Zug kommt um acht Uhr an.", ["an", "auf"]),
    "time_daily_routine": ("Ты описываешь начало своего дня.", "Du beschreibst den Beginn deines Tages.", "You describe the start of your day.", "Um acht Uhr fahre ich zur Arbeit.", ["uhr"]),
    "directions": ("Ты ищешь остановку в незнакомом городе.", "Du suchst in einer fremden Stadt die Haltestelle.", "You are looking for a stop in an unfamiliar city.", "Entschuldigung, wie komme ich zum Bahnhof?", ["wo", "wie"]),
    "shopping": ("Ты покупаешь продукты на рынке.", "Du kaufst auf dem Markt ein.", "You buy groceries at a market.", "Ich möchte bitte zwei Brötchen.", ["möchte", "hätte gern"]),
    "appointments": ("Ты подтверждаешь запись по телефону.", "Du bestätigst telefonisch einen Termin.", "You confirm an appointment by phone.", "Wir treffen uns am Dienstag um elf Uhr.", ["am", "um"]),
    "family": ("Ты коротко рассказываешь о родственнике.", "Du erzählst kurz von einem Familienmitglied.", "You briefly describe a family member.", "Mein Bruder lebt mit seiner Familie in Bonn.", ["mein", "meine"]),
    "simple_past_experience": ("Ты рассказываешь, что делал вчера.", "Du erzählst, was du gestern gemacht hast.", "You say what you did yesterday.", "Gestern habe ich meine Freundin besucht.", ["habe", "bin"]),
    "a1_final": ("Ты представляешься новой группе.", "Du stellst dich einer neuen Gruppe vor.", "You introduce yourself to a new group.", "Ich bin Omar, komme aus Köln und arbeite im Hotel.", ["ich", "komme"]),
    "dative_a2": ("Ты передаёшь вещь знакомому.", "Du gibst einer bekannten Person etwas.", "You give something to someone you know.", "Ich bringe meinem Nachbarn ein Paket.", ["meinem", "meiner"]),
    "dative_accusative": ("Ты объясняешь, кто получает какую вещь.", "Du erklärst, wer welche Sache bekommt.", "You explain who receives which item.", "Ich zeige meiner Kollegin den Plan.", ["meinem", "meiner"]),
    "two_way_prepositions": ("Ты переставляешь предмет в комнате.", "Du stellst einen Gegenstand im Zimmer um.", "You move an object in a room.", "Ich hänge das Bild an die Wand.", ["auf den", "in die", "an die"]),
    "dative_prepositions": ("Ты говоришь, с кем или где живёшь.", "Du sagst, mit wem oder wo du wohnst.", "You say whom you live with or where.", "Ich fahre mit meiner Schwester nach Berlin.", ["mit", "seit", "bei"]),
    "accusative_prepositions": ("Ты объясняешь назначение покупки.", "Du erklärst, für wen ein Kauf ist.", "You explain who a purchase is for.", "Diese Blumen sind für meine Mutter.", ["für", "ohne"]),
    "perfect_haben": ("Ты рассказываешь о вчерашнем вечере.", "Du erzählst von gestern Abend.", "You talk about yesterday evening.", "Gestern habe ich lange telefoniert.", ["habe", "hat"]),
    "perfect_sein": ("Ты рассказываешь о поездке.", "Du erzählst von einer Fahrt.", "You talk about a trip.", "Am Samstag bin ich nach Bremen gefahren.", ["bin", "sind"]),
    "perfect_participles": ("Ты перечисляешь завершённые дела.", "Du nennst erledigte Aufgaben.", "You list completed tasks.", "Ich habe eingekauft und das Essen vorbereitet.", ["ge", "geschrieben"]),
    "modal_past_a2": ("Ты сравниваешь прошлые обязанности с сегодняшними.", "Du vergleichst frühere Pflichten mit heute.", "You compare past duties with today.", "Als Kind durfte ich lange draußen spielen.", ["musste", "konnte", "durfte"]),
    "past_sequence": ("Ты рассказываешь два события по порядку.", "Du erzählst zwei Ereignisse in Reihenfolge.", "You narrate two events in order.", "Dann habe ich angerufen, danach bin ich losgefahren.", ["zuerst", "danach"]),
    "weil_clause": ("Ты объясняешь своё решение.", "Du begründest deine Entscheidung.", "You explain your decision.", "Ich fahre mit dem Bus, weil es regnet.", ["weil"]),
    "dass_clause": ("Ты передаёшь мнение или информацию.", "Du gibst eine Meinung oder Information weiter.", "You report an opinion or information.", "Ich denke, dass die Prüfung gut läuft.", ["dass"]),
    "wenn_clause": ("Ты описываешь условие для плана.", "Du nennst eine Bedingung für einen Plan.", "You state a condition for a plan.", "Wenn das Wetter gut ist, gehen wir spazieren.", ["wenn"]),
    "comparatives": ("Ты сравниваешь два варианта поездки.", "Du vergleichst zwei Reisemöglichkeiten.", "You compare two travel options.", "Das Fahrrad ist günstiger als das Auto.", ["als", "am"]),
    "reflexive_verbs": ("Ты рассказываешь об интересе или привычке.", "Du sprichst über ein Interesse oder eine Gewohnheit.", "You talk about an interest or habit.", "Wir treffen uns jeden Freitag im Café.", ["mich", "dich", "sich", "uns"]),
    "requests_a2": ("Ты вежливо просишь о помощи.", "Du bittest höflich um Hilfe.", "You ask politely for help.", "Würden Sie mir bitte kurz helfen?", ["könnten", "würden"]),
    "formal_message_a2": ("Ты переносишь запись письмом.", "Du verschiebst einen Termin schriftlich.", "You reschedule an appointment in writing.", "Sehr geehrter Herr Wolf, leider kann ich morgen nicht kommen.", ["sehr geehrte", "leider"]),
    "opinions_a2": ("Ты высказываешь мнение и называешь причину.", "Du äußerst eine Meinung mit Begründung.", "You give an opinion and a reason.", "Ich finde die Wohnung praktisch, weil sie zentral liegt.", ["ich finde", "weil"]),
    "problem_solution_a2": ("Ты объясняешь проблему сотруднику сервиса.", "Du erklärst einem Servicemitarbeiter ein Problem.", "You explain a problem to service staff.", "Mein Ticket funktioniert nicht. Können Sie mir helfen?", ["deshalb", "können sie"]),
    "a2_final": ("Ты рассказываешь о перемене и следующем плане.", "Du erzählst von einer Veränderung und deinem nächsten Plan.", "You describe a change and your next plan.", "Vor zwei Monaten habe ich einen Kurs begonnen, weil ich die B1-Prüfung machen möchte.", ["weil", "habe", "bin"]),
}


# The first five A1 lessons are the product's quality reference: one connected
# story, one immediately useful outcome per lesson, and language a beginner can
# reuse during a real first conversation. Later modules should follow this shape.
A1_FIRST_CONVERSATION = {
    "greetings": {
        "title": ("Поздоровайся", "Begrüße jemanden", "Greet someone"),
        "scenario": ("Первый день на языковых курсах. Ты входишь в класс.", "Dein erster Tag im Sprachkurs. Du kommst in den Raum.", "It is your first day at a language course. You enter the room."),
        "can_do": ("Ты сможешь поздороваться и назвать своё имя.", "Du kannst grüßen und deinen Namen sagen.", "You can say hello and give your name."),
        "rule": ("Скажи Guten Morgen или Hallo. Затем: Ich heiße + имя.", "Sage Guten Morgen oder Hallo. Dann: Ich heiße + Name.", "Say Guten Morgen or Hallo. Then use: Ich heiße + name."),
        "model": "Guten Morgen! Ich heiße Mia.",
        "alternate": "Hallo! Ich heiße Amir.",
        "wrong": "Guten Morgen! Ich heißen Mia.",
        "choice": ("Что ты скажешь преподавателю?", "Was sagst du zur Kursleiterin?", "What do you say to the teacher?"),
        "listen_answer": ("Приветствие и имя", "Begrüßung und Name", "Greeting and name"),
        "listen_options": (("Приветствие и имя", "Только город", "Вопрос о работе"), ("Begrüßung und Name", "Nur ein Ort", "Eine Frage zur Arbeit"), ("Greeting and name", "Only a city", "A question about work")),
        "task": ("Поздоровайся и назови своё имя.", "Begrüße die Person und sage deinen Namen.", "Greet the person and say your name."),
        "patterns": ["hallo", "heiße"],
    },
    "personal_details": {
        "title": ("Скажи, откуда ты", "Sage, woher du kommst", "Say where you are from"),
        "scenario": ("Сосед по курсу спрашивает, откуда ты и где живёшь.", "Eine Person im Kurs fragt, woher du kommst und wo du wohnst.", "Someone in the course asks where you are from and where you live."),
        "can_do": ("Ты сможешь коротко рассказать, откуда ты и где живёшь.", "Du kannst kurz sagen, woher du kommst und wo du wohnst.", "You can briefly say where you are from and where you live."),
        "rule": ("Ich komme aus + страна/город. Ich wohne in + город.", "Ich komme aus + Land/Stadt. Ich wohne in + Stadt.", "Use Ich komme aus + country/city and Ich wohne in + city."),
        "model": "Ich komme aus Kyjiw und wohne in Hamburg.",
        "alternate": "Ich komme aus Syrien und wohne in Bremen.",
        "wrong": "Ich aus Kyjiw und ich wohnen Hamburg.",
        "choice": ("Как представиться новому участнику курса?", "Wie stellst du dich einer neuen Person im Kurs vor?", "How do you introduce yourself to a new classmate?"),
        "listen_answer": ("Происхождение и место жительства", "Herkunft und Wohnort", "Origin and place of residence"),
        "listen_options": (("Происхождение и место жительства", "Возраст и телефон", "Заказ в кафе"), ("Herkunft und Wohnort", "Alter und Telefonnummer", "Eine Bestellung im Café"), ("Origin and place of residence", "Age and phone number", "An order in a café")),
        "task": ("Скажи, откуда ты и где сейчас живёшь.", "Sage, woher du kommst und wo du jetzt wohnst.", "Say where you are from and where you live now."),
        "patterns": ["komme aus", "wohne in"],
    },
    "main_clause": {
        "title": ("Расскажи о себе", "Erzähle von dir", "Talk about yourself"),
        "scenario": ("В перерыве вы говорите о работе и изучении немецкого.", "In der Pause sprecht ihr über Arbeit und Deutschlernen.", "During the break you talk about work and learning German."),
        "can_do": ("Ты сможешь сказать, чем занимаешься сегодня.", "Du kannst sagen, was du heute machst.", "You can say what you are doing today."),
        "rule": ("В обычной фразе действие стоит на втором месте: Heute lerne ich Deutsch.", "Im Aussagesatz steht das Verb auf Position 2: Heute lerne ich Deutsch.", "In a statement, the verb is in position 2: Heute lerne ich Deutsch."),
        "model": "Heute lerne ich Deutsch.",
        "alternate": "Am Vormittag arbeite ich im Hotel.",
        "wrong": "Heute ich lerne Deutsch.",
        "choice": ("Как сказать, что ты сегодня учишь немецкий?", "Wie sagst du, dass du heute Deutsch lernst?", "How do you say that you are learning German today?"),
        "listen_answer": ("Время + действие + человек", "Zeit + Verb + Person", "Time + verb + person"),
        "listen_options": (("Время + действие + человек", "Человек + два глагола", "Только приветствие"), ("Zeit + Verb + Person", "Person + zwei Verben", "Nur eine Begrüßung"), ("Time + verb + person", "Person + two verbs", "Only a greeting")),
        "task": ("Скажи одной фразой, что ты делаешь сегодня.", "Sage in einem Satz, was du heute machst.", "Say in one sentence what you are doing today."),
        "patterns": ["ich"],
    },
    "yes_no_questions": {
        "title": ("Задай простой вопрос", "Stelle eine einfache Frage", "Ask a simple question"),
        "scenario": ("Ты хочешь узнать, придёт ли новый знакомый завтра.", "Du möchtest wissen, ob die neue Bekanntschaft morgen kommt.", "You want to know whether your new acquaintance is coming tomorrow."),
        "can_do": ("Ты сможешь задать вопрос с ответом ja или nein.", "Du kannst eine Frage mit ja oder nein stellen.", "You can ask a yes-or-no question."),
        "rule": ("В вопросе без вопросительного слова действие стоит первым: Kommst du morgen?", "In einer Ja-/Nein-Frage steht das Verb zuerst: Kommst du morgen?", "In a yes-or-no question, the verb comes first: Kommst du morgen?"),
        "model": "Kommst du morgen zum Kurs?",
        "alternate": "Lernst du auch Deutsch?",
        "wrong": "Du kommst morgen zum Kurs?",
        "choice": ("Как прямо спросить о завтрашнем курсе?", "Wie fragst du direkt nach dem Kurs morgen?", "How do you ask directly about tomorrow's course?"),
        "listen_answer": ("Вопрос с ja или nein", "Frage mit ja oder nein", "A yes-or-no question"),
        "listen_options": (("Вопрос с ja или nein", "Рассказ о вчера", "Просьба в магазине"), ("Frage mit ja oder nein", "Erzählung über gestern", "Bitte im Geschäft"), ("A yes-or-no question", "A story about yesterday", "A request in a shop")),
        "task": ("Спроси собеседника, учит ли он немецкий.", "Frage die Person, ob sie Deutsch lernt.", "Ask the person whether they are learning German."),
        "patterns": ["du"],
    },
    "w_questions": {
        "title": ("Поддержи разговор", "Halte das Gespräch am Laufen", "Keep the conversation going"),
        "scenario": ("Перед уходом ты хочешь узнать больше о новом знакомом.", "Bevor ihr geht, möchtest du mehr über die neue Bekanntschaft wissen.", "Before leaving, you want to learn more about your new acquaintance."),
        "can_do": ("Ты сможешь спросить где, откуда и что человек делает.", "Du kannst nach Ort, Herkunft und Tätigkeit fragen.", "You can ask about place, origin, and activity."),
        "rule": ("Сначала вопросительное слово, затем действие: Wo wohnst du?", "Zuerst kommt das Fragewort, dann das Verb: Wo wohnst du?", "Put the question word first and the verb second: Wo wohnst du?"),
        "model": "Wo wohnst du?",
        "alternate": "Woher kommst du?",
        "wrong": "Wo du wohnst?",
        "choice": ("Как спросить нового знакомого о месте жительства?", "Wie fragst du die neue Bekanntschaft nach dem Wohnort?", "How do you ask your new acquaintance where they live?"),
        "listen_answer": ("Вопрос о месте", "Frage nach einem Ort", "A question about a place"),
        "listen_options": (("Вопрос о месте", "Приветствие", "Ответ о времени"), ("Frage nach einem Ort", "Begrüßung", "Antwort über eine Zeit"), ("A question about a place", "A greeting", "An answer about time")),
        "task": ("Задай два вопроса: откуда человек и где он живёт.", "Stelle zwei Fragen: Woher kommt die Person und wo wohnt sie?", "Ask two questions: where the person comes from and where they live."),
        "patterns": ["wo", "woher"],
        "checkpoint": True,
    },
}


# Every gold-module lesson closes with a short, contextual conversation.  The
# German partner lines stay authentic while the coaching goal is localized.
A1_MISSION_DIALOGUES = {
    "greetings": [
        ("Guten Morgen! Willkommen im Kurs. Wie heißt du?", ("Поздоровайся и назови своё имя.", "Begrüße die Person und sage deinen Namen.", "Greet the person and say your name."), "Hallo! Ich heiße …", "Hallo! Ich heiße Mia."),
        ("Freut mich! Schön, dass du da bist.", ("Ответь коротко и дружелюбно.", "Antworte kurz und freundlich.", "Reply briefly and politely."), "Danke, freut mich!", "Danke, freut mich!"),
    ],
    "personal_details": [
        ("Hallo! Woher kommst du?", ("Скажи, откуда ты.", "Sage, woher du kommst.", "Say where you are from."), "Ich komme aus …", "Ich komme aus Kyjiw."),
        ("Und wo wohnst du jetzt?", ("Скажи, где ты сейчас живёшь.", "Sage, wo du jetzt wohnst.", "Say where you live now."), "Ich wohne in …", "Ich wohne in Hamburg."),
    ],
    "main_clause": [
        ("Was machst du heute?", ("Начни со слова Heute и назови действие.", "Beginne mit Heute und nenne eine Handlung.", "Begin with Heute and name an action."), "Heute … ich …", "Heute lerne ich Deutsch."),
        ("Und was machst du am Abend?", ("Начни с Am Abend; глагол поставь вторым.", "Beginne mit Am Abend; das Verb steht an Position zwei.", "Begin with Am Abend; put the verb in position two."), "Am Abend … ich …", "Am Abend koche ich zu Hause."),
    ],
    "yes_no_questions": [
        ("Ich komme morgen wieder zum Kurs.", ("Спроси, придёт ли собеседник завтра.", "Frage, ob die Person morgen kommt.", "Ask whether the person is coming tomorrow."), "Kommst du …?", "Kommst du morgen zum Kurs?"),
        ("Ja, gern. Und du?", ("Задай ещё один вопрос с ответом ja или nein.", "Stelle noch eine Ja-/Nein-Frage.", "Ask one more yes-or-no question."), "Lernst du …?", "Lernst du auch Deutsch?"),
    ],
    "w_questions": [
        ("Guten Morgen! Ich heiße Lena. Wie heißt du?", ("Поздоровайся и назови своё имя.", "Begrüße die Person und sage deinen Namen.", "Greet the person and say your name."), "Hallo! Ich heiße …", "Hallo! Ich heiße Alex."),
        ("Freut mich! Frag mich, woher ich komme.", ("Задай вопрос с Woher.", "Stelle eine Frage mit Woher.", "Ask a question with Woher."), "Woher …?", "Woher kommst du?"),
        ("Ich komme aus Köln. Frag mich jetzt, wo ich wohne.", ("Задай вопрос с Wo.", "Stelle eine Frage mit Wo.", "Ask a question with Wo."), "Wo …?", "Wo wohnst du?"),
    ],
}


# The remaining A1 route is authored as connected real-life missions instead
# of grammar-labelled template drills.  Each five-lesson module ends in a
# checkpoint that reuses several earlier skills without showing a model first.
A1_MISSION_BLUEPRINTS = {
    "present_regular": {
        "module_title": ("Повседневная жизнь", "Alltag", "Everyday life"),
        "title": ("Расскажи о своей привычке", "Erzähle von deiner Gewohnheit", "Describe your routine"),
        "scenario": ("После курса вы говорите о том, как учите немецкий дома.", "Nach dem Kurs sprecht ihr darüber, wie ihr zu Hause Deutsch lernt.", "After class, you talk about how you study German at home."),
        "can_do": ("Ты сможешь описать одну регулярную привычку.", "Du kannst eine regelmäßige Gewohnheit beschreiben.", "You can describe one regular habit."),
        "task": ("Расскажи, когда и как ты обычно учишь немецкий.", "Erzähle, wann und wie du normalerweise Deutsch lernst.", "Say when and how you normally study German."),
        "alternate": "Ich übe jeden Morgen zehn Minuten.",
        "turns": [
            ("Wann lernst du normalerweise Deutsch?", ("Назови время и действие.", "Nenne eine Zeit und eine Handlung.", "Give a time and an activity."), "Ich lerne …", "Ich lerne jeden Abend Deutsch."),
            ("Und wie übst du zu Hause?", ("Назови ещё одну привычку.", "Nenne noch eine Gewohnheit.", "Name one more habit."), "Ich … jeden …", "Ich höre jeden Morgen einen Podcast."),
        ],
    },
    "sein_haben": {
        "module_title": ("Повседневная жизнь", "Alltag", "Everyday life"),
        "title": ("Скажи, как ты себя чувствуешь", "Sage, wie es dir geht", "Say how you feel"),
        "scenario": ("Друг спрашивает, готов ли ты пойти на встречу.", "Ein Freund fragt, ob du für ein Treffen bereit bist.", "A friend asks whether you are ready to meet."),
        "can_do": ("Ты сможешь сказать о своём состоянии и времени.", "Du kannst über deinen Zustand und deine Zeit sprechen.", "You can talk about how you feel and whether you have time."),
        "task": ("Скажи, как ты себя чувствуешь и есть ли у тебя время.", "Sage, wie du dich fühlst und ob du Zeit hast.", "Say how you feel and whether you have time."),
        "alternate": "Ich bin bereit und habe heute Zeit.",
        "turns": [
            ("Wie geht es dir heute?", ("Ответь с sein.", "Antworte mit sein.", "Answer using sein."), "Ich bin …", "Ich bin heute etwas müde."),
            ("Hast du trotzdem Zeit für einen Kaffee?", ("Ответь с haben.", "Antworte mit haben.", "Answer using haben."), "Ich habe …", "Ja, ich habe eine halbe Stunde Zeit."),
        ],
    },
    "noun_gender": {
        "module_title": ("Повседневная жизнь", "Alltag", "Everyday life"),
        "title": ("Назови вещи вокруг", "Benenne Dinge um dich herum", "Name things around you"),
        "scenario": ("Ты показываешь новому соседу вещи в общей кухне.", "Du zeigst einem neuen Mitbewohner Dinge in der gemeinsamen Küche.", "You show a new flatmate things in the shared kitchen."),
        "can_do": ("Ты сможешь назвать предметы с правильным артиклем.", "Du kannst Gegenstände mit dem richtigen Artikel nennen.", "You can name objects with the correct article."),
        "task": ("Покажи и назови два предмета с ein или eine.", "Zeige und benenne zwei Gegenstände mit ein oder eine.", "Point out and name two objects using ein or eine."),
        "alternate": "Hier sind ein Tisch und eine Lampe.",
        "turns": [
            ("Was ist das neben dem Fenster?", ("Назови предмет с артиклем.", "Nenne den Gegenstand mit Artikel.", "Name the object with its article."), "Das ist ein/eine …", "Das ist ein Tisch."),
            ("Und was steht auf dem Tisch?", ("Назови второй предмет.", "Nenne einen zweiten Gegenstand.", "Name a second object."), "Da steht …", "Da steht eine Lampe."),
        ],
    },
    "plural": {
        "module_title": ("Повседневная жизнь", "Alltag", "Everyday life"),
        "title": ("Опиши несколько вещей", "Beschreibe mehrere Dinge", "Describe several things"),
        "scenario": ("Вы вместе проверяете, что уже есть в комнате.", "Ihr prüft gemeinsam, was schon im Zimmer steht.", "Together, you check what is already in the room."),
        "can_do": ("Ты сможешь сказать о нескольких предметах.", "Du kannst über mehrere Gegenstände sprechen.", "You can talk about several objects."),
        "task": ("Назови две группы предметов во множественном числе.", "Nenne zwei Gruppen von Gegenständen im Plural.", "Name two groups of objects in the plural."),
        "alternate": "Die Stühle stehen am Fenster.",
        "turns": [
            ("Was steht am Fenster?", ("Ответь во множественном числе.", "Antworte im Plural.", "Answer in the plural."), "Die … stehen …", "Die Stühle stehen am Fenster."),
            ("Und wo liegen die Bücher?", ("Назови место.", "Nenne den Ort.", "Give the location."), "Die Bücher liegen …", "Die Bücher liegen auf dem Tisch."),
        ],
    },
    "negation": {
        "module_title": ("Повседневная жизнь", "Alltag", "Everyday life"),
        "title": ("Объясни, чего не хватает", "Erkläre, was fehlt", "Explain what is missing"),
        "scenario": ("Перед поездкой вы проверяете вещи и планы на день.", "Vor einer Fahrt prüft ihr eure Sachen und Pläne für den Tag.", "Before a trip, you check your things and plans for the day."),
        "can_do": ("Ты сможешь сказать, чего у тебя нет и что ты не делаешь.", "Du kannst sagen, was du nicht hast und was du nicht machst.", "You can say what you do not have and do not do."),
        "task": ("Скажи одну фразу с kein и одну с nicht.", "Sage einen Satz mit kein und einen mit nicht.", "Say one sentence with kein and one with nicht."),
        "alternate": "Ich habe keine Fahrkarte und fahre heute nicht.",
        "checkpoint": True,
        "turns": [
            ("Hast du eine Fahrkarte?", ("Ответь с kein.", "Antworte mit kein.", "Answer using kein."), "Ich habe kein/keine …", "Nein, ich habe keine Fahrkarte."),
            ("Fährst du heute mit?", ("Ответь с nicht.", "Antworte mit nicht.", "Answer using nicht."), "Ich fahre heute nicht.", "Nein, ich fahre heute nicht."),
            ("Was fehlt dir noch?", ("Назови ещё одну вещь, которой нет.", "Nenne noch eine Sache, die fehlt.", "Name one more thing you do not have."), "Ich habe kein/keine …", "Ich habe kein Ladegerät."),
        ],
    },
    "accusative_a1": {
        "module_title": ("В городе", "Unterwegs", "Out and about"),
        "title": ("Закажи в кафе", "Bestelle im Café", "Order at a café"),
        "scenario": ("Ты делаешь простой заказ в кафе.", "Du bestellst etwas in einem Café.", "You place a simple order at a café."),
        "can_do": ("Ты сможешь заказать напиток и еду.", "Du kannst ein Getränk und etwas zu essen bestellen.", "You can order a drink and something to eat."),
        "task": ("Закажи два продукта с правильными артиклями.", "Bestelle zwei Produkte mit den richtigen Artikeln.", "Order two items using the correct articles."),
        "alternate": "Ich nehme einen Tee und eine Suppe.",
        "turns": [
            ("Guten Tag! Was möchten Sie trinken?", ("Закажи напиток.", "Bestelle ein Getränk.", "Order a drink."), "Ich nehme einen/eine …", "Ich nehme einen Kaffee."),
            ("Möchten Sie auch etwas essen?", ("Закажи еду.", "Bestelle etwas zu essen.", "Order something to eat."), "Und ein/eine …", "Ja, und ein Brötchen, bitte."),
        ],
    },
    "modal_verbs_a1": {
        "module_title": ("В городе", "Unterwegs", "Out and about"),
        "title": ("Договорись о планах", "Sprich über Pläne", "Talk about plans"),
        "scenario": ("Друг предлагает встретиться после работы.", "Ein Freund möchte sich nach der Arbeit treffen.", "A friend wants to meet after work."),
        "can_do": ("Ты сможешь сказать, что можешь или должен сделать.", "Du kannst sagen, was du kannst oder musst.", "You can say what you can or must do."),
        "task": ("Скажи, что ты должен сделать и когда можешь встретиться.", "Sage, was du tun musst und wann du dich treffen kannst.", "Say what you must do and when you can meet."),
        "alternate": "Ich muss bis sechs arbeiten, aber danach kann ich kommen.",
        "turns": [
            ("Kannst du heute um fünf kommen?", ("Скажи, что ты должен сделать.", "Sage, was du tun musst.", "Say what you have to do."), "Ich muss …", "Ich muss bis sechs arbeiten."),
            ("Wann kannst du kommen?", ("Предложи время с können.", "Schlage eine Zeit mit können vor.", "Offer a time using können."), "Ich kann um …", "Ich kann um halb sieben kommen."),
        ],
    },
    "separable_verbs_a1": {
        "module_title": ("В городе", "Unterwegs", "Out and about"),
        "title": ("Сообщи время", "Nenne eine Uhrzeit", "Give a time"),
        "scenario": ("Вы уточняете, когда начинается курс и прибывает поезд.", "Ihr klärt, wann der Kurs beginnt und der Zug ankommt.", "You check when the course starts and the train arrives."),
        "can_do": ("Ты сможешь сообщить время действия с отделяемым глаголом.", "Du kannst eine Zeit mit einem trennbaren Verb nennen.", "You can give an action time using a separable verb."),
        "task": ("Скажи, когда начинается событие и когда ты прибываешь.", "Sage, wann etwas anfängt und wann du ankommst.", "Say when an event starts and when you arrive."),
        "alternate": "Der Zug kommt um acht Uhr an.",
        "turns": [
            ("Wann fängt der Kurs an?", ("Назови время начала.", "Nenne die Anfangszeit.", "Give the start time."), "Der Kurs fängt um … an.", "Der Kurs fängt um neun Uhr an."),
            ("Und wann kommst du an?", ("Назови время прибытия.", "Nenne deine Ankunftszeit.", "Give your arrival time."), "Ich komme um … an.", "Ich komme um Viertel vor neun an."),
        ],
    },
    "time_daily_routine": {
        "module_title": ("В городе", "Unterwegs", "Out and about"),
        "title": ("Опиши свой день", "Beschreibe deinen Tag", "Describe your day"),
        "scenario": ("Новый коллега спрашивает о твоём обычном рабочем дне.", "Ein neuer Kollege fragt nach deinem normalen Arbeitstag.", "A new colleague asks about your usual workday."),
        "can_do": ("Ты сможешь назвать время двух ежедневных действий.", "Du kannst die Zeit von zwei täglichen Handlungen nennen.", "You can give the time of two daily activities."),
        "task": ("Расскажи, когда ты встаёшь и начинаешь работу или учёбу.", "Erzähle, wann du aufstehst und mit der Arbeit oder dem Lernen beginnst.", "Say when you get up and start work or study."),
        "alternate": "Um sieben Uhr stehe ich auf, und um neun Uhr arbeite ich.",
        "turns": [
            ("Wann stehst du normalerweise auf?", ("Назови время.", "Nenne eine Uhrzeit.", "Give a time."), "Um … stehe ich auf.", "Um sieben Uhr stehe ich auf."),
            ("Wann beginnt dein Arbeitstag?", ("Назови второе время и действие.", "Nenne eine zweite Zeit und Handlung.", "Give a second time and activity."), "Um … arbeite/lerne ich.", "Um neun Uhr arbeite ich."),
        ],
    },
    "directions": {
        "module_title": ("В городе", "Unterwegs", "Out and about"),
        "title": ("Найди дорогу", "Finde den Weg", "Find your way"),
        "scenario": ("В незнакомом городе ты ищешь вокзал и остановку.", "In einer fremden Stadt suchst du den Bahnhof und eine Haltestelle.", "In an unfamiliar city, you are looking for the station and a stop."),
        "can_do": ("Ты сможешь вежливо спросить дорогу и уточнить направление.", "Du kannst höflich nach dem Weg fragen und die Richtung klären.", "You can politely ask for directions and clarify the route."),
        "task": ("Спроси дорогу к вокзалу и уточни, где остановка.", "Frage nach dem Weg zum Bahnhof und wo die Haltestelle ist.", "Ask the way to the station and where the stop is."),
        "alternate": "Entschuldigung, wie komme ich zum Bahnhof?",
        "checkpoint": True,
        "turns": [
            ("Guten Tag. Kann ich Ihnen helfen?", ("Вежливо спроси дорогу к вокзалу.", "Frage höflich nach dem Weg zum Bahnhof.", "Politely ask the way to the station."), "Entschuldigung, wie komme ich …?", "Entschuldigung, wie komme ich zum Bahnhof?"),
            ("Gehen Sie geradeaus und dann links.", ("Уточни, где находится остановка.", "Frage, wo die Haltestelle ist.", "Ask where the stop is."), "Wo ist …?", "Danke. Und wo ist die Bushaltestelle?"),
            ("Direkt vor dem Bahnhof.", ("Поблагодари и подтверди.", "Bedanke dich und bestätige.", "Thank the person and confirm."), "Danke …", "Vielen Dank für Ihre Hilfe!"),
        ],
    },
    "shopping": {
        "module_title": ("Самостоятельность", "Selbstständig im Alltag", "Independent everyday life"),
        "title": ("Купи продукты", "Kaufe Lebensmittel", "Buy groceries"),
        "scenario": ("На рынке ты покупаешь фрукты и хлеб.", "Auf dem Markt kaufst du Obst und Brot.", "At a market, you buy fruit and bread."),
        "can_do": ("Ты сможешь попросить нужное количество и узнать цену.", "Du kannst eine Menge bestellen und nach dem Preis fragen.", "You can ask for an amount and its price."),
        "task": ("Закажи два продукта и спроси общую цену.", "Bestelle zwei Produkte und frage nach dem Gesamtpreis.", "Order two products and ask for the total price."),
        "alternate": "Ich hätte gern ein Kilo Äpfel und zwei Brötchen.",
        "turns": [
            ("Guten Tag! Was darf es sein?", ("Закажи продукт и количество.", "Bestelle ein Produkt mit Menge.", "Order a product and amount."), "Ich hätte gern …", "Ich hätte gern ein Kilo Äpfel."),
            ("Gern. Sonst noch etwas?", ("Добавь второй продукт и спроси цену.", "Füge ein zweites Produkt hinzu und frage nach dem Preis.", "Add a second product and ask the price."), "… und … Was kostet das?", "Zwei Brötchen, bitte. Was kostet das zusammen?"),
        ],
    },
    "appointments": {
        "module_title": ("Самостоятельность", "Selbstständig im Alltag", "Independent everyday life"),
        "title": ("Подтверди запись", "Bestätige einen Termin", "Confirm an appointment"),
        "scenario": ("Ты подтверждаешь запись к врачу по телефону.", "Du bestätigst telefonisch einen Arzttermin.", "You confirm a medical appointment by phone."),
        "can_do": ("Ты сможешь назвать день и точное время встречи.", "Du kannst den Tag und die genaue Uhrzeit eines Termins nennen.", "You can give the day and exact time of an appointment."),
        "task": ("Подтверди день и время записи, затем повтори их.", "Bestätige Tag und Uhrzeit des Termins und wiederhole sie.", "Confirm the appointment day and time, then repeat them."),
        "alternate": "Wir treffen uns am Dienstag um elf Uhr.",
        "turns": [
            ("Ihr Termin ist am Montag. Passt das?", ("Подтверди день.", "Bestätige den Tag.", "Confirm the day."), "Ja, am …", "Ja, am Montag passt es."),
            ("Gut. Wir erwarten Sie um zehn Uhr.", ("Повтори день и время.", "Wiederhole Tag und Uhrzeit.", "Repeat the day and time."), "Also am … um …", "Danke, also am Montag um zehn Uhr."),
        ],
    },
    "family": {
        "module_title": ("Самостоятельность", "Selbstständig im Alltag", "Independent everyday life"),
        "title": ("Расскажи о семье", "Erzähle von deiner Familie", "Talk about your family"),
        "scenario": ("Знакомый спрашивает, кто живёт рядом с тобой.", "Eine Bekannte fragt, wer in deiner Nähe wohnt.", "An acquaintance asks who lives near you."),
        "can_do": ("Ты сможешь коротко рассказать о двух родственниках.", "Du kannst kurz von zwei Familienmitgliedern erzählen.", "You can briefly describe two family members."),
        "task": ("Расскажи о двух родственниках и где они живут.", "Erzähle von zwei Familienmitgliedern und wo sie wohnen.", "Talk about two relatives and where they live."),
        "alternate": "Meine Schwester wohnt in Köln, und mein Bruder lebt in Bonn.",
        "turns": [
            ("Hast du Geschwister?", ("Расскажи об одном родственнике.", "Erzähle von einem Familienmitglied.", "Talk about one relative."), "Mein/Meine …", "Ja, meine Schwester wohnt in Köln."),
            ("Und wo lebt dein Bruder?", ("Расскажи о втором родственнике.", "Erzähle von einem zweiten Familienmitglied.", "Talk about a second relative."), "Mein Bruder …", "Mein Bruder lebt mit seiner Familie in Bonn."),
        ],
    },
    "simple_past_experience": {
        "module_title": ("Самостоятельность", "Selbstständig im Alltag", "Independent everyday life"),
        "title": ("Расскажи о вчерашнем дне", "Erzähle von gestern", "Talk about yesterday"),
        "scenario": ("Коллега спрашивает, почему вчера тебя не было.", "Eine Kollegin fragt, warum du gestern nicht da warst.", "A colleague asks why you were absent yesterday."),
        "can_do": ("Ты сможешь назвать два завершённых действия.", "Du kannst zwei abgeschlossene Handlungen nennen.", "You can name two completed activities."),
        "task": ("Расскажи двумя фразами, что ты делал вчера.", "Erzähle in zwei Sätzen, was du gestern gemacht hast.", "Use two sentences to say what you did yesterday."),
        "alternate": "Gestern habe ich gearbeitet und danach meine Freundin besucht.",
        "turns": [
            ("Was hast du gestern gemacht?", ("Назови первое действие в Perfekt.", "Nenne die erste Handlung im Perfekt.", "Give the first activity in the perfect tense."), "Gestern habe/bin ich …", "Gestern habe ich lange gearbeitet."),
            ("Und was hast du danach gemacht?", ("Назови второе действие.", "Nenne eine zweite Handlung.", "Give a second activity."), "Danach habe/bin ich …", "Danach habe ich meine Freundin besucht."),
        ],
    },
    "a1_final": {
        "module_title": ("Самостоятельность", "Selbstständig im Alltag", "Independent everyday life"),
        "title": ("Проведи настоящий разговор", "Führe ein echtes Gespräch", "Have a real conversation"),
        "scenario": ("Ты знакомишься с новой группой и договариваешься о встрече.", "Du lernst eine neue Gruppe kennen und verabredest dich.", "You meet a new group and arrange to meet."),
        "can_do": ("Ты сможешь представиться, рассказать о себе и задать вопрос без подсказки.", "Du kannst dich vorstellen, von dir erzählen und ohne Hilfe eine Frage stellen.", "You can introduce yourself, talk about yourself, and ask a question without help."),
        "task": ("Представься, назови город и занятие, затем задай собеседнику вопрос.", "Stelle dich vor, nenne deinen Wohnort und deine Tätigkeit und stelle dann eine Frage.", "Introduce yourself, give your city and activity, then ask the other person a question."),
        "alternate": "Ich heiße Lina, wohne in Bremen und lerne jeden Tag Deutsch. Wo wohnst du?",
        "checkpoint": True,
        "turns": [
            ("Hallo! Wir kennen uns noch nicht. Erzähl kurz von dir.", ("Назови имя и город.", "Nenne deinen Namen und Wohnort.", "Give your name and city."), "Ich heiße … und wohne in …", "Ich heiße Lina und wohne in Bremen."),
            ("Was machst du normalerweise am Abend?", ("Расскажи об одном регулярном действии.", "Erzähle von einer regelmäßigen Handlung.", "Describe one regular activity."), "Am Abend … ich …", "Am Abend lerne ich Deutsch."),
            ("Hast du noch eine Frage an mich?", ("Задай самостоятельный вопрос.", "Stelle selbstständig eine Frage.", "Ask an independent question."), "Wo/Wann/Was …?", "Wo wohnst du?"),
        ],
    },
}


# A2 keeps the same short daily loop as A1, but asks the learner to connect
# ideas, narrate events, and resolve everyday problems. Each module is one
# practical story arc and closes with an unaided transfer conversation.
A2_MISSION_BLUEPRINTS = {
    "dative_a2": {
        "module_title": ("Люди и вещи", "Menschen und Dinge", "People and things"),
        "title": ("Передай нужную вещь", "Gib die richtige Sache weiter", "Pass on the right item"),
        "scenario": ("Коллега просит передать документы другому человеку.", "Eine Kollegin bittet dich, Unterlagen an eine andere Person weiterzugeben.", "A colleague asks you to pass documents to another person."),
        "can_do": ("Ты сможешь сказать, кому передаёшь вещь.", "Du kannst sagen, wem du etwas gibst.", "You can say who you are giving something to."),
        "task": ("Скажи, кому и что ты передаёшь.", "Sage, wem du was gibst.", "Say what you are giving and to whom."),
        "alternate": "Ich bringe meinem Nachbarn ein Paket.",
        "turns": [
            ("Kannst du Frau Berger diese Mappe geben?", ("Подтверди и назови получателя.", "Bestätige und nenne die Empfängerin.", "Confirm and name the recipient."), "Ja, ich gebe …", "Ja, ich gebe Frau Berger die Mappe."),
            ("Und wem gibst du den Schlüssel?", ("Назови второго получателя.", "Nenne den zweiten Empfänger.", "Name the second recipient."), "Ich gebe …", "Ich gebe meinem Kollegen den Schlüssel."),
        ],
    },
    "dative_accusative": {
        "module_title": ("Люди и вещи", "Menschen und Dinge", "People and things"),
        "title": ("Объясни, кто что получает", "Erkläre, wer was bekommt", "Explain who receives what"),
        "scenario": ("Ты распределяешь материалы перед встречей.", "Du verteilst vor einer Besprechung die Materialien.", "You distribute materials before a meeting."),
        "can_do": ("Ты сможешь различать человека и предмет в одной фразе.", "Du kannst Person und Sache in einem Satz unterscheiden.", "You can distinguish the person and item in one sentence."),
        "task": ("Распредели два предмета между двумя людьми.", "Verteile zwei Dinge an zwei Personen.", "Distribute two items between two people."),
        "alternate": "Ich zeige meiner Kollegin den Plan.",
        "turns": [
            ("Wer bekommt den Plan?", ("Назови человека в Dativ.", "Nenne die Person im Dativ.", "Name the person in the dative."), "Ich gebe … den Plan.", "Ich gebe meiner Kollegin den Plan."),
            ("Und was gibst du dem neuen Mitarbeiter?", ("Назови предмет в Akkusativ.", "Nenne die Sache im Akkusativ.", "Name the item in the accusative."), "Dem Mitarbeiter gebe ich …", "Dem neuen Mitarbeiter gebe ich die Zugangskarte."),
        ],
    },
    "two_way_prepositions": {
        "module_title": ("Люди и вещи", "Menschen und Dinge", "People and things"),
        "title": ("Расставь вещи в комнате", "Richte den Raum ein", "Arrange the room"),
        "scenario": ("Перед встречей вы готовите комнату.", "Vor einem Treffen bereitet ihr den Raum vor.", "You prepare a room before a meeting."),
        "can_do": ("Ты сможешь сказать, где предмет находится и куда его поставить.", "Du kannst sagen, wo etwas ist und wohin es gestellt wird.", "You can say where something is and where to put it."),
        "task": ("Опиши положение одного предмета и перемещение другого.", "Beschreibe den Ort eines Gegenstands und die Bewegung eines anderen.", "Describe one item's location and move another item."),
        "alternate": "Die Tasche liegt auf dem Stuhl, und ich stelle die Vase auf den Tisch.",
        "turns": [
            ("Wo liegt die Tasche?", ("Ответь на wo с Dativ.", "Antworte auf wo mit Dativ.", "Answer wo using the dative."), "Sie liegt auf …", "Sie liegt auf dem Stuhl."),
            ("Wohin stellst du die Vase?", ("Ответь на wohin с Akkusativ.", "Antworte auf wohin mit Akkusativ.", "Answer wohin using the accusative."), "Ich stelle sie auf …", "Ich stelle sie auf den Tisch."),
        ],
    },
    "dative_prepositions": {
        "module_title": ("Люди и вещи", "Menschen und Dinge", "People and things"),
        "title": ("Расскажи о жизни здесь", "Erzähle von deinem Leben hier", "Talk about your life here"),
        "scenario": ("Новый знакомый спрашивает, как давно и с кем ты живёшь в городе.", "Eine neue Bekanntschaft fragt, seit wann und mit wem du in der Stadt lebst.", "A new acquaintance asks how long and with whom you have lived in the city."),
        "can_do": ("Ты сможешь использовать mit, bei и seit в личном рассказе.", "Du kannst mit, bei und seit in einem persönlichen Gespräch verwenden.", "You can use mit, bei, and seit in a personal conversation."),
        "task": ("Скажи, с кем ты живёшь и как давно ты здесь.", "Sage, mit wem du wohnst und seit wann du hier bist.", "Say who you live with and how long you have been here."),
        "alternate": "Ich wohne seit einem Jahr bei meiner Tante.",
        "turns": [
            ("Seit wann wohnst du hier?", ("Ответь с seit.", "Antworte mit seit.", "Answer using seit."), "Seit …", "Ich wohne seit einem Jahr hier."),
            ("Wohnst du allein?", ("Ответь с mit или bei.", "Antworte mit mit oder bei.", "Answer using mit or bei."), "Ich wohne mit/bei …", "Nein, ich wohne mit meiner Schwester."),
        ],
    },
    "accusative_prepositions": {
        "module_title": ("Люди и вещи", "Menschen und Dinge", "People and things"),
        "title": ("Подготовь всё к встрече", "Bereite alles für das Treffen vor", "Prepare everything for the meeting"),
        "scenario": ("Ты объясняешь, для кого покупки и без чего встреча не состоится.", "Du erklärst, für wen die Einkäufe sind und ohne was das Treffen nicht stattfinden kann.", "You explain who the purchases are for and what the meeting cannot happen without."),
        "can_do": ("Ты сможешь использовать für и ohne в реальной ситуации.", "Du kannst für und ohne in einer echten Situation verwenden.", "You can use für and ohne in a real situation."),
        "task": ("Скажи, для кого одна вещь и без чего нельзя начать.", "Sage, für wen eine Sache ist und ohne was ihr nicht beginnen könnt.", "Say who one item is for and what you cannot start without."),
        "alternate": "Die Blumen sind für meine Kollegin, und ohne den Schlüssel kommen wir nicht hinein.",
        "checkpoint": True,
        "turns": [
            ("Für wen sind die Blumen?", ("Ответь с für.", "Antworte mit für.", "Answer using für."), "Sie sind für …", "Sie sind für meine Kollegin."),
            ("Können wir ohne den Schlüssel anfangen?", ("Ответь с ohne.", "Antworte mit ohne.", "Answer using ohne."), "Ohne … können wir nicht …", "Nein, ohne den Schlüssel können wir nicht anfangen."),
            ("Was gibst du Herrn Klein?", ("Соедини человека и предмет самостоятельно.", "Verbinde Person und Sache selbstständig.", "Connect a person and item independently."), "Ich gebe …", "Ich gebe Herrn Klein die Unterlagen."),
        ],
    },
    "perfect_haben": {
        "module_title": ("Что произошло", "Was passiert ist", "What happened"),
        "title": ("Расскажи о вчерашнем вечере", "Erzähle von gestern Abend", "Talk about yesterday evening"),
        "scenario": ("Друг спрашивает, почему ты вчера не ответил.", "Ein Freund fragt, warum du gestern nicht geantwortet hast.", "A friend asks why you did not reply yesterday."),
        "can_do": ("Ты сможешь назвать завершённые действия с haben.", "Du kannst abgeschlossene Handlungen mit haben nennen.", "You can describe completed actions with haben."),
        "task": ("Назови два действия, которые ты сделал вчера.", "Nenne zwei Dinge, die du gestern gemacht hast.", "Name two things you did yesterday."),
        "alternate": "Gestern habe ich lange gearbeitet und danach telefoniert.",
        "turns": [
            ("Was hast du gestern Abend gemacht?", ("Назови действие в Perfekt.", "Nenne eine Handlung im Perfekt.", "Give one action in the perfect tense."), "Ich habe …", "Ich habe lange gearbeitet."),
            ("Hast du meine Nachricht gelesen?", ("Ответь ещё одной формой с haben.", "Antworte mit einer weiteren haben-Form.", "Answer with another haben form."), "Ja/Nein, ich habe …", "Ja, ich habe deine Nachricht später gelesen."),
        ],
    },
    "perfect_sein": {
        "module_title": ("Что произошло", "Was passiert ist", "What happened"),
        "title": ("Расскажи о поездке", "Erzähle von einer Fahrt", "Talk about a trip"),
        "scenario": ("Вы обсуждаете поездку на выходных.", "Ihr sprecht über eine Fahrt am Wochenende.", "You talk about a weekend trip."),
        "can_do": ("Ты сможешь рассказать о движении и перемене с sein.", "Du kannst Bewegung und Veränderung mit sein beschreiben.", "You can describe movement and change using sein."),
        "task": ("Скажи, куда ты ездил и когда вернулся.", "Sage, wohin du gefahren und wann du zurückgekommen bist.", "Say where you went and when you returned."),
        "alternate": "Am Samstag bin ich nach Bremen gefahren und am Abend zurückgekommen.",
        "turns": [
            ("Wohin bist du am Wochenende gefahren?", ("Назови направление с sein.", "Nenne ein Ziel mit sein.", "Give a destination using sein."), "Ich bin nach … gefahren.", "Ich bin nach Bremen gefahren."),
            ("Wann bist du zurückgekommen?", ("Назови время возвращения.", "Nenne die Rückkehrzeit.", "Give the return time."), "Ich bin … zurückgekommen.", "Ich bin am Sonntagabend zurückgekommen."),
        ],
    },
    "perfect_participles": {
        "module_title": ("Что произошло", "Was passiert ist", "What happened"),
        "title": ("Отчитайся о сделанном", "Berichte, was erledigt ist", "Report what is done"),
        "scenario": ("Перед окончанием рабочего дня коллега уточняет, что уже готово.", "Vor Feierabend fragt eine Kollegin, was schon erledigt ist.", "Before the workday ends, a colleague asks what is finished."),
        "can_do": ("Ты сможешь перечислить несколько завершённых дел.", "Du kannst mehrere erledigte Aufgaben nennen.", "You can list several completed tasks."),
        "task": ("Назови два завершённых дела и одно ещё незавершённое.", "Nenne zwei erledigte Aufgaben und eine offene Aufgabe.", "Name two completed tasks and one unfinished task."),
        "alternate": "Ich habe die E-Mail geschrieben und die Unterlagen abgeschickt, aber noch nicht angerufen.",
        "turns": [
            ("Was hast du schon erledigt?", ("Назови два Partizip II.", "Nenne zwei Partizip-II-Formen.", "Use two past participles."), "Ich habe … und …", "Ich habe die E-Mail geschrieben und die Unterlagen abgeschickt."),
            ("Was ist noch offen?", ("Скажи, что ещё не сделано.", "Sage, was noch nicht gemacht ist.", "Say what is not done yet."), "Ich habe noch nicht …", "Ich habe den Kunden noch nicht angerufen."),
        ],
    },
    "modal_past_a2": {
        "module_title": ("Что произошло", "Was passiert ist", "What happened"),
        "title": ("Объясни прошлые обязанности", "Erkläre frühere Pflichten", "Explain past obligations"),
        "scenario": ("Вы сравниваете прошлый рабочий день с сегодняшним.", "Ihr vergleicht den gestrigen Arbeitstag mit heute.", "You compare yesterday's workday with today."),
        "can_do": ("Ты сможешь сказать, что должен, мог или не мог сделать.", "Du kannst sagen, was du tun musstest, konntest oder nicht konntest.", "You can say what you had to, could, or could not do."),
        "task": ("Скажи, что ты должен был сделать и чего не смог.", "Sage, was du tun musstest und was du nicht konntest.", "Say what you had to do and what you could not do."),
        "alternate": "Ich musste länger arbeiten und konnte deshalb nicht kommen.",
        "turns": [
            ("Warum warst du gestern so lange im Büro?", ("Ответь с musste.", "Antworte mit musste.", "Answer using musste."), "Ich musste …", "Ich musste einen Bericht fertigstellen."),
            ("Konntest du danach noch einkaufen?", ("Ответь с konnte.", "Antworte mit konnte.", "Answer using konnte."), "Ich konnte …", "Nein, ich konnte danach nicht mehr einkaufen."),
        ],
    },
    "past_sequence": {
        "module_title": ("Что произошло", "Was passiert ist", "What happened"),
        "title": ("Расскажи историю по порядку", "Erzähle eine Geschichte der Reihe nach", "Tell a story in order"),
        "scenario": ("Ты объясняешь, почему опоздал на важную встречу.", "Du erklärst, warum du zu einem wichtigen Termin zu spät gekommen bist.", "You explain why you were late for an important appointment."),
        "can_do": ("Ты сможешь связать несколько событий в понятную историю.", "Du kannst mehrere Ereignisse zu einer klaren Geschichte verbinden.", "You can connect several events into a clear story."),
        "task": ("Расскажи три события по порядку и объясни опоздание.", "Erzähle drei Ereignisse der Reihe nach und erkläre die Verspätung.", "Tell three events in order and explain why you were late."),
        "alternate": "Zuerst ist der Bus nicht gekommen, dann habe ich ein Taxi gerufen, und danach bin ich losgefahren.",
        "checkpoint": True,
        "turns": [
            ("Warum bist du zu spät gekommen?", ("Начни историю с zuerst.", "Beginne die Geschichte mit zuerst.", "Begin the story with zuerst."), "Zuerst …", "Zuerst ist der Bus nicht gekommen."),
            ("Was hast du dann gemacht?", ("Продолжи с dann.", "Fahre mit dann fort.", "Continue using dann."), "Dann habe/bin ich …", "Dann habe ich ein Taxi gerufen."),
            ("Und was ist danach passiert?", ("Заверши историю с danach.", "Beende die Geschichte mit danach.", "Finish the story using danach."), "Danach …", "Danach bin ich zur Arbeit gefahren."),
        ],
    },
    "weil_clause": {
        "module_title": ("Решения и причины", "Entscheidungen und Gründe", "Decisions and reasons"),
        "title": ("Объясни своё решение", "Begründe deine Entscheidung", "Explain your decision"),
        "scenario": ("Друг спрашивает, почему ты изменил план.", "Ein Freund fragt, warum du deinen Plan geändert hast.", "A friend asks why you changed your plan."),
        "can_do": ("Ты сможешь назвать решение и причину с weil.", "Du kannst eine Entscheidung mit weil begründen.", "You can explain a decision using weil."),
        "task": ("Скажи, что ты решил и почему.", "Sage, was du entschieden hast und warum.", "Say what you decided and why."),
        "alternate": "Ich fahre mit dem Bus, weil es stark regnet.",
        "turns": [
            ("Warum kommst du heute nicht mit dem Fahrrad?", ("Ответь с weil; глагол в конце.", "Antworte mit weil; das Verb steht am Ende.", "Answer using weil with the verb at the end."), "…, weil …", "Ich fahre mit dem Bus, weil es regnet."),
            ("Warum gehst du früher nach Hause?", ("Назови вторую причину.", "Nenne einen zweiten Grund.", "Give a second reason."), "Ich gehe …, weil …", "Ich gehe früher, weil ich einen Termin habe."),
        ],
    },
    "dass_clause": {
        "module_title": ("Решения и причины", "Entscheidungen und Gründe", "Decisions and reasons"),
        "title": ("Передай важную информацию", "Gib wichtige Informationen weiter", "Pass on important information"),
        "scenario": ("Ты сообщаешь коллеге изменения в расписании.", "Du informierst eine Kollegin über Änderungen im Zeitplan.", "You tell a colleague about changes to the schedule."),
        "can_do": ("Ты сможешь передать мнение или информацию с dass.", "Du kannst eine Meinung oder Information mit dass weitergeben.", "You can report an opinion or information using dass."),
        "task": ("Передай две важные новости с dass.", "Gib zwei wichtige Informationen mit dass weiter.", "Pass on two important pieces of information using dass."),
        "alternate": "Ich glaube, dass die Besprechung später beginnt.",
        "turns": [
            ("Was hat Frau Weber über den Termin gesagt?", ("Передай информацию с dass.", "Gib die Information mit dass weiter.", "Report the information using dass."), "Sie hat gesagt, dass …", "Sie hat gesagt, dass der Termin später beginnt."),
            ("Und was denkst du über den neuen Plan?", ("Назови мнение с dass.", "Nenne deine Meinung mit dass.", "Give your opinion using dass."), "Ich denke, dass …", "Ich denke, dass der neue Plan besser ist."),
        ],
    },
    "wenn_clause": {
        "module_title": ("Решения и причины", "Entscheidungen und Gründe", "Decisions and reasons"),
        "title": ("Договорись при условии", "Vereinbare etwas mit einer Bedingung", "Make a conditional arrangement"),
        "scenario": ("Вы планируете выходные, но всё зависит от погоды и времени.", "Ihr plant das Wochenende, aber alles hängt vom Wetter und von der Zeit ab.", "You plan the weekend, but everything depends on weather and time."),
        "can_do": ("Ты сможешь согласовать план с условием wenn.", "Du kannst einen Plan mit einer wenn-Bedingung vereinbaren.", "You can agree on a plan with a wenn condition."),
        "task": ("Предложи два плана с разными условиями.", "Schlage zwei Pläne mit unterschiedlichen Bedingungen vor.", "Suggest two plans with different conditions."),
        "alternate": "Wenn das Wetter gut ist, gehen wir an die Elbe.",
        "turns": [
            ("Was machen wir, wenn das Wetter gut ist?", ("Предложи план с wenn.", "Schlage einen Plan mit wenn vor.", "Suggest a plan using wenn."), "Wenn …, …", "Wenn das Wetter gut ist, gehen wir spazieren."),
            ("Und wenn es regnet?", ("Предложи запасной вариант.", "Schlage eine Alternative vor.", "Suggest a backup plan."), "Wenn es regnet, …", "Wenn es regnet, besuchen wir ein Museum."),
        ],
    },
    "comparatives": {
        "module_title": ("Решения и причины", "Entscheidungen und Gründe", "Decisions and reasons"),
        "title": ("Сравни два варианта", "Vergleiche zwei Möglichkeiten", "Compare two options"),
        "scenario": ("Вы выбираете транспорт для поездки.", "Ihr wählt ein Verkehrsmittel für eine Reise.", "You choose transport for a trip."),
        "can_do": ("Ты сможешь сравнить варианты и выбрать лучший.", "Du kannst Möglichkeiten vergleichen und die beste wählen.", "You can compare options and choose the best one."),
        "task": ("Сравни поезд и автобус по двум критериям и выбери один.", "Vergleiche Zug und Bus nach zwei Kriterien und entscheide dich.", "Compare train and bus using two criteria and choose one."),
        "alternate": "Der Zug ist schneller, aber der Bus ist günstiger. Ich nehme den Zug.",
        "turns": [
            ("Ist der Zug besser als der Bus?", ("Сравни скорость или удобство.", "Vergleiche Geschwindigkeit oder Komfort.", "Compare speed or comfort."), "Der Zug ist … als …", "Der Zug ist schneller als der Bus."),
            ("Welche Verbindung nimmst du?", ("Выбери и коротко обоснуй.", "Entscheide dich und begründe kurz.", "Choose and give a short reason."), "Ich nehme …, weil …", "Ich nehme den Zug, weil er bequemer ist."),
        ],
    },
    "reflexive_verbs": {
        "module_title": ("Решения и причины", "Entscheidungen und Gründe", "Decisions and reasons"),
        "title": ("Обсуди интересы и планы", "Sprich über Interessen und Pläne", "Discuss interests and plans"),
        "scenario": ("Вы знакомитесь в группе и выбираете совместное занятие.", "Ihr lernt euch in einer Gruppe kennen und wählt eine gemeinsame Aktivität.", "You meet in a group and choose an activity together."),
        "can_do": ("Ты сможешь говорить об интересах, встречах и договорённостях.", "Du kannst über Interessen, Treffen und Verabredungen sprechen.", "You can talk about interests, meetings, and arrangements."),
        "task": ("Расскажи, чем ты интересуешься, и договорись о встрече.", "Erzähle, wofür du dich interessierst, und verabrede dich.", "Say what interests you and arrange to meet."),
        "alternate": "Ich interessiere mich für Fotografie. Treffen wir uns am Samstag?",
        "checkpoint": True,
        "turns": [
            ("Wofür interessierst du dich?", ("Ответь с sich interessieren.", "Antworte mit sich interessieren.", "Answer using sich interessieren."), "Ich interessiere mich für …", "Ich interessiere mich für moderne Kunst."),
            ("Möchtest du gemeinsam eine Ausstellung besuchen?", ("Ответь и предложи время.", "Antworte und schlage eine Zeit vor.", "Answer and suggest a time."), "Ja, wir können uns … treffen.", "Ja, wir können uns am Samstag treffen."),
            ("Warum passt dir dieser Tag?", ("Объясни причину с weil.", "Begründe mit weil.", "Explain using weil."), "…, weil …", "Der Samstag passt mir, weil ich nicht arbeiten muss."),
        ],
    },
    "requests_a2": {
        "module_title": ("Решение проблем", "Probleme lösen", "Solving problems"),
        "title": ("Попроси о помощи вежливо", "Bitte höflich um Hilfe", "Ask for help politely"),
        "scenario": ("В учреждении тебе нужна помощь с формуляром.", "In einer Behörde brauchst du Hilfe mit einem Formular.", "At a public office, you need help with a form."),
        "can_do": ("Ты сможешь вежливо объяснить просьбу.", "Du kannst eine Bitte höflich formulieren.", "You can make a polite request."),
        "task": ("Поздоровайся, сформулируй просьбу и уточни следующий шаг.", "Begrüße die Person, formuliere deine Bitte und frage nach dem nächsten Schritt.", "Greet the person, make your request, and ask about the next step."),
        "alternate": "Entschuldigung, könnten Sie mir bitte mit diesem Formular helfen?",
        "turns": [
            ("Guten Tag. Was kann ich für Sie tun?", ("Сформулируй вежливую просьбу.", "Formuliere eine höfliche Bitte.", "Make a polite request."), "Könnten Sie mir bitte …?", "Könnten Sie mir bitte mit diesem Formular helfen?"),
            ("Natürlich. Haben Sie Ihren Ausweis dabei?", ("Ответь и уточни следующий шаг.", "Antworte und frage nach dem nächsten Schritt.", "Answer and ask about the next step."), "Ja. Was muss ich …?", "Ja. Was muss ich danach machen?"),
        ],
    },
    "formal_message_a2": {
        "module_title": ("Решение проблем", "Probleme lösen", "Solving problems"),
        "title": ("Перенеси встречу письменно", "Verschiebe einen Termin schriftlich", "Reschedule an appointment in writing"),
        "scenario": ("Ты не можешь прийти к врачу и пишешь короткое сообщение.", "Du kannst nicht zum Arzttermin kommen und schreibst eine kurze Nachricht.", "You cannot attend a medical appointment and write a short message."),
        "can_do": ("Ты сможешь написать понятное официальное сообщение.", "Du kannst eine klare formelle Nachricht schreiben.", "You can write a clear formal message."),
        "task": ("Напиши обращение, причину, просьбу о новой дате и прощание.", "Schreibe Anrede, Grund, Bitte um einen neuen Termin und Gruß.", "Write a greeting, reason, request for a new date, and closing."),
        "alternate": "Sehr geehrte Frau Klein, leider kann ich morgen nicht kommen. Könnten Sie mir bitte einen neuen Termin geben? Mit freundlichen Grüßen",
        "turns": [
            ("Schreiben Sie zuerst, warum Sie sich melden.", ("Начни официально и назови проблему.", "Beginne formell und nenne das Problem.", "Start formally and state the problem."), "Sehr geehrte …, leider …", "Sehr geehrte Frau Klein, leider kann ich morgen nicht kommen."),
            ("Welche Lösung möchten Sie?", ("Вежливо попроси новую дату.", "Bitte höflich um einen neuen Termin.", "Politely request a new date."), "Könnten Sie …?", "Könnten Sie mir bitte einen neuen Termin geben?"),
        ],
    },
    "opinions_a2": {
        "module_title": ("Решение проблем", "Probleme lösen", "Solving problems"),
        "title": ("Выскажи мнение с причиной", "Äußere eine begründete Meinung", "Give a reasoned opinion"),
        "scenario": ("На курсе обсуждают, лучше учиться онлайн или очно.", "Im Kurs diskutiert ihr, ob Online- oder Präsenzunterricht besser ist.", "In class, you discuss whether online or in-person learning is better."),
        "can_do": ("Ты сможешь высказать мнение и привести причину.", "Du kannst deine Meinung äußern und begründen.", "You can state and support an opinion."),
        "task": ("Выбери формат обучения, назови преимущество и недостаток.", "Wähle eine Lernform und nenne einen Vorteil und einen Nachteil.", "Choose a learning format and give one advantage and disadvantage."),
        "alternate": "Ich finde Präsenzunterricht besser, weil man direkt fragen kann. Online ist aber flexibler.",
        "turns": [
            ("Lernst du lieber online oder im Kurs?", ("Назови мнение.", "Nenne deine Meinung.", "State your opinion."), "Ich finde … besser.", "Ich finde Präsenzunterricht besser."),
            ("Warum? Gibt es auch einen Nachteil?", ("Назови причину и один минус.", "Nenne einen Grund und einen Nachteil.", "Give a reason and one drawback."), "…, weil … Aber …", "Weil ich direkt fragen kann. Aber der Weg zum Kurs dauert lange."),
        ],
    },
    "problem_solution_a2": {
        "module_title": ("Решение проблем", "Probleme lösen", "Solving problems"),
        "title": ("Реши проблему в сервисе", "Löse ein Problem beim Service", "Solve a service problem"),
        "scenario": ("Твой поезд отменён, и тебе нужна другая связь.", "Dein Zug fällt aus, und du brauchst eine andere Verbindung.", "Your train is cancelled and you need another connection."),
        "can_do": ("Ты сможешь объяснить проблему и попросить конкретное решение.", "Du kannst ein Problem erklären und um eine konkrete Lösung bitten.", "You can explain a problem and request a specific solution."),
        "task": ("Объясни отмену, назови цель поездки и попроси альтернативу.", "Erkläre den Ausfall, nenne dein Reiseziel und bitte um eine Alternative.", "Explain the cancellation, give your destination, and ask for an alternative."),
        "alternate": "Mein Zug nach Berlin fällt aus. Deshalb brauche ich eine andere Verbindung. Können Sie mir helfen?",
        "turns": [
            ("Guten Tag. Was ist passiert?", ("Коротко объясни проблему.", "Erkläre das Problem kurz.", "Briefly explain the problem."), "Mein Zug …", "Mein Zug nach Berlin fällt aus."),
            ("Was brauchen Sie jetzt?", ("Попроси конкретное решение.", "Bitte um eine konkrete Lösung.", "Ask for a specific solution."), "Deshalb brauche ich …", "Deshalb brauche ich eine andere Verbindung."),
        ],
    },
    "a2_final": {
        "module_title": ("Решение проблем", "Probleme lösen", "Solving problems"),
        "title": ("Справься с реальной ситуацией", "Bewältige eine echte Situation", "Handle a real-life situation"),
        "scenario": ("Ты опоздал на рабочую встречу, объясняешь прошлое и предлагаешь решение.", "Du kommst zu spät zu einem Arbeitstermin, erklärst, was passiert ist, und schlägst eine Lösung vor.", "You are late for a work meeting, explain what happened, and suggest a solution."),
        "can_do": ("Ты сможешь связно объяснить событие, причину и следующий шаг без подсказки.", "Du kannst ein Ereignis, einen Grund und den nächsten Schritt ohne Hilfe zusammenhängend erklären.", "You can clearly explain an event, reason, and next step without help."),
        "task": ("Извинись, расскажи, что произошло, объясни причину и предложи решение.", "Entschuldige dich, erzähle, was passiert ist, begründe es und schlage eine Lösung vor.", "Apologise, explain what happened and why, then suggest a solution."),
        "alternate": "Entschuldigung für die Verspätung. Mein Zug ist ausgefallen, deshalb musste ich auf den Bus warten. Können wir jetzt beginnen?",
        "checkpoint": True,
        "turns": [
            ("Sie kommen zwanzig Minuten zu spät. Was ist passiert?", ("Извинись и начни рассказ в Perfekt.", "Entschuldige dich und beginne im Perfekt.", "Apologise and begin in the perfect tense."), "Entschuldigung. … ist/hat …", "Entschuldigung. Mein Zug ist ausgefallen."),
            ("Warum haben Sie nicht angerufen?", ("Объясни причину с weil.", "Begründe mit weil.", "Explain using weil."), "…, weil …", "Ich konnte nicht anrufen, weil mein Akku leer war."),
            ("Wie lösen wir das jetzt?", ("Предложи конкретный следующий шаг.", "Schlage einen konkreten nächsten Schritt vor.", "Suggest a concrete next step."), "Könnten wir …?", "Könnten wir die wichtigsten Punkte jetzt besprechen?"),
        ],
    },
}


for _level, _curriculum, _blueprints in (
    ("A1", A1_CURRICULUM[5:], A1_MISSION_BLUEPRINTS),
    ("A2", A2_CURRICULUM, A2_MISSION_BLUEPRINTS),
):
  for _row in _curriculum:
    _day, _module, _topic, _pillar, _title_ru, _title_de, _title_en, _focus, _model, _wrong = _row
    _blueprint = _blueprints[_topic]
    _scenario = _blueprint["scenario"]
    _can_do = _blueprint["can_do"]
    _task = _blueprint["task"]
    _rule = (
        f"Используй модель «{_focus}» в своей фразе; личные детали можно менять.",
        f"Nutze das Muster „{_focus}“ in deinem eigenen Satz; persönliche Details dürfen anders sein.",
        f"Use the “{_focus}” pattern in your own sentence; personal details may be different.",
    )
    A1_FIRST_CONVERSATION[_topic] = {
        "module_title": _blueprint["module_title"],
        "title": _blueprint["title"],
        "scenario": _scenario,
        "can_do": _can_do,
        "rule": _rule,
        "model": _model,
        "alternate": _blueprint["alternate"],
        "wrong": _wrong,
        "choice": (
            f"Какая фраза подходит к ситуации: {_scenario[0]}",
            f"Welcher Satz passt zur Situation: {_scenario[1]}",
            f"Which sentence fits this situation: {_scenario[2]}",
        ),
        "listen_answer": (_can_do[0], _can_do[1], _can_do[2]),
        "listen_options": (
            (_can_do[0], "Человек меняет тему", "Это только приветствие"),
            (_can_do[1], "Die Person wechselt das Thema", "Das ist nur eine Begrüßung"),
            (_can_do[2], "The speaker changes the subject", "It is only a greeting"),
        ),
        "task": _task,
        "patterns": PRACTICE_VARIANTS[_topic][4][:3],
        "checkpoint": bool(_blueprint.get("checkpoint")),
    }
    A1_MISSION_DIALOGUES[_topic] = _blueprint["turns"]


def _mission_turns(topic: str, language_index: int) -> list[dict]:
    return [
        {
            "partner": partner,
            "goal": goals[language_index],
            "placeholder": placeholder,
            "model": model,
        }
        for partner, goals, placeholder, model in A1_MISSION_DIALOGUES[topic]
    ]


def _localized(base: dict, ru: dict, de: dict, en: dict) -> dict:
    return {**base, "i18n": {"ru": ru, "de": de, "en": en}}


def build_foundation_content(row: tuple, level: str) -> dict:
    day, module, topic, pillar, title_ru, title_de, title_en, focus, model, wrong = row
    starter = A1_FIRST_CONVERSATION.get(topic)
    if starter:
        exercise_prefix = level.lower()
        title_ru, title_de, title_en = starter["title"]
        module_title_ru, module_title_de, module_title_en = starter.get(
            "module_title",
            ("Первый разговор", "Das erste Gespräch", "Your first conversation"),
        )
        scenario_ru, scenario_de, scenario_en = starter["scenario"]
        can_do_ru, can_do_de, can_do_en = starter["can_do"]
        rule_ru, rule_de, rule_en = starter["rule"]
        model = starter["model"]
        wrong = starter["wrong"]
        choices = [model, wrong, "Danke, gleichfalls!"]
        listen_ru, listen_de, listen_en = starter["listen_answer"]
        options_ru, options_de, options_en = starter["listen_options"]
        task_ru, task_de, task_en = starter["task"]
        tokens = model.rstrip(".?!").split()
        mixed_tokens = tokens[1::2] + tokens[::2]
        mission_turns = {
            "ru": _mission_turns(topic, 0),
            "de": _mission_turns(topic, 1),
            "en": _mission_turns(topic, 2),
        }
        mission_model = "\n".join(turn["model"] for turn in mission_turns["ru"])
        exercises = [
            _localized(
                {"id":f"{exercise_prefix}-{day}-build","type":"reorder","stage":"guided","question":"Собери полезную фразу.","answer":model,"accepted_answers":[model,model.rstrip(".?!")],"tokens":mixed_tokens,"hint":rule_ru,"explanation":rule_ru,"misconception":"foundation_mission_form","accessibility_label":"Собери немецкую фразу"},
                {"question":"Собери полезную фразу.","hint":rule_ru,"explanation":rule_ru,"accessibility_label":"Собери немецкую фразу"},
                {"question":"Baue den nützlichen Satz.","hint":rule_de,"explanation":rule_de,"accessibility_label":"Deutschen Satz bauen"},
                {"question":"Build the useful sentence.","hint":rule_en,"explanation":rule_en,"accessibility_label":"Build the German sentence"},
            ),
            _localized(
                {"id":f"{exercise_prefix}-{day}-analogy","type":"analogy_choice","stage":"independent","question":starter["choice"][0],"answer":model,"accepted_answers":[model],"options":choices,"analogy_source":starter["alternate"],"analogy_target":scenario_ru,"pattern_label":"Та же структура — новая ситуация","explanation":rule_ru,"misconception":"foundation_mission_transfer","accessibility_label":"Перенеси знакомую структуру в новую ситуацию"},
                {"question":starter["choice"][0],"analogy_target":scenario_ru,"pattern_label":"Та же структура — новая ситуация","explanation":rule_ru,"accessibility_label":"Перенеси знакомую структуру в новую ситуацию"},
                {"question":starter["choice"][1],"analogy_target":scenario_de,"pattern_label":"Gleiches Muster – neue Situation","explanation":rule_de,"accessibility_label":"Bekanntes Muster auf eine neue Situation übertragen"},
                {"question":starter["choice"][2],"analogy_target":scenario_en,"pattern_label":"Same pattern — new situation","explanation":rule_en,"accessibility_label":"Transfer a familiar pattern to a new situation"},
            ),
            _localized(
                {"id":f"{exercise_prefix}-{day}-listen","type":"listening_choice","stage":"independent","question":"Послушай. Что делает говорящий?","answer":listen_ru,"accepted_answers":[listen_ru],"options":list(options_ru),"audio_text":model,"explanation":model,"misconception":"foundation_mission_listening","accessibility_label":"Послушай и выбери смысл"},
                {"question":"Послушай. Что делает говорящий?","answer":listen_ru,"accepted_answers":[listen_ru],"options":list(options_ru),"accessibility_label":"Послушай и выбери смысл"},
                {"question":"Höre zu. Was macht die sprechende Person?","answer":listen_de,"accepted_answers":[listen_de],"options":list(options_de),"accessibility_label":"Hören und Bedeutung wählen"},
                {"question":"Listen. What is the speaker doing?","answer":listen_en,"accepted_answers":[listen_en],"options":list(options_en),"accessibility_label":"Listen and choose the meaning"},
            ),
            _localized(
                {"id":f"{exercise_prefix}-{day}-use","type":"dialogue","stage":"transfer","mission_role":"final","question":task_ru,"answer":mission_model,"model_answer":mission_model,"accepted_answers":[mission_model,mission_model.rstrip(".?!")],"target_patterns":(["heiße","woher","wo"] if level == "A1" and day == 5 else starter["patterns"]),"hint":rule_ru,"explanation":"Смысл должен подходить ситуации. Личные данные могут отличаться.","misconception":"foundation_mission_transfer","accessibility_label":"Пройди реальный мини-диалог","conversation_turns":mission_turns["ru"]},
                {"question":task_ru,"hint":rule_ru,"explanation":"Смысл должен подходить ситуации. Личные данные могут отличаться.","accessibility_label":"Пройди реальный мини-диалог","conversation_turns":mission_turns["ru"]},
                {"question":task_de,"hint":rule_de,"explanation":"Die Antwort muss zur Situation passen. Persönliche Angaben dürfen anders sein.","accessibility_label":"Ein echtes Mini-Gespräch führen","conversation_turns":mission_turns["de"]},
                {"question":task_en,"hint":rule_en,"explanation":"The answer must fit the situation. Personal details may be different.","accessibility_label":"Complete a real mini dialogue","conversation_turns":mission_turns["en"]},
            ),
            _localized(
                {"id":f"{exercise_prefix}-{day}-speak","type":"repeat","stage":"transfer","question":"Скажи фразу вслух.","answer":starter["alternate"],"accepted_answers":[starter["alternate"],starter["alternate"].rstrip(".?!")],"audio_text":starter["alternate"],"explanation":"Говори спокойно. Важно, чтобы ключевые слова были понятны.","misconception":"foundation_mission_fluency","accessibility_label":"Повтори немецкую фразу"},
                {"question":"Скажи фразу вслух.","explanation":"Говори спокойно. Важно, чтобы ключевые слова были понятны.","accessibility_label":"Повтори немецкую фразу"},
                {"question":"Sprich den Satz laut.","explanation":"Sprich ruhig. Die Schlüsselwörter sollen verständlich sein.","accessibility_label":"Deutschen Satz nachsprechen"},
                {"question":"Say the sentence aloud.","explanation":"Speak calmly. The key words should be clear.","accessibility_label":"Repeat the German sentence"},
            ),
        ]
        return {
            "day":day,"week":module,"track":level,"module":module,"quality_version":8,
            "learning_method":"mission_loop_v1","module_title":module_title_ru,
            "module_step":((day - 1) % 5) + 1,"module_size":5,"checkpoint":bool(starter.get("checkpoint")),
            "title":title_ru,"objective":can_do_ru,"can_do":can_do_ru,
            "communication_goal":task_ru,"mission":task_ru,"success_evidence":can_do_ru,"scenario":scenario_ru,"rule":rule_ru,
            "examples":[model,starter["alternate"],f"❌ {wrong}"],"audio_text":model,"cefr":level,
            "prerequisites":[] if day == 1 else [(A1_CURRICULUM if level == "A1" else A2_CURRICULUM)[day - 2][2]],
            "common_mistakes":[f"❌ {wrong}",f"✅ {model}"],
            "recall_prompt":"Закрой пример и произнеси свою версию без подсказки.",
            "i18n":{
                "ru":{"title":title_ru,"module_title":module_title_ru,"objective":can_do_ru,"can_do":can_do_ru,"communication_goal":task_ru,"mission":task_ru,"success_evidence":can_do_ru,"scenario":scenario_ru,"rule":rule_ru,"recall_prompt":"Закрой пример и произнеси свою версию без подсказки."},
                "de":{"title":title_de,"module_title":module_title_de,"objective":can_do_de,"can_do":can_do_de,"communication_goal":task_de,"mission":task_de,"success_evidence":can_do_de,"scenario":scenario_de,"rule":rule_de,"recall_prompt":"Verdecke das Beispiel und sage deine eigene Version ohne Hilfe."},
                "en":{"title":title_en,"module_title":module_title_en,"objective":can_do_en,"can_do":can_do_en,"communication_goal":task_en,"mission":task_en,"success_evidence":can_do_en,"scenario":scenario_en,"rule":rule_en,"recall_prompt":"Hide the example and say your own version without help."},
            },
            "exercises":exercises,
        }
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
    scenario_ru, scenario_de, scenario_en, alternate, patterns = PRACTICE_VARIANTS[topic]
    patterns = patterns[:3]
    listening_options = list(dict.fromkeys([focus, "Frage", "Vergangenheit", "Zeitangabe"]))[:3]
    guided_kind = ("error_repair", "reorder", "transform")[(day - 1) % 3]
    guided_base = {"type":guided_kind,"stage":"guided","question":f"Исправь: {wrong}","answer":model,"accepted_answers":[model,model.rstrip(".")],"hint":rules["ru"],"explanation":rules["ru"],"misconception":"foundation_form"}
    if guided_kind == "reorder":
        tokens = model.rstrip(".?!").split()
        guided_base.update({"question":"Собери фразу для ситуации.", "tokens":tokens[1::2] + tokens[::2]})
    exercises = [
        _localized(
            guided_base,
            {"question": guided_base["question"],"hint":rules["ru"],"explanation":rules["ru"]},
            {"question":"Bilde den passenden Satz." if guided_kind == "reorder" else f"Korrigiere: {wrong}","hint":rules["de"],"explanation":rules["de"]},
            {"question":"Build the sentence for the situation." if guided_kind == "reorder" else f"Correct: {wrong}","hint":rules["en"],"explanation":rules["en"]},
        ),
        _localized(
            {"type":"context_choice","stage":"independent","question":f"Ситуация: {scenario_ru} Выбери подходящую фразу.","answer":model,"accepted_answers":[model],"options":[model,wrong,"Das weiß ich leider nicht."],"explanation":rules["ru"],"misconception":"foundation_context"},
            {"question":f"Ситуация: {scenario_ru} Выбери подходящую фразу.","explanation":rules["ru"]},
            {"question":f"Situation: {scenario_de} Wähle den passenden Satz.","explanation":rules["de"]},
            {"question":f"Situation: {scenario_en} Choose the sentence that fits.","explanation":rules["en"]},
        ),
        _localized(
            {"type":"listening_choice","stage":"independent","question":"Прослушай модель. Какую структуру ты слышишь?","answer":focus,"accepted_answers":[focus],"options":listening_options,"explanation":model,"misconception":"foundation_listening"},
            {"question":"Прослушай модель. Какую структуру ты слышишь?","explanation":model},
            {"question":"Höre das Modell. Welche Struktur hörst du?","explanation":model},
            {"question":"Listen to the model. Which pattern do you hear?","explanation":model},
        ),
        _localized(
            {"type":"dialogue","stage":"transfer","question":f"{scenario_ru} {goals['ru']}","answer":model,"model_answer":model,"accepted_answers":[model,model.rstrip(".")],"target_patterns":patterns,"hint":rules["ru"],"explanation":"Сравни смысл и структуру с моделью — слова могут отличаться.","misconception":"foundation_transfer"},
            {"question":f"{scenario_ru} {goals['ru']}","hint":rules["ru"],"explanation":"Сравни смысл и структуру с моделью — слова могут отличаться."},
            {"question":f"{scenario_de} {goals['de']}","hint":rules["de"],"explanation":"Vergleiche Bedeutung und Struktur; deine Wörter dürfen anders sein."},
            {"question":f"{scenario_en} {goals['en']}","hint":rules["en"],"explanation":"Compare meaning and structure; your wording may differ."},
        ),
        _localized(
            {"type":"repeat","stage":"transfer","question":"Произнеси модель вслух.","answer":model,"accepted_answers":[model,model.rstrip(".")],"explanation":"Повтори спокойно и чётко.","misconception":"foundation_fluency"},
            {"question":"Произнеси модель вслух.","explanation":"Повтори спокойно и чётко."},
            {"question":"Sprich das Modell laut nach.","explanation":"Sprich ruhig und deutlich."},
            {"question":"Say the model aloud.","explanation":"Speak calmly and clearly."},
        ),
    ]
    track_curriculum = A1_CURRICULUM if level == "A1" else A2_CURRICULUM
    prerequisites = [] if day == 1 else [track_curriculum[day - 2][2]]
    return {
        "day":day,"week":module,"track":level,"module":module,"quality_version":5,
        "learning_method":"notice_build_use_reflect","title":title_ru,"objective":goals["ru"],
        "communication_goal":goals["ru"],"scenario":scenario_ru,"rule":rules["ru"],"examples":[model,alternate,"Das ist heute wichtig für mich." if level == "A1" else "In dieser Situation würde ich ähnlich reagieren."],
        "audio_text":model,"cefr":level,"prerequisites":prerequisites,"common_mistakes":[f"❌ {wrong}",f"✅ {model}"],
        "recall_prompt":"Закрой пример, назови правило и создай собственную фразу.",
        "i18n":{"ru":{"title":title_ru,"rule":rules["ru"],"objective":goals["ru"],"scenario":scenario_ru},"de":{"title":title_de,"rule":rules["de"],"objective":goals["de"],"scenario":scenario_de},"en":{"title":title_en,"rule":rules["en"],"objective":goals["en"],"scenario":scenario_en}},
        "exercises":exercises,
    }
