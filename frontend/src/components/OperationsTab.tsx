import React, { useCallback, useEffect, useState } from 'react';

import { AgentStatus, getAgentStatus } from '../api';

interface OperationsTabProps {
  agentId: string;
}

const HEALTHY_STATES = new Set(['ok', 'online', 'idle', 'running']);

const OperationsTab: React.FC<OperationsTabProps> = ({ agentId }) => {
  const [status, setStatus] = useState<AgentStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    setError(null);
    try {
      const data = await getAgentStatus(agentId);
      setStatus(data);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch operational status.');
    } finally {
      setLoading(false);
    }
  }, [agentId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void fetchStatus();

    const interval = setInterval(fetchStatus, 15 * 60 * 1000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  if (loading && !status) {
    return <div className="text-muted font-mono">Loading operational status...</div>;
  }

  const state = status?.status || 'unknown';
  const isHealthy = HEALTHY_STATES.has(state.toLowerCase());
  const intelSections = status?.intel?.sections || [];

  return (
    <div className="flex flex-col gap-6 pb-8">
      {error && (
        <div className="bg-[#f8514920] border border-error text-error px-4 py-2 rounded text-sm flex justify-between items-center">
          <span>{error}</span>
          <button onClick={fetchStatus} className="underline hover:text-white transition-colors">
            Retry
          </button>
        </div>
      )}

      <section className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-surface border border-border rounded p-4">
          <p className="text-xs uppercase text-muted tracking-widest mb-2">State</p>
          <div className="flex items-center gap-3">
            <span className={`w-3 h-3 rounded-full ${isHealthy ? 'bg-success' : 'bg-warning'}`} />
            <span className="capitalize font-mono text-lg">{state}</span>
          </div>
        </div>
        <div className="bg-surface border border-border rounded p-4">
          <p className="text-xs uppercase text-muted tracking-widest mb-2">Active Tasks</p>
          <p className="font-mono text-lg">{status?.active_tasks.length || 0}</p>
        </div>
        <div className="bg-surface border border-border rounded p-4 flex items-start justify-between gap-4">
          <div>
            <p className="text-xs uppercase text-muted tracking-widest mb-2">Cron Jobs</p>
            <p className="font-mono text-lg">{status?.cron_jobs.length || 0}</p>
          </div>
          <button
            onClick={fetchStatus}
            disabled={loading}
            className="text-xs px-3 py-1 bg-background border border-border rounded hover:bg-border transition-colors disabled:opacity-50"
          >
            Refresh
          </button>
        </div>
      </section>

      <section>
        <h3 className="text-lg font-bold text-accent mb-3">Runtime Intel</h3>
        {intelSections.length === 0 ? (
          <div className="bg-surface border border-border rounded p-4 text-sm text-muted">
            No SSH CLI intel returned for this agent yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
            {intelSections.map((section) => (
              <article key={section.id} className="bg-surface border border-border rounded overflow-hidden">
                <header className="px-3 py-2 bg-background border-b border-border flex justify-between items-center">
                  <h4 className="text-sm font-bold text-text">{section.title}</h4>
                  <span className="text-[10px] uppercase tracking-widest text-muted">{status?.intel?.source}</span>
                </header>
                <pre className="p-3 max-h-72 overflow-auto whitespace-pre-wrap break-words text-xs leading-relaxed text-text font-mono">
                  {section.content}
                </pre>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        <div>
          <h3 className="text-lg font-bold text-accent mb-3">Active Tasks</h3>
          <div className="flex flex-col gap-2">
            {status?.active_tasks.length === 0 ? (
              <p className="text-muted text-sm italic">No active tasks.</p>
            ) : (
              status?.active_tasks.map((task) => (
                <div key={task.id} className="bg-surface border border-border rounded p-3 text-sm font-mono">
                  {task.description}
                </div>
              ))
            )}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-bold text-accent mb-3">Cron Jobs</h3>
          <div className="flex flex-col gap-2">
            {status?.cron_jobs.length === 0 ? (
              <p className="text-muted text-sm italic">No scheduled cron jobs.</p>
            ) : (
              status?.cron_jobs.map((job) => (
                <div key={job.id} className="bg-surface border border-border rounded p-3 text-sm font-mono">
                  <span className="font-bold">{job.id}</span>
                  <span className="block text-muted text-xs">{job.schedule}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </section>
    </div>
  );
};

export default OperationsTab;
