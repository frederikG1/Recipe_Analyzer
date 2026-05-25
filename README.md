# Heading 1 En applikation der analyserer og beregner kalorier samt makro-indhold for ingredienser ved hjælp af en LLM og fødevareoplsyninger tilgået via USDA FoodData Central

1. Opstart
  Opret .env og kopier indhold fra .env.example
  MISTRAL_API_KEY hentes fra https://console.mistral.ai/home?profile_dialog=api-keys efter oprettelse af bruger

2. Kør program via docker
  docker compose up
  
  Og frontenden kan herefter åbnes på http://localhost:8501


3. Kør program lokalt
  python -m venv .venv
  source .venv/Scripts/activate     # Windows: .venv\Scripts\activate
  pip install -r backend/requirements-dev.txt
  pip install -r frontend/requirements.txt

herefter startes backend og frontend i hver sin terminal
  #T1
  cd backend
  uvicorn app.main:app --reload

  #T2
  streamlit run frontend/app.py

4. Test og kodekvalitet
   pytest
   mypy backend/app
   ruff check backend/


