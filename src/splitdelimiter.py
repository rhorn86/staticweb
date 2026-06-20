from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: TextType
    ) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # example: "Here is `code text` followed by **bold text** followed by _italic text_"
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            if delimiter in old_node.text:
                split_text = old_node.text.split(delimiter)
                if len(split_text) % 2 == 0:
                    raise Exception("unmatched markdown delimiter")
                for i in range(len(split_text)):
                    if i % 2 == 0 and len(split_text[i]) > 0:
                        new_node = TextNode(split_text[i], TextType.TEXT)
                        new_nodes.append(new_node)
                    else: 
                        if len(split_text[i]) > 0:
                            new_node = TextNode(split_text[i], text_type)
                            new_nodes.append(new_node)
            else:
                new_nodes.append(old_node)


    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        remaining_text = old_node.text
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text)
            if not matches and old_node.text:
                new_nodes.append(old_node)
            else:
                for alt_text, url in matches:
                    delimiter = f"![{alt_text}]({url})"
                    split_text = remaining_text.split(delimiter, 1)
                    left = TextNode(split_text[0], TextType.TEXT)
                    center = TextNode(alt_text, TextType.IMAGE, url)
                    if left.text:
                        new_nodes.append(left)
                    new_nodes.append(center)
                    remaining_text = split_text[1]
                right = TextNode(remaining_text, TextType.TEXT)
                if right.text:
                    new_nodes.append(right)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        remaining_text = old_node.text
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text)
            if not matches and old_node.text:
                new_nodes.append(old_node)
            else:
                for anchor_text, url in matches:
                    delimiter = f"[{anchor_text}]({url})"
                    split_text = remaining_text.split(delimiter, 1)
                    left = TextNode(split_text[0], TextType.TEXT)
                    center = TextNode(anchor_text, TextType.LINK, url)
                    if left.text:
                        new_nodes.append(left)
                    new_nodes.append(center)
                    remaining_text = split_text[1]
                right = TextNode(remaining_text, TextType.TEXT)
                if right.text:
                    new_nodes.append(right)
    return new_nodes

