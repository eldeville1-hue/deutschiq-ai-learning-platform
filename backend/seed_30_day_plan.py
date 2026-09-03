"""Добавляет/обновляет оригинальный 30-дневный roadmap DeutschIQ."""
from app.core.database import SessionLocal
from app.models.lesson import Lesson


CURRICULUM = [
    # Неделя 1 — Satzbau
    (1, "Позиция глагола в главном предложении", "В повествовательном предложении спрягаемый глагол стоит на втором месте.", "word_order", "Heute lerne ich Deutsch.", "Поставьте слова правильно: heute / ich / Deutsch / lerne", "Heute lerne ich Deutsch."),
    (2, "Инверсия после обстоятельства", "Если предложение начинается со времени или места, подлежащее идёт после глагола.", "word_order", "Am Montag arbeite ich zu Hause.", "Составьте: am Montag / ich / zu Hause / arbeite", "Am Montag arbeite ich zu Hause."),
    (3, "Вопросы с вопросительным словом", "После вопросительного слова идёт глагол, затем подлежащее.", "word_order", "Wann kommst du nach Hause?", "Составьте вопрос: wann / du / nach Hause / kommst", "Wann kommst du nach Hause?"),
    (4, "Да/нет-вопросы", "В вопросе без вопросительного слова глагол занимает первое место.", "word_order", "Lernst du heute Deutsch?", "Составьте вопрос: du / heute / Deutsch / lernst", "Lernst du heute Deutsch?"),
    (5, "Модальные глаголы", "Модальный глагол стоит на втором месте, смысловой инфинитив — в конце.", "modal_verbs", "Ich kann heute länger arbeiten.", "Составьте: ich / heute / länger / arbeiten / kann", "Ich kann heute länger arbeiten."),
    (6, "Отделяемые приставки", "Спрягаемая часть стоит на втором месте, приставка — в конце.", "word_order", "Ich stehe jeden Tag um sieben Uhr auf.", "Составьте: ich / um sieben Uhr / aufstehe", "Ich stehe um sieben Uhr auf."),
    (7, "Придаточные с weil", "В придаточном предложении с weil спрягаемый глагол стоит в конце.", "subordinate_clauses", "Ich lerne Deutsch, weil ich in Berlin lebe.", "Соедините с weil: Ich lerne Deutsch. Ich lebe in Berlin.", "Ich lerne Deutsch, weil ich in Berlin lebe."),
    # Неделя 2 — Dativ/Akkusativ
    (8, "Akkusativ: прямой объект", "Akkusativ обозначает предмет или человека, на которого направлено действие.", "dative_case", "Ich sehe den Mann.", "Вставьте артикль: Ich sehe ___ Mann.", "den"),
    (9, "Dativ: получатель действия", "Dativ отвечает на вопросы wem? — кому? чему?", "dative_case", "Ich helfe dem Mann.", "Вставьте артикль: Ich helfe ___ Mann.", "dem"),
    (10, "geben: Dativ + Akkusativ", "С geben получатель стоит в Dativ, а предмет — в Akkusativ.", "dative_case", "Ich gebe dem Kind das Buch.", "Вставьте: Ich gebe ___ Kind das Buch.", "dem"),
    (11, "Предлоги с Akkusativ", "durch, für, gegen, ohne и um всегда требуют Akkusativ.", "prepositions", "Das Geschenk ist für meinen Bruder.", "Вставьте: Das ist für ___ Bruder. (mein)", "meinen"),
    (12, "Предлоги с Dativ", "aus, bei, mit, nach, seit, von и zu всегда требуют Dativ.", "prepositions", "Ich fahre mit dem Bus.", "Вставьте: Ich fahre mit ___ Bus.", "dem"),
    (13, "Личные местоимения в Dativ", "mir, dir, ihm, ihr, uns, euch, ihnen/Ihnen заменяют объект в Dativ.", "dative_pronouns", "Kannst du mir helfen?", "Замените dem Mann: Ich helfe ___.", "ihm"),
    (14, "Wechselpräpositionen: wo/wohin", "Wo? требует Dativ; wohin? требует Akkusativ.", "dative_case", "Das Buch liegt auf dem Tisch. Ich lege es auf den Tisch.", "Wo? Das Bild hängt an ___ Wand.", "der"),
    # Неделя 3 — Artikel
    (15, "Род существительных: основы", "Артикль нужно учить вместе с существительным: der Tisch, die Lampe, das Buch.", "articles", "Das Buch liegt auf dem Tisch.", "Выберите артикль: ___ Buch", "das"),
    (16, "Мужской род по окончаниям", "Существительные на -er, -ling, -ismus часто мужского рода.", "articles", "der Lehrer, der Frühling, der Tourismus", "Артикль: ___ Frühling", "der"),
    (17, "Женский род по окончаниям", "Существительные на -ung, -heit, -keit, -schaft, -tion обычно женского рода.", "articles", "die Wohnung, die Freiheit, die Möglichkeit", "Артикль: ___ Wohnung", "die"),
    (18, "Средний род по окончаниям", "Уменьшительные на -chen/-lein и многие слова на -ment имеют das.", "articles", "das Mädchen, das Brötchen, das Instrument", "Артикль: ___ Brötchen", "das"),
    (19, "Неопределённый артикль", "ein используется с мужским и средним родом, eine — с женским.", "articles", "Das ist ein Tisch und eine Lampe.", "Вставьте: Das ist ___ Lampe.", "eine"),
    (20, "Отрицание kein", "kein склоняется как ein и отрицает существительное без определённого артикля.", "articles", "Ich habe kein Auto.", "Отрицайте: Ich habe ein Auto.", "Ich habe kein Auto."),
    (21, "Артикли во множественном числе", "Во множественном числе определённый артикль — die; неопределённого артикля нет.", "articles", "Die Bücher sind neu.", "Вставьте: ___ Bücher sind interessant.", "Die"),
    # Неделя 4 — Perfekt
    (22, "Perfekt: формула", "Perfekt образуется из haben/sein и Partizip II в конце предложения.", "perfekt_auxiliary", "Ich habe Deutsch gelernt.", "Преобразуйте: Ich lerne Deutsch.", "Ich habe Deutsch gelernt."),
    (23, "Partizip II правильных глаголов", "Обычно используется ge- + основа + -t: machen → gemacht.", "participles", "Wir haben die Aufgabe gemacht.", "Partizip II от machen", "gemacht"),
    (24, "Partizip II неправильных глаголов", "Форму сильного глагола нужно учить: schreiben → geschrieben.", "participles", "Sie hat eine E-Mail geschrieben.", "Partizip II от schreiben", "geschrieben"),
    (25, "Perfekt с haben", "Большинство переходных и возвратных глаголов образуют Perfekt с haben.", "perfekt_auxiliary", "Ich habe einen Film gesehen.", "Вставьте: Ich ___ einen Film gesehen.", "habe"),
    (26, "Perfekt с sein", "Глаголы перемещения и изменения состояния часто образуют Perfekt с sein.", "verbs_of_movement", "Wir sind nach Köln gefahren.", "Вставьте: Wir ___ nach Köln gefahren.", "sind"),
    (27, "Отделяемые глаголы в Perfekt", "ge ставится между приставкой и основой: aufstehen → aufgestanden.", "participles", "Ich bin früh aufgestanden.", "Partizip II от aufstehen", "aufgestanden"),
    (28, "Неотделяемые приставки", "После be-, er-, ver-, ent-, zer- частица ge- не используется.", "participles", "Er hat die Rechnung bezahlt.", "Partizip II от bezahlen", "bezahlt"),
    (29, "Порядок слов в Perfekt", "В главном предложении haben/sein стоит на втором месте, Partizip II — в конце.", "word_order", "Gestern habe ich lange gearbeitet.", "Составьте: gestern / ich / lange / gearbeitet / habe", "Gestern habe ich lange gearbeitet."),
    (30, "Финальная тренировка: рассказ о прошлом", "Соединяйте временные маркеры и Perfekt, чтобы рассказывать о событиях последовательно.", "perfekt_auxiliary", "Zuerst bin ich aufgestanden, dann habe ich gefrühstückt.", "Переведите: Сначала я встал, затем позавтракал.", "Zuerst bin ich aufgestanden, dann habe ich gefrühstückt."),
]

# У каждого дня есть собственная коммуникативная цель и диагностическая ошибка.
# Это не декоративный текст: target_patterns используются fallback-проверкой свободной фразы.
LESSON_DETAILS = {
    1: ("❌ Ich heute Deutsch lerne.", "✅ Ich lerne heute Deutsch.", "Расскажи, что ты делаешь сегодня.", ["lerne", "mache", "arbeite"]),
    2: ("❌ Am Montag ich arbeite zu Hause.", "✅ Am Montag arbeite ich zu Hause.", "Опиши свой план на конкретный день.", ["montag", "heute", "morgen"]),
    3: ("❌ Wann du kommst nach Hause?", "✅ Wann kommst du nach Hause?", "Задай собеседнику вопрос о времени.", ["wann", "kommst", "gehst"]),
    4: ("❌ Du lernst heute Deutsch?", "✅ Lernst du heute Deutsch?", "Задай вопрос, на который отвечают ja или nein.", ["du"]),
    5: ("❌ Ich kann spreche Deutsch.", "✅ Ich kann Deutsch sprechen.", "Скажи, что ты можешь или должен сделать.", ["kann", "muss", "will"]),
    6: ("❌ Ich aufstehe um sieben Uhr.", "✅ Ich stehe um sieben Uhr auf.", "Опиши действие с отделяемым глаголом.", ["auf", "ein", "an"]),
    7: ("❌ Weil ich bin müde.", "✅ Weil ich müde bin.", "Объясни причину своего действия.", ["weil"]),
    8: ("❌ Ich sehe der Mann.", "✅ Ich sehe den Mann.", "Скажи, кого или что ты видишь.", ["den", "einen"]),
    9: ("❌ Ich helfe den Mann.", "✅ Ich helfe dem Mann.", "Скажи, кому ты помогаешь.", ["dem", "einem", "mir", "dir"]),
    10: ("❌ Ich gebe das Kind dem Buch.", "✅ Ich gebe dem Kind das Buch.", "Скажи, кому и что ты даёшь.", ["gebe", "gibst", "dem"]),
    11: ("❌ Das Geschenk ist für meinem Bruder.", "✅ Das Geschenk ist für meinen Bruder.", "Скажи, для кого предназначена вещь.", ["für", "ohne", "durch"]),
    12: ("❌ Ich fahre mit den Bus.", "✅ Ich fahre mit dem Bus.", "Расскажи, на чём или с кем ты едешь.", ["mit", "nach", "zu"]),
    13: ("❌ Kannst du ich helfen?", "✅ Kannst du mir helfen?", "Попроси о помощи или скажи, кому помогаешь.", ["mir", "dir", "ihm", "ihr"]),
    14: ("❌ Ich lege das Buch auf dem Tisch.", "✅ Ich lege das Buch auf den Tisch.", "Опиши положение или направление предмета.", ["auf", "in", "an"]),
    15: ("❌ die Buch", "✅ das Buch", "Назови предмет вместе с правильным артиклем.", ["der", "die", "das"]),
    16: ("❌ die Frühling", "✅ der Frühling", "Используй существительное мужского рода.", ["der"]),
    17: ("❌ das Wohnung", "✅ die Wohnung", "Опиши существительное женского рода.", ["die"]),
    18: ("❌ der Mädchen", "✅ das Mädchen", "Используй существительное среднего рода.", ["das"]),
    19: ("❌ Das ist ein Lampe.", "✅ Das ist eine Lampe.", "Представь новый предмет через ein/eine.", ["ein", "eine"]),
    20: ("❌ Ich habe nicht Auto.", "✅ Ich habe kein Auto.", "Скажи, что у тебя чего-то нет.", ["kein", "keine", "keinen"]),
    21: ("❌ Die Büchers sind neu.", "✅ Die Bücher sind neu.", "Скажи что-нибудь о нескольких предметах.", ["die", "sind"]),
    22: ("❌ Ich Deutsch gelernt habe.", "✅ Ich habe Deutsch gelernt.", "Расскажи о завершённом действии.", ["habe", "bin"]),
    23: ("❌ Ich habe die Aufgabe gemachen.", "✅ Ich habe die Aufgabe gemacht.", "Расскажи о действии правильного глагола в прошлом.", ["gemacht", "gelernt", "gearbeitet"]),
    24: ("❌ Sie hat eine E-Mail geschreibt.", "✅ Sie hat eine E-Mail geschrieben.", "Используй сильный глагол в Perfekt.", ["geschrieben", "gesehen", "gelesen"]),
    25: ("❌ Ich bin einen Film gesehen.", "✅ Ich habe einen Film gesehen.", "Расскажи, что ты делал или видел.", ["habe", "hat"]),
    26: ("❌ Wir haben nach Köln gefahren.", "✅ Wir sind nach Köln gefahren.", "Расскажи о перемещении в прошлом.", ["bin", "bist", "ist", "sind"]),
    27: ("❌ Ich bin geaufstanden.", "✅ Ich bin aufgestanden.", "Расскажи о прошлом с отделяемым глаголом.", ["aufgestanden", "eingekauft", "angerufen"]),
    28: ("❌ Er hat die Rechnung gebezaht.", "✅ Er hat die Rechnung bezahlt.", "Используй неотделяемый глагол в Perfekt.", ["bezahlt", "verkauft", "erzählt"]),
    29: ("❌ Gestern ich habe lange gearbeitet.", "✅ Gestern habe ich lange gearbeitet.", "Расскажи, что ты делал вчера.", ["gestern", "habe", "bin"]),
    30: ("❌ Zuerst ich bin aufgestanden.", "✅ Zuerst bin ich aufgestanden.", "Расскажи о двух событиях прошлого по порядку.", ["zuerst", "dann"]),
}


def build_content(day, topic, rule, example, question, answer):
    week = min((day - 1) // 7 + 1, 4)
    wrong, correction, communication_goal, target_patterns = LESSON_DETAILS[day]
    return {
        "day": day,
        "week": week,
        "title": f"Tag {day}: {topic}",
        "objective": communication_goal,
        "communication_goal": communication_goal,
        "rule": rule,
        "examples": [example, correction.removeprefix("✅ ")],
        "audio_text": example,
        "cefr": "A2" if day <= 21 else "B1",
        "prerequisites": [] if day == 1 else [CURRICULUM[day - 2][3]],
        "common_mistakes": [wrong, correction],
        "recall_prompt": "Закрой пример и скажи правило своими словами. Затем придумай один новый элемент для своей фразы.",
        "exercises": [
            {"type": "fill", "stage": "guided", "question": question, "answer": answer, "accepted_answers": [answer], "hint": rule, "explanation": f"Правило: {rule}"},
            {"type": "reorder", "stage": "independent", "question": "Соберите предложение в правильном порядке.", "tokens": example.rstrip(".?!").split(), "answer": example, "accepted_answers": [example, example.rstrip(".?!")], "explanation": "Спрягаемый глагол и остальные части предложения должны занимать позиции по правилу урока."},
            {"type": "production", "stage": "transfer", "question": communication_goal, "answer": example, "model_answer": example, "accepted_answers": [example, example.rstrip(".?!")], "target_patterns": target_patterns, "hint": "Используй структуру урока, но выбери собственные детали.", "explanation": "Проверь, выполнена ли коммуникативная цель, затем сравни грамматику с моделью."},
        ],
    }


def seed():
    db = SessionLocal()
    try:
        for day, topic, rule, tag, example, question, answer in CURRICULUM:
            content = build_content(day, topic, rule, example, question, answer)
            existing = db.query(Lesson).filter(Lesson.topic == topic).first()
            if existing:
                existing.level = "A2" if day <= 21 else "B1"
                existing.pillar = "grammar"
                existing.weak_point_tags = [tag]
                existing.content = content
                existing.estimated_time = 15
                existing.is_active = True
            else:
                db.add(Lesson(
                    level="A2" if day <= 21 else "B1",
                    pillar="grammar",
                    topic=topic,
                    weak_point_tags=[tag],
                    content=content,
                    xp_reward=50,
                    estimated_time=15,
                    is_active=True,
                ))
        db.commit()
        print("✅ 30-дневный roadmap добавлен: 30 уроков, 90 упражнений")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
