import React from 'react';

function Header() {
  // Determine API URL based on environment
  const apiUrl = import.meta.env.VITE_API_URL || 
    (window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api');
  const docsUrl = apiUrl.startsWith('/') 
    ? `${window.location.origin.replace(':80', ':8000')}/docs`
    : `${apiUrl}/docs`;

  return (
    <div className="header">
      <h1>Churn Prediction</h1>
      <div className="header-links">
        <a href={docsUrl} target="_blank" rel="noopener noreferrer">
          API Docs
        </a>
        <a href={apiUrl} target="_blank" rel="noopener noreferrer">
          Backend
        </a>
      </div>
    </div>
  );
}

export default Header;
