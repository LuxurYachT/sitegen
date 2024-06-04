import re, os, shutil
from textnode import TextNode
from leafnode import LeafNode
from blocknode import BlockNode
from parentnode import ParentNode



def main():
    move_static_to_public(os.path.expanduser("~/workspace/sitegen/static"))
    generate_page(os.path.expanduser("~/workspace/sitegen/content/index.md"), os.path.expanduser("~/workspace/sitegen/template.html"), os.path.expanduser("~/workspace/sitegen/public"))


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    html = create_html(markdown)
    title = extract_title(markdown)
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    target_file_path = os.path.join(dest_path, "index.html")
    with open(target_file_path, "w") as file:
        file.write(new_page)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case "image":
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError("Invalid text type in ", text_node.text," with type ", text_node.text_type)

def split_nodes_delimiter(old_nodes, delimiter, regex, target):
    new_nodes = []
    for node in old_nodes:
        limits = re.findall(regex, node.text)
        if node.text_type != "text":
            new_nodes.append(node)
        elif not limits:
            new_nodes.append(node)
        else:
            working = []
            for i in limits:
                working = node.text.split(f"{i}", 1)
                if working[0] and working[1]:
                    new_node = prepare_text_node(working[0])
                    new_nodes.append(new_node)
                    new_node = TextNode(i.strip(delimiter), target)
                    new_nodes.append(new_node)
                    node.text = working[1]
                if not working[0] and working[1]:
                    new_node = TextNode(i.strip(delimiter), target)
                    new_nodes.append(new_node)
                    node.text = working[1]
                if working[0] and not working[1]:
                    new_node = prepare_text_node(working[0])
                    new_nodes.append(new_node)
                    new_node = TextNode(i.strip(delimiter), target)
                    new_nodes.append(new_node)
                    node.text = ""
                if not working[0] and not working[1]:
                    new_node = TextNode(i.strip(delimiter), target)
                    new_nodes.append(new_node)
                    node.text = ""
            if node.text:
                new_nodes.append(prepare_text_node(node.text))
    return new_nodes


def prepare_text_node(text):
    new_text_type = id_text_type(text)
    new_text = text.strip("*`")
    return TextNode(new_text, new_text_type)


def id_text_type(text):
    if text.startswith("**"):
        return "bold"
    if text.startswith("*"):
        return "italic"
    if text.startswith("`"):
        return "code"
    else:
        return "text"
                    

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if node.text_type != "text":
            new_nodes.append(node)
        elif not images:
            new_nodes.append(node)
        else:
            working = []
            for image_tup in images:
                working = node.text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                if working[0] and working[1]:
                    new_node = TextNode(working[0], "text")
                    new_nodes.append(new_node)
                    new_node = TextNode(image_tup[0], "image", image_tup[1])
                    new_nodes.append(new_node)
                    node.text = working[1]
                if not working[0] and working[1]:
                    new_node = TextNode(image_tup[0], "image", image_tup[1])
                    new_nodes.append(new_node)
                    node.text = working[1]
                if working[0] and not working[1]:
                    new_node = TextNode(working[0], "text")
                    new_nodes.append(new_node)
                    new_node = TextNode(image_tup[0], "image", image_tup[1])
                    new_nodes.append(new_node)
                    node.text = ""
                if not working[0] and not working[1]:
                    new_node = TextNode(image_tup[0], "image", image_tup[1])
                    new_nodes.append(new_node)
                    node.text = ""
            if node.text:
                new_nodes.append(prepare_text_node(node.text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text) 
        if node.text_type != "text":
            new_nodes.append(node)
        elif not links:
            new_nodes.append(node)
        else:
            for link_tup in links:
                working = node.text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                if working[0] and working[1]:
                    new_node = TextNode(working[0], "text")
                    new_nodes.append(new_node)
                    new_node = TextNode(link_tup[0], "link", link_tup[1])
                    new_nodes.append(new_node)
                    node.text = working[1]
                if not working[0] and working[1]:
                    new_node = TextNode(link_tup[0], "link", link_tup[1])
                    new_nodes.append(new_node)
                    node.text = working[1]
                if working[0] and not working[1]:
                    new_node = TextNode(working[0], "text")
                    new_nodes.append(new_node)
                    new_node = TextNode(link_tup[0], "link", link_tup[1])
                    new_nodes.append(new_node)
                    node.text = ""
                if not working[0] and not working[1]:
                    new_node = TextNode(link_tup[0], "link", link_tup[1])
                    new_nodes.append(new_node)
                    node.text = ""
            if node.text:
                new_nodes.append(prepare_text_node(node.text))
    return new_nodes
    

def text_to_textnode(text):
    delimiter_types = {
        "bold":{"lim":"**", "reg":r"\*\*.*?\*\*"},
        "italic":{"lim":"*", "reg":r"\*.*?\*"},
        "code":{"lim":"`", "reg":r"\`.*?\`"}
    }
    node = TextNode(text, "text")
    text_nodes = [node]
    for key in delimiter_types:
        text_nodes = split_nodes_delimiter(text_nodes, delimiter_types[key]["lim"], delimiter_types[key]["reg"], key)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


def markdown_to_block(text):
    blocks = text.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip(" ")
    return blocks


def block_to_block_type(blocks):
    typed_blocks = []
    for block in blocks:
        new_text = ""
        new_type = ""
        if check_for_heading(block):
            new_type = f"h{count_headings(block)}"
            new_text = new_text = block.split(" ", 1)[1]
        elif check_for_codeblock(block):
            new_type = "code"
            new_text = block
        elif check_unordered(block):
            new_type = "ul"
            new_text = strip_multiline(block.split("\n"))
        elif check_ordered(block):
            new_type = "ol"
            new_text = strip_multiline(block.split("\n"))
        elif chcek_for_quote(block):
            new_type = "quoteblock"
            new_text = block.split(" ", 1)[1]
        else:
            new_type = "p"
            new_text = block
        typed_blocks.append(BlockNode(new_text, new_type))
    return typed_blocks

def strip_multiline(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.split(" ", 1)[1])
    return "\n".join(new_lines)

def check_for_heading(block):
    return bool(re.match(r"^#{1,6}\s", block))

def count_headings(text):
    count = 0
    for char in text:
        if char == "#":
            count += 1
        elif char == " ":
            return count
    return count

def check_for_codeblock(block):
    return bool(re.match(r'^(```).*?(```)$', block, re.S))

def chcek_for_quote(block):
    return bool(block.startswith(">"))

def check_unordered(block):
    if bool(block.startswith("* ")):
        return True
    elif bool(block.startswith("- ")):
        return True
    return False

def check_ordered(block):
    lines = block.split("\n")
    if len(lines) > 1:
        if lines[0].startswith("1") and lines[1].startswith("2"):
            return True
    return False


def markdown_to_html_node(markdown):
    blocks = block_to_block_type(markdown_to_block(markdown))
    parent_nodes = []
    for block in blocks:
        parent_nodes.append(block_to_html(block))
    return parent_nodes


def extract_title(markdown):
    lines = markdown.split("\n\n")
    for line in lines:
        if line.startswith("# "):
            return line


def block_to_html(block):
    text_nodes = text_to_textnode(block.block_text)
    leaves = []
    for node in text_nodes:
        leaves.append(text_node_to_html_node(node))
    return ParentNode(block.block_type, leaves)

    
def create_html(markdown):
    htmlnodes = markdown_to_html_node(markdown)
    div = ParentNode("div", htmlnodes)
    return div.to_html()

def move_static_to_public(path, parent_path=""):
    path = os.path.expanduser(path)
    target_base = os.path.expanduser("~/workspace/sitegen/public")
    target_path = os.path.join(target_base, parent_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    dir_contents = os.listdir(path)
    for i in dir_contents:
        item_path = os.path.join(path, i)
        if os.path.isfile(item_path):
            shutil.copy(item_path, target_path)
            os.remove(item_path)
        else:
            move_static_to_public(item_path, os.path.join(parent_path, i))
            shutil.rmtree(item_path)

main()

