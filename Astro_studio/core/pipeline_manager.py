from pathlib import Path
import shutil

from core.pipeline_guard import PipelineGuard
from core.siril_runner import SirilRunner
from core.prepare_sequence import prepare_sequence


class PipelineManager:

    def __init__(self, workdir: str, siril_path: str):

        self.workdir = Path(workdir)

        self.guard = PipelineGuard(self.workdir)
        self.runner = SirilRunner(siril_path)

        # Scripts Siril
        self.step1_script = Path("scripts/01_astrometry.ssf")
        self.step2_script = Path("scripts/02_registration.ssf")
        self.step3_script = Path("scripts/03_linear_match.ssf")


    # =========================================================
    # CALLBACK SAFE
    # =========================================================

    def _safe_callback(self, callback):

        def wrapper(line):

            if callback:
                callback(line)

        return wrapper



    # =========================================================
    # PREPARE
    # =========================================================

    def prepare(self):

        self.guard.check_workdir()

        structure = prepare_sequence(self.workdir)

        self.guard.check_inputs()

        return structure



    # =========================================================
    # RUN SIRIL
    # =========================================================

    def run_astrometry(self, callback=None):

        return self.runner.run(
            script=self.step1_script,
            workdir=self.workdir,
            callback=self._safe_callback(callback)
        )


    def run_registration(self, callback=None):

        return self.runner.run(
            script=self.step2_script,
            workdir=self.workdir,
            callback=self._safe_callback(callback)
        )


    def run_linear_match(self, callback=None):

        return self.runner.run(
            script=self.step3_script,
            workdir=self.workdir,
            callback=self._safe_callback(callback)
        )



    # =========================================================
    # COPY FILES
    # =========================================================

    def copy_files(self, src_dir, dst_dir, files):

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
    # CLEANUP
    # =========================================================
    def cleanup(self):

        process_dir = self.workdir / "process"

        if process_dir.exists():
            shutil.rmtree(process_dir)

        print("Temporary process directory removed.")

    # =========================================================
    # STEP 0
    # COPY ORIGINAL FILES -> ASTROMETRIE
    # =========================================================

    def copy_inputs_to_astrometry(self):

        source = self.workdir


        destination = (
            self.workdir
            / "process"
            / "astrometrie"
        )


        self.copy_files(

            source,

            destination,

            [
                "HA.fit",
                "OIII.fit",
                "SII.fit"
            ]

        )



    # =========================================================
    # STEP 4
    # READ colors_conversion.txt
    #
    # Exemple :
    #
    # HA_astrom.fit   -> process/colors_00001.fit
    # OIII_astrom.fit -> process/colors_00002.fit
    # SII_astrom.fit  -> process/colors_00003.fit
    #
    # Retour :
    #
    # {
    #   "00001":"HA.fit",
    #   "00002":"OIII.fit",
    #   "00003":"SII.fit"
    # }
    #
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


        with open(txt, "r", encoding="utf-8") as file:


            for line in file:


                if "->" not in line:
                    continue


                left, right = line.split("->")


                left = left.strip()
                right = right.strip()


                # colors_00001.fit

                number = (
                    Path(right)
                    .stem
                    .split("_")[-1]
                )


                # HA_astrom.fit

                channel = (

                    Path(left)
                    .stem
                    .replace("_astrom", "")
                    .strip()

                )


                mapping[number] = channel + ".fit"


        return mapping



    # =========================================================
    # STEP 4
    # RENAME r_colors -> CHANNEL
    # DANS registration/process
    # =========================================================

    def rename_registered_files(self, mapping):


        reg_dir = (

            self.workdir
            / "process"
            / "registration"
            / "process"

        )


        for number, channel in mapping.items():


            src = (
                reg_dir
                / f"r_colors_{number}.fit"
            )


            dst = (
                reg_dir
                / channel
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
    # FULL PIPELINE
    # =========================================================

    def run_full(self, callback=None, progress_callback=None):


        logs = []


        def log(msg):

            logs.append(msg)

            if callback:
                callback(msg)



        # =====================================================
        # PREPARE
        # =====================================================

        log(
            "🧹 Preparing pipeline workspace..."
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



        # =====================================================
        # STEP 0
        # =====================================================

        log(
            "📂 STEP 0 - Copy inputs → astrometrie"
        )


        try:

            self.copy_inputs_to_astrometry()


        except Exception as e:

            log(
                f"❌ COPY INPUT FAILED : {e}"
            )

            return False, logs



        log(
            "✔ Inputs copied"
        )



        # =====================================================
        # STEP 1 ASTROMETRY
        # =====================================================

        log(
            "▶ STEP 1 - Astrometry"
        )


        ok, _ = self.run_astrometry(
            callback=log
        )


        if not ok:

            log(
                "❌ STEP 1 FAILED"
            )

            return False, logs



        log(
            "✔ STEP 1 done"
        )



        # =====================================================
        # STEP 2 COPY ASTROM -> REGISTRATION
        # =====================================================

        log(
            "📂 STEP 2 - Copy astrom → registration"
        )


        try:


            self.copy_files(

                self.workdir
                / "process"
                / "astrometrie",

                self.workdir
                / "process"
                / "registration",

                [
                    "HA_astrom.fit",
                    "OIII_astrom.fit",
                    "SII_astrom.fit"
                ]

            )


        except Exception as e:


            log(
                f"❌ COPY ASTROM FAILED : {e}"
            )

            return False, logs



        log(
            "✔ Copy astrom done"
        )



        # =====================================================
        # STEP 3 REGISTRATION
        # =====================================================

        log(
            "▶ STEP 3 - Registration"
        )


        ok, _ = self.run_registration(
            callback=log
        )


        if not ok:

            log(
                "❌ STEP 3 FAILED"
            )

            return False, logs



        log(
            "✔ STEP 3 done"
        )



        # =====================================================
        # STEP 4 RENAME
        # =====================================================

        log(
            "🏷️ STEP 4 - Rename using colors_conversion.txt"
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



        log(
            "✔ Rename done"
        )



        # =====================================================
        # STEP 5 COPY TO LINEAR
        # =====================================================

        log(
            "📂 STEP 5 - Copy channels → linear"
        )


        try:


            self.copy_files(

                self.workdir
                / "process"
                / "registration"
                / "process",

                self.workdir
                / "process"
                / "linear",

                [
                    "HA.fit",
                    "OIII.fit",
                    "SII.fit"
                ]

            )


        except Exception as e:


            log(
                f"❌ COPY LINEAR FAILED : {e}"
            )

            return False, logs



        log(
            "✔ Linear files ready"
        )



        # =====================================================
        # STEP 6 LINEAR MATCH
        # =====================================================

        log(
            "▶ STEP 6 - Linear Match (HA reference)"
        )


        ok, _ = self.run_linear_match(
            callback=log
        )


        if not ok:

            log(
                "❌ STEP 6 FAILED"
            )

            return False, logs



        log(
            "✔ STEP 6 done"
        )



        if progress_callback:

            progress_callback(1.0)

        # =====================================================
        # STEP 7 - CLEANUP
        # =====================================================
        log("🧹 STEP 7 - Cleaning temporary files")

        try:
            self.cleanup()
        except Exception as e:
            log(f"⚠ Cleanup failed: {e}")

        log("✔ Cleanup done")

        # =====================================================
        # END
        # =====================================================
        log("🎉 PIPELINE COMPLETE")

        return True, logs