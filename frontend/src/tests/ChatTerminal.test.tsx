import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ChatTerminal from '../components/ChatTerminal';
import * as api from '../api';

vi.mock('../api', () => ({
  getChatHistory: vi.fn(),
  sendMessage: vi.fn(),
}));

describe('ChatTerminal', () => {
  const mockHistory = [
    { id: 'm1', role: 'user', content: 'hello', timestamp: '2026-04-24T12:00:00Z' },
    { id: 'm2', role: 'agent', content: 'hi there', timestamp: '2026-04-24T12:00:01Z' },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('renders history and sends new message', async () => {
    vi.mocked(api.getChatHistory).mockResolvedValueOnce(mockHistory);
    vi.mocked(api.sendMessage).mockResolvedValue({
      id: 'm3', role: 'agent', content: 'replying...', timestamp: '2026-04-24T12:00:02Z'
    });
    // On second fetchHistory call, return the new list
    vi.mocked(api.getChatHistory).mockResolvedValueOnce([
      ...mockHistory,
      { id: 'm2.5', role: 'user', content: 'how are you?', timestamp: '2026-04-24T12:00:02Z' },
      { id: 'm3', role: 'agent', content: 'replying...', timestamp: '2026-04-24T12:00:02Z' }
    ]);

    render(<ChatTerminal agentId="123" />);

    await waitFor(() => {
      expect(api.getChatHistory).toHaveBeenCalledWith('123');
    });

    expect(screen.getByText('hello')).toBeInTheDocument();
    expect(screen.getByText('hi there')).toBeInTheDocument();

    const input = screen.getByPlaceholderText(/Type a message/i);
    fireEvent.change(input, { target: { value: 'how are you?' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });

    await waitFor(() => {
      expect(api.sendMessage).toHaveBeenCalledWith('123', 'how are you?');
    });

    expect(await screen.findByText('replying...')).toBeInTheDocument();
  });
});
