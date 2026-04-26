import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AgentCard from '../components/AgentCard';

import { MemoryRouter } from 'react-router-dom';

describe('AgentCard', () => {
  it('renders agent details correctly', () => {
    const mockAgent = {
      id: '123',
      name: 'Hermes Lead Gen',
      ip_address: '10.0.0.5',
      ssh_username: 'admin',
      api_endpoint: 'http://10.0.0.5:8000',
      business_group: 'Acme',
      created_at: '2023-10-01T12:00:00Z',
    };

    render(
      <MemoryRouter>
        <AgentCard agent={mockAgent} />
      </MemoryRouter>
    );

    expect(screen.getByText('Hermes Lead Gen')).toBeInTheDocument();
    expect(screen.getByText('10.0.0.5')).toBeInTheDocument();
    expect(screen.getByText('Acme')).toBeInTheDocument();
  });
});
