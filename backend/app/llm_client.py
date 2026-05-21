import json
import os
from typing import Any

import httpx
from dotenv import load_dotenv

from app.models import ParsedIngredient

load_dotenv()

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

SYSTEM_PROMPT = """Du er en ekspert i at parse opskrifter til struktureret data.

Når brugeren sender en opskrift, returnér et JSON-objekt med følgende struktur:

{
  "ingredients": [
    {"name": "ingrediens-navn", "amount": tal, "unit": "enhed"}
  ]
}

Regler:
- name: ingrediensens navn på dansk, i ental, i grundform (fx "tomat" ikke "tomater")
- amount: et tal. Hvis der står "en teskefuld", skriv 1. Hvis der står "en knivspids", skriv 0.25.
- unit: SI-enhed eller almindelig enhed. Brug "g", "ml", "stk", "tsk", "spsk", "dl".
- Hvis en mængde ikke kan udledes, sæt amount til null.
- Hvis en enhed ikke er angivet eller ikke giver mening, sæt unit til null.

Returnér KUN JSON. Ingen forklaring, ingen markdown, ingen kommentarer."""


async def extract_ingredients(recipe_text: str) -> list[ParsedIngredient]:
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY er ikke sat i environment")

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload: dict[str, Any] = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": recipe_text},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(MISTRAL_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    return [ParsedIngredient(**item) for item in parsed["ingredients"]]