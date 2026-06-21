import sys
from copy_static import copy_static
from generate_pages_recursive import generate_pages_recursive

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_static("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
