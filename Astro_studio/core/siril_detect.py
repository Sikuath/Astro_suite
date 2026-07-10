from pathlib import Path


# ─────────────────────────────
# DETECTION AUTOMATIQUE SIRIL
# ─────────────────────────────

def detect_siril():

    candidates = [

        # Installation classique Windows
        Path(
            r"C:\Program Files\Siril\bin\siril-cli.exe"
        ),

        # Installation 32 bits éventuelle
        Path(
            r"C:\Program Files (x86)\Siril\bin\siril-cli.exe"
        ),

    ]


    for path in candidates:

        if path.exists():

            return str(path)


    return None