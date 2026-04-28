import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dia-Collect 232", layout="wide")

# --- IDENTIFICATION DANS LA SIDEBAR ---
st.sidebar.title("👨‍🎓 Identification")
st.sidebar.markdown(f"""
**Nom :** TSIADZE DONFACK DARLENE  
**Matricule :** 24G2361  
**Filière :** Informatique (Niveau 2)  
**Université :** Yaoundé I
""")

st.title("🩺 Dia-Collect 232 : Recensement du Diabète")

# --- DEFINITION DU FICHIER DE DONNEES ---
DB_FILE = 'data_collecte.csv'

# --- STRUCTURE DES ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📝 Collecte", "📊 Analyse Descriptive", "💡 Note Conceptuelle"])

# --- ONGLET 1 : COLLECTE ---
with tab1:
    st.subheader("Enregistrement des données cliniques")
    with st.form("form_patient", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Identifiant du Patient", placeholder="Ex: P-001")
            age = st.number_input("Âge", 0, 120, 25)
            genre = st.selectbox("Genre", ["Masculin", "Féminin"])
        with col2:
            poids = st.number_input("Poids (kg)", 1.0, 250.0, 70.0)
            taille = st.number_input("Taille (m)", 0.5, 2.5, 1.70)
            glycemie = st.number_input("Glycémie (g/L)", 0.1, 8.0, 1.0)
        
        submit = st.form_submit_button("Valider et Enregistrer")

        if submit:
            if nom:
                # Calcul de l'IMC
                imc = round(poids / (taille ** 2), 2)
                # Création de la ligne
                nouveau_patient = pd.DataFrame([{
                    "Nom": nom, 
                    "Age": age, 
                    "Genre": genre, 
                    "Glycemie": glycemie, 
                    "IMC": imc
                }])
                
                # Sauvegarde locale
                if not os.path.isfile(DB_FILE):
                    nouveau_patient.to_csv(DB_FILE, index=False)
                else:
                    nouveau_patient.to_csv(DB_FILE, mode='a', header=False, index=False)
                
                st.success(f"✅ Patient {nom} enregistré !")
            else:
                st.error("⚠️ L'identifiant est obligatoire.")

# --- ONGLET 2 : ANALYSE DESCRIPTIVE (LES 3 GRAPHES) ---
with tab2:
    st.header("Visualisation des Statistiques")
    
    if os.path.isfile(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        # --- GRAPHE 1 : RÉPARTITION PAR GENRE ---
        st.subheader("1. Répartition par Genre")
        fig1 = px.pie(df, names='Genre', hole=0.4, title="Structure de l'échantillon")
        st.plotly_chart(fig1, use_container_width=True)
        st.info("📌 **Analyse :** Ce graphique circulaire montre la balance entre les hommes et les femmes dans notre étude.")

        st.divider()

        # --- GRAPHE 2 : GLYCÉMIE PAR ÂGE ---
        st.subheader("2. Glycémie en fonction de l'Âge")
        fig2 = px.bar(df, x="Age", y="Glycemie", color="Genre", title="Distribution de la Glycémie")
        st.plotly_chart(fig2, use_container_width=True)
        st.info("📌 **Analyse :** Ce diagramme permet d'identifier si certaines tranches d'âge présentent des taux de glycémie plus élevés.")

        st.divider()

        # --- GRAPHE 3 : CORRÉLATION IMC / GLYCÉMIE ---
        st.subheader("3. Corrélation entre IMC et Glycémie")
        fig3 = px.scatter(df, x="IMC", y="Glycemie", color="Genre", size="Age", title="Analyse Bivariée")
        st.plotly_chart(fig3, use_container_width=True)
        st.info("📌 **Analyse :** Ce nuage de points explore la relation entre le surpoids (IMC) et le taux de sucre dans le sang.")
        
        st.divider()
        st.write("### Base de données actuelle")
        st.dataframe(df, use_container_width=True)
        
        # BOUTON DE SAUVEGARDE POUR RENDRE LES DONNEES PERMANENTES SUR TON PC
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger les données (Sauvegarde CSV)", data=csv, file_name='donnees_diabete.csv', mime='text/csv')
    else:
        st.warning("Aucune donnée enregistrée. Remplissez le formulaire de l'onglet Collecte.")

# --- ONGLET 3 : NOTE CONCEPTUELLE ---
with tab3:
    st.header("Note Conceptuelle")
    st.markdown("""
    **Projet INF 232** Ce système permet de digitaliser la collecte des données cliniques pour une meilleure analyse épidémiologique du diabète à Yaoundé.  
    
    **Outils utilisés :** - Python & Streamlit (Interface)  
    - Pandas (Gestion des données)  
    - Plotly (Visualisation graphique)  
    
    **Auteur :** TSIADZE DONFACK DARLENE
    """)
