from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    import re
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    else:
        num = 1
        for line in lines:
            if not re.match(f"^{num}+\. ", line):
                return BlockType.PARAGRAPH
            num += 1
        return BlockType.ORDERED_LIST