class HTMLNode():

    def __init__(
            self,
            tag: str | None = None,
            value: str | None = None,
            children: list["HTMLNode"] | None = None,
            props: dict[str, str] | None = None
        ) -> None:

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None or self.props == {}:
            return ""
        attribute_str = ""
        for key, value in self.props.items():
            attribute_str += f" {key}=\"{value}\""
        return attribute_str

    def __repr__(self) -> str:
        return f"""<HTMLNode Object>:
            tag: {self.tag}
            value: {self.value}
            children: {self.children!r}
            props: {self.props!r}"""

class LeafNode(HTMLNode):

    def __init__(
            self,
            tag: str | None,
            value: str | None,
            props: dict[str, str] | None = None
        ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"""<LeafNode Object>:
            tag: {self.tag}
            value: {self.value}
            props: {self.props!r}"""

class ParentNode(HTMLNode):

    def __init__(
            self,
            tag: str,
            children: list[HTMLNode],
            props: dict[str, str] | None = None
        ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag value")
        if not self.children:
            raise ValueError("Parent node must have at least one child node")
        inner_elements = ""
        for child in self.children:
            inner_elements += child.to_html()
        if not self.props:
            return f"<{self.tag}>{inner_elements}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{inner_elements}</{self.tag}>"

