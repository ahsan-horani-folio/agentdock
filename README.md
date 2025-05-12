
# 🤖 AgentDock — GenAI Hackathon Submission

AgentDock is a multi-agent orchestration platform that uses LLMs to intelligently route natural language queries to connected tools like GitHub and Jira.

Built for the **Folio3 GenAI Hackathon**, AgentDock enables:
- 🔁 Dynamic registration of intelligent agents
- 💬 Natural language interactions via OpenAI (GPT-3.5)
- 🔍 Prompt-driven querying of real GitHub & Jira APIs
- 📜 Logs for all agent actions
- 📦 Fully dockerized deployment

---

## 📦 Tech Stack

| Layer     | Stack                     |
|-----------|---------------------------|
| Backend   | Python 3.10, FastAPI, OpenAI, httpx |
| Frontend  | React, TailwindCSS        |
| Agents    | GitHubAgent, JiraAgent (fully integrated) |
| AI Model  | OpenAI GPT-3.5-turbo      |
| Container | Docker + Docker Compose   |

---

## 🚀 Features

### ✅ MCP-Compliant Backend (FastAPI)
- Modular agent handler framework
- OpenAI LLM used for extracting structured parameters from prompts
- Real-time GitHub PR summary via `GitHubAgent`
- Real-time Jira issue search via `JiraAgent`

### ✅ React UI
- Register new agents with config (name, type, token, repo, etc.)
- Auto-populated agent dropdown (fetched from backend)
- Dynamic prompt input + config fallback
- Logs panel to view past queries/responses

---

## 💡 Sample Prompts

### GitHubAgent
- `"Summarize last 3 closed PRs"`
- `"Get PRs from develop branch in octocat/Hello-World"`

### JiraAgent
- `"List 5 open bugs assigned to John"`
- `"Closed tasks from last week in AGD project"`

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/agentdock.git
cd agentdock
```

---

### 2. Create `.env` in Project Root

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 3. Start Backend (Docker)

```bash
docker-compose up --build
```

> API available at: `http://localhost:8000`

---

### 4. Start Frontend (React)

```bash
cd frontend
npm install
npm start
```

> UI available at: `http://localhost:3000`

---

## 🔐 Register Agents via UI

### Example: GitHubAgent Config

```json
{
  "default_repo": "octocat/Hello-World",
  "token": "ghp_xxxxxxxxxxxxxxxxxx"
}
```

### Example: JiraAgent Config

```json
{
  "base_url": "https://yourdomain.atlassian.net",
  "project": "AGD",
  "email": "you@example.com",
  "api_token": "xxxxxxxxxxxxxxxx"
}
```

---

## 📁 Folder Structure

```
agentdock/
├── backend/
│   ├── main.py
│   ├── mcp/router.py
│   ├── agents/github_agent.py
│   ├── agents/jira_agent.py
│   └── services/llm_client.py
├── frontend/
│   ├── src/components/QueryForm.jsx
│   ├── src/components/AgentRegistry.jsx
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## ✅ Hackathon Compliance

- ✅ Dockerized solution
- ✅ Natural language interface
- ✅ Multiple tool integrations (GitHub, Jira)
- ✅ AI-first design using OpenAI LLM
- ✅ Original work with free-tier services only

---

## 👤 Author

- **Developer:** Ahsan Horani  
- **Track:** Solo Submission  
- **Event:** Folio3 GenAI Hackathon 2025  
