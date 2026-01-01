import './InfoPanel.css';

function InfoPanel() {
  return (
    <aside className="info-panel">
      <div className="info-card">
        <h3>✨ Features</h3>
        <div className="info-card-content">
          <ul className="feature-list">
            <li>Natural language understanding</li>
            <li>Real-time weather forecasts</li>
            <li>Top attractions & landmarks</li>
            <li>Distance-based clustering</li>
            <li>Multi-day trip planning</li>
          </ul>
        </div>
      </div>

      <div className="info-card">
        <h3>💡 Example Queries</h3>
        <div className="info-card-content">
          <div className="example-queries">
            <div className="example-query">"Plan a 4-day trip to London"</div>
            <div className="example-query">"What attractions are near the city center in Amsterdam?"</div>
            <div className="example-query">"Tell me about the weather in Dubai"</div>
            <div className="example-query">"I want to explore New York for a weekend"</div>
          </div>
        </div>
      </div>

      <div className="info-card">
        <h3>🔧 Tech Stack</h3>
        <div className="info-card-content">
          <ul className="feature-list">
            <li>GPT-4 for NLP</li>
            <li>OpenWeatherMap API</li>
            <li>Foursquare Places API</li>
            <li>Redis caching</li>
            <li>React + TypeScript</li>
          </ul>
        </div>
      </div>
    </aside>
  );
}

export default InfoPanel;

