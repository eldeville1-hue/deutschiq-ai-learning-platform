export type ExerciseStage = 'guided' | 'independent' | 'transfer' | 'review' | 'checkpoint';

export type ExerciseKind =
  | 'choice'
  | 'analogy'
  | 'cloze'
  | 'reorder'
  | 'repair'
  | 'listen_choice'
  | 'speak'
  | 'write';

export type LearningExercise = {
  id?: string | number;
  type: string;
  stage?: ExerciseStage | string;
  question: string;
  answer?: string;
  options?: string[];
  tokens?: string[];
  hint?: string;
  model_answer?: string;
  audio_text?: string;
  analogy_source?: string;
  analogy_target?: string;
  pattern_label?: string;
  conversation_turns?: Array<{
    partner: string;
    goal: string;
    placeholder?: string;
    model?: string;
  }>;
};

export const exerciseKind = (exercise: LearningExercise): ExerciseKind => {
  if (exercise.type === 'reorder') return 'reorder';
  if (exercise.type === 'analogy_choice') return 'analogy';
  if (exercise.type === 'listening_choice') return 'listen_choice';
  if (['context_choice', 'choose', 'choice'].includes(exercise.type)) return 'choice';
  if (exercise.type === 'repeat' || exercise.type === 'speak') return 'speak';
  if (exercise.type === 'dialogue' || exercise.type === 'production' || exercise.type === 'write') return 'write';
  if (exercise.type === 'error_repair' || exercise.type === 'repair') return 'repair';
  return 'cloze';
};
