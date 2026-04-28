import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dia-Collect 232", layout="wide")

# --- IDENTIFICATION (SIDEBAR) ---
st.sidebar.title("👨‍🎓 Identification")
st.sidebar.markdown("""
**Nom :** TSIADZE DONFACK DARLENE  
**Matricule :** 24G2361  
**Niveau :** Informatique Niveau 2
""")

st.title("🩺 Dia-Collect : Système de Surveillance du Diabète")

# Nom du fichier de données
DB_FILE = 'data_collecte.csv'

# --- STRUCTURE DES ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📝 Collecte", "📊 Analyse Descriptive", "💡 Note Conceptuelle"])

# --- ONGLET 1 : COLLECTE ---
with tab1:
    st.subheader("Enregistrement des données cliniques")
    with st.form("form_patient", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            # On utilise "Nom" comme identifiant principal
            nom = st.text_input("Identifiant Patient (Ex: P-001)")
            age = st.number_input("Âge", 0, 120, 25)
            genre = st.selectbox("Genre", ["Masculin", "Féminin"])
        with col2:
            poids = st.number_input("Poids (kg)", 1.0, 250.0, 70.0)
            taille = st.number_input("Taille (m)", 0.5, 2.5, 1.75)
            glycemie = st.number_input("Glycémie (
