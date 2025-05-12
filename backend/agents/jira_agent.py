import httpx
from base64 import b64encode

async def handle_jira(text, config=None):
    base_url = config.get("base_url")
    project = config.get("project")
    email = config.get("email")
    api_token = config.get("api_token")

    if not all([base_url, project, email, api_token]):
        return ["Missing required Jira config values"]

    # Basic Auth
    auth_header = b64encode(f"{email}:{api_token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Accept": "application/json"
    }

    jql = f"project = {project} ORDER BY created DESC"
    url = f"{base_url}/rest/api/3/search?jql={jql}&maxResults=5"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            issues = response.json().get("issues", [])

        return [
            f"{issue['key']}: {issue['fields']['summary']}"
            for issue in issues
        ] or ["No issues found in project."]
        
    except httpx.HTTPStatusError as e:
        return [f"Jira API Error: {e.response.status_code} - {e.response.text}"]
    except Exception as ex:
        return [f"Unexpected error: {str(ex)}"]
