import re

def extract_title(markdown: str) -> str:
    h1_match = ""
    for line in markdown.splitlines():
        match = re.search(r"^# .*$", line)
        if match:
            h1_match = line
            break
    if h1_match:
        return h1_match[2:]
    else:
        raise Exception("No header found")


