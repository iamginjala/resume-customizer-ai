import anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

api = os.getenv("ANTHROPIC_API_KEY")

_MODEL = "claude-haiku-4-5"
_INPUT_PRICE = 1.00   # $ per 1M tokens
_OUTPUT_PRICE = 5.00  # $ per 1M tokens

def analyze(job_description: str) -> tuple[dict, dict]:
    client = anthropic.Anthropic(api_key=api)
    message = client.messages.create(
    model=_MODEL,
    max_tokens=1024,
    system="You are a job description analyzer. Extract key information and return JSON only. No extra text, no markdown, no code fences. Always return exactly these keys: job_title, required_skills, nice_to_have_skills, key_responsibilities, keywords, experience_years",
    messages=[{"role": "user", "content": job_description}])
    text = message.content[0].text.strip() # type: ignore
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    cost = (input_tokens / 1_000_000) * _INPUT_PRICE + (output_tokens / 1_000_000) * _OUTPUT_PRICE
    usage = {"model": _MODEL, "input_tokens": input_tokens, "output_tokens": output_tokens, "cost": cost}
    return json.loads(text.strip()), usage