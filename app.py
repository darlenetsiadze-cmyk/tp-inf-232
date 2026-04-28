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
            glycemie = st.number_input("Glycémie (g/L)", 0.1, 8.0, 1.0)
        
        tension = st.slider("Pression Artérielle (mmHg)", 50, 200, 120)
        
        submit = st.form_submit_button("Valider et Enregistrer")

        if submit:
            if nom:
                imc = round(poids / (taille ** 2), 2)
                # Création du dictionnaire de données (Les noms ici doivent être dans le CSV)
                nouveau = pd.DataFrame([{
                    "Nom": nom, 
                    "Age": age, 
                    "Genre": genre, 
                    "Glycemie": glycemie, 
                    "IMC": imc, 
                    "Tension": tension
                }])
                
                # Sauvegarde
                if not os.path.isfile(DB_FILE):
                    nouveau.to_csv(DB_FILE, index=False)
                else:
                    nouveau.to_csv(DB_FILE, mode='a', header=False, index=False)
                st.success(f"✅ Données enregistrées pour {nom}")
            else:
                st.error("⚠️ L'identifiant est obligatoire !")

# --- ONGLET 2 : ANALYSE DESCRIPTIVE ---
with tab2:
    st.header("Tableau de Bord Statistique")
    
    if os.path.isfile(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        # Petit résumé (Metrics)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Patients", len(df))
        c2.metric("Moyenne Glycémie", f"{df['Glycemie'].mean():.2f} g/L")
        c3.metric("Moyenne IMC", f"{df['IMC'].mean():.2f}")

        st.divider()

        # GRAPHE 1 : RÉPARTITION PAR GENRE
        st.subheader("1. Répartition par Genre")
        fig1 = px.pie(df, names='Genre', hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)
        st.info("📌 **Explication :** Ce graphique montre l'équilibre hommes/femmes de notre base de données.")

        # GRAPHE 2 : RELATION AGE VS GLYCEMIE (Corrigé sans l'erreur 'ID')
        st.subheader("2. Relation Age vs Glycémie")
        fig2 = px.scatter(
            df, 
            x="Age", 
            y="Glycemie", 
            color="Genre",
            hover_name="Nom", # On utilise "Nom" car "ID" n'existe pas
            title="Analyse de la Glycémie par âge"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.info("📌 **Explication :** Ce nuage de points permet de voir si le taux de sucre augmente avec l'âge.")

        # GRAPHE 3 : CORRÉLATION IMC / GLYCÉMIE
        st.subheader("3. Corrélation IMC vs Glycémie")
        fig3 = px.scatter(df, x="IMC", y="Glycemie", color="Genre")
        st.plotly_chart(fig3, use_container_width=True)
        st.info("📌 **Explication :** Ce graphique vérifie si un IMC élevé est un facteur de risque pour le diabète.")

        st.divider()
        st.write("### Aperçu de la base de données")
        st.dataframe(df, use_container_width=True)
        
        # Bouton de téléchargement
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger la base complète", data=csv, file_name='donnees_diabete.csv', mime='text/csv')
    else:
        st.warning("⚠️ Aucune donnée disponible. Veuillez remplir le formulaire.")

# --- ONGLET 3 : NOTE CONCEPTUELLE ---
with tab3:
    st.header("💡 Note Technique & Conceptuelle")
    st.markdown(f"""
    ### 🎯 Contexte du Projet
    Cette application répond aux exigences du **TP INF 232 EC2 (Analyse de Données)**. Elle se concentre sur le secteur de la **Santé Publique**, spécifiquement le suivi du diabète en milieu universitaire.

    ### 🛠️ Choix Techniques (Qualités de l'application) :
    1.  **Créativité :** Intégration d'un calculateur d'IMC automatique et d'une analyse bivariée en temps réel.
    2.  **Robustesse :** Persistance des données via CSV et gestion automatique des tris.
    3.  **Efficacité :** Interface simplifiée permettant une saisie rapide et une visualisation immédiate.
    4.  **Fiabilité :** Algorithmes de calcul basés sur les standards de l'OMS (Organisation Mondiale de la Santé).

    **Étudiante :** TSIADZE DONFACK DARLENE| **Niveau :** L2 Informatique (Ngoa-Ekélé)
    """)
