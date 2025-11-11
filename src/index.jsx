import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css'; // Import the global CSS
import { ThemeProvider } from './context/ThemeContext'; // Import ThemeProvider

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider> {/* Wrap App with ThemeProvider */}
        <App />
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);