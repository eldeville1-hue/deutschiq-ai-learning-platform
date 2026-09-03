// frontend/mini-app/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';
import './styles/v6.css';
import './styles/v13.css';

const telegram = (window as any).Telegram?.WebApp;
telegram?.ready();
telegram?.expand();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
