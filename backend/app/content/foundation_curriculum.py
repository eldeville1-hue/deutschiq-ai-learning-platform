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


for _row in A1_CURRICULUM[5:]:
    _day, _module, _topic, _pillar, _title_ru, _title_de, _title_en, _focus, _model, _wrong = _row
    _blueprint = A1_MISSION_BLUEPRINTS[_topic]
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
    starter = A1_FIRST_CONVERSATION.get(topic) if level == "A1" else None
    if starter:
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
                {"id":f"a1-{day}-build","type":"reorder","stage":"guided","question":"Собери полезную фразу.","answer":model,"accepted_answers":[model,model.rstrip(".?!")],"tokens":mixed_tokens,"hint":rule_ru,"explanation":rule_ru,"misconception":"a1_first_conversation_form","accessibility_label":"Собери немецкую фразу"},
                {"question":"Собери полезную фразу.","hint":rule_ru,"explanation":rule_ru,"accessibility_label":"Собери немецкую фразу"},
                {"question":"Baue den nützlichen Satz.","hint":rule_de,"explanation":rule_de,"accessibility_label":"Deutschen Satz bauen"},
                {"question":"Build the useful sentence.","hint":rule_en,"explanation":rule_en,"accessibility_label":"Build the German sentence"},
            ),
            _localized(
                {"id":f"a1-{day}-analogy","type":"analogy_choice","stage":"independent","question":starter["choice"][0],"answer":model,"accepted_answers":[model],"options":choices,"analogy_source":starter["alternate"],"analogy_target":scenario_ru,"pattern_label":"Та же структура — новая ситуация","explanation":rule_ru,"misconception":"a1_first_conversation_transfer","accessibility_label":"Перенеси знакомую структуру в новую ситуацию"},
                {"question":starter["choice"][0],"analogy_target":scenario_ru,"pattern_label":"Та же структура — новая ситуация","explanation":rule_ru,"accessibility_label":"Перенеси знакомую структуру в новую ситуацию"},
                {"question":starter["choice"][1],"analogy_target":scenario_de,"pattern_label":"Gleiches Muster – neue Situation","explanation":rule_de,"accessibility_label":"Bekanntes Muster auf eine neue Situation übertragen"},
                {"question":starter["choice"][2],"analogy_target":scenario_en,"pattern_label":"Same pattern — new situation","explanation":rule_en,"accessibility_label":"Transfer a familiar pattern to a new situation"},
            ),
            _localized(
                {"id":f"a1-{day}-listen","type":"listening_choice","stage":"independent","question":"Послушай. Что делает говорящий?","answer":listen_ru,"accepted_answers":[listen_ru],"options":list(options_ru),"audio_text":model,"explanation":model,"misconception":"a1_first_conversation_listening","accessibility_label":"Послушай и выбери смысл"},
                {"question":"Послушай. Что делает говорящий?","answer":listen_ru,"accepted_answers":[listen_ru],"options":list(options_ru),"accessibility_label":"Послушай и выбери смысл"},
                {"question":"Höre zu. Was macht die sprechende Person?","answer":listen_de,"accepted_answers":[listen_de],"options":list(options_de),"accessibility_label":"Hören und Bedeutung wählen"},
                {"question":"Listen. What is the speaker doing?","answer":listen_en,"accepted_answers":[listen_en],"options":list(options_en),"accessibility_label":"Listen and choose the meaning"},
            ),
            _localized(
                {"id":f"a1-{day}-use","type":"dialogue","stage":"transfer","mission_role":"final","question":task_ru,"answer":mission_model,"model_answer":mission_model,"accepted_answers":[model,model.rstrip(".?!")],"target_patterns":(["heiße","woher","wo"] if day == 5 else starter["patterns"]),"hint":rule_ru,"explanation":"Смысл должен подходить ситуации. Личные данные могут отличаться.","misconception":"a1_first_conversation_transfer","accessibility_label":"Пройди реальный мини-диалог","conversation_turns":mission_turns["ru"]},
                {"question":task_ru,"hint":rule_ru,"explanation":"Смысл должен подходить ситуации. Личные данные могут отличаться.","accessibility_label":"Пройди реальный мини-диалог","conversation_turns":mission_turns["ru"]},
                {"question":task_de,"hint":rule_de,"explanation":"Die Antwort muss zur Situation passen. Persönliche Angaben dürfen anders sein.","accessibility_label":"Ein echtes Mini-Gespräch führen","conversation_turns":mission_turns["de"]},
                {"question":task_en,"hint":rule_en,"explanation":"The answer must fit the situation. Personal details may be different.","accessibility_label":"Complete a real mini dialogue","conversation_turns":mission_turns["en"]},
            ),
            _localized(
                {"id":f"a1-{day}-speak","type":"repeat","stage":"transfer","question":"Скажи фразу вслух.","answer":starter["alternate"],"accepted_answers":[starter["alternate"],starter["alternate"].rstrip(".?!")],"audio_text":starter["alternate"],"explanation":"Говори спокойно. Важно, чтобы ключевые слова были понятны.","misconception":"a1_first_conversation_fluency","accessibility_label":"Повтори немецкую фразу"},
                {"question":"Скажи фразу вслух.","explanation":"Говори спокойно. Важно, чтобы ключевые слова были понятны.","accessibility_label":"Повтори немецкую фразу"},
                {"question":"Sprich den Satz laut.","explanation":"Sprich ruhig. Die Schlüsselwörter sollen verständlich sein.","accessibility_label":"Deutschen Satz nachsprechen"},
                {"question":"Say the sentence aloud.","explanation":"Speak calmly. The key words should be clear.","accessibility_label":"Repeat the German sentence"},
            ),
        ]
        return {
            "day":day,"week":module,"track":"A1","module":module,"quality_version":7,
            "learning_method":"mission_loop_v1","module_title":module_title_ru,
            "module_step":((day - 1) % 5) + 1,"module_size":5,"checkpoint":bool(starter.get("checkpoint")),
            "title":title_ru,"objective":can_do_ru,"can_do":can_do_ru,
            "communication_goal":task_ru,"mission":task_ru,"success_evidence":can_do_ru,"scenario":scenario_ru,"rule":rule_ru,
            "examples":[model,starter["alternate"],f"❌ {wrong}"],"audio_text":model,"cefr":"A1",
            "prerequisites":[] if day == 1 else [A1_CURRICULUM[day - 2][2]],
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
