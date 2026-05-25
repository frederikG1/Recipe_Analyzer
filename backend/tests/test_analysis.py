from app.analysis import calculate_totals, optimize_ingredient, to_grams
from app.models import Ingredient, ParsedIngredient


def test_to_grams_basic_units() -> None:
    # Tester konvertering for typiske enheder
    assert to_grams(100, "g") == 100.0
    assert to_grams(200, "ml") == 200.0
    assert to_grams(1, "dl") == 100.0
    assert to_grams(1, "tsk") == 5.0
    assert to_grams(1, "spsk") == 15.0
    assert to_grams(2, "stk") == 100.0
    
def test_to_grams_returns_none_for_invalid_input() -> None:
    # Tester at None returneres når input mangler.
    assert to_grams(None, "g") is None
    assert to_grams(100, None) is None
    assert to_grams(None, None) is None
    assert to_grams(100, "ukendt_enhed") is None
    
def test_optimize_ingredient_with_food() -> None:
    parsed = ParsedIngredient(
        name="mel",
        name_en="wheat flour",
        name_usda="Flour, wheat, all-purpose, enriched, bleached",
        amount=100,
        unit="g",
    )
    result = optimize_ingredient(parsed)
    
    #Tester at vi faktisk returnerer en Ingredient
    assert isinstance(result, Ingredient)
    
    assert result.name == "mel"
    assert result.amount == 100
    assert result.unit == "g"
    
    assert result.calories > 0
    assert result.protein_g > 0
    assert result.carbs_g > 0
    assert result.fat_g > 0
    

#Tester om alle fire felter er 0 (empty array)
def test_calculate_totals() -> None:
    totals = calculate_totals([])
    
    assert totals.calories == 0
    assert totals.protein_g == 0
    assert totals.carbs_g == 0
    assert totals.fat_g == 0

#Tester om summen af to ingredienser beregnes rigtigt
def test_calculate_totals_sums() -> None:
    ing1 = Ingredient(
        name="a",
        amount=100,
        unit="g",
        calories=100,
        protein_g=10,
        carbs_g=20,
        fat_g=5,
    )
    ing2 = Ingredient(
        name="b",
        amount=50,
        unit="g",
        calories=50,
        protein_g=5,
        carbs_g=10,
        fat_g=2,
    )
    
    totals = calculate_totals([ing1, ing2])
    
    assert totals.calories == 150     # 100 + 50
    assert totals.protein_g == 15     # 10 + 5
    assert totals.carbs_g == 30       # 20 + 10
    assert totals.fat_g == 7          # 5 + 2