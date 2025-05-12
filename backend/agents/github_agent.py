from backend.services.llm_client import extract_github_params

async def handle_github(text, default_repo=None, default_token=None, limit=5):
    parsed = await extract_github_params(text)
    print("🧠 LLM parsed:", parsed)

    repo = parsed.get("repo") or default_repo
    token = default_token
    state = parsed.get("state", "open")
    limit = parsed.get("limit", limit)

    if not repo or not token:
        return ["Missing repo or token"]

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    params = {
        "state": state,
        "per_page": limit
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.github.com/repos/{repo}/pulls", headers=headers, params=params)
            response.raise_for_status()
            prs = response.json()

        return [
            f"PR #{pr['number']} by {pr['user']['login']} — \"{pr['title']}\" (Status: {pr['state']})"
            for pr in prs
        ] or ["No matching pull requests."]
    
    except httpx.HTTPStatusError as e:
        return [f"GitHub API Error: {e.response.status_code} - {e.response.text}"]
    except Exception as ex:
        return [f"Unexpected error: {str(ex)}"]
