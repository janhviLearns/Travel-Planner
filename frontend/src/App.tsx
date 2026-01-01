import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import InfoPanel from './components/InfoPanel';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <div className="container">
        <ChatInterface />
        <InfoPanel />
      </div>
    </div>
  );
}

export default App;

