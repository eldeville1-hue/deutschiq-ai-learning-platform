import { tr } from "../i18n/language";

// Source figures for the current B2 data-description exercise. Keep these
// separate from wording recognition so future exercises can supply other data.
export type B2DataFigures = { earlier: { year: number; percent: number }; later: { year: number; percent: number } };

const B2_DATA_DESCRIPTION: B2DataFigures = {
  earlier: { year: 2020, percent: 36 },
  later: { year: 2025, percent: 48 },
} as const;

export function getB2WritingReviewHints(exerciseId: string, answer: string, lang: Parameters<typeof tr>[0], figures: B2DataFigures = B2_DATA_DESCRIPTION): string[] {
  const answerText = answer.toLocaleLowerCase('de-DE').trim();
  const change = figures.later.percent - figures.earlier.percent;
  const isDefaultData = figures.earlier.year === 2020 && figures.earlier.percent === 36 && figures.later.year === 2025 && figures.later.percent === 48;
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
    const directionRu = change > 0 ? 'рост' : change < 0 ? 'снижение' : 'отсутствие изменений';
    const directionDe = change > 0 ? 'den Anstieg' : change < 0 ? 'den Rückgang' : 'die unveränderten Werte';
    const directionEn = change > 0 ? 'increase' : change < 0 ? 'decrease' : 'unchanged value';
    return [tr(lang,
      `Разверни описание данных: сопоставь ${figures.earlier.year} год (${figures.earlier.percent} %) и ${figures.later.year} год (${figures.later.percent} %), опиши ${directionRu} (${Math.abs(change)} процентных пунктов). Не придумывай причины изменения.`,
      `Baue deine Datenbeschreibung aus: Vergleiche ${figures.earlier.year} (${figures.earlier.percent} %) mit ${figures.later.year} (${figures.later.percent} %) und beschreibe ${directionDe} (${Math.abs(change)} Prozentpunkte). Erfinde keine Ursachen.`,
      `Develop your data description: compare ${figures.earlier.year} (${figures.earlier.percent}%) with ${figures.later.year} (${figures.later.percent}%) and describe the ${directionEn} (${Math.abs(change)} percentage points). Do not invent causes.`)];
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
    // The evidence-transfer scenario asks whether advertising caused the rise.
    // A bare causal assertion is not supported by two observations. Negated
    // claims ("nicht durch Werbung") must not trigger this guidance.
    const evidenceScenario = figures.earlier.year === 2020 && figures.earlier.percent === 25
      && figures.later.year === 2025 && figures.later.percent === 35;
    const assertsAdvertisingCause = /\\b(?:wegen|aufgrund|durch)\\s+(?:die\\s+)?werbung\\b|\\bwerbung\\s+(?:hat|habe)\\s+(?:den\\s+)?(?:anstieg|zuwachs|wachstum)\\s+(?:verursacht|bewirkt)\\b|\\bdurch\\s+(?:die\\s+)?werbung\\s+(?:wurde|wird)\\s+(?:der\\s+)?(?:anstieg|zuwachs|wachstum)\\s+(?:verursacht|bewirkt)\\b/i.test(answerText);
    const qualifiesCause = /\\b(?:nicht|kein(?:e|en|er)?|unbekannt|unklar|unbewiesen|unbelegt|nicht nachweisbar|nicht belegt)\\b/i.test(answerText);
    if (evidenceScenario && assertsAdvertisingCause && !qualifiesCause)
      missingElements.push(tr(lang,
        'Отдели наблюдение от причины: рост с 25 % до 35 % подтверждён, но влияние рекламы этими данными не доказано.',
        'Trenne Beobachtung und Ursache: Der Anstieg von 25 % auf 35 % ist belegt, eine Wirkung der Werbung aber nicht.',
        'Separate observation from cause: the rise from 25% to 35% is supported, but these figures do not establish an advertising effect.'));
    // Recognize local year/value relationships without scanning unrelated prose.
    const reversedPair = ([ [figures.earlier.year, figures.later.percent], [figures.later.year, figures.earlier.percent] ] as const).some(([year, value]) => {
      const yearFirst = new RegExp('\\b' + year + '\\b\\s*(?::|[–—-]|\\s+(?:(?:lag|betrug|waren|war)\\s+(?:(?:der\\s+anteil|die\\s+quote|der\\s+wert)\\s+)?(?:bei\\s+)?|bei\\s+))\\s*' + value + '(?=\\s|%|[.,;!?]|$)', 'i');
      const valueFirst = new RegExp('\\b' + value + '\\s*(?:%|prozent)\\s*(?:im\\s+jahr|in|für)\\s+' + year + '\\b', 'i');
      return yearFirst.test(answerText) || valueFirst.test(answerText);
    });
    if (reversedPair)
      missingElements.push(tr(lang,
        `Проверь соответствие данных: в ${figures.earlier.year} году было ${figures.earlier.percent} %, в ${figures.later.year} году — ${figures.later.percent} %.`,
        `Prüfe die Zuordnung: ${figures.earlier.year} waren es ${figures.earlier.percent} %, ${figures.later.year} waren es ${figures.later.percent} %.`,
        `Check the year-to-value pairing: ${figures.earlier.percent}% in ${figures.earlier.year} and ${figures.later.percent}% in ${figures.later.year}.`));
    // Detect only explicit claims of decline; do not infer meaning from
    // unrelated words such as "Rückgang" in a comparison or quoted opinion.
    const claimsDecline = /\b(?:der anteil|die quote|der wert|die zahl)\s+(?:ist|war|hat sich)\s+(?:gesunken|gefallen|verringert|reduziert)\b|\b(?:der anteil|die quote|der wert|die zahl)\s+(?:sank|fiel)\b/i.test(answerText) || /\b(?:der anteil|die quote|der wert|die zahl)\s+(?:ging|geht)\s+zurück\b|\b(?:der anteil|die quote|der wert|die zahl)\s+(?:nahm|nimmt)\s+ab\b/i.test(answerText);
    const claimsIncrease = /\b(?:der anteil|die quote|der wert|die zahl)\s+(?:ist|war|hat sich)\s+(?:gestiegen|gewachsen|erhöht|vergrößert)\b|\b(?:der anteil|die quote|der wert|die zahl)\s+(?:stieg|wuchs)\b/i.test(answerText) || /\b(?:der anteil|die quote|der wert|die zahl)\s+(?:nahm|nimmt)\s+zu\b/i.test(answerText);
    const claimsStable = /\b(?:der anteil|die quote|der wert|die zahl)\s+(?:ist|war|blieb)\s+(?:unverändert|gleich|stabil|konstant)\b|\b(?:keine veränderung|kein unterschied)\b/i.test(answerText) || /\b(?:der anteil|die quote|der wert|die zahl)\s+blieb\s+auf\s+(?:demselben|gleichem|dem gleichen)\s+niveau\b/i.test(answerText);
    if ((change > 0 && (claimsDecline || claimsStable)) || (change < 0 && (claimsIncrease || claimsStable)) || (change === 0 && (claimsIncrease || claimsDecline)))
      missingElements.push(tr(lang,
        `Проверь направление изменения: показатель ${change > 0 ? 'вырос' : change < 0 ? 'снизился' : 'не изменился'} с ${figures.earlier.percent} % до ${figures.later.percent} %.`,
        `Prüfe die Richtung der Veränderung: Der Wert ${change > 0 ? 'stieg' : change < 0 ? 'sank' : 'blieb unverändert'} von ${figures.earlier.percent} % auf ${figures.later.percent} %.`,
        `Check the direction of change: the value ${change > 0 ? 'increased' : change < 0 ? 'decreased' : 'remained unchanged'} from ${figures.earlier.percent}% to ${figures.later.percent}%.`));
    // Only interpret an explicit percentage-point difference; other
    // percentages may be base values or relative changes.
    const pointDifference = /\b(\d+(?:[.,]\d+)?)\s*(?:prozentpunkt(?:e|en)?|percentage[\s-]+points?)\b|\b(?:prozentpunkt(?:e|en)?|percentage[\s-]+points?)\s*(?:von\s+)?(\d+(?:[.,]\d+)?)\b/i;
    const matches = [...answerText.matchAll(new RegExp(pointDifference.source, "gi"))];
    const pointValues = matches.map(match => Number((match[1] || match[2]).replace(",", ".")));
    const correctPointDifference = pointValues.some(value => Math.abs(value - Math.abs(change)) < 0.001);
    const wrongPointDifference = pointValues.length > 0 && !correctPointDifference;
    if (wrongPointDifference)
      missingElements.push(tr(lang,
        `Проверь разницу: между ${figures.earlier.percent} % и ${figures.later.percent} % — ${Math.abs(change)} процентных пунктов.`,
        `Prüfe die Differenz: Zwischen ${figures.earlier.percent} % und ${figures.later.percent} % liegen ${Math.abs(change)} Prozentpunkte.`,
        `Check the difference: ${figures.earlier.percent}% to ${figures.later.percent}% is ${Math.abs(change)} percentage points.`));
    // Keep the established wording for the original lesson while making
    // the number-based unit check work for other exercise figures.
    const mentionsDifferenceInPoints = isDefaultData
      ? correctPointDifference || /\bzwölf\s+prozentpunkt(?:e|en)?\b/i.test(answerText)
      : correctPointDifference;
    const explicitlyWrongDifferenceUnit = /\b(?:anstieg|zunahme|differenz|unterschied|veränderung|steigerung)\b[^.!?]{0,65}?\b(?:um|von|beträgt|liegt bei|ist)\s+(?:nur\s+)?(?:12|zwölf)\s*(?:%|prozent)(?=\s|[.,;!?]|$)/i.test(answerText)
      || /\b(?:12|zwölf)\s*(?:%|prozent)(?=\s|[.,;!?]|$)[^.!?]{0,35}?\b(?:mehr|anstieg|zunahme|unterschied)\b/i.test(answerText);
    if (explicitlyWrongDifferenceUnit && isDefaultData)
      missingElements.push(tr(lang,
        'Исправь единицу изменения: рост с 36 % до 48 % составляет 12 процентных пунктов, а не 12 %.',
        'Korrigiere die Einheit: Von 36 % auf 48 % sind es 12 Prozentpunkte, nicht 12 %.',
        'Correct the change unit: 36% to 48% is 12 percentage points, not 12%.'));
    // In transfer tasks the point difference varies; check explicit unit
    // confusion against that exercise's numbers, not the original 12-point task.
    const statedChangeAsPercent = !isDefaultData && new RegExp(
      '(?:\\b(?:anstieg|zunahme|differenz|unterschied|veränderung|rückgang|abnahme)\\b[^.!?]{0,65}?(?:um|von|beträgt|liegt bei|ist)\\s+|\\bum\\s+)' +
      Math.abs(change) + '\\s*(?:%|prozent)(?=\\s|[.,;!?]|$)', 'i'
    ).test(answerText);
    if (statedChangeAsPercent)
      missingElements.push(tr(lang,
        `Проверь единицу изменения: от ${figures.earlier.percent} % до ${figures.later.percent} % — это ${Math.abs(change)} процентных пунктов, не ${Math.abs(change)} %.`,
        `Prüfe die Einheit: Von ${figures.earlier.percent} % auf ${figures.later.percent} % sind es ${Math.abs(change)} Prozentpunkte, nicht ${Math.abs(change)} %.`,
        `Check the unit: ${figures.earlier.percent}% to ${figures.later.percent}% is ${Math.abs(change)} percentage points, not ${Math.abs(change)}%.`));
    const describesNoChange = change === 0 && (claimsStable || /\b(?:blieb|bleibt|ist|war)\s+(?:unverändert|gleich|stabil|konstant)\b/i.test(answerText));
    if (!describesNoChange && !mentionsDifferenceInPoints && !explicitlyWrongDifferenceUnit && !statedChangeAsPercent && !wrongPointDifference)
      missingElements.push(tr(lang,
        `Проверь, указана ли разница именно в процентных пунктах (${Math.abs(change)}), а не в процентах.`,
        `Prüfe, ob du den Unterschied als ${Math.abs(change)} Prozentpunkte und nicht als Prozent angegeben hast.`,
        `Check that the difference is expressed as ${Math.abs(change)} percentage points, not percent.`));
    for (const number of [figures.earlier.year, figures.later.year, figures.earlier.percent, figures.later.percent].map(String)) {
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
