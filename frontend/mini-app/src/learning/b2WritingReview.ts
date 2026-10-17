import { tr } from "../i18n/language";

export function getB2WritingReviewHints(exerciseId: string, answer: string, lang: Parameters<typeof tr>[0]): string[] {
  const answerText = answer.toLocaleLowerCase('de-DE').trim();
  // Keyword presence is only a weak signal, never evidence of writing quality.
  // Avoid claiming that a very short or empty response meets the criteria.
  const minimumWords = 12;
  const words = answerText.match(/[\p{L}\p{N}]+/gu) || [];
  if (words.length < minimumWords && ['argument_structure-dialogue', 'counterargument-dialogue', 'data_description-dialogue'].includes(exerciseId)) {
    if (exerciseId === 'argument_structure-dialogue')
      return [tr(lang,
        'Разверни ответ: сформулируй позицию, объясни причину и добавь конкретный пример. Образец: Ich bin für sichere Radwege, weil sie Unfälle verhindern können. Zum Beispiel kommen Kinder so sicherer zur Schule. Nutze die Struktur, aber formuliere deine eigene Begründung und dein eigenes Beispiel.',
        'Baue deinen Text aus: Formuliere deine Position, begründe sie und ergänze ein konkretes Beispiel. Beispiel: Ich bin für sichere Radwege, weil sie Unfälle verhindern können. Zum Beispiel kommen Kinder so sicherer zur Schule. Nutze die Struktur, aber formuliere deine eigene Begründung und dein eigenes Beispiel.',
        'Develop your answer: state your position, explain why, and add a concrete example. Example: Ich bin für sichere Radwege, weil sie Unfälle verhindern können. Zum Beispiel kommen Kinder so sicherer zur Schule. Nutze die Struktur, aber formuliere deine eigene Begründung und dein eigenes Beispiel.')];
    if (exerciseId === 'counterargument-dialogue')
      return [tr(lang,
        'Разверни ответ: признай опасение о расходах и объясни, почему твой аргумент его перевешивает. Образец: Die Sorge um die Kosten ist verständlich. Langfristig kann die Modernisierung jedoch Energie sparen. Nutze die Struktur und antworte mit deinen eigenen Gründen.',
        'Baue deinen Text aus: Greife die Sorge um die Kosten auf und begründe deine Erwiderung. Beispiel: Die Sorge um die Kosten ist verständlich. Langfristig kann die Modernisierung jedoch Energie sparen. Nutze die Struktur und antworte mit deinen eigenen Gründen.',
        'Develop your answer: acknowledge the cost concern and explain your response. Example: Die Sorge um die Kosten ist verständlich. Langfristig kann die Modernisierung jedoch Energie sparen. Nutze die Struktur und antworte mit deinen eigenen Gründen.')];
    return [tr(lang,
      'Разверни описание: сравни 2020 год (36 %) и 2025 год (48 %) и назови разницу в процентных пунктах. Образец: Der Anteil stieg von 36 % im Jahr 2020 auf 48 % im Jahr 2025, also um 12 Prozentpunkte. Nutze die Struktur und beschreibe die Veränderung mit eigenen Worten.',
      'Baue deine Beschreibung aus: Vergleiche 2020 (36 %) mit 2025 (48 %) und nenne die Differenz in Prozentpunkten. Beispiel: Der Anteil stieg von 36 % im Jahr 2020 auf 48 % im Jahr 2025, also um 12 Prozentpunkte. Nutze die Struktur und beschreibe die Veränderung mit eigenen Worten.',
      'Develop your description: compare 2020 (36%) with 2025 (48%) and state the difference in percentage points. Example: Der Anteil stieg von 36 % im Jahr 2020 auf 48 % im Jahr 2025, also um 12 Prozentpunkte. Nutze die Struktur und beschreibe die Veränderung mit eigenen Worten.')];
  }
  const missingElements: string[] = [];
  if (exerciseId === 'argument_structure-dialogue') {
    if (!/\b(weil|denn|da|deshalb|daher|zumal|aufgrund|wegen|aus diesem grund|ein grund|führt dazu|trägt dazu bei|ermöglicht|bewirkt)\b/i.test(answerText))
      missingElements.push(tr(lang, 'Проверь, понятна ли причина твоей позиции. Её можно выразить разными способами.', 'Prüfe, ob deine Begründung deutlich wird. Du kannst sie unterschiedlich formulieren.', 'Check whether your reasoning is clear; there are several ways to express it.'));
    if (!/\b(zum beispiel|beispielsweise|etwa wenn|konkret|beispiel|belegen|zeigt sich|so könnte)\b/i.test(answerText))
      missingElements.push(tr(lang, 'Проверь, есть ли конкретный пример или доказательство.', 'Prüfe, ob ein konkretes Beispiel oder ein Beleg enthalten ist.', 'Check whether you included a concrete example or supporting evidence.'));
  } else if (exerciseId === 'counterargument-dialogue') {
    if (!/\b(zwar|obwohl|auch wenn|einerseits|verständlich|nachvollziehbar|es stimmt|ich verstehe|der einwand|die sorge|zugegeben)\b/i.test(answerText))
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
    // Detect only explicit claims of decline; do not infer meaning from
    // unrelated words such as "Rückgang" in a comparison or quoted opinion.
    const claimsDecline = /\b(?:der anteil|die quote|der wert|die zahl)\s+(?:ist|war|hat sich)\s+(?:gesunken|gefallen|verringert|reduziert)\b|\b(?:der anteil|die quote|der wert|die zahl)\s+(?:sank|fiel)\b/i.test(answerText);
    if (claimsDecline)
      missingElements.push(tr(lang,
        'Проверь направление изменения: показатель вырос с 36 % до 48 %.',
        'Prüfe die Richtung der Veränderung: Der Wert stieg von 36 % auf 48 %.',
        'Check the direction of change: the value increased from 36% to 48%.'));
    // A number and its unit must describe the same difference, not merely
    // appear in unrelated parts of the response.
    const mentionsDifferenceInPoints = /\b(?:12|zwölf)\s*(?:prozentpunkt(?:e|en)?|percentage[\s-]+points?)\b|\b(?:prozentpunkt(?:e|en)?|percentage[\s-]+points?)\s*(?:von\s+)?(?:12|zwölf)\b/i.test(answerText);
    if (!mentionsDifferenceInPoints)
      missingElements.push(tr(lang,
        'Проверь, указана ли разница именно в процентных пунктах (12), а не в процентах.',
        'Prüfe, ob du den Unterschied als 12 Prozentpunkte und nicht als 12 Prozent angegeben hast.',
        'Check that the difference is expressed as 12 percentage points, not 12 percent.'));
    for (const number of ['2020', '2025', '36', '48']) {
      if (!new RegExp(`(^|\\D)${number}(?!\\d)`).test(answerText))
        missingElements.push(tr(lang, `Проверь, указано ли значение ${number}.`, `Prüfe, ob der Wert ${number} genannt wird.`, `Check whether you included ${number}.`));
    }
  }

  // Complete numerical coverage still needs a human judgment about clarity
  // and interpretation; never silently equate an empty checklist with mastery.
  if (missingElements.length === 0 && exerciseId === 'data_description-dialogue') {
    missingElements.push(tr(lang,
      'Перечитай описание: понятно ли, что именно сравнивается, как изменился показатель и какой вывод подтверждают данные?',
      'Lies deine Beschreibung noch einmal: Ist klar, was verglichen wird, wie sich der Wert verändert hat und welche Schlussfolgerung die Daten stützen?',
      'Reread your description: Is it clear what is compared, how the value changed, and which conclusion the data supports?'));
  }
  // Even when common signal words are present, a checklist cannot establish
  // whether the argument is convincing or the objection is answered fairly.
  if (missingElements.length === 0 && exerciseId === 'argument_structure-dialogue') {
    missingElements.push(tr(lang,
      'Перечитай текст: ясно ли выражена твоя позиция и действительно ли пример подтверждает довод?',
      'Lies deinen Text noch einmal: Ist deine Position klar und stützt dein Beispiel wirklich die Begründung?',
      'Reread your draft: Is your position clear, and does your example actually support your reason?'));
  } else if (missingElements.length === 0 && exerciseId === 'counterargument-dialogue') {
    missingElements.push(tr(lang,
      'Перечитай текст: честно ли представлено возражение и объяснено ли, почему твой ответ убедителен?',
      'Lies deinen Text noch einmal: Ist der Einwand fair dargestellt und ist deine Erwiderung nachvollziehbar begründet?',
      'Reread your draft: Is the objection represented fairly, and is your response supported by reasoning?'));
  }
  // Keep the first actionable revision steps visible rather than overwhelming
  // the learner with a long checklist. This is guidance, not a correctness score.
  return missingElements.slice(0, 3);
}
