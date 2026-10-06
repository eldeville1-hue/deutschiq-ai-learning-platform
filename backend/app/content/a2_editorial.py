"""A2 explanations and listening meanings, aligned with the recorded models.

Entries use Russian, German, English order. Listening labels describe only
the recording, rather than claiming that the whole lesson mission is heard.
"""

A2_GRAMMAR_RULES = {
    "dative_a2": (
        "После geben получатель стоит в Dativ: meiner Freundin, meinem Kollegen. Предмет — в Akkusativ: das Buch, den Schlüssel.",
        "Bei geben steht die empfangende Person im Dativ: meiner Freundin, meinem Kollegen. Die Sache steht im Akkusativ: das Buch, den Schlüssel.",
        "With geben, put the recipient in the dative: meiner Freundin, meinem Kollegen. The item is accusative: das Buch, den Schlüssel.",
    ),
    "dative_accusative": (
        "Wem? — Dativ: den Schülern, meiner Kollegin. Was? — Akkusativ: die Aufgabe, den Plan. С двумя существительными получатель обычно стоит перед предметом; это не правило для всех местоимений.",
        "Wem? — Dativ: den Schülern, meiner Kollegin. Was? — Akkusativ: die Aufgabe, den Plan. Bei zwei Nomen steht die Person meist vor der Sache; für Pronomen gilt das nicht immer.",
        "Wem? identifies the dative recipient: den Schülern, meiner Kollegin. Was? identifies the accusative item: die Aufgabe, den Plan. With two nouns the recipient usually comes first; pronouns can follow a different order.",
    ),
    "two_way_prepositions": (
        "С Wechselpräpositionen: положение (wo?) — Dativ, направление к новому месту (wohin?) — Akkusativ. Die Tasche liegt auf dem Stuhl. Ich stelle die Vase auf den Tisch. Движение само по себе не требует Akkusativ.",
        "Bei Wechselpräpositionen: Ort (wo?) — Dativ; Ziel einer Ortsveränderung (wohin?) — Akkusativ. Die Tasche liegt auf dem Stuhl. Ich stelle die Vase auf den Tisch. Bewegung allein verlangt keinen Akkusativ.",
        "With two-way prepositions, location (wo?) takes dative and a destination (wohin?) takes accusative: auf dem Stuhl versus auf den Tisch. Movement alone does not require accusative.",
    ),
    "dative_prepositions": (
        "Mit, bei, seit, nach, aus, von и zu требуют Dativ: mit meiner Schwester, bei meiner Tante, seit einem Jahr. Для ситуации, которая продолжается, используй seit + Präsens.",
        "Mit, bei, seit, nach, aus, von und zu verlangen Dativ: mit meiner Schwester, bei meiner Tante, seit einem Jahr. Für eine Situation, die noch andauert, nutzt du seit + Präsens.",
        "Mit, bei, seit, nach, aus, von and zu take dative: mit meiner Schwester, bei meiner Tante, seit einem Jahr. Use seit with the present tense for a situation that still continues.",
    ),
    "accusative_prepositions": (
        "Für, ohne, durch, gegen и um требуют Akkusativ: für meinen Bruder, ohne den Schlüssel. После начального Ohne den Schlüssel идёт изменяемый глагол: können wir …",
        "Für, ohne, durch, gegen und um verlangen Akkusativ: für meinen Bruder, ohne den Schlüssel. Nach Ohne den Schlüssel am Satzanfang folgt das konjugierte Verb: können wir …",
        "Für, ohne, durch, gegen and um take accusative: für meinen Bruder, ohne den Schlüssel. After an opening Ohne den Schlüssel, put the conjugated verb before the subject: können wir …",
    ),
    "perfect_haben": (
        "Perfekt: изменяемый haben на втором месте, Partizip II в конце: Ich habe einen Film gesehen. Arbeiten → gearbeitet, lesen → gelesen. Большинство глаголов используют haben.",
        "Perfekt: konjugiertes haben an zweiter Stelle, Partizip II am Ende: Ich habe einen Film gesehen. Arbeiten → gearbeitet, lesen → gelesen. Die meisten Verben verwenden haben.",
        "For the perfect tense, put conjugated haben second and the past participle last: Ich habe einen Film gesehen. Arbeiten → gearbeitet; lesen → gelesen. Most verbs use haben.",
    ),
    "perfect_sein": (
        "Смена места без прямого дополнения часто требует sein: Ich bin nach Bremen gefahren. Смена состояния: einschlafen → ist eingeschlafen. Не все глаголы движения используют sein: Ich habe getanzt.",
        "Ein Ortswechsel ohne Akkusativobjekt verlangt oft sein: Ich bin nach Bremen gefahren. Zustandswechsel: einschlafen → ist eingeschlafen. Nicht jedes Bewegungsverb verwendet sein: Ich habe getanzt.",
        "A change of location without a direct object often uses sein: Ich bin nach Bremen gefahren. A change of state also can: ist eingeschlafen. Movement does not always mean sein: Ich habe getanzt.",
    ),
    "perfect_participles": (
        "Учи Partizip II с глаголом: schreiben → geschrieben, abschicken → abgeschickt, anrufen → angerufen. У отделяемого глагола ge стоит между приставкой и основой; у besuchen нет ge: besucht.",
        "Lerne das Partizip II mit dem Verb: schreiben → geschrieben, abschicken → abgeschickt, anrufen → angerufen. Bei trennbaren Verben steht ge zwischen Vorsilbe und Stamm; besuchen hat kein ge: besucht.",
        "Learn each past participle with its verb: schreiben → geschrieben, abschicken → abgeschickt, anrufen → angerufen. Separable verbs put ge after the prefix; besuchen has no ge: besucht.",
    ),
    "modal_past_a2": (
        "О прошлой обязанности: ich musste. О возможности: ich konnte; разрешении: ich durfte. Инфинитив стоит в конце: Ich musste arbeiten und konnte nicht kommen.",
        "Frühere Pflicht: ich musste. Möglichkeit: ich konnte; Erlaubnis: ich durfte. Der Infinitiv steht am Ende: Ich musste arbeiten und konnte nicht kommen.",
        "Use ich musste for a past obligation, ich konnte for ability or possibility, and ich durfte for permission. Put the infinitive last: Ich musste arbeiten und konnte nicht kommen.",
    ),
    "past_sequence": (
        "Zuerst, dann, danach связывают события. После такого слова изменяемый глагол стоит перед подлежащим: Dann habe ich ein Taxi gerufen. Partizip II остаётся в конце.",
        "Zuerst, dann und danach verbinden Ereignisse. Danach steht das konjugierte Verb vor dem Subjekt: Dann habe ich ein Taxi gerufen. Das Partizip II bleibt am Ende.",
        "Use zuerst, dann and danach to sequence events. After one of these opening words, put the conjugated verb before the subject: Dann habe ich ein Taxi gerufen. The participle stays last.",
    ),
    "weil_clause": (
        "Weil вводит причину. Перед придаточным — запятая, изменяемый глагол — в конце: Ich fahre mit dem Bus, weil es regnet. С модальным глаголом: weil ich arbeiten muss.",
        "Weil nennt einen Grund. Vor dem Nebensatz steht ein Komma; das konjugierte Verb steht am Ende: Ich fahre mit dem Bus, weil es regnet. Mit Modalverb: weil ich arbeiten muss.",
        "Weil introduces a reason. Use a comma before the clause and put the conjugated verb last: Ich fahre mit dem Bus, weil es regnet. With a modal: weil ich arbeiten muss.",
    ),
    "dass_clause": (
        "Dass передаёт информацию или мнение. Перед dass — запятая, изменяемый глагол — в конце: Sie hat gesagt, dass der Termin später beginnt. Ich denke, dass der Plan besser ist.",
        "Dass gibt eine Information oder Meinung wieder. Vor dass steht ein Komma; das konjugierte Verb steht am Ende: Sie hat gesagt, dass der Termin später beginnt. Ich denke, dass der Plan besser ist.",
        "Dass reports information or an opinion. Use a comma before dass and put the conjugated verb last: Sie hat gesagt, dass der Termin später beginnt. Ich denke, dass der Plan besser ist.",
    ),
    "wenn_clause": (
        "В придаточном с wenn изменяемый глагол стоит в конце. Если придаточное первое, после запятой сразу идёт глагол главного предложения: Wenn es regnet, besuchen wir ein Museum.",
        "Im wenn-Satz steht das konjugierte Verb am Ende. Steht der Nebensatz zuerst, folgt nach dem Komma sofort das Verb des Hauptsatzes: Wenn es regnet, besuchen wir ein Museum.",
        "Put the conjugated verb last in a wenn clause. If that clause comes first, put the main-clause verb immediately after the comma: Wenn es regnet, besuchen wir ein Museum.",
    ),
    "comparatives": (
        "Сравнение: schneller/günstiger/bequemer als … Не mehr schnell. Равенство: so schnell wie … Формы с изменением гласной учи отдельно: gut → besser.",
        "Vergleich: schneller/günstiger/bequemer als … Nicht mehr schnell. Gleichheit: so schnell wie … Lerne unregelmäßige Formen einzeln: gut → besser.",
        "Compare with schneller/günstiger/bequemer als … rather than mehr schnell. For equality use so schnell wie … Learn irregular forms separately: gut → besser.",
    ),
    "reflexive_verbs": (
        "Местоимение зависит от подлежащего: ich interessiere mich, du interessierst dich, wir interessieren uns. Sich interessieren für + Akkusativ. Sich treffen: Wir treffen uns am Samstag.",
        "Das Pronomen passt zum Subjekt: ich interessiere mich, du interessierst dich, wir interessieren uns. Sich interessieren für + Akkusativ. Sich treffen: Wir treffen uns am Samstag.",
        "Match the reflexive pronoun to the subject: ich interessiere mich, du interessierst dich, wir interessieren uns. Use sich interessieren für with accusative. For meeting: Wir treffen uns am Samstag.",
    ),
    "requests_a2": (
        "Вежливая просьба: Könnten Sie mir bitte …? Смысловой глагол — в конце в инфинитиве: helfen / geben. Mir — Dativ. Könnten мягче, чем Können, но Können Sie … bitte? тоже вежливо.",
        "Höfliche Bitte: Könnten Sie mir bitte …? Der Infinitiv steht am Ende: helfen / geben. Mir steht im Dativ. Könnten klingt vorsichtiger; auch Können Sie … bitte? ist höflich.",
        "Make a polite request with Könnten Sie mir bitte …? Put the infinitive last: helfen / geben. Mir is dative. Könnten sounds more tentative; Können Sie … bitte? is also polite.",
    ),
    "formal_message_a2": (
        "Для первого официального сообщения: Sehr geehrte Frau Klein, затем с новой строки leider kann ich …; просьба: Könnten Sie mir bitte …? Заверши Mit freundlichen Grüßen и именем. После обращения с запятой продолжай со строчной буквы.",
        "Für eine erste formelle Nachricht: Sehr geehrte Frau Klein, dann in einer neuen Zeile leider kann ich …; Bitte: Könnten Sie mir bitte …? Schließe mit Mit freundlichen Grüßen und deinem Namen. Nach der Anrede mit Komma geht es klein weiter.",
        "For a first formal message, use Sehr geehrte Frau Klein, then a new line starting leider kann ich …; request with Könnten Sie mir bitte …? Close with Mit freundlichen Grüßen and your name. Continue in lowercase after the greeting's comma.",
    ),
    "opinions_a2": (
        "Мнение: Ich finde … besser/gut. Причина: weil + глагол в конце. Добавь недостаток с aber: Aber der Weg zum Kurs dauert lange. В диалоге ответ Weil … может стоять отдельно после Warum?.",
        "Meinung: Ich finde … besser/gut. Grund: weil + Verb am Ende. Ergänze einen Nachteil mit aber: Aber der Weg zum Kurs dauert lange. Im Gespräch ist eine Antwort mit Weil … nach Warum? möglich.",
        "State an opinion with Ich finde … besser/gut. Give a reason using weil and a final verb. Add a drawback with aber. In conversation, a standalone Weil … answer can respond to Warum?.",
    ),
    "problem_solution_a2": (
        "Проблема: Mein Zug fällt aus — отделяемая приставка в конце. Следствие: Deshalb brauche ich … — глагол перед ich. Назови пункт назначения и попроси другую Verbindung (вариант поездки).",
        "Problem: Mein Zug fällt aus — die trennbare Vorsilbe steht am Ende. Folge: Deshalb brauche ich … — Verb vor ich. Nenne dein Reiseziel und bitte um eine andere Verbindung.",
        "State the problem: Mein Zug fällt aus, with the separable prefix last. State the consequence: Deshalb brauche ich …, with the verb before ich. Give your destination and request another travel connection.",
    ),
    "a2_final": (
        "Соедини изученные навыки: извинение, событие в Perfekt, причина с weil (глагол в конце) и вежливое предложение решения. Ich konnte nicht anrufen, weil mein Akku leer war. Könnten wir jetzt beginnen?",
        "Verbinde die geübten Fähigkeiten: Entschuldigung, Ereignis im Perfekt, Grund mit weil (Verb am Ende) und höflicher Lösungsvorschlag. Ich konnte nicht anrufen, weil mein Akku leer war. Könnten wir jetzt beginnen?",
        "Combine the skills you practised: an apology, an event in the perfect tense, a weil reason with a final verb, and a polite solution. Ich konnte nicht anrufen, weil mein Akku leer war. Könnten wir jetzt beginnen?",
    ),
}

A2_LISTENING_MEANINGS = {
    "dative_a2": ("Человек даёт подруге книгу", "Die Person gibt ihrer Freundin ein Buch", "The speaker gives a friend a book"),
    "dative_accusative": ("Учитель объясняет ученикам задание", "Der Lehrer erklärt den Schülern eine Aufgabe", "The teacher explains a task to the students"),
    "two_way_prepositions": ("Человек ставит вазу на стол", "Die Person stellt eine Vase auf den Tisch", "The speaker puts a vase on the table"),
    "dative_prepositions": ("Человек уже год живёт у тёти", "Die Person wohnt seit einem Jahr bei ihrer Tante", "The speaker has lived with an aunt for a year"),
    "accusative_prepositions": ("Подарок предназначен брату", "Das Geschenk ist für den Bruder", "The gift is for the speaker's brother"),
    "perfect_haben": ("Человек вчера посмотрел фильм", "Die Person hat gestern einen Film gesehen", "The speaker watched a film yesterday"),
    "perfect_sein": ("Люди ездили в Любек на выходных", "Die Personen sind am Wochenende nach Lübeck gefahren", "The speakers went to Lübeck at the weekend"),
    "perfect_participles": ("Человек написал и отправил электронное письмо", "Die Person hat eine E-Mail geschrieben und abgeschickt", "The speaker wrote and sent an email"),
    "modal_past_a2": ("Раньше человек должен был работать каждую субботу", "Die Person musste früher jeden Samstag arbeiten", "The speaker used to have to work every Saturday"),
    "past_sequence": ("Сначала человек встал, затем позавтракал", "Die Person ist zuerst aufgestanden und hat danach gefrühstückt", "The speaker got up first and then had breakfast"),
    "weil_clause": ("Человек учит немецкий, потому что работает в Германии", "Die Person lernt Deutsch, weil sie in Deutschland arbeitet", "The speaker studies German because they work in Germany"),
    "dass_clause": ("Человек считает курс очень полезным", "Die Person glaubt, dass der Kurs sehr hilfreich ist", "The speaker thinks the course is very helpful"),
    "wenn_clause": ("Человек посещает друзей, когда есть время", "Die Person besucht ihre Freunde, wenn sie Zeit hat", "The speaker visits friends when they have time"),
    "comparatives": ("Поезд быстрее автобуса", "Der Zug ist schneller als der Bus", "The train is faster than the bus"),
    "reflexive_verbs": ("Человек интересуется современным искусством", "Die Person interessiert sich für moderne Kunst", "The speaker is interested in modern art"),
    "requests_a2": ("Человек вежливо просит назначить встречу", "Die Person bittet höflich um einen Termin", "The speaker politely asks for an appointment"),
    "formal_message_a2": ("Человек официально просит перенести запись", "Die Person möchte einen Termin formell verschieben", "The speaker formally requests to reschedule an appointment"),
    "opinions_a2": ("Человеку нравится курс, потому что там много говорят", "Die Person findet den Kurs gut, weil dort viel gesprochen wird", "The speaker likes the course because they speak a lot there"),
    "problem_solution_a2": ("Поезд отменён, человеку нужен другой вариант поездки", "Der Zug fällt aus; die Person braucht eine andere Verbindung", "The train is cancelled and the speaker needs another connection"),
    "a2_final": ("Человек переехал в прошлом году, потому что нашёл новую работу", "Die Person ist letztes Jahr wegen einer neuen Stelle umgezogen", "The speaker moved last year because they found a new job"),
}

A2_LISTENING_DISTRACTORS = {
    "dative_a2": (("Подруга даёт человеку книгу", "Человек просит подругу дать книгу"), ("Die Freundin gibt der Person ein Buch", "Die Person bittet ihre Freundin um ein Buch"), ("The friend gives the speaker a book", "The speaker asks a friend for a book")),
    "dative_accusative": (("Ученики объясняют учителю задание", "Учитель задаёт ученикам вопрос"), ("Die Schüler erklären dem Lehrer die Aufgabe", "Der Lehrer stellt den Schülern eine Frage"), ("The students explain the task to the teacher", "The teacher asks the students a question")),
    "two_way_prepositions": (("Ваза уже стоит на столе", "Человек ставит вазу под стол"), ("Die Vase steht schon auf dem Tisch", "Die Person stellt die Vase unter den Tisch"), ("The vase is already on the table", "The speaker puts the vase under the table")),
    "dative_prepositions": (("Человек жил у тёти год, но уже уехал", "Человек переедет к тёте через год"), ("Die Person hat ein Jahr bei ihrer Tante gewohnt und ist schon ausgezogen", "Die Person zieht in einem Jahr zu ihrer Tante"), ("The speaker lived with an aunt for a year and has already left", "The speaker will move in with an aunt in a year")),
    "accusative_prepositions": (("Подарок от брата", "Подарок для сестры"), ("Das Geschenk kommt vom Bruder", "Das Geschenk ist für die Schwester"), ("The gift is from the brother", "The gift is for the sister")),
    "perfect_haben": (("Человек посмотрит фильм завтра", "Человек вчера прочитал книгу"), ("Die Person sieht morgen einen Film", "Die Person hat gestern ein Buch gelesen"), ("The speaker will watch a film tomorrow", "The speaker read a book yesterday")),
    "perfect_sein": (("Люди поедут в Любек на следующих выходных", "Люди ездили в Бремен на выходных"), ("Die Personen fahren nächstes Wochenende nach Lübeck", "Die Personen sind am Wochenende nach Bremen gefahren"), ("The speakers will go to Lübeck next weekend", "The speakers went to Bremen at the weekend")),
    "perfect_participles": (("Человек написал письмо, но ещё не отправил", "Человек получил и прочитал письмо"), ("Die Person hat eine E-Mail geschrieben, aber noch nicht abgeschickt", "Die Person hat eine E-Mail bekommen und gelesen"), ("The speaker wrote an email but has not sent it yet", "The speaker received and read an email")),
    "modal_past_a2": (("Раньше человек мог работать каждую субботу", "Человек должен работать каждую субботу сейчас"), ("Die Person konnte früher jeden Samstag arbeiten", "Die Person muss jetzt jeden Samstag arbeiten"), ("The speaker used to be able to work every Saturday", "The speaker has to work every Saturday now")),
    "past_sequence": (("Сначала человек позавтракал, затем встал", "Человек встал, но не позавтракал"), ("Die Person hat zuerst gefrühstückt und ist danach aufgestanden", "Die Person ist aufgestanden, hat aber nicht gefrühstückt"), ("The speaker had breakfast first and then got up", "The speaker got up but did not have breakfast")),
    "weil_clause": (("Человек учит немецкий, потому что учится в Германии", "Человек работает в Германии, потому что учит немецкий"), ("Die Person lernt Deutsch, weil sie in Deutschland studiert", "Die Person arbeitet in Deutschland, weil sie Deutsch lernt"), ("The speaker studies German because they study in Germany", "The speaker works in Germany because they study German")),
    "dass_clause": (("Человек считает курс бесполезным", "Человек знает, что курс уже закончился"), ("Die Person glaubt, dass der Kurs nicht hilfreich ist", "Die Person weiß, dass der Kurs schon zu Ende ist"), ("The speaker thinks the course is unhelpful", "The speaker knows the course has already ended")),
    "wenn_clause": (("Друзья посещают человека, когда у них есть время", "Человек посещает друзей, даже когда нет времени"), ("Die Freunde besuchen die Person, wenn sie Zeit haben", "Die Person besucht ihre Freunde auch ohne Zeit"), ("The friends visit the speaker when they have time", "The speaker visits friends even when they have no time")),
    "comparatives": (("Автобус быстрее поезда", "Поезд и автобус одинаково быстрые"), ("Der Bus ist schneller als der Zug", "Zug und Bus sind gleich schnell"), ("The bus is faster than the train", "The train and bus are equally fast")),
    "reflexive_verbs": (("Человек не интересуется современным искусством", "Человек интересуется классической музыкой"), ("Die Person interessiert sich nicht für moderne Kunst", "Die Person interessiert sich für klassische Musik"), ("The speaker is not interested in modern art", "The speaker is interested in classical music")),
    "requests_a2": (("Человек просит отменить запись", "Человек просит объяснить формуляр"), ("Die Person bittet darum, einen Termin abzusagen", "Die Person bittet um eine Erklärung zum Formular"), ("The speaker asks to cancel an appointment", "The speaker asks for an explanation of a form")),
    "formal_message_a2": (("Человек подтверждает запись без изменений", "Человек просит совсем отменить запись"), ("Die Person bestätigt den unveränderten Termin", "Die Person möchte den Termin ganz absagen"), ("The speaker confirms the unchanged appointment", "The speaker wants to cancel the appointment entirely")),
    "opinions_a2": (("Курс нравится человеку, потому что там мало говорят", "Курс не нравится человеку, потому что там много говорят"), ("Die Person findet den Kurs gut, weil dort wenig gesprochen wird", "Die Person findet den Kurs schlecht, weil dort viel gesprochen wird"), ("The speaker likes the course because they speak little there", "The speaker dislikes the course because they speak a lot there")),
    "problem_solution_a2": (("Поезд опаздывает, но человек ждёт именно его", "Человек нашёл другой вариант поездки и купил билет"), ("Der Zug hat Verspätung und die Person wartet auf ihn", "Die Person hat eine andere Verbindung gefunden und eine Fahrkarte gekauft"), ("The train is delayed and the speaker is waiting for it", "The speaker found another connection and bought a ticket")),
    "a2_final": (("Человек переедет в следующем году из-за новой работы", "Человек переехал в прошлом году, потому что потерял работу"), ("Die Person zieht nächstes Jahr wegen einer neuen Stelle um", "Die Person ist letztes Jahr umgezogen, weil sie ihre Stelle verloren hat"), ("The speaker will move next year because of a new job", "The speaker moved last year because they lost their job")),
}

A2_REPAIR_ALTERNATIVES = {
    "two_way_prepositions": ["Auf den Tisch stelle ich die Vase."],
    "perfect_participles": ["Sie hat die E-Mail geschrieben und dann abgeschickt."],
    "past_sequence": ["Zuerst bin ich aufgestanden. Danach habe ich gefrühstückt."],
    "wenn_clause": ["Ich besuche meine Freunde, wenn ich Zeit habe."],
    "reflexive_verbs": ["Für moderne Kunst interessiere ich mich."],
    "opinions_a2": ["Weil wir viel sprechen, finde ich den Kurs gut."],
    "a2_final": ["Ich bin letztes Jahr umgezogen, weil ich eine neue Stelle gefunden habe."],
}
