# ==========================================================
# Astro Suite
# core/prompt_builder.py
#
# Construction du prompt envoyé à Astro IA
# ==========================================================

from pathlib import Path
import json

from core.config import load_config


# ==========================================================
# DERNIERE SESSION
# ==========================================================

def get_latest_session_file():

    config = load_config()

    session_folder = Path(
        config["paths"]["data_sessions"]
    )

    if not session_folder.exists():
        return None

    files = sorted(
        session_folder.glob("astro_session_*.json"),
        reverse=True
    )

    if not files:
        return None

    return files[0]


# ==========================================================
# LECTURE JSON
# ==========================================================

def load_latest_session():

    session_file = get_latest_session_file()

    if session_file is None:
        return {}

    try:

        with open(
            session_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}


# ==========================================================
# PROMPT SYSTEME
# ==========================================================

def load_system_prompt():

    prompt_file = (
        Path(__file__).parent.parent
        / "prompts"
        / "astro_system_prompt.txt"
    )

    if not prompt_file.exists():

        return ""

    return prompt_file.read_text(
        encoding="utf-8"
    )


# ==========================================================
# CONSTRUCTION PROMPT
# ==========================================================

def build_prompt(
    user_request=""
):

    session = load_latest_session()

    system_prompt = load_system_prompt()

    session_json = json.dumps(
        session,
        indent=4,
        ensure_ascii=False
    )

    prompt = f"""
{system_prompt}

==========================================================
CONTEXTE DE SESSION ASTROPHOTOGRAPHIQUE
==========================================================

Le bloc ci-dessous provient automatiquement
de la dernière session Astro Suite.

Utilise ces informations comme contexte de référence.

Ne les recopie pas inutilement.

Appuie-toi dessus pour interpréter l'image.

```json
{session_json}