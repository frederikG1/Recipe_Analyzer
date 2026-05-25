FROM python:3.12-slim

# Arbejdsmappen inde i containeren
WORKDIR /app

# Kopiér requirements først og installer dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiér koden
COPY backend/app/ ./app/
COPY data/ ./data/

ENV NUTRITION_CSV_PATH=/app/data/nutrition.csv

# Expose FastApi porten
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]