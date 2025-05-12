import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

async def extract_github_params(text):
    prompt = f"""
You are an intelligent assistant helping extract parameters from natural language GitHub queries. 
From the following text, return a JSON object with: repo, limit, state, branch. If not present, set them to null or default.

Input: "{text}"
Respond only with a valid JSON.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return eval(response['choices'][0]['message']['content'])


async def extract_jira_params(text):
    prompt = f"""
You are an assistant that extracts structured query parameters from natural language Jira prompts.

From this input: "{text}"

Return a JSON with:
- jql_filters: string (only the WHERE clause after `project = XYZ AND ...`)
- limit: integer (number of issues to return)

Example output:
{{
  "jql_filters": "status = Done AND assignee = John AND priority = High",
  "limit": 3
}}

Respond only with valid JSON.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return eval(response['choices'][0]['message']['content'])
