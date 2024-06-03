import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        node3 = TextNode("This isn't a text node", "italics", "http://virus.com")
        self.assertNotEqual(node, node3)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
