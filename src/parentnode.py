from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, value=None, props=None):
        super().__init__(tag, value, children, props)
        if self.tag == None:
            raise ValueError("Tag not set")
        if self.children == None:
            raise ValueError("No children")
        
    def to_html(self):
        new_html = ""
        for child in self.children:
            if new_html:
                new_html += child.to_html()
            else:
                new_html = child.to_html()
        if self.tag == "code":
            return f"<pre><{self.tag}>{new_html}</{self.tag}></pre>"
        return f"<{self.tag}>{new_html}</{self.tag}>"
        