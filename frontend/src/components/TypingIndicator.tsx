import './TypingIndicator.css';

function TypingIndicator() {
  return (
    <div className="message ai">
      <div className="message-avatar">🤖</div>
      <div className="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
}

export default TypingIndicator;

