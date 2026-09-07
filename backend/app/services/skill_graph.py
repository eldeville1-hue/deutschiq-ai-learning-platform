"""A small, explicit skill graph for the first DeutschIQ learning track.

The graph is deliberately code-owned and versioned. Lesson tags may evolve,
but recommendations must remain explainable and deterministic.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    id: str
    pillar: str
    level: str
    prerequisites: tuple[str, ...] = ()


SKILLS: dict[str, Skill] = {
    "word_order": Skill("word_order", "grammar", "A1"),
    "modal_verbs": Skill("modal_verbs", "grammar", "A2", ("word_order",)),
    "subordinate_clauses": Skill("subordinate_clauses", "grammar", "B1", ("word_order", "modal_verbs")),
    "dative_case": Skill("dative_case", "grammar", "A2", ("word_order",)),
    "prepositions": Skill("prepositions", "grammar", "A2", ("dative_case",)),
    "dative_pronouns": Skill("dative_pronouns", "grammar", "A2", ("dative_case",)),
    "articles": Skill("articles", "grammar", "A1", ("word_order",)),
    "perfekt_auxiliary": Skill("perfekt_auxiliary", "grammar", "A2", ("word_order",)),
    "participles": Skill("participles", "grammar", "A2", ("perfekt_auxiliary",)),
    "verbs_of_movement": Skill("verbs_of_movement", "grammar", "A2", ("perfekt_auxiliary",)),
    "adjective_endings": Skill("adjective_endings", "grammar", "B1", ("articles", "dative_case")),
}


def skill_for(topic: str) -> Skill:
    return SKILLS.get(topic, Skill(topic, "general", "A1"))


def prerequisites_met(topic: str, mastery: dict[str, float], threshold: float = 45.0) -> bool:
    return all(mastery.get(item, 0.0) >= threshold for item in skill_for(topic).prerequisites)


def blocked_by(topic: str, mastery: dict[str, float], threshold: float = 45.0) -> list[str]:
    return [item for item in skill_for(topic).prerequisites if mastery.get(item, 0.0) < threshold]
