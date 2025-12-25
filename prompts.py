# prompts.py

CHUNK_PROMPT = """
You are a market analyst.

Summarize the following text in 3 bullet points:
- Overall market sentiment
- Key sectors
- Important signals

Text:
{text}
"""

FINAL_PROMPT = """
You are a senior market strategist.

Based on the summaries below:
1. Identify overall market trend (Bullish / Bearish / Neutral)
2. List top 3 drivers
3. Give a short summary (max 120 words)
4. Mention risks

Return JSON strictly:

{{
  "trend": "",
  "drivers": [],
  "summary": "",
  "risks": []
}}

Summaries:
{summaries}
"""
