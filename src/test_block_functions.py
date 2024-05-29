import unittest
from block_functions import (
    markdown_to_blocks,
    block_to_type,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)
from htmlnode import ParentNode
from textnode import TextNode

class BlockFunctionsTest(unittest.TestCase):
    def test_markdown_to_blocks(self):
        nodes = markdown_to_blocks("""This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items""")
        self.assertListEqual(["This is **bolded** paragraph", "This is another paragraph with *italic* text and "
                                                              "`code` here\nThis is the same paragraph on a new "
                                                              "line", "* This is a list\n* with items"], nodes)

    def test_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_type(block), block_type_heading)

    def test_code(self):
        block = "```\nCode block\n```"
        self.assertEqual(block_type_code, block_to_type(block))

    def test_quote(self):
        block = "> Quote\n> Another line"
        self.assertEqual(block_to_type(block), block_type_quote)

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2"
        self.assertEqual(block_to_type(block), block_type_unordered_list)

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_type(block), block_type_ordered_list)

    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_type(block), block_type_paragraph)

    def test_markdown_to_blocks(self):
        markdown = "# Heading\n\nParagraph\n\n- List item 1\n- List item 2"
        expected_blocks = ["# Heading", "Paragraph", "- List item 1\n- List item 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_block_to_type(self):
        heading_block = "# Heading"
        code_block = "```python\nprint('Hello, World!')\n```"
        quote_block = "> This is a quote"
        unordered_list_block = "- Item 1\n- Item 2"
        ordered_list_block = "1. Item 1\n2. Item 2"
        paragraph_block = "This is a paragraph."

        self.assertEqual(block_to_type(heading_block), block_type_heading)
        self.assertEqual(block_to_type(code_block), block_type_code)
        self.assertEqual(block_to_type(quote_block), block_type_quote)
        self.assertEqual(block_to_type(unordered_list_block), block_type_unordered_list)
        self.assertEqual(block_to_type(ordered_list_block), block_type_ordered_list)
        self.assertEqual(block_to_type(paragraph_block), block_type_paragraph)

if __name__ == '__main__':
    unittest.main()
