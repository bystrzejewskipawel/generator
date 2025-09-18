import unittest

from main import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_delimiter, split_nodes_link, split_markup, markdown_to_blocks, markdown_to_html_node
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
#     def test_extract_markdown_images(self):
#         matches = extract_markdown_images(
#             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
#         )
#         self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

#     def test_extract_markdown_links(self):
#         matches = extract_markdown_links(
#             "This is text with an [link](https://google.com)"
#         )
#         self.assertListEqual([("link", "https://google.com")], matches)

#     def test_split_nodes(self):
#         node = TextNode("This is text with a `code block` word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#         self.assertEqual(new_nodes, [
#             TextNode("This is text with a ", TextType.TEXT),
#             TextNode("code block", TextType.CODE),
#             TextNode(" word", TextType.TEXT),
#         ])

#     def test_split_images(self):
#         node = TextNode(
#             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#             TextType.TEXT,
#         )
#         new_nodes = split_nodes_image([node])
#         self.assertListEqual(
#             [
#                 TextNode("This is text with an ", TextType.TEXT),
#                 TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
#                 TextNode(" and another ", TextType.TEXT),
#                 TextNode(
#                     "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
#                 ),
#             ],
#             new_nodes,
#         )

#     def test_split_links(self):
#         node = TextNode(
#             "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
#             TextType.TEXT,
#         )
#         new_nodes = split_nodes_link([node])
#         self.assertListEqual(
#             [
#                 TextNode("This is text with an ", TextType.TEXT),
#                 TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
#                 TextNode(" and another ", TextType.TEXT),
#                 TextNode(
#                     "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
#                 ),
#             ],
#             new_nodes,
#         )

#     def test_split_markup(self):
#         text = r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#         new_nodes = [
#             TextNode("This is ", TextType.TEXT),
#             TextNode("text", TextType.BOLD),
#             TextNode(" with an ", TextType.TEXT),
#             TextNode("italic", TextType.ITALIC),
#             TextNode(" word and a ", TextType.TEXT),
#             TextNode("code block", TextType.CODE),
#             TextNode(" and an ", TextType.TEXT),
#             TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
#             TextNode(" and a ", TextType.TEXT),
#             TextNode("link", TextType.LINK, "https://boot.dev"),
#         ]
#         self.assertListEqual(
#             split_markup(text),
#             new_nodes,
#         )

#     def test_markdown_to_blocks(self):
#         md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items
# """
#         blocks = markdown_to_blocks(md)
#         self.assertEqual(
#             blocks,
#             [
#                 "This is **bolded** paragraph",
#                 "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
#                 "- This is a list\n- with items",
#             ],
#         )

#     def test_paragraphs(self):
#         md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """

#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
#         )

#     def test_codeblock(self):
#         md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """

#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
#         )

#     def test_generate_page(self):
#         from main import generate_page
#         generate_page("content/index.md", "template.html", "public/index.html")
#         with open("public/index.html", "r") as f:
#             final_html = f.read()
#         self.assertIn("<!DOCTYPE html>", final_html)
#         self.assertIn("<title>My Static Site</title>", final_html)
#         self.assertIn("<h1>Welcome to My Static Site</h1>", final_html)
#         self.assertIn("<p>This is a simple static site generated from Markdown files.</p>", final_html)
#         self.assertIn('<img src="https://i.imgur.com/zjjcJKZ.png" alt="Sample Image">', final_html)
#         self.assertIn('<a href="https://boot.dev">boot.dev</a>', final_html)

    def test_list(self):
        md = """
1. This is **bolded** paragraph
2. this is _italic_ text
3. This is normal text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bolded</b> paragraph</li><li>this is <i>italic</i> text</li><li>This is normal text</li></ol></div>",
        )

    def test_quote(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size."\n\n-- J.R.R. Tolkien</blockquote></div>',
        )

if __name__ == "__main__":
    unittest.main()