export type LearningPhaseKind = 'review' | 'repair' | 'learn' | 'mission';

export type LearningPhase = {
  kind: LearningPhaseKind;
  count?: number;
  minutes?: number;
};

export type JourneyLesson = {
  id: number;
  topic: string;
  title: string;
  level: string;
  track: string;
  week: number;
  moduleTitle: string;
  moduleStep: number | null;
  moduleSize: number | null;
  scenario: string;
  canDo: string;
  minutes: number;
  completed: boolean;
  recommended: boolean;
  mastery: number | null;
  attempts: number;
  evidenceStatus: 'not_enough_evidence' | 'building' | 'retained' | 'needs_review';
  blockedBy: string[];
};

const text = (value: unknown) => typeof value === 'string' ? value.trim() : '';
const positiveNumber = (value: unknown, fallback = 0) => {
  const number = Number(value);
  return Number.isFinite(number) && number > 0 ? number : fallback;
};

export const normalizeJourneyLesson = (value: unknown): JourneyLesson | null => {
  if (!value || typeof value !== 'object') return null;
  const item = value as Record<string, unknown>;
  const id = positiveNumber(item.id);
  const topic = text(item.topic);
  const title = text(item.title);
  if (!id || (!topic && !title)) return null;

  return {
    id,
    topic,
    title,
    level: text(item.level) || text(item.track) || 'A1',
    track: text(item.track) || text(item.level) || 'A1',
    week: positiveNumber(item.week, 1),
    moduleTitle: text(item.module_title) || text(item.week_title),
    moduleStep: positiveNumber(item.module_step || item.day) || null,
    moduleSize: positiveNumber(item.module_size) || null,
    scenario: text(item.scenario),
    canDo: text(item.can_do) || text(item.objective),
    minutes: positiveNumber(item.minutes || item.estimated_time, 6),
    completed: Boolean(item.completed),
    recommended: Boolean(item.recommended),
    mastery: item.mastery == null ? null : Math.max(0, Math.min(100, Number(item.mastery) || 0)),
    attempts: positiveNumber(item.attempts),
    evidenceStatus: ['not_enough_evidence', 'building', 'retained', 'needs_review'].includes(String(item.evidence_status))
      ? item.evidence_status as JourneyLesson['evidenceStatus']
      : 'not_enough_evidence',
    blockedBy: Array.isArray(item.blocked_by) ? item.blocked_by.map(String) : [],
  };
};

export const normalizeJourneyLessons = (value: unknown): JourneyLesson[] => (
  Array.isArray(value)
    ? value.map(normalizeJourneyLesson).filter((item): item is JourneyLesson => Boolean(item))
    : []
);

export const selectCurrentLesson = (lessons: JourneyLesson[]) => (
  lessons.find(item => item.recommended)
  || lessons.find(item => !item.completed && item.blockedBy.length === 0)
  || lessons.find(item => !item.completed)
  || lessons[0]
  || null
);

export const normalizeLearningPhases = (value: unknown): LearningPhase[] => {
  if (!Array.isArray(value)) return [];
  return value.flatMap(item => {
    if (!item || typeof item !== 'object') return [];
    const phase = item as Record<string, unknown>;
    if (!['review', 'repair', 'learn', 'mission'].includes(String(phase.kind))) return [];
    return [{
      kind: String(phase.kind) as LearningPhaseKind,
      count: positiveNumber(phase.count) || undefined,
      minutes: positiveNumber(phase.minutes) || undefined,
    }];
  });
};
