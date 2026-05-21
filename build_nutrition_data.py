import pandas as pd

NUTRIENT_IDS = {
    "calories": 1008,
    "protein_g": 1003,
    "carbs_g": 1005,
    "fat_g": 1004,
}

food = pd.read_csv("data/usda/food.csv")
food_nutrient = pd.read_csv("data/usda/food_nutrient.csv", low_memory=False)
print(f"Læste {len(food)} fødevarer og {len(food_nutrient)} næringsstof-rækker")

nutrient = pd.read_csv("data/usda/nutrient.csv")

foundation = food[food["data_type"] == "foundation_food"]
print(f"Filtreret til {len(foundation)} foundation_food rækker")

foundation_ids = foundation["fdc_id"]

relevant_nutrients = food_nutrient[
    food_nutrient["nutrient_id"].isin(NUTRIENT_IDS.values()) & food_nutrient["fdc_id"].isin(foundation_ids)
]
print(f"Filtreret til {len(relevant_nutrients)} relevante næringsstof-rækker")

pivoted = relevant_nutrients.pivot(index="fdc_id", columns="nutrient_id", values="amount")
print(f"Efter pivot: {pivoted.shape[0]} fødevarer med {pivoted.shape[1]} næringsstof-kolonner")
    

# original = {"calories": 1008, "protein_g": 1003, "carbs_g": 1005, "fat_g": 1004}
id_to_name = {v: k for k, v in NUTRIENT_IDS.items()}
pivoted = pivoted.rename(columns=id_to_name)
print(pivoted.head())

merged = foundation.merge(pivoted, left_on="fdc_id", right_index=True)
print(f"Efter merge: {len(merged)} rækker")

result = merged[["description", "calories", "protein_g", "carbs_g", "fat_g"]].copy()
result = result.rename(columns={"description": "name"})


result["calories"] = result["calories"].fillna(
    result["protein_g"] * 4 + result["carbs_g"] * 4 + result["fat_g"] * 9
)
print(f"Efter Atwater-beregning: {result['calories'].isna().sum()} mangler stadig kalorier")

result = result.dropna(subset=["calories", "protein_g", "carbs_g", "fat_g"])
print(f"Efter dropna: {len(result)} rækker tilbage")

result.to_csv("data/nutrition.csv", index=False)
print(f"\n {len(result)} sendt til nutrition.csv")
print(f"\nFørste 5 rækker:")
print(result.head())



