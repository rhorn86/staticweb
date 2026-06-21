import os
from markdown_to_html import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/"):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_contents = f.read()
    
    html_node = markdown_to_html_node(markdown_contents)
    content = html_node.to_html()
    title = extract_title(markdown_contents)

    with open(template_path) as ff:
        template = ff.read()

    template_with_title = template.replace("{{ Title }}", title)
    html_document = template_with_title.replace("{{ Content }}", content)
    html_document = html_document.replace("href=\"/", f"href=\"{basepath}")
    html_document = html_document.replace("src=\"/", f"src=\"{basepath}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html_document)
