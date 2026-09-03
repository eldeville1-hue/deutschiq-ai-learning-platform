type Language = 'de' | 'ru';

const translations = {
  de: {
    // ===== НАВИГАЦИЯ =====
    nav: {
      overview: "Übersicht",
      analysis: "Analyse",
      plan: "Lernplan",
      tutor: "KI-Tutor",
      profile: "Profil",
    },

    // ===== ПРИВЕТСТВИЕ =====
    welcome: {
      title: "Dein persönlicher Deutsch-Lernassistent",
      startDiagnostic: "Diagnose starten",
      myPlan: "Mein Lernplan",
      subtitle: "Erstelle deinen persönlichen Lernplan",
    },

    // ===== ГЛАВНАЯ =====
    dashboard: {
      title: "Dein persönlicher Deutsch-Lernassistent",
      goodJob: "Gut gemacht!",
      subtext: "Du bist auf einem starken Weg!",
      levelLabel: "Oberes Mittelstufenniveau",
      target: "Ziel: B2 – 60% erreicht",
      stats: [
        { label: "Grammatik", value: "6.8", trend: "up" },
        { label: "Aussprache", value: "7.2", trend: "up" },
        { label: "Wortschatz", value: "5.4", trend: "down" },
        { label: "Hörverstehen", value: "8.1", trend: "up" },
      ],
      weaknesses: {
        title: "Verbesserungspotenzial",
        items: [
          { name: "Fälle (Dativ/Akkusativ)", percent: 31 },
          { name: "Nomen-Verb-Verbindungen", percent: 28 },
          { name: "Konjunktiv II", percent: 24 },
        ],
      },
    },

    // ===== ДИАГНОСТИКА =====
    diagnostic: {
      title: "Diagnose",
      question: "Frage {current} von {total}",
      finish: "Abschließen",
      loading: "Fragen werden geladen...",
      noQuestions: "Keine Fragen. Überprüfen Sie die API.",
      submit: "Ergebnisse anzeigen",
    },

    // ===== РЕЗУЛЬТАТЫ =====
    result: {
      title: "Ihr Ergebnis",
      level: "Ihr Niveau: {level}",
      overall: "Gesamtpunktzahl: {score}%",
      pillars: {
        grammar: "Grammatik",
        vocabulary: "Wortschatz",
        listening: "Hörverstehen",
        pronunciation: "Aussprache",
      },
      weaknesses: "Schwächen",
      noWeaknesses: "Hervorragend! Keine Schwächen gefunden.",
      toPlan: "Zum Plan",
      backToHome: "Zur Startseite",
    },

    // ===== ПЛАН (ДОБАВЛЕНЫ КЛЮЧИ) =====
    plan: {
      title: "Ihr Lernplan",
      empty: "Sie haben noch keine Lektionen. Machen Sie den Diagnosetest!",
      toDiagnostic: "Diagnose machen",
      lessonsCount: "{count} Lektionen, die Ihre Schwächen abdecken",
      weaknessesTitle: "Ihre Schwächen",
      weaknessesSubtext: "Diese Themen werden in der Pro-Version abgedeckt",
      noWeaknesses: "Machen Sie den Diagnosetest, um Ihre Schwächen zu sehen",
      locked: "Pro",
      freePlan: "Kostenlos",
      unlockAll: "🔓 Alle Lektionen freischalten",
      unlockSubtext: "Zugang zu personalisierten Übungen, KI-Tutor und vollem Plan",
      oneTime: "Einmalzahlung über Telegram Stars",
      proActive: "⭐ Pro-Zugang aktiv!",
      proDescription: "Alle Lektionen und Funktionen sind freigeschaltet",
    },

    // ===== УРОК =====
    lesson: {
      back: "Zurück",
      complete: "📚 Lektion abschließen",
      completed: "✅ Lektion abgeschlossen!",
      toPlan: "📋 Zurück zur Übersicht",
      generate: "🎯 Personalisierte Übungen generieren",
      generating: "Generiere...",
      exercises: "Übungen",
      personalizedExercises: "Personalisierte Übungen",
      rule: "Regel",
      examples: "Beispiele",
      commonMistakes: "Häufige Fehler",
      check: "Prüfen",
      correct: "✅ Richtig!",
      incorrect: "❌ Falsch. Richtige Antwort: {answer}",
      hint: "💡 {hint}",
      type: "Typ",
      audio: "🔊 Hören Sie zu:",
      minutes: "Min.",
    },

    // ===== ТЬЮТОР =====
    tutor: {
      title: "KI-Tutor",
      subtitle: "Stellen Sie eine Frage zur deutschen Sprache",
      placeholder: "Zum Beispiel: Wie wird das Perfekt mit 'sein' gebildet?",
      ask: "Fragen",
      thinking: "Denke nach...",
      answer: "Antwort:",
    },

    // ===== ПРОФИЛЬ =====
    profile: {
      title: "Profil",
      level: "Niveau",
      xp: "XP",
      streak: "Serie",
      subscription: "Abonnement",
      settings: "⚙️ Einstellungen",
      language: "Sprache",
      theme: "Design",
      upgrade: "🚀 Upgrade auf Pro",
      free: "Kostenlos",
      pro: "⭐ Pro",
      back: "Zurück",
      badges: "🏅 Erfolge",
      noBadges: "Noch keine Erfolge",
    },

    // ===== АНАЛИТИКА =====
    analytics: {
      title: "Analyse",
      subtitle: "Ihr Fortschritt im Überblick",
      overall: "Gesamtfortschritt",
      levelProgress: "Level-Fortschritt",
      pillars: "Pillar-Entwicklung",
      weeks: "Letzte 4 Wochen",
      badges: "Abzeichen",
      noData: "Noch keine Daten. Machen Sie die Diagnose!",
    },

    // ===== ОБЩЕЕ =====
    common: {
      loading: "Laden...",
      error: "Fehler",
      back: "Zurück",
      continue: "Weiter",
      save: "Speichern",
      cancel: "Abbrechen",
    },
  },

  // ================================================
  // РУССКАЯ ВЕРСИЯ
  // ================================================

  ru: {
    // ===== НАВИГАЦИЯ =====
    nav: {
      overview: "Обзор",
      analysis: "Анализ",
      plan: "План",
      tutor: "ИИ-репетитор",
      profile: "Профиль",
    },

    // ===== ПРИВЕТСТВИЕ =====
    welcome: {
      title: "Твой персональный помощник по немецкому",
      startDiagnostic: "Начать диагностику",
      myPlan: "Мой план",
      subtitle: "Создай свой персональный план обучения",
    },

    // ===== ГЛАВНАЯ =====
    dashboard: {
      title: "Твой персональный помощник по немецкому",
      goodJob: "Отлично!",
      subtext: "Ты на верном пути!",
      levelLabel: "Выше среднего",
      target: "Цель: B2 – 60% достигнуто",
      stats: [
        { label: "Грамматика", value: "6.8", trend: "up" },
        { label: "Произношение", value: "7.2", trend: "up" },
        { label: "Словарный запас", value: "5.4", trend: "down" },
        { label: "Аудирование", value: "8.1", trend: "up" },
      ],
      weaknesses: {
        title: "Слабые места",
        items: [
          { name: "Падежи (Dativ/Akkusativ)", percent: 31 },
          { name: "Глагольные связки", percent: 28 },
          { name: "Konjunktiv II", percent: 24 },
        ],
      },
    },

    // ===== ДИАГНОСТИКА =====
    diagnostic: {
      title: "Диагностика",
      question: "Вопрос {current} из {total}",
      finish: "Завершить",
      loading: "Загрузка вопросов...",
      noQuestions: "Нет вопросов. Проверьте API.",
      submit: "Показать результаты",
    },

    // ===== РЕЗУЛЬТАТЫ =====
    result: {
      title: "Ваш результат",
      level: "Ваш уровень: {level}",
      overall: "Общий балл: {score}%",
      pillars: {
        grammar: "Грамматика",
        vocabulary: "Лексика",
        listening: "Аудирование",
        pronunciation: "Произношение",
      },
      weaknesses: "Слабые места",
      noWeaknesses: "Отлично! Слабых мест не найдено.",
      toPlan: "Перейти к плану",
      backToHome: "На главную",
    },

    // ===== ПЛАН (ДОБАВЛЕНЫ КЛЮЧИ) =====
    plan: {
      title: "Ваш план обучения",
      empty: "У вас пока нет уроков. Пройдите диагностику!",
      toDiagnostic: "Пройти диагностику",
      lessonsCount: "{count} уроков, которые помогут закрыть ваши слабые места",
      weaknessesTitle: "Ваши слабые места",
      weaknessesSubtext: "Эти темы закрыты в Pro-версии",
      noWeaknesses: "Пройдите диагностику, чтобы увидеть свои слабые места",
      locked: "Pro",
      freePlan: "Бесплатно",
      unlockAll: "🔓 Откройте все уроки",
      unlockSubtext: "Доступ к персонализированным упражнениям, AI-тьютору и полному плану",
      oneTime: "Разовая оплата через Telegram Stars",
      proActive: "⭐ Pro-доступ активен!",
      proDescription: "Все уроки и функции открыты",
    },

    // ===== УРОК =====
    lesson: {
      back: "Назад",
      complete: "📚 Завершить урок",
      completed: "✅ Урок завершён!",
      toPlan: "📋 К списку уроков",
      generate: "🎯 Сгенерировать персонализированные упражнения",
      generating: "Генерация...",
      exercises: "Упражнения",
      personalizedExercises: "Персонализированные упражнения",
      rule: "Правило",
      examples: "Примеры",
      commonMistakes: "Частые ошибки",
      check: "Проверить",
      correct: "✅ Правильно!",
      incorrect: "❌ Неправильно. Правильный ответ: {answer}",
      hint: "💡 {hint}",
      type: "Тип",
      audio: "🔊 Прослушайте:",
      minutes: "мин.",
    },

    // ===== ТЬЮТОР =====
    tutor: {
      title: "ИИ-репетитор",
      subtitle: "Задайте вопрос по немецкому языку",
      placeholder: "Например: Как образуется Perfekt с 'sein'?",
      ask: "Спросить",
      thinking: "Думаю...",
      answer: "Ответ:",
    },

    // ===== ПРОФИЛЬ =====
    profile: {
      title: "Профиль",
      level: "Уровень",
      xp: "XP",
      streak: "Серия",
      subscription: "Подписка",
      settings: "⚙️ Настройки",
      language: "Язык",
      theme: "Тема",
      upgrade: "🚀 Купить Pro",
      free: "Бесплатно",
      pro: "⭐ Pro",
      back: "Назад",
      badges: "🏅 Достижения",
      noBadges: "Пока нет достижений",
    },

    // ===== АНАЛИТИКА =====
    analytics: {
      title: "Анализ",
      subtitle: "Ваш прогресс в цифрах",
      overall: "Общий прогресс",
      levelProgress: "Прогресс уровня",
      pillars: "Развитие по разделам",
      weeks: "Последние 4 недели",
      badges: "Достижения",
      noData: "Пока нет данных. Пройдите диагностику!",
    },

    // ===== ОБЩЕЕ =====
    common: {
      loading: "Загрузка...",
      error: "Ошибка",
      back: "Назад",
      continue: "Продолжить",
      save: "Сохранить",
      cancel: "Отмена",
    },
  },
};

export const getText = (lang: Language) => translations[lang];
