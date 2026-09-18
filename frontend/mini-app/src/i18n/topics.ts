import type { AppLanguage } from './language';

const TOPICS: Record<string, Record<AppLanguage, string>> = {
  gender: { ru: 'Род существительных', de: 'Genus', en: 'Noun gender' },
  articles: { ru: 'Артикли', de: 'Artikel', en: 'Articles' },
  article_declension: { ru: 'Склонение артиклей', de: 'Artikeldeklination', en: 'Article declension' },
  haben_conjugation: { ru: 'Спряжение haben', de: 'Konjugation von haben', en: 'Conjugating haben' },
  sein_conjugation: { ru: 'Спряжение sein', de: 'Konjugation von sein', en: 'Conjugating sein' },
  word_order: { ru: 'Порядок слов', de: 'Satzbau', en: 'Word order' },
  dative_case: { ru: 'Dativ и Akkusativ', de: 'Dativ und Akkusativ', en: 'Dative and accusative' },
  dativ_akkusativ: { ru: 'Dativ и Akkusativ', de: 'Dativ und Akkusativ', en: 'Dative and accusative' },
  perfekt_auxiliary: { ru: 'Perfekt с haben и sein', de: 'Perfekt mit haben und sein', en: 'Perfect tense with haben and sein' },
  grammar: { ru: 'Грамматика', de: 'Grammatik', en: 'Grammar' },
  vocabulary: { ru: 'Словарный запас', de: 'Wortschatz', en: 'Vocabulary' },
  listening: { ru: 'Аудирование', de: 'Hörverstehen', en: 'Listening' },
  pronunciation: { ru: 'Произношение', de: 'Aussprache', en: 'Pronunciation' },
  speaking: { ru: 'Говорение', de: 'Sprechen', en: 'Speaking' },
  fruits: { ru: 'Фрукты', de: 'Obst', en: 'Fruit' },
  verbs: { ru: 'Глаголы', de: 'Verben', en: 'Verbs' },
  perfekt_haben_sein: { ru: 'Perfekt с haben и sein', de: 'Perfekt mit haben und sein', en: 'Perfect tense with haben and sein' },
  verbs_of_movement: { ru: 'Глаголы движения', de: 'Bewegungsverben', en: 'Verbs of movement' },
  modal_verbs: { ru: 'Модальные глаголы', de: 'Modalverben', en: 'Modal verbs' },
  travel_vocabulary: { ru: 'Лексика о путешествиях', de: 'Reisewortschatz', en: 'Travel vocabulary' },
  prepositions_temporal: { ru: 'Предлоги времени', de: 'Temporale Präpositionen', en: 'Time prepositions' },
  passiv: { ru: 'Пассивный залог', de: 'Passiv', en: 'Passive voice' },
  subordinate_clauses: { ru: 'Придаточные предложения', de: 'Nebensätze', en: 'Subordinate clauses' },
  konjunktiv_ii: { ru: 'Konjunktiv II', de: 'Konjunktiv II', en: 'Subjunctive II' },
  work_vocabulary: { ru: 'Работа и профессия', de: 'Arbeit und Beruf', en: 'Work and careers' },
  relative_clauses: { ru: 'Относительные предложения', de: 'Relativsätze', en: 'Relative clauses' },
  konjunktiv_i: { ru: 'Косвенная речь', de: 'Indirekte Rede', en: 'Reported speech' },
  genitive_prepositions: { ru: 'Предлоги с Genitiv', de: 'Genitivpräpositionen', en: 'Genitive prepositions' },
  advanced_prepositions: { ru: 'Сложные предлоги', de: 'Fortgeschrittene Präpositionen', en: 'Advanced prepositions' },
  idioms: { ru: 'Устойчивые выражения', de: 'Redewendungen', en: 'Idioms' },
  participles: { ru: 'Причастия', de: 'Partizipien', en: 'Participles' },
  nominal_style: { ru: 'Номинальный стиль', de: 'Nominalstil', en: 'Nominal style' },
  prepositions: { ru: 'Предлоги', de: 'Präpositionen', en: 'Prepositions' },
  dative_pronouns: { ru: 'Местоимения в Dativ', de: 'Dativpronomen', en: 'Dative pronouns' },
};

export const topicLabel = (value: string, lang: AppLanguage) => {
  const key = value.trim().toLowerCase().replaceAll(' ', '_').replaceAll('&', '').replaceAll('__', '_');
  return TOPICS[key]?.[lang] || value.replaceAll('_', ' ');
};
