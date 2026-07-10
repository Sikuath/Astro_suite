from pathlib import Path
import shutil


def prepare_sequence(workdir: Path):
    workdir = Path(workdir)

    process_dir = workdir / "process"

    astrom_dir = process_dir / "astrometrie"
    reg_dir = process_dir / "registration"
    linear_dir = process_dir / "linear"
    lum_dir = process_dir / "luminance"

    # =================================================
    # 1. CLEAN TOTAL PIPELINE
    # =================================================
    if process_dir.exists():
        shutil.rmtree(process_dir)

    # =================================================
    # 2. CREATE ALL STAGES
    # =================================================
    astrom_dir.mkdir(parents=True, exist_ok=True)
    reg_dir.mkdir(parents=True, exist_ok=True)
    linear_dir.mkdir(parents=True, exist_ok=True)
    lum_dir.mkdir(parents=True, exist_ok=True)

    # =================================================
    # 3. COPY RAW INPUTS → ASTROMETRY ONLY
    # =================================================
    inputs = ["SII.fit", "HA.fit", "OIII.fit"]

    missing = []

    for fname in inputs:
        src = workdir / fname
        dst = astrom_dir / fname

        if not src.exists():
            missing.append(fname)
            continue

        shutil.copy2(src, dst)

    if missing:
        raise FileNotFoundError(f"[prepare_sequence] Fichiers manquants : {missing}")

    # =================================================
    # 4. RETURN PIPELINE STRUCTURE
    # =================================================
    return {
        "astrometrie": astrom_dir,
        "registration": reg_dir,
        "linear": linear_dir,
        "luminance": lum_dir
    }