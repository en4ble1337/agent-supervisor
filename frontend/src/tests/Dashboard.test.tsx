import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Dashboard from '../pages/Dashboard';
import * as api from '../api';

import { MemoryRouter } from 'react-router-dom';

vi.mock('../api', () => ({
  getAgents: vi.fn(),
  getAgentStatus: vi.fn(),
}));

describe('Dashboard', () => {
  const mockAgents = [
    { id: '1', name: 'Agent 1', ip_address: '10.0.0.1', ssh_username: 'u1', api_endpoint: 'http://1', business_group: 'Acme', created_at: 'now' },
    { id: '2', name: 'Agent 2', ip_address: '10.0.0.2', ssh_username: 'u2', api_endpoint: 'http://2', business_group: 'Stark', created_at: 'now' },
  ];

  const mockStatus = {
    id: '1',
    status: 'running',
    active_tasks: [
      { id: 'task-1', description: 'Build prospect database' },
      { id: 'task-2', description: 'Enrich contacts' },
    ],
    cron_jobs: [{ id: 'cron-1', schedule: '0 8 * * *' }],
    intel: {
      source: 'ssh-cli',
      sections: [{ id: 'runtime', title: 'Hermes Status', content: 'Gateway Service: running' }],
    },
  };

  beforeEach(() => {
    vi.resetAllMocks();
    vi.mocked(api.getAgentStatus).mockResolvedValue(mockStatus);
  });

  it('renders agents and filters by business group', async () => {
    vi.mocked(api.getAgents).mockResolvedValue(mockAgents);

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    // Initial load fetches all agents
    await waitFor(() => {
      expect(api.getAgents).toHaveBeenCalledWith('');
    });

    expect(screen.getAllByText('Agent 1').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Agent 2').length).toBeGreaterThan(0);

    // Now let's filter by Acme
    const filterSelect = screen.getByRole('combobox');
    
    // Changing the filter should refetch
    vi.mocked(api.getAgents).mockResolvedValue([mockAgents[0]]);
    fireEvent.change(filterSelect, { target: { value: 'Acme' } });

    await waitFor(() => {
      expect(api.getAgents).toHaveBeenCalledWith('Acme');
    });

    // Wait for the UI to update
    await waitFor(() => {
      expect(screen.queryAllByText('Agent 2')).toHaveLength(0);
    });
    expect(screen.getAllByText('Agent 1').length).toBeGreaterThan(0);
  });

  it('renders live cockpit statistics from agent status and removes broadcast controls', async () => {
    vi.mocked(api.getAgents).mockResolvedValue(mockAgents);
    vi.mocked(api.getAgentStatus).mockImplementation(async (id: string) => {
      if (id === '2') {
        throw new Error('Agent API is unreachable.');
      }
      return mockStatus;
    });

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(api.getAgentStatus).toHaveBeenCalledTimes(2);
    });

    expect(screen.getByTestId('total-agents-stat')).toHaveTextContent('2');
    expect(screen.getByTestId('online-agents-stat')).toHaveTextContent('1');
    expect(screen.getByTestId('attention-agents-stat')).toHaveTextContent('1');
    expect(screen.getByTestId('active-tasks-stat')).toHaveTextContent('2');
    expect(screen.getByTestId('cron-jobs-stat')).toHaveTextContent('1');
    expect(screen.getAllByText('Runtime Intel').length).toBeGreaterThan(0);
    expect(screen.getByText('Build prospect database')).toBeInTheDocument();
    expect(screen.queryByText('Broadcast Console')).not.toBeInTheDocument();
    expect(screen.queryByTestId('broadcast-console')).not.toBeInTheDocument();
  });
});
