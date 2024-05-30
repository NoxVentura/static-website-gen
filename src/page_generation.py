import os
from pathlib import Path

from block_functions import markdown_to_html_node


def extract_title(markdown):
    line = markdown.split('\n')[0]
    if line.startswith('#'):
        return line[2:]
    raise Exception("Invalid Start of markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as reader:
        markdown = reader.read()

    with open(template_path, "r") as reader:
        template = reader.read()

    htmlnode = markdown_to_html_node(markdown)
    html = htmlnode.to_html()
    title = extract_title(markdown)

    with open(dest_path, "w") as writer:
        writer.write(template.replace("{{ Title }}", title).replace("{{ Content }}", html))


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for listed_dir in os.listdir(dir_path_content):
        updated_source = os.path.join(dir_path_content, listed_dir)
        if os.path.isfile(updated_source):
            if Path(updated_source).suffix == '.md':
                updated_destination = os.path.join(dest_dir_path, f"{Path(updated_source).stem}.html")
                print(f"The file {updated_source} is being converted to html.{updated_destination}")
                generate_page(updated_source, template_path, updated_destination)
        else:
            generate_page_recursive(updated_source, template_path, os.path.join(dest_dir_path, listed_dir))
