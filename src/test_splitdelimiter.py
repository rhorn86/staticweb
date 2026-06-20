import unittest
from splitdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestDelimiter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This node is only text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This node is only text")
        self.assertEqual(len(new_nodes), 1)

    def test_code(self):
        node = TextNode("Text `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[2].text, " text")

    def test_bold(self):
        node = TextNode("Text **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " text")

    def test_italic(self):
        node = TextNode("Text _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[2].text, " text")

    def test_two_nodes(self):
        node1 = TextNode("`val height = 7`", TextType.CODE)
        node2 = TextNode("Some **bold** and _italic_ text", TextType.TEXT)
        old_nodes = [node1, node2]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "`val height = 7`")
        self.assertEqual(new_nodes[1].text, "Some **bold** and ")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "italic")
        self.assertEqual(new_nodes[2].text_type, TextType.ITALIC)

    def test_two_inlines(self):
        node = TextNode("Text **bold** more text **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[3].text, "more bold")

    def test_unmatched_delimiter(self):
        node = TextNode("Text `code text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
