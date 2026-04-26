import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import FileBrowser from '../components/FileBrowser';
import * as api from '../api';

vi.mock('../api', () => ({
  getAgentFiles: vi.fn(),
}));

describe('FileBrowser', () => {
  const mockFiles = [
    { name: 'src', type: 'directory' },
    { name: 'README.md', type: 'file' },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('renders files and navigates directories', async () => {
    vi.mocked(api.getAgentFiles).mockResolvedValue(mockFiles);

    render(<FileBrowser agentId="123" />);

    // Initial load for root
    await waitFor(() => {
      expect(api.getAgentFiles).toHaveBeenCalledWith('123', '/');
    });

    expect(await screen.findByText('src')).toBeInTheDocument();
    expect(screen.getByText('README.md')).toBeInTheDocument();

    // Click on directory to navigate
    vi.mocked(api.getAgentFiles).mockResolvedValue([{ name: 'main.py', type: 'file' }]);
    fireEvent.click(screen.getByText('src'));

    await waitFor(() => {
      expect(api.getAgentFiles).toHaveBeenCalledWith('123', '/src');
    });

    expect(await screen.findByText('main.py')).toBeInTheDocument();
    expect(screen.queryByText('README.md')).not.toBeInTheDocument();
  });
});
