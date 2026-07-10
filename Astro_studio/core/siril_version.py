import subprocess


def get_siril_version(siril_path):

    try:

        result = subprocess.run(
            [
                siril_path,
                "--version"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )


        output = (
            result.stdout
            +
            result.stderr
        )


        return output.strip()


    except Exception:

        return "Version inconnue"