import unittest
from extract_title import extract_title
from textwrap import dedent

class TestExtractTitle(unittest.TestCase):
    def test_first_line(self):
        md = dedent("""
                    # Success!

                    ## Blah Blah
                    """)
        header = extract_title(md)
        self.assertEqual(header, "Success!")

    def test_other_line(self):
        md = dedent("""
                    ## Wrong

                    ### Still Wrong

                    # Success!
                    """)
        header = extract_title(md)
        self.assertEqual(header, "Success!")
