from pathlib import Path
import subprocess


class SirilRunner:

    def __init__(self, siril_path: str):

        # 🔥 IMPORTANT : on force le fichier exact
        self.siril = Path(siril_path).resolve()

        if not self.siril.exists():
            raise FileNotFoundError(f"Siril introuvable : {self.siril}")

        if self.siril.is_dir():
            raise ValueError(
                f"Le chemin Siril pointe vers un dossier, pas un exe : {self.siril}"
            )

    def run(self, script: Path, workdir: Path, callback=None):

        script = Path(script).resolve()
        workdir = Path(workdir).resolve()

        if not script.exists():
            raise FileNotFoundError(f"Script introuvable : {script}")

        if not workdir.exists():
            raise FileNotFoundError(f"Workdir introuvable : {workdir}")

        # 🔥 DEBUG ULTRA IMPORTANT
        print("SIRIL EXE:", self.siril)
        print("SCRIPT:", script)
        print("WORKDIR:", workdir)

        # ✔ commande directe sans cmd / shell
        command = [
            str(self.siril),   # 👈 DOIT être le .exe
            "-d", str(workdir),
            "-s", str(script),
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(workdir),
            shell=False
        )

        logs = []

        for line in process.stdout:
            line = line.rstrip()
            logs.append(line)

            if callback:
                callback(line)

        process.wait()

        return process.returncode == 0, logs