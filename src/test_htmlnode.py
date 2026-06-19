import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_link(self):
        node = HTMLNode("a", "Click here", props = {"href": "https://archlinux.org"})
        self.assertEqual(node.props_to_html(), " href=\"https://archlinux.org\"")

    def test_p(self):
        ch_node2 = HTMLNode("li", "Hello")
        ch_node = HTMLNode("ul", children = [ch_node2])
        node = HTMLNode("p", "This is paragraph text.", [ch_node])
        self.assertEqual(node.children[0] if node.children is not None else None, ch_node)

    def test_h1(self):
        node = HTMLNode("h1", "This is a heading", props = {"color": "red"})
        self.assertEqual(node.value, "This is a heading")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link", {"href": "https://duckduckgo.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://duckduckgo.com\">Link</a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


