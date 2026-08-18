import { render, screen, waitFor, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import OperationsTab from '../components/OperationsTab';
import * as api from '../api';

vi.mock('../api', () => ({
  getAgentStatus: vi.fn(),
}));

describe('OperationsTab', () => {
  const mockStatus = {
    id: '123',
    status: 'online',
    active_tasks: [{ id: 't1', description: 'Working on SEO' }],
    cron_jobs: [{ id: 'c1', schedule: '0 * * * *' }],
    intel: {
      source: 'ssh-cli',
      sections: [
        { id: 'hermes-status', title: 'Hermes Status', content: 'Gateway Service: running' },
        { id: 'hermes-sessions', title: 'Sessions', content: 'Research  2h ago  20260503_abc' },
      ],
    },
  };

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('renders status and tasks correctly', async () => {
    vi.mocked(api.getAgentStatus).mockResolvedValue(mockStatus);

    render(<OperationsTab agentId="123" />);

    expect(await screen.findByText(/online/i)).toBeInTheDocument();
    expect(screen.getByText('Working on SEO')).toBeInTheDocument();
    expect(screen.getByText('0 * * * *')).toBeInTheDocument();
    expect(screen.getByText(/Runtime Intel/i)).toBeInTheDocument();
    expect(screen.getByText(/Gateway Service: running/i)).toBeInTheDocument();
    expect(screen.getByText(/Research\s+2h ago/i)).toBeInTheDocument();
  });

  it('does not render direct control forms in the observability view', async () => {
    vi.mocked(api.getAgentStatus).mockResolvedValue(mockStatus);

    render(<OperationsTab agentId="123" />);

    expect(await screen.findByText(/Runtime Intel/i)).toBeInTheDocument();
    expect(screen.queryByText(/Quick Actions/i)).not.toBeInTheDocument();
    expect(screen.queryByPlaceholderText(/Action name/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Add Cron Job/i)).not.toBeInTheDocument();
  });

  it('refreshes data when refresh button is clicked', async () => {
    vi.mocked(api.getAgentStatus).mockResolvedValue(mockStatus);
    render(<OperationsTab agentId="123" />);

    await waitFor(() => expect(api.getAgentStatus).toHaveBeenCalledTimes(1));

    const refreshBtn = screen.getByRole('button', { name: /refresh/i });
    fireEvent.click(refreshBtn);

    await waitFor(() => expect(api.getAgentStatus).toHaveBeenCalledTimes(2));
  });

  it('polls for status every 15 minutes', async () => {
    vi.useFakeTimers();
    vi.mocked(api.getAgentStatus).mockResolvedValue(mockStatus);
    render(<OperationsTab agentId="123" />);

    await vi.waitFor(() => expect(api.getAgentStatus).toHaveBeenCalledTimes(1));

    // Fast-forward 15 minutes
    act(() => {
      vi.advanceTimersByTime(15 * 60 * 1000);
    });

    await vi.waitFor(() => expect(api.getAgentStatus).toHaveBeenCalledTimes(2));
    vi.useRealTimers();
  });
});
