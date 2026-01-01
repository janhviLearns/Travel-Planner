import { useState, useRef, useEffect } from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { sendChatMessage } from '../api';
import ChatMessage from './ChatMessage';
import TypingIndicator from './TypingIndicator';
import './ChatInterface.css';

const SUGGESTIONS = [
  { emoji: '🗼', label: '3 days in Paris', query: 'Plan a 3-day trip to Paris' },
  { emoji: '🌤️', label: 'Tokyo weather', query: "What's the weather like in Tokyo?" },
  { emoji: '🏛️', label: 'Rome attractions', query: 'Tell me about attractions in Rome' },
  { emoji: '🏖️', label: 'Barcelona itinerary', query: 'I want to visit Barcelona for 5 days' },
];

function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    // Welcome message
    const timer = setTimeout(() => {
      if (messages.length === 0) {
        addMessage(
          "Hello! 👋 I'm your AI travel assistant. Ask me about any destination, and I'll help you plan your trip with weather forecasts, attractions, and personalized recommendations!",
          false
        );
      }
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  const addMessage = (content: string, isUser: boolean) => {
    const newMessage: ChatMessageType = {
      id: Date.now().toString(),
      content,
      isUser,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    console.log('[ChatInterface] Submitting message:', userMessage);
    setInput('');
    addMessage(userMessage, true);
    setIsLoading(true);

    try {
      console.log('[ChatInterface] Calling sendChatMessage...');
      const response = await sendChatMessage(userMessage);
      console.log('[ChatInterface] Received response:', response);
      
      if (response.response) {
        console.log('[ChatInterface] Adding response message:', response.response.substring(0, 100));
        addMessage(response.response, false);
      } else if (response.error) {
        console.warn('[ChatInterface] Error in response:', response.error);
        addMessage(`Sorry, I encountered an error: ${response.error}`, false);
      } else {
        console.warn('[ChatInterface] No response or error in data');
        addMessage("I'm not sure how to respond to that. Could you try rephrasing?", false);
      }
    } catch (error) {
      console.error('[ChatInterface] Exception caught:', error);
      addMessage(
        "I'm having trouble connecting. Please check if the server is running.",
        false
      );
      console.error('Error:', error);
    } finally {
      console.log('[ChatInterface] Setting isLoading to false');
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (query: string) => {
    setInput(query);
    textareaRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-section">
      <div className="chat-container">
        <div className="chat-header">
          <h2>Chat with Travel AI</h2>
          <p>Ask me anything about destinations, weather, attractions, and travel planning!</p>
        </div>

        <div className="chat-messages">
          {messages.length === 0 && !isLoading && (
            <div className="empty-state">
              <div className="empty-state-icon">💬</div>
              <h3>Start a Conversation</h3>
              <p>Ask me about any destination and I'll help you plan your perfect trip!</p>
            </div>
          )}
          
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          
          {isLoading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        <form className="chat-input-container" onSubmit={handleSubmit}>
          <div className="chat-input-wrapper">
            <textarea
              ref={textareaRef}
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="e.g., Plan a 3-day trip to Paris..."
              rows={1}
              disabled={isLoading}
            />
            <button
              type="submit"
              className="send-button"
              disabled={!input.trim() || isLoading}
            >
              <span>Send</span>
              <span>📤</span>
            </button>
          </div>
          <div className="suggestions">
            {SUGGESTIONS.map((suggestion, index) => (
              <button
                key={index}
                type="button"
                className="suggestion-chip"
                onClick={() => handleSuggestionClick(suggestion.query)}
                disabled={isLoading}
              >
                {suggestion.emoji} {suggestion.label}
              </button>
            ))}
          </div>
        </form>
      </div>
    </div>
  );
}

export default ChatInterface;

