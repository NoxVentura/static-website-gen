import unittest
from htmlnode import HtmlNode, LeafNode


class TestHtmlLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HtmlNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
    
    def test_to_html_no_children(self):
        node = LeafNode("p","Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
