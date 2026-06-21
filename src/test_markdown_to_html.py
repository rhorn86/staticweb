import unittest
from markdown_to_html import *
from textwrap import dedent

class TestMDToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = dedent("""\
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = dedent("""\
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        markdown = dedent("""
        ### This is a heading
        """)
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading</h3></div>"
        )

    def test_quote(self):
        md = dedent("""
        > Now I am writing a quote with
        > extra lines to see how that goes.
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Now I am writing a quote with extra lines to see how that goes.</blockquote></div>"
        )

    def test_ulist(self):
        md = dedent("""
        - list item 1
        - list item 2
        - list item 3
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>list item 1</li><li>list item 2</li><li>list item 3</li></ul></div>"
        )

    def test_olist(self):
        md = dedent("""
        1. list item 1
        2. list item 2
        3. list item 3
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>list item 1</li><li>list item 2</li><li>list item 3</li></ol></div>"
        )

    def test_full_document(self):
        md = dedent("""
                    # Header 1

                    ## Header 2

                    This section contains **bold** text as well as _italic_ text.
                    I will also provide a [link](https://archlinux.org) here. Next
                    I will provide an ![image](www.images.com/my_image.png) here.

                    ## Header 3

                    - List items go here
                    - and here too

                    1. And now we have ordered list items here
                    2. and here as well

                    ```
                    This is a code block
                    ```

                    > And now we are
                    > quoting stuff.
                    """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Header 1</h1><h2>Header 2</h2><p>This section contains <b>bold</b> text as well as <i>italic</i> text. I will also provide a <a href=\"https://archlinux.org\">link</a> here. Next I will provide an <img src=\"www.images.com/my_image.png\" alt=\"image\"></img> here.</p><h2>Header 3</h2><ul><li>List items go here</li><li>and here too</li></ul><ol><li>And now we have ordered list items here</li><li>and here as well</li></ol><pre><code>This is a code block\n</code></pre><blockquote>And now we are quoting stuff.</blockquote></div>"
        )
