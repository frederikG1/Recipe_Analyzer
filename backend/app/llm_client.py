import json
import os
from typing import Any

import httpx
from dotenv import load_dotenv

from app.models import ParsedIngredient
from app.nutrition import get_all_food_names

load_dotenv()

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")


def system_prompt() -> str:
    """Du er en ekspert i at parse opskrifter til struktureret data."""
    food_names = get_all_food_names()
    food_list_str = "\n".join(f"- {name}" for name in food_names)
    
    return f"""Du er en ekspert i at parse opskrifter til struktureret data.
    

Når brugeren sender en opskrift, returnér et JSON-objekt med følgende struktur:

{{
  "ingredients": [
    {{
      "name": "dansk-navn",
      "name_en": "english name",
      "name_usda": "USDA navn fra listen eller null",
      "amount": tal,
      "unit": "enhed"
    }}
  ]
}}

Regler:
- name: ingrediensens navn på dansk, i ental, grundform (fx "tomat" ikke "tomater")
- name_en: samme ingrediens på engelsk, i ental, så generisk som muligt
- name_usda: VÆLG det navn fra USDA-listen nedenfor der bedst matcher ingrediensen. Hvis intet i listen er en rimelig match, sæt til null. Tænk ikke kun på string-lighed - tænk på om det er den SAMME fødevare. Fx "butter" matcher "Butter, salted" men IKKE "Peanut butter, smooth style". Fx "salt" har intet rimelig match i listen og bør være null
- amount: tal. "en teskefuld" = 1, "en knivspids" = 0.25.
- unit: SI-enhed eller almindelig enhed: "g", "ml", "stk", "tsk", "spsk", "dl".
- Hvis mængde ikke kan udledes, sæt amount til null.
- Hvis enhed ikke er angivet, sæt unit til null.

USDA-fødevareliste (vælg name_usda fra denne liste):
{food_list_str}

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
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": recipe_text},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(MISTRAL_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    return [ParsedIngredient(**item) for item in parsed["ingredients"]]