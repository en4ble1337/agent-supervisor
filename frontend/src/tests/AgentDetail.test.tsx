import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import AgentDetail from '../pages/AgentDetail';
import { MemoryRouter, Route, Routes } from 'react-router-dom';

// Mock all components used in tabs to avoid actual API calls
vi.mock('../components/OperationsTab', () => ({
  default: () => <div>Operations Content</div>
}));
vi.mock('../components/FileBrowser', () => ({
  default: () => <div>Files Content</div>
}));
vi.mock('../components/LogsViewer', () => ({
  default: () => <div>Logs Content</div>
}));
vi.mock('../components/ChatTerminal', () => ({
  default: () => <div>Chat Content</div>
}));

describe('AgentDetail', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  const renderComponent = () => render(
    <MemoryRouter initialEntries={['/agents/123']}>
      <Routes>
        <Route path="/agents/:id" element={<AgentDetail />} />
      </Routes>
    </MemoryRouter>
  );

  it('renders all tabs and defaults to Operations', () => {
    renderComponent();
    expect(screen.getByRole('button', { name: /Operations/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Chat/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Files/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Logs/i })).toBeInTheDocument();
    
    expect(screen.getByText(/Operations Content/i)).toBeInTheDocument();
  });

  it('switches tabs on click', async () => {
    renderComponent();
    
    fireEvent.click(screen.getByRole('button', { name: /Chat/i }));
    expect(screen.getByText(/Chat Content/i)).toBeInTheDocument();
    expect(screen.queryByText(/Operations Content/i)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Files/i }));
    expect(screen.getByText(/Files Content/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Logs/i }));
    expect(screen.getByText(/Logs Content/i)).toBeInTheDocument();
  });
});
