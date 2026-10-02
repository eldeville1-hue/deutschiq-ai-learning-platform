import React, { useMemo, useState } from 'react';
import { FaCheck, FaExclamationTriangle, FaFlask, FaLock } from 'react-icons/fa';

const signal = (value: number | null | undefined, suffix = '%') => value == null ? 'Not enough evidence' : `${value}${suffix}`;

const stageCopy: Record<string, { title: string; body: string }> = {
  blocked: { title: 'Publishing is blocked', body: 'At least one A1 lesson fails a required content or localisation gate.' },
  ready_for_closed_beta: { title: 'Ready for a controlled beta', body: 'The learning loop is instrumented. Invite real learners and collect evidence before claiming effectiveness.' },
  collecting_evidence: { title: 'Collecting learning evidence', body: 'The system is live, but the sample is still too small for reliable lesson decisions.' },
  content_review_required: { title: 'Some lessons need intervention', body: 'The sample is large enough and one or more learning signals crossed a review threshold.' },
  evidence_ready: { title: 'A1 evidence gate passed', body: 'The closed beta has enough activity to begin evidence-led curriculum decisions.' },
};

export const ContentHealth: React.FC<{ data: any; onAcceptanceUpdate: (id: string, passed: boolean, notes: string) => Promise<void> }> = ({ data, onAcceptanceUpdate }) => {
  const [filter, setFilter] = useState('all');
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState('');
  const readiness = data.readiness || { stage: 'blocked', gates: [] };
  const copy = stageCopy[readiness.stage] || stageCopy.blocked;
  const rows = useMemo(() => (data.content_health || []).filter((item: any) => filter === 'all' || item.status === filter), [data.content_health, filter]);
  const counts = useMemo(() => (data.content_health || []).reduce((result: Record<string, number>, item: any) => ({ ...result, [item.status]: (result[item.status] || 0) + 1 }), {}), [data.content_health]);

  return <div className="health-workspace">
    <section className={`readiness-hero stage-${readiness.stage}`}>
      <div className="readiness-mark">{readiness.all_gates_passed ? <FaCheck /> : <FaFlask />}</div>
      <div><small>A1 BETA READINESS</small><h2>{copy.title}</h2><p>{copy.body}</p></div>
      <strong>{readiness.stage.replaceAll('_', ' ')}</strong>
    </section>

    <section className="readiness-gates">
      {(readiness.gates || []).map((gate: any) => <article className={gate.passed ? 'passed' : 'waiting'} key={gate.id}>
        <span>{gate.passed ? <FaCheck /> : <FaLock />}</span>
        <div><strong>{gate.label}</strong><small>{gate.evidence}</small></div>
      </article>)}
    </section>

    <section className="control-panel control-wide acceptance-panel">
      <header><FaFlask /><div><small>REAL DEVICE ACCEPTANCE</small><h2>Human checks that browser automation cannot certify</h2></div></header>
      <p className="acceptance-explainer">Mark a check only after completing it in the Telegram app on the named device or failure condition. Notes stay attached to the release gate.</p>
      <div className="acceptance-list">
        {(data.acceptance?.checks || []).map((check: any) => {
          const currentNotes = notes[check.id] ?? check.notes ?? '';
          return <article className={check.passed ? 'passed' : ''} key={check.id}>
            <span>{check.passed ? <FaCheck /> : <FaLock />}</span>
            <div><strong>{check.label}</strong><input maxLength={500} value={currentNotes} onChange={event => setNotes(value => ({ ...value, [check.id]: event.target.value }))} placeholder="Device, OS, Telegram version, result or issue" /></div>
            <button type="button" disabled={saving === check.id} onClick={async () => { setSaving(check.id); try { await onAcceptanceUpdate(check.id, !check.passed, currentNotes); } finally { setSaving(''); } }}>{saving === check.id ? 'Saving…' : check.passed ? 'Reopen' : 'Mark passed'}</button>
          </article>;
        })}
      </div>
      <footer>{data.acceptance?.passed || 0}/{data.acceptance?.required || 0} checks passed. Automated QA cannot change this gate.</footer>
    </section>

    <section className="control-panel control-wide health-table-panel">
      <header><FaExclamationTriangle /><div><small>CONTENT HEALTH</small><h2>Every A1 lesson, publishing gate + learner evidence</h2></div></header>
      <div className="health-filters">
        {['all', 'blocked', 'collecting', 'awaiting_recall', 'needs_review', 'healthy'].map(status => <button type="button" className={filter === status ? 'active' : ''} onClick={() => setFilter(status)} key={status}>{status.replaceAll('_', ' ')}{status !== 'all' ? ` · ${counts[status] || 0}` : ` · ${(data.content_health || []).length}`}</button>)}
      </div>
      <div className="health-table">
        <div className="health-table-head"><span>Lesson</span><span>Evidence</span><span>Completion</span><span>Recall</span><span>Decision</span></div>
        {rows.map((item: any) => <article className="health-table-row" key={item.lesson_id}>
          <div><small>DAY {item.day} · MODULE {item.module}</small><strong>{item.title}</strong><span>{item.topic}</span></div>
          <div><strong>{item.sample.learners} learners</strong><span>{item.sample.completed} completed · {item.sample.attempts} attempts</span></div>
          <div><strong>{signal(item.signals.completion_rate)}</strong><span>{item.sample.started < 5 ? `${item.sample.started}/5 starts` : signal(item.signals.skip_rate) + ' skipped'}</span></div>
          <div><strong>{signal(item.signals.review_success)}</strong><span>{item.sample.reviews}/5 recall answers</span></div>
          <div><b className={`health-status ${item.status}`}>{item.status.replaceAll('_', ' ')}</b><span>{item.reasons?.[0] || 'Signals are within the review thresholds'}</span></div>
        </article>)}
      </div>
      {!rows.length && <p className="control-empty">No lessons match this filter.</p>}
      <footer>Rates appear only after at least five relevant observations. Until then, DeutschIQ reports that evidence is insufficient.</footer>
    </section>
  </div>;
};
