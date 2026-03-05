import streamlit as st

# ─── Config page ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Devine le Nombre • 2 Joueurs", page_icon="🎯")

st.markdown("""
<style>
  .stApp { background: #0a0a0f; color: #fff; }
  h1 { text-align: center; font-size: 2.2rem; }
  .player1 { color: #ff5050; font-weight: bold; }
  .player2 { color: #50a0ff; font-weight: bold; }
  .hint-up   { background: rgba(255,200,50,0.12); border-left: 3px solid #ffc832;
               padding: 8px 14px; border-radius: 6px; margin: 4px 0; }
  .hint-down { background: rgba(255,100,50,0.12); border-left: 3px solid #ff6432;
               padding: 8px 14px; border-radius: 6px; margin: 4px 0; }
  .found     { background: rgba(80,255,120,0.12); border-left: 3px solid #50ff78;
               padding: 8px 14px; border-radius: 6px; margin: 4px 0; }
</style>
""", unsafe_allow_html=True)

# ─── Phases : setup → guess → win ─────────────────────────────────────────────
SETUP = "setup"
GUESS = "guess"
WIN   = "win"

def init():
    defaults = {
        "phase":    SETUP,
        "names":    ["Joueur 1", "Joueur 2"],
        "secrets":  [None, None],
        "history":  [[], []],
        "attempts": [0, 0],
        "turn":     0,
        "winner":   None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

st.title("🎯 Devine le Nombre !")
st.markdown("<p style='text-align:center;color:#888;letter-spacing:3px;font-size:12px;'>2 JOUEURS • 1–100 • PREMIER QUI TROUVE GAGNE</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — SETUP : chaque joueur choisit son nombre secret
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == SETUP:
    st.markdown("---")
    st.subheader("🔒 Choisissez vos nombres secrets")
    st.caption("Chaque joueur saisit son nombre secret à tour de rôle. L'autre ne regarde pas !")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="player1">🔴 Joueur 1</p>', unsafe_allow_html=True)
        name1 = st.text_input("Nom du joueur 1", value="Joueur 1", key="name1_input")
        secret1 = st.number_input("Nombre secret (1–100)", min_value=1, max_value=100,
                                  key="secret1_input", label_visibility="visible")

    with col2:
        st.markdown('<p class="player2">🔵 Joueur 2</p>', unsafe_allow_html=True)
        name2 = st.text_input("Nom du joueur 2", value="Joueur 2", key="name2_input")
        secret2 = st.number_input("Nombre secret (1–100)", min_value=1, max_value=100,
                                  key="secret2_input", label_visibility="visible")

    st.markdown("---")
    if st.button("🚀 Commencer la partie", use_container_width=True, type="primary"):
        st.session_state.names   = [name1.strip() or "Joueur 1", name2.strip() or "Joueur 2"]
        st.session_state.secrets = [int(secret1), int(secret2)]
        st.session_state.phase   = GUESS
        st.session_state.turn    = 0
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — GUESS : les joueurs devinent en alternance
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == GUESS:
    names   = st.session_state.names
    secrets = st.session_state.secrets
    turn    = st.session_state.turn
    opp     = 1 - turn

    # Indicateur de tour
    color_cls = "player1" if turn == 0 else "player2"
    icon      = "🔴" if turn == 0 else "🔵"
    st.markdown(f'<h3 style="text-align:center">{icon} Tour de <span class="{color_cls}">{names[turn]}</span></h3>',
                unsafe_allow_html=True)
    st.caption(f"{names[turn]} doit deviner le nombre secret de {names[opp]}")
    st.markdown("---")

    # Historique des tentatives du joueur actif
    history = st.session_state.history[turn]
    if history:
        st.markdown(f"**Tes essais précédents ({names[turn]}) :**")
        for fb in history:
            st.markdown(f'<div class="{fb["css"]}">{fb["icon"]} {fb["text"]}</div>',
                        unsafe_allow_html=True)
        st.markdown("")

    # Saisie du prochain essai
    attempt_n = st.session_state.attempts[turn] + 1
    guess = st.number_input(
        f"Essai #{attempt_n} — entre un nombre entre 1 et 100 :",
        min_value=1, max_value=100, key=f"guess_{turn}_{attempt_n}"
    )

    if st.button(f"✅ Valider mon essai", use_container_width=True, type="primary"):
        secret = secrets[opp]
        st.session_state.attempts[turn] += 1

        if guess == secret:
            st.session_state.history[turn].append({
                "text": f"{guess} → Trouvé !",
                "icon": "🎯",
                "css":  "found",
            })
            st.session_state.winner = turn
            st.session_state.phase  = WIN
        elif guess < secret:
            st.session_state.history[turn].append({
                "text": f"{guess} → c'est plus grand",
                "icon": "📈",
                "css":  "hint-up",
            })
            st.session_state.turn = opp  # passe la main
        else:
            st.session_state.history[turn].append({
                "text": f"{guess} → c'est plus petit",
                "icon": "📉",
                "css":  "hint-down",
            })
            st.session_state.turn = opp  # passe la main

        st.rerun()

    # Récap tentatives en bas
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(f"🔴 Essais {names[0]}", st.session_state.attempts[0])
    with c2:
        st.metric(f"🔵 Essais {names[1]}", st.session_state.attempts[1])

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — WIN
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == WIN:
    winner  = st.session_state.winner
    names   = st.session_state.names
    secrets = st.session_state.secrets
    attempts= st.session_state.attempts

    color_cls = "player1" if winner == 0 else "player2"
    icon      = "🔴" if winner == 0 else "🔵"

    st.markdown("---")
    st.markdown(f'<h2 style="text-align:center">🏆 <span class="{color_cls}">{names[winner]}</span> a gagné !</h2>',
                unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align:center;color:#aaa;">A trouvé <b>{secrets[1-winner]}</b> '
        f'en <b>{attempts[winner]}</b> essai{"s" if attempts[winner]>1 else ""} !</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<p class="player1">🔴 {names[0]}</p>', unsafe_allow_html=True)
        st.metric("Essais", attempts[0])
        st.caption(f"Nombre secret de {names[1]} : **{secrets[1]}**")
    with col2:
        st.markdown(f'<p class="player2">🔵 {names[1]}</p>', unsafe_allow_html=True)
        st.metric("Essais", attempts[1])
        st.caption(f"Nombre secret de {names[0]} : **{secrets[0]}**")

    st.markdown("---")
    if st.button("🔄 Rejouer", use_container_width=True):
        for key in ["phase","names","secrets","history","attempts","turn","winner"]:
            del st.session_state[key]
        st.rerun()
