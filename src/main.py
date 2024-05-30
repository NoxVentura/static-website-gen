from copy_recursively import copy_dir_recur
from page_generation import generate_page_recursive
import os
import shutil


def main():
    source_path = "./static"
    destination_path = "./public"
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)

    copy_dir_recur(source_path, destination_path)

    generate_page_recursive("content", "template.html", destination_path)

if __name__ == '__main__':
    main()
