import numpy as np
from app.models import Ingredient, NutritionTotals, ParsedIngredient
from app.nutrition import load_nutrition_data

UNIT_TO_GRAMS: dict[str, float] = {
    "g": 1.0,
    "ml": 1.0,
    "dl": 100.0,
    "tsk": 5.0,
    "spsk": 15.0,
    "stk": 50.0, #antager typisk æg-størrelse
}

#Konverterer "amount" + "unit" til gram. Returnerer None hvis ikke muligt
def to_grams(amount: float | None, unit: str | None) -> float | None:
    
    if amount is None or unit is None:
        return None
    
    multiplier = UNIT_TO_GRAMS.get(unit.lower())
    if multiplier is None:
        return None
    
    return amount*multiplier

# Tager en ingrediens fra Mistral og tilføjer rigtige ernæringsværdier
# ved at slå op i USDA-databasen
def optimize_ingredient(parsed: ParsedIngredient) -> Ingredient:
    # Default-værdier hvis det ikke kan beregnes
    calories = 0.0
    protein_g = 0.0
    carbs_g = 0.0
    fat_g = 0.0
    
    #Beregner hvis Mistral finder match
    if parsed.name_usda is not None:
        df = load_nutrition_data()
        #Tjekker i DB efter navn der matcher det valgte
        match = df[df["name"] == parsed.name_usda]
        

        
        if not match.empty:
            grams = to_grams(parsed.amount, parsed.unit)
            
            if grams is not None:
                #USDA-værdier er pr 100g, der bliver skaleret
                scale = grams / 100
                #for at finde første row (indexing)
                row = match.iloc[0]
                calories = float(row["calories"]) * scale
                protein_g = float(row["protein_g"]) * scale
                carbs_g = float(row["carbs_g"]) * scale
                fat_g = float(row["fat_g"]) * scale
    
    return Ingredient(
        name=parsed.name,
        amount=parsed.amount,
        unit=parsed.unit,
        calories=calories,
        protein_g=protein_g,
        carbs_g=carbs_g,
        fat_g=fat_g,
    )

#Beregner totaler med sum
def calculate_totals(ingredients: list[Ingredient]) -> NutritionTotals:
    if not ingredients:
        return NutritionTotals(calories=0.0, protein_g=0.0, carbs_g=0.0, fat_g=0.0)
    
    calories = np.array([ing.calories for ing in ingredients]).sum()
    protein_g = np.array([ing.protein_g for ing in ingredients]).sum()
    carbs_g = np.array([ing.carbs_g for ing in ingredients]).sum()
    fat_g = np.array([ing.fat_g for ing in ingredients]).sum()
    
    return NutritionTotals(
        calories=float(calories),
        protein_g=float(protein_g),
        carbs_g=float(carbs_g),
        fat_g=float(fat_g),
    )