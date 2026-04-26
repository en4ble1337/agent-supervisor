import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import AddAgent from './pages/AddAgent';
import AgentDetail from './pages/AgentDetail';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/add" element={<AddAgent />} />
        <Route path="/agents/:id" element={<AgentDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
