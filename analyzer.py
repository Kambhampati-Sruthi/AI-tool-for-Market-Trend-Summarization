import subprocess
import json
import re

MODEL_NAME = "aicrue:latest"

PROMPT = """
You are a market analysis AI.

Analyze the following market or sales data and return ONLY valid JSON
with the following structure:

{{
  "trend": "Positive | Negative | Neutral",
  "drivers": ["driver1", "driver2"],
  "summary": "short summary",
  "risks": ["risk1", "risk2"]
}}

Data:
{text}
"""

def extract_json(text):
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group() if match else None

def call_ollama(prompt):
    try:
        process = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        raw_output = process.stdout.strip()
        json_text = extract_json(raw_output)

        if not json_text:
            return json.dumps({
                "trend": "Unknown",
                "drivers": [],
                "summary": "No valid JSON detected.",
                "risks": []
            })

        parsed = json.loads(json_text)
        return json.dumps(parsed)

    except Exception as e:
        return json.dumps({
            "trend": "Error",
            "drivers": [],
            "summary": str(e),
            "risks": []
        })

def analyze_market(text):
    final_prompt = PROMPT.format(text=text)
    return call_ollama(final_prompt)
