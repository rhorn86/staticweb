

def markdown_to_blocks(markdown: str) -> list[str]:
    split_blocks = markdown.split("\n\n")
    new_blocks = []
    for block in split_blocks:
        stripped = block.strip()
        if stripped:
            new_blocks.append(stripped)
    return new_blocks
