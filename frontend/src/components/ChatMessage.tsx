import { ChatMessage as ChatMessageType } from '../types';
import './ChatMessage.css';

interface ChatMessageProps {
  message: ChatMessageType;
}

function ChatMessage({ message }: ChatMessageProps) {
  const formatTime = (date: Date) => {
    return new Date(date).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`message ${message.isUser ? 'user' : 'ai'}`}>
      <div className="message-avatar">
        {message.isUser ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <div className="message-text">
          {message.content.split('\n').map((line, index) => (
            <span key={index}>
              {line}
              {index < message.content.split('\n').length - 1 && <br />}
            </span>
          ))}
        </div>
        <div className="message-time">{formatTime(message.timestamp)}</div>
      </div>
    </div>
  );
}

export default ChatMessage;

