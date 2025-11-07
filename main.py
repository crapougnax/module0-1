import streamlit as st
import requests
from loguru import logger

st.title("Translator")

st.text_input("Votre message", key="texte")

if st.button("Analyser"):
    texte = st.session_state.texte
    # Si il y a du text alors
    if texte:
        logger.info(f"Texte à analyser: {texte}")
        try:
            response = requests.post("http://127.0.0.1:9000/chat/", json={"texte": texte})
            # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
            response.raise_for_status()
            payload = response.json()
            st.write("Résultats de l'analyse :")
            print(payload)
            # st.write(f"Polarité négative : {sentiment['neg']}")
            # st.write(f"Polarité neutre : {sentiment['neu']}")
            # st.write(f"Polarité positive : {sentiment['pos']}")
            # st.write(f"Score composé : {sentiment['compound']}")

            # if sentiment['compound'] >= 0.05 :
            #     st.write("Sentiment global : Positif 😀")
            # elif sentiment['compound'] <= -0.05 :
            #     st.write("Sentiment global : Négatif 🙁")
            # else :
            #     st.write("Sentiment global : Neutre 😐")
            #     logger.info(f"Résultats affichés: {sentiment}")

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la requête : {e}")
