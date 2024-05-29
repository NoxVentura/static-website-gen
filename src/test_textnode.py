import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_split_delim(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes,
                         [TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code),
                          TextNode(" word", text_type_text), ])

    # def test_split_delim_not_found(self):
    #     node = TextNode("This text *has *unclosed* delimiters.", text_type_text)
    #     self.assertEqual(split_nodes_delimiter([node], '*', text_type_italic),
    #                      ValueError("Invalid Markdown Formatting"))
    def test_extract_markdown_images(self):
        text = ("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets"
                "/course_assets/zjjcJKZ.png) and ![another]("
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)")
        self.assertListEqual(extract_markdown_images(text), [("image", "https://storage.googleapis.com/qvault-webapp"
                                                                       "-dynamic-assets/course_assets/zjjcJKZ.png"),
                                                             ("another",
                                                              "https://storage.googleapis.com/qvault-webapp-dynamic"
                                                              "-assets/course_assets/dfsdkjfd.png")])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertListEqual(extract_markdown_links(text),
                             [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_empty_old_nodes(self):
        result = split_nodes_image([])
        self.assertEqual(result, [])

    def test_no_images(self):
        node = TextNode("This is a text without any images", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://www.example.com/image.png)", text_type_text)
        expected_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image,
                     "https://www.example.com/image.png")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_nodes)

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image1](https://www.example.com/image1.png) and ![image2]("
            "https://www.example.com/image2.png)",
            text_type_text)
        expected_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image1", text_type_image,
                     "https://www.example.com/image1.png"),
            TextNode(" and ", text_type_text),
            TextNode("image2", text_type_image,
                     "https://www.example.com/image2.png")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_nodes)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image,
                         "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image]("
            "https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("This is a text without links", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_single_link(self):
        node = TextNode(
            "This is a text with a [single link](https://example.com)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is a text with a ", text_type_text),
            TextNode("single link", text_type_link, "https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_links(self):
        node = TextNode("Text with [link1](https://link1.com) and [link2](https://link2.com)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Text with ", text_type_text),
            TextNode("link1", text_type_link, "https://link1.com"),
            TextNode(" and ", text_type_text),
            TextNode("link2", text_type_link, "https://link2.com")
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that "
            "follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link,
                         "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes)

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image]("
            "https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
