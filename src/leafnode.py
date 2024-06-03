from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None, children=None):
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        htmld = ""
        if self.value == None:
            raise ValueError
        if self.tag:
            htmld = htmld + f"<{self.tag}{self.props_to_html()}>"
        htmld = htmld + self.value
        if self.tag:
            htmld = htmld + f"</{self.tag}>"
        return htmld

    def __repr__(self) -> str:
        return super().__repr__()
    