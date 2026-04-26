import React, { useState } from 'react';

import { Agent, sendBroadcast } from '../api';

interface BroadcastConsoleProps {
  agents: Agent[];
}

const BroadcastConsole: React.FC<BroadcastConsoleProps> = ({ agents }) => {
  const [content, setContent] = useState('');
  const [businessGroup, setBusinessGroup] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Record<string, { status: string; reply?: string; error?: string }> | null>(
    null,
  );

  const businessGroups = Array.from(new Set(agents.map((a) => a.business_group)));

  const handleBroadcast = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    setLoading(true);
    setResults(null);
    try {
      const data = await sendBroadcast(content, businessGroup || undefined);
      setResults(data);
    } catch (err) {
      console.error(err);
      alert('Broadcast failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-surface border border-border rounded-lg p-6 flex flex-col gap-6">
      <header>
        <h2 className="text-xl font-bold text-accent">Multi-Agent Broadcast</h2>
        <p className="text-muted text-sm">Send a command to multiple agents at once</p>
      </header>

      <form onSubmit={handleBroadcast} className="flex flex-col gap-4">
        <div className="flex flex-col gap-1">
          <label htmlFor="target-group" className="text-sm font-bold text-text">
            Target Business
          </label>
          <select
            id="target-group"
            value={businessGroup}
            onChange={(e) => setBusinessGroup(e.target.value)}
            className="bg-background border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2"
          >
            <option value="">All Agents</option>
            {businessGroups.map((bg) => (
              <option key={bg} value={bg}>
                {bg}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label htmlFor="broadcast-msg" className="text-sm font-bold text-text">
            Message
          </label>
          <textarea
            id="broadcast-msg"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter broadcast message..."
            className="bg-background border border-border rounded p-2 text-sm font-mono focus:ring-accent focus:border-accent h-24"
          />
        </div>

        <button
          type="submit"
          disabled={loading || !content.trim()}
          className="bg-accent text-black font-bold py-2 rounded hover:bg-blue-400 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Executing Broadcast...' : '🚀 Execute Broadcast'}
        </button>
      </form>

      {results && (
        <div className="flex flex-col gap-2">
          <h3 className="text-sm font-bold text-muted uppercase">Broadcast Results</h3>
          <div className="flex flex-col gap-2 max-h-60 overflow-y-auto">
            {Object.entries(results).map(([agentId, result]) => {
              const agent = agents.find((a) => a.id === agentId);
              return (
                <div key={agentId} className="bg-background border border-border rounded p-3 text-xs font-mono">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-accent">{agent?.name || agentId}</span>
                    <span className={result.status === 'success' ? 'text-success' : 'text-error'}>
                      {result.status.toUpperCase()}
                    </span>
                  </div>
                  {result.status === 'success' ? (
                    <div className="text-text whitespace-pre-wrap">{result.reply}</div>
                  ) : (
                    <div className="text-error">{result.error}</div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default BroadcastConsole;
