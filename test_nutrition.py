"""Manuelt verifikationsscript for nutrition.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.nutrition import find_matching_ingredient

queries = ["egg", "wheat flour", "milk", "tomato", "butter", "salt", "asfaltkage"]

for q in queries:
    match = find_matching_ingredient(q)
    if match:
        name, score = match
        print(f"{q!r:20} → {name!r} (score: {score:.1f})")
    else:
        print(f"{q!r:20} → INGEN MATCH")