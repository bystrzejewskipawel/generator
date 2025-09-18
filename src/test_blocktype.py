import unittest

from blocktype import BlockType, block_to_block_type

class TestTextNode(unittest.TestCase):
    def test_heading(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "``` This is a code block ```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_eq(self):
        block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_neq(self):
        block = "> quote line 1\n>> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_numb_list_eq(self):
        block = "1. quote line 1\n2. quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_numb_list_neq(self):
        block = "1. quote line 1\n3. quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)        

if __name__ == "__main__":
    unittest.main()