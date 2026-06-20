import unittest
from blocktype import BlockType, block_to_block_type
import re

class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        markdown = """
This text should return a paragraph
block type. We will see how this
goes.
"""
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading(self):
        markdown = "### Heading 3"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_code(self):
        markdown = """
```
x = 5
y = 5

print(x + Y)
```
"""
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        markdown = """
> This is a quote, that continues
> on multiples lines.
"""

        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_ulist(self):
        markdown = """
- one item
- two item
- three item
"""
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_olist(self):
        markdown = """
1. first item
2. second item
3. third item
"""
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.OLIST)


