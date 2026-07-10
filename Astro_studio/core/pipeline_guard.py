from pathlib import Path


class PipelineGuard:
    """
    Sécurise le pipeline Astro Studio avant exécution Siril.

    Rôle UNIQUE :
    - vérifier que les fichiers nécessaires existent
    - éviter de lancer Siril avec un dataset incomplet
    """

    REQUIRED_INPUTS = ["SII.fit", "HA.fit", "OIII.fit"]

    def __init__(self, workdir: Path):
        self.workdir = Path(workdir)

    # -----------------------------
    # CHECK INPUT FILES
    # -----------------------------
    def check_inputs(self) -> bool:
        """
        Vérifie que tous les fichiers nécessaires sont présents.
        """

        missing = []

        for filename in self.REQUIRED_INPUTS:
            file_path = self.workdir / filename

            if not file_path.exists():
                missing.append(filename)

        if missing:
            raise FileNotFoundError(
                f"[PipelineGuard] Fichiers manquants : {missing}"
            )

        return True

    # -----------------------------
    # VALIDATE WORKDIR
    # -----------------------------
    def check_workdir(self) -> bool:
        """
        Vérifie que le dossier de travail existe.
        """

        if not self.workdir.exists():
            raise FileNotFoundError(
                f"[PipelineGuard] Workdir introuvable : {self.workdir}"
            )

        return True

    # -----------------------------
    # FULL VALIDATION
    # -----------------------------
    def run(self) -> bool:
        """
        Point d'entrée unique du guard.
        """

        self.check_workdir()
        self.check_inputs()

        return True