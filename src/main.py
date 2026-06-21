from copy_static import copy_static
from generate_pages_recursive import generate_pages_recursive

def main():

    copy_static("static", "public")

    generate_pages_recursive("content", "template.html", "public")

main()
