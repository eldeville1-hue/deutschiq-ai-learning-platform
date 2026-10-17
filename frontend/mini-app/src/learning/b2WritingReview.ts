import { tr } from "../i18n/language";

export function getB2WritingReviewHints(exerciseId: string, answer: string, lang: Parameters<typeof tr>[0]): string[] {
  const answerText = answer.toLocaleLowerCase('de-DE').trim();
  // Keyword presence is only a weak signal, never evidence of writing quality.
  // Avoid claiming that a very short or empty response meets the criteria.
  const minimumWords = 12;
  const words = answerText.match(/[\p{L}\p{N}]+/gu) || [];
  if (words.length < minimumWords && ['argument_structure-dialogue', 'counterargument-dialogue', 'data_description-dialogue'].includes(exerciseId)) {
    return [tr(lang,
      'Ответ пока слишком краткий для содержательной самопроверки. Раскрой мысль несколькими предложениями.',
      'Dein Text ist für eine sinnvolle Selbstkontrolle noch sehr kurz. Führe deine Gedanken in mehreren Sätzen aus.',
      'Your response is too brief for a useful self-check. Develop your ideas in several sentences.')];
  }
  const missingElements: string[] = [];
  if (exerciseId === 'argument_structure-dialogue') {
    if (!/\b(weil|denn|da|deshalb|daher|zumal|aufgrund|wegen|aus diesem grund|ein grund|führt dazu|trägt dazu bei|ermöglicht|bewirkt)\b/i.test(answerText))
      missingElements.push(tr(lang, 'Проверь, понятна ли причина твоей позиции. Её можно выразить разными способами.', 'Prüfe, ob deine Begründung deutlich wird. Du kannst sie unterschiedlich formulieren.', 'Check whether your reasoning is clear; there are several ways to express it.'));
    if (!/\b(zum beispiel|beispielsweise|etwa|konkret|beispiel|belegen|zeigt sich|so könnte|etwa wenn)\b/i.test(answerText))
      missingElements.push(tr(lang, 'Проверь, есть ли конкретный пример или доказательство.', 'Prüfe, ob ein konkretes Beispiel oder ein Beleg enthalten ist.', 'Check whether you included a concrete example or supporting evidence.'));
  } else if (exerciseId === 'counterargument-dialogue') {
    if (!/\b(zwar|obwohl|auch wenn|einerseits|natürlich|verständlich|nachvollziehbar|es stimmt|ich verstehe|der einwand|die sorge|zugegeben)\b/i.test(answerText))
      missingElements.push(tr(lang, 'Проверь, признал(а) ли ты возражение.', 'Prüfe, ob du den Einwand aufgegriffen hast.', 'Check whether you acknowledged the objection.'));
    if (!/\b(aber|jedoch|dennoch|andererseits|trotzdem|allerdings|hingegen|gleichwohl|dagegen|demgegenüber|auf lange sicht|langfristig)\b/i.test(answerText))
      missingElements.push(tr(lang, 'Проверь, есть ли обоснованный ответ на возражение.', 'Prüfe, ob du dem Einwand eine begründete Antwort gegenüberstellst.', 'Check whether you gave a reasoned response to the objection.'));
  } else if (exerciseId === 'data_description-dialogue') {
    // Only flag a reversed pairing when the year and its value are adjacent.
    // Longer prose can mention both years and values in different orders.
    const reversedPair = /\b2020\b\s*(?:[:–—-]|(?:lag|waren|betrug|bei))?\s*(?:bei\s*)?48\s*%?/i.test(answerText)
      || /\b2025\b\s*(?:[:–—-]|(?:lag|waren|betrug|bei))?\s*(?:bei\s*)?36\s*%?/i.test(answerText);
    if (reversedPair)
      missingElements.push(tr(lang,
        'Проверь соответствие данных: в 2020 году было 36 %, в 2025 году — 48 %.',
        'Prüfe die Zuordnung: 2020 waren es 36 %, 2025 waren es 48 %.',
        'Check the year-to-value pairing: 36% in 2020 and 48% in 2025.'));
    const mentionsDifference = /\b(12|zwölf)\b/i.test(answerText);
    const mentionsPoints = /prozentpunkt(?:e|en)?|percentage.points?/i.test(answerText);
    if (!mentionsDifference || !mentionsPoints)
      missingElements.push(tr(lang,
        'Проверь, указана ли разница именно в процентных пунктах (12), а не в процентах.',
        'Prüfe, ob du den Unterschied als 12 Prozentpunkte und nicht als 12 Prozent angegeben hast.',
        'Check that the difference is expressed as 12 percentage points, not 12 percent.'));
    for (const number of ['2020', '2025', '36', '48']) {
      if (!new RegExp(`(^|\\D)${number}(?!\\d)`).test(answerText))
        missingElements.push(tr(lang, `Проверь, указано ли значение ${number}.`, `Prüfe, ob der Wert ${number} genannt wird.`, `Check whether you included ${number}.`));
    }
  }

  // Keep the first actionable revision steps visible rather than overwhelming
  // the learner with a long checklist. This is guidance, not a correctness score.
  return missingElements.slice(0, 3);
}
