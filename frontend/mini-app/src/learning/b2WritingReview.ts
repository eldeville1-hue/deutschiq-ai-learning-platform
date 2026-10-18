import { tr } from "../i18n/language";

export function getB2WritingReviewHints(exerciseId: string, answer: string, lang: Parameters<typeof tr>[0]): string[] {
  const answerText = answer.toLocaleLowerCase('de-DE').trim();
  // Keyword presence is only a weak signal, never evidence of writing quality.
  // Avoid claiming that a very short or empty response meets the criteria.
  const minimumWords = 12;
  const words = answerText.match(/[\p{L}\p{N}]+/gu) || [];
  if (words.length < minimumWords && ['argument_structure-dialogue', 'counterargument-dialogue', 'data_description-dialogue'].includes(exerciseId)) {
    // Give a revision goal, not a ready-made answer. The model is available
    // separately only after the learner chooses to compare their own draft.
    if (exerciseId === 'argument_structure-dialogue')
      return [tr(lang,
        'Разверни свой довод: обозначь позицию, объясни причину и добавь собственный конкретный пример. Проверь, что пример действительно подтверждает причину.',
        'Baue dein Argument aus: Nenne deine Position, begründe sie und ergänze ein eigenes konkretes Beispiel. Prüfe, ob das Beispiel deinen Grund tatsächlich stützt.',
        'Develop your argument: state your position, explain your reason, and add your own concrete example. Check that your example supports your reason.')];
    if (exerciseId === 'counterargument-dialogue')
      return [tr(lang,
        'Разверни ответ: справедливо изложи опасение о расходах, затем приведи собственный контраргумент и обоснуй его.',
        'Baue deine Antwort aus: Stelle die Kostensorge fair dar, formuliere dann dein eigenes Gegenargument und begründe es.',
        'Develop your response: acknowledge the cost concern fairly, then give your own counterargument and explain why it matters.')];
    return [tr(lang,
      'Разверни описание данных: сопоставь 2020 год (36 %) и 2025 год (48 %), укажи рост на 12 процентных пунктов. Не придумывай причины изменения.',
      'Baue deine Datenbeschreibung aus: Vergleiche 2020 (36 %) mit 2025 (48 %) und nenne den Anstieg um 12 Prozentpunkte. Erfinde keine Ursachen.',
      'Develop your data description: compare 2020 (36%) with 2025 (48%) and describe the 12-percentage-point increase. Do not invent causes.')];
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
    // Also recognize explicit value-first pairs, e.g. "48 % im Jahr 2020".
    // Do not flag mere co-occurrence of values and years in a long sentence.
    const reversedValueFirstPair = /\b48\s*(?:%|prozent)\s*(?:im\s+jahr|in|für)\s+2020\b/i.test(answerText)
      || /\b36\s*(?:%|prozent)\s*(?:im\s+jahr|in|für)\s+2025\b/i.test(answerText);
    if (reversedPair || reversedValueFirstPair)
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
    // A draft can contain the correct unit elsewhere while explicitly
    // mislabelling the twelve-point change as twelve percent.
    const explicitlyWrongDifferenceUnit = /\b(?:anstieg|zunahme|differenz|unterschied|veränderung|steigerung)\b[^.!?]{0,65}?\b(?:um|von|beträgt|liegt bei|ist)\s+(?:nur\s+)?(?:12|zwölf)\s*(?:%|prozent)(?=\s|[.,;!?]|$)/i.test(answerText)
      || /\b(?:12|zwölf)\s*(?:%|prozent)(?=\s|[.,;!?]|$)[^.!?]{0,35}?\b(?:mehr|anstieg|zunahme|unterschied)\b/i.test(answerText);
    if (explicitlyWrongDifferenceUnit)
      missingElements.push(tr(lang,
        'Исправь единицу изменения: рост с 36 % до 48 % составляет 12 процентных пунктов, а не 12 %.',
        'Korrigiere die Einheit: Von 36 % auf 48 % sind es 12 Prozentpunkte, nicht 12 %.',
        'Correct the change unit: 36% to 48% is 12 percentage points, not 12%.'));
    if (!mentionsDifferenceInPoints && !explicitlyWrongDifferenceUnit)
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
