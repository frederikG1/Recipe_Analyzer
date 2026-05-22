import os

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Opskrift-analysator", page_icon="🍳")

st.title("🍳 Opskrift-analysator")
st.markdown("Skriv din opskrift, og få beregnet kalorier og makroer")


recipe_text = st.text_area(
    "Indtast opskrift",
    placeholder="Fx: 2 æg, 100 g mel, 200 ml mælk",
    height=150,
)

if st.button("Analysér", type="primary"):
    if not recipe_text.strip():
        st.warning("Skriv en opskrift først.")
    else:
        with st.spinner("Analyserer opskrift..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={"recipe_text": recipe_text},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()
                
                ingredients = data["ingredients"]
                totals = data["totals"]
                
                # Totaler i columns
                st.subheader("Totaler")
                col1, col2, col3, col4 = st.columns(4)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Kalorier", f"{totals['calories']:.0f} kcal")
                col2.metric("Protein", f"{totals['protein_g']:.1f} g")
                col3.metric("Kulhydrater", f"{totals['carbs_g']:.1f} g")
                col4.metric("Fedt", f"{totals['fat_g']:.1f} g")
                #0 decimaler til kcal, 1 decimal til resten
                
                # Ingredienser som tabel
                st.subheader("Ingredienser")
                df = pd.DataFrame(ingredients)
                df = df.rename(columns={
                    "name": "Ingrediens",
                    "amount": "Mængde",
                    "unit": "Enhed",
                    "calories": "Kalorier",
                    "protein_g": "Protein (g)",
                    "carbs_g": "Kulhydrater (g)",
                    "fat_g": "Fedt (g)",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                #Advarsel om ingredienser som ikke kunne findes
                missing = [ing["name"] for ing in ingredients if ing ["calories"] == 0]
                if missing:
                    st.warning(
                        f"Følgende ingredienser kunne ikke findes i databasen: "
                        f"{', '.join(missing)}. De bidrager ikke til totalerne"
                    )
                
                # Pie chart
                st.subheader("Makrofordeling (kalorier)")
                protein_kcal = totals["protein_g"] * 4
                carbs_kcal = totals["carbs_g"] * 4
                fat_kcal = totals["fat_g"] * 9

                if protein_kcal + carbs_kcal + fat_kcal > 0:
                    fig, ax = plt.subplots()
                    ax.pie(
                        [protein_kcal, carbs_kcal, fat_kcal],
                        labels=["Protein", "Kulhydrater", "Fedt"],
                        autopct="%1.1f%%",
                        colors=["#4CAF50", "#2196F3", "#FF9800"],
                    )
                    ax.set_aspect("equal")
                    st.pyplot(fig)
                else:
                    st.info("Ingen makro-data at vise.")
                
                
            except requests.RequestException as e:
                st.error(f"Fejl ved kald af backend: {e}")