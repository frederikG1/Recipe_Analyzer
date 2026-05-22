# Matcher ingrediensnavne mod USDA-dataen

from functools import lru_cache
from pathlib import Path

import pandas as pd
from rapidfuzz import process, fuzz

from app.models import Ingredient, ParsedIngredient

#Path til nutrition.csv (3x parent fordi vi skal ud af app/nutrition.py)
NUTRITION_CSV_PATH = Path(__file__).parents[2] / "data" / "nutrition.csv"


#kører funktionen og gemmer resultatet 1 resultat i cache. Sparer tid
@lru_cache(maxsize=1)
def load_nutrition_data() -> pd.DataFrame:
    return pd.read_csv(NUTRITION_CSV_PATH)


def get_all_food_names() -> list[str]:
    df = load_nutrition_data()
    return df["name"].tolist()