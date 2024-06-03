import unittest

from htmlnode import HTMLNode

class testHTMLNode(unittest.TestCase):
    def test_props_output(self):
        node = HTMLNode(None,None,None,{"href":"foo.bar", "target": "_blank"})
        self.assertEqual(node.props_to_html(), f' href="foo.bar" target="_blank"')