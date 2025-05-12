import httpx

GITHUB_API = "https://api.github.com"

async def handle_github(text, repo: str, token: str, limit: int = 5):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API}/repos/{repo}/pulls"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params={"state": "open", "per_page": limit})
            response.raise_for_status()
            prs = response.json()

        summaries = []
        for pr in prs:
            summaries.append(
                f"PR #{pr['number']} by {pr['user']['login']} — \"{pr['title']}\" (Status: {pr['state']})"
            )

        return summaries if summaries else ["No open pull requests found."]

    except httpx.HTTPStatusError as e:
        return [f"GitHub API Error: {e.response.status_code} - {e.response.text}"]
    except Exception as e:
        return [f"Unexpected error: {str(e)}"]
