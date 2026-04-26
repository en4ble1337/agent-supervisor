import React, { useEffect, useState, useCallback } from 'react';
import { Agent, getAgents } from '../api';
import AgentCard from '../components/AgentCard';
import BroadcastConsole from '../components/BroadcastConsole';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [businessGroup, setBusinessGroup] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAgents = useCallback(async (group: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAgents(group);
      setAgents(data);
    } catch (err) {
      console.error(err);
      setError('Failed to load agents.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchAgents(businessGroup);
  }, [businessGroup, fetchAgents]);

  const knownGroups = ['Acme', 'Stark', 'X Marketing', 'Wayne Ent'];

  return (
    <div className="min-h-screen bg-background text-text p-6 flex flex-col gap-6">
      <header className="flex justify-between items-center border-b border-border pb-4">
        <div>
          <h1 className="text-2xl font-bold text-accent">Agent Supervisor</h1>
          <p className="text-muted text-sm">Operator Cockpit</p>
        </div>
        <div className="flex gap-4 items-center">
          <select
            value={businessGroup}
            onChange={(e) => setBusinessGroup(e.target.value)}
            className="bg-surface border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2.5"
            aria-label="Filter by Business Group"
          >
            <option value="">All Businesses</option>
            {knownGroups.map((group) => (
              <option key={group} value={group}>
                {group}
              </option>
            ))}
          </select>
          <Link
            to="/add"
            className="px-4 py-2 bg-accent text-[#0d1117] font-bold rounded hover:bg-blue-400 transition-colors whitespace-nowrap text-sm"
          >
            + Add Agent
          </Link>
        </div>
      </header>

      <main>
        {loading ? (
          <div className="text-muted">Loading agents...</div>
        ) : error ? (
          <div className="text-error">{error}</div>
        ) : agents.length === 0 ? (
          <div className="text-muted">No agents found.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {agents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        )}
      </main>

      <footer className="mt-auto pt-6 border-t border-border">
        <BroadcastConsole agents={agents} />
      </footer>
    </div>
  );
};

export default Dashboard;
