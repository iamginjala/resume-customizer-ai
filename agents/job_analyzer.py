import anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

api = os.getenv("ANTHROPIC_API_KEY")

def analyze(job_description: str):
    client = anthropic.Anthropic(api_key=api)
    message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    system="You are a job description analyzer. Extract key information and return JSON only. No extra text, no markdown, no code fences. Always return exactly these keys: job_title, required_skills, nice_to_have_skills, key_responsibilities, keywords, experience_years",
    messages=[{"role": "user", "content": job_description}])
    return json.loads(message.content[0].text) # type: ignore