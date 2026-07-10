from pathlib import Path
import subprocess


class SirilRunner:

    def __init__(self, siril_path: str):

        self.siril = Path(siril_path).resolve()

        if not self.siril.exists():
            raise FileNotFoundError(f"Siril introuvable : {self.siril}")

        if self.siril.is_dir():
            raise ValueError("Le chemin Siril pointe vers un dossier")

        # 🔥 safety check : on force CLI si possible
        if "siril-cli" not in self.siril.name.lower():
            print("⚠️ Attention : utilise siril-cli.exe pour un pipeline fiable")

    # -----------------------------
    # RUN SCRIPT
    # -----------------------------
    def run(self, script: Path, workdir: Path, callback=None):

        script = Path(script).resolve()
        workdir = Path(workdir).resolve()

        if not script.exists():
            raise FileNotFoundError(f"Script introuvable : {script}")

        if not workdir.exists():
            raise FileNotFoundError(f"Workdir introuvable : {workdir}")

        # 🔥 commande Siril CLI correcte
        command = [
            str(self.siril),
            "-d", str(workdir),     # dossier de travail Siril
            "-s", str(script),      # script .ssf
        ]

        print("🚀 RUN SIRIL:")
        print("EXE   :", self.siril)
        print("SCRIPT:", script)
        print("DIR   :", workdir)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False
        )

        logs = []
        error_detected = False

        for line in process.stdout:
            line = line.rstrip()
            logs.append(line)

            # 🔥 détection erreur Siril
            if "Erreur" in line or "ERROR" in line:
                error_detected = True

            if callback:
                callback(line)

        process.wait()

        success = process.returncode == 0 and not error_detected

        return success, logs