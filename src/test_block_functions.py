import unittest
from block_functions import (markdown_to_blocks)

class MyTestCase(unittest.TestCase):
    def test_markdown_to_blocks(self):
        nodes = markdown_to_blocks("""This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items""")
        self.assertListEqual(["This is **bolded** paragraph", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", "* This is a list\n* with items"], nodes)


if __name__ == '__main__':
    unittest.main()
