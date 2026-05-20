from fastapi import FastAPI

from app.models import AnalysisResponse, Ingredient, NutritionTotals, RecipeRequest

app = FastAPI()


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: RecipeRequest) -> AnalysisResponse:
    # Dummy-data - vi ignorerer request.recipe_text for nu
    dummy_ingredient = Ingredient(
        name="æg",
        amount=2,
        unit="stk",
        calories=140,
        protein_g=12,
        carbs_g=1,
        fat_g=10,
    )

    dummy_totals = NutritionTotals(
        calories=140,
        protein_g=12,
        carbs_g=1,
        fat_g=10,
    )

    return AnalysisResponse(
        ingredients=[dummy_ingredient],
        totals=dummy_totals,
    )