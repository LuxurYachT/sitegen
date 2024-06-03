import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class ParentTest(unittest.TestCase):
    def testParent(self):
        node = ParentNode("p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
        node1 = ParentNode("p",[ParentNode("b", [LeafNode("i", "Bold text")])])
    #    self.assertEqual(node1.to_html(), "<p><i><b>Bold text</b></i></p>")