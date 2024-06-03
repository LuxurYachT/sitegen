import unittest

from leafnode import LeafNode


class TestLeaf(unittest.TestCase):
    def test_leaf_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node1 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node1.to_html(), '<p>This is a paragraph of text.</p>')