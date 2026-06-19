from textnode import TextNode, TextType

def main():

    text_node = TextNode("Here is some text", TextType.LINK, "https://archlinux.org")
    print(text_node)

main()
