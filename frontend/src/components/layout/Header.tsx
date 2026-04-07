import { useState, useEffect } from 'react';
import api from '../../services/api';

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export default function Header({ title, subtitle }: HeaderProps) {
  const [apiStatus, setApiStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await api.get('/api/health');
        setApiStatus('connected');
      } catch {
        setApiStatus('disconnected');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="header">
      <div>
        <div className="header-title">{title}</div>
        {subtitle && <div className="header-subtitle">{subtitle}</div>}
      </div>
      <div className="header-actions">
        <div className={`api-badge ${apiStatus === 'checking' ? 'connected' : apiStatus}`}>
          <div className="status-dot" />
          {apiStatus === 'checking' ? 'Checking...' : apiStatus === 'connected' ? 'API Connected' : 'API Offline'}
        </div>
      </div>
    </div>
  );
}
