from pathlib import Path
import shutil


def reject_file(file_path, rejected_folder):

    file_path = Path(file_path)

    rejected_folder = Path(
        rejected_folder
    )


    rejected_folder.mkdir(
        parents=True,
        exist_ok=True
    )


    destination = rejected_folder / file_path.name


    shutil.move(
        str(file_path),
        str(destination)
    )


    return destination



def clear_rejected_folder(folder):

    folder = Path(folder)

    if not folder.exists():
        return


    for item in folder.iterdir():

        if item.is_file() or item.is_symlink():

            item.unlink()

        elif item.is_dir():

            shutil.rmtree(item)