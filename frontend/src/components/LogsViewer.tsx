import React, { useEffect, useState, useCallback, useRef } from 'react';
import { getAgentLogs } from '../api';

interface LogsViewerProps {
  agentId: string;
}

const LogsViewer: React.FC<LogsViewerProps> = ({ agentId }) => {
  const [logs, setLogs] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAgentLogs(agentId);
      setLogs(data.logs);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch logs.');
    } finally {
      setLoading(false);
    }
  }, [agentId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchLogs();
  }, [fetchLogs]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="flex flex-col gap-4 h-full">
      <header className="flex justify-between items-center bg-surface border border-border p-3 rounded-t-lg">
        <div className="flex items-center gap-4 text-sm font-mono">
          <span className="text-muted">Source:</span>
          <span className="text-text">/var/log/syslog [tail]</span>
        </div>
        <button 
          onClick={fetchLogs}
          className="text-xs px-2 py-1 bg-background border border-border rounded hover:bg-border transition-colors"
        >
          Refresh
        </button>
      </header>

      <div 
        ref={scrollRef}
        className="bg-black border-x border-b border-border rounded-b-lg p-4 h-[500px] overflow-y-auto font-mono text-xs leading-relaxed"
      >
        {loading && !logs ? (
          <div className="text-muted italic">Connecting to log stream...</div>
        ) : error ? (
          <div className="text-error">{error}</div>
        ) : (
          <pre className="whitespace-pre-wrap break-all text-success">
            {logs || 'No logs available.'}
          </pre>
        )}
      </div>
    </div>
  );
};

export default LogsViewer;
