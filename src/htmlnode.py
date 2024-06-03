class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        htmld = ""
        if self.props == None:
            return ""
        for prop in self.props:
            htmld = htmld + f' {prop}="{self.props[prop]}"'
        return htmld
    
    def __eq__(node1, node2) -> bool:
        if node1.tag == node2.tag and node1.value == node2.value and node1.children == node2.children and node1.props == node2.props:
            return True
        else:
            return False    
    
    def __repr__(self) -> str:
        return repr(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")