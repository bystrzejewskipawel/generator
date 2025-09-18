import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("div", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(str(node), "HTMLNode(tag=div, value=None, children=[], props={'class': 'my-class', 'id': 'my-id'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # def test_neq(self):
    #     node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
    #     node2 = TextNode("This is a text node", TextType.BOLD)
    #     self.assertNotEqual(node, node2)

    # def test_eq2(self):
    #     node = TextNode("This is a text node", TextType.BOLD, None)
    #     node2 = TextNode("This is a text node", TextType.BOLD)
    #     self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()