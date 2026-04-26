import React, { useCallback, useEffect, useState } from 'react';

import { addAgentCron, deleteAgentCron, AgentStatus, getAgentStatus, triggerAgentAction } from '../api';

interface OperationsTabProps {
  agentId: string;
}

const OperationsTab: React.FC<OperationsTabProps> = ({ agentId }) => {
  const [status, setStatus] = useState<AgentStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionInProgress, setActionInProgress] = useState(false);

  // Form states
  const [actionName, setActionName] = useState('');
  const [cronName, setCronName] = useState('');
  const [cronSchedule, setCronSchedule] = useState('');
  const [cronCommand, setCronCommand] = useState('');

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
    fetchStatus();

    // 15 minute polling
    const interval = setInterval(fetchStatus, 15 * 60 * 1000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  const handleTriggerAction = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!actionName) return;

    setActionInProgress(true);
    setError(null);
    try {
      await triggerAgentAction(agentId, actionName);
      setActionName('');
      await fetchStatus();
    } catch (err) {
      console.error(err);
      setError('Failed to trigger action.');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleAddCron = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cronName || !cronSchedule || !cronCommand) return;

    setActionInProgress(true);
    setError(null);
    try {
      await addAgentCron(agentId, cronName, cronSchedule, cronCommand);
      setCronName('');
      setCronSchedule('');
      setCronCommand('');
      await fetchStatus();
    } catch (err) {
      console.error(err);
      setError('Failed to add cron job.');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleDeleteCron = async (name: string) => {
    if (!window.confirm(`Are you sure you want to delete cron job "${name}"?`)) return;

    setActionInProgress(true);
    setError(null);
    try {
      await deleteAgentCron(agentId, name);
      await fetchStatus();
    } catch (err) {
      console.error(err);
      setError('Failed to delete cron job.');
    } finally {
      setActionInProgress(false);
    }
  };

  if (loading && !status) {
    return <div className="text-muted font-mono">Loading operational status...</div>;
  }

  return (
    <div className="flex flex-col gap-8 pb-8">
      {error && (
        <div className="bg-[#f8514920] border border-error text-error px-4 py-2 rounded text-sm flex justify-between items-center">
          <span>{error}</span>
          <button onClick={fetchStatus} className="underline hover:text-white transition-colors">
            Retry
          </button>
        </div>
      )}

      {/* State Section */}
      <section>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-accent">Overall State</h3>
          <button
            onClick={fetchStatus}
            disabled={actionInProgress}
            className="text-xs px-3 py-1 bg-surface border border-border rounded hover:bg-border transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            <span>Refresh</span>
          </button>
        </div>
        <div className="bg-surface border border-border rounded p-4 flex items-center gap-4">
          <div className={`w-3 h-3 rounded-full ${status?.status === 'online' ? 'bg-success' : 'bg-warning'}`}></div>
          <span className="capitalize font-mono">{status?.status || 'Unknown'}</span>
        </div>
      </section>

      {/* Quick Actions Section */}
      <section>
        <h3 className="text-lg font-bold text-accent mb-4">Quick Actions</h3>
        <form onSubmit={handleTriggerAction} className="flex gap-2">
          <input
            type="text"
            value={actionName}
            onChange={(e) => setActionName(e.target.value)}
            placeholder="Action name (e.g., restart, clear_cache)"
            className="flex-1 bg-background border border-border rounded px-3 py-2 text-sm font-mono focus:border-accent outline-none"
            disabled={actionInProgress}
          />
          <button
            type="submit"
            disabled={actionInProgress || !actionName}
            className="px-4 py-2 bg-accent text-background font-bold rounded hover:opacity-90 transition-opacity disabled:opacity-50 text-sm"
          >
            Trigger
          </button>
        </form>
      </section>

      {/* Active Tasks Section */}
      <section>
        <h3 className="text-lg font-bold text-accent mb-4">Active Tasks</h3>
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
      </section>

      {/* Cron Jobs Section */}
      <section>
        <h3 className="text-lg font-bold text-accent mb-4">Cron Jobs</h3>
        
        {/* Add Cron Form */}
        <form onSubmit={handleAddCron} className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-4">
          <input
            type="text"
            value={cronName}
            onChange={(e) => setCronName(e.target.value)}
            placeholder="Job Name"
            className="bg-background border border-border rounded px-3 py-2 text-sm font-mono outline-none focus:border-accent"
            disabled={actionInProgress}
          />
          <input
            type="text"
            value={cronSchedule}
            onChange={(e) => setCronSchedule(e.target.value)}
            placeholder="Schedule (*/5 * * * *)"
            className="bg-background border border-border rounded px-3 py-2 text-sm font-mono outline-none focus:border-accent"
            disabled={actionInProgress}
          />
          <input
            type="text"
            value={cronCommand}
            onChange={(e) => setCronCommand(e.target.value)}
            placeholder="Command"
            className="bg-background border border-border rounded px-3 py-2 text-sm font-mono outline-none focus:border-accent"
            disabled={actionInProgress}
          />
          <button
            type="submit"
            disabled={actionInProgress || !cronName || !cronSchedule || !cronCommand}
            className="md:col-span-3 px-4 py-2 bg-surface border border-border rounded hover:bg-border transition-colors font-bold disabled:opacity-50 text-sm"
          >
            Add Cron Job
          </button>
        </form>

        <div className="flex flex-col gap-2">
          {status?.cron_jobs.length === 0 ? (
            <p className="text-muted text-sm italic">No scheduled cron jobs.</p>
          ) : (
            status?.cron_jobs.map((job) => (
              <div
                key={job.id}
                className="bg-surface border border-border rounded p-3 text-sm font-mono flex justify-between items-center group"
              >
                <div className="flex flex-col">
                  <span className="font-bold">{job.id}</span>
                  <span className="text-muted text-xs">{job.schedule}</span>
                </div>
                <button
                  onClick={() => handleDeleteCron(job.id)}
                  disabled={actionInProgress}
                  className="text-error opacity-0 group-hover:opacity-100 transition-opacity hover:underline text-xs"
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
};

export default OperationsTab;
