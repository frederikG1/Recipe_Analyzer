from fastapi import FastAPI

from app.analysis import calculate_totals, optimize_ingredient
from app.llm_client import extract_ingredients
from app.models import AnalysisResponse, Ingredient, NutritionTotals, RecipeRequest

app = FastAPI()


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: RecipeRequest) -> AnalysisResponse:
    parsed_ingredients = await extract_ingredients(request.recipe_text)

    #"Optimizer" hver ingrediens med de rigtige makroer fra DB
    ingredients = [optimize_ingredient(p) for p in parsed_ingredients]
    
    totals = calculate_totals(ingredients)

    return AnalysisResponse(ingredients=ingredients, totals=totals)