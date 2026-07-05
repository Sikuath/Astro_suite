import streamlit as st
from pathlib import Path
import time


def show_preprocessing():

    st.title("🔭 Prétraitement Siril")

    workdir = st.session_state.get("workdir")
    siril = st.session_state.get("siril")

    if not workdir or not siril:
        st.warning("Projet ou Siril non configuré")
        return

    st.markdown("### 📂 Projet actif")
    st.code(workdir)

    # -------------------------
    # UI STATUS
    # -------------------------
    st.markdown("## ⚙️ Pipeline")

    steps = [
        "Astrométrie",
        "Alignement",
        "Linear match",
        "Normalisation"
    ]

    progress = st.progress(0)
    log_box = st.empty()

    # -------------------------
    # START BUTTON
    # -------------------------
    if st.button("🚀 Lancer le prétraitement"):

        for i, step in enumerate(steps):

            log_box.info(f"▶ {step} en cours...")

            # ici plus tard: runner.run(script)
            time.sleep(1)  # simulation

            log_box.success(f"✔ {step} terminé")

            progress.progress((i + 1) / len(steps))

        st.success("🎉 Prétraitement terminé !")