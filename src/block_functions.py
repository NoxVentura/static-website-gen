import re
from htmlnode import ParentNode
from textnode import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    processed_text = markdown.strip().split('\n\n')
    processed_text = [block.strip() for block in processed_text]
    return processed_text


def block_to_type(block):
    if re.search(r"^#{1,6}\s.+", block):
        return block_type_heading
    elif re.search(r"^```[\s\S]*?^```$", block, re.MULTILINE):
        return block_type_code
    elif re.search(r"^(?:>\s?.*?\n?)+$", block):
        return block_type_quote
    elif re.search(r"^(?:[*\-]\s+.+\n?)+$", block, re.MULTILINE):
        return block_type_unordered_list
    elif re.search(r"^(?:\d+\.\s+.+\n?)+$", block, re.MULTILINE):
        return block_type_ordered_list
    else:
        return block_type_paragraph


def paragraph_to_html_node(block):
    children = [text_to_textnodes(line) for line in block.split("\n")]
    return ParentNode("p", children)


def heading_to_html_node(block):
    hash_count = block.count('#')
    children = [text_to_textnodes(line) for line in block[hash_count:].split("\n")]
    return ParentNode(f"h{hash_count}", children)


def code_to_html_node(block):
    text = block[3:-3]  # Adjusted index to remove triple backticks
    children = text_to_textnodes(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    children = [text_to_textnodes(line[2:]) for line in lines]  # Adjusted index to remove '>'
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = [ParentNode("li", [text_to_textnodes(line[2:])]) for line in lines]  # Adjusted index to remove '*'
    return ParentNode("ul", children)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = [ParentNode("li", [text_to_textnodes(line[3:])]) for line in lines]  # Adjusted index to remove numbers
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
