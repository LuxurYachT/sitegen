import unittest

from main import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnode, markdown_to_block, check_for_heading, block_to_block_type
from textnode import TextNode
from blocknode import BlockNode


class TestSplit(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", "text")
        self.assertEqual(split_nodes_delimiter([node], "`", r"\`.*?\`", "code"), [TextNode("This is text with a ", "text"), TextNode("code block", "code"), TextNode(" word", "text")])
        node1 = TextNode("We test **bold** words", "text")
        self.assertEqual(split_nodes_delimiter([node1], "**", r"\*\*.*?\*\*", "bold"), [TextNode("We test ", "text"), TextNode("bold", "bold"), TextNode(" words", "text"),])
        node2 = TextNode("This *is* rather *tricky*", "text")
        self.assertEqual(split_nodes_delimiter([node2], "*", r"\*.*?\*", "italic"), [
            TextNode("This ", "text"),
            TextNode("is", "italic"), 
            TextNode(" rather ", "text"),
            TextNode("tricky", "italic")
        ])
        self.assertEqual(split_nodes_delimiter([TextNode("This is text with a `code block` word", "text")], "**", r"\*\*.*?\*\*", "bold" ), [TextNode("This is text with a `code block` word", "text")])

    def test_extract_images(self):
        self.assertEqual(extract_markdown_images("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_split_images(self):
        node = [TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", "text")]
        self.assertEqual(split_nodes_image([TextNode("This is an ![image](image.com) of an orange ![image](duck.com)", "text")]), [TextNode("This is an ", "text"), TextNode("image", "image", "image.com"), TextNode(" of an orange ", "text"), TextNode("image", "image", "duck.com")])
     
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode("second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ])


    def test_split_links(self):
        node = [TextNode("This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.com) and another [second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.com)", "text")]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is text with an ", "text"),
            TextNode("image", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.com"),
            TextNode(" and another ", "text"),
            TextNode("second image", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.com"
            ),
        ])


    def test_text_to_nodes(self):
        self.assertEqual(text_to_textnode("Hello world"), [TextNode("Hello world", "text")])
        self.assertEqual(text_to_textnode("That is text with a `code brick` lux"), [TextNode("That is text with a ", "text"), TextNode("code brick", "code"), TextNode(" lux", "text")])
        self.assertEqual(text_to_textnode("This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"),
                         [
    TextNode("This is ", "text"),
    TextNode("text", "bold"),
    TextNode(" with an ", "text"),
    TextNode("italic", "italic"),
    TextNode(" word and a ", "text"),
    TextNode("code block", "code"),
    TextNode(" and an ", "text"),
    TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and a ", "text"),
    TextNode("link", "link", "https://boot.dev"),
])
        self.assertEqual(text_to_textnode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"),
                        [TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode("second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ])

    def test_mark_to_block(self):
        text = """This is a line

        this is another"""
        self.assertEqual(markdown_to_block(text), ["This is a line", "this is another"])
        text1 = """## This is a heading

        ```this is code```

        > Leonardo"""
        self.assertEqual(markdown_to_block(text1), ["## This is a heading", "```this is code```", "> Leonardo"])
    
    def test_check_headings(self):
        self.assertEqual(check_for_heading("## This is a heading"), True)
        self.assertEqual(check_for_heading(" This isn't"), False)
        self.assertEqual(check_for_heading("This is a #"), False)

    def test_block_typer(self):
        ordered_list = "1. First\n2.Second\n3. Third"
        self.assertEqual(block_to_block_type(ordered_list), [BlockNode(ordered_list, "ol")])