agents_registry = {}
tools_registry = {}

import datetime

logs = []

from fastapi import APIRouter, Request
# from agents.github_agent import handle_github
from backend.agents.github_agent import handle_github
from fastapi import HTTPException
from backend.agents.jira_agent import handle_jira


router = APIRouter()

@router.post("/tools/register")
def register_tool(tool: dict):
    name = tool.get("name")
    config = tool.get("config", {})

    if not name:
        raise HTTPException(status_code=400, detail="Tool 'name' is required")

    tools_registry[name] = {
        "config": config
    }
    return {"message": f"Tool '{name}' registered successfully."}

@router.get("/tools")
def list_tools():
    return {"tools": tools_registry}

@router.post("/agents/register")
def register_agent(agent: dict):
    name = agent.get("name")
    type_ = agent.get("type")
    config = agent.get("config", {})

    if not name or not type_:
        raise HTTPException(status_code=400, detail="Agent 'name' and 'type' are required")

    agents_registry[name] = {
        "type": type_,
        "config": config
    }
    return {"message": f"Agent '{name}' registered successfully."}

AGENT_HANDLERS = {
    "github": handle_github,
    "jira": handle_jira,
}

@router.post("/query")
async def handle_query(req: Request):
    data = await req.json()
    text = data.get("text")
    agent_name = data.get("agent")

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agent": agent_name,
        "input": text,
        "response": None
    }

    # Validate if agent is registered
    if agent_name not in agents_registry:
        log_entry["response"] = ["Agent not registered"]
        logs.append(log_entry)
        return {"error": f"Agent '{agent_name}' is not registered"}

    agent_def = agents_registry[agent_name]
    handler = AGENT_HANDLERS.get(agent_def["type"])

    if not handler:
        log_entry["response"] = ["Unsupported agent type"]
        logs.append(log_entry)
        return {"error": f"Unsupported agent type: {agent_def['type']}"}

    # Build args from config + form data
    if agent_def["type"] == "github":
        repo = data.get("repo") or agent_def["config"].get("default_repo")
        token = data.get("token") or agent_def["config"].get("token")
        limit = data.get("limit", 5)
        response = await handler(text, repo, token, limit)
    else:
        # For jira or any other agents
        response = await handler(text, config=agent_def.get("config"))

    log_entry["response"] = response
    logs.append(log_entry)
    return {"response": response}


@router.get("/agents")
def list_agents():
    return {"agents": agents_registry}

@router.get("/logs")
def get_logs():
    return {"logs": logs[-20:]}  # return latest 20 logs
