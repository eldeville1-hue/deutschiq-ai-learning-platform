export type AppLanguage = 'ru' | 'de';

const TOPICS: Record<string, Record<AppLanguage, string>> = {
  gender: { ru: 'Род существительных', de: 'Genus' },
  articles: { ru: 'Артикли', de: 'Artikel' },
  article_declension: { ru: 'Склонение артиклей', de: 'Artikeldeklination' },
  haben_conjugation: { ru: 'Спряжение haben', de: 'Konjugation von haben' },
  sein_conjugation: { ru: 'Спряжение sein', de: 'Konjugation von sein' },
  word_order: { ru: 'Порядок слов', de: 'Satzbau' },
  dative_case: { ru: 'Дательный и винительный падежи', de: 'Dativ und Akkusativ' },
  dativ_akkusativ: { ru: 'Дательный и винительный падежи', de: 'Dativ und Akkusativ' },
  perfekt_auxiliary: { ru: 'Perfekt с haben и sein', de: 'Perfekt mit haben und sein' },
  grammar: { ru: 'Грамматика', de: 'Grammatik' },
  vocabulary: { ru: 'Словарный запас', de: 'Wortschatz' },
  listening: { ru: 'Аудирование', de: 'Hörverstehen' },
  pronunciation: { ru: 'Произношение', de: 'Aussprache' },
  fruits: { ru: 'Фрукты', de: 'Obst' },
  verbs: { ru: 'Глаголы', de: 'Verben' },
  perfekt_haben_sein: { ru: 'Perfekt с haben и sein', de: 'Perfekt mit haben und sein' },
  verbs_of_movement: { ru: 'Глаголы движения', de: 'Bewegungsverben' },
  modal_verbs: { ru: 'Модальные глаголы', de: 'Modalverben' },
  travel_vocabulary: { ru: 'Лексика о путешествиях', de: 'Reisewortschatz' },
  prepositions_temporal: { ru: 'Предлоги времени', de: 'Temporale Präpositionen' },
  passiv: { ru: 'Пассивный залог', de: 'Passiv' },
  subordinate_clauses: { ru: 'Придаточные предложения', de: 'Nebensätze' },
  konjunktiv_ii: { ru: 'Konjunktiv II', de: 'Konjunktiv II' },
  work_vocabulary: { ru: 'Работа и профессия', de: 'Arbeit und Beruf' },
  relative_clauses: { ru: 'Относительные предложения', de: 'Relativsätze' },
  konjunktiv_i: { ru: 'Косвенная речь', de: 'Indirekte Rede' },
  genitive_prepositions: { ru: 'Предлоги с Genitiv', de: 'Genitivpräpositionen' },
  idioms: { ru: 'Устойчивые выражения', de: 'Redewendungen' },
  participles: { ru: 'Причастия', de: 'Partizipien' },
  nominal_style: { ru: 'Номинальный стиль', de: 'Nominalstil' },
};

export const topicLabel = (value: string, lang: AppLanguage) => {
  const key = value.trim().toLowerCase().replaceAll(' ', '_').replaceAll('&', '').replaceAll('__', '_');
  return TOPICS[key]?.[lang] || value.replaceAll('_', ' ');
};
