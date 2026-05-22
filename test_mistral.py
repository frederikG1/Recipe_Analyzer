"""Manuelt verifikationsscript - kører IKKE som en del af pytest."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.llm_client import extract_ingredients


async def main() -> None:
    recipes = [
        "2 æg, 100 g mel, 200 ml mælk",
        "1 spsk smør, en knivspids salt, lidt peber",
        "Pasta carbonara: 200g spaghetti, 100g pancetta, 2 æggeblommer, 50g parmesan, sort peber",
    ]

    for recipe in recipes:
        print(f"\n--- Opskrift: {recipe} ---")
        ingredients = await extract_ingredients(recipe)
        for ing in ingredients:
            print(f"  {ing.name} ({ing.name_en}) -> USDA: {ing.name_usda}, amount={ing.amount}, unit={ing.unit}")


if __name__ == "__main__":
    asyncio.run(main())