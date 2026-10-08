"""Hand-authored linguistic challenge cases (not independently reviewed).

Run: python -m tests.linguistic_challenge_suite
"""
import json
from collections import Counter
from pathlib import Path
from app.services.answer_intelligence import evaluate_structured_answer

# Each item: level, task family, target, response, provisional verdict,
# intended error category. These labels are design hypotheses, not gold data.
CASES = [
 ("A1","translation","Ich habe einen Hund.","Ich habe einen Hund.","correct",None),
 ("A1","translation","Ich habe einen Hund.","Ich habe ein Hund.","incorrect","article"),
 ("A1","translation","Ich habe einen Hund.","Ich habe keinen Hund.","incorrect","negation"),
 ("A1","choice","Ich trinke Wasser.","Ich trinke Wasser.","correct",None),
 ("A1","choice","Ich trinke Wasser.","Ich trinke Milch.","incorrect","vocabulary"),
 ("A1","reorder","Wir lernen heute Deutsch.","Heute lernen wir Deutsch.","incorrect","word_order"),
 ("A1","sentence","Sie wohnt in Berlin.","Sie lebt in Berlin.","correct",None),
 ("A1","sentence","Sie wohnt in Berlin.","Sie wohnt nicht in Berlin.","incorrect","negation"),
 ("A1","error_repair","Er hat einen Stift.","Er hat ein Stift.","incorrect","article"),
 ("A1","translation","Ich kaufe Brot.","Ich kaufe Brot.","correct",None),
 ("A2","translation","Ich bin gestern nach Hause gegangen.","Gestern bin ich nach Hause gegangen.","correct",None),
 ("A2","translation","Ich bin gestern nach Hause gegangen.","Ich habe gestern nach Hause gegangen.","incorrect","auxiliary"),
 ("A2","sentence","Ich warte auf den Bus.","Ich warte auf dem Bus.","incorrect","case"),
 ("A2","translation","Ich muss morgen arbeiten.","Morgen muss ich arbeiten.","correct",None),
 ("A2","choice","Ich interessiere mich für Musik.","Ich interessiere mich an Musik.","incorrect","preposition"),
 ("A2","error_repair","Ich habe meine Freundin besucht.","Ich habe meine Freundin besuchen.","incorrect","participle"),
 ("A2","sentence","Wenn es regnet, bleibe ich zu Hause.","Wenn es regnet, ich bleibe zu Hause.","incorrect","word_order"),
 ("A2","translation","Kannst du mir helfen?","Kannst du mir bitte helfen?","correct",None),
 ("A2","translation","Wir sind nach Hamburg gefahren.","Wir haben nach Hamburg gefahren.","incorrect","auxiliary"),
 ("A2","free_text","Ich freue mich auf das Wochenende.","Ich freue mich über das Wochenende.","uncertain","preposition"),
 ("B1","translation","Ich lerne Deutsch, damit ich eine Ausbildung machen kann.","Ich lerne Deutsch, um eine Ausbildung machen zu können.","correct",None),
 ("B1","sentence","Ich glaube, dass er heute kommt.","Ich glaube, dass er kommt heute.","incorrect","word_order"),
 ("B1","error_repair","Das Fahrrad, das ich gekauft habe, ist neu.","Das Fahrrad, den ich gekauft habe, ist neu.","incorrect","relative_pronoun"),
 ("B1","translation","Wenn ich Zeit hätte, würde ich mitkommen.","Hätte ich Zeit, würde ich mitkommen.","correct",None),
 ("B1","sentence","Obwohl es regnet, gehen wir spazieren.","Obwohl es regnet, wir gehen spazieren.","incorrect","word_order"),
 ("B1","translation","Der Brief wurde gestern geschrieben.","Gestern wurde der Brief geschrieben.","correct",None),
 ("B1","sentence","Ich weiß nicht, ob sie kommt.","Ich weiß nicht, dass sie kommt.","incorrect","meaning"),
 ("B1","translation","Er hat gesagt, dass er krank ist.","Er sagte, er sei krank.","correct",None),
 ("B1","choice","Ich habe mich um die Stelle beworben.","Ich habe mich für die Stelle beworben.","incorrect","preposition"),
 ("B1","free_text","Ich würde lieber zu Hause bleiben.","Ich möchte heute lieber zu Hause bleiben.","uncertain",None),
 ("B2","translation","Hätte ich früher davon erfahren, hätte ich anders gehandelt.","Wenn ich früher davon erfahren hätte, hätte ich anders gehandelt.","correct",None),
 ("B2","sentence","Der Bericht, auf den wir uns beziehen, ist umstritten.","Der Bericht, auf dem wir uns beziehen, ist umstritten.","incorrect","preposition"),
 ("B2","translation","Obwohl erhebliche Zweifel bestanden, wurde die Entscheidung getroffen.","Die Entscheidung wurde getroffen, obwohl erhebliche Zweifel bestanden.","correct",None),
 ("B2","sentence","Es lässt sich kaum bestreiten, dass Bildung Chancen eröffnet.","Es lässt sich kaum bestreiten, dass Bildung eröffnet Chancen.","incorrect","word_order"),
 ("B2","error_repair","Die Maßnahme trägt dazu bei, Energie zu sparen.","Die Maßnahme trägt dazu bei, Energie sparen.","incorrect","infinitive"),
 ("B2","translation","Anstatt die Ursachen zu untersuchen, wurden nur Symptome behandelt.","Es wurden nur Symptome behandelt, statt die Ursachen zu untersuchen.","correct",None),
 ("B2","sentence","Unter der Voraussetzung, dass alle zustimmen, beginnen wir.","Unter der Voraussetzung, dass alle zustimmen, wir beginnen.","incorrect","word_order"),
 ("B2","translation","Die Ergebnisse sind vielversprechend, aber Langzeitdaten fehlen.","Obgleich die Ergebnisse vielversprechend sind, fehlen Langzeitdaten.","correct",None),
 ("B2","free_text","Es wäre sinnvoll gewesen, die Betroffenen einzubeziehen.","Die Betroffenen hätten beteiligt werden sollen.","uncertain",None),
 ("B2","sentence","Die Digitalisierung stellt Unternehmen vor neue Herausforderungen.","Die Digitalisierung stellt Unternehmen keine neuen Herausforderungen.","incorrect","negation"),
]

KNOWN_ALTERNATIVES = {
    ("A2", "Ich bin gestern nach Hause gegangen."): ["Gestern bin ich nach Hause gegangen."],
    ("A2", "Ich muss morgen arbeiten."): ["Morgen muss ich arbeiten."],
    ("A1", "Sie wohnt in Berlin."): ["Sie lebt in Berlin."],
    ("A2", "Kannst du mir helfen?"): ["Kannst du mir bitte helfen?"],
    ("B1", "Der Brief wurde gestern geschrieben."): ["Gestern wurde der Brief geschrieben."],
    ("B1", "Wenn ich Zeit hätte, würde ich mitkommen."): ["Hätte ich Zeit, würde ich mitkommen."],
}

def build_challenges():
    result = []
    for i, (level, family, target, answer, verdict, error) in enumerate(CASES):
        result.append({
            "id": f"challenge-{level}-{i:03d}", "cefr": level,
            "objective": f"Express the target meaning in German: {target}",
            "exercise": {"type": family, "question": f"Express the target meaning in German: {target}",
                         "answer": target,
                         "accepted_answers": [target, *KNOWN_ALTERNATIVES.get((level, target), [])]},
            "learner_answer": answer, "task_family": family,
            "provisional_expected": verdict, "provisional_error_type": error,
            "source": "hand_authored_unreviewed",
            "split": "challenge",
            "human_review": {"status": "pending", "reviewer": None, "decision": None, "notes": ""},
        })
    return result

def audit(rows=None, evaluator=evaluate_structured_answer):
    rows = build_challenges() if rows is None else rows
    failures = []
    confusion = Counter()
    diagnosis_confusion = Counter()
    for row in rows:
        result = evaluator(row["learner_answer"], row["exercise"])
        prediction = ("uncertain" if result["evaluation_status"] != "verified"
                      else "correct" if result["correct"] else "incorrect")
        expected = row["provisional_expected"]
        confusion[f"{expected}->{prediction}"] += 1
        expected_error = row.get("provisional_error_type")
        predicted_errors = [e["type"] for e in result.get("errors", [])]
        # Diagnostic labels are provisional hypotheses; mismatches are review
        # candidates, not automatically confirmed model errors.
        if expected_error and prediction == "incorrect":
            diagnosis_confusion["match" if expected_error in predicted_errors else "mismatch"] += 1
        if prediction != expected or (expected_error and prediction == "incorrect" and expected_error not in predicted_errors):
            failures.append({"id": row["id"], "cefr": row["cefr"],
                             "task_family": row["task_family"],
                             "provisional_expected": expected, "predicted": prediction,
                             "answer": row["learner_answer"],
                             "provisional_error_type": expected_error,
                             "predicted_errors": predicted_errors,
                             "decision_disagreement": prediction != expected})
    return {"cases": len(rows), "provisional_confusion": dict(sorted(confusion.items())),
            "diagnosis_comparison": dict(sorted(diagnosis_confusion.items())),
            "disagreements": failures, "disagreement_count": len(failures),
            "human_reviewed": 0, "release_evidence": False}

def main():
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
