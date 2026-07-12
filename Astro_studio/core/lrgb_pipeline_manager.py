from pathlib import Path
import shutil

from core.lrgb_pipeline_guard import LRGBPipelineGuard
from core.siril_runner import SirilRunner
from core.prepare_lrgb_sequence import prepare_lrgb_sequence



class LRGBPipelineManager:


    def __init__(
        self,
        workdir: str,
        siril_path: str
    ):


        self.workdir = Path(workdir)


        self.guard = LRGBPipelineGuard(
            self.workdir
        )


        self.runner = SirilRunner(
            siril_path
        )


        # Scripts LRGB

        self.step1_script = Path(
            "scripts/01_LRGB_astrometry.ssf"
        )

        self.step2_script = Path(
            "scripts/02_LRGB_registration.ssf"
        )

        self.step3_script = Path(
            "scripts/03_LRGB_linear_match.ssf"
        )



    # =========================================================
    # CALLBACK SAFE
    # =========================================================

    def _safe_callback(
        self,
        callback
    ):


        def wrapper(line):

            if callback:

                callback(line)


        return wrapper




    # =========================================================
    # PREPARE
    # =========================================================

    def prepare(self):


        self.guard.check_workdir()


        structure = prepare_lrgb_sequence(
            self.workdir
        )


        self.guard.check_inputs()


        return structure




    # =========================================================
    # RUN SIRIL
    # =========================================================

    def run_astrometry(
        self,
        callback=None
    ):


        return self.runner.run(

            script=self.step1_script,

            workdir=self.workdir,

            callback=self._safe_callback(
                callback
            )
        )



    def run_registration(
        self,
        callback=None
    ):


        return self.runner.run(

            script=self.step2_script,

            workdir=self.workdir,

            callback=self._safe_callback(
                callback
            )
        )



    def run_linear_match(
        self,
        callback=None
    ):


        return self.runner.run(

            script=self.step3_script,

            workdir=self.workdir,

            callback=self._safe_callback(
                callback
            )
        )




    # =========================================================
    # COPY
    # =========================================================

    def copy_files(
        self,
        src_dir,
        dst_dir,
        files
    ):


        dst_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        for filename in files:


            src = src_dir / filename

            dst = dst_dir / filename



            if not src.exists():

                raise FileNotFoundError(
                    f"Missing file : {src}"
                )



            shutil.copy2(
                src,
                dst
            )




    # =========================================================
    # STEP 0
    # COPY INPUTS
    # =========================================================

    def copy_inputs_to_astrometry(self):


        self.copy_files(

            self.workdir,

            self.workdir
            / "process"
            / "astrometrie",

            [

                "L.fit",
                "R.fit",
                "G.fit",
                "B.fit"

            ]

        )




    # =========================================================
    # READ CONVERSION
    # =========================================================

    def read_conversion_mapping(self):


        txt = (

            self.workdir
            / "process"
            / "registration"
            / "process"
            / "colors_conversion.txt"

        )


        if not txt.exists():

            raise FileNotFoundError(
                f"Missing : {txt}"
            )


        mapping = {}



        with open(
            txt,
            "r",
            encoding="utf-8"
        ) as file:



            for line in file:


                if "->" not in line:

                    continue



                left, right = line.split(
                    "->"
                )



                left = left.strip()

                right = right.strip()



                number = (

                    Path(right)
                    .stem
                    .split("_")[-1]

                )



                channel = (

                    Path(left)
                    .stem
                    .replace(
                        "_astrom",
                        ""
                    )
                    .strip()

                )


                mapping[number] = channel + ".fit"



        return mapping




    # =========================================================
    # RENAME REGISTERED
    # =========================================================

    def rename_registered_files(
        self,
        mapping
    ):


        reg_dir = (

            self.workdir
            / "process"
            / "registration"
            / "process"

        )



        for number, channel in mapping.items():


            src = (

                reg_dir
                /
                f"r_colors_{number}.fit"

            )


            dst = (

                reg_dir
                /
                channel

            )



            if not src.exists():

                raise FileNotFoundError(
                    f"Missing : {src}"
                )



            if dst.exists():

                dst.unlink()



            shutil.move(

                str(src),

                str(dst)

            )




    # =========================================================
    # CLEANUP
    # =========================================================

    def cleanup(self):


        process = self.workdir / "process"


        for folder in [

            "astrometrie",
            "registration"

        ]:


            path = process / folder


            if path.exists():

                shutil.rmtree(
                    path
                )



        print(
            "Temporary LRGB folders removed."
        )




    # =========================================================
    # FULL PIPELINE
    # =========================================================

    def run_full(
        self,
        callback=None,
        progress_callback=None
    ):


        logs = []



        def log(msg):

            logs.append(msg)

            if callback:

                callback(msg)




        # ==========================
        # PREPARE
        # ==========================

        log(
            "🧹 Preparing LRGB workspace..."
        )


        try:

            self.prepare()


        except Exception as e:


            log(
                f"❌ PREPARE FAILED : {e}"
            )

            return False, logs




        log(
            "✔ Workspace ready"
        )




        # ==========================
        # COPY INPUTS
        # ==========================

        log(
            "📂 STEP 0 - Copy LRGB inputs"
        )


        try:

            self.copy_inputs_to_astrometry()


        except Exception as e:


            log(
                f"❌ COPY FAILED : {e}"
            )

            return False, logs




        # ==========================
        # ASTROMETRY
        # ==========================

        log(
            "▶ STEP 1 - LRGB Astrometry"
        )


        ok, _ = self.run_astrometry(
            callback=log
        )


        if not ok:


            log(
                "❌ ASTROMETRY FAILED"
            )

            return False, logs




        log(
            "✔ Astrometry done"
        )




        # ==========================
        # COPY ASTROM
        # ==========================

        log(
            "📂 STEP 2 - Copy astrometric files"
        )



        try:


            self.copy_files(

                self.workdir
                /
                "process"
                /
                "astrometrie",

                self.workdir
                /
                "process"
                /
                "registration",

                [

                    "L_astrom.fit",
                    "R_astrom.fit",
                    "G_astrom.fit",
                    "B_astrom.fit"

                ]

            )


        except Exception as e:


            log(
                f"❌ COPY ASTROM FAILED : {e}"
            )

            return False, logs




        # ==========================
        # REGISTRATION
        # ==========================

        log(
            "▶ STEP 3 - LRGB Registration"
        )


        ok, _ = self.run_registration(
            callback=log
        )


        if not ok:


            log(
                "❌ REGISTRATION FAILED"
            )

            return False, logs




        # ==========================
        # RENAME
        # ==========================

        log(
            "🏷️ STEP 4 - Rename registered files"
        )


        try:


            mapping = self.read_conversion_mapping()


            log(
                f"Mapping : {mapping}"
            )


            self.rename_registered_files(
                mapping
            )


        except Exception as e:


            log(
                f"❌ RENAME FAILED : {e}"
            )

            return False, logs




        # ==========================
        # COPY LINEAR
        # ==========================

        log(
            "📂 STEP 5 - Prepare linear channels"
        )


        try:


            self.copy_files(

                self.workdir
                /
                "process"
                /
                "registration"
                /
                "process",

                self.workdir
                /
                "process"
                /
                "linear",

                [

                    "L.fit",
                    "R.fit",
                    "G.fit",
                    "B.fit"

                ]

            )


        except Exception as e:


            log(
                f"❌ LINEAR COPY FAILED : {e}"
            )

            return False, logs




        # ==========================
        # LINEAR MATCH
        # ==========================

        log(
            "▶ STEP 6 - Linear Match (L reference)"
        )


        ok, _ = self.run_linear_match(
            callback=log
        )


        if not ok:


            log(
                "❌ LINEAR MATCH FAILED"
            )

            return False, logs




        log(
            "✔ Linear Match done"
        )




        if progress_callback:

            progress_callback(
                1.0
            )




        # ==========================
        # CLEAN
        # ==========================

        log(
            "🧹 STEP 7 - Cleaning temporary folders"
        )


        try:

            self.cleanup()


        except Exception as e:


            log(
                f"⚠ Cleanup failed : {e}"
            )



        log(
            "🎉 LRGB PIPELINE COMPLETE"
        )


        return True, logs