# backend/generate_lessons_full.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.lesson import Lesson

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
db = Session()

# ==========================================
# 50+ УРОКОВ ДЛЯ ВСЕХ УРОВНЕЙ
# ==========================================

lessons_data = [
    # ==========================================
    # УРОВЕНЬ A1 – 12 уроков
    # ==========================================
    {
        "level": "A1",
        "pillar": "grammar",
        "topic": "Спряжение глагола haben",
        "weak_point_tags": ["haben_conjugation"],
        "content": {
            "title": "Глагол haben — спряжение",
            "rule": "Глагол 'haben' (иметь) спрягается: ich habe, du hast, er/sie/es hat, wir haben, ihr habt, sie haben.",
            "examples": ["Ich habe einen Hund.", "Du hast ein Buch.", "Er hat eine Schwester."],
            "common_mistakes": ["❌ Ich hat einen Hund.", "✅ Ich habe einen Hund."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ einen Hund.", "answer": "habe"},
                {"type": "fill", "question": "Du ___ ein Buch.", "answer": "hast"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "grammar",
        "topic": "Спряжение глагола sein",
        "weak_point_tags": ["present_tense"],
        "content": {
            "title": "Глагол sein — спряжение",
            "rule": "Глагол 'sein' (быть): ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie sind.",
            "examples": ["Ich bin Student.", "Du bist groß.", "Er ist aus Berlin."],
            "common_mistakes": ["❌ Ich ist Student.", "✅ Ich bin Student."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ Student.", "answer": "bin"},
                {"type": "fill", "question": "Du ___ groß.", "answer": "bist"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "grammar",
        "topic": "Артикли (der/die/das)",
        "weak_point_tags": ["articles", "gender"],
        "content": {
            "title": "Определённые артикли",
            "rule": "der — мужской, die — женский, das — средний.",
            "examples": ["der Mann", "die Frau", "das Auto"],
            "common_mistakes": ["❌ das Tisch", "✅ der Tisch"],
            "exercises": [
                {"type": "fill", "question": "___ Auto ist neu.", "answer": "Das"},
                {"type": "fill", "question": "___ Frau ist schön.", "answer": "Die"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "grammar",
        "topic": "Порядок слов в главном предложении",
        "weak_point_tags": ["word_order"],
        "content": {
            "title": "Порядок слов",
            "rule": "Глагол всегда на втором месте: Ich gehe heute nach Hause.",
            "examples": ["Ich gehe heute nach Hause.", "Heute gehe ich nach Hause."],
            "common_mistakes": ["❌ Ich heute gehe nach Hause.", "✅ Ich gehe heute nach Hause."],
            "exercises": [
                {"type": "fill", "question": "___ ich heute nach Hause.", "answer": "Gehe"},
                {"type": "fill", "question": "Heute ___ ich nach Hause.", "answer": "gehe"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "vocabulary",
        "topic": "Семья (Familie)",
        "weak_point_tags": ["basic_vocabulary", "fruits"],
        "content": {
            "title": "Семья",
            "rule": "Vater (отец), Mutter (мать), Bruder (брат), Schwester (сестра), Sohn (сын), Tochter (дочь).",
            "examples": ["Das ist meine Mutter.", "Ich habe einen Bruder."],
            "common_mistakes": ["❌ Mein Mutter", "✅ Meine Mutter"],
            "exercises": [
                {"type": "fill", "question": "Das ist ___ Vater.", "answer": "mein"},
                {"type": "fill", "question": "Ich habe eine ___. (сестра)", "answer": "Schwester"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "vocabulary",
        "topic": "Еда и напитки (Essen und Trinken)",
        "weak_point_tags": ["fruits", "basic_vocabulary"],
        "content": {
            "title": "Еда и напитки",
            "rule": "das Brot (хлеб), der Käse (сыр), das Wasser (вода), der Saft (сок), der Kaffee (кофе).",
            "examples": ["Ich esse Brot.", "Trinkst du Wasser?"],
            "common_mistakes": ["❌ Ich trinke Brot.", "✅ Ich esse Brot."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ Brot. (essen)", "answer": "esse"},
                {"type": "fill", "question": "___ du Wasser? (trinken)", "answer": "Trinkst"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "vocabulary",
        "topic": "Цвета (Farben)",
        "weak_point_tags": ["basic_vocabulary", "fruits"],
        "content": {
            "title": "Цвета",
            "rule": "rot (красный), blau (синий), grün (зелёный), gelb (жёлтый), schwarz (чёрный), weiß (белый).",
            "examples": ["Das Auto ist rot.", "Der Himmel ist blau."],
            "common_mistakes": ["❌ Der Auto ist rot.", "✅ Das Auto ist rot."],
            "exercises": [
                {"type": "fill", "question": "Das Auto ist ___. (красный)", "answer": "rot"},
                {"type": "fill", "question": "Der Himmel ist ___. (синий)", "answer": "blau"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "vocabulary",
        "topic": "Приветствия (Begrüßung)",
        "weak_point_tags": ["basic_vocabulary"],
        "content": {
            "title": "Приветствия",
            "rule": "Hallo! (Привет!), Guten Morgen! (Доброе утро!), Tschüss! (Пока!), Auf Wiedersehen! (До свидания!).",
            "examples": ["Hallo, wie geht es dir?", "Guten Morgen, Herr Müller."],
            "common_mistakes": ["❌ Tschüss! (неформально)", "✅ Auf Wiedersehen! (формально)"],
            "exercises": [
                {"type": "fill", "question": "___! (Привет!)", "answer": "Hallo"},
                {"type": "fill", "question": "___! (До свидания!)", "answer": "Auf Wiedersehen"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "grammar",
        "topic": "Отрицание nicht",
        "weak_point_tags": ["word_order"],
        "content": {
            "title": "Отрицание nicht",
            "rule": "'nicht' ставится перед отрицаемым словом или в конце предложения.",
            "examples": ["Ich gehe nicht.", "Das ist nicht mein Buch."],
            "common_mistakes": ["❌ Ich nicht gehe.", "✅ Ich gehe nicht."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ gehe. (nicht)", "answer": "nicht"},
                {"type": "fill", "question": "Das ist ___ mein Buch. (nicht)", "answer": "nicht"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "pronunciation",
        "topic": "Произношение: ch (ich-Laut)",
        "weak_point_tags": ["pronunciation_ch"],
        "content": {
            "title": "Звук 'ch' — мягкий вариант",
            "rule": "После e, i, ä, ö, ü звук 'ch' произносится мягко (как 'х' в слове 'хитрый').",
            "examples": ["ich", "mich", "dich", "welche"],
            "common_mistakes": ["❌ ich — твёрдый х", "✅ ich — мягкий х"],
            "exercises": [
                {"type": "fill", "question": "Как произносится 'ich'?", "answer": "мягко"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "pronunciation",
        "topic": "Произношение: ch (ach-Laut)",
        "weak_point_tags": ["pronunciation_ch"],
        "content": {
            "title": "Звук 'ch' — твёрдый вариант",
            "rule": "После a, o, u звук 'ch' произносится твёрдо (как 'х' в слове 'хор').",
            "examples": ["acht", "Buch", "machen", "Tuch"],
            "common_mistakes": ["❌ ach — мягкий х", "✅ ach — твёрдый х"],
            "exercises": [
                {"type": "fill", "question": "Как произносится 'Buch'?", "answer": "твёрдо"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "listening",
        "topic": "Аудирование: приветствие",
        "weak_point_tags": ["listening_greetings"],
        "content": {
            "title": "Аудирование — приветствие",
            "rule": "Прослушайте диалог и ответьте на вопросы.",
            "examples": ["A: Guten Tag! Wie geht es Ihnen?", "B: Danke, gut! Und Ihnen?"],
            "common_mistakes": [],
            "exercises": [
                {"type": "listen", "question": "Как ответил собеседник?", "answer": "Danke, gut!"}
            ]
        },
        "xp_reward": 50
    },
    # ==========================================
    # УРОВЕНЬ A2 – 12 уроков
    # ==========================================
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Perfekt с sein",
        "weak_point_tags": ["perfekt_auxiliary", "verbs_of_movement"],
        "content": {
            "title": "Perfekt с sein",
            "rule": "Глаголы движения и изменения состояния образуют Perfekt с 'sein'.",
            "examples": ["Ich bin nach Berlin gefahren.", "Er ist um 8 Uhr aufgestanden."],
            "common_mistakes": ["❌ Ich habe nach Berlin gefahren.", "✅ Ich bin nach Berlin gefahren."],
            "exercises": [
                {"type": "fill", "question": "Gestern ___ ich früh ___ (aufstehen).", "answer": "bin ... aufgestanden"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Perfekt с haben",
        "weak_point_tags": ["perfekt_auxiliary"],
        "content": {
            "title": "Perfekt с haben",
            "rule": "Большинство глаголов образуют Perfekt с 'haben'.",
            "examples": ["Ich habe das Buch gelesen.", "Sie hat einen Brief geschrieben."],
            "common_mistakes": ["❌ Ich bin das Buch gelesen.", "✅ Ich habe das Buch gelesen."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ das Buch ___ (lesen).", "answer": "habe ... gelesen"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Модальные глаголы: können",
        "weak_point_tags": ["modal_verbs", "können"],
        "content": {
            "title": "Модальный глагол können",
            "rule": "ich kann, du kannst, er/sie/es kann, wir können, ihr könnt, sie können.",
            "examples": ["Ich kann Deutsch sprechen.", "Kannst du mir helfen?"],
            "common_mistakes": ["❌ Ich kann Deutsch spricht.", "✅ Ich kann Deutsch sprechen."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ Deutsch ___ (sprechen).", "answer": "kann ... sprechen"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Модальные глаголы: müssen",
        "weak_point_tags": ["modal_verbs"],
        "content": {
            "title": "Модальный глагол müssen",
            "rule": "ich muss, du musst, er/sie/es muss, wir müssen, ihr müsst, sie müssen.",
            "examples": ["Ich muss heute arbeiten.", "Musst du morgen kommen?"],
            "common_mistakes": ["❌ Ich muss Deutsch sprechen.", "✅ Ich muss Deutsch sprechen."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ heute arbeiten.", "answer": "muss"},
                {"type": "fill", "question": "___ du morgen kommen?", "answer": "Musst"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Dativ (дательный падеж)",
        "weak_point_tags": ["dative_case", "article_declension"],
        "content": {
            "title": "Dativ",
            "rule": "der → dem, die → der, das → dem, die (мн.) → den.",
            "examples": ["Ich gebe dem Mann das Buch.", "Sie hilft der Frau."],
            "common_mistakes": ["❌ Ich gebe den Mann das Buch.", "✅ Ich gebe dem Mann das Buch."],
            "exercises": [
                {"type": "fill", "question": "Ich gebe ___ Mann das Buch.", "answer": "dem"},
                {"type": "fill", "question": "Sie hilft ___ Frau.", "answer": "der"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Akkusativ (винительный падеж)",
        "weak_point_tags": ["dative_case"],
        "content": {
            "title": "Akkusativ",
            "rule": "der → den, die → die, das → das, die (мн.) → die.",
            "examples": ["Ich sehe den Mann.", "Ich liebe die Frau."],
            "common_mistakes": ["❌ Ich sehe der Mann.", "✅ Ich sehe den Mann."],
            "exercises": [
                {"type": "fill", "question": "Ich sehe ___ Mann.", "answer": "den"},
                {"type": "fill", "question": "Ich liebe ___ Frau.", "answer": "die"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Предлоги с Dativ (aus, bei, mit)",
        "weak_point_tags": ["prepositions_temporal"],
        "content": {
            "title": "Предлоги с Dativ",
            "rule": "aus, bei, mit, nach, seit, von, zu — всегда с Dativ.",
            "examples": ["Ich bin bei meiner Freundin.", "Sie kommt aus Deutschland."],
            "common_mistakes": ["❌ Ich bin bei meine Freundin.", "✅ Ich bin bei meiner Freundin."],
            "exercises": [
                {"type": "fill", "question": "Ich bin bei ___ Freundin.", "answer": "meiner"},
                {"type": "fill", "question": "Sie kommt aus ___. (Deutschland)", "answer": "Deutschland"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "vocabulary",
        "topic": "Транспорт (Verkehrsmittel)",
        "weak_point_tags": ["travel_vocabulary"],
        "content": {
            "title": "Транспорт",
            "rule": "mit dem Zug (поездом), mit dem Bus, mit dem Auto, zu Fuß (пешком).",
            "examples": ["Ich fahre mit dem Zug.", "Wir fahren mit dem Auto."],
            "common_mistakes": ["❌ Ich fahre mit Zug.", "✅ Ich fahre mit dem Zug."],
            "exercises": [
                {"type": "fill", "question": "Ich fahre ___ dem Zug.", "answer": "mit"},
                {"type": "fill", "question": "Wir fahren ___ Auto.", "answer": "mit dem"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "vocabulary",
        "topic": "В городе (In der Stadt)",
        "weak_point_tags": ["travel_vocabulary"],
        "content": {
            "title": "В городе",
            "rule": "der Bahnhof (вокзал), die Apotheke (аптека), das Kino (кино), das Restaurant (ресторан).",
            "examples": ["Wo ist der Bahnhof?", "Ich gehe ins Kino."],
            "common_mistakes": ["❌ Ich gehe in Kino.", "✅ Ich gehe ins Kino."],
            "exercises": [
                {"type": "fill", "question": "Wo ist der ___? (вокзал)", "answer": "Bahnhof"},
                {"type": "fill", "question": "Ich gehe ins ___. (кино)", "answer": "Kino"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "vocabulary",
        "topic": "Покупки (Einkaufen)",
        "weak_point_tags": ["basic_vocabulary"],
        "content": {
            "title": "Покупки",
            "rule": "der Laden (магазин), die Tasche (сумка), das Geld (деньги), der Preis (цена).",
            "examples": ["Ich kaufe eine Tasche.", "Wie viel kostet das?"],
            "common_mistakes": ["❌ Ich kaufe ein Tasche.", "✅ Ich kaufe eine Tasche."],
            "exercises": [
                {"type": "fill", "question": "Ich kaufe eine ___. (сумка)", "answer": "Tasche"},
                {"type": "fill", "question": "Wie viel kostet ___? (это)", "answer": "das"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "listening",
        "topic": "Аудирование: в кафе",
        "weak_point_tags": ["listening_cafe"],
        "content": {
            "title": "Аудирование — в кафе",
            "rule": "Прослушайте диалог в кафе.",
            "examples": ["A: Guten Tag! Was möchten Sie?", "B: Ich hätte gerne einen Kaffee."],
            "common_mistakes": [],
            "exercises": [
                {"type": "listen", "question": "Was möchte der Gast?", "answer": "Kaffee"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "pronunciation",
        "topic": "Произношение: sch и ch",
        "weak_point_tags": ["pronunciation_sch"],
        "content": {
            "title": "Звуки sch и ch",
            "rule": "'sch' — мягкий 'ш' (Schule), 'ch' — мягкий/твёрдый 'х'.",
            "examples": ["Schule", "Tisch", "Buch", "machen"],
            "common_mistakes": ["❌ Schule — 'ч'", "✅ Schule — 'ш'"],
            "exercises": [
                {"type": "fill", "question": "Как произносится 'Schule'?", "answer": "ш"}
            ]
        },
        "xp_reward": 50
    },
    # ==========================================
    # УРОВЕНЬ B1 – 12 уроков
    # ==========================================
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Passiv в настоящем времени",
        "weak_point_tags": ["passiv", "process_passive"],
        "content": {
            "title": "Passiv Präsens",
            "rule": "wird + Partizip II: Das Haus wird gebaut.",
            "examples": ["Das Haus wird gebaut.", "Der Brief wird geschrieben."],
            "common_mistakes": ["❌ Das Haus ist gebaut (Zustandspassiv)", "✅ Das Haus wird gebaut."],
            "exercises": [
                {"type": "fill", "question": "Das Haus ___ gebaut.", "answer": "wird"},
                {"type": "fill", "question": "Der Brief ___ geschrieben.", "answer": "wird"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Passiv в прошедшем времени",
        "weak_point_tags": ["passiv", "process_passive"],
        "content": {
            "title": "Passiv Präteritum",
            "rule": "wurde + Partizip II: Das Haus wurde gebaut.",
            "examples": ["Das Haus wurde gebaut.", "Der Brief wurde geschrieben."],
            "common_mistakes": ["❌ Das Haus ist gebaut worden.", "✅ Das Haus wurde gebaut."],
            "exercises": [
                {"type": "fill", "question": "Das Haus ___ gebaut.", "answer": "wurde"},
                {"type": "fill", "question": "Der Brief ___ geschrieben.", "answer": "wurde"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Konjunktiv II (вежливые просьбы)",
        "weak_point_tags": ["konjunktiv_ii", "polite_requests"],
        "content": {
            "title": "Konjunktiv II",
            "rule": "hätte, wäre, würde + инфинитив для вежливых просьб.",
            "examples": ["Ich hätte gern ein Glas Wasser.", "Würden Sie mir helfen?"],
            "common_mistakes": ["❌ Ich habe gern ein Glas Wasser.", "✅ Ich hätte gern ein Glas Wasser."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ gern ein Glas Wasser.", "answer": "hätte"},
                {"type": "fill", "question": "___ Sie mir helfen?", "answer": "Würden"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Konjunktiv II (гипотетические ситуации)",
        "weak_point_tags": ["konjunktiv_ii"],
        "content": {
            "title": "Konjunktiv II — гипотезы",
            "rule": "würde + инфинитив для выражения гипотетических ситуаций.",
            "examples": ["Wenn ich Zeit hätte, würde ich kommen.", "Ich würde gerne reisen."],
            "common_mistakes": ["❌ Wenn ich Zeit habe, würde ich kommen.", "✅ Wenn ich Zeit hätte, würde ich kommen."],
            "exercises": [
                {"type": "fill", "question": "Wenn ich Zeit hätte, ___ ich kommen.", "answer": "würde"},
                {"type": "fill", "question": "Ich ___ gerne reisen.", "answer": "würde"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Относительные придаточные (Relativsätze)",
        "weak_point_tags": ["relative_clauses", "relative_pronouns"],
        "content": {
            "title": "Относительные придаточные",
            "rule": "der, die, das — согласуются с определяемым словом.",
            "examples": ["Der Mann, der dort steht, ist mein Chef.", "Die Frau, die ich sehe, ist meine Lehrerin."],
            "common_mistakes": ["❌ Der Mann, den dort steht.", "✅ Der Mann, der dort steht."],
            "exercises": [
                {"type": "fill", "question": "Der Mann, ___ dort steht, ist mein Chef.", "answer": "der"},
                {"type": "fill", "question": "Die Frau, ___ ich sehe, ist meine Lehrerin.", "answer": "die"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Придаточные с dass и ob",
        "weak_point_tags": ["subordinate_clauses"],
        "content": {
            "title": "Придаточные с dass/ob",
            "rule": "'dass' — что, 'ob' — ли. Глагол в конце.",
            "examples": ["Ich weiß, dass er kommt.", "Ich weiß nicht, ob er kommt."],
            "common_mistakes": ["❌ Ich weiß, dass er kommt heute.", "✅ Ich weiß, dass er heute kommt."],
            "exercises": [
                {"type": "fill", "question": "Ich weiß, ___ er kommt.", "answer": "dass"},
                {"type": "fill", "question": "Ich weiß nicht, ___ er kommt.", "answer": "ob"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Придаточные причины (weil, da)",
        "weak_point_tags": ["subordinate_clauses"],
        "content": {
            "title": "Придаточные причины",
            "rule": "'weil' и 'da' — потому что, так как. Глагол в конце.",
            "examples": ["Ich bleibe zu Hause, weil ich krank bin.", "Da ich müde bin, gehe ich schlafen."],
            "common_mistakes": ["❌ weil ich bin krank.", "✅ weil ich krank bin."],
            "exercises": [
                {"type": "fill", "question": "Ich bleibe zu Hause, ___ ich krank bin.", "answer": "weil"},
                {"type": "fill", "question": "___ ich müde bin, gehe ich schlafen.", "answer": "Da"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "vocabulary",
        "topic": "Работа (Beruf)",
        "weak_point_tags": ["work_vocabulary", "finance"],
        "content": {
            "title": "Работа",
            "rule": "der Beruf (профессия), die Arbeit (работа), der Kollege (коллега), die Gehaltserhöhung (повышение зарплаты).",
            "examples": ["Mein Beruf ist Lehrer.", "Ich habe eine Gehaltserhöhung bekommen."],
            "common_mistakes": ["❌ Mein Beruf ist Lehrerin (для мужчины).", "✅ Mein Beruf ist Lehrer."],
            "exercises": [
                {"type": "fill", "question": "Mein ___ ist Lehrer.", "answer": "Beruf"},
                {"type": "fill", "question": "Ich habe eine ___ bekommen. (повышение зарплаты)", "answer": "Gehaltserhöhung"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "vocabulary",
        "topic": "Путешествия (Reisen)",
        "weak_point_tags": ["travel_vocabulary"],
        "content": {
            "title": "Путешествия",
            "rule": "das Hotel (отель), der Flug (перелёт), das Gepäck (багаж), der Koffer (чемодан).",
            "examples": ["Wir haben ein Hotel gebucht.", "Mein Koffer ist schwer."],
            "common_mistakes": ["❌ Wir haben ein Hotel buucht.", "✅ Wir haben ein Hotel gebucht."],
            "exercises": [
                {"type": "fill", "question": "Wir haben ein ___ gebucht. (отель)", "answer": "Hotel"},
                {"type": "fill", "question": "Mein ___ ist schwer. (чемодан)", "answer": "Koffer"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "vocabulary",
        "topic": "Здоровье (Gesundheit)",
        "weak_point_tags": ["basic_vocabulary"],
        "content": {
            "title": "Здоровье",
            "rule": "der Arzt (врач), die Krankheit (болезнь), die Apotheke (аптека), das Rezept (рецепт).",
            "examples": ["Ich muss zum Arzt gehen.", "Kannst du ein Rezept bekommen?"],
            "common_mistakes": ["❌ Ich muss zur Arzt gehen.", "✅ Ich muss zum Arzt gehen."],
            "exercises": [
                {"type": "fill", "question": "Ich muss zum ___ gehen. (врач)", "answer": "Arzt"},
                {"type": "fill", "question": "Kannst du ein ___ bekommen? (рецепт)", "answer": "Rezept"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "listening",
        "topic": "Аудирование: новости",
        "weak_point_tags": ["listening_news"],
        "content": {
            "title": "Аудирование — новости",
            "rule": "Прослушайте краткую новость.",
            "examples": ["Die Regierung hat ein neues Gesetz beschlossen."],
            "common_mistakes": [],
            "exercises": [
                {"type": "listen", "question": "Wer hat ein Gesetz beschlossen?", "answer": "Die Regierung"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "pronunciation",
        "topic": "Ударение в словах",
        "weak_point_tags": ["pronunciation_stress"],
        "content": {
            "title": "Ударение",
            "rule": "Ударение обычно на первом слоге: Krankenhaus (KRA-ken-haus), Fernseher (FERN-se-her).",
            "examples": ["Krankenhaus", "Fernseher", "Hauptbahnhof"],
            "common_mistakes": ["❌ Ударение на втором слоге", "✅ Ударение на первом слоге"],
            "exercises": [
                {"type": "fill", "question": "На какой слог ударение в 'Krankenhaus'?", "answer": "первый"}
            ]
        },
        "xp_reward": 50
    },
    # ==========================================
    # УРОВЕНЬ B2 – 8 уроков
    # ==========================================
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Konjunktiv I (косвенная речь)",
        "weak_point_tags": ["konjunktiv_i", "indirect_speech"],
        "content": {
            "title": "Konjunktiv I",
            "rule": "Используется для передачи чужих слов: Er sagte, er habe keine Zeit.",
            "examples": ["Er sagte, er habe keine Zeit.", "Sie meinte, sie sei müde."],
            "common_mistakes": ["❌ Er sagte, er hat keine Zeit.", "✅ Er sagte, er habe keine Zeit."],
            "exercises": [
                {"type": "fill", "question": "Er sagte, er ___ keine Zeit.", "answer": "habe"},
                {"type": "fill", "question": "Sie meinte, sie ___ müde.", "answer": "sei"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Предлоги с Genitiv",
        "weak_point_tags": ["genitive_prepositions", "advanced_prepositions"],
        "content": {
            "title": "Предлоги с Genitiv",
            "rule": "wegen, trotz, während, aufgrund — требуют Genitiv.",
            "examples": ["Wegen des Wetters bleiben wir zu Hause.", "Trotz der Kälte gehe ich spazieren."],
            "common_mistakes": ["❌ Wegen dem Wetter", "✅ Wegen des Wetters"],
            "exercises": [
                {"type": "fill", "question": "___ des Wetters bleiben wir zu Hause.", "answer": "Wegen"},
                {"type": "fill", "question": "___ der Kälte gehe ich spazieren.", "answer": "Trotz"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Придаточные цели (damit, um...zu)",
        "weak_point_tags": ["purpose_clauses"],
        "content": {
            "title": "Придаточные цели",
            "rule": "'damit' + Nebensatz, 'um...zu' + Infinitiv.",
            "examples": ["Ich lerne Deutsch, damit ich in Berlin arbeiten kann.", "Ich lerne Deutsch, um in Berlin zu arbeiten."],
            "common_mistakes": ["❌ Ich lerne Deutsch, um ich in Berlin arbeite.", "✅ Ich lerne Deutsch, um in Berlin zu arbeiten."],
            "exercises": [
                {"type": "fill", "question": "Ich lerne Deutsch, ___ ich in Berlin arbeiten kann.", "answer": "damit"},
                {"type": "fill", "question": "Ich lerne Deutsch, ___ in Berlin zu arbeiten.", "answer": "um"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Уступительные предложения (obwohl)",
        "weak_point_tags": ["conjunctions", "concession"],
        "content": {
            "title": "Уступительные предложения",
            "rule": "'obwohl' — хотя. Глагол в конце.",
            "examples": ["Obwohl er krank ist, geht er zur Arbeit."],
            "common_mistakes": ["❌ Obwohl er ist krank.", "✅ Obwohl er krank ist."],
            "exercises": [
                {"type": "fill", "question": "___ er krank ist, geht er zur Arbeit.", "answer": "Obwohl"},
                {"type": "fill", "question": "Sie kommt, ___ sie müde ist.", "answer": "obwohl"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "vocabulary",
        "topic": "Абстрактные существительные",
        "weak_point_tags": ["abstract_nouns", "academic_vocabulary"],
        "content": {
            "title": "Абстрактные существительные",
            "rule": "die Folge (последствие), die Ursache (причина), die Wirkung (эффект).",
            "examples": ["Die Folge des Unfalls war schlimm.", "Die Ursache ist unbekannt."],
            "common_mistakes": ["❌ Das Folge", "✅ Die Folge"],
            "exercises": [
                {"type": "fill", "question": "Die ___ des Unfalls war schlimm.", "answer": "Folge"},
                {"type": "fill", "question": "Die ___ ist unbekannt.", "answer": "Ursache"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "vocabulary",
        "topic": "Прилагательные для описания",
        "weak_point_tags": ["adjectives", "descriptive"],
        "content": {
            "title": "Прилагательные",
            "rule": "intelligent (умный), kreativ (креативный), geduldig (терпеливый), zuverlässig (надёжный).",
            "examples": ["Sie ist sehr intelligent.", "Er ist zuverlässig."],
            "common_mistakes": ["❌ Sie ist sehr intelligent.", "✅ Sie ist sehr intelligent."],
            "exercises": [
                {"type": "fill", "question": "Sie ist sehr ___ (умная).", "answer": "intelligent"},
                {"type": "fill", "question": "Er ist ___ (надёжный).", "answer": "zuverlässig"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "listening",
        "topic": "Аудирование: политика",
        "weak_point_tags": ["listening_politics"],
        "content": {
            "title": "Аудирование — политика",
            "rule": "Прослушайте новость о политике.",
            "examples": ["Der Bundeskanzler hat eine Rede gehalten."],
            "common_mistakes": [],
            "exercises": [
                {"type": "listen", "question": "Wer hat eine Rede gehalten?", "answer": "Der Bundeskanzler"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "pronunciation",
        "topic": "Произношение иностранных слов",
        "weak_point_tags": ["pronunciation_foreign"],
        "content": {
            "title": "Иностранные слова",
            "rule": "Слова из французского и английского сохраняют своё произношение.",
            "examples": ["Restaurant (re-sto-ran)", "Computer (com-pju-ter)"],
            "common_mistakes": ["❌ Restaurant — 'ресторант'", "✅ Restaurant — 'ресторан'"],
            "exercises": [
                {"type": "fill", "question": "Как произносится 'Restaurant'?", "answer": "ресторан"}
            ]
        },
        "xp_reward": 50
    },
    # ==========================================
    # УРОВЕНЬ C1 – 6 уроков
    # ==========================================
    {
        "level": "C1",
        "pillar": "grammar",
        "topic": "Номинальный стиль (Nominalstil)",
        "weak_point_tags": ["nominal_style", "abstract_nouns"],
        "content": {
            "title": "Номинальный стиль",
            "rule": "Замена глаголов на абстрактные существительные: Die Lösung des Problems.",
            "examples": ["Die Lösung des Problems erfordert Geduld."],
            "common_mistakes": ["❌ Das Problem lösen erfordert Geduld.", "✅ Die Lösung des Problems erfordert Geduld."],
            "exercises": [
                {"type": "fill", "question": "Die ___ des Problems erfordert Geduld.", "answer": "Lösung"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "C1",
        "pillar": "grammar",
        "topic": "Futur II (будущее время)",
        "weak_point_tags": ["complex_tenses"],
        "content": {
            "title": "Futur II",
            "rule": "wird + Partizip II + haben/sein: Bis morgen werde ich das Buch gelesen haben.",
            "examples": ["Bis morgen werde ich das Buch gelesen haben."],
            "common_mistakes": ["❌ Bis morgen ich werde das Buch gelesen haben.", "✅ Bis morgen werde ich das Buch gelesen haben."],
            "exercises": [
                {"type": "fill", "question": "Bis morgen ___ ich das Buch gelesen haben.", "answer": "werde"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "C1",
        "pillar": "grammar",
        "topic": "Plusquamperfekt (предпрошедшее время)",
        "weak_point_tags": ["complex_tenses"],
        "content": {
            "title": "Plusquamperfekt",
            "rule": "hatte/war + Partizip II: Ich hatte das Buch gelesen, bevor er kam.",
            "examples": ["Ich hatte das Buch gelesen, bevor er kam."],
            "common_mistakes": ["❌ Ich habe das Buch gelesen, bevor er kam.", "✅ Ich hatte das Buch gelesen, bevor er kam."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ das Buch gelesen, bevor er kam.", "answer": "hatte"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "C1",
        "pillar": "vocabulary",
        "topic": "Формальные выражения",
        "weak_point_tags": ["formal_vocabulary", "academic_vocabulary"],
        "content": {
            "title": "Формальные выражения",
            "rule": "in Anbetracht (учитывая), aufgrund (на основании), hinsichtlich (относительно).",
            "examples": ["In Anbetracht der Situation...", "Hinsichtlich des Projekts..."],
            "common_mistakes": ["❌ In Anbetracht von der Situation", "✅ In Anbetracht der Situation"],
            "exercises": [
                {"type": "fill", "question": "___ der Situation...", "answer": "In Anbetracht"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "C1",
        "pillar": "vocabulary",
        "topic": "Сложные идиомы",
        "weak_point_tags": ["idioms", "advanced_expressions"],
        "content": {
            "title": "Сложные идиомы",
            "rule": "etwas auf die leichte Schulter nehmen (не относиться серьёзно), die Katze im Sack kaufen (кот в мешке).",
            "examples": ["Nimm das Problem nicht auf die leichte Schulter!"],
            "common_mistakes": ["❌ Ich habe die Katze im Sack gekauft.", "✅ Ich habe die Katze im Sack gekauft."],
            "exercises": [
                {"type": "fill", "question": "Nimm das Problem nicht auf die ___ Schulter!", "answer": "leichte"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "C1",
        "pillar": "listening",
        "topic": "Аудирование: лекция",
        "weak_point_tags": ["listening_lecture"],
        "content": {
            "title": "Аудирование — лекция",
            "rule": "Прослушайте отрывок из лекции.",
            "examples": ["Die Wissenschaft hat in den letzten Jahren große Fortschritte gemacht."],
            "common_mistakes": [],
            "exercises": [
                {"type": "listen", "question": "Welche Fortschritte wurden gemacht?", "answer": "wissenschaftliche Fortschritte"}
            ]
        },
        "xp_reward": 50
    },
]

# ==========================================
# ЗАГРУЗКА В БД
# ==========================================

print("📚 Добавление уроков...")
count = 0
for lesson in lessons_data:
    existing = db.query(Lesson).filter(Lesson.topic == lesson["topic"]).first()
    if not existing:
        db.add(Lesson(**lesson))
        count += 1
        print(f"➕ Добавлен: {lesson['topic']} ({lesson['level']})")
    else:
        print(f"⏩ Урок '{lesson['topic']}' уже существует.")

db.commit()
print(f"\n✅ Добавлено {count} новых уроков. Всего в БД: {db.query(Lesson).count()} уроков.")

