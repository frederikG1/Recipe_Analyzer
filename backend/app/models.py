from pydantic import BaseModel

class RecipeRequest(BaseModel):
    recipe_text: str

class Ingredient(BaseModel):
    name: str
    amount: float | None = None
    unit: str | None = None
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float

class NutritionTotals(BaseModel):
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float

class AnalysisResponse(BaseModel):
    ingredients: list[Ingredient]
    totals: NutritionTotals

