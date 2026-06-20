from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(markdown: str) -> BlockType:
    markdown = markdown.strip()
    lines = markdown.split("\n")

    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING

    if re.match(r"^`{3}\n[\s\S]*`{3}$", markdown):
        return BlockType.CODE

    quote_test = True
    for line in lines:
        if not re.match(r"^>", line):
            quote_test = False
            break
    if quote_test:
        return BlockType.QUOTE

    ulist_test = True
    for line in lines:
        if not re.match(r"^- ", line):
            ulist_test = False
            break
    if ulist_test:
        return BlockType.ULIST

    olist_test = True
    for i in range(1, len(lines) + 1):
        if not re.match(rf"^{i}\. ", lines[i-1]):
            olist_test = False
            break
    if olist_test:
        return BlockType.OLIST

    return BlockType.PARAGRAPH

