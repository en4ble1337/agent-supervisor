import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import LogsViewer from '../components/LogsViewer';
import * as api from '../api';

vi.mock('../api', () => ({
  getAgentLogs: vi.fn(),
}));

describe('LogsViewer', () => {
  const mockLogs = { logs: '2026-04-24: Booting...\n2026-04-24: Agent online.' };

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('renders logs correctly and refreshes', async () => {
    vi.mocked(api.getAgentLogs).mockResolvedValue(mockLogs);

    render(<LogsViewer agentId="123" />);

    await waitFor(() => {
      expect(api.getAgentLogs).toHaveBeenCalledWith('123');
    });

    expect(screen.getByText(/Booting.../i)).toBeInTheDocument();
    expect(screen.getByText(/Agent online./i)).toBeInTheDocument();

    // Refresh
    const newLogs = { logs: '2026-04-24: Booting...\n2026-04-24: Agent online.\n2026-04-24: Task received.' };
    vi.mocked(api.getAgentLogs).mockResolvedValue(newLogs);
    fireEvent.click(screen.getByRole('button', { name: /refresh/i }));

    await waitFor(() => {
      expect(screen.getByText(/Task received./i)).toBeInTheDocument();
    });
  });
});
