import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import BroadcastConsole from '../components/BroadcastConsole';
import * as api from '../api';

vi.mock('../api', () => ({
  sendBroadcast: vi.fn(),
}));

describe('BroadcastConsole', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('sends broadcast to business group and displays results', async () => {
    const mockResults = {
      '1': { status: 'success', reply: 'I am ready' },
      '2': { status: 'error', error: 'Timed out' },
    };
    vi.mocked(api.sendBroadcast).mockResolvedValue(mockResults);

    render(<BroadcastConsole agents={[{ id: '1', name: 'A1', business_group: 'Acme', ip_address: '1', ssh_username: 'u', api_endpoint: 'h', created_at: '' }]} />);

    const input = screen.getByPlaceholderText(/Enter broadcast message/i);
    fireEvent.change(input, { target: { value: 'Global Reset' } });
    
    const select = screen.getByLabelText(/Target Business/i);
    fireEvent.change(select, { target: { value: 'Acme' } });

    fireEvent.click(screen.getByRole('button', { name: /Broadcast/i }));

    await waitFor(() => {
      expect(api.sendBroadcast).toHaveBeenCalledWith('Global Reset', 'Acme');
    });

    expect(await screen.findByText(/I am ready/i)).toBeInTheDocument();
    expect(screen.getByText(/Timed out/i)).toBeInTheDocument();
  });
});
