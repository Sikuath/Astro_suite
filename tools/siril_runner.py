import subprocess
from pathlib import Path
import streamlit as st



# ─────────────────────────────
# AFFICHAGE TERMINAL SIRIL
# ─────────────────────────────

def show_terminal(
    stdout,
    stderr=None
):
    """
    Affichage des logs Siril
    style terminal sombre.
    """


    if stdout:

        st.markdown(
            f"""
            <div style="
                background:#111827;
                color:#00ff88;
                padding:15px;
                border-radius:10px;
                font-family:Consolas, monospace;
                font-size:0.85em;
                white-space:pre-wrap;
                height:320px;
                overflow-y:auto;
                border:1px solid #374151;
            ">
{stdout}
            </div>
            """,
            unsafe_allow_html=True
        )



    if stderr:

        st.markdown(
            f"""
            <div style="
                background:#2b1111;
                color:#ff8080;
                padding:15px;
                border-radius:10px;
                font-family:Consolas, monospace;
                font-size:0.85em;
                white-space:pre-wrap;
                border:1px solid #7f1d1d;
            ">
{stderr}
            </div>
            """,
            unsafe_allow_html=True
        )




# ─────────────────────────────
# LANCEMENT SCRIPT SIRIL
# ─────────────────────────────

def run_siril_script(script_path):
    """
    Lance un script Siril externe.

    script_path :
        chemin complet vers le fichier .ssf

    Exemple :
        Astro_studio/scripts/04_RGB.ssf
    """



    # conversion Path

    script_path = Path(
        script_path
    )



    # -------------------------
    # VERIFICATION SCRIPT
    # -------------------------

    if not script_path.exists():

        st.error(
            f"Script Siril introuvable :\n{script_path}"
        )

        return False




    # -------------------------
    # RECUPERATION SIRIL
    # -------------------------

    siril = st.session_state.get(
        "siril"
    )


    if not siril:

        st.error(
            "Chemin Siril non configuré."
        )

        return False




    siril_path = Path(
        siril
    )



    if not siril_path.exists():

        st.error(
            f"Siril introuvable :\n{siril_path}"
        )

        return False




    # -------------------------
    # EXECUTION
    # -------------------------

    try:


        result = subprocess.run(

            [
                str(siril_path),

                "-s",

                str(script_path)

            ],

            capture_output=True,

            text=True

        )



        # -------------------------
        # AFFICHAGE TERMINAL
        # -------------------------

        show_terminal(
            result.stdout,
            result.stderr
        )




        # -------------------------
        # RESULTAT
        # -------------------------

        if result.returncode == 0:

            return True



        else:

            st.error(
                f"Siril a retourné le code {result.returncode}"
            )

            return False




    except Exception as e:


        st.error(
            f"Erreur lancement Siril : {e}"
        )

        return False