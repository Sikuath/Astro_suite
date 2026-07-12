from pathlib import Path


class LRGBPipelineGuard:
    """
    Sécurise le pipeline LRGB Astro Studio avant exécution Siril.

    Rôle :
    - vérifier que les fichiers nécessaires existent
    - empêcher le lancement Siril avec un dataset incomplet
    """


    REQUIRED_INPUTS = [

        "L.fit",

        "R.fit",

        "G.fit",

        "B.fit"

    ]



    def __init__(self, workdir: Path):

        self.workdir = Path(workdir)



    # -----------------------------
    # CHECK INPUT FILES
    # -----------------------------

    def check_inputs(self) -> bool:

        """
        Vérifie la présence des couches LRGB.
        """

        missing = []


        for filename in self.REQUIRED_INPUTS:


            file_path = self.workdir / filename


            if not file_path.exists():

                missing.append(filename)



        if missing:

            raise FileNotFoundError(
                f"[LRGBPipelineGuard] Fichiers manquants : {missing}"
            )



        return True



    # -----------------------------
    # VALIDATE WORKDIR
    # -----------------------------

    def check_workdir(self) -> bool:

        """
        Vérifie que le dossier projet existe.
        """

        if not self.workdir.exists():

            raise FileNotFoundError(
                f"[LRGBPipelineGuard] Workdir introuvable : {self.workdir}"
            )


        return True



    # -----------------------------
    # FULL VALIDATION
    # -----------------------------

    def run(self) -> bool:

        """
        Validation complète avant pipeline.
        """

        self.check_workdir()

        self.check_inputs()


        return True