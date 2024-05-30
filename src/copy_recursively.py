import os
import shutil


def copy_dir_recur(source_path, destination_path):
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    for listed_dir in os.listdir(source_path):
        updated_source = os.path.join(source_path, listed_dir)
        updated_destination = os.path.join(destination_path, listed_dir)
        if os.path.isfile(updated_source):
            print(f"Copying {updated_source} to {updated_destination} ")
            shutil.copy(updated_source, updated_destination)
        else:
            copy_dir_recur(updated_source, updated_destination)
