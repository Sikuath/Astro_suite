import streamlit as st
from pathlib import Path
import subprocess
import shutil
import re
import time


from core.config import load_config

from ui.theme import load_theme
from ui.sidebar import show_sidebar



# =====================================================
# Configuration
# =====================================================

st.set_page_config(
    page_title="Traitement Siril",
    page_icon="🖥️",
    layout="wide"
)



st.session_state.workflow_step = 5


load_theme()
show_sidebar()



# =====================================================
# Titre
# =====================================================

st.title(
    "🖥️ Traitement Siril"
)



# =====================================================
# Configuration projet
# =====================================================

config = load_config()


lights_folder = Path(
    config.get(
        "lights_folder",
        ""
    )
)


siril_exe = config.get(
    "siril_path",
    ""
)


processing_type = st.session_state.get(
    "session_analysis",
    {}
).get(
    "type",
    "Inconnu"
)



if not lights_folder.exists():

    st.error(
        "❌ Dossier Lights introuvable"
    )

    st.stop()



if not Path(siril_exe).exists():

    st.error(
        "❌ Siril introuvable"
    )

    st.stop()



# =====================================================
# Chemins Astro_suite
# =====================================================

base_dir = lights_folder.parent


script_dir = Path(
    r"F:\Astro_suite\Astro_pretraitement\scripts"
)


x_temp_dir = base_dir / "x_temp"


log_file = x_temp_dir / "lights_conversion.txt"



scripts = {

    "alignement":
        script_dir /
        "Alignement_lights.ssf",

    "LRGB":
        script_dir /
        "Traitement_LRGB.ssf",

    "SHO":
        script_dir /
        "Traitement_SHO.ssf",

    "LSHO":
        script_dir /
        "Traitement_LSHO.ssf"

}



dest_dirs = {

    "L": base_dir / "L",
    "R": base_dir / "R",
    "G": base_dir / "G",
    "B": base_dir / "B",
    "H": base_dir / "H",
    "O": base_dir / "O",
    "S": base_dir / "S"

}



# =====================================================
# Résumé
# =====================================================

st.subheader(
    "🚀 Pipeline en cours"
)


col1,col2,col3 = st.columns(3)


with col1:

    st.info(
        f"""
🎨 Traitement

**{processing_type}**
"""
    )


with col2:

    st.info(
        f"""
📁 Images

**{len(list(lights_folder.glob('*.fit')))} lights**
"""
    )


with col3:

    st.info(
        f"""
⚙️ Siril

**{Path(siril_exe).name}**
"""
    )



# =====================================================
# Terminal fixe
# =====================================================

st.divider()

st.subheader(
    "🖥️ Console Siril"
)



terminal = st.empty()


progress = st.progress(0)



if "siril_logs" not in st.session_state:

    st.session_state.siril_logs = []



def write_log(text):

    st.session_state.siril_logs.append(text)


    html = f"""
    <div style="
        height:400px;
        overflow-y:auto;
        background:#111;
        color:#00ff66;
        padding:15px;
        font-family:monospace;
        border-radius:8px;
        ">
    {"<br>".join(st.session_state.siril_logs)}
    </div>
    """


    terminal.markdown(
        html,
        unsafe_allow_html=True
    )



# =====================================================
# Siril
# =====================================================

def run_siril(script, name):


    write_log(
        f"🔧 {name}"
    )


    write_log(
        f"📜 {script.name}"
    )



    if not script.exists():

        write_log(
            f"❌ Script absent : {script}"
        )

        return False



    cmd = [

        siril_exe,

        "-s",

        str(script)

    ]



    proc = subprocess.Popen(

        cmd,

        cwd=str(script.parent),

        stdout=subprocess.PIPE,

        stderr=subprocess.STDOUT,

        text=True,

        encoding="utf-8",

        errors="replace"

    )



    for line in proc.stdout:

        line=line.strip()

        if line:

            write_log(line)



    proc.wait()



    if proc.returncode != 0:

        write_log(
            "❌ Erreur Siril"
        )

        return False



    write_log(
        "✅ Étape terminée"
    )


    return True



# =====================================================
# Déplacement couches
# =====================================================

def move_layers():


    if not log_file.exists():

        write_log(
            "⚠️ Log Siril absent"
        )

        return False



    pattern = re.compile(
        r"'[^']+[\\/](Light_[^']+\.fit)'\s*->\s*'\.\./x_temp[\\/](lights_\d+\.fit)'",
        re.IGNORECASE
    )


    moved = 0



    with open(
        log_file,
        encoding="utf-8",
        errors="ignore"
    ) as f:


        for line in f:


            m = pattern.search(line)


            if not m:

                continue



            source = m.group(1).lower()

            dest = m.group(2)



            couche=None


            for c in dest_dirs:

                if f"_{c.lower()}_" in source:

                    couche=c



            if couche:


                src=x_temp_dir/dest

                dst=dest_dirs[couche]/dest


                dest_dirs[couche].mkdir(
                    exist_ok=True
                )


                if src.exists():

                    shutil.move(
                        src,
                        dst
                    )

                    moved += 1



    write_log(
        f"✅ {moved} fichiers répartis"
    )


# =====================================================
# Nettoyage
# =====================================================

def clean_temp():

    if not x_temp_dir.exists():

        return


    for item in x_temp_dir.iterdir():

        try:

            if item.is_file():

                item.unlink()

            else:

                shutil.rmtree(item)

        except:

            pass



    write_log(
        "🧹 x_temp nettoyé"
    )



# =====================================================
# PIPELINE AUTOMATIQUE
# =====================================================

if "pipeline_started" not in st.session_state:


    st.session_state.pipeline_started=True


    start=time.time()


    write_log(
        "🚀 Démarrage Astro_suite"
    )


    write_log(
        f"📂 Projet : {base_dir}"
    )


    write_log(
        f"📜 Scripts : {script_dir}"
    )



    for d in dest_dirs.values():

        d.mkdir(
            exist_ok=True
        )



    progress.progress(20)



    if run_siril(
        scripts["alignement"],
        "Alignement des lights"
    ):


        progress.progress(60)


        move_layers()


        progress.progress(75)


        clean_temp()


        progress.progress(85)



        if processing_type in scripts:

            run_siril(
                scripts[processing_type],
                f"Traitement {processing_type}"
            )


        else:

            write_log(
                "❌ Type inconnu"
            )



    progress.progress(100)



    elapsed=time.time()-start


    write_log(
        f"🎉 Pipeline terminé en {elapsed:.1f}s"
    )


    st.success(
        "🎉 Traitement terminé"
    )