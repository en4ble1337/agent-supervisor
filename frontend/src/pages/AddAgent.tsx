import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createAgent } from '../api';

const RUNTIME_DEFAULTS = [
  {
    name: 'OpenClaw',
    port: 18789,
    example: 'http://<ip>:18789',
    note: 'Binds to 127.0.0.1 by default. Bind to 0.0.0.0 for remote access.',
    color: '#f78166',
  },
  {
    name: 'Hermes',
    port: 8642,
    example: 'http://<ip>:8642',
    note: 'Port 8642 is the agent API. Port 9119 is the built-in web dashboard (do not use for this field).',
    color: '#79c0ff',
  },
];

const AddAgent: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDefaults, setShowDefaults] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    ip_address: '',
    ssh_username: '',
    ssh_password: '',
    api_endpoint: '',
    business_group: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createAgent(formData);
      navigate('/');
    } catch (err: unknown) {
      let message = 'An unexpected error occurred.';
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosError = err as { response: { data: { error: { code: string } } } };
        const code = axiosError.response?.data?.error?.code;
        if (code === 'SSH_AUTH_FAILED') {
          message = 'Invalid SSH credentials or unreachable.';
        } else if (code === 'AGENT_UNREACHABLE') {
          message = 'Agent API is unreachable.';
        }
      }
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-text p-6 flex justify-center items-start pt-10">
      <div className="w-full max-w-lg bg-surface border border-border rounded-lg p-6 flex flex-col gap-6">
        <header>
          <h2 className="text-2xl font-bold text-accent">Add Agent</h2>
          <p className="text-muted text-sm">Register a new agent via SSH</p>
        </header>

        {error && (
          <div className="bg-[#f8514920] border border-error text-error px-4 py-2 rounded text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1">
            <label htmlFor="name" className="text-sm font-bold text-text">Name</label>
            <input
              id="name"
              name="name"
              type="text"
              required
              value={formData.name}
              onChange={handleChange}
              className="bg-background border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2"
              placeholder="e.g. Lead Gen Agent"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label htmlFor="ip_address" className="text-sm font-bold text-text">IP Address</label>
            <input
              id="ip_address"
              name="ip_address"
              type="text"
              required
              value={formData.ip_address}
              onChange={handleChange}
              className="bg-background border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2"
              placeholder="e.g. 10.0.0.5"
            />
          </div>

          <div className="flex gap-4">
            <div className="flex flex-col gap-1 w-1/2">
              <label htmlFor="ssh_username" className="text-sm font-bold text-text">SSH Username</label>
              <input
                id="ssh_username"
                name="ssh_username"
                type="text"
                required
                value={formData.ssh_username}
                onChange={handleChange}
                className="bg-background border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2"
              />
            </div>
            <div className="flex flex-col gap-1 w-1/2">
              <label htmlFor="ssh_password" className="text-sm font-bold text-text">SSH Password</label>
              <input
                id="ssh_password"
                name="ssh_password"
                type="password"
                required
                value={formData.ssh_password}
                onChange={handleChange}
                className="bg-background border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2"
              />
            </div>
          </div>

          <div className="flex flex-col gap-1">
            <div className="flex items-center justify-between">
              <label htmlFor="api_endpoint" className="text-sm font-bold text-text">API Endpoint</label>
              <button
                type="button"
                id="runtime-defaults-toggle"
                onClick={() => setShowDefaults(v => !v)}
                className="text-xs text-accent hover:text-blue-300 transition-colors flex items-center gap-1"
              >
                <span>{showDefaults ? '▾' : '▸'}</span>
                Runtime Defaults
              </button>
            </div>
            <input
              id="api_endpoint"
              name="api_endpoint"
              type="text"
              required
              value={formData.api_endpoint}
              onChange={handleChange}
              className="bg-background border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2"
              placeholder="e.g. http://10.0.0.5:18789 (OpenClaw) or :8642 (Hermes)"
            />
            {showDefaults && (
              <div id="runtime-defaults-panel" className="mt-2 rounded border border-border bg-[#161b22] p-3 flex flex-col gap-3">
                <p className="text-xs text-muted uppercase tracking-widest font-bold">Default API Ports by Runtime</p>
                {RUNTIME_DEFAULTS.map(rt => (
                  <div key={rt.name} className="flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      <span
                        className="text-xs font-bold px-2 py-0.5 rounded"
                        style={{ background: `${rt.color}22`, color: rt.color, border: `1px solid ${rt.color}55` }}
                      >
                        {rt.name}
                      </span>
                      <code className="text-xs text-text font-mono">{rt.example}</code>
                      <span className="text-xs text-muted ml-auto">:{rt.port}</span>
                    </div>
                    <p className="text-xs text-muted pl-1">{rt.note}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-col gap-1">
            <label htmlFor="business_group" className="text-sm font-bold text-text">Business Group</label>
            <input
              id="business_group"
              name="business_group"
              type="text"
              required
              value={formData.business_group}
              onChange={handleChange}
              className="bg-background border border-border text-text text-sm rounded focus:ring-accent focus:border-accent block w-full p-2"
              placeholder="e.g. Acme Corp"
            />
          </div>

          <div className="flex justify-end gap-2 mt-4">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="px-4 py-2 bg-background border border-border text-text rounded hover:bg-border transition-colors text-sm"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-accent text-[#0d1117] font-bold rounded hover:bg-blue-400 transition-colors text-sm disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Adding...' : 'Add Agent'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddAgent;
