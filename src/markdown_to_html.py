import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_to_blocks import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from text_to_text_nodes import text_to_textnodes
from textnode import TextNode, TextType

def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                children = text_to_children(block)
                parent_node = ParentNode(tag="p", children=children)
                parent_nodes.append(parent_node)
            case BlockType.HEADING:
                children = text_to_children(block)
                tag = markdown_header_to_html_tag(block)
                parent_node = ParentNode(tag=tag, children=children)
                parent_nodes.append(parent_node)
            case BlockType.QUOTE:
                children = text_to_children(block)
                parent_node = ParentNode(tag="blockquote", children=children)
                parent_nodes.append(parent_node)
            case BlockType.ULIST:
                children = text_to_children(block)
                parent_node = ParentNode(tag="ul", children=children)
                parent_nodes.append(parent_node)
            case BlockType.OLIST:
                children = text_to_children(block)
                parent_node = ParentNode(tag="ol", children=children)
                parent_nodes.append(parent_node)
            case BlockType.CODE:
                text = code_block_to_text(block)
                text_node = TextNode(text, TextType.CODE)
                html_node = textnode_to_htmlnode(text_node)
                parent_node = ParentNode(tag="pre", children=[html_node])
                parent_nodes.append(parent_node)
    root_parent_node = ParentNode(tag="div", children=parent_nodes)
    return root_parent_node

def code_block_to_text(block: str) -> str:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block.removeprefix("```").removesuffix("```")
    if text.startswith("\n"):
        text = text[1:]
    return text


def text_to_children(text: str) -> list[HTMLNode]:
    if block_to_block_type(text) == BlockType.ULIST:
        list_items = text.split("\n")
        parent_nodes = []
        for item in list_items:
            item_text = item[2:]
            text_nodes = text_to_textnodes(item_text)
            html_nodes = []
            for node in text_nodes:
                html_node = textnode_to_htmlnode(node)
                html_nodes.append(html_node)
            parent_node = ParentNode("li", html_nodes)
            parent_nodes.append(parent_node)
        return parent_nodes

    if block_to_block_type(text) == BlockType.OLIST:
        list_items = text.split("\n")
        parent_nodes = []
        for item in list_items:
            item_text = re.sub(r"^\d+\. ", "", item)
            text_nodes = text_to_textnodes(item_text)
            html_nodes = []
            for node in text_nodes:
                html_node = textnode_to_htmlnode(node)
                html_nodes.append(html_node)
            parent_node = ParentNode("li", html_nodes)
            parent_nodes.append(parent_node)
        return parent_nodes

    if block_to_block_type(text) == BlockType.HEADING:
        text = text.strip()
        header_pattern = re.findall(r"^#{1,6} ", text)
        if header_pattern:
            text = text.removeprefix(header_pattern[0])

    if block_to_block_type(text) == BlockType.QUOTE:
        text = text.strip()
        text_lines = text.split("\n")
        new_text_list = []
        for line in text_lines:
            quote_pattern = re.findall(r"^> {0,1}", line)
            if quote_pattern:
                line = line.removeprefix(quote_pattern[0])
                new_text_list.append(line)
        text = " ".join(new_text_list)

    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = textnode_to_htmlnode(node)
        html_nodes.append(html_node)
    return html_nodes

def textnode_to_htmlnode(node: TextNode) -> HTMLNode:
    match node.text_type:
        case TextType.TEXT:
            html_node = LeafNode(tag=None, value=node.text)
            return html_node
        case TextType.BOLD:
            html_node = LeafNode("b", node.text)
            return html_node
        case TextType.ITALIC:
            html_node = LeafNode("i", node.text)
            return html_node
        case TextType.CODE:
            html_node = LeafNode("code", node.text)
            return html_node
        case TextType.LINK:
            if node.url is not None:
                url = {"href": node.url}
            else:
                raise ValueError("LINK TextType requires a URL")
            html_node = LeafNode("a", node.text, url)
            return html_node
        case TextType.IMAGE:
            if node.url is not None:
                url = {"src": node.url, "alt": node.text}
            else:
                raise ValueError("IMAGE TextType requires a URL")
            html_node = LeafNode(tag="img", value="", props=url)
            return html_node
        # case _:
            # raise TypeError("must be a valid TextType")

def markdown_header_to_html_tag(markdown_header: str) -> str:
    header = re.findall(r"^#{1,6} ", markdown_header)
    count = 0
    for char in header[0]:
        if char == "#":
            count += 1
    if 0 < count <= 6:
        return f"h{count}"
    else:
        raise ValueError("invalid header")


