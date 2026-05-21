from fastapi import FastAPI

from app.llm_client import extract_ingredients
from app.models import AnalysisResponse, Ingredient, NutritionTotals, RecipeRequest

app = FastAPI()


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: RecipeRequest) -> AnalysisResponse:
    parsed_ingredients = await extract_ingredients(request.recipe_text)

    ingredients = [
        Ingredient(
            name=p.name,
            amount=p.amount,
            unit=p.unit,
            calories=0.0,
            protein_g=0.0,
            carbs_g=0.0,
            fat_g=0.0,
        )
        for p in parsed_ingredients
    ]

    totals = NutritionTotals(
        calories=0.0,
        protein_g=0.0,
        carbs_g=0.0,
        fat_g=0.0,
    )

    return AnalysisResponse(ingredients=ingredients, totals=totals)