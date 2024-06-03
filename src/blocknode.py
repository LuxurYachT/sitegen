class BlockNode:
    def __init__(self, block_text, block_type) -> None:
        self.block_text = block_text
        self.block_type = block_type

    def __eq__(node1, node2) -> bool:
        if node1.block_text == node2.block_text and node1.block_type == node2.block_type:
            return True
        else:
            return False        

    def __repr__(self) -> str:
        return repr(f"BlockNode({self.block_text}, {self.block_type})")