from splitdelimiter import *
from textnode import TextNode, TextType

def text_to_textnodes(text: str) -> list[TextNode]:
    text_node_from_text = TextNode(text, TextType.TEXT)
    split_images = split_nodes_image([text_node_from_text])
    split_links = split_nodes_link(split_images)
    split_bold = split_nodes_delimiter(split_links, "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    return split_code


