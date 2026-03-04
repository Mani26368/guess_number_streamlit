import streamlit as st
import random

st.title("🎮 Devine le nombre !")
st.write("J'ai choisi un nombre entre 1 et 100. Tu as **3 tentatives** pour le trouver !")

# Initialiser le jeu
if 'nombre_secret' not in st.session_state:
    st.session_state.nombre_secret = random.randint(1, 100)
    st.session_state.tentatives = 3
    st.session_state.gagne = False
    st.session_state.perdu = False

# Afficher les tentatives restantes
st.info(f"🎯 Tentatives restantes : {st.session_state.tentatives}")

# Input du joueur
if not st.session_state.gagne and not st.session_state.perdu:
    nombre_saisi = st.text_input("Entre un nombre entre 1 et 100 :")

    if st.button("✅ Valider"):
        try:
            nombre = int(nombre_saisi)

            if nombre < 1 or nombre > 100:
                st.error("❌ Entre un nombre entre 1 et 100 !")
            else:
                st.session_state.tentatives -= 1

                if nombre == st.session_state.nombre_secret:
                    st.session_state.gagne = True
                elif nombre < st.session_state.nombre_secret:
                    st.warning("📈 C'est **plus grand** !")
                else:
                    st.warning("📉 C'est **plus petit** !")

                if st.session_state.tentatives == 0 and not st.session_state.gagne:
                    st.session_state.perdu = True

        except ValueError:
            st.error("❌ Veuillez entrer un nombre valide !")

# Résultat final
if st.session_state.gagne:
    st.success(f"🎉 Bravo ! Tu as trouvé le nombre **{st.session_state.nombre_secret}** !")
elif st.session_state.perdu:
    st.error(f"😢 Perdu ! Le nombre secret était **{st.session_state.nombre_secret}**")

# Bouton rejouer
if st.session_state.gagne or st.session_state.perdu:
    if st.button("🔄 Rejouer"):
        st.session_state.nombre_secret = random.randint(1, 100)
        st.session_state.tentatives = 3
        st.session_state.gagne = False
        st.session_state.perdu = False
        st.rerun()
