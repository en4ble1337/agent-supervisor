import { describe, it, expect, vi } from 'vitest';
import axios from 'axios';
import { 
  getAgents, 
  createAgent, 
  getAgentStatus, 
  getAgentFiles, 
  getAgentLogs, 
  sendMessage, 
  getChatHistory, 
  sendBroadcast
} from '../api';

vi.mock('axios');

describe('API Service', () => {
  describe('getAgents', () => {
    it('fetches agents without business group filter', async () => {
      const mockAgents = [{ id: '1', name: 'Agent 1', business_group: 'Acme' }];
      vi.mocked(axios.get).mockResolvedValueOnce({ data: mockAgents });

      const agents = await getAgents();

      expect(axios.get).toHaveBeenCalledWith('/api/agents', { params: { business_group: undefined } });
      expect(agents).toEqual(mockAgents);
    });

    it('fetches agents with business group filter', async () => {
      const mockAgents = [{ id: '1', name: 'Agent 1', business_group: 'Acme' }];
      vi.mocked(axios.get).mockResolvedValueOnce({ data: mockAgents });

      const agents = await getAgents('Acme');

      expect(axios.get).toHaveBeenCalledWith('/api/agents', { params: { business_group: 'Acme' } });
      expect(agents).toEqual(mockAgents);
    });
  });

  describe('createAgent', () => {
    it('sends POST request to create an agent', async () => {
      const mockAgent = { id: '2', name: 'Agent 2' };
      const payload = { name: 'Agent 2', ip_address: '1.1.1.1', ssh_username: 'u', ssh_password: 'p', api_endpoint: 'http', business_group: 'Acme' };
      
      vi.mocked(axios.post).mockResolvedValueOnce({ data: mockAgent });

      const result = await createAgent(payload);

      expect(axios.post).toHaveBeenCalledWith('/api/agents', payload);
      expect(result).toEqual(mockAgent);
    });
  });

  describe('getAgentStatus', () => {
    it('fetches agent status by id', async () => {
      const mockStatus = { id: '1', status: 'online', active_tasks: [], cron_jobs: [] };
      vi.mocked(axios.get).mockResolvedValueOnce({ data: mockStatus });

      const result = await getAgentStatus('1');

      expect(axios.get).toHaveBeenCalledWith('/api/agents/1/status');
      expect(result).toEqual(mockStatus);
    });
  });

  describe('getAgentFiles', () => {
    it('fetches agent files by path', async () => {
      const mockFiles = [{ name: 'test.txt', type: 'file' }];
      vi.mocked(axios.get).mockResolvedValueOnce({ data: mockFiles });

      const result = await getAgentFiles('1', '/tmp');

      expect(axios.get).toHaveBeenCalledWith('/api/agents/1/files', { params: { path: '/tmp' } });
      expect(result).toEqual(mockFiles);
    });
  });

  describe('getAgentLogs', () => {
    it('fetches agent logs', async () => {
      const mockLogs = { logs: 'line 1\nline 2' };
      vi.mocked(axios.get).mockResolvedValueOnce({ data: mockLogs });

      const result = await getAgentLogs('1');

      expect(axios.get).toHaveBeenCalledWith('/api/agents/1/logs', { params: { log_path: undefined } });
      expect(result).toEqual(mockLogs);
    });
  });

  describe('sendMessage', () => {
    it('sends a chat message and returns reply', async () => {
      const mockReply = { id: 'm1', content: 'hello', role: 'agent' };
      vi.mocked(axios.post).mockResolvedValueOnce({ data: mockReply });

      const result = await sendMessage('1', 'hi');

      expect(axios.post).toHaveBeenCalledWith('/api/agents/1/chat', { content: 'hi' });
      expect(result).toEqual(mockReply);
    });
  });

  describe('getChatHistory', () => {
    it('fetches chat history', async () => {
      const mockHistory = [{ id: 'm1', content: 'hi', role: 'user' }];
      vi.mocked(axios.get).mockResolvedValueOnce({ data: mockHistory });

      const result = await getChatHistory('1');

      expect(axios.get).toHaveBeenCalledWith('/api/agents/1/chat');
      expect(result).toEqual(mockHistory);
    });
  });

  describe('sendBroadcast', () => {
    it('sends a broadcast message', async () => {
      const mockResult = { '1': { status: 'success' } };
      vi.mocked(axios.post).mockResolvedValueOnce({ data: mockResult });

      const result = await sendBroadcast('hello', 'Acme');

      expect(axios.post).toHaveBeenCalledWith('/api/broadcast', { content: 'hello', business_group: 'Acme', agent_ids: undefined });
      expect(result).toEqual(mockResult);
    });
  });
});
