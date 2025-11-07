import React from 'react';
import { DeploymentForm } from './components/DeploymentForm';

const App: React.FC = () => {
  return (
    <div style={{ padding: '20px', backgroundColor: '#121212', color: '#00FFA3', minHeight: '100vh' }}>
      <h1>AI-Powered Autodeploy Dashboard</h1>
      <DeploymentForm />
    </div>
  );
};

export default App;
