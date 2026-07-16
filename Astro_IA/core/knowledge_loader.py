# ==========================================================
# Astro IA
# Knowledge Loader
# Chargement hiérarchisé de la base de connaissances
# ==========================================================

from pathlib import Path


# ==========================================================
# DOSSIER DOCUMENTATION
# ==========================================================

KNOWLEDGE_DIR = (
    Path(__file__).parent.parent / "knowledge"
)


# ==========================================================
# CHARGEMENT DOCUMENT
# ==========================================================

def load_document(filename):

    path = KNOWLEDGE_DIR / filename

    if not path.exists():
        return f"""
DOCUMENT ABSENT

Fichier :
{filename}
"""

    try:
        return path.read_text(
            encoding="utf-8"
        )

    except Exception as e:
        return f"""
ERREUR DE LECTURE

Fichier :
{filename}

Erreur :
{e}
"""


# ==========================================================
# AJOUT DOCUMENT
# ==========================================================

def add_document(
    documents,
    title,
    filename
):

    documents.append(
        f"""

############################################################
# {title}
############################################################

{load_document(filename)}

"""
    )


# ==========================================================
# CONSTRUCTION BASE DE CONNAISSANCES
# ==========================================================

def get_relevant_knowledge(
    workflow=None,
    camera=None
):

    documents = []

    # ======================================================
    # 1 - GARDE-FOUS
    # ======================================================

    add_document(
        documents,
        "INTERDICTIONS ET GARDE-FOUS",
        "interdictions.md"
    )

    # ======================================================
    # 2 - REGLES GENERALES
    # ======================================================

    add_document(
        documents,
        "REGLES GENERALES ASTRO IA",
        "regles_astro.md"
    )
    

    # ======================================================
    # 3 - BIBLIOTHEQUE DES DEFAUTS VISUELS
    # ======================================================

    add_document(
        documents,
        "BIBLIOTHEQUE DES DEFAUTS VISUELS",
        "defauts_visuels.md"
    )

    # ======================================================
    # 4 - WORKFLOW COMPLET
    # ======================================================

    add_document(
        documents,
        "WORKFLOW COMPLET SIRIL + GIMP",
        "workflow_traitement_complet.md"
    )

    # ======================================================
    # 5 - PROCEDURES SIRIL
    # ======================================================

    add_document(
        documents,
        "PROCEDURES DETAILLEES SIRIL",
        "workflow_siril.md"
    )

    # ======================================================
    # 6 - PROCEDURES GIMP
    # ======================================================

    add_document(
        documents,
        "PROCEDURES DETAILLEES GIMP",
        "workflow_gimp.md"
    )

    # ======================================================
    # 7 - WORKFLOW SPECIFIQUE
    # ======================================================

    if workflow:

        workflow = workflow.upper()

        if workflow == "SHO":

            add_document(
                documents,
                "WORKFLOW SHO",
                "workflow_sho.md"
            )

        elif workflow == "LRGB":

            add_document(
                documents,
                "WORKFLOW LRGB",
                "workflow_lrgb.md"
            )

    # ======================================================
    # 8 - CAMERA
    # ======================================================

    if camera:

        camera_upper = camera.upper()

        if "ASI2600" in camera_upper:

            add_document(
                documents,
                "CAMERA ZWO ASI2600MM PRO",
                "asi2600mm.md"
            )

    # ======================================================
    # CONTEXTE FINAL
    # ======================================================

    return "\n\n".join(documents)