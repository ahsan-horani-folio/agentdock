import React from "react";
import QueryForm from './components/QueryForm';
import AgentRegistry from './components/AgentRegistry';

function App() {
  return (
    <div className="min-h-screen bg-white text-gray-800 p-4">
      <QueryForm />
      <AgentRegistry />
    </div>
  );
}

export default App;
