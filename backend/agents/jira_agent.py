import httpx
from base64 import b64encode
from backend.services.llm_client import extract_jira_params

async def handle_jira(text, config=None):
    base_url = config.get("base_url")
    project = config.get("project")
    email = config.get("email")
    api_token = config.get("api_token")

    if not all([base_url, project, email, api_token]):
        return ["Missing Jira config"]

    # Parse user prompt using LLM
    parsed = await extract_jira_params(text)
    limit = parsed.get("limit", 5)
    status = parsed.get("status")
    assignee = parsed.get("assignee")
    priority = parsed.get("priority")
    keywords = parsed.get("keywords")

    # Build dynamic JQL query
    jql_parts = [f'project = "{project}"']
    if status:
        jql_parts.append(f'status = "{status}"')
    if assignee:
        jql_parts.append(f'assignee = "{assignee}"')
    if priority:
        jql_parts.append(f'priority = "{priority}"')
    if keywords:
        jql_parts.append(f'text ~ "{keywords}"')

    jql = " AND ".join(jql_parts) + " ORDER BY created DESC"

    url = f"{base_url}/rest/api/3/search?jql={jql}&maxResults={limit}"

    auth_header = b64encode(f"{email}:{api_token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            issues = response.json().get("issues", [])

        return [
            f"{issue['key']}: {issue['fields']['summary']}"
            for issue in issues
        ] or ["No matching issues found."]
    
    except httpx.HTTPStatusError as e:
        return [f"Jira API Error: {e.response.status_code} - {e.response.text}"]
    except Exception as ex:
        return [f"Unexpected error: {str(ex)}"]
