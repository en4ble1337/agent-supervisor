import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import OperationsTab from '../components/OperationsTab';
import FileBrowser from '../components/FileBrowser';
import LogsViewer from '../components/LogsViewer';
import ChatTerminal from '../components/ChatTerminal';

type TabType = 'operations' | 'chat' | 'files' | 'logs';

const AgentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState<TabType>('operations');

  const tabs: Array<{ id: TabType; label: string }> = [
    { id: 'operations', label: 'Operations' },
    { id: 'chat', label: 'Chat' },
    { id: 'files', label: 'Files' },
    { id: 'logs', label: 'Logs' },
  ];

  return (
    <div className="min-h-screen bg-background text-text flex flex-col">
      <header className="bg-surface border-b border-border p-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Link to="/" className="text-muted hover:text-accent transition-colors text-sm">
            &larr; Back to Dashboard
          </Link>
          <h1 className="text-xl font-bold text-accent">Agent Details</h1>
        </div>
        <div className="text-xs font-mono text-muted bg-background px-2 py-1 rounded border border-border">
          ID: {id}
        </div>
      </header>

      <nav className="bg-surface border-b border-border flex px-4">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-6 py-3 text-sm font-bold border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-accent text-accent'
                : 'border-transparent text-muted hover:text-text'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="flex-1 p-6 overflow-auto max-w-5xl w-full mx-auto">
        {activeTab === 'operations' && (
          <div data-testid="operations-tab">
            <OperationsTab agentId={id || ''} />
          </div>
        )}
        {activeTab === 'chat' && (
          <div data-testid="chat-tab">
            <ChatTerminal agentId={id || ''} />
          </div>
        )}
        {activeTab === 'files' && (
          <div data-testid="files-tab">
            <FileBrowser agentId={id || ''} />
          </div>
        )}
        {activeTab === 'logs' && (
          <div data-testid="logs-tab">
            <LogsViewer agentId={id || ''} />
          </div>
        )}
      </main>
    </div>
  );
};

export default AgentDetail;
