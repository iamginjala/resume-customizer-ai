import os
import anthropic
import json
import re
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("ANTHROPIC_API_KEY")

def check(resume: dict, job_analysis: dict) -> tuple[int, str]:
    client = anthropic.Anthropic(api_key=api)
    result = client.messages.create(
        max_tokens=1024,
        model="claude-haiku-4-5",
        system="You are a professional technical resume reviewer. Compare the job description and resume, then return JSON only with exactly two keys: score (integer 1-10) and feedback (string). No markdown, no code fences, no extra text.",
        messages=[{'role':'user','content':f'Resume: {json.dumps(resume)}\n\nJob Analysis: {json.dumps(job_analysis)}'}]
    )
    text = result.content[0].text.strip() # type: ignore
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
        else:
            raise
    return (parsed["score"], parsed["feedback"])
