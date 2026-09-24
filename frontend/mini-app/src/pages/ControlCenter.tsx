import React, { useEffect, useMemo, useState } from 'react';
import { FaChartLine, FaCheck, FaEye, FaLock, FaPlus, FaSyncAlt, FaTimes, FaVolumeUp } from 'react-icons/fa';
import { api } from '../services/api';
import { ExerciseInteraction } from '../components/learning/ExerciseInteraction';
import type { AppLanguage } from '../i18n/language';

const metric = (value: unknown) => Number(value || 0).toLocaleString();

type PreviewState = 'intro' | 'practice' | 'correct' | 'wrong' | 'complete';

const CurriculumPreview: React.FC<{ accessKey: string; catalog: any[] }> = ({ accessKey, catalog }) => {
  const [level, setLevel] = useState('A1');
  const [lang, setLang] = useState<AppLanguage>('ru');
  const [lessonId, setLessonId] = useState<number>(0);
  const [lesson, setLesson] = useState<any>(null);
  const [exerciseIndex, setExerciseIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [previewState, setPreviewState] = useState<PreviewState>('intro');
  const [deviceWidth, setDeviceWidth] = useState(390);
  const [loading, setLoading] = useState(false);
  const [previewError, setPreviewError] = useState('');
  const levelLessons = useMemo(() => catalog.filter(item => item.level === level), [catalog, level]);
  const exercise = lesson?.content?.exercises?.[exerciseIndex];

  useEffect(() => {
    const first = levelLessons[0];
    if (first && !levelLessons.some(item => item.id === lessonId)) setLessonId(first.id);
  }, [levelLessons, lessonId]);
  useEffect(() => {
    if (!lessonId) return;
    setLoading(true); setPreviewError('');
    api.getCurriculumPreviewLesson(accessKey, lessonId, lang)
      .then(value => { setLesson(value); setExerciseIndex(0); setAnswer(''); setPreviewState('intro'); })
      .catch(() => { setLesson(null); setPreviewError('Could not load this lesson. Refresh the dashboard and try again.'); })
      .finally(() => setLoading(false));
  }, [accessKey, lang, lessonId]);

  const speak = () => {
    const text = exercise?.audio_text || lesson?.content?.audio_text || lesson?.content?.examples?.[0];
    if (!text || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const voice = new SpeechSynthesisUtterance(text);
    voice.lang = 'de-DE'; voice.rate = .88;
    window.speechSynthesis.speak(voice);
  };
  const setState = (state: PreviewState) => {
    setPreviewState(state);
    if (state === 'correct') setAnswer(String(exercise?.answer || exercise?.accepted_answers?.[0] || ''));
    if (state === 'wrong') setAnswer('Ich Beispiel falsch.');
  };

  return <section className="control-panel control-wide curriculum-preview-panel">
    <header><FaEye /><div><small>OWNER PREVIEW · READ ONLY</small><h2>Curriculum laboratory</h2></div></header>
    <p className="control-empty">Inspect any lesson without sessions, XP, mastery, review dates, or product analytics.</p>
    <div className="preview-toolbar">
      <label>Level<select value={level} onChange={event => setLevel(event.target.value)}>{['A1','A2','B1','B2'].map(item => <option key={item}>{item}</option>)}</select></label>
      <label>Lesson<select value={lessonId} onChange={event => setLessonId(Number(event.target.value))}>{levelLessons.map(item => <option key={item.id} value={item.id}>{item.day || '—'} · {item.title}</option>)}</select></label>
      <label>Language<select value={lang} onChange={event => setLang(event.target.value as AppLanguage)}><option value="ru">RU</option><option value="de">DE</option><option value="en">EN</option></select></label>
      <label>Phone<select value={deviceWidth} onChange={event => setDeviceWidth(Number(event.target.value))}>{[320,360,390,430].map(width => <option key={width} value={width}>{width}px</option>)}</select></label>
    </div>
    <div className="preview-statebar">{(['intro','practice','correct','wrong','complete'] as PreviewState[]).map(state => <button key={state} className={previewState === state ? 'active' : ''} onClick={() => setState(state)}>{state}</button>)}</div>
    <div className="preview-workbench">
      <aside>{lesson?.content?.exercises?.map((item: any, index: number) => <button key={item.id || index} className={exerciseIndex === index ? 'active' : ''} onClick={() => { setExerciseIndex(index); setAnswer(''); setPreviewState('practice'); }}><b>{index + 1}</b><span>{item.type.replaceAll('_',' ')}</span></button>)}</aside>
      <div className="preview-device-wrap"><div className={`preview-device level-${level.toLowerCase()}`} style={{ width: deviceWidth }}>
        {loading ? <div className="analysis-loader" /> : previewError ? <div className="preview-load-error"><FaTimes /><p>{previewError}</p></div> : !lesson ? <div className="preview-load-error"><p>No active lesson is available at this level.</p></div> : <>
          <div className="preview-device-head"><span>PREVIEW</span><b>{level}</b><small>{lesson.content.module_title || lesson.pillar}</small></div>
          {previewState === 'intro' && <div className="preview-screen preview-intro">
            <small>{lesson.content.module_title || 'LESSON'} · {lesson.content.module_step || lesson.content.day || ''}</small>
            <h3>{lesson.content.title}</h3>
            <div className="preview-can-do"><small>CAN DO</small><strong>{lesson.content.can_do || lesson.content.objective}</strong></div>
            {lesson.content.scenario && <p>{lesson.content.scenario}</p>}
            <div className="preview-rule">{lesson.content.rule}</div>
          </div>}
          {['practice','correct','wrong'].includes(previewState) && exercise && <div className="preview-screen preview-practice">
            <div className="preview-exercise-head"><small>{exercise.type.replaceAll('_',' ')}</small><span>{exerciseIndex + 1}/{lesson.content.exercises.length}</span></div>
            <h3>{exercise.question}</h3>
            {(exercise.type === 'listening_choice' || exercise.type === 'listening' || exercise.type === 'repeat') && <button className="preview-listen" onClick={speak}><FaVolumeUp /> Play German audio</button>}
            <ExerciseInteraction exercise={{ ...exercise, id: `preview-${lesson.id}-${exerciseIndex}` }} answer={answer} onAnswer={setAnswer} disabled={previewState !== 'practice'} lang={lang} />
            {previewState === 'correct' && <div className="preview-feedback correct"><FaCheck /><div><b>Correct</b><p>{exercise.explanation}</p></div></div>}
            {previewState === 'wrong' && <div className="preview-feedback wrong"><FaTimes /><div><b>Needs repair</b><p>{exercise.explanation}</p><strong>{exercise.answer || exercise.accepted_answers?.[0]}</strong></div></div>}
          </div>}
          {previewState === 'complete' && <div className="preview-screen preview-complete"><FaCheck /><small>LESSON COMPLETE</small><h3>{lesson.content.title}</h3><strong>{lesson.content.can_do || lesson.content.objective}</strong><p>Preview completion does not change learner progress.</p></div>}
        </>}
      </div></div>
    </div>
  </section>;
};

export const ControlCenter: React.FC = () => {
  const [key, setKey] = useState(() => sessionStorage.getItem('deutschiq-control-key') || '');
  const [days, setDays] = useState(30);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [inviteLabel, setInviteLabel] = useState('Beta tester');
  const [inviteUses, setInviteUses] = useState(1);
  const [batchCount, setBatchCount] = useState(15);
  const [newInvites, setNewInvites] = useState<any[]>([]);
  const [curriculum, setCurriculum] = useState<any[]>([]);

  const load = async () => {
    if (!key.trim()) return;
    setLoading(true); setError('');
    try {
      const [result, curriculumResult] = await Promise.all([api.getBetaControlCenter(key.trim(), days), api.getCurriculumPreview(key.trim())]);
      sessionStorage.setItem('deutschiq-control-key', key.trim());
      setData(result);
      setCurriculum(curriculumResult || []);
    } catch (requestError: any) {
      setData(null);
      setError(requestError?.response?.status === 403 ? 'Access key is not valid.' : 'Control-center data is temporarily unavailable.');
    } finally { setLoading(false); }
  };
  const createInvite = async () => { await api.createBetaInvite(key, { label: inviteLabel, max_uses: inviteUses }); await load(); };
  const createBatch = async () => { const result = await api.createBetaInviteBatch(key, { label_prefix: inviteLabel, count: batchCount }); setNewInvites(result.invites || []); await load(); };
  const deactivateInvite = async (id: number) => { await api.deactivateBetaInvite(key, id); await load(); };
  const copyBatch = async () => { await navigator.clipboard.writeText(newInvites.map(item => `${item.label}: ${item.invite_url}`).join('\n')); };

  if (!data) return <main className="control-center-login"><div className="control-login-card"><FaLock /><small>DEUTSCHIQ INTERNAL</small><h1>Beta control center</h1><p>Enter the protected control-center key. It remains only in this browser session.</p><input type="password" value={key} onChange={event => setKey(event.target.value)} onKeyDown={event => event.key === 'Enter' && void load()} placeholder="Access key" autoComplete="current-password" /><button type="button" onClick={load} disabled={!key.trim() || loading}>{loading ? 'Opening…' : 'Open dashboard'}</button>{error && <div className="control-error">{error}</div>}</div></main>;

  const reliability = data.events?.reliability || {};
  const flags = (data.exercise_health || []).filter((item: any) => item.status !== 'healthy');
  return <main className="control-center">
    <header><div><small>DEUTSCHIQ · PRIVATE</small><h1>Beta control center</h1><p>Aggregated learning and reliability signals · no Telegram IDs</p></div><div className="control-actions"><select value={days} onChange={event => setDays(Number(event.target.value))}><option value={7}>7 days</option><option value={30}>30 days</option><option value={90}>90 days</option></select><button type="button" onClick={load} disabled={loading}><FaSyncAlt /> Refresh</button></div></header>
    <section className="control-metrics">
      <article><small>Total learners</small><strong>{metric(data.audience?.total_users)}</strong><span>{metric(data.audience?.new_users)} new</span></article>
      <article><small>Active learners</small><strong>{metric(data.audience?.active_learners)}</strong><span>{days}-day window</span></article>
      <article><small>Lesson completion</small><strong>{metric(data.funnel?.completion_rate)}%</strong><span>{metric(data.funnel?.lesson_completed)} learners</span></article>
      <article><small>Abandonments</small><strong>{metric(data.sessions?.abandoned_events)}</strong><span>{metric(data.sessions?.started)} sessions</span></article>
    </section>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>BETA COHORT</small><h2>Enrollment & retention</h2></div></header><div className="control-retention"><div><strong>{metric(data.beta?.enrolled)}</strong><span>enrolled</span></div><div><strong>{metric(data.beta?.onboarded)}</strong><span>onboarded</span></div>{['d1','d3','d7'].map(day=><div key={day}><strong>{data.retention?.[day]?.rate == null ? '—' : `${data.retention[day].rate}%`}</strong><span>{day.toUpperCase()} · {metric(data.retention?.[day]?.eligible)} eligible</span></div>)}</div></section>
    <CurriculumPreview accessKey={key} catalog={curriculum} />
    <section className="control-panel control-wide"><header><FaPlus /><div><small>ACCESS</small><h2>Invite codes</h2></div></header><div className="control-invite-create"><input value={inviteLabel} onChange={e=>setInviteLabel(e.target.value)} maxLength={64}/><input aria-label="Uses" type="number" min={1} max={500} value={inviteUses} onChange={e=>setInviteUses(Number(e.target.value))}/><button onClick={createInvite}><FaPlus/> Create invite</button></div><div className="control-batch"><span>Closed-beta batch</span><input aria-label="Batch size" type="number" min={1} max={50} value={batchCount} onChange={e=>setBatchCount(Number(e.target.value))}/><button onClick={createBatch}><FaPlus/> Create {batchCount} single-use links</button>{newInvites.length > 0 && <button onClick={copyBatch}>Copy latest batch</button>}</div><div className="control-invites">{(data.beta?.invites||[]).map((item:any)=><article key={item.id}><code>{item.code}</code><span>{item.label} · {item.uses}/{item.max_uses}</span><button disabled={!item.active} onClick={()=>deactivateInvite(item.id)}>{item.active?'Deactivate':'Inactive'}</button></article>)}</div></section>
    <div className="control-grid">
      <section className="control-panel"><header><FaChartLine /><div><small>FUNNEL</small><h2>Activation</h2></div></header>{[['Claimed invite',data.funnel?.invite_claimed],['Finished onboarding',data.funnel?.onboarding_completed],['Started diagnostic',data.funnel?.diagnostic_started],['Completed diagnostic',data.funnel?.diagnostic_completed],['Started a lesson',data.funnel?.lesson_started],['Completed a lesson',data.funnel?.lesson_completed]].map(([label,value])=><div className="control-row" key={String(label)}><span>{label}</span><b>{metric(value)}</b></div>)}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>RELIABILITY</small><h2>Client signals</h2></div></header>{[['API failures',reliability.api_failed],['Slow API',reliability.api_slow],['Client errors',reliability.client_error],['Reload loops',reliability.reload_loop_detected],['Microphone failures',reliability.microphone_failed]].map(([label,value])=><div className="control-row" key={String(label)}><span>{label}</span><b>{metric(value)}</b></div>)}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>ADAPTATION</small><h2>Lesson modes</h2></div></header>{(data.events?.learning_modes || []).length ? data.events.learning_modes.map((item:any)=><div className="control-row" key={item.mode}><span>{item.mode} · {metric(item.answers)} answers</span><b>{item.accuracy == null ? '—' : `${item.accuracy}%`}</b></div>) : <p className="control-empty">Mode results appear after new lesson attempts.</p>}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>AUDIENCE</small><h2>Languages</h2></div></header>{Object.entries(data.audience?.languages || {}).map(([language,value])=><div className="control-row" key={language}><span>{language.toUpperCase()}</span><b>{metric(value)}</b></div>)}</section>
    </div>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>TESTER PROGRESS</small><h2>Closed-beta cohort</h2></div></header>{(data.testers || []).length ? <div className="control-table"><div className="control-table-head control-tester-grid"><span>Tester</span><span>Journey</span><span>Lessons</span><span>Feedback</span><span>Last active</span></div>{data.testers.map((item:any)=><div className="control-table-row control-tester-grid" key={item.tester}><span><b className="tester-alias">{item.tester}</b><small>{item.language.toUpperCase()} · {item.invite}</small></span><span>{item.diagnostic_completed?'Diagnostic complete':item.onboarded?'Onboarded':'Invited'}</span><span>{item.lessons_completed}/{item.lessons_started}</span><span>{item.feedback_count}</span><span>{item.last_activity_at?new Date(item.last_activity_at).toLocaleDateString():'—'}</span></div>)}</div> : <p className="control-empty">Tester progress appears after invitations are claimed.</p>}</section>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>CONTENT FLAGS</small><h2>Exercises needing review</h2></div></header>{flags.length ? <div className="control-table"><div className="control-table-head"><span>Topic</span><span>Exercise</span><span>Attempts</span><span>Accuracy</span><span>Status</span></div>{flags.map((item:any)=><div className="control-table-row" key={`${item.lesson_id}-${item.exercise_index}`}><span>{item.topic}</span><span>#{item.exercise_index + 1}</span><span>{item.attempts}</span><span>{item.accuracy}%</span><b className={item.status}>{item.status.replace('_',' ')}</b></div>)}</div> : <p className="control-empty">No exercise has enough concerning data yet.</p>}</section>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>FEEDBACK</small><h2>Recent beta notes</h2></div></header>{(data.events?.feedback || []).length ? <div className="control-feedback">{data.events.feedback.map((item:any,index:number)=><article key={index}><p>{item.message}</p><span>{item.language.toUpperCase()} · {item.category} · {item.topic || item.page}{item.exercise_index != null ? ` · exercise ${item.exercise_index + 1}${item.exercise_type ? ` (${item.exercise_type})` : ''}` : ''}</span></article>)}</div> : <p className="control-empty">No beta feedback in this window.</p>}</section>
  </main>;
};
