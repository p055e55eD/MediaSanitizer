"""
NewsAnalyzer for MediaSanitizer.
Uses OpenAI API (GPT-3.5/4) to assess credibility, red flags, and key entities in Armenian or English news.
Loads API key securely from .env file.
"""

import os
from dotenv import load_dotenv
import openai
import json

# ---- Load API Key from .env ----
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("[Analyzer] ERROR: OPENAI_API_KEY not found! Set it in .env.")
    raise RuntimeError("OPENAI_API_KEY not set in .env")

# ---- OpenAI Client ----
openai.api_key = openai_api_key

class NewsAnalyzer:
    def __init__(self):
        pass

    def analyze(self, article):
        title = article.get("title", "").strip()
        content = article.get("content", "").strip()
        domain = article.get("domain", "unknown")

        if not content or len(content) < 60:
            print("[Analyzer] Content too short to analyze.")
            return None
        if not title:
            title = "No Title"

        prompt = self._build_prompt(title, content, domain)
        print("[Analyzer] Sending prompt to OpenAI (truncated):\n", prompt[:350], "\n---END PROMPT---")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt}
                ],
                max_tokens=900,
                temperature=0.1,
            )
            reply = response.choices[0].message.content.strip()
            print("[Analyzer] GPT raw reply (truncated):", reply[:200])

            # Try to parse as JSON
            try:
                parsed = json.loads(reply)
                # Defensive: Fallbacks if not present
                return {
                    "credibility_score": parsed.get("credibility_score"),
                    "red_flags": parsed.get("red_flags", []),
                    "entities": parsed.get("entities", []),
                    "summary": parsed.get("summary", ""),
                    "language": parsed.get("language", "hy")
                }
            except Exception as e:
                print("[Analyzer] Could not parse JSON, fallback to raw.")
                return {
                    "credibility_score": None,
                    "red_flags": [],
                    "entities": [],
                    "summary": reply,
                    "language": "hy"
                }

        except Exception as e:
            print("[Analyzer] OpenAI API exception:", e)
            return None

    def _build_prompt(self, title, content, domain):
        # Output will be JSON
        return (
            "You are an expert analyst of Armenian and English news articles. Write report only in English\n"
            "Analyze the following article and output valid JSON with these fields:\n"
            "  - give credibility_score integer between 0 and 100 based on some formula\n"
            "  - red_flags: list of strings describing potential bias or unverified claims\n"
            "  - entities: list of [name, type] pairs for key people/places/organizations\n"
            "  - summary: 3-5 sentence objective summary of credibility\n"
            "  - language: 'hy' or 'en'\n"
            "Respond in valid JSON only, no explanations or extra text.\n"
            f"Article title: {title}\n"
            f"Source: {domain}\n"
            f"Article content:\n{content}\n"
        )
