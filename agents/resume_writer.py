import os
from dotenv import load_dotenv
import json
import anthropic
from utils.cleaner import BANNED_WORDS

load_dotenv()

api = os.getenv("ANTHROPIC_API_KEY")



_MODEL = "claude-sonnet-5"
_INPUT_PRICE = 2.00   # $ per 1M tokens
_OUTPUT_PRICE = 10.00  # $ per 1M tokens

def write(job_analysis: dict, resume: dict, feedback: str = None) -> tuple[dict, dict]: # type: ignore
    client = anthropic.Anthropic(api_key=api)
    message = client.messages.create(
        max_tokens= 8192,
        model= _MODEL,
        system=f"""You are a professional resume writer. Customize the base resume to match the job analysis.
                Rules:
                    - Return JSON only. No markdown, no code fences, no extra text.
                    - Keep the exact same JSON keys as the base resume.
                    - Never use these words: {', '.join(BANNED_WORDS)}
                    - No em dashes. Use plain hyphens if needed.
                    - Write bullet points as plain sentences.
                    - If target_output_pages is 5, write detailed full bullets for every role.""",

        messages=[{
                    "role": "user",
                    "content": f"Job Analysis: {json.dumps(job_analysis)}\n\nBase Resume: {json.dumps(resume)}\n\nFeedback: {feedback}"
                }]


    )
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

    
