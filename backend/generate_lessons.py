# backend/generate_lessons.py
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
# УРОКИ ПО УРОВНЯМ
# ==========================================

lessons_data = [
    # ========== УРОВЕНЬ A1 ==========
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
        "topic": "Артикли (der/die/das)",
        "weak_point_tags": ["articles", "gender"],
        "content": {
            "title": "Определённые артикли",
            "rule": "der — мужской род, die — женский, das — средний.",
            "examples": ["der Mann (мужчина)", "die Frau (женщина)", "das Auto (машина)"],
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
        "topic": "Порядок слов в предложении",
        "weak_point_tags": ["word_order"],
        "content": {
            "title": "Порядок слов в главном предложении",
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
    # ========== УРОВЕНЬ A2 ==========
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
        "topic": "Дательный падеж (Dativ)",
        "weak_point_tags": ["dative_case", "article_declension"],
        "content": {
            "title": "Dativ — дательный падеж",
            "rule": "В Dativ артикли меняются: der → dem, die → der, das → dem.",
            "examples": ["Ich gebe dem Mann das Buch.", "Sie hilft der Frau."],
            "common_mistakes": ["❌ Ich gebe den Mann das Buch.", "✅ Ich gebe dem Mann das Buch."],
            "exercises": [
                {"type": "fill", "question": "Ich gebe ___ Mann das Buch.", "answer": "dem"}
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
            "rule": "Спряжение: ich kann, du kannst, er/sie/es kann, wir können, ihr könnt, sie können.",
            "examples": ["Ich kann Deutsch sprechen.", "Kannst du mir helfen?"],
            "common_mistakes": ["❌ Ich kann Deutsch spricht.", "✅ Ich kann Deutsch sprechen."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ Deutsch ___ (sprechen).", "answer": "kann ... sprechen"}
            ]
        },
        "xp_reward": 50
    },
    # ========== УРОВЕНЬ B1 ==========
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Passiv (страдательный залог)",
        "weak_point_tags": ["passiv", "process_passive"],
        "content": {
            "title": "Passiv в настоящем времени",
            "rule": "Passiv образуется с 'werden' + Partizip II: wird + Partizip II.",
            "examples": ["Das Haus wird gebaut.", "Der Brief wird geschrieben."],
            "common_mistakes": ["❌ Das Haus ist gebaut (Zustandspassiv)", "✅ Das Haus wird gebaut (Vorgangspassiv)"],
            "exercises": [
                {"type": "fill", "question": "Das Haus ___ gebaut.", "answer": "wird"}
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
            "rule": "Используем 'hätte', 'wäre' или 'würde' + инфинитив.",
            "examples": ["Ich hätte gern ein Glas Wasser.", "Würden Sie mir helfen?"],
            "common_mistakes": ["❌ Ich habe gern ein Glas Wasser.", "✅ Ich hätte gern ein Glas Wasser."],
            "exercises": [
                {"type": "fill", "question": "Ich ___ gern ein Glas Wasser.", "answer": "hätte"}
            ]
        },
        "xp_reward": 50
    },
    {
        "level": "B1",
        "pillar": "grammar",
        "topic": "Придаточные предложения (dass/ob)",
        "weak_point_tags": ["subordinate_clauses"],
        "content": {
            "title": "Придаточные с dass и ob",
            "rule": "'dass' — что, 'ob' — ли. Глагол в конце предложения.",
            "examples": ["Ich weiß, dass er kommt.", "Ich weiß nicht, ob er kommt."],
            "common_mistakes": ["❌ Ich weiß, dass er kommt heute.", "✅ Ich weiß, dass er heute kommt."],
            "exercises": [
                {"type": "fill", "question": "Ich weiß, ___ er kommt.", "answer": "dass"},
                {"type": "fill", "question": "Ich weiß nicht, ___ er kommt.", "answer": "ob"}
            ]
        },
        "xp_reward": 50
    },
    # ========== УРОВЕНЬ B2 ==========
    {
        "level": "B2",
        "pillar": "grammar",
        "topic": "Konjunktiv I (косвенная речь)",
        "weak_point_tags": ["konjunktiv_i", "indirect_speech"],
        "content": {
            "title": "Konjunktiv I — косвенная речь",
            "rule": "Используется для передачи чужих слов.",
            "examples": ["Er sagte, er habe keine Zeit."],
            "common_mistakes": ["❌ Er sagte, er hat keine Zeit.", "✅ Er sagte, er habe keine Zeit."],
            "exercises": [
                {"type": "fill", "question": "Er sagte, er ___ keine Zeit.", "answer": "habe"}
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
            "title": "Предлоги с родительным падежом",
            "rule": "Wegen, trotz, aufgrund — всегда с Genitiv.",
            "examples": ["Wegen des Wetters bleiben wir zu Hause.", "Trotz der Kälte gehe ich spazieren."],
            "common_mistakes": ["❌ Wegen dem Wetter", "✅ Wegen des Wetters"],
            "exercises": [
                {"type": "fill", "question": "___ des Wetters bleiben wir zu Hause.", "answer": "Wegen"}
            ]
        },
        "xp_reward": 50
    },
    # ========== УРОВЕНЬ C1 ==========
    {
        "level": "C1",
        "pillar": "grammar",
        "topic": "Номинальный стиль (Nominalstil)",
        "weak_point_tags": ["nominal_style", "abstract_nouns"],
        "content": {
            "title": "Номинальный стиль",
            "rule": "Замена глаголов на абстрактные существительные.",
            "examples": ["Die Lösung des Problems erfordert Geduld."],
            "common_mistakes": ["❌ Das Problem lösen erfordert Geduld.", "✅ Die Lösung des Problems erfordert Geduld."],
            "exercises": [
                {"type": "fill", "question": "Die ___ des Problems erfordert Geduld.", "answer": "Lösung"}
            ]
        },
        "xp_reward": 50
    },
]

# ==========================================
# ЗАГРУЗКА В БД
# ==========================================

for lesson in lessons_data:
    existing = db.query(Lesson).filter(Lesson.topic == lesson["topic"]).first()
    if not existing:
        db.add(Lesson(**lesson))
        print(f"➕ Добавлен урок: {lesson['topic']} ({lesson['level']})")
    else:
        print(f"⏩ Урок '{lesson['topic']}' уже существует, пропуск.")

db.commit()
print(f"\n✅ Добавлено {len(lessons_data)} уроков!")

