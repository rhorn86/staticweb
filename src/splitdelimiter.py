from textnode import TextNode, TextType

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





