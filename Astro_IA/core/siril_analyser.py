from pathlib import Path
import shutil
import csv
import json


class SirilAnalyser:


    def __init__(
        self,
        runner
    ):

        self.runner = runner


        self.script = (
            runner.script_dir
            /
            "Analyse_Champ.ssf"
        )



    # =====================================================
    # ANALYSE DU CHAMP
    # =====================================================

    def analyse_field(
        self,
        workdir: Path,
        fits_file: Path,
        callback=None
    ):


        workdir = Path(workdir)

        fits_file = Path(fits_file)



        if not fits_file.exists():

            raise FileNotFoundError(
                f"FITS introuvable : {fits_file}"
            )



        # -------------------------------------------------
        # préparation dossier Siril
        # -------------------------------------------------

        workdir.mkdir(
            exist_ok=True
        )



        siril_image = (
            workdir
            /
            "analyse.fit"
        )



        shutil.copy(

            fits_file,

            siril_image

        )



        # -------------------------------------------------
        # lancement Siril
        # -------------------------------------------------

        success, logs = self.runner.run(

            self.script,

            workdir,

            callback

        )



        if not success:

            raise RuntimeError(

                "Analyse Siril échouée\n\n"
                +
                "\n".join(logs)

            )



        # -------------------------------------------------
        # lecture CSV objets
        # -------------------------------------------------

        csv_file = (

            workdir

            /

            "objects.csv"

        )



        objects = []



        if csv_file.exists():


            with open(

                csv_file,

                newline="",

                encoding="utf-8"

            ) as f:


                reader = csv.DictReader(f)


                for row in reader:

                    objects.append(
                        row
                    )



        # -------------------------------------------------
        # lecture JSON Siril / Astro IA
        # sélection du JSON le plus récent
        # -------------------------------------------------

        json_candidates = [

            workdir / "objects.json",

            workdir / "analyse.json",

            workdir / "siril.json"

        ]


        # Recherche des sessions Astro IA horodatées

        astro_json_files = sorted(

            workdir.glob(

                "astro_session_*.json"

            ),

            key=lambda f: f.stat().st_mtime,

            reverse=True

        )


        # Le plus récent devient prioritaire

        if astro_json_files:

            json_candidates.insert(

                0,

                astro_json_files[0]

            )



        json_file = None

        siril_json = {}



        for candidate in json_candidates:


            if candidate.exists():


                json_file = candidate


                try:


                    with open(

                        candidate,

                        "r",

                        encoding="utf-8"

                    ) as f:


                        siril_json = json.load(f)



                except Exception:


                    siril_json = {}



                break



        # -------------------------------------------------
        # retour complet pour IA
        # -------------------------------------------------

        return {


            "objects":

                objects,


            "csv":

                str(csv_file),


            "json":

                siril_json,


            "json_file":

                str(json_file)
                if json_file
                else None,


            "workdir":

                str(workdir),


            "logs":

                logs

        }