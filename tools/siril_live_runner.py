import subprocess
from pathlib import Path
import streamlit as st



# ─────────────────────────────
# LANCEMENT SIRIL LIVE
# ─────────────────────────────

def run_siril_live_script(
    script_path,
    terminal
):
    """
    Lance un script Siril avec affichage
    des logs en direct dans un terminal Astro.

    Utilisé pour les étapes LRGB / RGB final.
    """



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



    logs = []



    # -------------------------
    # EXECUTION LIVE
    # -------------------------

    try:


        process = subprocess.Popen(

            [
                str(siril_path),

                "-s",

                str(script_path)

            ],

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            encoding="utf-8",

            errors="replace"

        )



        for line in process.stdout:


            # -------------------------
            # NETTOYAGE LOGS WINDOWS
            # -------------------------

            line = line.replace(
                "\r",
                ""
            ).rstrip()



            logs.append(
                line
            )



            # -------------------------
            # TERMINAL ASTRO
            # -------------------------

            terminal.code(

                "\n".join(
                    logs[-50:]
                ),

                language=None

            )



        process.wait()



        # -------------------------
        # RESULTAT
        # -------------------------

        if process.returncode == 0:

            return True



        else:

            st.error(
                f"Siril a retourné le code {process.returncode}"
            )

            return False



    except Exception as e:


        st.error(
            f"Erreur lancement Siril : {e}"
        )

        return False