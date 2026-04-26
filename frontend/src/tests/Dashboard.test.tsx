import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Dashboard from '../pages/Dashboard';
import * as api from '../api';

import { MemoryRouter } from 'react-router-dom';

vi.mock('../api', () => ({
  getAgents: vi.fn(),
}));

vi.mock('../components/BroadcastConsole', () => ({
  default: () => <div data-testid="broadcast-console">Broadcast Console</div>
}));

describe('Dashboard', () => {
  const mockAgents = [
    { id: '1', name: 'Agent 1', ip_address: '10.0.0.1', ssh_username: 'u1', api_endpoint: 'http://1', business_group: 'Acme', created_at: 'now' },
    { id: '2', name: 'Agent 2', ip_address: '10.0.0.2', ssh_username: 'u2', api_endpoint: 'http://2', business_group: 'Stark', created_at: 'now' },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
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

    expect(screen.getByText('Agent 1')).toBeInTheDocument();
    expect(screen.getByText('Agent 2')).toBeInTheDocument();

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
      expect(screen.queryByText('Agent 2')).not.toBeInTheDocument();
    });
    expect(screen.getByText('Agent 1')).toBeInTheDocument();
  });
});
