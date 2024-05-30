import re
from htmlnode import ParentNode
from textnode import text_to_textnodes, text_node_to_html

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.strip().split('\n\n')
    blocks = [block.strip() for block in blocks]
    return blocks


def block_to_type(block):
    if re.match(r"^#{1,6}\s.*", block):
        return block_type_heading
    elif re.match(r"^```[\s\S]*```$", block, re.MULTILINE):
        return block_type_code
    elif re.match(r"^>\s?.*", block):
        return block_type_quote
    elif re.match(r"^(?:[*\-]\s+.*\n?)+$", block, re.MULTILINE):
        return block_type_unordered_list
    elif re.match(r"^(?:\d+\.\s+.*\n?)+$", block, re.MULTILINE):
        return block_type_ordered_list
    else:
        return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)


def heading_to_html_node(block):
    hash_count = block.count('#')
    text = block[hash_count + 1:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{hash_count}", children)


def code_to_html_node(block):
    text = block[3:-3].strip()
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = [line.lstrip('>').strip() for line in lines]
    text = " ".join(stripped_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line.lstrip("*-").strip()
        item_children = text_to_children(text)
        children.append(ParentNode("li", item_children))
    return ParentNode("ul", children)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = re.sub(r"^\d+\.\s+", "", line).strip()
        item_children = text_to_children(text)
        children.append(ParentNode("li", item_children))
    return ParentNode("ol", children)


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_type(block)
        if block_type == block_type_heading:
            children.append(heading_to_html_node(block))
        elif block_type == block_type_code:
            children.append(code_to_html_node(block))
        elif block_type == block_type_quote:
            children.append(quote_to_html_node(block))
        elif block_type == block_type_unordered_list:
            children.append(unordered_list_to_html_node(block))
        elif block_type == block_type_ordered_list:
            children.append(ordered_list_to_html_node(block))
        else:
            children.append(paragraph_to_html_node(block))
    return ParentNode("div", children)
