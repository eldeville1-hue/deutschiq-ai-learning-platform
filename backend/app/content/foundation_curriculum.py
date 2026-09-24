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


def _localized(base: dict, ru: dict, de: dict, en: dict) -> dict:
    return {**base, "i18n": {"ru": ru, "de": de, "en": en}}


def build_foundation_content(row: tuple, level: str) -> dict:
    day, module, topic, pillar, title_ru, title_de, title_en, focus, model, wrong = row
    starter = A1_FIRST_CONVERSATION.get(topic) if level == "A1" and day <= 5 else None
    if starter:
        title_ru, title_de, title_en = starter["title"]
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
        exercises = [
            _localized(
                {"id":f"a1-{day}-build","type":"reorder","stage":"guided","question":"Собери полезную фразу.","answer":model,"accepted_answers":[model,model.rstrip(".?!")],"tokens":mixed_tokens,"hint":rule_ru,"explanation":rule_ru,"misconception":"a1_first_conversation_form","accessibility_label":"Собери немецкую фразу"},
                {"question":"Собери полезную фразу.","hint":rule_ru,"explanation":rule_ru,"accessibility_label":"Собери немецкую фразу"},
                {"question":"Baue den nützlichen Satz.","hint":rule_de,"explanation":rule_de,"accessibility_label":"Deutschen Satz bauen"},
                {"question":"Build the useful sentence.","hint":rule_en,"explanation":rule_en,"accessibility_label":"Build the German sentence"},
            ),
            _localized(
                {"id":f"a1-{day}-choose","type":"context_choice","stage":"independent","question":starter["choice"][0],"answer":model,"accepted_answers":[model],"options":choices,"explanation":rule_ru,"misconception":"a1_first_conversation_context","accessibility_label":"Выбери подходящую фразу"},
                {"question":starter["choice"][0],"explanation":rule_ru,"accessibility_label":"Выбери подходящую фразу"},
                {"question":starter["choice"][1],"explanation":rule_de,"accessibility_label":"Passenden Satz wählen"},
                {"question":starter["choice"][2],"explanation":rule_en,"accessibility_label":"Choose the matching sentence"},
            ),
            _localized(
                {"id":f"a1-{day}-listen","type":"listening_choice","stage":"independent","question":"Послушай. Что делает говорящий?","answer":listen_ru,"accepted_answers":[listen_ru],"options":list(options_ru),"audio_text":model,"explanation":model,"misconception":"a1_first_conversation_listening","accessibility_label":"Послушай и выбери смысл"},
                {"question":"Послушай. Что делает говорящий?","answer":listen_ru,"accepted_answers":[listen_ru],"options":list(options_ru),"accessibility_label":"Послушай и выбери смысл"},
                {"question":"Höre zu. Was macht die sprechende Person?","answer":listen_de,"accepted_answers":[listen_de],"options":list(options_de),"accessibility_label":"Hören und Bedeutung wählen"},
                {"question":"Listen. What is the speaker doing?","answer":listen_en,"accepted_answers":[listen_en],"options":list(options_en),"accessibility_label":"Listen and choose the meaning"},
            ),
            _localized(
                {"id":f"a1-{day}-use","type":"dialogue","stage":"transfer","question":task_ru,"answer":model,"model_answer":model,"accepted_answers":[model,model.rstrip(".?!")],"target_patterns":starter["patterns"],"hint":rule_ru,"explanation":"Смысл должен подходить ситуации. Личные данные могут отличаться.","misconception":"a1_first_conversation_transfer","accessibility_label":"Дай свой ответ по-немецки"},
                {"question":task_ru,"hint":rule_ru,"explanation":"Смысл должен подходить ситуации. Личные данные могут отличаться.","accessibility_label":"Дай свой ответ по-немецки"},
                {"question":task_de,"hint":rule_de,"explanation":"Die Antwort muss zur Situation passen. Persönliche Angaben dürfen anders sein.","accessibility_label":"Eigene Antwort auf Deutsch geben"},
                {"question":task_en,"hint":rule_en,"explanation":"The answer must fit the situation. Personal details may be different.","accessibility_label":"Give your own answer in German"},
            ),
            _localized(
                {"id":f"a1-{day}-speak","type":"repeat","stage":"transfer","question":"Скажи фразу вслух.","answer":starter["alternate"],"accepted_answers":[starter["alternate"],starter["alternate"].rstrip(".?!")],"audio_text":starter["alternate"],"explanation":"Говори спокойно. Важно, чтобы ключевые слова были понятны.","misconception":"a1_first_conversation_fluency","accessibility_label":"Повтори немецкую фразу"},
                {"question":"Скажи фразу вслух.","explanation":"Говори спокойно. Важно, чтобы ключевые слова были понятны.","accessibility_label":"Повтори немецкую фразу"},
                {"question":"Sprich den Satz laut.","explanation":"Sprich ruhig. Die Schlüsselwörter sollen verständlich sein.","accessibility_label":"Deutschen Satz nachsprechen"},
                {"question":"Say the sentence aloud.","explanation":"Speak calmly. The key words should be clear.","accessibility_label":"Repeat the German sentence"},
            ),
        ]
        return {
            "day":day,"week":1,"track":"A1","module":1,"quality_version":6,
            "learning_method":"notice_build_use_reflect","module_title":"Первый разговор",
            "module_step":day,"module_size":5,"checkpoint":bool(starter.get("checkpoint")),
            "title":title_ru,"objective":can_do_ru,"can_do":can_do_ru,
            "communication_goal":task_ru,"scenario":scenario_ru,"rule":rule_ru,
            "examples":[model,starter["alternate"],f"❌ {wrong}"],"audio_text":model,"cefr":"A1",
            "prerequisites":[] if day == 1 else [A1_CURRICULUM[day - 2][2]],
            "common_mistakes":[f"❌ {wrong}",f"✅ {model}"],
            "recall_prompt":"Закрой пример и произнеси свою версию без подсказки.",
            "i18n":{
                "ru":{"title":title_ru,"module_title":"Первый разговор","objective":can_do_ru,"can_do":can_do_ru,"communication_goal":task_ru,"scenario":scenario_ru,"rule":rule_ru,"recall_prompt":"Закрой пример и произнеси свою версию без подсказки."},
                "de":{"title":title_de,"module_title":"Das erste Gespräch","objective":can_do_de,"can_do":can_do_de,"communication_goal":task_de,"scenario":scenario_de,"rule":rule_de,"recall_prompt":"Verdecke das Beispiel und sage deine eigene Version ohne Hilfe."},
                "en":{"title":title_en,"module_title":"Your first conversation","objective":can_do_en,"can_do":can_do_en,"communication_goal":task_en,"scenario":scenario_en,"rule":rule_en,"recall_prompt":"Hide the example and say your own version without help."},
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
    return {
        "day":day,"week":module,"track":level,"module":module,"quality_version":5,
        "learning_method":"notice_build_use_reflect","title":title_ru,"objective":goals["ru"],
        "communication_goal":goals["ru"],"scenario":scenario_ru,"rule":rules["ru"],"examples":[model,alternate,"Das ist heute wichtig für mich." if level == "A1" else "In dieser Situation würde ich ähnlich reagieren."],
        "audio_text":model,"cefr":level,"prerequisites":[],"common_mistakes":[f"❌ {wrong}",f"✅ {model}"],
        "recall_prompt":"Закрой пример, назови правило и создай собственную фразу.",
        "i18n":{"ru":{"title":title_ru,"rule":rules["ru"],"objective":goals["ru"],"scenario":scenario_ru},"de":{"title":title_de,"rule":rules["de"],"objective":goals["de"],"scenario":scenario_de},"en":{"title":title_en,"rule":rules["en"],"objective":goals["en"],"scenario":scenario_en}},
        "exercises":exercises,
    }
