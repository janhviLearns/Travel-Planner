import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <div className="logo-icon">🌍</div>
          <div className="logo-text">
            <h1>AI Travel Planner</h1>
            <p>Natural Language Travel Intelligence</p>
          </div>
        </div>
        <div className="api-badge">
          Powered by GPT-4
        </div>
      </div>
    </header>
  );
}

export default Header;

