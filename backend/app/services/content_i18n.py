"""Localize lesson instructions while keeping German learning material unchanged."""
from copy import deepcopy

LESSON_COPY = {
"de": [
("Verbposition im Hauptsatz","Im Aussagesatz steht das konjugierte Verb an Position zwei.","Ordne die Wörter: heute / ich / Deutsch / lerne","Erzähle, was du heute machst."),
("Inversion nach einer Angabe","Beginnt der Satz mit Zeit oder Ort, folgt das Subjekt nach dem Verb.","Ordne: am Montag / ich / zu Hause / arbeite","Beschreibe deinen Plan für einen bestimmten Tag."),
("W-Fragen","Nach dem Fragewort folgen Verb und Subjekt.","Bilde die Frage: wann / du / nach Hause / kommst","Stelle eine Frage nach der Zeit."),
("Ja/Nein-Fragen","Ohne Fragewort steht das Verb an Position eins.","Bilde die Frage: du / heute / Deutsch / lernst","Stelle eine Ja/Nein-Frage."),
("Modalverben","Das Modalverb steht an Position zwei, der Infinitiv am Satzende.","Ordne: ich / heute / länger / arbeiten / kann","Sage, was du kannst oder musst."),
("Trennbare Verben","Der konjugierte Teil steht an Position zwei, die Vorsilbe am Ende.","Ordne: ich / um sieben Uhr / stehe / auf","Beschreibe eine Handlung mit einem trennbaren Verb."),
("Nebensätze mit weil","Im weil-Satz steht das konjugierte Verb am Ende.","Verbinde mit weil: Ich lerne Deutsch. Ich lebe in Berlin.","Begründe eine Handlung."),
("Akkusativ: direktes Objekt","Der Akkusativ bezeichnet das direkte Ziel einer Handlung.","Setze den Artikel ein: Ich sehe ___ Mann.","Sage, wen oder was du siehst."),
("Dativ: Empfänger","Der Dativ antwortet auf wem?.","Setze den Artikel ein: Ich helfe ___ Mann.","Sage, wem du hilfst."),
("geben: Dativ und Akkusativ","Bei geben steht der Empfänger im Dativ und die Sache im Akkusativ.","Ergänze: Ich gebe ___ Kind das Buch.","Sage, wem du was gibst."),
("Präpositionen mit Akkusativ","durch, für, gegen, ohne und um verlangen immer den Akkusativ.","Ergänze: Das ist für ___ Bruder. (mein)","Sage, für wen etwas bestimmt ist."),
("Präpositionen mit Dativ","aus, bei, mit, nach, seit, von und zu verlangen immer den Dativ.","Ergänze: Ich fahre mit ___ Bus.","Sage, womit oder mit wem du fährst."),
("Personalpronomen im Dativ","mir, dir, ihm, ihr, uns, euch und ihnen ersetzen ein Dativobjekt.","Ersetze dem Mann: Ich helfe ___.","Bitte um Hilfe oder sage, wem du hilfst."),
("Wechselpräpositionen: wo/wohin","Wo? verlangt Dativ; wohin? verlangt Akkusativ.","Wo? Das Bild hängt an ___ Wand.","Beschreibe Position oder Richtung."),
("Genus von Nomen","Lerne den Artikel zusammen mit dem Nomen: der Tisch, die Lampe, das Buch.","Wähle den Artikel: ___ Buch","Nenne einen Gegenstand mit dem richtigen Artikel."),
("Maskuline Endungen","Nomen auf -er, -ling und -ismus sind häufig maskulin.","Artikel: ___ Frühling","Verwende ein maskulines Nomen."),
("Feminine Endungen","Nomen auf -ung, -heit, -keit, -schaft und -tion sind meist feminin.","Artikel: ___ Wohnung","Verwende ein feminines Nomen."),
("Neutrale Endungen","Verkleinerungen auf -chen/-lein und viele Wörter auf -ment sind neutral.","Artikel: ___ Brötchen","Verwende ein neutrales Nomen."),
("Unbestimmter Artikel","ein steht bei maskulinen und neutralen Nomen, eine bei femininen.","Ergänze: Das ist ___ Lampe.","Stelle einen neuen Gegenstand mit ein/eine vor."),
("Verneinung mit kein","kein wird wie ein dekliniert und verneint Nomen ohne bestimmten Artikel.","Verneine: Ich habe ein Auto.","Sage, dass du etwas nicht hast."),
("Artikel im Plural","Im Plural lautet der bestimmte Artikel die; einen unbestimmten Artikel gibt es nicht.","Ergänze: ___ Bücher sind interessant.","Sage etwas über mehrere Dinge."),
("Perfekt: Grundform","Das Perfekt besteht aus haben/sein und dem Partizip II am Satzende.","Setze ins Perfekt: Ich lerne Deutsch.","Erzähle von einer abgeschlossenen Handlung."),
("Partizip II regelmäßiger Verben","Meist gilt ge- + Stamm + -t: machen → gemacht.","Bilde das Partizip II von machen.","Erzähle mit einem regelmäßigen Verb von der Vergangenheit."),
("Partizip II unregelmäßiger Verben","Starke Verbformen müssen gelernt werden: schreiben → geschrieben.","Bilde das Partizip II von schreiben.","Verwende ein starkes Verb im Perfekt."),
("Perfekt mit haben","Die meisten transitiven und reflexiven Verben bilden das Perfekt mit haben.","Ergänze: Ich ___ einen Film gesehen.","Erzähle, was du gemacht oder gesehen hast."),
("Perfekt mit sein","Verben der Bewegung und Zustandsänderung bilden das Perfekt oft mit sein.","Ergänze: Wir ___ nach Köln gefahren.","Erzähle von einer Bewegung in der Vergangenheit."),
("Trennbare Verben im Perfekt","ge steht zwischen Vorsilbe und Stamm: aufstehen → aufgestanden.","Bilde das Partizip II von aufstehen.","Erzähle mit einem trennbaren Verb von der Vergangenheit."),
("Untrennbare Vorsilben","Nach be-, er-, ver-, ent- und zer- steht kein ge-.","Bilde das Partizip II von bezahlen.","Verwende ein untrennbares Verb im Perfekt."),
("Wortstellung im Perfekt","Im Hauptsatz steht haben/sein an Position zwei und das Partizip II am Ende.","Ordne: gestern / ich / lange / gearbeitet / habe","Erzähle, was du gestern gemacht hast."),
("Abschluss: über Vergangenes erzählen","Verbinde Zeitangaben und Perfekt, um Ereignisse in Reihenfolge zu erzählen.","Übersetze: Zuerst stand ich auf, dann frühstückte ich.","Erzähle zwei vergangene Ereignisse in ihrer Reihenfolge."),
],
"en": [
("Verb position in main clauses","In a statement, the conjugated verb takes position two.","Put the words in order: heute / ich / Deutsch / lerne","Say what you are doing today."),
("Inversion after an opener","When time or place comes first, the subject follows the verb.","Put in order: am Montag / ich / zu Hause / arbeite","Describe your plan for a specific day."),
("W-questions","A question word is followed by the verb and then the subject.","Build the question: wann / du / nach Hause / kommst","Ask someone about a time."),
("Yes/no questions","Without a question word, the verb comes first.","Build the question: du / heute / Deutsch / lernst","Ask a yes/no question."),
("Modal verbs","The modal verb takes position two and the infinitive goes at the end.","Put in order: ich / heute / länger / arbeiten / kann","Say what you can or must do."),
("Separable verbs","The conjugated part takes position two and the prefix goes at the end.","Put in order: ich / um sieben Uhr / stehe / auf","Describe an action with a separable verb."),
("Clauses with weil","In a weil-clause, the conjugated verb goes at the end.","Join with weil: Ich lerne Deutsch. Ich lebe in Berlin.","Give a reason for an action."),
("Accusative: direct object","The accusative marks the direct target of an action.","Add the article: Ich sehe ___ Mann.","Say whom or what you see."),
("Dative: recipient","The dative answers the question wem?.","Add the article: Ich helfe ___ Mann.","Say whom you help."),
("geben: dative and accusative","With geben, the recipient is dative and the thing is accusative.","Complete: Ich gebe ___ Kind das Buch.","Say what you give and to whom."),
("Accusative prepositions","durch, für, gegen, ohne and um always take the accusative.","Complete: Das ist für ___ Bruder. (mein)","Say who something is for."),
("Dative prepositions","aus, bei, mit, nach, seit, von and zu always take the dative.","Complete: Ich fahre mit ___ Bus.","Say how or with whom you travel."),
("Dative personal pronouns","mir, dir, ihm, ihr, uns, euch and ihnen replace a dative object.","Replace dem Mann: Ich helfe ___.","Ask for help or say whom you help."),
("Two-way prepositions: where/where to","Wo? takes dative; wohin? takes accusative.","Wo? Das Bild hängt an ___ Wand.","Describe a position or direction."),
("Noun gender basics","Learn each article with its noun: der Tisch, die Lampe, das Buch.","Choose the article: ___ Buch","Name an object with the correct article."),
("Masculine endings","Nouns ending in -er, -ling and -ismus are often masculine.","Article: ___ Frühling","Use a masculine noun."),
("Feminine endings","Nouns ending in -ung, -heit, -keit, -schaft and -tion are usually feminine.","Article: ___ Wohnung","Use a feminine noun."),
("Neuter endings","Diminutives in -chen/-lein and many words in -ment are neuter.","Article: ___ Brötchen","Use a neuter noun."),
("Indefinite article","ein is used with masculine and neuter nouns; eine with feminine nouns.","Complete: Das ist ___ Lampe.","Introduce a new object with ein/eine."),
("Negation with kein","kein declines like ein and negates a noun without a definite article.","Make negative: Ich habe ein Auto.","Say that you do not have something."),
("Articles in the plural","The plural definite article is die; there is no indefinite plural article.","Complete: ___ Bücher sind interessant.","Say something about several objects."),
("Perfect tense: pattern","The perfect tense uses haben/sein and a past participle at the end.","Change to the perfect: Ich lerne Deutsch.","Describe a completed action."),
("Past participles: regular verbs","The usual pattern is ge- + stem + -t: machen → gemacht.","Give the past participle of machen.","Describe a past action with a regular verb."),
("Past participles: irregular verbs","Strong verb forms must be learned: schreiben → geschrieben.","Give the past participle of schreiben.","Use a strong verb in the perfect tense."),
("Perfect tense with haben","Most transitive and reflexive verbs form the perfect with haben.","Complete: Ich ___ einen Film gesehen.","Say what you did or saw."),
("Perfect tense with sein","Movement and change-of-state verbs often form the perfect with sein.","Complete: Wir ___ nach Köln gefahren.","Describe movement in the past."),
("Separable verbs in the perfect","ge goes between prefix and stem: aufstehen → aufgestanden.","Give the past participle of aufstehen.","Describe the past with a separable verb."),
("Inseparable prefixes","There is no ge- after be-, er-, ver-, ent- and zer-.","Give the past participle of bezahlen.","Use an inseparable verb in the perfect tense."),
("Word order in the perfect","In a main clause, haben/sein takes position two and the participle goes at the end.","Put in order: gestern / ich / lange / gearbeitet / habe","Say what you did yesterday."),
("Final practice: tell a past story","Link time markers and the perfect tense to put events in order.","Translate: First I got up, then I had breakfast.","Tell two past events in order."),
]}

def normalize_language(value: str | None) -> str:
    code = (value or "en").lower().split("-")[0]
    return code if code in ("de", "en", "ru") else "en"

def localize_lesson_content(content: dict, language: str) -> dict:
    lang = normalize_language(language)
    value = deepcopy(content)
    if lang == "ru":
        return value
    day = int(value.get("day") or 0)
    if not 1 <= day <= 30:
        return value
    title, rule, question, goal = LESSON_COPY[lang][day - 1]
    value.update({"title": title, "rule": rule, "objective": goal, "communication_goal": goal})
    value["recall_prompt"] = "Close the example, explain the rule in your own words, then make one new sentence." if lang == "en" else "Schließe das Beispiel, erkläre die Regel mit eigenen Worten und bilde einen neuen Satz."
    exercises = value.get("exercises") or []
    if exercises:
        exercises[0].update({"question": question, "hint": rule, "explanation": ("Rule: " if lang == "en" else "Regel: ") + rule})
    if len(exercises) > 1:
        exercises[1].update({"question": "Listen and write the sentence in German." if lang == "en" else "Höre zu und schreibe den Satz auf Deutsch.", "hint": "Identify the verb first, then reconstruct the remaining words." if lang == "en" else "Erkenne zuerst das Verb und ergänze dann den Rest.", "explanation": ("You heard: " if lang == "en" else "Du hast gehört: ") + str(exercises[1].get("answer", ""))})
    if len(exercises) > 2:
        exercises[2].update({"question": goal, "hint": "Use today's structure with your own details." if lang == "en" else "Nutze die Struktur mit eigenen Details.", "explanation": "Check the goal, then compare your grammar with the model." if lang == "en" else "Prüfe das Ziel und vergleiche deine Grammatik mit dem Modell."})
    if len(exercises) > 3:
        exercises[3].update({"question": "Say the model aloud. Keep the word order and endings." if lang == "en" else "Sprich das Modell laut. Achte auf Wortstellung und Endungen.", "explanation": "Repeat once calmly and clearly." if lang == "en" else "Wiederhole den Satz einmal ruhig und deutlich."})
    return value
