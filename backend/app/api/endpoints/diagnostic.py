from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from app.core.database import get_db
from app.models.user import User
from app.models.diagnostic import DiagnosticResult, DiagnosticMistake
from app.services.diagnostic import calculate_level_and_scores
from sqlalchemy.exc import SQLAlchemyError
from app.core.telegram_auth import telegram_user_id, assert_owner

router = APIRouter(prefix="/api/diagnostic", tags=["diagnostic"])

MOCK_QUESTIONS = [
    # A1
    {"id": 1, "pillar": "grammar", "difficulty": "A1", "text": "Ich ______ einen Hund.", "options": ["habe", "bin", "hat", "hast"], "correct_answer": "habe", "weak_tags": ["haben_conjugation"], "explanation": "'Ich habe' — правильное спряжение."},
    {"id": 2, "pillar": "grammar", "difficulty": "A1", "text": "______ Auto ist neu.", "options": ["Der", "Die", "Das", "Den"], "correct_answer": "Das", "weak_tags": ["articles", "gender"], "explanation": "Auto — средний род, артикль 'das'."},
    {"id": 3, "pillar": "vocabulary", "difficulty": "A1", "text": "Wie sagt man 'Apple' auf Deutsch?", "options": ["Apfel", "Birne", "Kirsche", "Orange"], "correct_answer": "Apfel", "weak_tags": ["fruits"], "explanation": "Apple — Apfel."},
    {"id": 4, "pillar": "grammar", "difficulty": "A1", "text": "Was ist die richtige Wortstellung?", "options": ["Ich heute gehe nach Hause.", "Ich gehe heute nach Hause.", "Heute ich gehe nach Hause.", "Gehe ich heute nach Hause."], "correct_answer": "Ich gehe heute nach Hause.", "weak_tags": ["word_order"], "explanation": "Глагол на втором месте."},
    # A2
    {"id": 5, "pillar": "grammar", "difficulty": "A2", "text": "Wann ______ du nach Berlin gefahren?", "options": ["bist", "hast", "warst", "hattest"], "correct_answer": "bist", "weak_tags": ["perfekt_auxiliary", "verbs_of_movement"], "explanation": "'fahren' — движение, вспомогательный 'sein'."},
    {"id": 6, "pillar": "grammar", "difficulty": "A2", "text": "Ich gebe ______ Mann das Buch.", "options": ["dem", "den", "der", "des"], "correct_answer": "dem", "weak_tags": ["dative_case", "article_declension"], "explanation": "Dativ мужского рода — 'dem'."},
    {"id": 7, "pillar": "grammar", "difficulty": "A2", "text": "Ich ______ Deutsch sprechen.", "options": ["kann", "könne", "könnt", "konnte"], "correct_answer": "kann", "weak_tags": ["modal_verbs", "können"], "explanation": "'können' в 1 лице — 'kann'."},
    {"id": 8, "pillar": "vocabulary", "difficulty": "A2", "text": "Was braucht man am Flughafen?", "options": ["der Pass", "die Karte", "das Ticket", "Alle Antworten sind richtig"], "correct_answer": "Alle Antworten sind richtig", "weak_tags": ["travel_vocabulary"], "explanation": "Alle drei sind richtig."},
    {"id": 9, "pillar": "grammar", "difficulty": "A2", "text": "Ich stehe ______ 7 Uhr auf.", "options": ["um", "am", "im", "in"], "correct_answer": "um", "weak_tags": ["prepositions_temporal"], "explanation": "Um für Uhrzeiten."},
    # B1
    {"id": 10, "pillar": "grammar", "difficulty": "B1", "text": "Das Haus ______ gebaut.", "options": ["wird", "wurde", "ist", "war"], "correct_answer": "wird", "weak_tags": ["passiv", "process_passive"], "explanation": "Passiv Präsens: wird + Partizip II."},
    {"id": 11, "pillar": "grammar", "difficulty": "B1", "text": "Ich weiß nicht, ______ er kommt.", "options": ["dass", "ob", "wenn", "weil"], "correct_answer": "ob", "weak_tags": ["subordinate_clauses"], "explanation": "'ob' — 'ли'."},
    {"id": 12, "pillar": "grammar", "difficulty": "B1", "text": "Ich ______ gern ein Glas Wasser.", "options": ["hätte", "habe", "hatte", "haben"], "correct_answer": "hätte", "weak_tags": ["konjunktiv_ii", "polite_requests"], "explanation": "Konjunktiv II für Höflichkeit."},
    {"id": 13, "pillar": "vocabulary", "difficulty": "B1", "text": "Was bedeutet 'die Gehaltserhöhung'?", "options": ["Повышение зарплаты", "Сокращение зарплаты", "Премия", "Увольнение"], "correct_answer": "Повышение зарплаты", "weak_tags": ["work_vocabulary", "finance"], "explanation": "Gehaltserhöhung — повышение зарплаты."},
    {"id": 14, "pillar": "grammar", "difficulty": "B1", "text": "Der Mann, ______ dort steht, ist mein Chef.", "options": ["der", "den", "dem", "dessen"], "correct_answer": "der", "weak_tags": ["relative_clauses", "relative_pronouns"], "explanation": "Relative Pronomen Nominativ: der."},
    # B2
    {"id": 15, "pillar": "grammar", "difficulty": "B2", "text": "Er sagte, er ______ keine Zeit.", "options": ["habe", "hat", "hätte", "hatte"], "correct_answer": "habe", "weak_tags": ["konjunktiv_i", "indirect_speech"], "explanation": "Konjunktiv I für indirekte Rede."},
    {"id": 16, "pillar": "grammar", "difficulty": "B2", "text": "______ des Wetters bleiben wir zu Hause.", "options": ["Wegen", "Trotz", "Aufgrund", "Alle Antworten sind möglich"], "correct_answer": "Alle Antworten sind möglich", "weak_tags": ["genitive_prepositions", "advanced_prepositions"], "explanation": "Alle Präpositionen mit Genitiv."},
    {"id": 17, "pillar": "vocabulary", "difficulty": "B2", "text": "Was bedeutet 'die Katze im Sack kaufen'?", "options": ["Купить кота в мешке", "Купить что-то, не глядя", "Совершить удачную покупку", "Обмануть продавца"], "correct_answer": "Купить что-то, не глядя", "weak_tags": ["idioms", "colloquial_expressions"], "explanation": "Etwas ohne Prüfung kaufen."},
    {"id": 18, "pillar": "grammar", "difficulty": "B2", "text": "Das ______ Buch ist sehr interessant.", "options": ["gelesene", "gelesenes", "gelesener", "gelesenem"], "correct_answer": "gelesene", "weak_tags": ["participles", "adjective_declension"], "explanation": "Partizip II mit Endung -e."},
    # C1
    {"id": 19, "pillar": "grammar", "difficulty": "C1", "text": "Die ______ des Problems erfordert Geduld.", "options": ["Lösung", "Analyse", "Bearbeitung", "Alle Antworten sind möglich"], "correct_answer": "Alle Antworten sind möglich", "weak_tags": ["nominal_style", "abstract_nouns"], "explanation": "Alle Optionen sind korrekt."},
    {"id": 20, "pillar": "vocabulary", "difficulty": "C1", "text": "Was bedeutet 'sich etwas in den Kopf setzen'?", "options": ["Sich etwas fest vornehmen", "Etwas vergessen", "Etwas bereuen", "Jemanden überzeugen"], "correct_answer": "Sich etwas fest vornehmen", "weak_tags": ["idioms", "advanced_expressions"], "explanation": "Sich etwas fest vornehmen."},
]

class SubmitAnswers(BaseModel):
    user_id: int
    answers: Dict[int, str]

@router.get("/questions")
async def get_questions(lang: str = "ru", authenticated_id: int = Depends(telegram_user_id)):
    return [{key: value for key, value in question.items() if key not in ("correct_answer", "explanation", "weak_tags")} for question in MOCK_QUESTIONS]

@router.post("/submit")
async def submit_diagnostic(data: SubmitAnswers, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    result = calculate_level_and_scores(data.answers, MOCK_QUESTIONS)
    persisted = False
    try:
        user = db.query(User).filter(User.telegram_id == data.user_id).first()
        if not user:
            user = User(telegram_id=data.user_id)
            db.add(user)
            db.flush()
        diag = DiagnosticResult(
            user_id=user.id,
            overall_score=result["overall_score"],
            grammar_score=result["pillars"]["grammar"],
            vocabulary_score=result["pillars"]["vocabulary"],
            listening_score=result["pillars"]["listening"],
            pronunciation_score=result["pillars"]["pronunciation"],
            weak_points=result["weak_points"]
        )
        db.add(diag)
        db.flush()
        for question in MOCK_QUESTIONS:
            if question["id"] in data.answers and data.answers.get(question["id"]) != question["correct_answer"]:
                db.add(DiagnosticMistake(
                    diagnostic_id=diag.id,
                    topic=question.get("weak_tags", ["grammar"])[0],
                    question=question["text"],
                    user_answer=data.answers.get(question["id"], "—"),
                    correct_answer=question["correct_answer"],
                    explanation=question.get("explanation", ""),
                ))
        user.current_level = result["level"]
        user.diagnostic_completed = True
        db.commit()
        persisted = True
    except SQLAlchemyError:
        # Результат всё равно показываем; после запуска БД следующая попытка сохранится.
        db.rollback()
    return {
        "level": result["level"],
        "overall_score": result["overall_score"],
        "pillars": result["pillars"],
        "skill_status": {
            "grammar": "assessed",
            "vocabulary": "assessed",
            "listening": "not_assessed",
            "pronunciation": "not_assessed",
        },
        "confidence": "medium",
        "weak_points": result["weak_points"],
        "weak_tags": list(result["weak_points"].keys()),
        "persisted": persisted,
        "mistakes": [
            {
                "tag": question.get("weak_tags", ["grammar"])[0],
                "question": question["text"],
                "user_answer": data.answers.get(question["id"], "—"),
                "correct_answer": question["correct_answer"],
                "explanation": question.get("explanation", ""),
            }
            for question in MOCK_QUESTIONS
            if question["id"] in data.answers and data.answers.get(question["id"]) != question["correct_answer"]
        ],
    }
