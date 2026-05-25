from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_analyze_returns_200_for_valid_input() -> None:
    response = client.post("/analyze", json={"recipe_text": "2 æg, 100 g mel"})
    assert response.status_code == 200


def test_analyze_response_has_correct_structure() -> None:
    response = client.post("/analyze", json={"recipe_text": "2 æg"})
    data = response.json()
    
    # Top-level felter
    assert "ingredients" in data
    assert "totals" in data
    
    # ingredients skal være en liste
    assert isinstance(data["ingredients"], list)
    assert len(data["ingredients"]) > 0
    
    # Hver ingrediens skal have de rigtige felter
    first_ingredient = data["ingredients"][0]
    assert "name" in first_ingredient
    assert "calories" in first_ingredient
    assert "protein_g" in first_ingredient
    
    # totals skal have makro-felterne
    assert "calories" in data["totals"]
    assert "protein_g" in data["totals"]


def test_analyze_rejects_missing_recipe_text() -> None:
    response = client.post("/analyze", json={})
    assert response.status_code == 422  