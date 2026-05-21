import pandas as pd


NUTRIENT_IDS = {
    "calories": 1008,
    "protein_g": 1003,
    "carbs_g": 1005,
    "fat_g": 1004,
}

# Læs USDA's csv data
food = pd.read_csv("data/usda/food.csv")
food_nutrient = pd.read_csv("data/usda/food_nutrient.csv", low_memory=False)
nutrient = pd.read_csv("data/usda/nutrient.csv")
print(f"Læste {len(food)} fødevarer og {len(food_nutrient)} næringsstof-rækker")

# Behold kun rigtige fødevarer (drop sample_food, market_acquisition osv.)
foundation = food[food["data_type"] == "foundation_food"]
print(f"Filtreret til {len(foundation)} foundation_food rækker")

# Hent fdc_id'er for foundation_food - bruges til at filtrere næringsstof-tabellen
foundation_ids = foundation["fdc_id"]

# Behold kun de 4 makro-næringsstoffer OG kun rækker der hører til foundation_food
relevant_nutrients = food_nutrient[
    food_nutrient["nutrient_id"].isin(NUTRIENT_IDS.values())
    & food_nutrient["fdc_id"].isin(foundation_ids)
]
print(f"Filtreret til {len(relevant_nutrients)} relevante næringsstof-rækker")

# Pivot fra "lang" til "bred": én række per fødevare, kolonner = næringsstoffer
pivoted = relevant_nutrients.pivot(index="fdc_id", columns="nutrient_id", values="amount")
print(f"Efter pivot: {pivoted.shape[0]} fødevarer med {pivoted.shape[1]} næringsstof-kolonner")

# Omdøb kolonner fra numeriske ID'er (1008, 1003, ...) til vores feltnavne (calories, protein_g, ...)
id_to_name = {v: k for k, v in NUTRIENT_IDS.items()}
pivoted = pivoted.rename(columns=id_to_name)
print(pivoted.head())

# Join med foundation for at få fødevarenavnene ("description"-kolonnen)
merged = foundation.merge(pivoted, left_on="fdc_id", right_index=True)
print(f"Efter merge: {len(merged)} rækker")

# Vælg kun de kolonner vi vil have, og omdøb "description" til "name"
result = merged[["description", "calories", "protein_g", "carbs_g", "fat_g"]].copy()
result = result.rename(columns={"description": "name"})

# Beregn manglende kalorier via Atwater-formlen (4 kcal/g protein, 4 kcal/g carbs, 9 kcal/g fat)
result["calories"] = result["calories"].fillna(
    result["protein_g"] * 4 + result["carbs_g"] * 4 + result["fat_g"] * 9
)
print(f"Efter Atwater-beregning: {result['calories'].isna().sum()} mangler stadig kalorier")

# Fjern rækker hvor en eller flere makro-værdier mangler
result = result.dropna(subset=["calories", "protein_g", "carbs_g", "fat_g"])
print(f"Efter dropna: {len(result)} rækker tilbage")

# Gem som ren CSV (uden index-kolonne)
result.to_csv("data/nutrition.csv", index=False)
print(f"\n {len(result)} sendt til nutrition.csv")
print(f"\nFørste 5 rækker:")
print(result.head())