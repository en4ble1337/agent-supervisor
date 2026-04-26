import React, { useCallback, useEffect, useRef, useState } from 'react';

import { ChatMessage, getChatHistory, sendMessage } from '../api';

interface ChatTerminalProps {
  agentId: string;
}

const ChatTerminal: React.FC<ChatTerminalProps> = ({ agentId }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  const fetchHistory = useCallback(async () => {
    try {
      const history = await getChatHistory(agentId);
      setMessages(history);
    } catch (err) {
      console.error('Failed to fetch history', err);
    } finally {
      setFetching(false);
    }
  }, [agentId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchHistory();
  }, [fetchHistory]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputText.trim() || loading) return;

    const userContent = inputText;
    setInputText('');
    setLoading(true);

    try {
      await sendMessage(agentId, userContent);
      // Refetch history to get both user and agent message with correct IDs/timestamps
      await fetchHistory();
    } catch (err) {
      console.error('Failed to send message', err);
      alert('Failed to send message.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-black border border-border rounded-lg overflow-hidden font-mono">
      <header className="bg-surface p-3 border-b border-border flex justify-between items-center">
        <span className="text-accent text-xs">DIRECT_COMMS_V1.0</span>
        <span className="text-muted text-[10px]">ENCRYPTED SESSION</span>
      </header>

      <div ref={scrollRef} className="flex-1 p-4 overflow-y-auto flex flex-col gap-4 text-sm">
        {fetching ? (
          <div className="text-muted italic">Initializing session...</div>
        ) : messages.length === 0 ? (
          <div className="text-muted italic text-center py-10">No message history. Start typing below.</div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className={`max-w-[80%] p-3 rounded ${
                  msg.role === 'user'
                    ? 'bg-accent text-black rounded-tr-none'
                    : 'bg-surface text-text border border-border rounded-tl-none'
                }`}
              >
                <div className="text-[10px] opacity-50 mb-1">
                  {msg.role.toUpperCase()} - {new Date(msg.timestamp).toLocaleTimeString()}
                </div>
                <div className="whitespace-pre-wrap">{msg.content}</div>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex items-start">
            <div className="bg-surface text-muted border border-border p-2 rounded rounded-tl-none italic text-xs animate-pulse">
              Agent is processing...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSend} className="p-4 bg-surface border-t border-border flex gap-2">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          className="flex-1 bg-background border border-border rounded p-2 text-sm focus:ring-accent focus:border-accent resize-none h-10"
          rows={1}
        />
        <button
          type="submit"
          disabled={loading || !inputText.trim()}
          className="bg-accent text-black px-4 py-1 rounded font-bold hover:bg-blue-400 disabled:opacity-50 transition-colors"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatTerminal;
