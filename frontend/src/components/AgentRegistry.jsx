import React, { useState } from 'react';
import axios from 'axios';

export default function AgentRegistry() {
  const [name, setName] = useState("");
  const [type, setType] = useState("github");
  const [config, setConfig] = useState("{}");
  const [message, setMessage] = useState("");

  const registerAgent = async (e) => {
    e.preventDefault();
    try {
      const parsedConfig = config.trim() === "" ? {} : JSON.parse(config);
      const res = await axios.post("http://localhost:8000/mcp/agents/register", {
        name,
        type,
        config: parsedConfig
      });
      setMessage(res.data.message);
    } catch (err) {
      setMessage("Error: " + err.message);
    }
  };

  return (
    <div className="mt-10 border-t pt-6">
      <h2 className="text-xl font-bold mb-2">➕ Register New Agent</h2>
      <form onSubmit={registerAgent} className="space-y-2">
        <input className="w-full border p-2" placeholder="Agent Name (e.g. github1)" value={name} onChange={e => setName(e.target.value)} />
        <select className="w-full border p-2" value={type} onChange={e => setType(e.target.value)}>
          <option value="github">GitHubAgent</option>
          <option value="jira">JiraAgent</option>
        </select>
        <textarea className="w-full border p-2" rows="4" placeholder='Optional Config (JSON)' value={config} onChange={e => setConfig(e.target.value)} />
        <button className="bg-green-600 text-white p-2 w-full rounded">Register Agent</button>
      </form>
      {message && <p className="mt-2 text-sm text-blue-600">{message}</p>}
    </div>
  );
}
