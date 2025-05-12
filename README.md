# 🚀 AgentDock — GenAI Hackathon Submission

**AgentDock** is a multi-agent MCP (Model Context Protocol) server with a clean web UI that allows users to:
- Register and manage intelligent agents
- Interact with tools like GitHub via natural language
- Monitor agent activity through logs
- Dynamically register external tools (e.g., Jira, Slack, Shopify)

Designed to be modular, extensible, and fully dockerized.

---

## 📦 Tech Stack
- **Backend:** Python 3.10, FastAPI, httpx
- **Frontend:** React.js, Tailwind CSS
- **Containerization:** Docker, Docker Compose
- **Free APIs used:** GitHub REST API (via PAT)

---

## 🚀 Features Implemented

### ✅ Backend
- MCP-compliant API server (modular FastAPI)
- GitHubAgent: Fetch & summarize recent PRs
- Agent Registration API (`/mcp/agents/register`)
- Tool Registration API Stub (`/mcp/tools/register`)
- Logs API (`/mcp/logs`) with timestamp, input, agent, and response

### ✅ Frontend
- Natural Language Query Interface
- Agent selection & GitHub PR summary trigger
- Agent Registration Form (name, type, config)
- View Logs Panel with history of interactions

---

## 🖥️ Live Features (Screenshots Available)
- GitHubAgent: Summarize latest pull requests from any repo
- Agent logs: View past inputs and results with timestamps
- Dynamic agent registration with JSON config

---

## 🛠️ How to Run the Project

1. Clone the Repository

git clone https://github.com/your-username/agentdock.git
cd agentdock

2. Start Backend (FastAPI in Docker)

docker-compose up --build

API available at: http://localhost:8000

3. Start Frontend (React App)

cd frontend
npm install
npm start

Web UI: http://localhost:3000

🧪 Sample Query Payload

{
  "agent": "github",
  "text": "summarize latest PRs",
  "repo": "octocat/Hello-World",
  "token": "<your_github_pat>",
  "limit": 5
}

📁 Folder Structure

agentdock/
├── backend/
│   ├── main.py
│   ├── mcp/router.py
│   ├── agents/github_agent.py
│   └── services/
├── frontend/
│   ├── src/components/QueryForm.jsx
│   ├── src/components/AgentRegistry.jsx
├── Dockerfile
├── docker-compose.yml
└── README.md
