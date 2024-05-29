
import re

block_type_paragraph="paragraph"
block_type_heading="heading"
block_type_code="code"
block_type_quote="quote"
block_type_unordered_list="unordered_list"
block_type_ordered_list="ordered_list"

def markdown_to_blocks(markdown):
    processed_text = markdown.strip('')
    processed_text = processed_text.split('\n\n')
    processed_text = [block.strip('') for block in processed_text]
    return processed_text

def block_to_type(block):
