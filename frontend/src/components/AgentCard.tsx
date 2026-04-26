import React from 'react';
import { Link } from 'react-router-dom';
import { Agent } from '../api';

interface AgentCardProps {
  agent: Agent;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent }) => {
  return (
    <Link 
      to={`/agents/${agent.id}`}
      className="bg-surface border border-border rounded-lg p-4 flex flex-col gap-2 hover:border-accent transition-colors block"
    >
      <div className="flex justify-between items-start">
        <h3 className="text-accent font-bold text-lg">{agent.name}</h3>
        <span className="bg-background text-muted text-xs px-2 py-1 rounded border border-border">
          {agent.business_group}
        </span>
      </div>
      <div className="text-sm text-text">
        <div className="flex gap-2">
          <span className="text-muted">IP:</span>
          <span>{agent.ip_address}</span>
        </div>
        <div className="flex gap-2">
          <span className="text-muted">API:</span>
          <span className="truncate">{agent.api_endpoint}</span>
        </div>
      </div>
    </Link>
  );
};

export default AgentCard;
