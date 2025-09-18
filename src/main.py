from textnode import TextNode, TextType, text_node_to_html_node
from blocktype import BlockType, block_to_block_type
from htmlnode import LeafNode, ParentNode
import os, shutil
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_from_source_to_dest("static", "docs")
    generate_pages_recursive("content","template.html","docs", basepath)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for f in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, f)
        if os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, f), basepath)
        elif os.path.isfile(full_path) and f.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, f.replace(".md", ".html"))
            generate_page(full_path, template_path, dest_path, basepath)

def copy_from_source_to_dest(source, dest):
    for f in os.listdir(dest):
        if os.path.isdir(os.path.join(dest, f)):
            shutil.rmtree(os.path.join(dest, f))
        elif os.path.isfile(os.path.join(dest, f)):
            os.remove(os.path.join(dest, f))
    for f in os.listdir(source):
        if os.path.isdir(os.path.join(source, f)):
            os.mkdir(os.path.join(dest, f))
            copy_from_source_to_dest(os.path.join(source, f), os.path.join(dest, f))
        elif os.path.isfile(os.path.join(source, f)):
            shutil.copy(os.path.join(source, f), os.path.join(dest, f))

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise ValueError("No title found in markdown")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    html_content = html_node.to_html()
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            content = block.lstrip("#").strip()
            content = text_to_children(content)
            html_nodes.append(ParentNode(f"h{block.count('#')}", children=content))
        elif block_type == BlockType.CODE:
            content = block.strip("`").strip()
            html_nodes.append(LeafNode("pre", f"<code>{content}</code>"))
        elif block_type == BlockType.QUOTE:
            content = "\n".join([line.lstrip("> ").strip() for line in block.split("\n")])
            html_nodes.append(LeafNode("blockquote", content))
        elif block_type == BlockType.ORDERED_LIST:
            items = [line[line.find(".")+1:].strip() for line in block.split("\n")]
            list_items = []
            for item in items:
                children = text_to_children(item)
                list_items.append(ParentNode("li", children=children))
            html_nodes.append(ParentNode("ol", children=list_items))
        elif block_type == BlockType.UNORDERED_LIST:
            items = [line.lstrip("- ").strip() for line in block.split("\n")]
            list_items = []
            for item in items:
                children = text_to_children(item)
                list_items.append(ParentNode("li", children=children))
            html_nodes.append(ParentNode("ul", children=list_items))
        else:
            content = block.strip()
            content = text_to_children(content)
            html_nodes.append(ParentNode("p", children=content))
    return  ParentNode("div", children=html_nodes)

def text_to_children(text):
    nodes = split_markup(text)
    html_nodes = []
    for node in nodes:
        html_node=text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    all_nodes = []
    for old_node in old_nodes:
        new_nodes = []
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(TextNode(old_node.text, old_node.text_type, old_node.url))
            all_nodes.extend(new_nodes)
            continue
        parts = old_node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
        all_nodes.extend(new_nodes)
    return all_nodes

def extract_markdown_images(text):
    import re
    pattern = r"!\[(.+?)\]\((.+?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    import re
    pattern = r"\[(.+?)\]\((.+?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    out_nodes = []
    for old_node in old_nodes:
        new_nodes = []
        images = extract_markdown_images(old_node.text)
        if not images:
            out_nodes.append(old_node)
            continue
        text = old_node.text
        index = 0
        while len(text) > 0:
            part = text[0:text.find(f"![{images[index][0]}]({images[index][1]})") if index < len(images) else len(text)]
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
                text = text.replace(part, "", 1)
            if index < len(images):
                new_nodes.append(TextNode(images[index][0], TextType.IMAGE, images[index][1]))
                text = text.replace(f"![{images[index][0]}]({images[index][1]})", "", 1)
            index += 1
        out_nodes.extend(new_nodes)
    return out_nodes

def split_nodes_link(old_nodes):
    out_nodes = []
    for old_node in old_nodes:
        new_nodes = []
        links = extract_markdown_links(old_node.text)
        if not links:
            out_nodes.append(old_node)
            continue
        text = old_node.text
        index = 0
        while len(text) > 0:
            part = text[0:text.find(f"[{links[index][0]}]({links[index][1]})") if index < len(links) else len(text)]
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
                text = text.replace(part, "", 1)
            if index < len(links):
                new_nodes.append(TextNode(links[index][0], TextType.LINK, links[index][1]))
                text = text.replace(f"[{links[index][0]}]({links[index][1]})", "", 1)
            index += 1
        out_nodes.extend(new_nodes)
    return out_nodes

def split_markup(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        line = line.strip()
        if line:
            blocks.append(line)
    return blocks

if __name__ == "__main__":
    main()