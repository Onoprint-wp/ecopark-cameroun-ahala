import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { EcoParkProvider } from './context/EcoParkContext';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <EcoParkProvider>
          <App />
        </EcoParkProvider>
      </AuthProvider>
    </ThemeProvider>
  </StrictMode>
);
