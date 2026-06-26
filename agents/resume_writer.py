import os
from dotenv import load_dotenv
import json
import anthropic
from utils.cleaner import BANNED_WORDS

load_dotenv()

api = os.getenv("ANTHROPIC_API_KEY")



def write(job_analysis: dict, resume: dict,feedback: str = None) ->dict: # type: ignore
    client = anthropic.Anthropic(api_key=api)
    message = client.messages.create(
        max_tokens= 8192,
        model= "claude-sonnet-4-6",
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
    return json.loads(text.strip())

    
