"""Reproducible *synthetic* evaluation fixture generator for DeutschIQ 88.

Generated labels are provisional and MUST NOT be described as human-reviewed.\nThis synthetic stress fixture is not a linguistically validated held-out dataset.
Run: python -m tests.generate_evaluation_benchmark
"""
import json
from pathlib import Path

LEVELS = ("A1", "A2", "B1", "B2")
TEMPLATES = (
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Kaffee.", "correct", "choice"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe ein Kaffee.", "incorrect", "choice"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe keinen Kaffee.", "incorrect", "choice"),
    ("Ich kaufe einen Kaffee.", "Ich hole einen Kaffee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich besorge einen Kaffee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe ein Kaffee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufen einen Kaffee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe keinen Kaffee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Kafee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Tee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Kaffee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe Kaffee.", "uncertain", "translation"),
)
# Each case receives its own ID, level and contextual prompt. Repeated surface
# forms deliberately test whether the exercise objective changes the verdict.
CONTEXTS = (
    "Choose the exact response.",
    "Translate: I am buying a coffee.",
    "Translate: I am getting a coffee.",
    "Write a sentence about buying coffee.",
    "Practice accusative articles.",
    "Practice present-tense conjugation.",
    "Practice negation.",
    "Respond to a café order.",
    "Use a natural German expression.",
    "Compare the model answer with your response.",
)

# Level-specific constructions; labels remain provisional and never count as reviews.
LEVEL_SENTENCES = {
    "A1": ("Ich trinke Wasser.", "Sie wohnt in Berlin.", "Wir lernen Deutsch.", "Er hat einen Hund.", "Ich brauche einen Stift.", "Das Buch liegt auf dem Tisch.", "Heute ist Montag.", "Meine Schwester kocht Reis.", "Ich fahre mit dem Bus.", "Wir kaufen frisches Brot."),
    "A2": ("Gestern habe ich meine Freundin besucht.", "Wenn es regnet, bleibe ich zu Hause.", "Ich muss morgen früh aufstehen.", "Wir sind letztes Jahr nach Hamburg gefahren.", "Kannst du mir bitte den Weg erklären?", "Ich interessiere mich für deutsche Musik.", "Sie hat sich über das Geschenk gefreut.", "Obwohl ich müde bin, gehe ich spazieren.", "Er wartet seit einer Stunde auf den Zug.", "Ich habe vergessen, die Tür zu schließen."),
    "B1": ("Ich lerne Deutsch, damit ich eine Ausbildung machen kann.", "Nachdem wir gegessen hatten, gingen wir ins Kino.", "Das Fahrrad, das ich gestern gekauft habe, ist gebraucht.", "Ich würde lieber zu Hause bleiben, wenn ich könnte.", "Er behauptet, dass er die E-Mail nicht erhalten hat.", "Trotz des schlechten Wetters fand das Konzert statt.", "Die Wohnung wird nächste Woche renoviert.", "Sie hat vor, sich für die Stelle zu bewerben.", "Je mehr ich übe, desto sicherer spreche ich.", "Ich frage mich, ob der Termin verschoben wurde."),
    "B2": ("Die Entscheidung wurde getroffen, obwohl erhebliche Zweifel bestanden.", "Hätte ich früher davon erfahren, hätte ich anders gehandelt.", "Es lässt sich kaum bestreiten, dass Bildung Chancen eröffnet.", "Der Bericht, auf den sich die Kommission bezieht, ist umstritten.", "Anstatt die Ursachen zu untersuchen, wurden nur Symptome behandelt.", "Die Maßnahme soll dazu beitragen, den Energieverbrauch zu senken.", "Obgleich die Ergebnisse vielversprechend sind, fehlen Langzeitdaten.", "Unter der Voraussetzung, dass alle zustimmen, kann das Projekt beginnen.", "Die zunehmende Digitalisierung stellt Unternehmen vor neue Herausforderungen.", "Es wäre sinnvoll gewesen, die Betroffenen rechtzeitig einzubeziehen."),
}
VARIANTS = ("exact", "punctuation", "lowercase", "empty", "omit_first", "omit_last", "swap_first", "repeat_first", "reverse", "negate", "prefix", "suffix")

def build_cases():
    rows = []
    for level in LEVELS:
        for index, model in enumerate(LEVEL_SENTENCES[level]):
            words = model.rstrip(".?!").split()
            # Rotate objectives across distinct exercise families. All labels
            # remain synthetic hypotheses, never independent review evidence.
            families = ("reorder", "error_repair", "translation", "sentence",
                        "writing", "choice", "free_text", "context_choice",
                        "reorder", "translation")
            family = families[index]
            objective = {
                "reorder": f"Put the tokens into the original German sentence: {model}",
                "error_repair": f"Repair the German sentence to match the target: {model}",
                "translation": f"Express this target meaning in German: {model}",
                "sentence": f"Write a grammatical sentence conveying: {model}",
                "writing": f"Write a natural German sentence with this meaning: {model}",
                "choice": f"Select the option matching the target exactly: {model}",
                "free_text": f"Respond in German, expressing this idea: {model}",
                "context_choice": f"Choose the answer matching this situation: {model}",
            }[family]
            for variant in VARIANTS:
                if variant == "exact":
                    response = model
                elif variant == "punctuation":
                    response = model.rstrip(".?!")
                elif variant == "lowercase":
                    response = model.lower()
                elif variant == "empty":
                    response = ""
                elif variant == "omit_first":
                    response = " ".join(words[1:])
                elif variant == "omit_last":
                    response = " ".join(words[:-1])
                elif variant == "swap_first":
                    response = " ".join([words[1], words[0], *words[2:]])
                elif variant == "repeat_first":
                    response = " ".join([words[0], *words])
                elif variant == "reverse":
                    response = " ".join(reversed(words))
                elif variant == "negate":
                    response = model.rstrip(".?!") + " nicht."
                elif variant == "prefix":
                    response = "Vielleicht " + model[0].lower() + model[1:]
                else:
                    response = model.rstrip(".?!") + " heute."
                rows.append({
                    "id": f"{level}-{index:02d}-{variant}",
                    "cefr": level,
                    "objective": objective,
                    "exercise": {"type": family, "question": objective, "answer": model},
                    "learner_answer": response,
                    "provisional_expected": ("correct" if variant in {"exact", "punctuation", "lowercase"}\n                                             else "uncertain" if family in {"translation", "sentence", "writing", "free_text"}\n                                             else "incorrect"),
                    "human_review": {"status": "pending", "reviewer": None, "decision": None, "notes": ""},
                    "source": "synthetic_level_specific",
                    "task_family": family,
                    "split": "development" if index < 8 else "holdout",
                })
    return rows

def main():
    path = Path(__file__).resolve().parent / "fixtures" / "evaluation_v88_synthetic.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_cases()
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    print(f"Wrote {len(rows)} provisional cases to {path}")

if __name__ == "__main__":
    main()
