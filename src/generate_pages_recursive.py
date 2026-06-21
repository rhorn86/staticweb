import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):

    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")

    if not os.path.exists(dir_path_content):
        raise Exception(f"{dir_path_content} path not found")

    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(src_path) and src_path.endswith(".md"):
            dest_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(src_path, template_path, dest_path)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path)



