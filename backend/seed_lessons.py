# backend/seed_lessons.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.lesson import Lesson

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
db = Session()

lessons_data = [
    # ============================= УРОВЕНЬ A1 =============================
    # Грамматика A1
    {
        "level": "A1",
        "pillar": "grammar",
        "topic": "Спряжение глагола haben",
        "weak_point_tags": ["haben_conjugation"],
        "content": {
            "title": "Глагол haben — спряжение в настоящем времени",
            "rule": "Глагол 'haben' (иметь) спрягается по лицам. В 1-м лице ед.ч. — 'habe', во 2-м — 'hast', в 3-м — 'hat'.",
            "examples": [
                "Ich habe einen Hund.",
                "Du hast ein Buch.",
                "Er hat eine Schwester."
            ],
            "common_mistakes": [
                "❌ Ich hat einen Hund.",
                "✅ Ich habe einen Hund."
            ],
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
            "title": "Глагол sein — спряжение в настоящем времени",
            "rule": "Глагол 'sein' (быть) — неправильный, но очень частотный. Запомните формы: ich bin, du bist, er/sie/es ist.",
            "examples": [
                "Ich bin Student.",
                "Du bist groß.",
                "Sie ist aus Berlin."
            ],
            "common_mistakes": [
                "❌ Ich ist Student.",
                "✅ Ich bin Student."
            ],
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
        "topic": "Порядок слов в простом предложении (главное предложение)",
        "weak_point_tags": ["word_order", "main_clause"],
        "content": {
            "title": "Порядок слов в главном предложении",
            "rule": "В главном предложении глагол стоит на втором месте. Подлежащее обычно на первом, но может быть и другой член предложения.",
            "examples": [
                "Ich gehe heute nach Hause.",
                "Heute gehe ich nach Hause.",
                "Nach Hause gehe ich heute."
            ],
            "common_mistakes": [
                "❌ Ich heute gehe nach Hause.",
                "✅ Ich gehe heute nach Hause."
            ],
            "exercises": [
                {"type": "fill", "question": "___ ich heute nach Hause.", "answer": "Gehe"},
                {"type": "fill", "question": "Heute ___ ich nach Hause.", "answer": "gehe"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A1",
        "pillar": "grammar",
        "topic": "Артикли (определённый и неопределённый)",
        "weak_point_tags": ["articles", "gender"],
        "content": {
            "title": "Артикли — der/die/das",
            "rule": "В немецком языке каждый существительный имеет род: мужской (der), женский (die) или средний (das). Артикль нужно запоминать вместе со словом.",
            "examples": [
                "der Tisch (стол)",
                "die Lampe (лампа)",
                "das Buch (книга)"
            ],
            "common_mistakes": [
                "❌ das Tisch",
                "✅ der Tisch"
            ],
            "exercises": [
                {"type": "fill", "question": "___ Buch (какой артикль?)", "answer": "das"},
                {"type": "fill", "question": "___ Lampe (какой артикль?)", "answer": "die"}
            ]
        },
        "xp_reward": 50
    },
    # Лексика A1
    {
        "level": "A1",
        "pillar": "vocabulary",
        "topic": "Семья (Familie)",
        "weak_point_tags": ["basic_vocabulary"],
        "content": {
            "title": "Слова по теме 'Семья'",
            "rule": "Запомните основные слова: Vater (отец), Mutter (мать), Bruder (брат), Schwester (сестра), Sohn (сын), Tochter (дочь).",
            "examples": [
                "Das ist meine Mutter.",
                "Ich habe einen Bruder.",
                "Meine Schwester ist jung."
            ],
            "common_mistakes": [
                "❌ Mein Mutter",
                "✅ Meine Mutter (женский род)"
            ],
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
        "weak_point_tags": ["fruits"],
        "content": {
            "title": "Еда и напитки",
            "rule": "Основные слова: das Brot (хлеб), der Käse (сыр), das Wasser (вода), der Saft (сок), der Kaffee (кофе).",
            "examples": [
                "Ich esse Brot.",
                "Trinkst du Wasser?",
                "Der Kaffee ist heiß."
            ],
            "common_mistakes": [
                "❌ Ich trinke Brot.",
                "✅ Ich esse Brot."
            ],
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
        "weak_point_tags": ["basic_vocabulary"],
        "content": {
            "title": "Цвета по-немецки",
            "rule": "rot (красный), blau (синий), grün (зелёный), gelb (жёлтый), schwarz (чёрный), weiß (белый).",
            "examples": [
                "Das Auto ist rot.",
                "Der Himmel ist blau.",
                "Die Blume ist gelb."
            ],
            "common_mistakes": [
                "❌ Der Auto ist rot.",
                "✅ Das Auto ist rot."
            ],
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
        "topic": "Приветствия и прощания",
        "weak_point_tags": ["basic_vocabulary"],
        "content": {
            "title": "Приветствия и прощания",
            "rule": "Hallo! (Привет!), Guten Morgen! (Доброе утро!), Tschüss! (Пока!), Auf Wiedersehen! (До свидания!).",
            "examples": [
                "Hallo, wie geht es dir?",
                "Guten Morgen, Herr Müller.",
                "Tschüss, bis morgen!"
            ],
            "common_mistakes": [
                "❌ Tschüss sagen mit 'Auf'",
                "✅ Tschüss! (неформально)"
            ],
            "exercises": [
                {"type": "fill", "question": "___! (Привет!)", "answer": "Hallo"},
                {"type": "fill", "question": "___! (До свидания!)", "answer": "Auf Wiedersehen"}
            ]
        },
        "xp_reward": 50
    },
    # ============================= УРОВЕНЬ A2 =============================
    # Грамматика A2
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Perfekt с sein",
        "weak_point_tags": ["perfekt_auxiliary", "verbs_of_movement"],
        "content": {
            "title": "Perfekt — вспомогательный глагол sein",
            "rule": "Глаголы движения (fahren, gehen, kommen, laufen) и изменения состояния (aufstehen, einschlafen) образуют Perfekt с 'sein'.",
            "examples": [
                "Ich bin nach Berlin gefahren.",
                "Er ist um 8 Uhr aufgestanden.",
                "Das Wetter ist schön geblieben."
            ],
            "common_mistakes": [
                "❌ Ich habe nach Berlin gefahren.",
                "✅ Ich bin nach Berlin gefahren."
            ],
            "exercises": [
                {"type": "fill", "question": "Gestern ___ ich früh ___ (aufstehen).", "answer": "bin ... aufgestanden"},
                {"type": "fill", "question": "Meine Eltern ___ nach Italien ___ (fliegen).", "answer": "sind ... geflogen"}
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
            "title": "Perfekt — вспомогательный глагол haben",
            "rule": "Большинство глаголов образуют Perfekt с 'haben'. Например: lesen, schreiben, machen, trinken.",
            "examples": [
                "Ich habe das Buch gelesen.",
                "Sie hat einen Brief geschrieben.",
                "Wir haben Kaffee getrunken."
            ],
            "common_mistakes": [
                "❌ Ich bin das Buch gelesen.",
                "✅ Ich habe das Buch gelesen."
            ],
            "exercises": [
                {"type": "fill", "question": "Ich ___ das Buch ___ (lesen).", "answer": "habe ... gelesen"},
                {"type": "fill", "question": "Sie ___ einen Brief ___ (schreiben).", "answer": "hat ... geschrieben"}
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
            "title": "Модальный глагол können (мочь, уметь)",
            "rule": "Спряжение: ich kann, du kannst, er/sie/es kann, wir können, ihr könnt, sie können. В предложении с модальным глаголом основной глагол стоит в инфинитиве в конце.",
            "examples": [
                "Ich kann Deutsch sprechen.",
                "Kannst du mir helfen?",
                "Er kann gut singen."
            ],
            "common_mistakes": [
                "❌ Ich kann Deutsch spricht.",
                "✅ Ich kann Deutsch sprechen."
            ],
            "exercises": [
                {"type": "fill", "question": "Ich ___ Deutsch ___ (sprechen).", "answer": "kann ... sprechen"},
                {"type": "fill", "question": "___ du mir helfen? (können)", "answer": "Kannst"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "grammar",
        "topic": "Dativ (падеж)",
        "weak_point_tags": ["dative_case", "article_declension"],
        "content": {
            "title": "Dativ — дательный падеж",
            "rule": "Dativ отвечает на вопрос 'кому?', 'чему?'. Артикли меняются: der → dem, die → der, das → dem, die (мн.) → den.",
            "examples": [
                "Ich gebe dem Mann das Buch.",
                "Sie hilft der Frau.",
                "Wir kaufen dem Kind ein Spielzeug."
            ],
            "common_mistakes": [
                "❌ Ich gebe den Mann das Buch.",
                "✅ Ich gebe dem Mann das Buch."
            ],
            "exercises": [
                {"type": "fill", "question": "Ich gebe ___ Mann das Buch. (der/dem)", "answer": "dem"},
                {"type": "fill", "question": "Sie hilft ___ Frau. (die/der)", "answer": "der"}
            ]
        },
        "xp_reward": 50
    },
    # Лексика A2
    {
        "level": "A2",
        "pillar": "vocabulary",
        "topic": "Предлоги места (in, auf, unter)",
        "weak_point_tags": ["prepositions_temporal"],
        "content": {
            "title": "Предлоги места с Dativ",
            "rule": "in (в), auf (на), unter (под) — требуют Dativ, если указывают местоположение.",
            "examples": [
                "Das Buch liegt auf dem Tisch.",
                "Ich bin in der Schule.",
                "Die Katze ist unter dem Bett."
            ],
            "common_mistakes": [
                "❌ auf den Tisch (Akkusativ)",
                "✅ auf dem Tisch (Dativ)"
            ],
            "exercises": [
                {"type": "fill", "question": "Das Buch liegt ___ (на) dem Tisch.", "answer": "auf"},
                {"type": "fill", "question": "Ich bin ___ (в) der Schule.", "answer": "in"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "A2",
        "pillar": "vocabulary",
        "topic": "Транспорт (Verkehrsmittel)",
        "weak_point_tags": ["travel_vocabulary", "airport"],
        "content": {
            "title": "Средства передвижения",
            "rule": "С транспортом используется предлог 'mit' + Dativ: mit dem Zug (поездом), mit dem Bus, mit dem Auto, zu Fuß (пешком).",
            "examples": [
                "Ich fahre mit dem Zug.",
                "Wir fahren mit dem Auto nach Berlin.",
                "Sie geht zu Fuß."
            ],
            "common_mistakes": [
                "❌ Ich fahre mit Zug.",
                "✅ Ich fahre mit dem Zug."
            ],
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
        "topic": "Еда (Lebensmittel)",
        "weak_point_tags": ["fruits"],
        "content": {
            "title": "Продукты питания",
            "rule": "der Kuchen (пирог), die Wurst (колбаса), das Ei (яйцо), der Reis (рис), das Gemüse (овощи).",
            "examples": [
                "Ich esse gerne Kuchen.",
                "Kaufst du Wurst?",
                "Gemüse ist gesund."
            ],
            "common_mistakes": [
                "❌ Ich esse gern der Kuchen.",
                "✅ Ich esse gerne Kuchen."
            ],
            "exercises": [
                {"type": "fill", "question": "Ich esse gerne ___ (пирог).", "answer": "Kuchen"},
                {"type": "fill", "question": "___ ist gesund. (овощи)", "answer": "Gemüse"}
            ]
        },
        "xp_reward": 50
    },
    # Произношение A2
    {
        "level": "A2",
        "pillar": "pronunciation",
        "topic": "Произношение: ch (ich-Laut vs ach-Laut)",
        "weak_point_tags": ["pronunciation_ch"],
        "content": {
            "title": "Звук 'ch' — два варианта",
            "rule": "После гласных e, i, ä, ö, ü — мягкий 'ich-Laut' (как х в слове 'хитрый'). После a, o, u — твёрдый 'ach-Laut' (как х в слове 'хор').",
            "examples": [
                "ich, mich, dich — мягкий",
                "acht, Buch, machen — твёрдый"
            ],
            "common_mistakes": [
                "❌ 'ich' произносить как 'ич' с твёрдым х",
                "✅ 'ich' — мягкий звук"
            ],
            "exercises": [
                {"type": "fill", "question": "Как произносится 'ich'? (мягкий/твёрдый)", "answer": "мягкий"},
                {"type": "fill", "question": "Как произносится 'Buch'? (мягкий/твёрдый)", "answer": "твёрдый"}
            ]
        },
        "xp_reward": 50
    },
    # ============================= УРОВЕНЬ B1 =============================
    # Грамматика B1
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Passiv (страдательный залог) в настоящем времени",
        "weak_point_tags": ["passiv", "process_passive"],
        "content": {
            "title": "Passiv — образование",
            "rule": "Passiv образуется с помощью 'werden' + Partizip II. В Präsens: wird + Partizip II.",
            "examples": [
                "Das Haus wird gebaut.",
                "Der Brief wird geschrieben.",
                "Die Tür wird geöffnet."
            ],
            "common_mistakes": [
                "❌ Das Haus ist gebaut (это Zustandspassiv)",
                "✅ Das Haus wird gebaut (Vorgangspassiv)"
            ],
            "exercises": [
                {"type": "fill", "question": "Das Haus ___ gebaut. (werden)", "answer": "wird"},
                {"type": "fill", "question": "Der Brief ___ geschrieben. (werden)", "answer": "wird"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Nebensätze: dass и ob",
        "weak_point_tags": ["subordinate_clauses"],
        "content": {
            "title": "Придаточные предложения с 'dass' и 'ob'",
            "rule": "Союз 'dass' — что, 'ob' — ли. Глагол в придаточном стоит в конце.",
            "examples": [
                "Ich weiß, dass er kommt.",
                "Ich weiß nicht, ob er kommt.",
                "Er sagt, dass sie heute arbeitet."
            ],
            "common_mistakes": [
                "❌ Ich weiß, dass er kommt heute.",
                "✅ Ich weiß, dass er heute kommt."
            ],
            "exercises": [
                {"type": "fill", "question": "Ich weiß, ___ er kommt. (dass/ob)", "answer": "dass"},
                {"type": "fill", "question": "Ich weiß nicht, ___ er kommt. (dass/ob)", "answer": "ob"}
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
            "title": "Konjunktiv II для вежливых просьб",
            "rule": "Используем 'hätte', 'wäre' или 'würde' + инфинитив для вежливых просьб и гипотетических ситуаций.",
            "examples": [
                "Ich hätte gern ein Glas Wasser.",
                "Würden Sie mir helfen?",
                "Wenn ich Zeit hätte, würde ich kommen."
            ],
            "common_mistakes": [
                "❌ Ich habe gern ein Glas Wasser.",
                "✅ Ich hätte gern ein Glas Wasser."
            ],
            "exercises": [
                {"type": "fill", "question": "Ich ___ gern ein Glas Wasser. (hätte/habe)", "answer": "hätte"},
                {"type": "fill", "question": "___ Sie mir helfen? (Würden/Werden)", "answer": "Würden"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Relativsätze (относительные придаточные)",
        "weak_point_tags": ["relative_clauses", "relative_pronouns"],
        "content": {
            "title": "Относительные придаточные",
            "rule": "Относительное местоимение согласуется в роде и числе с определяемым словом. Падеж зависит от функции в придаточном.",
            "examples": [
                "Der Mann, der dort steht, ist mein Chef.",
                "Die Frau, die ich sehe, ist meine Lehrerin.",
                "Das Buch, das ich lese, ist interessant."
            ],
            "common_mistakes": [
                "❌ Der Mann, den dort steht.",
                "✅ Der Mann, der dort steht."
            ],
            "exercises": [
                {"type": "fill", "question": "Der Mann, ___ dort steht, ist mein Chef. (der/den)", "answer": "der"},
                {"type": "fill", "question": "Die Frau, ___ ich sehe, ist meine Lehrerin. (die/der)", "answer": "die"}
            ]
        },
        "xp_reward": 50
    },
    # Лексика B1
    {
        "level": "B1",
        "pillar": "vocabulary",
        "topic": "Глаголы с предлогами (управление)",
        "weak_point_tags": ["work_vocabulary", "finance"],
        "content": {
            "title": "Глаголы с фиксированными предлогами",
            "rule": "Некоторые глаголы требуют определённого предлога: warten auf (ждать), sich freuen auf/über (радоваться), denken an (думать о).",
            "examples": [
                "Ich warte auf den Bus.",
                "Sie freut sich über das Geschenk.",
                "Denkst du an mich?"
            ],
            "common_mistakes": [
                "❌ Ich warte den Bus.",
                "✅ Ich warte auf den Bus."
            ],
            "exercises": [
                {"type": "fill", "question": "Ich warte ___ den Bus. (auf/an)", "answer": "auf"},
                {"type": "fill", "question": "Denkst du ___ mich? (an/auf)", "answer": "an"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "vocabulary",
        "topic": "Прилагательные для описания характера",
        "weak_point_tags": ["work_vocabulary", "finance"],
        "content": {
            "title": "Прилагательные для описания характера",
            "rule": "freundlich (дружелюбный), ehrlich (честный), geduldig (терпеливый), fleißig (прилежный).",
            "examples": [
                "Meine Lehrerin ist freundlich.",
                "Er ist sehr ehrlich.",
                "Sie ist fleißig und geduldig."
            ],
            "common_mistakes": [
                "❌ Er ist fleißige.",
                "✅ Er ist fleißig."
            ],
            "exercises": [
                {"type": "fill", "question": "Sie ist sehr ___ (дружелюбная).", "answer": "freundlich"},
                {"type": "fill", "question": "Er ist ___ (честный).", "answer": "ehrlich"}
            ]
        },
        "xp_reward": 50
    },
    # Аудирование B1
    {
        "level": "B1",
        "pillar": "listening",
        "topic": "Понимание диалога (в кафе)",
        "weak_point_tags": ["listening_cafe"],
        "content": {
            "title": "Аудирование — диалог в кафе",
            "rule": "Прослушайте диалог и ответьте на вопросы (пока текст, позже аудио).",
            "examples": [
                "A: Guten Tag! Was möchten Sie?",
                "B: Ich hätte gerne einen Kaffee und ein Stück Kuchen."
            ],
            "common_mistakes": [
                "Пропуск артиклей в заказе"
            ],
            "exercises": [
                {"type": "fill", "question": "Was möchte der Gast? (Ключевые слова)", "answer": "Kaffee und Kuchen"}
            ]
        },
        "xp_reward": 50
    },
    # Произношение B1
    {
        "level": "B1",
        "pillar": "pronunciation",
        "topic": "Ударение в сложных словах",
        "weak_point_tags": ["pronunciation_stress"],
        "content": {
            "title": "Ударение в сложных существительных",
            "rule": "В немецких сложных словах ударение обычно падает на первый корень.",
            "examples": [
                "Krankenhaus (KRA-ken-haus)",
                "Fernseher (FERN-se-her)",
                "Hauptbahnhof (HAUPT-bahn-hof)"
            ],
            "common_mistakes": [
                "❌ Ударение на втором слоге",
                "✅ Ударение на первом слоге"
            ],
            "exercises": [
                {"type": "fill", "question": "На какой слог падает ударение в слове 'Krankenhaus'?", "answer": "первый"},
                {"type": "fill", "question": "На какой слог падает ударение в слове 'Fernseher'?", "answer": "первый"}
            ]
        },
        "xp_reward": 50
    },
    # ============================= УРОВЕНЬ B2 =============================
    # Грамматика B2
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Относительные придаточные в Dativ",
        "weak_point_tags": ["relative_clauses"],
        "content": {
            "title": "Относительные местоимения в Dativ",
            "rule": "Относительное местоимение согласуется в падеже с управляющим глаголом. Если глагол требует Dativ, используем 'dem' (мужской/средний) или 'der' (женский).",
            "examples": [
                "Der Mann, dem ich helfe, ist krank.",
                "Die Frau, der ich helfe, ist nett.",
                "Das Kind, dem ich helfe, ist klein."
            ],
            "common_mistakes": [
                "❌ Der Mann, den ich helfe.",
                "✅ Der Mann, dem ich helfe."
            ],
            "exercises": [
                {"type": "fill", "question": "Der Mann, ___ ich helfe, ist krank.", "answer": "dem"},
                {"type": "fill", "question": "Die Frau, ___ ich helfe, ist nett.", "answer": "der"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Уступительные предложения (obwohl)",
        "weak_point_tags": ["subordinate_clauses"],
        "content": {
            "title": "Уступительные придаточные с 'obwohl'",
            "rule": "'Obwohl' — 'хотя'. Глагол в конце придаточного.",
            "examples": [
                "Obwohl er krank ist, geht er zur Arbeit.",
                "Sie kommt, obwohl sie müde ist.",
                "Ich esse, obwohl ich keinen Hunger habe."
            ],
            "common_mistakes": [
                "❌ Obwohl er ist krank.",
                "✅ Obwohl er krank ist."
            ],
            "exercises": [
                {"type": "fill", "question": "___ er krank ist, geht er zur Arbeit. (Obwohl/Weil)", "answer": "Obwohl"},
                {"type": "fill", "question": "Sie kommt, ___ sie müde ist.", "answer": "obwohl"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Konjunktiv II модальных глаголов",
        "weak_point_tags": ["konjunktiv_ii"],
        "content": {
            "title": "Konjunktiv II с модальными глаголами",
            "rule": "Для выражения гипотетических возможностей используем формы: könnte, müsste, sollte, dürfte.",
            "examples": [
                "Ich könnte heute früher kommen.",
                "Er müsste mehr lernen.",
                "Sie sollte sich ausruhen."
            ],
            "common_mistakes": [
                "❌ Ich kann heute früher kommen (Indikativ)",
                "✅ Ich könnte heute früher kommen (Konjunktiv)"
            ],
            "exercises": [
                {"type": "fill", "question": "Ich ___ heute früher kommen. (können, Konjunktiv)", "answer": "könnte"},
                {"type": "fill", "question": "Er ___ mehr lernen. (müssen, Konjunktiv)", "answer": "müsste"}
            ]
        },
        "xp_reward": 50
    },
    # Лексика B2
    {
        "level": "B2",
        "pillar": "vocabulary",
        "topic": "Устойчивые выражения с предлогами",
        "weak_point_tags": ["idioms", "colloquial_expressions"],
        "content": {
            "title": "Устойчивые выражения с предлогами",
            "rule": "Некоторые выражения требуют конкретного предлога: an Erfahrung (в опыте), auf jeden Fall (в любом случае), mit der Zeit (со временем).",
            "examples": [
                "Er ist an Erfahrung sehr gut.",
                "Auf jeden Fall komme ich.",
                "Mit der Zeit wird es besser."
            ],
            "common_mistakes": [
                "❌ Er ist in Erfahrung gut.",
                "✅ Er ist an Erfahrung gut."
            ],
            "exercises": [
                {"type": "fill", "question": "Er ist ___ Erfahrung gut. (an/auf)", "answer": "an"},
                {"type": "fill", "question": "___ jeden Fall komme ich. (auf/an)", "answer": "Auf"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B2",
        "pillar": "vocabulary",
        "topic": "Абстрактные существительные (Folge, Ursache, Wirkung)",
        "weak_point_tags": ["abstract_nouns"],
        "content": {
            "title": "Абстрактные существительные",
            "rule": "die Folge (последствие), die Ursache (причина), die Wirkung (эффект).",
            "examples": [
                "Die Folge des Unfalls war schlimm.",
                "Die Ursache ist unbekannt.",
                "Die Wirkung des Medikaments ist gut."
            ],
            "common_mistakes": [
                "❌ Das Folge",
                "✅ Die Folge"
            ],
            "exercises": [
                {"type": "fill", "question": "Die ___ des Unfalls war schlimm. (Folge/Ursache)", "answer": "Folge"},
                {"type": "fill", "question": "Die ___ ist unbekannt. (Ursache/Wirkung)", "answer": "Ursache"}
            ]
        },
        "xp_reward": 50
    },
    # Аудирование B2
    {
        "level": "B2",
        "pillar": "listening",
        "topic": "Новости (Nachrichten)",
        "weak_point_tags": ["listening_news"],
        "content": {
            "title": "Аудирование — новости",
            "rule": "Прослушайте краткую новость и ответьте на вопросы (скоро будет аудио).",
            "examples": [
                "Die Regierung hat ein neues Gesetz beschlossen."
            ],
            "common_mistakes": [
                "Смешение Passiv und Aktiv"
            ],
            "exercises": [
                {"type": "fill", "question": "Wer hat das Gesetz beschlossen?", "answer": "Die Regierung"}
            ]
        },
        "xp_reward": 50
    }
]

# Добавление уроков в БД
for lesson in lessons_data:
    existing = db.query(Lesson).filter(Lesson.topic == lesson["topic"]).first()
    if not existing:
        db.add(Lesson(**lesson))
        print(f"➕ Добавлен урок: {lesson['topic']}")
    else:
        print(f"⏩ Урок '{lesson['topic']}' уже существует, пропуск.")

db.commit()
print("\n✅ Все уроки успешно добавлены в базу данных!")

