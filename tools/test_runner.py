import streamlit as st
from pathlib import Path

from core.siril_runner import SirilRunner


def test_runner():

    st.title("🧪 Test Siril")

    if st.button("Lancer Siril"):

        terminal = st.empty()

        logs = []

        def log(message):

            logs.append(message)

            terminal.code(
                "\n".join(logs),
                language=None,
            )

        runner = SirilRunner(
            st.session_state["siril"]
        )

        ok = runner.run(
            Path("scripts/test.ssf"),
            Path(st.session_state["workdir"]),
            callback=log,
        )

        if ok:
            st.success("Script terminé.")
        else:
            st.error("Erreur Siril.")