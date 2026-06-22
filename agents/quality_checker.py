import os
import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("ANTHROPIC_API_KEY")

def check(resume: dict, job_analysis: dict) -> tuple[int, str]:
    client = anthropic.Anthropic(api_key=api)
    result = client.messages.create(
        max_tokens= 512,
        model="claude-haiku-4-5",
        system="you are professional technical resume reviewer and compare the job description and resume and return the output as json with two parameters score (1 to 10) and feedback string",
        messages=[{'role':'user','content':f'Resume Analyis {json.dumps(resume)}\n\n  and job {json.dumps(job_analysis)}\n\n '}]
    )
    parsed = json.loads(result.content[0].text) # type: ignore
    return (parsed["score"], parsed["feedback"]) 
