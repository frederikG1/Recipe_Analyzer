import pandas as pd
from app.nutrition import get_all_food_names, load_nutrition_data


def test_load_nutrition_data_returns_valid_df() -> None:
    df = load_nutrition_data()
    
    #skal være et DataFrame
    assert isinstance(df, pd.DataFrame)
    
    #Må ikke være tomt
    assert len(df) > 0
    
    expected_columns = {"name", "calories", "protein_g", "carbs_g", "fat_g"}
    assert expected_columns.issubset(set(df.columns))
    
def test_get_all_food_names_returns_non_empty_list_of_strings() -> None:
    names = get_all_food_names()
    
    assert isinstance(names, list)
    assert len(names) > 0
    
    # Alle instancer skal være strings
    assert all(isinstance(name, str) for name in names)