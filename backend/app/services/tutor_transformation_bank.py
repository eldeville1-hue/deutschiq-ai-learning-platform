"""Reviewed B2 sentence-transformation tasks.

Each task has a unique source marker and explicitly reviewed complete answers.
"""
# id, level, topic, instruction (German), source, target, alternatives
TRANSFORMATIONS = (
    ("b2-t01", "B2", "obwohl_clause", "Verbinde mit obwohl.", "Es regnet. Wir gehen spazieren.", "Obwohl es regnet, gehen wir spazieren.", ("Wir gehen spazieren, obwohl es regnet.",)),
    ("b2-t02", "B2", "weil_clause", "Verbinde mit weil.", "Die Prüfung ist wichtig. Ich lerne täglich.", "Ich lerne täglich, weil die Prüfung wichtig ist.", ("Weil die Prüfung wichtig ist, lerne ich täglich.",)),
    ("b2-t03", "B2", "damit_clause", "Verbinde mit damit.", "Ich spreche deutlich. Alle verstehen mich.", "Ich spreche deutlich, damit alle mich verstehen.", ("Damit alle mich verstehen, spreche ich deutlich.",)),
    ("b2-t04", "B2", "konjunktiv_ii", "Formuliere einen irrealen Wunsch mit wenn.", "Ich habe nicht genug Zeit. Ich lese nicht mehr.", "Wenn ich mehr Zeit hätte, würde ich mehr lesen.", ("Ich würde mehr lesen, wenn ich mehr Zeit hätte.",)),
    ("b2-t05", "B2", "obwohl_clause", "Verbinde mit obwohl.", "Der Weg ist lang. Wir fahren mit dem Fahrrad.", "Obwohl der Weg lang ist, fahren wir mit dem Fahrrad.", ("Wir fahren mit dem Fahrrad, obwohl der Weg lang ist.",)),
    ("b2-t06", "B2", "weil_clause", "Verbinde mit weil.", "Die Daten fehlen. Wir verschieben die Entscheidung.", "Wir verschieben die Entscheidung, weil die Daten fehlen.", ("Weil die Daten fehlen, verschieben wir die Entscheidung.",)),
)
