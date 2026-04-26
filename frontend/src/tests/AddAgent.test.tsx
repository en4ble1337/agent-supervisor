import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import AddAgent from '../pages/AddAgent';
import * as api from '../api';
import { MemoryRouter } from 'react-router-dom';

vi.mock('../api', () => ({
  createAgent: vi.fn(),
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<Record<string, unknown>>('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('AddAgent', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  const renderComponent = () => render(
    <MemoryRouter>
      <AddAgent />
    </MemoryRouter>
  );

  it('renders the form correctly', () => {
    renderComponent();
    expect(screen.getByLabelText(/^Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/IP Address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/SSH Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/SSH Password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/API Endpoint/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Business Group/i)).toBeInTheDocument();
  });

  it('submits the form successfully and navigates to dashboard', async () => {
    vi.mocked(api.createAgent).mockResolvedValueOnce({ id: '1' } as api.Agent);

    renderComponent();

    fireEvent.change(screen.getByLabelText(/^Name/i), { target: { value: 'New Agent' } });
    fireEvent.change(screen.getByLabelText(/IP Address/i), { target: { value: '10.0.0.1' } });
    fireEvent.change(screen.getByLabelText(/SSH Username/i), { target: { value: 'admin' } });
    fireEvent.change(screen.getByLabelText(/SSH Password/i), { target: { value: 'pass' } });
    fireEvent.change(screen.getByLabelText(/API Endpoint/i), { target: { value: 'http://10.0.0.1' } });
    fireEvent.change(screen.getByLabelText(/Business Group/i), { target: { value: 'Acme' } });

    fireEvent.click(screen.getByRole('button', { name: /Add Agent/i }));

    await waitFor(() => {
      expect(api.createAgent).toHaveBeenCalledWith({
        name: 'New Agent',
        ip_address: '10.0.0.1',
        ssh_username: 'admin',
        ssh_password: 'pass',
        api_endpoint: 'http://10.0.0.1',
        business_group: 'Acme',
      });
    });

    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('displays SSH_AUTH_FAILED error', async () => {
    vi.mocked(api.createAgent).mockRejectedValueOnce({
      response: { data: { error: { code: 'SSH_AUTH_FAILED' } } }
    });

    renderComponent();

    fireEvent.change(screen.getByLabelText(/^Name/i), { target: { value: 'New Agent' } });
    fireEvent.change(screen.getByLabelText(/IP Address/i), { target: { value: '10.0.0.1' } });
    fireEvent.change(screen.getByLabelText(/SSH Username/i), { target: { value: 'admin' } });
    fireEvent.change(screen.getByLabelText(/SSH Password/i), { target: { value: 'pass' } });
    fireEvent.change(screen.getByLabelText(/API Endpoint/i), { target: { value: 'http://10.0.0.1' } });
    fireEvent.change(screen.getByLabelText(/Business Group/i), { target: { value: 'Acme' } });

    fireEvent.click(screen.getByRole('button', { name: /Add Agent/i }));

    await waitFor(() => {
      expect(screen.getByText(/Invalid SSH credentials/i)).toBeInTheDocument();
    });
  });

  it('displays AGENT_UNREACHABLE error', async () => {
    vi.mocked(api.createAgent).mockRejectedValueOnce({
      response: { data: { error: { code: 'AGENT_UNREACHABLE' } } }
    });

    renderComponent();

    fireEvent.change(screen.getByLabelText(/^Name/i), { target: { value: 'New Agent' } });
    fireEvent.change(screen.getByLabelText(/IP Address/i), { target: { value: '10.0.0.1' } });
    fireEvent.change(screen.getByLabelText(/SSH Username/i), { target: { value: 'admin' } });
    fireEvent.change(screen.getByLabelText(/SSH Password/i), { target: { value: 'pass' } });
    fireEvent.change(screen.getByLabelText(/API Endpoint/i), { target: { value: 'http://10.0.0.1' } });
    fireEvent.change(screen.getByLabelText(/Business Group/i), { target: { value: 'Acme' } });

    fireEvent.click(screen.getByRole('button', { name: /Add Agent/i }));

    await waitFor(() => {
      expect(screen.getByText(/Agent API is unreachable/i)).toBeInTheDocument();
    });
  });
});
