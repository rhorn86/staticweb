import os
import shutil

def copy_static(src: str, dest: str):
    if not os.path.exists(src):
        raise Exception(f"Source path {src} does not exist")

    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)
    copy_r(src, dest)

def copy_r(src: str, dest: str):
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dest_path = os.path.join(dest, entry)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_r(src_path, dest_path)

