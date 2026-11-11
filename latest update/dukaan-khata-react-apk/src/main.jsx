import React from 'react';
import { createRoot } from 'react-dom/client';
import { Capacitor } from '@capacitor/core';
import './style.css';

function App() {
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    // Wait until the app shell is mounted before showing the supplied prototype.
    setReady(true);
  }, []);
  return (
    <main className="app-shell">
      {!ready && <div className="loading">Loading app…</div>}
      <iframe
        title="Dukaan Khata mobile prototype"
        src={Capacitor.isNativePlatform() ? "/prototype.html?native=1" : "/prototype.html"}
        className="prototype-frame"
        allow="clipboard-read; clipboard-write"
      />
      <div className="platform-note" aria-hidden="true">
        {Capacitor.isNativePlatform() ? '' : ''}
      </div>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);
