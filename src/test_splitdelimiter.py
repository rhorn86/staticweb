import unittest
from splitdelimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
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

class TestImageSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images2(self):
        node = TextNode(
            "![image](https://i.love.candy.com/candyyy.png) followed by text, then ![another image](www.images.com/this_image.jpg) and more text again",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.love.candy.com/candyyy.png"),
                TextNode(" followed by text, then ", TextType.TEXT),
                TextNode("another image", TextType.IMAGE, "www.images.com/this_image.jpg"),
                TextNode(" and more text again", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.geocities.com) and another [second link](https://www.wikipedia.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.geocities.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.wikipedia.org"),
            ],
            new_nodes,
        )

    def test_split_links2(self):
        node1 = TextNode(
            "This is text with a [link](https://www.geocities.com) and another [second link](https://www.wikipedia.org)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "third link", TextType.LINK, "www.thirdaddress.com"
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.geocities.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.wikipedia.org"),
                TextNode("third link", TextType.LINK, "www.thirdaddress.com"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
