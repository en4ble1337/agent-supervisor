import axios from 'axios';

export interface Agent {
  id: string;
  name: string;
  ip_address: string;
  ssh_username: string;
  api_endpoint: string;
  business_group: string;
  created_at: string;
}

export interface AgentCreate {
  name: string;
  ip_address: string;
  ssh_username: string;
  ssh_password: string;
  api_endpoint: string;
  business_group: string;
}

export interface AgentStatus {
  id: string;
  status: string;
  active_tasks: Array<{ id: string; description: string }>;
  cron_jobs: Array<{ id: string; schedule: string }>;
}

export interface FileInfo {
  name: string;
  type: string;
}

export interface ChatMessage {
  id: string;
  agent_id: string;
  role: string;
  content: string;
  timestamp: string;
}

export interface AgentLogs {
  logs: string;
}

export const getAgents = async (businessGroup?: string): Promise<Agent[]> => {
  const response = await axios.get('/api/agents', {
    params: { business_group: businessGroup },
  });
  return response.data;
};

export const createAgent = async (agent: AgentCreate): Promise<Agent> => {
  const response = await axios.post('/api/agents', agent);
  return response.data;
};

export const getAgentStatus = async (id: string): Promise<AgentStatus> => {
  const response = await axios.get(`/api/agents/${id}/status`);
  return response.data;
};

export const getAgentFiles = async (id: string, path: string): Promise<FileInfo[]> => {
  const response = await axios.get(`/api/agents/${id}/files`, {
    params: { path },
  });
  return response.data;
};

export const getAgentLogs = async (id: string, logPath?: string): Promise<AgentLogs> => {
  const response = await axios.get(`/api/agents/${id}/logs`, {
    params: { log_path: logPath },
  });
  return response.data;
};

export const sendMessage = async (id: string, content: string): Promise<ChatMessage> => {
  const response = await axios.post(`/api/agents/${id}/chat`, { content });
  return response.data;
};

export const getChatHistory = async (id: string): Promise<ChatMessage[]> => {
  const response = await axios.get(`/api/agents/${id}/chat`);
  return response.data;
};

export const sendBroadcast = async (
  content: string,
  businessGroup?: string,
  agentIds?: string[],
): Promise<Record<string, { status: string; reply?: string; error?: string }>> => {
  const response = await axios.post('/api/broadcast', {
    content,
    business_group: businessGroup,
    agent_ids: agentIds,
  });
  return response.data;
};

export const triggerAgentAction = async (id: string, action: string, params: Record<string, any> = {}): Promise<any> => {
  const response = await axios.post(`/api/agents/${id}/actions`, { action, params });
  return response.data;
};

export const addAgentCron = async (id: string, name: string, schedule: string, command: string): Promise<any> => {
  const response = await axios.post(`/api/agents/${id}/crons`, { name, schedule, command });
  return response.data;
};

export const deleteAgentCron = async (id: string, name: string): Promise<any> => {
  const response = await axios.delete(`/api/agents/${id}/crons/${name}`);
  return response.data;
};
