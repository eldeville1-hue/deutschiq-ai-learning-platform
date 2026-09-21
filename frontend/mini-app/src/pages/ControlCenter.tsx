import React, { useState } from 'react';
import { FaChartLine, FaLock, FaSyncAlt } from 'react-icons/fa';
import { api } from '../services/api';

const metric = (value: unknown) => Number(value || 0).toLocaleString();

export const ControlCenter: React.FC = () => {
  const [key, setKey] = useState(() => sessionStorage.getItem('deutschiq-control-key') || '');
  const [days, setDays] = useState(30);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    if (!key.trim()) return;
    setLoading(true); setError('');
    try {
      const result = await api.getBetaControlCenter(key.trim(), days);
      sessionStorage.setItem('deutschiq-control-key', key.trim());
      setData(result);
    } catch (requestError: any) {
      setData(null);
      setError(requestError?.response?.status === 403 ? 'Access key is not valid.' : 'Control-center data is temporarily unavailable.');
    } finally { setLoading(false); }
  };

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
    <div className="control-grid">
      <section className="control-panel"><header><FaChartLine /><div><small>FUNNEL</small><h2>Activation</h2></div></header>{[['Diagnostic complete',data.funnel?.diagnostic_completed],['Started a lesson',data.funnel?.lesson_started],['Completed a lesson',data.funnel?.lesson_completed]].map(([label,value])=><div className="control-row" key={String(label)}><span>{label}</span><b>{metric(value)}</b></div>)}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>RELIABILITY</small><h2>Client signals</h2></div></header>{[['API failures',reliability.api_failed],['Slow API',reliability.api_slow],['Client errors',reliability.client_error],['Reload loops',reliability.reload_loop_detected],['Microphone failures',reliability.microphone_failed]].map(([label,value])=><div className="control-row" key={String(label)}><span>{label}</span><b>{metric(value)}</b></div>)}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>ADAPTATION</small><h2>Lesson modes</h2></div></header>{(data.events?.learning_modes || []).length ? data.events.learning_modes.map((item:any)=><div className="control-row" key={item.mode}><span>{item.mode} · {metric(item.answers)} answers</span><b>{item.accuracy == null ? '—' : `${item.accuracy}%`}</b></div>) : <p className="control-empty">Mode results appear after new lesson attempts.</p>}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>AUDIENCE</small><h2>Languages</h2></div></header>{Object.entries(data.audience?.languages || {}).map(([language,value])=><div className="control-row" key={language}><span>{language.toUpperCase()}</span><b>{metric(value)}</b></div>)}</section>
    </div>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>CONTENT FLAGS</small><h2>Exercises needing review</h2></div></header>{flags.length ? <div className="control-table"><div className="control-table-head"><span>Topic</span><span>Exercise</span><span>Attempts</span><span>Accuracy</span><span>Status</span></div>{flags.map((item:any)=><div className="control-table-row" key={`${item.lesson_id}-${item.exercise_index}`}><span>{item.topic}</span><span>#{item.exercise_index + 1}</span><span>{item.attempts}</span><span>{item.accuracy}%</span><b className={item.status}>{item.status.replace('_',' ')}</b></div>)}</div> : <p className="control-empty">No exercise has enough concerning data yet.</p>}</section>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>FEEDBACK</small><h2>Recent beta notes</h2></div></header>{(data.events?.feedback || []).length ? <div className="control-feedback">{data.events.feedback.map((item:any,index:number)=><article key={index}><p>{item.message}</p><span>{item.language.toUpperCase()} · {item.page}</span></article>)}</div> : <p className="control-empty">No beta feedback in this window.</p>}</section>
  </main>;
};
