import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { Agent, AgentStatus, getAgentStatus, getAgents } from '../api';
import { Link } from 'react-router-dom';

interface AgentStatusSnapshot {
  status?: AgentStatus;
  error?: string;
}

type Tone = 'neutral' | 'success' | 'warning' | 'error';

interface MetricTileProps {
  label: string;
  value: number | string;
  detail: string;
  tone?: Tone;
  testId?: string;
}

const statusTone = (status?: string, hasError = false): Tone => {
  if (hasError) {
    return 'error';
  }

  const normalized = status?.toLowerCase() ?? 'unknown';
  if (['ok', 'online', 'running', 'healthy', 'idle'].includes(normalized)) {
    return 'success';
  }
  if (['blocked', 'warning', 'degraded'].includes(normalized)) {
    return 'warning';
  }
  if (['error', 'failed', 'offline', 'unreachable'].includes(normalized)) {
    return 'error';
  }
  return 'neutral';
};

const toneClasses: Record<Tone, string> = {
  neutral: 'border-border text-text',
  success: 'border-success/60 text-success',
  warning: 'border-warning/70 text-warning',
  error: 'border-error/70 text-error',
};

const MetricTile: React.FC<MetricTileProps> = ({ label, value, detail, tone = 'neutral', testId }) => (
  <div className={`min-h-28 border bg-surface p-4 ${toneClasses[tone]}`}>
    <div className="text-xs uppercase tracking-normal text-muted">{label}</div>
    <div data-testid={testId} className="mt-3 text-3xl font-bold leading-none text-text">
      {value}
    </div>
    <div className="mt-3 text-xs leading-5 text-muted">{detail}</div>
  </div>
);

const Dashboard: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [statusByAgent, setStatusByAgent] = useState<Record<string, AgentStatusSnapshot>>({});
  const [businessGroup, setBusinessGroup] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [statusLoading, setStatusLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const fetchStatuses = useCallback(async (visibleAgents: Agent[]) => {
    if (visibleAgents.length === 0) {
      setStatusByAgent({});
      setLastUpdated(null);
      setStatusLoading(false);
      return;
    }

    setStatusLoading(true);
    const results = await Promise.allSettled(
      visibleAgents.map(async (agent) => ({
        agentId: agent.id,
        status: await getAgentStatus(agent.id),
      })),
    );

    const nextStatus = results.reduce<Record<string, AgentStatusSnapshot>>((acc, result, index) => {
      const agentId = visibleAgents[index].id;
      if (result.status === 'fulfilled') {
        acc[agentId] = { status: result.value.status };
      } else {
        acc[agentId] = {
          error: result.reason instanceof Error ? result.reason.message : 'Status unavailable.',
        };
      }
      return acc;
    }, {});

    setStatusByAgent(nextStatus);
    setLastUpdated(new Date().toLocaleTimeString());
    setStatusLoading(false);
  }, []);

  const fetchAgents = useCallback(async (group: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAgents(group);
      setStatusByAgent({});
      setAgents(data);
      void fetchStatuses(data);
    } catch (err) {
      console.error(err);
      setError('Failed to load agents.');
      setStatusByAgent({});
      setStatusLoading(false);
    } finally {
      setLoading(false);
    }
  }, [fetchStatuses]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchAgents(businessGroup);
  }, [businessGroup, fetchAgents]);

  const knownGroups = useMemo(
    () => Array.from(new Set(['Acme', 'Stark', 'X Marketing', 'Wayne Ent', ...agents.map((agent) => agent.business_group)])).sort(),
    [agents],
  );

  const agentRows = useMemo(
    () => agents.map((agent) => ({ agent, snapshot: statusByAgent[agent.id] })),
    [agents, statusByAgent],
  );

  const cockpit = useMemo(() => {
    const totalTasks = agentRows.reduce(
      (total, row) => total + (row.snapshot?.status?.active_tasks.length ?? 0),
      0,
    );
    const totalCrons = agentRows.reduce(
      (total, row) => total + (row.snapshot?.status?.cron_jobs.length ?? 0),
      0,
    );
    const attentionAgents = agentRows.filter((row) => statusTone(row.snapshot?.status?.status, Boolean(row.snapshot?.error)) === 'error').length;
    const onlineAgents = agentRows.filter((row) => statusTone(row.snapshot?.status?.status, Boolean(row.snapshot?.error)) === 'success').length;
    const intelAgents = agentRows.filter((row) => (row.snapshot?.status?.intel?.sections.length ?? 0) > 0).length;

    const groupRows = agentRows.reduce<Record<string, { total: number; online: number; attention: number; tasks: number; crons: number }>>(
      (acc, row) => {
        const group = row.agent.business_group;
        const tone = statusTone(row.snapshot?.status?.status, Boolean(row.snapshot?.error));
        acc[group] ??= { total: 0, online: 0, attention: 0, tasks: 0, crons: 0 };
        acc[group].total += 1;
        acc[group].online += tone === 'success' ? 1 : 0;
        acc[group].attention += tone === 'error' ? 1 : 0;
        acc[group].tasks += row.snapshot?.status?.active_tasks.length ?? 0;
        acc[group].crons += row.snapshot?.status?.cron_jobs.length ?? 0;
        return acc;
      },
      {},
    );

    const tasks = agentRows.flatMap((row) =>
      (row.snapshot?.status?.active_tasks ?? []).map((task) => ({
        ...task,
        agentName: row.agent.name,
        businessGroup: row.agent.business_group,
      })),
    );

    const crons = agentRows.flatMap((row) =>
      (row.snapshot?.status?.cron_jobs ?? []).map((cron) => ({
        ...cron,
        agentName: row.agent.name,
        businessGroup: row.agent.business_group,
      })),
    );

    return {
      totalTasks,
      totalCrons,
      attentionAgents,
      onlineAgents,
      intelAgents,
      groupRows: Object.entries(groupRows).sort(([left], [right]) => left.localeCompare(right)),
      tasks,
      crons,
    };
  }, [agentRows]);

  return (
    <div className="min-h-screen bg-background text-text p-5 lg:p-6">
      <header className="flex flex-col gap-4 border-b border-border pb-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-normal text-muted">Single Pane Supervisor</p>
          <h1 className="mt-1 text-3xl font-bold text-text">Operator Cockpit</h1>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <select
            value={businessGroup}
            onChange={(e) => setBusinessGroup(e.target.value)}
            className="min-h-10 bg-surface border border-border text-text text-sm focus:ring-accent focus:border-accent block w-full p-2.5 sm:w-56"
            aria-label="Filter by Business Group"
          >
            <option value="">All Businesses</option>
            {knownGroups.map((group) => (
              <option key={group} value={group}>
                {group}
              </option>
            ))}
          </select>
          <button
            type="button"
            onClick={() => fetchAgents(businessGroup)}
            className="min-h-10 border border-border bg-surface px-4 py-2 text-sm font-bold text-text transition-colors hover:border-accent disabled:opacity-60"
            disabled={loading || statusLoading}
          >
            {loading || statusLoading ? 'Refreshing' : 'Refresh'}
          </button>
          <Link
            to="/add"
            className="min-h-10 bg-accent px-4 py-2 text-center text-sm font-bold text-[#0d1117] transition-colors hover:bg-blue-400"
          >
            Add Agent
          </Link>
        </div>
      </header>

      <main className="mt-6 flex flex-col gap-6">
        {loading ? (
          <div className="text-muted">Loading agents...</div>
        ) : error ? (
          <div className="text-error">{error}</div>
        ) : agents.length === 0 ? (
          <div className="border border-border bg-surface p-6 text-muted">No agents found.</div>
        ) : (
          <>
            <section className="grid grid-cols-2 gap-3 xl:grid-cols-6">
              <MetricTile
                label="Agents"
                value={agents.length}
                detail="Visible registry"
                testId="total-agents-stat"
              />
              <MetricTile
                label="Online"
                value={cockpit.onlineAgents}
                detail="Healthy status"
                tone="success"
                testId="online-agents-stat"
              />
              <MetricTile
                label="Attention"
                value={cockpit.attentionAgents}
                detail="Unreachable or failed"
                tone={cockpit.attentionAgents > 0 ? 'error' : 'neutral'}
                testId="attention-agents-stat"
              />
              <MetricTile
                label="Active Tasks"
                value={cockpit.totalTasks}
                detail="Current workload"
                tone={cockpit.totalTasks > 0 ? 'warning' : 'neutral'}
                testId="active-tasks-stat"
              />
              <MetricTile
                label="Cron Jobs"
                value={cockpit.totalCrons}
                detail="Scheduled jobs"
                testId="cron-jobs-stat"
              />
              <MetricTile
                label="Runtime Intel"
                value={cockpit.intelAgents}
                detail={lastUpdated ? `Last refresh ${lastUpdated}` : 'Waiting for status'}
                tone="success"
              />
            </section>

            <section>
              <div className="mb-3 flex items-center justify-between">
                <h2 className="text-sm font-bold uppercase tracking-normal text-muted">Business Groups</h2>
                {statusLoading && <span className="text-xs text-warning">Polling runtime status...</span>}
              </div>
              <div className="grid gap-3 lg:grid-cols-2 xl:grid-cols-3">
                {cockpit.groupRows.map(([group, row]) => (
                  <div key={group} className="border border-border bg-surface p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <div className="text-lg font-bold text-text">{group}</div>
                        <div className="mt-1 text-xs text-muted">{row.total} Agents registered</div>
                      </div>
                      <div className="text-right text-xs leading-5 text-muted">
                        <div>
                          <span className="text-success">{row.online}</span> online
                        </div>
                        <div>
                          <span className={row.attention > 0 ? 'text-error' : 'text-muted'}>{row.attention}</span> attention
                        </div>
                      </div>
                    </div>
                    <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
                      <div className="border border-border bg-background p-3">
                        <div className="text-xs text-muted">Tasks</div>
                        <div className="mt-1 text-xl font-bold text-text">{row.tasks}</div>
                      </div>
                      <div className="border border-border bg-background p-3">
                        <div className="text-xs text-muted">Cron Jobs</div>
                        <div className="mt-1 text-xl font-bold text-text">{row.crons}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <section>
              <div className="mb-3 flex items-center justify-between">
                <h2 className="text-sm font-bold uppercase tracking-normal text-muted">Agent Matrix</h2>
                <span className="text-xs text-muted">{lastUpdated ? `Last refresh ${lastUpdated}` : 'Polling'}</span>
              </div>
              <div className="overflow-hidden border border-border">
                <div className="hidden grid-cols-[1.4fr_1fr_0.8fr_0.6fr_0.6fr_1.4fr] border-b border-border bg-surface px-4 py-3 text-xs uppercase tracking-normal text-muted lg:grid">
                  <div>Agent</div>
                  <div>Business</div>
                  <div>Status</div>
                  <div>Tasks</div>
                  <div>Crons</div>
                  <div>Endpoint</div>
                </div>
                <div className="divide-y divide-border">
                  {agentRows.map(({ agent, snapshot }) => {
                    const tone = statusTone(snapshot?.status?.status, Boolean(snapshot?.error));
                    const statusLabel = snapshot?.error ? 'unreachable' : snapshot?.status?.status ?? 'unknown';
                    return (
                      <Link
                        key={agent.id}
                        to={`/agents/${agent.id}`}
                        className="grid gap-3 bg-background px-4 py-4 transition-colors hover:bg-surface lg:grid-cols-[1.4fr_1fr_0.8fr_0.6fr_0.6fr_1.4fr] lg:items-center"
                      >
                        <div>
                          <div className="font-bold text-accent">{agent.name}</div>
                          <div className="mt-1 text-xs text-muted">{agent.ip_address}</div>
                        </div>
                        <div className="text-sm text-text">{agent.business_group}</div>
                        <div>
                          <span className={`inline-flex min-w-24 justify-center border px-2 py-1 text-xs uppercase ${toneClasses[tone]}`}>
                            {statusLabel}
                          </span>
                        </div>
                        <div className="text-sm text-text">{snapshot?.status?.active_tasks.length ?? 0}</div>
                        <div className="text-sm text-text">{snapshot?.status?.cron_jobs.length ?? 0}</div>
                        <div className="min-w-0 truncate text-xs text-muted">{agent.api_endpoint}</div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            </section>

            <section className="grid gap-4 xl:grid-cols-3">
              <div className="border border-border bg-surface p-4">
                <h2 className="text-sm font-bold uppercase tracking-normal text-muted">Active Work</h2>
                <div className="mt-4 flex flex-col gap-3">
                  {cockpit.tasks.length > 0 ? (
                    cockpit.tasks.map((task) => (
                      <div key={`${task.agentName}-${task.id}`} className="border border-border bg-background p-3">
                        <div className="text-sm font-bold text-text">{task.description}</div>
                        <div className="mt-2 text-xs text-muted">
                          {task.agentName} / {task.businessGroup}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-sm leading-6 text-muted">No active tasks reported by visible Agents.</div>
                  )}
                </div>
              </div>

              <div className="border border-border bg-surface p-4">
                <h2 className="text-sm font-bold uppercase tracking-normal text-muted">Schedules</h2>
                <div className="mt-4 flex flex-col gap-3">
                  {cockpit.crons.length > 0 ? (
                    cockpit.crons.map((cron) => (
                      <div key={`${cron.agentName}-${cron.id}`} className="border border-border bg-background p-3">
                        <div className="text-sm font-bold text-text">{cron.schedule}</div>
                        <div className="mt-2 text-xs text-muted">
                          {cron.agentName} / {cron.businessGroup}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-sm leading-6 text-muted">No cron jobs reported by visible Agents.</div>
                  )}
                </div>
              </div>

              <div className="border border-border bg-surface p-4">
                <h2 className="text-sm font-bold uppercase tracking-normal text-muted">Runtime Intel</h2>
                <div className="mt-4 flex flex-col gap-3">
                  {agentRows
                    .filter((row) => (row.snapshot?.status?.intel?.sections.length ?? 0) > 0)
                    .map((row) => (
                      <div key={row.agent.id} className="border border-border bg-background p-3">
                        <div className="flex items-center justify-between gap-3">
                          <div className="text-sm font-bold text-text">{row.agent.name}</div>
                          <div className="text-xs text-success">{row.snapshot?.status?.intel?.source}</div>
                        </div>
                        <div className="mt-2 text-xs text-muted">
                          {row.snapshot?.status?.intel?.sections.map((section) => section.title).join(' / ')}
                        </div>
                      </div>
                    ))}
                  {cockpit.intelAgents === 0 && (
                    <div className="text-sm leading-6 text-muted">No runtime intel returned yet.</div>
                  )}
                </div>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
