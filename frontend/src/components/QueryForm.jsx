import React, { useState, useEffect } from "react";
import axios from "axios";

export default function QueryForm() {
  const [agent, setAgent] = useState("github");
  const [text, setText] = useState("Summarize latest PRs");
  const [repo, setRepo] = useState("magento/magento2");
  const [token, setToken] = useState("");
  const [response, setResponse] = useState(null);
  const [logs, setLogs] = useState([]);
  const [showLogs, setShowLogs] = useState(false);
  const [availableAgents, setAvailableAgents] = useState([]);
  const [agentConfig, setAgentConfig] = useState({});

  useEffect(() => {
    axios.get("http://localhost:8000/mcp/agents")
      .then(res => {
        setAvailableAgents(Object.keys(res.data.agents || {}));
      })
      .catch(err => {
        console.error("Failed to fetch agents", err);
      });
  }, []);


  const loadLogs = async () => {
    try {
      const res = await axios.get("http://localhost:8000/mcp/logs");
      setLogs(res.data.logs);
      setShowLogs(true);
    } catch (err) {
      console.error("Failed to load logs", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/mcp/query", {
        agent,
        text,
        repo: agentConfig.default_repo || repo,
        token: agentConfig.token || token,
        limit: 5
      });

      setResponse(res.data.response);
    } catch (err) {
      setResponse(["Error: " + err.message]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold">🧠 AgentDock UI</h1>
      <form onSubmit={handleSubmit} className="space-y-2">
        
        <select
          value={agent}
          onChange={e => setAgent(e.target.value)}
          className="w-full border p-2"
        >
          {availableAgents.map((a) => (
            <option key={a} value={a}>{a}</option>
          ))}
        </select>



        {agent === "github" && !agentConfig.default_repo && (
          <input
            className="w-full border p-2"
            placeholder="GitHub Repo (e.g. octocat/Hello-World)"
            value={repo}
            onChange={e => setRepo(e.target.value)}
          />
        )}

        {agent === "github" && !agentConfig.token && (
        <input
          className="w-full border p-2"
          placeholder="GitHub Token"
          type="password"
          value={token}
          onChange={e => setToken(e.target.value)}
        />
      )}

        <input className="w-full border p-2" placeholder="Ask something..." value={text} onChange={e => setText(e.target.value)} />
        <button className="bg-blue-600 text-white p-2 w-full rounded">Ask Agent</button>
      </form>
      <div className="bg-gray-100 p-4 rounded">
        <h2 className="font-semibold mb-2">Response</h2>
        <pre className="whitespace-pre-wrap">{response ? response.join("\n\n") : "No response yet."}</pre>

        <button
          className="bg-gray-700 text-white p-2 w-full rounded"
          onClick={loadLogs}
        >
          View Logs
        </button>

        {showLogs && (
          <div className="bg-gray-50 border p-4 mt-4 rounded max-h-96 overflow-y-scroll">
            <h3 className="font-semibold mb-2">📜 Recent Logs</h3>
            {logs.map((log, index) => (
              <div key={index} className="border-b py-2 text-sm">
                <p><strong>{log.timestamp}</strong></p>
                <p><strong>Agent:</strong> {log.agent}</p>
                <p><strong>Input:</strong> {log.input}</p>
                <p><strong>Response:</strong> {Array.isArray(log.response) ? log.response.join(", ") : log.response}</p>
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  );
}
