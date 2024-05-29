from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("Invalid Markdown Formatting")
            for i, part in enumerate(parts):
                if part:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, text_type_text))
                    else:
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text):
    match_list = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return match_list


def extract_markdown_links(text):
    match_list = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return match_list


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text or not extract_markdown_images(node.text):
            new_nodes.append(node)
        else:
            found_images = extract_markdown_images(node.text)
            process_text = node.text
            for alt, url in found_images:
                split_text = process_text.split(f"![{alt}]({url})", maxsplit=1)
                first = split_text[0]
                if first:
                    new_nodes.append(TextNode(first, text_type_text))
                new_nodes.append(TextNode(alt, text_type_image, url))
                process_text = split_text[1]
            if process_text:
                new_nodes.append(TextNode(process_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text or not extract_markdown_links(node.text):
            new_nodes.append(node)
        else:
            found_images = extract_markdown_links(node.text)
            process_text = node.text
            for alt, url in found_images:
                split_text = process_text.split(f"[{alt}]({url})", maxsplit=1)
                first = split_text[0]
                if first:
                    new_nodes.append(TextNode(first, text_type_text))
                new_nodes.append(TextNode(alt, text_type_link, url))
                process_text = split_text[1]
            if process_text:
                new_nodes.append(TextNode(process_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
    nodes = split_nodes_delimiter(nodes, '`', text_type_code)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)
