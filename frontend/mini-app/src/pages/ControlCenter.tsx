import React, { useState } from 'react';
import '../styles/qa-control-center.css';
import { FaChartLine, FaEye, FaHeartbeat, FaLock, FaPlus, FaSignOutAlt, FaSyncAlt } from 'react-icons/fa';
import { api } from '../services/api';
import { QaPreviewLab } from '../components/qa/QaPreviewLab';
import { ContentHealth } from '../components/qa/ContentHealth';

const metric = (value: unknown) => Number(value || 0).toLocaleString();

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
  const [section, setSection] = useState<'qa' | 'health' | 'signals' | 'access'>('qa');

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
  const logout = () => { sessionStorage.removeItem('deutschiq-control-key'); setData(null); setCurriculum([]); setKey(''); };

  if (!data) return <main className="control-center-login"><div className="control-login-card"><FaLock /><small>DEUTSCHIQ INTERNAL</small><h1>Owner quality center</h1><p>Enter the protected owner key. It stays only in this browser session and is verified by the backend.</p><input type="password" value={key} onChange={event => setKey(event.target.value)} onKeyDown={event => event.key === 'Enter' && void load()} placeholder="Owner access key" autoComplete="current-password" /><button type="button" onClick={load} disabled={!key.trim() || loading}>{loading ? 'Verifying…' : 'Open quality center'}</button>{error && <div className="control-error">{error}</div>}</div></main>;

  const reliability = data.events?.reliability || {};
  const flags = (data.exercise_health || []).filter((item: any) => item.status !== 'healthy');
  return <main className="control-center">
    <header><div><small>DEUTSCHIQ · OWNER ONLY</small><h1>Quality center</h1><p>Preview the complete learner journey before every release.</p></div><div className="control-actions"><select aria-label="Analytics range" value={days} onChange={event => setDays(Number(event.target.value))}><option value={7}>7 days</option><option value={30}>30 days</option><option value={90}>90 days</option></select><button type="button" onClick={load} disabled={loading}><FaSyncAlt /> Refresh</button><button type="button" className="control-logout" onClick={logout}><FaSignOutAlt /> Lock</button></div></header>
    <nav className="control-sections" aria-label="Quality center sections"><button className={section === 'qa' ? 'active' : ''} onClick={() => setSection('qa')}><FaEye /> QA preview</button><button className={section === 'health' ? 'active' : ''} onClick={() => setSection('health')}><FaHeartbeat /> Content health</button><button className={section === 'signals' ? 'active' : ''} onClick={() => setSection('signals')}><FaChartLine /> Product signals</button><button className={section === 'access' ? 'active' : ''} onClick={() => setSection('access')}><FaLock /> Beta access</button></nav>
    {section === 'qa' && <QaPreviewLab accessKey={key} catalog={curriculum} />}
    {section === 'health' && <ContentHealth data={data} />}
    {section === 'signals' && <>
    <section className="control-metrics">
      <article><small>Total learners</small><strong>{metric(data.audience?.total_users)}</strong><span>{metric(data.audience?.new_users)} new</span></article>
      <article><small>Active learners</small><strong>{metric(data.audience?.active_learners)}</strong><span>{days}-day window</span></article>
      <article><small>Lesson completion</small><strong>{metric(data.funnel?.completion_rate)}%</strong><span>{metric(data.funnel?.lesson_completed)} learners</span></article>
      <article><small>Abandonments</small><strong>{metric(data.sessions?.abandoned_events)}</strong><span>{metric(data.sessions?.started)} sessions</span></article>
    </section>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>BETA COHORT</small><h2>Enrollment & retention</h2></div></header><div className="control-retention"><div><strong>{metric(data.beta?.enrolled)}</strong><span>enrolled</span></div><div><strong>{metric(data.beta?.onboarded)}</strong><span>onboarded</span></div>{['d1','d3','d7'].map(day=><div key={day}><strong>{data.retention?.[day]?.rate == null ? '—' : `${data.retention[day].rate}%`}</strong><span>{day.toUpperCase()} · {metric(data.retention?.[day]?.eligible)} eligible</span></div>)}</div></section>
    <div className="control-grid">
      <section className="control-panel"><header><FaChartLine /><div><small>FUNNEL</small><h2>Activation</h2></div></header>{[['Claimed invite',data.funnel?.invite_claimed],['Finished onboarding',data.funnel?.onboarding_completed],['Started diagnostic',data.funnel?.diagnostic_started],['Completed diagnostic',data.funnel?.diagnostic_completed],['Started a lesson',data.funnel?.lesson_started],['Completed a lesson',data.funnel?.lesson_completed]].map(([label,value])=><div className="control-row" key={String(label)}><span>{label}</span><b>{metric(value)}</b></div>)}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>RELIABILITY</small><h2>Client signals</h2></div></header>{[['API failures',reliability.api_failed],['Slow API',reliability.api_slow],['Client errors',reliability.client_error],['Reload loops',reliability.reload_loop_detected],['Microphone failures',reliability.microphone_failed]].map(([label,value])=><div className="control-row" key={String(label)}><span>{label}</span><b>{metric(value)}</b></div>)}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>ADAPTATION</small><h2>Lesson modes</h2></div></header>{(data.events?.learning_modes || []).length ? data.events.learning_modes.map((item:any)=><div className="control-row" key={item.mode}><span>{item.mode} · {metric(item.answers)} answers</span><b>{item.accuracy == null ? '—' : `${item.accuracy}%`}</b></div>) : <p className="control-empty">Mode results appear after new lesson attempts.</p>}</section>
      <section className="control-panel"><header><FaChartLine /><div><small>AUDIENCE</small><h2>Languages</h2></div></header>{Object.entries(data.audience?.languages || {}).map(([language,value])=><div className="control-row" key={language}><span>{language.toUpperCase()}</span><b>{metric(value)}</b></div>)}</section>
    </div>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>TESTER PROGRESS</small><h2>Closed-beta cohort</h2></div></header>{(data.testers || []).length ? <div className="control-table"><div className="control-table-head control-tester-grid"><span>Tester</span><span>Journey</span><span>Lessons</span><span>Feedback</span><span>Last active</span></div>{data.testers.map((item:any)=><div className="control-table-row control-tester-grid" key={item.tester}><span><b className="tester-alias">{item.tester}</b><small>{item.language.toUpperCase()} · {item.invite}</small></span><span>{item.diagnostic_completed?'Diagnostic complete':item.onboarded?'Onboarded':'Invited'}</span><span>{item.lessons_completed}/{item.lessons_started}</span><span>{item.feedback_count}</span><span>{item.last_activity_at?new Date(item.last_activity_at).toLocaleDateString():'—'}</span></div>)}</div> : <p className="control-empty">Tester progress appears after invitations are claimed.</p>}</section>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>CONTENT FLAGS</small><h2>Exercises needing review</h2></div></header>{flags.length ? <div className="control-table"><div className="control-table-head"><span>Topic</span><span>Exercise</span><span>Attempts</span><span>Accuracy</span><span>Status</span></div>{flags.map((item:any)=><div className="control-table-row" key={`${item.lesson_id}-${item.exercise_index}`}><span>{item.topic}</span><span>#{item.exercise_index + 1}</span><span>{item.attempts}</span><span>{item.accuracy}%</span><b className={item.status}>{item.status.replace('_',' ')}</b></div>)}</div> : <p className="control-empty">No exercise has enough concerning data yet.</p>}</section>
    <section className="control-panel control-wide"><header><FaChartLine /><div><small>FEEDBACK</small><h2>Recent beta notes</h2></div></header>{(data.events?.feedback || []).length ? <div className="control-feedback">{data.events.feedback.map((item:any,index:number)=><article key={index}><p>{item.message}</p><span>{item.language.toUpperCase()} · {item.category} · {item.topic || item.page}{item.exercise_index != null ? ` · exercise ${item.exercise_index + 1}${item.exercise_type ? ` (${item.exercise_type})` : ''}` : ''}</span></article>)}</div> : <p className="control-empty">No beta feedback in this window.</p>}</section>
    </>}
    {section === 'access' && <section className="control-panel control-wide"><header><FaPlus /><div><small>ACCESS</small><h2>Invite codes</h2></div></header><div className="control-invite-create"><input value={inviteLabel} onChange={e=>setInviteLabel(e.target.value)} maxLength={64}/><input aria-label="Uses" type="number" min={1} max={500} value={inviteUses} onChange={e=>setInviteUses(Number(e.target.value))}/><button onClick={createInvite}><FaPlus/> Create invite</button></div><div className="control-batch"><span>Closed-beta batch</span><input aria-label="Batch size" type="number" min={1} max={50} value={batchCount} onChange={e=>setBatchCount(Number(e.target.value))}/><button onClick={createBatch}><FaPlus/> Create {batchCount} single-use links</button>{newInvites.length > 0 && <button onClick={copyBatch}>Copy latest batch</button>}</div><div className="control-invites">{(data.beta?.invites||[]).map((item:any)=><article key={item.id}><code>{item.code}</code><span>{item.label} · {item.uses}/{item.max_uses}</span><button disabled={!item.active} onClick={()=>deactivateInvite(item.id)}>{item.active?'Deactivate':'Inactive'}</button></article>)}</div></section>}
  </main>;
};
