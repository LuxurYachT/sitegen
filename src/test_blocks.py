import unittest

from blocknode import BlockNode
from parentnode import ParentNode
from leafnode import LeafNode
from main import block_to_block_type, markdown_to_block, markdown_to_html_node


class TestBlocks(unittest.TestCase):
    def test_block_typer(self):
        self.assertEqual(BlockNode("This is a quote", "quote"), BlockNode("This is a quote", "quote"))
        self.assertEqual(block_to_block_type(["> This is a quote"]), [BlockNode("This is a quote", "quoteblock")])
        self.assertEqual(block_to_block_type(["### Heading"]), [BlockNode("Heading", "h3")])
        self.assertEqual(block_to_block_type(["```Code```"]), [BlockNode("```Code```", "code")])
        text = """1 thing\n2 stuff\n3 crap"""
        text1 = """thing\nstuff\ncrap"""
        self.assertEqual(block_to_block_type([text]), [BlockNode(text1, "ol")])
        self.assertEqual(block_to_block_type(["Test"]), [BlockNode("Test", "p")])
    
    def test_block_to_node(self):
        text = """## This is a **heading**

        ```this is code```

        > Leonardo"""
        self.assertEqual(block_to_block_type(markdown_to_block(text)), [BlockNode("This is a **heading**", "h2"), BlockNode("```this is code```", "code"), BlockNode("Leonardo", "quoteblock")])


    def test_blocks_to_textnode(self):
        text = """### This heading is text

**This paragraph is bold!**

> *Italic Quote*"""
        self.assertEqual(markdown_to_html_node("Test"), [ParentNode("p", [LeafNode(None, "Test")])])