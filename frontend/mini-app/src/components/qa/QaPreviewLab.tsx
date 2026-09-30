import React, { useEffect, useMemo, useState } from 'react';
import {
  FaArrowRight, FaBookOpen, FaCheck, FaExclamationTriangle, FaEye, FaGraduationCap,
  FaHome, FaLock, FaMicrophoneSlash, FaPlaneDeparture, FaRedo, FaRoute,
  FaSignal, FaTimes, FaWifi,
} from 'react-icons/fa';
import { api } from '../../services/api';
import { ExerciseInteraction } from '../learning/ExerciseInteraction';
import { LessonCompletion } from '../learning/LessonCompletion';
import type { AppLanguage } from '../../i18n/language';

type QaSurface = 'overview' | 'plan' | 'lesson' | 'checkpoint' | 'promotion';
type QaLearner = 'new' | 'active' | 'review' | 'graduation';
type QaState = 'ready' | 'loading' | 'offline' | 'error' | 'wrong' | 'retry' | 'complete' | 'pass' | 'fail' | 'mic_denied';

type Props = {
  accessKey: string;
  catalog: any[];
};

const copy = {
  ru: {
    preview: 'ПРЕДПРОСМОТР · БЕЗ ЗАПИСИ ДАННЫХ', today: 'ТВОЙ ШАГ СЕГОДНЯ',
    greeting: 'Доброе утро', learner: 'Дарья', review: '4 на повторение', progress: 'Прогресс',
    start: 'Начать с повторения', continue: 'Продолжить', route: 'ТВОЙ МАРШРУТ', next: 'Следующие шаги',
    lesson: 'ТЕКУЩИЙ УРОК', canDo: 'ПОСЛЕ УРОКА', check: 'Проверить', wrong: 'Исправь только эту часть',
    retry: 'Ещё одна попытка', checkpoint: 'ВЫПУСКНАЯ МИССИЯ', independent: 'Ответь самостоятельно — без подсказок.',
    passed: 'Уровень завершён', failed: 'Нужна одна короткая тренировка', startLevel: 'Начать A2', repair: 'Исправить слабое место',
    loading: 'Загружаем твой маршрут…', offline: 'Нет сети', offlineBody: 'Сохранённый урок доступен. Результат отправится позже.',
    error: 'Не удалось загрузить экран', errorBody: 'Прогресс сохранён. Попробуй ещё раз.', again: 'Повторить',
    mic: 'Микрофон недоступен', micBody: 'Можно написать ответ — урок не блокируется.', typeInstead: 'Написать ответ',
    newTitle: 'Немецкий, который подстраивается под тебя', newBody: 'Короткая диагностика найдёт правильную точку старта.', diagnose: 'Узнать свой уровень',
  },
  de: {
    preview: 'VORSCHAU · KEINE LERNDATEN', today: 'DEIN SCHRITT HEUTE',
    greeting: 'Guten Morgen', learner: 'Daria', review: '4 Wiederholungen', progress: 'Fortschritt',
    start: 'Mit Wiederholung starten', continue: 'Weiter', route: 'DEIN LERNWEG', next: 'Nächste Schritte',
    lesson: 'AKTUELLE LEKTION', canDo: 'NACH DIESER LEKTION', check: 'Prüfen', wrong: 'Korrigiere nur diesen Teil',
    retry: 'Noch ein Versuch', checkpoint: 'ABSCHLUSSMISSION', independent: 'Antworte selbstständig – ohne Hinweise.',
    passed: 'Niveau abgeschlossen', failed: 'Eine kurze Übung fehlt noch', startLevel: 'A2 starten', repair: 'Schwäche gezielt üben',
    loading: 'Dein Lernweg wird geladen…', offline: 'Keine Verbindung', offlineBody: 'Die gespeicherte Lektion ist verfügbar. Das Ergebnis wird später gesendet.',
    error: 'Diese Ansicht konnte nicht geladen werden', errorBody: 'Dein Fortschritt ist sicher. Versuche es erneut.', again: 'Erneut versuchen',
    mic: 'Mikrofon nicht verfügbar', micBody: 'Du kannst deine Antwort schreiben – die Lektion bleibt offen.', typeInstead: 'Antwort schreiben',
    newTitle: 'Deutsch, das sich an dich anpasst', newBody: 'Eine kurze Einstufung findet deinen richtigen Startpunkt.', diagnose: 'Mein Niveau finden',
  },
} as const;

const surfaceOptions: Array<[QaSurface, string]> = [
  ['overview', 'Overview'], ['plan', 'Plan'], ['lesson', 'Lesson'], ['checkpoint', 'Graduation'], ['promotion', 'Promotion'],
];
const stateOptions: Array<[QaState, string]> = [
  ['ready', 'Ready'], ['loading', 'Loading'], ['offline', 'Offline'], ['error', 'Server error'],
  ['wrong', 'Wrong answer'], ['retry', 'Retry'], ['complete', 'Complete'], ['pass', 'Checkpoint passed'],
  ['fail', 'Checkpoint failed'], ['mic_denied', 'Microphone denied'],
];

const StateSurface: React.FC<{ state: QaState; lang: 'ru' | 'de' }> = ({ state, lang }) => {
  const t = copy[lang];
  if (state === 'loading') return <div className="qa-system-state loading"><span className="qa-spinner" /><strong>{t.loading}</strong><i /><i /><i /></div>;
  if (state === 'offline') return <div className="qa-system-state"><FaWifi /><strong>{t.offline}</strong><p>{t.offlineBody}</p><button>{t.continue}</button></div>;
  if (state === 'error') return <div className="qa-system-state danger"><FaExclamationTriangle /><strong>{t.error}</strong><p>{t.errorBody}</p><button>{t.again}</button></div>;
  if (state === 'mic_denied') return <div className="qa-system-state"><FaMicrophoneSlash /><strong>{t.mic}</strong><p>{t.micBody}</p><button>{t.typeInstead}</button></div>;
  return null;
};

const PreviewNav: React.FC<{ active: QaSurface }> = ({ active }) => <nav className="qa-preview-nav" aria-hidden="true">
  <span className={active === 'overview' ? 'active' : ''}><FaHome /></span>
  <span className={active === 'plan' ? 'active' : ''}><FaRoute /></span>
  <span className={active === 'lesson' ? 'active' : ''}><FaBookOpen /></span>
  <span><FaGraduationCap /></span>
</nav>;

export const QaPreviewLab: React.FC<Props> = ({ accessKey, catalog }) => {
  const [surface, setSurface] = useState<QaSurface>('overview');
  const [learner, setLearner] = useState<QaLearner>('active');
  const [state, setState] = useState<QaState>('ready');
  const [level, setLevel] = useState('A1');
  const [lang, setLang] = useState<'ru' | 'de'>('ru');
  const [deviceWidth, setDeviceWidth] = useState(390);
  const [keyboard, setKeyboard] = useState(false);
  const [lessonId, setLessonId] = useState(0);
  const [lesson, setLesson] = useState<any>(null);
  const [lessonLoading, setLessonLoading] = useState(false);
  const [answer, setAnswer] = useState('');
  const levelLessons = useMemo(() => catalog.filter(item => item.level === level), [catalog, level]);
  const selectedCatalogLesson = useMemo(() => catalog.find(item => item.id === lessonId), [catalog, lessonId]);
  const exercise = lesson?.content?.exercises?.[Math.min(1, (lesson?.content?.exercises?.length || 1) - 1)];
  const t = copy[lang];

  useEffect(() => {
    const first = levelLessons[0];
    if (first && !levelLessons.some(item => item.id === lessonId)) setLessonId(first.id);
  }, [lessonId, levelLessons]);

  useEffect(() => {
    if (!lessonId) return;
    setLessonLoading(true);
    api.getCurriculumPreviewLesson(accessKey, lessonId, lang as AppLanguage)
      .then(value => { setLesson(value); setAnswer(''); })
      .catch(() => setLesson(null))
      .finally(() => setLessonLoading(false));
  }, [accessKey, lang, lessonId]);

  useEffect(() => {
    if (state === 'wrong') setAnswer('Ich komme aus Hamburg seit zwei Jahre.');
    else if (state === 'complete' || state === 'pass') setAnswer('Ich komme aus Kyiv und wohne jetzt in Hamburg.');
    else setAnswer('');
  }, [state]);

  const exceptional = ['loading', 'offline', 'error', 'mic_denied'].includes(state);
  const title = lesson?.content?.title || (lang === 'ru' ? 'Рассказать, откуда ты' : 'Sagen, woher du kommst');
  const canDo = lesson?.content?.success_evidence || lesson?.content?.can_do || lesson?.content?.objective || (lang === 'ru' ? 'Ты можешь коротко представиться.' : 'Du kannst dich kurz vorstellen.');
  const scenario = lesson?.content?.scenario || (lang === 'ru' ? 'Кто-то на курсе спрашивает, откуда ты.' : 'Jemand im Kurs fragt, woher du kommst.');

  const renderOverview = () => learner === 'new' ? <section className="qa-new-user">
    <span className="qa-brand-orbit">Q</span><small>DEUTSCHIQ</small><h2>{t.newTitle}</h2><p>{t.newBody}</p><button>{t.diagnose}<FaArrowRight /></button>
  </section> : <section className="qa-overview-screen">
    <header><div><small>{t.greeting}</small><strong>{t.learner}</strong></div><span>🔥 {learner === 'review' ? 7 : 4}</span></header>
    <div className="qa-level-line"><b>{level}</b><span><i style={{ height: learner === 'graduation' ? '100%' : '42%' }} /></span><small>{level === 'A1' ? 'A2' : 'B1'}</small></div>
    <article><small>{t.today}</small><em>{learner === 'graduation' ? '20/20' : '2/5'}</em><h2>{learner === 'graduation' ? t.checkpoint : title}</h2><p>{learner === 'graduation' ? t.independent : scenario}</p><div><FaCheck /><span><small>{t.canDo}</small><strong>{canDo}</strong></span></div><button>{learner === 'review' ? t.start : t.continue}<FaArrowRight /></button></article>
    <footer><FaRedo /><span><b>{learner === 'review' ? 4 : 2}</b><small>{t.review}</small></span><a>{t.progress} →</a></footer>
  </section>;

  const renderPlan = () => <section className="qa-plan-screen">
    <small>{t.route}</small><h2>{level} <span>→</span> {level === 'A1' ? 'A2' : 'B1'}</h2>
    <div className="qa-level-picker">{['A1','A2','B1','B2'].map((item, index) => <span className={item === level ? 'active' : index > (level === 'A1' ? 0 : 1) ? 'locked' : 'done'} key={item}>{item}{index > (level === 'A1' ? 0 : 1) && <FaLock />}</span>)}</div>
    <header><small>MODULE 1 · {learner === 'graduation' ? '20/20' : '2/20'}</small><b>{t.next}</b><em>{learner === 'graduation' ? '100%' : '10%'}</em></header>
    <div className="qa-plan-list">{[0,1,2,3].map(index => <article className={index === 0 ? 'done' : index === 1 ? 'current' : 'locked'} key={index}><span>{index === 0 ? <FaCheck /> : index === 1 ? '02' : <FaLock />}</span><div><strong>{index === 0 ? (lang === 'ru' ? 'Поздороваться' : 'Jemanden begrüßen') : index === 1 ? title : lang === 'ru' ? 'Следующая ситуация' : 'Nächste Situation'}</strong><small>{index === 0 ? (lang === 'ru' ? 'Завершено' : 'Abgeschlossen') : index === 1 ? (lang === 'ru' ? 'Готово к старту' : 'Startklar') : (lang === 'ru' ? 'Сначала предыдущий шаг' : 'Zuerst den vorherigen Schritt')}</small></div>{index < 2 && <FaArrowRight />}</article>)}</div>
  </section>;

  const renderLesson = () => {
    if (state === 'complete' || state === 'retry') return <LessonCompletion lang={lang} state="ready" outcome={{ passed: state === 'complete', first_try_correct: 3, corrected_retries: 1, needs_review: state === 'retry' ? 1 : 0, exercise_count: 4, mastery: state === 'complete' ? 78 : 55, xp_gained: state === 'complete' ? 40 : 0, mission_score: state === 'complete' ? 84 : 58, mission_answer: answer || 'Ich komme aus Kyiv und wohne jetzt in Hamburg.', mission_model: 'Ich komme aus Kyiv und wohne seit zwei Jahren in Hamburg.', review_in_days: 1 }} content={lesson?.content || { can_do: canDo }} skillTitle={title} milestoneSent={true} onRetrySave={() => undefined} onFinish={() => undefined} onBackToPlan={() => undefined} onRate={() => undefined} />;
    return <section className="qa-lesson-screen">
      <header><small>{t.lesson}</small><span>2/5</span></header><div className="qa-progress"><i /></div><h2>{exercise?.question || title}</h2><p>{exercise?.instruction || scenario}</p>
      {exercise ? <ExerciseInteraction exercise={{ ...exercise, id: `qa-${lessonId}` }} answer={answer} onAnswer={setAnswer} disabled={state === 'wrong'} lang={lang} /> : <textarea value={answer} onChange={event => setAnswer(event.target.value)} placeholder="…" />}
      {state === 'wrong' && <div className="qa-feedback wrong"><FaTimes /><span><strong>{t.wrong}</strong><p>{exercise?.explanation || 'seit zwei Jahren'}</p></span></div>}
      <button className="qa-primary">{state === 'wrong' ? t.retry : t.check}<FaArrowRight /></button>
    </section>;
  };

  const renderCheckpoint = () => <section className={`qa-checkpoint-screen ${state === 'pass' ? 'passed' : state === 'fail' ? 'failed' : ''}`}>
    <span>{state === 'pass' ? <FaGraduationCap /> : state === 'fail' ? <FaRedo /> : <FaPlaneDeparture />}</span><small>{t.checkpoint}</small>
    <h2>{state === 'pass' ? t.passed : state === 'fail' ? t.failed : title}</h2><p>{state === 'ready' ? t.independent : canDo}</p>
    {state === 'pass' && <div className="qa-evidence"><b>82%</b><span>A1 ✓ · 0% → A2</span></div>}
    {state === 'fail' && <div className="qa-evidence"><b>63%</b><span>{lang === 'ru' ? 'Порядок слов · 1 миссия' : 'Wortstellung · 1 Mission'}</span></div>}
    <button>{state === 'pass' ? t.startLevel : state === 'fail' ? t.repair : t.continue}<FaArrowRight /></button>
  </section>;

  const renderPromotion = () => <section className="qa-promotion-screen"><span><FaGraduationCap /></span><small>A1 · COMPLETE</small><h2>{t.passed}</h2><p>{lang === 'ru' ? 'Ты доказала навык в четырёх реальных разговорах.' : 'Du hast dein Können in vier echten Gesprächen gezeigt.'}</p><div><b>A1</b><FaArrowRight /><b>A2</b></div><button>{t.startLevel}<FaArrowRight /></button></section>;

  const body = exceptional ? <StateSurface state={state} lang={lang} /> : surface === 'overview' ? renderOverview() : surface === 'plan' ? renderPlan() : surface === 'lesson' ? renderLesson() : surface === 'checkpoint' ? renderCheckpoint() : renderPromotion();

  return <section className="control-panel control-wide qa-lab" data-testid="qa-lab">
    <header><FaEye /><div><small>OWNER QA · READ ONLY</small><h2>Journey preview</h2><p>Every state uses deterministic data. Nothing here creates sessions, XP, mastery, reviews, or analytics.</p></div></header>
    <div className="qa-toolbar">
      <label>Screen<select aria-label="Preview screen" value={surface} onChange={event => setSurface(event.target.value as QaSurface)}>{surfaceOptions.map(([value,label]) => <option key={value} value={value}>{label}</option>)}</select></label>
      <label>Learner<select aria-label="Learner state" value={learner} onChange={event => setLearner(event.target.value as QaLearner)}><option value="new">New learner</option><option value="active">Active learner</option><option value="review">Review due</option><option value="graduation">Graduation ready</option></select></label>
      <label>UI state<select aria-label="Interface state" value={state} onChange={event => setState(event.target.value as QaState)}>{stateOptions.map(([value,label]) => <option key={value} value={value}>{label}</option>)}</select></label>
      <label>Level<select aria-label="Preview level" value={level} onChange={event => setLevel(event.target.value)}>{['A1','A2','B1','B2'].map(item => <option key={item}>{item}</option>)}</select></label>
      <label>Lesson<select aria-label="Preview lesson" value={lessonId} onChange={event => setLessonId(Number(event.target.value))}>{levelLessons.map(item => <option key={item.id} value={item.id}>{item.day || '—'} · {item.title}</option>)}</select></label>
      <label>Language<select aria-label="Preview language" value={lang} onChange={event => setLang(event.target.value as 'ru'|'de')}><option value="ru">RU</option><option value="de">DE</option></select></label>
      <label>Phone<select aria-label="Preview width" value={deviceWidth} onChange={event => setDeviceWidth(Number(event.target.value))}>{[320,360,390,430].map(width => <option key={width} value={width}>{width}px</option>)}</select></label>
      <label className="qa-toggle"><input type="checkbox" checked={keyboard} onChange={event => setKeyboard(event.target.checked)} /> Keyboard</label>
    </div>
    <div className="qa-status-strip"><span><FaSignal /> Protected owner route</span><span><FaCheck /> Analytics excluded</span><span><FaCheck /> Learner writes blocked</span><span>{deviceWidth}px · {lang.toUpperCase()} · {surface}</span></div>
    <div className="qa-workbench">
      <aside>
        <strong>Publishing gate</strong>
        <span className={selectedCatalogLesson?.publish_ready ? 'gate-pass' : 'gate-fail'}>{selectedCatalogLesson?.publish_ready ? <FaCheck /> : <FaTimes />}{selectedCatalogLesson?.publish_ready ? 'Ready to publish' : 'Publishing blocked'}</span>
        {([
          ['RU copy reviewed', selectedCatalogLesson?.reviewed_languages?.includes('ru')],
          ['DE copy reviewed', selectedCatalogLesson?.reviewed_languages?.includes('de')],
          ['Changed-context review', selectedCatalogLesson?.delayed_review_method === 'changed_context_retrieval'],
        ] as Array<[string, boolean]>).map(([label, passed]) => <span className={passed ? 'gate-pass' : 'gate-fail'} key={label}>{passed ? <FaCheck /> : <FaTimes />}{label}</span>)}
        {(selectedCatalogLesson?.publication_blockers || []).map((blocker: string) => <span className="gate-fail" key={blocker}><FaTimes />{blocker}</span>)}
        <strong className="qa-check-title">Device checks</strong>
        {['No horizontal overflow','44px touch targets','Readable at 320px','Bottom dock clear','RU/DE copy fits','Offline recovery visible'].map(item => <span key={item}><FaCheck />{item}</span>)}
      </aside>
      <div className="qa-device-stage">
        <div className={`qa-device level-${level.toLowerCase()}${keyboard ? ' keyboard-open' : ''}`} style={{ width: deviceWidth }} data-testid="qa-device">
          <div className="qa-device-status"><span>9:41</span><b>{t.preview}</b><span>●●●</span></div>
          <div className="qa-device-brand"><span>DeutschIQ</span><small>mini app</small></div>
          <div className="qa-device-content">{lessonLoading && surface === 'lesson' ? <StateSurface state="loading" lang={lang} /> : body}</div>
          {!exceptional && surface !== 'lesson' && surface !== 'checkpoint' && surface !== 'promotion' && <PreviewNav active={surface} />}
          {keyboard && <div className="qa-keyboard" aria-hidden="true">{(lang === 'ru'
            ? ['Й Ц У К Е Н Г Ш Щ З Х','Ф Ы В А П Р О Л Д Ж Э','Я Ч С М И Т Ь Б Ю']
            : ['Q W E R T Z U I O P Ü','A S D F G H J K L Ö Ä','Y X C V B N M']).map(row => <span key={row}>{row}</span>)}</div>}
        </div>
      </div>
    </div>
  </section>;
};
